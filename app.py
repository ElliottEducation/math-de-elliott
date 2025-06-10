import streamlit as st
import json
import random
import os
import re

def load_questions_from_json(file_path):
    """加载JSON题目数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"找不到文件: {file_path}")
        return []

def display_question_with_latex(question_data, question_number):
    """
    显示带有LaTeX渲染的题目
    """
    # 显示题干
    st.markdown(f"**Q{question_number}:** {question_data['question']}")
    
    # 显示选项
    options = question_data.get('options', {})
    if options:
        col1, col2 = st.columns(2)
        option_keys = sorted(options.keys())
        
        with col1:
            for i in range(0, len(option_keys), 2):
                key = option_keys[i]
                st.markdown(f"**{key}.** {options[key]}")
        
        with col2:
            for i in range(1, len(option_keys), 2):
                if i < len(option_keys):
                    key = option_keys[i]
                    st.markdown(f"**{key}.** {options[key]}")
    
    # 显示答案和解释（可折叠）
    with st.expander("📖 答案与解释"):
        answer = question_data.get('answer', 'N/A')
        correct_answer = question_data.get('correct_answer', '')
        solution = question_data.get('solution', '无解释')
        
        st.markdown(f"**正确答案:** {answer} - {correct_answer}")
        st.markdown(f"**解释:** {solution}")
        
        # 显示额外信息
        difficulty = question_data.get('difficulty', 'N/A')
        chapter = question_data.get('chapter', 'N/A')
        st.markdown(f"**难度:** {difficulty.title()} | **章节:** {chapter}")

def filter_questions(questions, year=None, level=None, chapter=None, difficulty=None):
    """根据条件筛选题目"""
    filtered = questions
    
    if year:
        filtered = [q for q in filtered if q.get('year') == year]
    if level:
        filtered = [q for q in filtered if q.get('level') == level]
    if chapter:
        filtered = [q for q in filtered if q.get('chapter') == chapter]
    if difficulty:
        filtered = [q for q in filtered if q.get('difficulty') == difficulty]
    
    return filtered

def main():
    """主应用程序"""
    st.set_page_config(
        page_title="🧮 HSC Math Question Explorer",
        page_icon="🧮",
        layout="wide"
    )
    
    st.title("🧮 HSC Math Question Explorer")
    st.markdown("*A lightweight, elegant HSC math question generator built with Streamlit*")
    
    # 加载题目数据
    questions_file = "questions.json"  # 您的JSON文件名
    all_questions = load_questions_from_json(questions_file)
    
    if not all_questions:
        st.error("无法加载题目数据。请确保questions.json文件存在。")
        return
    
    # 获取所有可用的选项值
    years = sorted(list(set(q.get('year', '') for q in all_questions if q.get('year'))))
    levels = sorted(list(set(q.get('level', '') for q in all_questions if q.get('level'))))
    chapters = sorted(list(set(q.get('chapter', '') for q in all_questions if q.get('chapter'))))
    difficulties = sorted(list(set(q.get('difficulty', '') for q in all_questions if q.get('difficulty'))))
    
    # 侧边栏设置
    with st.sidebar:
        st.header("⚙️ 筛选设置")
        
        # 年级选择
        selected_year = st.selectbox(
            "📚 选择年级", 
            ["All"] + years, 
            key="year"
        )
        if selected_year == "All":
            selected_year = None
        
        # 级别选择  
        selected_level = st.selectbox(
            "📊 选择级别", 
            ["All"] + levels, 
            key="level"
        )
        if selected_level == "All":
            selected_level = None
        
        # 章节选择
        selected_chapter = st.selectbox(
            "📖 选择章节", 
            ["All"] + chapters, 
            key="chapter"
        )
        if selected_chapter == "All":
            selected_chapter = None
        
        # 难度选择
        selected_difficulty = st.selectbox(
            "⭐ 选择难度", 
            ["All"] + difficulties, 
            key="difficulty"
        )
        if selected_difficulty == "All":
            selected_difficulty = None
        
        # 题目数量
        num_questions = st.slider("🔢 题目数量", 1, 10, 5)
        
        # 生成题目按钮
        generate_btn = st.button("🎲 生成题目", type="primary")
        
        # 显示统计信息
        st.markdown("---")
        st.subheader("📊 题库统计")
        filtered_count = len(filter_questions(
            all_questions, selected_year, selected_level, 
            selected_chapter, selected_difficulty
        ))
        st.markdown(f"**可用题目:** {filtered_count}/{len(all_questions)}")
    
    # 主内容区域
    if generate_btn or 'current_questions' not in st.session_state:
        # 筛选题目
        filtered_questions = filter_questions(
            all_questions, selected_year, selected_level, 
            selected_chapter, selected_difficulty
        )
        
        if not filtered_questions:
            st.warning("没有找到符合条件的题目。请调整筛选条件。")
            return
        
        # 随机选择题目
        selected_count = min(num_questions, len(filtered_questions))
        st.session_state.current_questions = random.sample(filtered_questions, selected_count)
        
        st.success(f"已生成 {selected_count} 道题目！")
    
    # 显示题目
    if 'current_questions' in st.session_state:
        st.markdown("---")
        
        # 显示当前筛选条件
        conditions = []
        if selected_year: conditions.append(f"年级: {selected_year}")
        if selected_level: conditions.append(f"级别: {selected_level}")
        if selected_chapter: conditions.append(f"章节: {selected_chapter}")
        if selected_difficulty: conditions.append(f"难度: {selected_difficulty}")
        
        if conditions:
            st.markdown(f"**当前筛选条件:** {' | '.join(conditions)}")
            st.markdown("---")
        
        # 显示题目
        for i, question in enumerate(st.session_state.current_questions, 1):
            display_question_with_latex(question, i)
            if i < len(st.session_state.current_questions):
                st.markdown("---")
        
        # 更多题目按钮
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 更多题目?", type="secondary"):
                st.rerun()

if __name__ == "__main__":
    main()
