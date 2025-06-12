import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import stripe
from subscribe_pro import create_checkout_session, upgrade_user_role
from urllib.parse import urlparse, parse_qs

# ---------- 🔧 加载配置 ----------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- 🧠 页面状态初始化 ----------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------- 👤 登录 ----------
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

# ---------- 🆕 注册 ----------
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

# ---------- 🧠 主页面 ----------
def main_app():
    email = st.session_state.get("email", "user@example.com")
    st.title("📚 Welcome to Math de Elliott")
    st.markdown(f"### 👋 Hello, {email}")

    # ✅ 检查用户身份
    user_role = get_user_role(email)

    if is_payment_success():
        upgraded = upgrade_user_role(email)
        if upgraded:
            st.success("🎉 You have been upgraded to Pro!")

    # 🔒 显示订阅按钮
    if user_role != "pro":
        st.warning("⚠️ You are on the Free Plan. Upgrade to access all questions!")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Subscribe Monthly ($20/month)"):
                checkout_url = create_checkout_session(email, billing_period="monthly")
                if checkout_url:
                    st.success("Redirecting to Stripe...")
                    st.markdown(f"[👉 Click to Pay]({checkout_url})", unsafe_allow_html=True)

        with col2:
            if st.button("Subscribe Yearly ($199/year)"):
                checkout_url = create_checkout_session(email, billing_period="yearly")
                if checkout_url:
                    st.success("Redirecting to Stripe...")
                    st.markdown(f"[👉 Click to Pay]({checkout_url})", unsafe_allow_html=True)

    # ✅ Pro 用户可以访问全部功能
    if user_role == "pro":
        st.success("🌟 You are a Pro user. Full access granted!")
        st.markdown("🔓 Here is your full access to all modules and features.")
        # 👉 在这里加载你所有 premium 功能模块

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ---------- 🔍 获取用户角色 ----------
def get_user_role(email):
    try:
        result = supabase.table("users").select("user_role").eq("email", email).single().execute()
        return result.data.get("user_role", "free")
    except Exception:
        return "free"

# ---------- ✅ 检查是否支付成功回调 ----------
def is_payment_success():
    query_params = st.experimental_get_query_params()
    return query_params.get("success", ["false"])[0] == "true" and "email" in query_params

# ---------- 🔁 页面导航 ----------
if st.session_state.page == "login":
    login()
elif st.session_state.page == "register":
    register()
else:
    main_app()
