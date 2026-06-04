"""
app/agent.py
The AI brain of the complaint resolution system.

Flow:
1. Receive complaint + order_id
2. Query RAG for relevant policy chunks
3. Look up order from orders.json
4. Send everything to Groq LLM
5. Get structured decision back
"""

import os
import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from rag.query import query_policy

load_dotenv()

# ── Load orders from JSON ─────────────────────────────────────────────
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


# ── Load Groq LLM ─────────────────────────────────────────────────────
def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
        max_tokens=1024,
    )


# ── Main decision prompt ──────────────────────────────────────────────
DECISION_PROMPT = PromptTemplate.from_template("""
You are an expert e-commerce customer support agent for an Indian e-commerce platform.
Your job is to resolve customer complaints fairly based on company policy.

CUSTOMER COMPLAINT:
{complaint}

ORDER DETAILS:
{order_details}

RELEVANT POLICY SECTIONS:
{policy_chunks}

Based on the complaint, order details, and policy sections above, make a decision.

Rules:
- If product is damaged or defective and within return window → REPLACE
- If customer wants refund and is within return window → REFUND  
- If order value is above Rs 50000 → ESCALATE to senior team
- If complaint is unclear or policy does not cover the situation → ESCALATE
- If beyond return window → ESCALATE
- If order not found → ESCALATE

You MUST respond in this exact JSON format only, nothing else:
{{
  "decision": "REFUND" or "REPLACE" or "ESCALATE",
  "reason": "clear explanation of why this decision was made based on policy",
  "confidence": 0.0 to 1.0,
  "policy_reference": "which policy section supports this decision",
  "email_subject": "subject line for customer email",
  "email_body": "full polite professional email to customer in English explaining the decision and next steps"
}}
""")


# ── Resolve a complaint ───────────────────────────────────────────────
def resolve_complaint(complaint: str, order_id: str = None) -> dict:
    """
    Main function that resolves a complaint.
    Returns structured decision dict.
    """

    print(f"\n{'='*60}")
    print(f"Processing complaint...")
    print(f"Complaint: {complaint[:100]}...")

    # Step 1 — Get order details
    order_details = "No order ID provided."
    if order_id:
        order = get_order_by_id(order_id)
        if order:
            order_details = f"""
Order ID:         {order['order_id']}
Customer:         {order['customer_name']}
Product:          {order['product_name']}
Category:         {order['category']}
Order Value:      Rs {order['order_value']}
Company:          {order['company']}
Is Delivered:     {order['is_delivered']}
Days Since Delivery: {order['days_since_delivery']}
Payment Method:   {order['payment_method']}
"""
            print(f"✅ Order found: {order['product_name']}")
        else:
            order_details = f"Order ID {order_id} not found in system."
            print(f"❌ Order {order_id} not found")

    # Step 2 — Query RAG for relevant policy
    print(f"🔍 Querying policy database...")
    rag_results = query_policy(complaint, n_results=3)

    policy_chunks = ""
    for i, (doc, meta) in enumerate(zip(
        rag_results["documents"][0],
        rag_results["metadatas"][0]
    )):
        policy_chunks += f"\n[Policy {i+1} from {meta['source']}]\n{doc}\n"

    # Step 3 — Build prompt and call LLM
    print(f"🤖 Calling Groq LLM...")
    llm    = get_llm()
    prompt = DECISION_PROMPT.format(
        complaint     = complaint,
        order_details = order_details,
        policy_chunks = policy_chunks,
    )

    response = llm.invoke(prompt)
    raw      = response.content.strip()

    # Step 4 — Parse JSON response
    try:
        # Clean up response if LLM adds extra text
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        result = json.loads(raw)
        print(f"✅ Decision: {result['decision']} (confidence: {result['confidence']})")
        return result

    except json.JSONDecodeError:
        print(f"⚠️  Could not parse LLM response, escalating")
        return {
            "decision":         "ESCALATE",
            "reason":           "System could not process complaint automatically",
            "confidence":       0.0,
            "policy_reference": "N/A",
            "email_subject":    "Your complaint has been received",
            "email_body":       f"Dear Customer,\n\nThank you for reaching out. Your complaint has been forwarded to our senior support team who will contact you within 24 hours.\n\nOrder ID: {order_id}\n\nRegards,\nSupport Team"
        }


# ── Test it ───────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("TEST 1 — Damaged product")
    result = resolve_complaint(
        complaint="I received my boAt Airdopes and one earbud is not working at all. It is clearly defective. I want a replacement.",
        order_id="ORD-1003"
    )
    print(json.dumps(result, indent=2))

    print("\nTEST 2 — Refund request")
    result = resolve_complaint(
        complaint="The jeans I ordered are of very poor quality. I am not happy. I want my money back.",
        order_id="ORD-1002"
    )
    print(json.dumps(result, indent=2))

    print("\nTEST 3 — High value order")
    result = resolve_complaint(
        complaint="My HP Laptop stopped working after 2 days. This is unacceptable for a Rs 54990 product.",
        order_id="ORD-1007"
    )
    print(json.dumps(result, indent=2))