import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
from subscribe_pro import create_checkout_session

load_dotenv()

# Supabase keys from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Stripe checkout session environment
DOMAIN_URL = os.getenv("DOMAIN_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Math de Elliott", layout="centered")
st.title("📘 Math de Elliott")

# Session state to manage login
if "user" not in st.session_state:
    st.session_state["user"] = None

# -------------------- UI Helper --------------------
def show_login_ui():
    with st.form("login"):
        st.subheader("🔐 Login to your account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if result.user:
                st.session_state["user"] = result.user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Login failed. Please check your credentials.")

def show_register_ui():
    with st.form("register"):
        st.subheader("📝 Register a new account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        if submit:
            try:
                result = supabase.auth.sign_up({"email": email, "password": password})
                if result.user:
                    st.success("Account created! Please login.")
                    st.rerun()
                else:
                    st.error("Registration failed.")
            except Exception as e:
                st.error(str(e))

# -------------------- Login / Register Flow --------------------
if st.session_state["user"] is None:
    st.info("Please login or register to continue.")
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])
    with tab1:
        show_login_ui()
    with tab2:
        show_register_ui()
    st.stop()

# -------------------- Main App --------------------
user = st.session_state["user"]
st.success(f"Welcome, {user.email}")

# Simulated Pro Check (will replace with Webhook in future)
st.markdown("#### ✨ Upgrade to Pro to unlock all chapters")

col1, col2 = st.columns(2)
with col1:
    if st.button("💳 Upgrade to Pro (Monthly)"):
        url = create_checkout_session(mode="monthly", user_email=user.email)
        st.markdown(f"[👉 Click here to complete monthly payment]({url})", unsafe_allow_html=True)

with col2:
    if st.button("💳 Upgrade to Pro (Yearly)"):
        url = create_checkout_session(mode="yearly", user_email=user.email)
        st.markdown(f"[👉 Click here to complete yearly payment]({url})", unsafe_allow_html=True)

st.divider()
st.markdown("#### 📚 Try the demo modules below before upgrading:")
st.info("You can explore 3 free demo chapters to experience the platform.")

# Example: Load demo chapters (replace with your own logic)
demo_chapters = [
    "Year 12 Extension 1 – Trigonometric Integrals",
    "Year 12 Extension 2 – Harder Calculus",
    "Year 12 Advanced – Applications of Derivatives"
]
for chapter in demo_chapters:
    st.markdown(f"✅ {chapter}")

# Logout
if st.button("🚪 Logout"):
    st.session_state["user"] = None
    st.rerun()
