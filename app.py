import streamlit as st
import json
import random
import os
import re
import inspect
from utils.question_loader import load_all_questions, get_available_options

def extract_options_from_questions(questions):
    """从问题数据中提取可用选项"""
    years = set()
    levels = set()
    topics = set()
    difficulties = set()
    
    for question in questions:
        if 'year' in question and question['year']:
            years.add(question['year'])
        if 'level' in question and question['level']:
            levels.add(question['level'])
        if 'topic' in question and question['topic']:
            topics.add(question['topic'])
        if 'difficulty' in question and question['difficulty']:
            difficulties.add(question['difficulty'])
    
    return {
        'years': sorted(list(years)),
        'levels': sorted(list(levels)),
        'topics': sorted(list(topics)),
        'difficulties': sorted(list(difficulties))
    }

def display_question_with_latex(question_data, i):
    """显示单个问题，支持LaTeX渲染"""
    st.write(f"**Q{i}:** {question_data.get('question', '')}")
    
    # 显示处理
    options = question_data.get('options', [])
    if options:
        col1, col2 = st.columns(2)
        
        # 处理不同的数据格式
        if isinstance(options, dict):
            # 如果 options 是字典
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
                        
        elif isinstance(options, list):
            # 如果 options 是列表
            with col1:
                for i in range(0, len(options), 2):
                    option_letter = chr(65 + i)  # A, B, C, D...
                    st.markdown(f"**{option_letter}.** {options[i]}")
            
            with col2:
                for i in range(1, len(options), 2):
                    if i < len(options):
                        option_letter = chr(65 + i)  # A, B, C, D...
                        st.markdown(f"**{option_letter}.** {options[i]}")
    
    # 显示答案（如果存在）
    if 'answer' in question_data:
        with st.expander("查看答案"):
            st.write(f"**答案:** {question_data['answer']}")
            if 'explanation' in question_data:
                st.write(f"**解释:** {question_data['explanation']}")

def main():
    st.set_page_config(
        page_title="HSC Math Question Explorer",
        page_icon="🧮",
        layout="wide"
    )
    
    st.title("🧮 HSC Math Question Explorer")
    st.markdown("*A lightweight, elegant HSC math question generator built with Streamlit*")
    
    # 加载所有问题
    try:
        all_questions = load_all_questions()
        if not all_questions:
            st.error("无法加载问题数据，请检查数据文件。")
            return
        else:
            st.success(f"成功加载 {len(all_questions)} 道题目")
            # 显示第一个问题的结构以便调试
            if len(all_questions) > 0:
                st.write("第一个问题的数据结构:", all_questions[0])
    except Exception as e:
        st.error(f"加载问题时出错: {str(e)}")
        return
    
    # 获取可用选项
    try:
        # 检查 get_available_options 函数是否需要参数
        import inspect
        sig = inspect.signature(get_available_options)
        if len(sig.parameters) == 0:
            # 如果函数不需要参数
            available_options = get_available_options()
        else:
            # 如果函数需要参数
            available_options = get_available_options(all_questions)
    except Exception as e:
        st.error(f"获取选项时出错: {str(e)}")
        # 从 all_questions 中手动提取选项
        available_options = extract_options_from_questions(all_questions)
    
    # 侧边栏过滤器
    st.sidebar.header("筛选条件")
    
    # 年级过滤
    selected_years = st.sidebar.multiselect(
        "选择年级:",
        options=available_options.get('years', []),
        default=available_options.get('years', [])[:1] if available_options.get('years') else []
    )
    
    # 级别过滤
    selected_levels = st.sidebar.multiselect(
        "选择级别:",
        options=available_options.get('levels', []),
        default=available_options.get('levels', [])[:1] if available_options.get('levels') else []
    )
    
    # 主题过滤
    selected_topics = st.sidebar.multiselect(
        "选择主题:",
        options=available_options.get('topics', []),
        default=[]
    )
    
    # 难度过滤
    selected_difficulties = st.sidebar.multiselect(
        "选择难度:",
        options=available_options.get('difficulties', []),
        default=[]
    )
    
    # 问题数量
    num_questions = st.sidebar.slider(
        "生成问题数量:",
        min_value=1,
        max_value=min(20, len(all_questions)),
        value=3
    )
    
    # 过滤问题
    filtered_questions = []
    for question in all_questions:
        # 检查年级
        if selected_years and question.get('year') not in selected_years:
            continue
        
        # 检查级别
        if selected_levels and question.get('level') not in selected_levels:
            continue
        
        # 检查主题
        if selected_topics and question.get('topic') not in selected_topics:
            continue
        
        # 检查难度
        if selected_difficulties and question.get('difficulty') not in selected_difficulties:
            continue
        
        filtered_questions.append(question)
    
    # 生成按钮
    if st.sidebar.button("生成新题目", type="primary"):
        st.session_state.generated_questions = []
        if filtered_questions:
            selected_questions = random.sample(
                filtered_questions, 
                min(num_questions, len(filtered_questions))
            )
            st.session_state.generated_questions = selected_questions
        else:
            st.warning("没有符合条件的题目，请调整筛选条件。")
    
    # 显示当前筛选条件
    if any([selected_years, selected_levels, selected_topics, selected_difficulties]):
        filter_info = []
        if selected_years:
            filter_info.append(f"年级: {', '.join(map(str, selected_years))}")
        if selected_levels:
            filter_info.append(f"级别: {', '.join(selected_levels)}")
        if selected_topics:
            filter_info.append(f"主题: {', '.join(selected_topics)}")
        if selected_difficulties:
            filter_info.append(f"难度: {', '.join(selected_difficulties)}")
        
        st.info(f"当前筛选条件: {' | '.join(filter_info)}")
    
    # 显示可用题目数量
    st.info(f"符合条件的题目数量: {len(filtered_questions)}")
    
    # 显示生成的问题
    if hasattr(st.session_state, 'generated_questions') and st.session_state.generated_questions:
        st.success(f"已生成 {len(st.session_state.generated_questions)} 道题目！")
        
        for i, question in enumerate(st.session_state.generated_questions, 1):
            with st.container():
                st.markdown("---")
                display_question_with_latex(question, i)
    else:
        st.info("点击侧边栏的'生成新题目'按钮开始！")
    
    # 显示统计信息
    with st.expander("📊 数据统计"):
        st.write(f"总题目数量: {len(all_questions)}")
        st.write(f"可用年级: {', '.join(map(str, available_options.get('years', [])))}")
        st.write(f"可用级别: {', '.join(available_options.get('levels', []))}")
        st.write(f"可用主题: {', '.join(available_options.get('topics', []))}")
        st.write(f"可用难度: {', '.join(available_options.get('difficulties', []))}")

if __name__ == "__main__":
    main()
