import streamlit as st
import os
import json
from dotenv import load_dotenv
from supabase_utils import supabase  # 你需要确保这个模块存在且正确

# ✅ 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(page_title="HSC Math Question Explorer", layout="centered")
st.title("📘 HSC Math Question Explorer")

# 登录状态初始化
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.user_role = "free"

# ========== 登录 / 注册 区域 ==========
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    # 登录界面
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

    # 注册界面
    with tab2:
    email = st.text_input("Register Email", key="reg_email")
    full_name = st.text_input("Full Name")
    if st.button("Register"):
        try:
            res = supabase.table("users").insert({
                "email": email,
                "full_name": full_name,
                "user_role": "free"
            }).execute()

            if res.status_code == 201:
                st.success("🎉 Registered successfully! Now login.")
            else:
                st.error(f"Registration failed. Server response: {res.data}")
        except Exception as e:
            st.error(f"❌ Error occurred: {e}")


    st.stop()  # ⛔ 停止渲染题库，直到登录成功

# ========== 登录成功后 ==========
st.success(f"Logged in as: {st.session_state.user} ({st.session_state.user_role})")
if st.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

# ========== 题库内容 ==========
QUESTION_DIR = "questions"

years = sorted([d for d in os.listdir(QUESTION_DIR) if os.path.isdir(os.path.join(QUESTION_DIR, d))])
if st.session_state.user_role == "free":
    years = years[:1]  # 限制免费用户只能浏览第一个年级

selected_year = st.selectbox("📅 Select Year", ["All"] + years)

levels = []
if selected_year != "All":
    levels = sorted([d for d in os.listdir(os.path.join(QUESTION_DIR, selected_year)) if os.path.isdir(os.path.join(QUESTION_DIR, selected_year, d))])
if st.session_state.user_role == "free":
    levels = levels[:1]  # 限制免费用户只能访问一个 level

selected_level = st.selectbox("📘 Select Level", ["All"] + levels)

modules = []
module_file_map = {}
if selected_year != "All" and selected_level != "All":
    module_path = os.path.join(QUESTION_DIR, selected_year, selected_level)
    files = [f for f in os.listdir(module_path) if f.endswith(".json")]
    modules = [f.replace(".json", "").replace("-", " ").title() for f in files]
    module_file_map = dict(zip(modules, files))

    if st.session_state.user_role == "free":
        modules = modules[:2]  # 限制免费用户最多浏览2个模块

selected_module = st.selectbox("📚 Select Module", ["All"] + modules)

if selected_module != "All":
    json_path = os.path.join(QUESTION_DIR, selected_year, selected_level, module_file_map[selected_module])
    if st.button("🔍 Generate Questions"):
        with open(json_path, "r", encoding="utf-8") as f:
            questions = json.load(f)

            if st.session_state.user_role == "free":
                questions = questions[:3]
                st.info("🆓 Free users can view 3 questions per module.")

            for i, q in enumerate(questions, 1):
                st.markdown(f"### Q{i}: {q['question']}")
                for opt in q["options"]:
                    st.markdown(f"- {opt}")
                with st.expander("Answer & Solution"):
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.markdown(f"**Solution:** {q['solution']}")
