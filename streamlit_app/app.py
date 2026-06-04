"""
streamlit_app/app.py
Main Streamlit UI with login, signup, agent dashboard, admin dashboard.
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import login, signup, create_default_admin
from app.db import create_tables

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Complaint Resolution",
    page_icon="🛒",
    layout="wide"
)

# ── Initialize database on first run ─────────────────────────────────
create_tables()
create_default_admin()

# ── Session state ─────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"


# ── Logout ────────────────────────────────────────────────────────────
def logout():
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()


# ══════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🛒 AI Complaint Resolution")
        st.markdown("#### Login to your account")
        st.divider()

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        # ── Login tab ─────────────────────────────────────────────────
        with tab1:
            email    = st.text_input("Email", placeholder="your@email.com", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    user, error = login(email, password)
                    if error:
                        st.error(error)
                    else:
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        st.success(f"Welcome {user.name}!")
                        st.rerun()

            st.divider()
            st.caption("Default admin: admin@complaints.com / admin123")

        # ── Signup tab ────────────────────────────────────────────────
        with tab2:
            name      = st.text_input("Full Name", placeholder="Rahul Sharma", key="signup_name")
            email2    = st.text_input("Email", placeholder="your@email.com", key="signup_email")
            password2 = st.text_input("Password", type="password", key="signup_password")
            password3 = st.text_input("Confirm Password", type="password", key="signup_confirm")
            role      = st.selectbox("Role", ["agent", "admin"], key="signup_role")

            if st.button("Create Account", use_container_width=True, type="primary"):
                if not name or not email2 or not password2:
                    st.error("Please fill in all fields")
                elif password2 != password3:
                    st.error("Passwords do not match")
                elif len(password2) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    user, error = signup(name, email2, password2, role)
                    if error:
                        st.error(error)
                    else:
                        st.success(f"Account created! Please login.")


# ══════════════════════════════════════════════════════════════════════
# AGENT DASHBOARD
# ══════════════════════════════════════════════════════════════════════
def show_agent_dashboard():
    from app.agent import resolve_complaint, get_order_by_id
    from app.db import save_complaint, get_complaints_by_user

    user = st.session_state.user

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 🎧 Agent Dashboard")
        st.caption(f"Logged in as: {user.name} ({user.email})")
    with col2:
        if st.button("Logout", type="secondary"):
            logout()

    st.divider()

    # ── Submit complaint ───────────────────────────────────────────────
    st.markdown("### 📝 Submit New Complaint")

    col1, col2 = st.columns([2, 1])
    with col1:
        complaint_text = st.text_area(
            "Customer Complaint",
            placeholder="Paste the customer complaint here...",
            height=150
        )
    with col2:
        order_id = st.text_input(
            "Order ID (optional)",
            placeholder="e.g. ORD-1003"
        )
        st.markdown("#### Sample Order IDs")
        st.caption("ORD-1001 → OnePlus (Amazon)")
        st.caption("ORD-1002 → Jeans (Meesho)")
        st.caption("ORD-1003 → boAt (Flipkart)")
        st.caption("ORD-1007 → HP Laptop (Flipkart)")

    if st.button("🤖 Resolve Complaint", type="primary", use_container_width=True):
        if not complaint_text.strip():
            st.error("Please enter a complaint")
        else:
            with st.spinner("AI is analyzing the complaint... please wait 20-30 seconds"):
                # Run agent
                result = resolve_complaint(
                    complaint=complaint_text,
                    order_id=order_id if order_id else None
                )

                # Save to DB
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

            # Show result
            st.divider()
            st.markdown("### ✅ Resolution")

            # Decision badge
            decision = result["decision"]
            if decision == "REPLACE":
                st.success(f"## Decision: {decision}")
            elif decision == "REFUND":
                st.info(f"## Decision: {decision}")
            else:
                st.warning(f"## Decision: {decision}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence", f"{int(result['confidence'] * 100)}%")
            with col2:
                st.metric("Policy Reference", result.get("policy_reference", "N/A")[:30])

            st.markdown("**Reason:**")
            st.write(result["reason"])

            st.markdown("**📧 Email Draft:**")
            st.markdown(f"**Subject:** {result.get('email_subject', '')}")
            st.text_area("Email Body", value=result.get("email_body", ""), height=200)

    st.divider()

    # ── My complaints ──────────────────────────────────────────────────
    st.markdown("### 📋 My Resolved Complaints")

    my_complaints = get_complaints_by_user(user.id)

    if not my_complaints:
        st.info("No complaints resolved yet. Submit one above!")
    else:
        for c in my_complaints:
            with st.expander(f"[{c.id}] {c.decision} — {c.product_name or 'Unknown product'} — {c.created_at.strftime('%d %b %Y %H:%M')}"):
                st.write(f"**Complaint:** {c.complaint_text}")
                st.write(f"**Decision:** {c.decision}")
                st.write(f"**Reason:** {c.reason}")
                st.write(f"**Confidence:** {int(c.confidence * 100)}%")
                if c.email_body:
                    st.write(f"**Email sent:** {c.email_body[:200]}...")


# ══════════════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════
def show_admin_dashboard():
    from app.db import (
        get_all_complaints, get_all_users,
        save_complaint
    )
    from app.agent import resolve_complaint, get_order_by_id

    user = st.session_state.user

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 👑 Admin Dashboard")
        st.caption(f"Logged in as: {user.name} ({user.email})")
    with col2:
        if st.button("Logout", type="secondary"):
            logout()

    st.divider()

    # ── Tabs ───────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Stats",
        "📝 Submit Complaint",
        "📋 All Complaints",
        "👥 All Users"
    ])

    # ── Tab 1: Stats ───────────────────────────────────────────────────
    with tab1:
        st.markdown("### 📊 System Statistics")
        all_complaints = get_all_complaints()
        total     = len(all_complaints)
        refunds   = sum(1 for c in all_complaints if c.decision == "REFUND")
        replaces  = sum(1 for c in all_complaints if c.decision == "REPLACE")
        escalates = sum(1 for c in all_complaints if c.decision == "ESCALATE")
        avg_conf  = sum(c.confidence for c in all_complaints) / total if total > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Complaints", total)
        col2.metric("Refunds", refunds)
        col3.metric("Replacements", replaces)
        col4.metric("Escalated", escalates)

        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("Avg Confidence", f"{int(avg_conf * 100)}%")
        resolution_rate = round((refunds + replaces) / total * 100) if total > 0 else 0
        col2.metric("Resolution Rate", f"{resolution_rate}%")

    # ── Tab 2: Submit ──────────────────────────────────────────────────
    with tab2:
        st.markdown("### 📝 Submit New Complaint")
        col1, col2 = st.columns([2, 1])
        with col1:
            complaint_text = st.text_area(
                "Customer Complaint",
                placeholder="Paste the customer complaint here...",
                height=150,
                key="admin_complaint"
            )
        with col2:
            order_id = st.text_input(
                "Order ID (optional)",
                placeholder="e.g. ORD-1003",
                key="admin_order_id"
            )

        if st.button("🤖 Resolve Complaint", type="primary", key="admin_resolve"):
            if not complaint_text.strip():
                st.error("Please enter a complaint")
            else:
                with st.spinner("AI is analyzing... please wait"):
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

                decision = result["decision"]
                if decision == "REPLACE":
                    st.success(f"Decision: {decision}")
                elif decision == "REFUND":
                    st.info(f"Decision: {decision}")
                else:
                    st.warning(f"Decision: {decision}")

                st.write(f"**Reason:** {result['reason']}")
                st.write(f"**Confidence:** {int(result['confidence'] * 100)}%")
                st.text_area("Email Draft", value=result.get("email_body", ""), height=200, key="admin_email")

    # ── Tab 3: All complaints ──────────────────────────────────────────
    with tab3:
        st.markdown("### 📋 All Complaints — Audit Log")
        all_complaints = get_all_complaints()

        if not all_complaints:
            st.info("No complaints yet")
        else:
            for c in all_complaints:
                with st.expander(f"[ID:{c.id}] {c.decision} | {c.product_name or 'Unknown'} | {c.customer_name or 'Unknown'} | {c.created_at.strftime('%d %b %Y %H:%M')}"):
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"**Decision:** {c.decision}")
                    col2.write(f"**Confidence:** {int(c.confidence * 100)}%")
                    col3.write(f"**Company:** {c.company or 'N/A'}")
                    st.write(f"**Complaint:** {c.complaint_text}")
                    st.write(f"**Reason:** {c.reason}")
                    st.write(f"**Policy:** {c.policy_reference or 'N/A'}")
                    if c.email_body:
                        st.write(f"**Email:** {c.email_body}")

    # ── Tab 4: All users ───────────────────────────────────────────────
    with tab4:
        st.markdown("### 👥 All Registered Users")
        all_users = get_all_users()

        for u in all_users:
            with st.expander(f"{u.name} — {u.role.upper()} — {u.email}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**ID:** {u.id}")
                col2.write(f"**Role:** {u.role}")
                col3.write(f"**Joined:** {u.created_at.strftime('%d %b %Y')}")


# ══════════════════════════════════════════════════════════════════════
# ROUTER — shows correct page based on session
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