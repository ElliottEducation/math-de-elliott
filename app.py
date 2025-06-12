import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.question_loader import load_questions

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Math de Elliott – HSC Practice Questions", layout="wide")
st.markdown("""
    <h1 style='font-size: 36px;'>📘 Math de Elliott – HSC Practice Questions</h1>
""", unsafe_allow_html=True)

# --------- 🔐 Simulated Subscription ---------
is_subscribed = False
free_modules = [
    ("year12", "extension1", "trigonometric"),
    ("year12", "extension2", "harder_questions")
]

# Session state setup
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = 1

# ---- Login/Register Logic ----
def login_section():
    st.subheader("🔐 Login or Register")

    with st.container():
        st.markdown("""
        <div style="background-color:#eaf2fb; padding:10px; border-radius:8px;">
        <b>🖋️ Free demo chapters available:</b><br>
        • Year 12 Extension 1 → <code>trigonometric</code><br>
        • Year 12 Extension 2 → <code>harder_questions</code><br><br>
        👉 Try these before subscribing!
        </div>
        """, unsafe_allow_html=True)

    tabs = st.tabs(["🔑 Login", "🆕 Register"])

    with tabs[0]:
        st.subheader("🔐 Login to Your Account")
        login_email = st.text_input("Login Email", placeholder="you@example.com", key="login_email")
        if st.button("Login"):
            response = supabase.auth.sign_in_with_otp({"email": login_email})
            st.success(f"✅ Welcome, {login_email}! Please check your inbox for a login link.")
            st.session_state.user = login_email  # Simulate login

    with tabs[1]:
        st.subheader("🆕 Register a New Account")
        register_email = st.text_input("Register Email", placeholder="you@example.com", key="register_email")
        if st.button("Register"):
            response = supabase.auth.sign_up({"email": register_email})
            if response.get("error"):
                st.error("❌ Registration failed. This email may already be registered.")
            else:
                st.success("✅ Registered successfully! Please check your email to verify.")

if not st.session_state.user:
    login_section()
    st.stop()

# ---- Main App Logic ----
st.markdown("---")
st.subheader("📚 Select Year / Level / Module")

col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("🗓 Select Year", ["year11", "year12"], index=1)
with col2:
    level = st.selectbox("📘 Select Level", ["extension1", "extension2"], index=0)
with col3:
    module = st.selectbox("📂 Select Module", sorted(
        [f.replace(".json", "") for f in os.listdir(f"questions/{year}/{level}") if f.endswith(".json")]
    ))

# Load and Display Questions
question_path = f"questions/{year}/{level}/{module}.json"
questions = load_questions(question_path)

if not questions:
    st.error("❌ No questions found in this module.")
    st.stop()

# Restrict content if not subscribed and not demo module
if not is_subscribed and (year, level, module) not in free_modules:
    st.warning("⚠️ This is a premium module. Only 3 sample questions are shown.")
    questions = questions[:3]

# Pagination
questions_per_page = 5
start = (st.session_state.page - 1) * questions_per_page
end = start + questions_per_page
paged_questions = questions[start:end]

# Render Questions
for idx, q in enumerate(paged_questions):
    st.markdown(f"### Question {start + idx + 1}")
    st.markdown(q["question"])
    selected = st.radio(f"Choose your answer for Q{idx+1}:", q["options"], key=f"q{idx}")
    if st.button(f"Submit Q{idx+1}"):
        if selected == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")
    with st.expander("💡 Hint"):
        st.markdown(q["hint"])

# Page navigation
st.markdown("---")
col_left, col_right = st.columns([1, 1])
with col_left:
    if st.button("⬅️ Previous") and st.session_state.page > 1:
        st.session_state.page -= 1
with col_right:
    if st.button("Next ➡️") and end < len(questions):
        st.session_state.page += 1
