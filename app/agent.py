"""
app/agent.py
AI brain with multilingual support.

Flow:
1. Detect language of complaint
2. Translate to English if needed
3. Query RAG for relevant policy
4. Look up order
5. Send to Groq LLM for decision
6. Translate email back to customer's language
7. Send email to customer
"""

import os
import re
import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from rag.query import query_policy
from app.translator import (
    detect_language,
    translate_to_english,
    translate_email,
    get_language_name
)

load_dotenv()


# ── Load orders ───────────────────────────────────────────────────────
def load_orders() -> list:
    orders_path = os.path.join("data", "orders.json")
    with open(orders_path, "r") as f:
        return json.load(f)


def get_order_by_id(order_id: str) -> dict:
    orders = load_orders()
    for order in orders:
        if order["order_id"] == order_id:
            return order
    return None


# ── LLM ───────────────────────────────────────────────────────────────
def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
        max_tokens=1024,
    )


# ── Prompt ────────────────────────────────────────────────────────────
DECISION_PROMPT = PromptTemplate.from_template("""
You are an expert e-commerce customer support agent for an Indian e-commerce platform.
Resolve customer complaints fairly based on company policy.

CUSTOMER COMPLAINT:
{complaint}

ORDER DETAILS:
{order_details}

RELEVANT POLICY SECTIONS:
{policy_chunks}

DECISION RULES:
1. Product damaged or defective + delivered within 10 days = REPLACE
2. Customer wants refund + delivered within 10 days = REFUND
3. Order value above Rs 50000 = ESCALATE
4. Product not delivered yet = ESCALATE
5. Beyond 30 days since delivery = ESCALATE
6. Order not found = ESCALATE
7. Complaint unclear = ESCALATE

IMPORTANT: You MUST return ONLY a JSON object. No explanation before or after.
No markdown. No code blocks. Just the raw JSON object starting with {{ and ending with }}.

{{
  "decision": "REPLACE",
  "reason": "explain why based on policy and order details",
  "confidence": 0.85,
  "policy_reference": "policy section used",
  "email_subject": "short email subject",
  "email_body": "full professional email to customer with next steps"
}}

Replace the values above with your actual decision. Return ONLY the JSON.
""")


# ── Main resolve function ─────────────────────────────────────────────
def resolve_complaint(complaint: str, order_id: str = None) -> dict:
    """
    Resolves a complaint in any language.
    Returns structured decision with email in customer's language.
    """
    print(f"\n{'='*60}")
    print(f"Processing complaint...")

    # Step 1 — Detect language
    lang_code = detect_language(complaint)
    lang_name = get_language_name(lang_code)
    print(f"🌐 Language detected: {lang_name} ({lang_code})")

    # Step 2 — Translate to English for RAG
    if lang_code != "en":
        complaint_english = translate_to_english(complaint, lang_code)
        print(f"🔄 Translated: {complaint_english[:100]}...")
    else:
        complaint_english = complaint

    # Step 3 — Get order details
    order_details = "No order ID provided."
    order = None
    if order_id:
        order = get_order_by_id(order_id)
        if order:
            order_details = f"""
Order ID:             {order['order_id']}
Customer:             {order['customer_name']}
Product:              {order['product_name']}
Category:             {order['category']}
Order Value:          Rs {order['order_value']}
Company:              {order['company']}
Is Delivered:         {order['is_delivered']}
Days Since Delivery:  {order['days_since_delivery']}
Payment Method:       {order['payment_method']}
"""
            print(f"✅ Order found: {order['product_name']}")
        else:
            order_details = f"Order {order_id} not found."
            print(f"❌ Order not found")

    # Step 4 — RAG query
        # Step 4 — RAG query filtered by company
        print(f"🔍 Querying policy database...")

        # Get company from order if available
        order_company = None
        if order and order.get("company"):
            order_company = order["company"]
            print(f"   Filtering by company: {order_company}")

        rag_results = query_policy(complaint_english, n_results=3, company=order_company)
        policy_chunks = ""
        for i, (doc, meta) in enumerate(zip(
                rag_results["documents"][0],
                rag_results["metadatas"][0]
        )):
            policy_chunks += f"\n[Policy {i + 1} from {meta['source']}]\n{doc}\n"
    # Step 5 — Call LLM
    print(f"🤖 Calling Groq LLM...")
    llm    = get_llm()
    prompt = DECISION_PROMPT.format(
        complaint     = complaint_english,
        order_details = order_details,
        policy_chunks = policy_chunks,
    )

    response = llm.invoke(prompt)
    raw      = response.content.strip()
    print(f"🔍 Raw LLM response: {raw[:300]}")

    # Step 6 — Parse JSON response
    try:
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            raw = json_match.group()

        result = json.loads(raw)

        if "decision" not in result:
            raise ValueError("No decision in response")
        if result["decision"] not in ["REFUND", "REPLACE", "ESCALATE"]:
            result["decision"] = "ESCALATE"

    except Exception as e:
        print(f"⚠️ Parse error: {e}")
        result = {
            "decision":         "ESCALATE",
            "reason":           "System could not process automatically. Escalating to human agent.",
            "confidence":       0.0,
            "policy_reference": "N/A",
            "email_subject":    "Your complaint has been received",
            "email_body":       f"Dear Customer,\n\nThank you for contacting us. Your complaint has been forwarded to our senior support team who will contact you within 24 hours.\n\nOrder ID: {order_id or 'N/A'}\n\nRegards,\nSupport Team",
        }

    # Step 7 — Translate email back to customer's language
    # THIS IS OUTSIDE THE TRY/EXCEPT — always runs
    if lang_code != "en":
        print(f"🔄 Translating email back to {lang_name}...")
        result["email_body"]    = translate_email(result.get("email_body", ""), lang_code)
        result["email_subject"] = translate_email(result.get("email_subject", ""), lang_code)

    # Step 8 — Add language info
    result["language_detected"]  = lang_code
    result["language_name"]      = lang_name
    result["original_complaint"] = complaint
    result["english_complaint"]  = complaint_english

    # Step 9 — Send email to customer
    result["email_sent"]   = False
    result["email_status"] = "No customer email found"

    if order and order.get("customer_email"):
        from app.email_sender import send_email
        email_result = send_email(
            to_email      = order["customer_email"],
            subject       = result.get("email_subject", "Update on your complaint"),
            body          = result.get("email_body", ""),
            customer_name = order.get("customer_name", "Customer")
        )
        result["email_sent"]   = email_result["success"]
        result["email_status"] = email_result["message"]

    print(f"✅ Final Decision: {result['decision']} (confidence: {result.get('confidence', 0)})")
    return result


# ── Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("TEST 1 — Hindi complaint")
    result = resolve_complaint(
        complaint="मुझे मेरा Apple iPhone 14 मिला लेकिन स्क्रीन टूटी हुई है। मुझे replacement चाहिए।",
        order_id="ORD-6643"
    )
    if result:
        print(f"Decision:   {result.get('decision')}")
        print(f"Language:   {result.get('language_name')}")
        print(f"Confidence: {result.get('confidence')}")

    print("\nTEST 2 — Tamil complaint")
    result = resolve_complaint(
        complaint="என் தயாரிப்பு சேதமடைந்தது. எனக்கு பணம் திரும்ப வேண்டும்.",
        order_id="ORD-7911"
    )
    if result:
        print(f"Decision:   {result.get('decision')}")
        print(f"Language:   {result.get('language_name')}")
        print(f"Confidence: {result.get('confidence')}")

    print("\nTEST 3 — English complaint")
    result = resolve_complaint(
        complaint="My ceiling fan stopped working after 2 days. Not acceptable.",
        order_id="ORD-5319"
    )
    if result:
        print(f"Decision:   {result.get('decision')}")
        print(f"Language:   {result.get('language_name')}")
        print(f"Confidence: {result.get('confidence')}")