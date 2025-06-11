import streamlit as st
import os
import json
import random
from supabase_utils import login_user

st.set_page_config(page_title="Math de Elliott – HSC Practice", layout="wide")
st.title("📘 Math de Elliott – HSC Practice Questions")

# --------- 🔐 Subscription simulation ---------
is_subscribed = False
free_modules = [
    ("year12", "extension1", "trigonometric"),
    ("year12", "extension2", "harder_questions")
]

# --------- 👤 Login Section ---------
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

# --------- 🧠 Dropdown Menus after Login ---------
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

# --------- 📄 Load and Process Questions ---------
json_path = os.path.join(BASE_DIR, year, level, f"{module}.json")

if not os.path.exists(json_path):
    st.error("❌ Question file not found.")
    st.stop()

with open(json_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# --------- 🔐 Restrict Content for Free Users ---------
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
        st.error("🔒 This module is for subscribers only. Please subscribe to access it.")
        st.stop()

# --------- 📊 Pagination ---------
questions_per_page = 5
total_pages = max(1, (len(questions) - 1) // questions_per_page + 1)
page = st.number_input("📑 Page", min_value=1, max_value=total_pages, value=1)

start = (page - 1) * questions_per_page
end = start + questions_per_page
display_questions = questions[start:end]

# --------- 📘 Render Questions ---------
for idx, q in enumerate(display_questions, start=1):
    st.markdown(f"### Question {idx}")
    st.markdown(q["question"])
    selected = st.radio(f"Choose answer for Q{idx}:", q["options"], key=f"q{idx}")
    
    if st.button(f"Submit Q{idx}"):
        if selected == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")

    with st.expander("💡 Hint"):
        st.markdown(q["solution"])
