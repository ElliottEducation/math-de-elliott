import streamlit as st
import json
import os
import random
from utils.question_loader import load_questions_from_directory

st.set_page_config(page_title="Math de Elliott – HSC Practice Questions")

st.title("📘 Math de Elliott – HSC Practice Questions")
st.markdown("Practice HSC Mathematics by selecting year, level, and topic. Each page shows 5 questions with hints.")

# Load the full question tree structure
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

# Step 1: Dropdown menus
selected_year = st.selectbox("🎯 Select Year", sorted(question_tree.keys()))
selected_level = st.selectbox("📘 Select Level", sorted(question_tree[selected_year].keys()))
selected_module = st.selectbox("🧠 Select Module", sorted(question_tree[selected_year][selected_level]))

# Step 2: Load selected file
json_path = os.path.join(BASE_DIR, selected_year, selected_level, f"{selected_module}.json")

questions = []
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

# Step 3: Pagination
questions_per_page = 5
total_pages = (len(questions) - 1) // questions_per_page + 1
page = st.number_input("📄 Page", min_value=1, max_value=max(1, total_pages), value=1)

start = (page - 1) * questions_per_page
end = start + questions_per_page
display_questions = questions[start:end]

# Step 4: Show each question
for idx, q in enumerate(display_questions, start=1):
    st.markdown(f"### Question {idx}")
    st.markdown(q["question"])
    selected_option = st.radio(f"Select your answer for Q{idx}:", q["options"], key=f"q{idx}")
    
    if st.button(f"Submit Q{idx}"):
        if selected_option == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")
    
    with st.expander("💡 Hint"):
        st.markdown(q["solution"])
