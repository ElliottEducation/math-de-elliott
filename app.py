import streamlit as st
import os
import json
from supabase_utils import supabase
from dotenv import load_dotenv

# 加载 .env 文件（本地调试时用）
load_dotenv()

# 设置页面信息
st.set_page_config(page_title="HSC Math Question Explorer", layout="centered")
st.title("📘 HSC Math Question Explorer")

# 初始化 Session State
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.user_role = "free"

# ========== 登录与注册 ==========
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        login_email = st.text_input("Login Email", key="login_email")
        if st.button("Login"):
            try:
                res = supabase.table("users").select("user_role").eq("email", login_email).execute()
                if res.data:
                    st.session_state.user = login_email
                    st.session_state.user_role = res.data[0]["user_role"]
                    st.success(f"✅ Welcome back, {login_email}!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Email not found. Please register.")
            except Exception as e:
                st.error(f"Login failed: {e}")

    with tab2:
        reg_email = st.text_input("Register Email", key="reg_email")
        full_name = st.text_input("Full Name")
        if st.button("Register"):
            try:
                res = supabase.table("users").insert({
                    "email": reg_email,
                    "full_name": full_name,
                    "user_role": "free"
                }).execute()
                if hasattr(res, "status_code") and res.status_code == 201:
                    st.success("🎉 Registered successfully! Now login.")
                else:
                    st.error("Registration failed. Email may already exist.")
            except Exception as e:
                st.error(f"Registration error: {e}")
    st.stop()

# ========== 登录成功后 ==========
st.success(f"Logged in as: {st.session_state.user} ({st.session_state.user_role})")
if st.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

# ========== 题库展示 ==========
QUESTION_DIR = "questions"

years = sorted([d for d in os.listdir(QUESTION_DIR) if os.path.isdir(os.path.join(QUESTION_DIR, d))])
selected_year = st.selectbox("📅 Select Year", ["All"] + years)

levels = []
if selected_year != "All":
    year_path = os.path.join(QUESTION_DIR, selected_year)
    levels = sorted([d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))])
selected_level = st.selectbox("📘 Select Level", ["All"] + levels)

modules = []
module_file_map = {}
if selected_year != "All" and selected_level != "All":
    module_path = os.path.join(QUESTION_DIR, selected_year, selected_level)
    files = [f for f in os.listdir(module_path) if f.endswith(".json")]
    modules = [f.replace(".json", "").replace("-", " ").title() for f in files]
    module_file_map = dict(zip(modules, files))

selected_module = st.selectbox("📚 Select Module", ["All"] + modules)

if selected_module != "All":
    json_path = os.path.join(QUESTION_DIR, selected_year, selected_level, module_file_map[selected_module])
    if st.button("🔍 Generate Questions"):
        with open(json_path, "r", encoding="utf-8") as f:
            questions = json.load(f)

            if st.session_state.user_role == "free":
                questions = questions[:3]
                st.info("🆓 Free users can view only 3 questions per module.")

            for i, q in enumerate(questions, 1):
                st.markdown(f"### Q{i}: {q['question']}")
                for opt in q["options"]:
                    st.markdown(f"- {opt}")
                with st.expander("Answer & Solution"):
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.markdown(f"**Solution:** {q['solution']}")
