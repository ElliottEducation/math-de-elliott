import streamlit as st
import json
import random
import os
from utils.question_loader import load_questions




# -------------------------
# Page Title and Layout
# -------------------------
st.set_page_config(page_title="HSC Math Question Bank", layout="wide")
st.title("📘 HSC Math Question Explorer")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Filter Questions")

# Load JSON data
question_dir = "questions"
question_files = [f for f in os.listdir(question_dir) if f.endswith(".json")]

all_questions = []
for file in question_files:
    with open(os.path.join(question_dir, file), "r", encoding="utf-8") as f:
        data = json.load(f)
        all_questions.extend(data)

# Extract unique filter options
years = sorted(set(q["year"] for q in all_questions))
levels = sorted(set(q["level"] for q in all_questions))
chapters = sorted(set(q["chapter"] for q in all_questions))

# Sidebar selectors
selected_year = st.sidebar.selectbox("📅 Select Year", ["All"] + years)
selected_level = st.sidebar.selectbox("📘 Select Level", ["All"] + levels)
selected_chapter = st.sidebar.selectbox("📚 Select Module", ["All"] + chapters)

# Filter logic
filtered_questions = [
    q for q in all_questions
    if (selected_year == "All" or q["year"] == selected_year)
    and (selected_level == "All" or q["level"] == selected_level)
    and (selected_chapter == "All" or q["chapter"] == selected_chapter)
]

# -------------------------
# Display Results
# -------------------------
if not filtered_questions:
    st.warning("No questions match your current filters.")
else:
    for idx, q in enumerate(filtered_questions, start=1):
        with st.expander(f"Q{idx}: {q['question']}"):
            for i, option in enumerate(q["options"]):
                st.write(f"({chr(65 + i)}) {option}")
            st.markdown(f"**✅ Answer**: `{q['answer']}`")
            st.markdown(f"**🧠 Explanation**: {q['solution']}")
            st.markdown(
                f"*Difficulty: `{q['difficulty']}` | Year: `{q['year']}` | Level: `{q['level']}`*"
            )
