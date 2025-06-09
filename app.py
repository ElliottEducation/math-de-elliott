import streamlit as st
import os
import json

st.set_page_config(page_title="HSC Math Question Explorer", layout="centered")
st.title("📘 HSC Math Question Explorer")

QUESTION_DIR = "questions"

# 自动提取 year
years = sorted([d for d in os.listdir(QUESTION_DIR) if os.path.isdir(os.path.join(QUESTION_DIR, d))])
selected_year = st.selectbox("📅 Select Year", ["All"] + years)

# 自动提取 level
levels = []
if selected_year != "All":
    year_path = os.path.join(QUESTION_DIR, selected_year)
    levels = sorted([d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))])
selected_level = st.selectbox("📘 Select Level", ["All"] + levels)

# 自动提取 module 文件
modules = []
module_file_map = {}
if selected_year != "All" and selected_level != "All":
    module_path = os.path.join(QUESTION_DIR, selected_year, selected_level)
    files = [f for f in os.listdir(module_path) if f.endswith(".json")]
    modules = [f.replace(".json", "").replace("-", " ").title() for f in files]
    module_file_map = dict(zip(modules, files))

selected_module = st.selectbox("📚 Select Module", ["All"] + modules)

# 加载并展示题目
if selected_module != "All":
    json_path = os.path.join(QUESTION_DIR, selected_year, selected_level, module_file_map[selected_module])
    if st.button("🔍 Generate Questions"):
        with open(json_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
            for i, q in enumerate(questions, 1):
                st.markdown(f"### Q{i}: {q['question']}")
                for opt in q["options"]:
                    st.markdown(f"- {opt}")
                with st.expander("Answer & Solution"):
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.markdown(f"**Solution:** {q['solution']}")
