import streamlit as st
import json
import random
from utils.question_loader import load_questions

st.set_page_config(page_title="Math de Elliott", layout="wide")
st.title("🧠 Math de Elliott")

level = st.selectbox("Select Level", ["Standard2", "Extension1", "Extension2"])
section_options = {
    "Standard2": ["Functions"],
    "Extension1": ["Derivatives"],
    "Extension2": ["Integrals"]
}
section = st.selectbox("Select Section", section_options[level])

if "questions" not in st.session_state:
    st.session_state.questions = []

if st.button("Generate Questions"):
    st.session_state.questions = load_questions(level, section, 10)

if st.session_state.questions:
    st.markdown(f"### Showing 10 Questions for {level} - {section}")
    for i, q in enumerate(st.session_state.questions, 1):
        st.markdown(f"**Q{i}. {q['question']}**")
        with st.expander("Show Answer & Explanation"):
            st.markdown(f"✅ **Answer:** {q['answer']}")
            st.markdown(f"🧠 *Explanation:* {q['explanation']}")
        st.markdown("---")

    if st.button("More Questions?"):
        st.session_state.questions = load_questions(level, section, 10)
