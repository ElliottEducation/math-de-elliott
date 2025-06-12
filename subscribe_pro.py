import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import stripe
from subscribe_pro import create_checkout_session

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
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# ---------- ✅ 成功支付后记录状态 ----------
def handle_payment_success(email):
    try:
        supabase.table("user_status").upsert({"email": email, "is_pro": True}).execute()
        st.session_state.is_pro = True
        st.success("✅ Your Pro subscription is now active!")
    except Exception as e:
        st.error(f"Database update failed: {e}")

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

                # 检查是否为 Pro 用户
                result = supabase.table("user_status").select("is_pro").eq("email", email).execute()
                if result.data and len(result.data) > 0 and result.data[0].get("is_pro"):
                    st.session_state.is_pro = True

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
    st.title("📚 Welcome to Math de Elliott")

    email = st.session_state.get("email", "user@example.com")
    st.markdown(f"### 👋 Hello, {email}")

    # 检查 URL 参数（Stripe 回调成功）
    query_params = st.experimental_get_query_params()
    if "success" in query_params:
        handle_payment_success(email)

    # 订阅提示或升级按钮
    if not st.session_state.is_pro:
        st.warning("🚫 You are currently using the free plan.")
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
    else:
        st.success("🎉 You are a Pro subscriber!")

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
