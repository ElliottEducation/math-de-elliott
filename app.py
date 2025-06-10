import streamlit as st
import os
import json
from dotenv import load_dotenv
from supabase_utils import supabase  # ✅ 请确保该文件已正确配置

# ====== 环境配置 ======
load_dotenv()

# ====== 页面设置 ======
st.set_page_config(page_title="HSC Math Question Explorer", layout="centered")
st.title("📘 HSC Math Question Explorer")

# ====== 登录状态初始化 ======
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.user_role = "free"

# ====== 登录 / 注册区域 ======
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        email = st.text_input("Login Email", key="login_email")
        if st.button("Login"):
            res = supabase.table("users").select("user_role").eq("email", email).execute()
            if res.data:
                st.session_state.user = email
                st.session_state.user_role = res.data[0]["user_role"]
                st.success(f"✅ Welcome back, {email}!")
                st.rerun()
            else:
                st.error("Email not found. Please register first.")

    with tab2:
        email = st.text_input("Register Email", key="reg_email")
        full_name = st.text_input("Full Name")
        if st.button("Register"):
            if not email or not full_name:
                st.warning("Please fill in all fields.")
            else:
                res = supabase.table("users").insert({
                    "email": email,
                    "full_name": full_name,
                    "user_role": "free"
                }).execute()
                if res.data:
                    st.success("🎉 Registered successfully! Now login.")
                else:
                    st.error(f"Registration failed: {res.error}")
    st.stop()

# ====== 登录后欢迎 + 登出按钮 ======
st.success(f"Logged in as: {st.session_state.user} ({st.session_state.user_role})")
if st.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

# ====== 题库功能区 ======
QUESTION_DIR = "questions"

# 📅 自动提取 year
years = sorted([d for d in os.listdir(QUESTION_DIR) if os.path.isdir(os.path.join(QUESTION_DIR, d))])
selected_year = st.selectbox("📅 Select Year", ["All"] + years)

# 📘 自动提取 level
levels = []
if selected_year != "All":
    year_path = os.path.join(QUESTION_DIR, selected_year)
    levels = sorted([d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))])
selected_level = st.selectbox("📘 Select Level", ["All"] + levels)

# 📚 自动提取 module
modules = []
module_file_map = {}
if selected_year != "All" and selected_level != "All":
    module_path = os.path.join(QUESTION_DIR, selected_year, selected_level)
    files = [f for f in os.listdir(module_path) if f.endswith(".json")]
    all_modules = [f.replace(".json", "").replace("-", " ").title() for f in files]
    module_file_map = dict(zip(all_modules, files))

    # 🚧 限制 Free 用户最多看到前 2 个模块
    if st.session_state.user_role == "free":
        modules = all_modules[:2]
        st.warning("🆓 Free users can view 2 modules only. Upgrade to Pro for full access.")
    else:
        modules = all_modules

selected_module = st.selectbox("📚 Select Module", ["All"] + modules)

# ====== LaTeX 渲染函数 ======
def render_question(q, idx):
    option_labels = ['A', 'B', 'C', 'D']
    
    # ✅ 题干处理
    if "\\(" in q["question"] or "\\int" in q["question"] or "f(x)" in q["question"]:
        st.markdown(f"### Q{idx}: {q['question']}", unsafe_allow_html=True)
    else:
        st.markdown(f"### Q{idx}:")
        st.latex(q["question"])  # 如果是纯公式

    # ✅ 选项横向两列展示（使用 st.latex 保证渲染）
    st.markdown("**Options:**", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(q["options"]):
        with cols[i % 2]:
            st.markdown(f"**{option_labels[i]}.**", unsafe_allow_html=True)
            st.latex(opt)  # ✅ 永远用 st.latex() 来渲染数学选项

    # ✅ 答案与解析
    with st.expander("📘 Answer & Solution"):
        st.markdown("**✅ Answer:**", unsafe_allow_html=True)
        st.latex(q["answer"])
        st.markdown("**📝 Solution:**", unsafe_allow_html=True)
        st.latex(q["solution"])

    st.markdown("---")




# ====== 展示题目 ======
if selected_module != "All":
    json_path = os.path.join(QUESTION_DIR, selected_year, selected_level, module_file_map[selected_module])
    if st.button("🔍 Generate Questions"):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                questions = json.load(f)

            # 🆓 Free 用户最多查看 3 道题
            if st.session_state.user_role == "free":
                questions = questions[:3]
                st.info("🆓 Free users can view 3 questions per module.")

            for i, q in enumerate(questions, 1):
                render_question(q, i)
        except Exception as e:
            st.error(f"❌ Failed to load questions: {e}")
