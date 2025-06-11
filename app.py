import streamlit as st
import os
import json
import random
from supabase_utils import login_user, register_user

st.set_page_config(page_title="Math de Elliott – HSC Practice", layout="wide")
st.title("📘 Math de Elliott – HSC Practice Questions")

# --------- 🔐 Simulated Subscription ---------
is_subscribed = False
free_modules = [
    ("year12", "extension1", "trigonometric"),
    ("year12", "extension2", "harder_questions")
]

# --------- 👤 Login + Register UI (Improved layout) ---------
if "user" not in st.session_state:
    st.markdown("### 🔐 Login or Register")

    st.info("🧪 Free demo chapters available:\n"
            "- `Year 12 Extension 1 → trigonometric`\n"
            "- `Year 12 Extension 2 → harder_questions`\n\n"
            "👉 Try these before subscribing!")

    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])

    with tab1:
        st.markdown("#### 🔐 Login to Your Account")
        login_col1, login_col2, login_col3 = st.columns([2, 3, 2])
        with login_col2:
            login_email = st.text_input("Login Email", key="login_email", placeholder="you@example.com")
            if st.button("Login"):
                user = login_user(login_email)
                if user:
                    st.success(f"✅ Welcome back, {login_email}!")
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Login failed. Please register first.")

    with tab2:
        st.markdown("#### 🆕 Create a New Account")
        reg_col1, reg_col2, reg_col3 = st.columns([2, 3, 2])
        with reg_col2:
            register_email = st.text_input("Register Email", key="register_email", placeholder="you@example.com")
            if st.button("Register"):
                user = register_user(register_email)
                if user:
                    st.success("🎉 Registration complete. Please login now.")
                else:
                    st.error("Registration failed.")

    st.stop()

# --------- 🧠 Dropdown Menus ---------
BASE_DIR = "questions"
question_tree = {}

for year in os.listdir(BASE_DIR):
    y_path = os.path.join(BASE_DIR, year)
    if os.path.isdir(y_path):
        question_tree[year] = {}
        for level in os.listdir(y_path):
            l_path = os.path.join(y_path, level)
            if os.path.isdir(l_path):
                modules = [f[:-5] for f in os.listdir(l_path) if f.endswith(".json")]
                question_tree[year][level] = modules

year = st.selectbox("📅 Select Year", sorted(question_tree.keys()))
level = st.selectbox("📘 Select Level", sorted(question_tree[year].keys()))
module = st.selectbox("📂 Select Module", sorted(question_tree[year][level]))

# --------- 📄 Load Questions ---------
json_path = os.path.join(BASE_DIR, year, level, f"{module}.json")

if not os.path.exists(json_path):
    st.error("❌ Question file not found.")
    st.stop()

with open(json_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# --------- 🔐 Subscription Access Control ---------
if not is_subscribed:
    if (year, level, module) in free_modules:
        st.warning(f"""
        💡 You're accessing a premium module: **{module.replace('_', ' ').title()}**

        Only 3 sample questions are available:
        - 1 x Easy
        - 1 x Medium
        - 1 x Hard

        🔓 To unlock full access:
        👉 [Subscribe Monthly (Simulated)](https://example.com/month)
        👉 [Subscribe Yearly (Simulated)](https://example.com/year)
        """)
        sample = {}
        for q in questions:
            d = q.get("difficulty", "").lower()
            if d in ["easy", "medium", "hard"] and d not in sample:
                sample[d] = q
        questions = list(sample.values())
    else:
        st.error("🔒 This module is only available to subscribers.")
        st.stop()

# --------- 📊 Pagination ---------
questions_per_page = 5
total_pages = max(1, (len(questions) - 1) // questions_per_page + 1)
page = st.number_input("📑 Page", min_value=1, max_value=total_pages, value=1)

start = (page - 1) * questions_per_page
end = start + questions_per_page
display_questions = questions[start:end]

# --------- ✅ Show Questions ---------
for idx, q in enumerate(display_questions, start=1):
    st.markdown(f"### Question {idx}")
    st.markdown(q["question"])
    selected_option = st.radio(f"Choose your answer for Q{idx}:", q["options"], key=f"q{idx}")

    if st.button(f"Submit Q{idx}"):
        if selected_option == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")

    with st.expander("💡 Hint"):
        st.markdown(q["solution"])
