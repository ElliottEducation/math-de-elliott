import streamlit as st
import json
import os

# --- Page Configuration ---
st.set_page_config(page_title="Math de Elliott", layout="centered")

st.title("📘 Math de Elliott – HSC Practice Questions")
st.markdown("Practice HSC Mathematics by selecting a topic. Each page shows 5 questions with hints.")

# --- Load available question files ---
question_dir = "questions"
available_paths = []
for root, _, files in os.walk(question_dir):
    for file in files:
        if file.endswith(".json"):
            relative_path = os.path.join(root, file).replace("\\", "/")
            available_paths.append(relative_path)

if not available_paths:
    st.warning("No question files found. Please add .json files to the 'questions/' directory.")
    st.stop()

# --- Select a question set ---
selected_path = st.selectbox("Select a question set:", available_paths)

# --- Load questions ---
try:
    with open(selected_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
except Exception as e:
    st.error(f"Failed to load questions: {e}")
    st.stop()

# --- Pagination (5 per page) ---
questions_per_page = 5
total_questions = len(questions)
total_pages = (total_questions + questions_per_page - 1) // questions_per_page

page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
start_idx = (page - 1) * questions_per_page
end_idx = min(start_idx + questions_per_page, total_questions)

# --- Display questions ---
for idx in range(start_idx, end_idx):
    q = questions[idx]
    st.markdown(f"### Question {idx + 1}")

    # Display question
    try:
        st.latex(q["question"])
    except:
        st.markdown(f"**{q['question']}**")

    # Display options if available
    if "options" in q:
        user_answer = st.radio("Your answer:", q["options"], key=f"q-{idx}")
        if st.button(f"Submit Q{idx + 1}"):
            if user_answer == q["answer"]:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: **{q['answer']}**")

        if "solution" in q:
            with st.expander("💡 Hint"):
                try:
                    st.latex(q["solution"])
                except:
                    st.markdown(q["solution"])

    else:
        st.info("⚠️ This question has no answer options.")

    st.markdown("---")
