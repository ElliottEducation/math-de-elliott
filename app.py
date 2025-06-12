import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import stripe
from subscribe_pro import create_checkout_session, upgrade_user_role

load_dotenv()

# ---------- 🔧 Supabase 设置 ----------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- 🔧 Stripe 设置 ----------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ---------- 🚪 页面切换变量 ----------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------- 👤 登录功能 ----------
def login():
    st.title("🔐 Login to Math de Elliott")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if user and user.user:
                st.session_state.user = user.user
                st.session_state.email = email
                st.session_state.page = "main"
                st.success("Login successful!")
            else:
                st.error("Login failed.")
        except Exception as e:
            st.error(f"Login error: {e}")

    st.markdown("Don't have an account? 👉 [Register now](#)", unsafe_allow_html=True)
    if st.button("Go to Register"):
        st.session_state.page = "register"

# ---------- 🆕 注册功能 ----------
def register():
    st.title("📝 Register for Math de Elliott")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        try:
            result = supabase.auth.sign_up({"email": email, "password": password})
            if result and result.user:
                st.success("Registration successful! Please check your email to confirm.")
            else:
                st.error("Registration failed.")
        except Exception as e:
            st.error(f"Registration error: {e}")

    if st.button("Back to Login"):
        st.session_state.page = "login"

# ---------- 🧠 主页面内容 ----------
def main_app():
    # ✅ 检查支付回调参数
    query_params = st.experimental_get_query_params()
    if "success" in query_params and "email" in query_params:
        email = query_params["email"][0]
        if upgrade_user_role(email):
            st.success("🎉 Your account has been upgraded to Pro!")
        else:
            st.error("⚠️ Failed to update your account. Please contact support.")

    st.title("📚 Welcome to Math de Elliott")

    email = st.session_state.get("email", "user@example.com")

    st.markdown(f"### 👋 Hello, {email}")

    # 🚀 升级为 Pro 订阅按钮
    st.markdown("### 💳 Upgrade to Pro Plan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Subscribe Monthly ($20/month)"):
            checkout_url = create_checkout_session(email, billing_period="monthly")
            if checkout_url:
                st.success("Redirecting to Stripe...")
                st.markdown(f"[Click to pay]({checkout_url})", unsafe_allow_html=True)

    with col2:
        if st.button("Subscribe Yearly ($199/year)"):
            checkout_url = create_checkout_session(email, billing_period="yearly")
            if checkout_url:
                st.success("Redirecting to Stripe...")
                st.markdown(f"[Click to pay]({checkout_url})", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ---------- 🔁 页面导航 ----------
if st.session_state.page == "login":
    login()
elif st.session_state.page == "register":
    register()
else:
    main_app()
