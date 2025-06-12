import streamlit as st
import os
from utils.question_loader import load_questions
from supabase_utils import login_user, register_user
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Math de Elliott – HSC Practice Questions", layout="centered")

st.title("📘 Math de Elliott – HSC Practice Questions")
st.write("Practice HSC Mathematics by selecting year, level, and topic. Each page shows 5 questions with hints.")

# Simulated subscription control
is_subscribed = False
free_modules = [
    ("year12", "extension1", "trigonometric"),
    ("year12", "extension2", "harder_questions")
]

# User session state
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ========== LOGIN / REGISTER ==========
if not st.session_state.user_email:
    st.subheader("🔐 Login or Register")
    st.info("📝 **Free demo chapters available:**\n"
            "- Year 12 Extension 1 ➜ `trigonometric`\n"
            "- Year 12 Extension 2 ➜ `harder_questions`\n\n"
            "👉 Try these before subscribing!")

    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])
    with tab1:
        st.subheader("🔐 Login to Your Account", anchor=False)
        email = st.text_input("Login Email", placeholder="you@example.com", label_visibility="collapsed")
        if st.button("Login"):
            if login_user(email):
                st.session_state.user_email = email
                st.success(f"Welcome back, {email}!")
                st.experimental_rerun()
            else:
                st.error("Login failed. Please try again or register.")

    with tab2:
        st.subheader("✍️ Register a New Account", anchor=False)
        new_email = st.text_input("Register Email", placeholder="you@example.com", label_visibility="collapsed", key="reg")
        if st.button("Register"):
            if register_user(new_email):
                st.success("✅ Registered! Please return to Login tab.")
            else:
                st.warning("Registration may have failed. Try again.")
    st.stop()

# ========== LOGGED-IN CONTENT ==========

# Sidebar Filters
st.subheader("📚 Select Year / Level / Module")
col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.selectbox("📅 Select Year", ["year11", "year12"])
with col2:
    selected_level = st.selectbox("📘 Select Level", ["extension1", "extension2"])
with col3:
    module_dir = os.path.join("questions", selected_year, selected_level)
    if os.path.exists(module_dir):
        available_modules = [f.replace(".json", "") for f in os.listdir(module_dir) if f.endswith(".json")]
        selected_module = st.selectbox("📂 Select Module", available_modules)
    else:
        st.warning("Module path not found.")
        st.stop()

# Determine access
is_free_module = (selected_year, selected_level, selected_module) in free_modules
if not is_subscribed and not is_free_module:
    st.warning("⚠️ This is a premium module. Only 3 sample questions are shown.")

# Load and display questions
questions = load_questions(selected_year, selected_level, selected_module)
page = st.number_input("📄 Page", min_value=1, max_value=len(questions) // 5 + 1, step=1)

start = (page - 1) * 5
end = start + (5 if is_subscribed or is_free_module else 3)

for i, q in enumerate(questions[start:end], start=1):
    st.markdown(f"### Question {i}")
    st.markdown(q["question"], unsafe_allow_html=True)
    selected_option = st.radio("Choose your answer for Q{}:".format(i), q["options"], key=f"q{i}")
    if st.button(f"Submit Q{i}"):
        if selected_option == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")

    if "hint" in q:
        with st.expander("💡 Hint"):
            st.markdown(q["hint"], unsafe_allow_html=True)
    else:
        st.info("ℹ️ No hint available for this question.")
