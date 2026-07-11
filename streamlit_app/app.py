"""
streamlit_app/app.py
Professional SaaS-style UI
Blue corporate theme with modern cards and gradients
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import login, signup, create_default_admin
from app.db import create_tables

st.set_page_config(
    page_title="ResolveAI — Complaint Resolution",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f1729 0%, #1a2744 50%, #0f1729 100%);
    min-height: 100vh;
}

/* Main container */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ── Cards ── */
.card {
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

.card-blue {
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    border: none;
    border-radius: 16px;
    padding: 1.5rem;
    color: white;
}

.card-green {
    background: linear-gradient(135deg, #065f46, #10b981);
    border: none;
    border-radius: 16px;
    padding: 1.2rem;
    color: white;
}

.card-orange {
    background: linear-gradient(135deg, #92400e, #f59e0b);
    border: none;
    border-radius: 16px;
    padding: 1.2rem;
    color: white;
}

.card-red {
    background: linear-gradient(135deg, #7f1d1d, #ef4444);
    border: none;
    border-radius: 16px;
    padding: 1.2rem;
    color: white;
}

/* ── Logo / Header ── */
.logo-text {
    font-size: 28px;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.tagline {
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    margin-top: -4px;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}

.metric-value {
    font-size: 38px;
    font-weight: 700;
    color: #60a5fa;
    line-height: 1;
}

.metric-label {
    font-size: 14px;
    color: rgba(255,255,255,0.5);
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Decision badges ── */
.badge-replace {
    display: inline-block;
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

.badge-refund {
    display: inline-block;
    background: linear-gradient(135deg, #065f46, #10b981);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

.badge-escalate {
    display: inline-block;
    background: linear-gradient(135deg, #92400e, #f59e0b);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
    padding: 0.6rem 1rem !important;
}

.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
    padding: 0.6rem 2rem !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
}

.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: rgba(255,255,255,0.6) !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* ── Text colors ── */
p, label, .stMarkdown {
    color: rgba(255,255,255,0.85) !important;
}

h1, h2, h3, h4 {
    color: white !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

[data-testid="metric-container"] label {
    color: rgba(255,255,255,0.5) !important;
    font-size: 12px !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #60a5fa !important;
    font-weight: 700 !important;
}

/* ── Success/Error/Info ── */
.stSuccess {
    background: rgba(16, 185, 129, 0.15) !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 10px !important;
    color: #34d399 !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 10px !important;
}

.stInfo {
    background: rgba(59, 130, 246, 0.15) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px !important;
    color: #93c5fd !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.15) !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 10px !important;
    color: #fcd34d !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #3b82f6 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }

/* ── Login card ── */
.login-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2.5rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
}

/* ── Nav bar ── */
.navbar {
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(145deg, rgba(37,99,235,0.2), rgba(124,58,237,0.1));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
}

/* ── Complaint item ── */
.complaint-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: all 0.2s;
}

.complaint-item:hover {
    background: rgba(255,255,255,0.07);
    border-color: rgba(99,102,241,0.3);
}
</style>
""", unsafe_allow_html=True)

# ── Initialize ────────────────────────────────────────────────────────
create_tables()
create_default_admin()

if "user" not in st.session_state:
    st.session_state.user = None
if "result" not in st.session_state:
    st.session_state.result = None


def logout():
    st.session_state.user = None
    st.session_state.result = None
    st.rerun()


# ══════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════
def show_login():
    # Hero section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("""
        <div style='text-align:center; margin-bottom: 2rem;'>
            <div style='font-size:48px; margin-bottom:8px;'>🛒</div>
            <div class='logo-text' style='font-size:36px;'>ResolveAI</div>
            <div class='tagline' style='font-size:17px; margin-top:8px;'>
                AI-Powered E-Commerce Complaint Resolution
            </div>
            <div style='margin-top:12px; display:flex; justify-content:center; gap:8px; flex-wrap:wrap;'>
                <span style='background:rgba(59,130,246,0.2); color:#93c5fd; padding:4px 12px; border-radius:20px; font-size:12px;'>RAG + LLM</span>
                <span style='background:rgba(124,58,237,0.2); color:#c4b5fd; padding:4px 12px; border-radius:20px; font-size:12px;'>Multilingual</span>
                <span style='background:rgba(16,185,129,0.2); color:#6ee7b7; padding:4px 12px; border-radius:20px; font-size:12px;'>Auto Email</span>
                <span style='background:rgba(245,158,11,0.2); color:#fcd34d; padding:4px 12px; border-radius:20px; font-size:12px;'>Audit Log</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐  Login", "✨  Sign Up"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            email    = st.text_input("Email address", placeholder="you@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In →", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    user, error = login(email, password)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.session_state.user = user
                        st.success(f"Welcome back, {user.name}!")
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.2);
                        border-radius:10px; padding:10px 14px;'>
                <div style='color:#93c5fd; font-size:12px; font-weight:600; margin-bottom:4px;'>
                    🔑 Default Admin Account
                </div>
                <div style='color:rgba(255,255,255,0.6); font-size:12px;'>
                    admin@complaints.com &nbsp;/&nbsp; admin123
                </div>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            name      = st.text_input("Full Name", placeholder="Rahul Sharma", key="su_name")
            email2    = st.text_input("Email", placeholder="you@example.com", key="su_email")
            col_a, col_b = st.columns(2)
            with col_a:
                pass2 = st.text_input("Password", type="password", key="su_pass")
            with col_b:
                pass3 = st.text_input("Confirm", type="password", key="su_conf")
            role = st.selectbox("Role", ["agent", "admin"], key="su_role")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create Account →", use_container_width=True, type="primary"):
                if not name or not email2 or not pass2:
                    st.error("Please fill in all fields")
                elif pass2 != pass3:
                    st.error("Passwords do not match")
                elif len(pass2) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    user, error = signup(name, email2, pass2, role)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success("✅ Account created! Please login.")

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════════════════
def show_navbar(user):
    role_badge = "👑 Admin" if user.role == "admin" else "🎧 Agent"
    role_color = "#a78bfa" if user.role == "admin" else "#60a5fa"

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:16px; padding:12px 0;'>
            <div class='logo-text' style='font-size:26px;'>🛒 ResolveAI</div>
            <span style='background:rgba(255,255,255,0.08); color:{role_color};
                         padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;'>
                {role_badge}
            </span>
            <span style='color:rgba(255,255,255,0.4); font-size:13px;'>
                {user.name} · {user.email}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", type="secondary", use_container_width=True):
            logout()

    st.markdown("<hr style='margin:0 0 1.5rem 0;'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# DECISION RESULT DISPLAY
# ══════════════════════════════════════════════════════════════════════
def show_result(result):
    if not result:
        st.error("❌ Agent failed to process. Please try again.")
        return

    decision   = result.get("decision", "ESCALATE")
    confidence = int(float(result.get("confidence", 0)) * 100)
    language   = result.get("language_name", "English")
    reason     = result.get("reason", "N/A")
    email_sent = result.get("email_sent", False)

    # Decision color
    colors = {
        "REPLACE":  ("#1e40af", "#3b82f6", "🔄"),
        "REFUND":   ("#065f46", "#10b981", "💰"),
        "ESCALATE": ("#92400e", "#f59e0b", "⚠️"),
    }
    c1, c2, emoji = colors.get(decision, ("#374151", "#6b7280", "❓"))

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {c1}33, {c2}22);
                border: 1px solid {c2}55;
                border-radius: 16px; padding: 1.5rem; margin: 1rem 0;'>
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:1rem;'>
            <span style='font-size:32px;'>{emoji}</span>
            <div>
                <div style='font-size:11px; color:rgba(255,255,255,0.5);
                            text-transform:uppercase; letter-spacing:0.1em;'>
                    Decision
                </div>
                <div style='font-size:28px; font-weight:700; color:white;'>
                    {decision}
                </div>
            </div>
            <div style='margin-left:auto; text-align:right;'>
                <div style='font-size:11px; color:rgba(255,255,255,0.5);'>Confidence</div>
                <div style='font-size:24px; font-weight:700; color:{c2};'>{confidence}%</div>
            </div>
        </div>
        <div style='background:rgba(0,0,0,0.2); border-radius:10px; padding:1rem;
                    font-size:14px; color:rgba(255,255,255,0.85); line-height:1.6;'>
            {reason}
        </div>
        <div style='display:flex; gap:8px; margin-top:1rem; flex-wrap:wrap;'>
            <span style='background:rgba(255,255,255,0.1); color:rgba(255,255,255,0.7);
                         padding:4px 12px; border-radius:20px; font-size:12px;'>
                🌐 {language}
            </span>
            <span style='background:rgba(255,255,255,0.1); color:rgba(255,255,255,0.7);
                         padding:4px 12px; border-radius:20px; font-size:12px;'>
                📋 {result.get("policy_reference", "N/A")[:40]}
            </span>
            <span style='background:{"rgba(16,185,129,0.2)" if email_sent else "rgba(255,255,255,0.08)"};
                         color:{"#6ee7b7" if email_sent else "rgba(255,255,255,0.5)"};
                         padding:4px 12px; border-radius:20px; font-size:12px;'>
                {"📧 Email sent ✓" if email_sent else "📧 Email not sent"}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Email draft
    if result.get("email_body"):
        with st.expander("📧 View Email Draft"):
            st.markdown(f"**Subject:** {result.get('email_subject', '')}")
            st.text_area("", value=result.get("email_body", ""), height=180,
                         label_visibility="collapsed")


# ══════════════════════════════════════════════════════════════════════
# AGENT DASHBOARD
# ══════════════════════════════════════════════════════════════════════
def show_agent_dashboard():
    from app.agent import resolve_complaint, get_order_by_id
    from app.db import save_complaint, get_complaints_by_user

    user = st.session_state.user
    show_navbar(user)

    col1, col2 = st.columns([3, 2], gap="large")

    # ── Left: Submit form ─────────────────────────────────────────────
    with col1:
        st.markdown("### 📝 Submit Complaint")
        st.markdown("""
        <div style='color:rgba(255,255,255,0.5); font-size:13px; margin-bottom:1rem;'>
            Paste the customer complaint in any language. The AI will detect language,
            search relevant policy, and make a decision automatically.
        </div>
        """, unsafe_allow_html=True)

        complaint_text = st.text_area(
            "Customer Complaint",
            placeholder="Type or paste complaint here...\n\nSupports English, Hindi (हिंदी), Tamil (தமிழ்), and more.",
            height=160,
            label_visibility="collapsed"
        )

        col_a, col_b = st.columns([2, 1])
        with col_a:
            order_id = st.text_input(
                "Order ID",
                placeholder="e.g. ORD-TEST-001",
                label_visibility="collapsed"
            )
        with col_b:
            submit = st.button(
                "🤖 Resolve",
                type="primary",
                use_container_width=True
            )

        if submit:
            if not complaint_text.strip():
                st.error("Please enter a complaint")
            else:
                with st.spinner("🤖 AI analyzing complaint..."):
                    result = None
                    try:
                        result = resolve_complaint(
                            complaint=complaint_text,
                            order_id=order_id if order_id else None
                        )
                        order = get_order_by_id(order_id) if order_id else None
                        save_complaint(
                            complaint_data={
                                "complaint": complaint_text,
                                "order_id":  order_id,
                                "order":     order
                            },
                            agent_result=result,
                            user_id=user.id
                        )
                        st.session_state.result = result
                    except Exception as e:
                        st.error(f"Error: {e}")

        if st.session_state.result:
            show_result(st.session_state.result)

    # ── Right: Sample IDs + history ───────────────────────────────────
    with col2:
        st.markdown("### 🗂 Quick Reference")
        st.markdown("""
        <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px; padding:1rem; margin-bottom:1rem;'>
            <div style='font-size:12px; font-weight:600; color:rgba(255,255,255,0.5);
                        text-transform:uppercase; margin-bottom:10px;'>Sample Order IDs</div>
            <div style='display:flex; flex-direction:column; gap:8px;'>
                <div style='display:flex; justify-content:space-between;
                            font-size:13px; color:rgba(255,255,255,0.7);'>
                    <span>ORD-TEST-001</span><span style='color:#60a5fa;'>Apple iPhone · Amazon</span>
                </div>
                <div style='display:flex; justify-content:space-between;
                            font-size:13px; color:rgba(255,255,255,0.7);'>
                    <span>ORD-6643</span><span style='color:#60a5fa;'>iPhone 14 · Amazon</span>
                </div>
                <div style='display:flex; justify-content:space-between;
                            font-size:13px; color:rgba(255,255,255,0.7);'>
                    <span>ORD-2784</span><span style='color:#a78bfa;'>Mamaearth · Meesho</span>
                </div>
                <div style='display:flex; justify-content:space-between;
                            font-size:13px; color:rgba(255,255,255,0.7);'>
                    <span>ORD-2362</span><span style='color:#34d399;'>Mi Smart TV · Flipkart</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 My Recent Complaints")
        my_complaints = get_complaints_by_user(user.id)

        if not my_complaints:
            st.markdown("""
            <div style='text-align:center; padding:2rem; color:rgba(255,255,255,0.3);'>
                No complaints yet.<br>Submit one to get started.
            </div>
            """, unsafe_allow_html=True)
        else:
            for c in my_complaints[:8]:
                colors_map = {
                    "REPLACE":  "#60a5fa",
                    "REFUND":   "#34d399",
                    "ESCALATE": "#fcd34d"
                }
                color = colors_map.get(c.decision, "#9ca3af")
                with st.expander(
                    f"{c.decision} — {c.product_name or 'Unknown'} — {c.created_at.strftime('%d %b %H:%M')}"
                ):
                    st.write(f"**Complaint:** {c.complaint_text[:150]}...")
                    st.write(f"**Reason:** {c.reason[:200]}...")
                    st.write(f"**Confidence:** {int(c.confidence * 100)}%")


# ══════════════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════
def show_admin_dashboard():
    from app.db import get_all_complaints, get_all_users, save_complaint
    from app.agent import resolve_complaint, get_order_by_id

    user = st.session_state.user
    show_navbar(user)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊  Overview",
        "📝  Resolve",
        "📋  Audit Log",
        "👥  Users"
    ])

    # ── Tab 1: Stats ───────────────────────────────────────────────────
    with tab1:
        all_complaints = get_all_complaints()
        total     = len(all_complaints)
        refunds   = sum(1 for c in all_complaints if c.decision == "REFUND")
        replaces  = sum(1 for c in all_complaints if c.decision == "REPLACE")
        escalates = sum(1 for c in all_complaints if c.decision == "ESCALATE")
        avg_conf  = sum(c.confidence for c in all_complaints) / total if total > 0 else 0
        res_rate  = round((refunds + replaces) / total * 100) if total > 0 else 0

        # Metrics row
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total}</div>
                <div class='metric-label'>Total Complaints</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#34d399;'>{refunds}</div>
                <div class='metric-label'>💰 Refunds</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#60a5fa;'>{replaces}</div>
                <div class='metric-label'>🔄 Replacements</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#fcd34d;'>{escalates}</div>
                <div class='metric-label'>⚠️ Escalated</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#a78bfa;'>{res_rate}%</div>
                <div class='metric-label'>Resolution Rate</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts
        if total > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Decision Breakdown")
                import pandas as pd
                chart_data = pd.DataFrame({
                    "Decision": ["REFUND", "REPLACE", "ESCALATE"],
                    "Count":    [refunds, replaces, escalates]
                })
                st.bar_chart(chart_data.set_index("Decision"), color="#3b82f6")

            with col2:
                st.markdown("#### Recent Activity")
                recent = all_complaints[:10]
                if recent:
                    activity_data = pd.DataFrame([{
                        "ID":       f"#{c.id}",
                        "Decision": c.decision,
                        "Product":  (c.product_name or "Unknown")[:20],
                        "Conf":     f"{int(c.confidence*100)}%",
                        "Date":     c.created_at.strftime("%d %b")
                    } for c in recent])
                    st.dataframe(
                        activity_data,
                        hide_index=True,
                        use_container_width=True
                    )

    # ── Tab 2: Submit ──────────────────────────────────────────────────
    with tab2:
        st.markdown("### 📝 Resolve a Complaint")
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            complaint_text = st.text_area(
                "Customer Complaint",
                placeholder="Paste complaint in any language...",
                height=160,
                key="admin_complaint"
            )
            col_a, col_b = st.columns([2, 1])
            with col_a:
                order_id = st.text_input(
                    "Order ID",
                    placeholder="e.g. ORD-TEST-001",
                    key="admin_order_id",
                    label_visibility="collapsed"
                )
            with col_b:
                resolve_btn = st.button(
                    "🤖 Resolve",
                    type="primary",
                    key="admin_resolve",
                    use_container_width=True
                )

            if resolve_btn:
                if not complaint_text.strip():
                    st.error("Please enter a complaint")
                else:
                    with st.spinner("🤖 AI analyzing..."):
                        result = None
                        try:
                            result = resolve_complaint(
                                complaint=complaint_text,
                                order_id=order_id if order_id else None
                            )
                            order = get_order_by_id(order_id) if order_id else None
                            save_complaint(
                                complaint_data={
                                    "complaint": complaint_text,
                                    "order_id":  order_id,
                                    "order":     order
                                },
                                agent_result=result,
                                user_id=user.id
                            )
                            st.session_state.result = result
                        except Exception as e:
                            st.error(f"Error: {e}")

            if st.session_state.get("result"):
                show_result(st.session_state.result)

        with col2:
            st.markdown("""
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                        border-radius:12px; padding:1.2rem;'>
                <div style='font-size:12px; font-weight:600; color:rgba(255,255,255,0.5);
                            text-transform:uppercase; margin-bottom:12px;'>How It Works</div>
                <div style='display:flex; flex-direction:column; gap:10px;'>
                    <div style='display:flex; gap:10px; align-items:flex-start;'>
                        <span style='background:rgba(59,130,246,0.2); color:#60a5fa;
                                     padding:2px 8px; border-radius:6px; font-size:11px;
                                     font-weight:600; flex-shrink:0;'>1</span>
                        <span style='font-size:13px; color:rgba(255,255,255,0.7);'>
                            Detects complaint language automatically</span>
                    </div>
                    <div style='display:flex; gap:10px; align-items:flex-start;'>
                        <span style='background:rgba(59,130,246,0.2); color:#60a5fa;
                                     padding:2px 8px; border-radius:6px; font-size:11px;
                                     font-weight:600; flex-shrink:0;'>2</span>
                        <span style='font-size:13px; color:rgba(255,255,255,0.7);'>
                            Searches company-specific policy via RAG</span>
                    </div>
                    <div style='display:flex; gap:10px; align-items:flex-start;'>
                        <span style='background:rgba(59,130,246,0.2); color:#60a5fa;
                                     padding:2px 8px; border-radius:6px; font-size:11px;
                                     font-weight:600; flex-shrink:0;'>3</span>
                        <span style='font-size:13px; color:rgba(255,255,255,0.7);'>
                            Checks order details and return window</span>
                    </div>
                    <div style='display:flex; gap:10px; align-items:flex-start;'>
                        <span style='background:rgba(59,130,246,0.2); color:#60a5fa;
                                     padding:2px 8px; border-radius:6px; font-size:11px;
                                     font-weight:600; flex-shrink:0;'>4</span>
                        <span style='font-size:13px; color:rgba(255,255,255,0.7);'>
                            Decides: Refund / Replace / Escalate</span>
                    </div>
                    <div style='display:flex; gap:10px; align-items:flex-start;'>
                        <span style='background:rgba(59,130,246,0.2); color:#60a5fa;
                                     padding:2px 8px; border-radius:6px; font-size:11px;
                                     font-weight:600; flex-shrink:0;'>5</span>
                        <span style='font-size:13px; color:rgba(255,255,255,0.7);'>
                            Sends personalised email to customer</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Audit Log ───────────────────────────────────────────────
    with tab3:
        st.markdown("### 📋 Audit Log — All Complaints")
        all_complaints = get_all_complaints()

        if not all_complaints:
            st.info("No complaints resolved yet.")
        else:
            # Summary table
            import pandas as pd
            table_data = pd.DataFrame([{
                "ID":        f"#{c.id}",
                "Decision":  c.decision,
                "Customer":  c.customer_name or "Unknown",
                "Product":   (c.product_name or "Unknown")[:25],
                "Company":   c.company or "N/A",
                "Conf":      f"{int(c.confidence*100)}%",
                "Date":      c.created_at.strftime("%d %b %Y %H:%M"),
            } for c in all_complaints])

            st.dataframe(table_data, hide_index=True, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Detailed View")

            for c in all_complaints:
                decision_emoji = {"REPLACE": "🔄", "REFUND": "💰", "ESCALATE": "⚠️"}.get(c.decision, "❓")
                with st.expander(
                    f"{decision_emoji} #{c.id} — {c.decision} | {c.customer_name or 'Unknown'} | {c.product_name or 'Unknown'} | {c.created_at.strftime('%d %b %Y')}"
                ):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Decision", c.decision)
                    col2.metric("Confidence", f"{int(c.confidence*100)}%")
                    col3.metric("Company", c.company or "N/A")
                    st.write(f"**Complaint:** {c.complaint_text}")
                    st.write(f"**Reason:** {c.reason}")
                    st.write(f"**Policy:** {c.policy_reference or 'N/A'}")
                    if c.email_body:
                        st.write(f"**Email:** {c.email_body[:300]}...")

    # ── Tab 4: Users ───────────────────────────────────────────────────
    with tab4:
        st.markdown("### 👥 All Users")
        all_users = get_all_users()

        import pandas as pd
        user_data = pd.DataFrame([{
            "ID":      u.id,
            "Name":    u.name,
            "Email":   u.email,
            "Role":    u.role.upper(),
            "Joined":  u.created_at.strftime("%d %b %Y"),
        } for u in all_users])

        st.dataframe(user_data, hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════
def main():
    if st.session_state.user is None:
        show_login()
    elif st.session_state.user.role == "admin":
        show_admin_dashboard()
    else:
        show_agent_dashboard()


if __name__ == "__main__":
    main()