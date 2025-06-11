import streamlit as st
import os
import json
import random
from utils.question_loader import load_questions_from_directory
from supabase_utils import login_user  # 你自己的Supabase函数模块

st.set_page_config(page_title="Math de Elliott – HSC Practice", layout="wide")

st.title("📘 Math de Elliott – HSC Practice Questions")

# --------- 🔐 Simulated Subscription Status ---------
# You can toggle this to simulate subscribed vs free user
is_subscribed = False
free_modules = [
    ("year12", "extension1", "trigonometric"),
    ("year12", "extension2", "harder_questions"),
]

# --------- 🧑‍💻 Login Section ---------
if "user" not in st.session_state:
    st.subheader("🔐 Login or Register")
    email = st.text_input("Login Email")
    if st.button("Login"):
        user = login_user(email)
        if user:
            st.success(f"✅ Welcome back, {email}!")
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Login failed.")
    st.stop()

# --------- 🧠 After Login ---------
st.markdown("Use the filters below to explore question modules:")

# Load dropdown structure
BASE_DIR = "questions"
question_tree = {}

for year in os.listdir(BASE_DIR):
    year_path = os.path.join(BASE_DIR, year)
    if os.path.isdir(year_path):
        question_tree[year] = {}
        for level in os.listdir(year_path):
            level_path = os.path.join(year_path, level)
            if os.path.isdir(level_path):
                modules = [f[:-5] for f in os.listdir(level_path) if f.endswith(".json")]
                question_tree[year][level] = modules

# Dropdown menus
year = st.selectbox("📅 Select Year", sorted(question_tree.keys()))
level = st.selectbox("📘 Select Level", sorted(question_tree[year].keys()))
module = st.selectbox("📂 Select Module", sorted(question_tree[year][level]))

# Construct path
filepath = os.path.join(BASE_DIR, year, level, f"{module}.json")

# Load questions
if not os.path.exists(filepath):
    st.error("❌ Question file not found.")
    st.stop()

with open(filepath, "r", encoding="utf-8") as f:
    questions = json.load(f)

# --------- 🔐 Apply Access Control ---------
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
        # Filter questions
        sample = {}
        for q in questions:
            d = q.get("difficulty", "").lower()
            if d in ["easy", "medium", "hard"] and d not in sample:
                sample[d] = q
        questions = list(sample.values())
    else:
        st.error("🔒 This module is for subscribers only. Please subscribe to continue.")
        st.stop()

# --------- 📄 Pagination ---------
questions_per_page = 5
total_pages = (len(questions) - 1) // questions_per_page + 1
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
