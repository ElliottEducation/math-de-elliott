# ====== 登录模块 + 题库模块 ======

import streamlit as st
import os
import json
from supabase_utils import supabase  # ✅ 确保此模块存在并正确引用 Supabase client

# 页面配置
st.set_page_config(page_title="HSC Math Question Explorer", layout="centered")

# 登录状态初始化
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.user_role = "free"

# ====== 登录界面 ======
if st.session_state.user is None:
    st.title("🔐 Welcome to Math de Elliott")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        email = st.text_input("Login Email", key="login_email")
        if st.button("Login"):
            res = supabase.table("users").select("user_role").eq("email", email).execute()
            if res.data:
                st.session_state.user = email
                st.session_state.user_role = res.data[0]["user_role"]
                st.success(f"✅ Welcome back, {email}!")
                st.experimental_rerun()
            else:
                st.error("Email not found. Please register first.")

    with tab2:
        email = st.text_input("Register Email", key="reg_email")
        full_name = st.text_input("Full Name")
        if st.button("Register"):
            res = supabase.table("users").insert({
                "email": email,
                "full_name": full_name,
                "user_role": "free"
            }).execute()
            if res.status_code == 201:
                st.success("🎉 Registered successfully! Now login.")
            else:
                st.error("Registration failed. Email may already exist.")

    st.stop()  # ⛔ 停止后续题库显示，直到登录

# ====== 登录后内容区 ======
st.title("📘 HSC Math Question Explorer")
st.success(f"✅ Logged in as: {st.session_state.user} ({st.session_state.user_role})")
if st.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

# ====== 题库功能区 ======

QUESTION_DIR = "questions"

# 选择年级
years = sorted([d for d in os.listdir(QUESTION_DIR) if os.path.isdir(os.path.join(QUESTION_DIR, d))])
selected_year = st.selectbox("📅 Select Year", ["All"] + years)

# 选择级别
levels = []
if selected_year != "All":
    year_path = os.path.join(QUESTION_DIR, selected_year)
    levels = sorted([d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))])
selected_level = st.selectbox("📘 Select Level", ["All"] + levels)

# 选择模块
modules = []
module_file_map = {}
if selected_year != "All" and selected_level != "All":
    module_path = os.path.join(QUESTION_DIR, selected_year, selected_level)
    files = [f for f in os.listdir(module_path) if f.endswith(".json")]
    modules = [f.replace(".json", "").replace("-", " ").title() for f in files]
    module_file_map = dict(zip(modules, files))

selected_module = st.selectbox("📚 Select Module", ["All"] + modules)

# 显示题目
if selected_module != "All":
    json_path = os.path.join(QUESTION_DIR, selected_year, selected_level, module_file_map[selected_module])
    if st.button("🔍 Generate Questions"):
        with open(json_path, "r", encoding="utf-8") as f:
            questions = json.load(f)

            # 限制 free 用户最多查看前 3 道题
            if st.session_state.user_role == "free":
                questions = questions[:3]
                st.info("🆓 Free users can view 3 questions per module. Upgrade to Pro to unlock all!")

            for i, q in enumerate(questions, 1):
                st.markdown(f"### Q{i}: {q['question']}")
                for opt in q["options"]:
                    st.markdown(f"- {opt}")
                with st.expander("Answer & Solution"):
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.markdown(f"**Solution:** {q['solution']}")
