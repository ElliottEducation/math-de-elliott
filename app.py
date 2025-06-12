import os
import json
import streamlit as st
from dotenv import load_dotenv
from utils.question_loader import load_questions
from supabase_utils import login_user, register_user
from subscribe_pro import create_checkout_session

# --- Load environment variables ---
load_dotenv()
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# --- Simulated subscription logic ---
free_modules = [
    ("year12", "extension1", "trigonometric"),
    ("year12", "extension2", "harder_questions"),
]

# --- Streamlit app starts here ---
st.set_page_config(page_title="Math de Elliott – HSC Practice Questions", page_icon="📘")
st.title("📘 Math de Elliott – HSC Practice Questions")

# --- Session state ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- Login/Register block ---
st.subheader("🔐 Login or Register")
with st.container():
    st.markdown(
        """
        <div style="background-color: #eef6ff; padding: 10px; border-radius: 5px;">
        <b>✏️ Free demo chapters available:</b><br>
        • Year 12 Extension 1 → <code>trigonometric</code><br>
        • Year 12 Extension 2 → <code>harder_questions</code><br>
        👉 Try these before subscribing!
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])

    with tab1:
        st.subheader("🔐 Login to Your Account")
        login_email = st.text_input("Login Email", key="login_email")
        if st.button("Login"):
            user = login_user(login_email)
            if user:
                st.session_state.user_email = login_email
                st.success(f"✅ Welcome back, {login_email}!")
                st.rerun()
            else:
                st.error("Login failed. Please try again or register.")

    with tab2:
        st.subheader("🆕 Create a New Account")
        register_email = st.text_input("Register Email", key="register_email")
        if st.button("Register"):
            user = register_user(register_email)
            if user:
                st.success("🎉 Registration successful! You can now login.")
            else:
                st.error("Registration failed. Try a different email.")

# --- Main Interface ---
user_email = st.session_state.user_email
if user_email:
    st.success(f"✅ Logged in as: {user_email}")

    # Simulate Pro access (to be replaced by real database/webhook logic)
    is_pro_user = False

    # --- Upgrade to Pro ---
    if not is_pro_user:
        with st.expander("✨ Upgrade to Pro"):
            st.markdown("**Get access to all premium questions by upgrading your account.**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Upgrade – $20/month"):
                    checkout_url = create_checkout_session(user_email, plan="monthly")
                    st.markdown(f"[👉 Click here to complete payment]({checkout_url})", unsafe_allow_html=True)
            with col2:
                if st.button("Upgrade – $199/year"):
                    checkout_url = create_checkout_session(user_email, plan="yearly")
                    st.markdown(f"[👉 Click here to complete payment]({checkout_url})", unsafe_allow_html=True)

    # Show success message if returning from Stripe
    if "payment" in st.query_params:
        if st.query_params["payment"] == "success":
            st.success("🎉 Payment successful! Your account will be upgraded to Pro soon.")
        elif st.query_params["payment"] == "cancelled":
            st.warning("⚠️ Payment was cancelled.")

    # --- Question selection UI ---
    st.subheader("📚 Select Year / Level / Module")
    year = st.selectbox("📅 Select Year", ["year11", "year12"])
    level = st.selectbox("📘 Select Level", ["standard1", "standard2", "advanced", "extension1", "extension2"])

    # Dynamically load available modules based on JSON files
    import os
    import glob
    available_modules = sorted([
        os.path.splitext(os.path.basename(f))[0] for f in glob.glob("questions/*.json")
    ])
    module = st.selectbox("📁 Select Module", available_modules)

    # Load questions
    questions = load_questions(year, level, module)
    if questions:
        # Check if current module is free or Pro
        if (year, level, module) not in free_modules:
            st.warning("⚠️ This is a premium module. Only 3 sample questions are shown.")
            questions = questions[:3]

        page = st.number_input("📄 Page", min_value=1, max_value=len(questions), step=1)
        q = questions[page - 1]

        st.markdown(f"### Question {page}")
        st.latex(q["question"])

        selected = st.radio("Choose your answer for Q1:", q["options"], key=f"q{page}")
        if st.button(f"Submit Q{page}"):
            if selected == q["answer"]:
                st.success("✅ Correct!")
            else:
                st.error("❌ Incorrect.")

        st.info(q.get("hint", "ℹ️ No hint available for this question."))
    else:
        st.warning("⚠️ No questions found for this module.")
else:
    st.warning("🔒 Please login to view or answer questions.")
