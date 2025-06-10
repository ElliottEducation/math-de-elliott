# Math de Elliott - LaTeX 渲染修复方案
# 这个文件包含了修复您的 Streamlit 应用中 LaTeX 公式渲染问题的完整解决方案

import streamlit as st
import json
import random
import re

def load_questions_from_json(file_path):
    """加载JSON题目数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"找不到文件: {file_path}")
        return []

def process_latex_text(text):
    """
    处理文本中的LaTeX公式
    将括号包围的数学表达式转换为LaTeX格式
    """
    if not text:
        return text
    
    # 将 ( ... ) 包围的数学表达式转换为 $...$
    # 匹配模式：\( ... \) 或 ( ... ) 其中包含数学符号
    patterns = [
        (r'\\\((.*?)\\\)', r'$\1$'),  # \( ... \) -> $ ... $
        (r'\\\[(.*?)\\\]', r'$$\1$$'),  # \[ ... \] -> $$ ... $$
        # 匹配包含数学符号的括号表达式
        (r'\(\s*([^()]*(?:[x²³⁴⁵⁶⁷⁸⁹⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉∞π∑∫≤≥≠±×÷√∂∇∆Δ∴∵∝∈∉⊂⊃∪∩∅ℝℕℤℚℂ°′″αβγδεζηθικλμνξπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΠΡΣΤΥΦΧΨΩ^_=+\-*/\\]|f[\'″‴]?|[a-zA-Z]+\'*)[^()]*)\s*\)', r'$\1$')
    ]
    
    processed_text = text
    for pattern, replacement in patterns:
        processed_text = re.sub(pattern, replacement, processed_text)
    
    # 特殊处理常见的数学表达式
    math_replacements = {
        'x^2': 'x^2',
        'x^3': 'x^3', 
        'f\'(x)': "f'(x)",
        'f\'\'(x)': "f''(x)",
        'sin(x)': r'\sin(x)',
        'cos(x)': r'\cos(x)',
        'tan(x)': r'\tan(x)',
        'ln(x)': r'\ln(x)',
        'log(x)': r'\log(x)',
        'sqrt': r'\sqrt',
        'pi': r'\pi',
        'theta': r'\theta',
        'alpha': r'\alpha',
        'beta': r'\beta',
        'gamma': r'\gamma',
        'infinity': r'\infty',
        '+-': r'\pm',
        '<=': r'\leq',
        '>=': r'\geq',
        '!=': r'\neq',
    }
    
    for old, new in math_replacements.items():
        processed_text = processed_text.replace(old, new)
    
    return processed_text

def display_question_with_latex(question_data, question_number):
    """
    显示带有LaTeX渲染的题目
    question_data: 题目数据字典
    question_number: 题目编号
    """
    # 处理题干
    question_text = process_latex_text(question_data.get('question', ''))
    st.markdown(f"**Q{question_number}:** {question_text}")
    
    # 显示选项
    options = question_data.get('options', {})
    if options:
        col1, col2 = st.columns(2)
        option_keys = sorted(options.keys())
        
        with col1:
            for i in range(0, len(option_keys), 2):
                key = option_keys[i]
                option_text = process_latex_text(options[key])
                st.markdown(f"**{key}.** {option_text}")
        
        with col2:
            for i in range(1, len(option_keys), 2):
                if i < len(option_keys):
                    key = option_keys[i]
                    option_text = process_latex_text(options[key])
                    st.markdown(f"**{key}.** {option_text}")
    
    # 显示答案和解释（可折叠）
    with st.expander("📖 答案与解释"):
        answer = question_data.get('answer', 'N/A')
        explanation = process_latex_text(question_data.get('explanation', '无解释'))
        
        st.markdown(f"**正确答案:** {answer}")
        st.markdown(f"**解释:** {explanation}")

def convert_json_to_latex_format(input_file, output_file):
    """
    将现有的JSON题库转换为LaTeX格式
    这个函数可以批量处理您的题库数据
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 处理每个题目
        for question in data:
            if 'question' in question:
                question['question'] = process_latex_text(question['question'])
            
            if 'options' in question:
                for key, value in question['options'].items():
                    question['options'][key] = process_latex_text(value)
            
            if 'explanation' in question:
                question['explanation'] = process_latex_text(question['explanation'])
        
        # 保存处理后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"转换过程中出错: {e}")
        return False

def main():
    """主应用程序"""
    st.set_page_config(
        page_title="🧮 HSC Math Question Explorer",
        page_icon="🧮",
        layout="wide"
    )
    
    st.title("🧮 HSC Math Question Explorer")
    st.markdown("*A lightweight, elegant HSC math question generator built with Streamlit*")
    
    # 侧边栏设置
    with st.sidebar:
        st.header("⚙️ 设置")
        
        # 年级选择
        year_options = ["year11", "year12"]
        selected_year = st.selectbox("📚 选择年级", year_options, key="year")
        
        # 级别选择  
        level_options = ["Standard2", "Extension1", "Extension2"]
        selected_level = st.selectbox("📊 选择级别", level_options, key="level")
        
        # 主题选择
        topic_options = ["Functions", "Derivatives", "Integrals", "Differentiation"]
        selected_topic = st.selectbox("🎯 选择主题", topic_options, key="topic")
        
        # 题目数量
        num_questions = st.slider("🔢 题目数量", 1, 10, 5)
        
        # 生成题目按钮
        generate_btn = st.button("🎲 生成题目", type="primary")
        
        # 数据转换工具
        st.markdown("---")
        st.subheader("🔧 数据转换工具")
        if st.button("转换现有JSON数据"):
            st.info("这个功能可以批量转换您现有的JSON题库，将数学表达式转换为LaTeX格式")
    
    # 主内容区域
    if generate_btn or 'questions' not in st.session_state:
        # 模拟加载题目（您需要替换为实际的JSON文件路径）
        sample_questions = [
            {
                "question": "Find the derivative of $f(x) = 3x^2 + 2x - 5$",
                "options": {
                    "A": "$f'(x) = 6x + 2$",
                    "B": "$f'(x) = 3x + 2$", 
                    "C": "$f'(x) = 6x - 2$",
                    "D": "$f'(x) = 6x$"
                },
                "answer": "A",
                "explanation": "使用幂规则：$\\frac{d}{dx}(ax^n) = nax^{n-1}$。因此 $\\frac{d}{dx}(3x^2) = 6x$，$\\frac{d}{dx}(2x) = 2$，常数项的导数为0。"
            },
            {
                "question": "If $f(x) = \\sin(x)$, what is $f''(x)$?",
                "options": {
                    "A": "$\\cos(x)$",
                    "B": "$-\\sin(x)$",
                    "C": "$-\\cos(x)$",
                    "D": "$\\sin(x)$"
                },
                "answer": "B", 
                "explanation": "$f'(x) = \\cos(x)$，然后 $f''(x) = \\frac{d}{dx}(\\cos(x)) = -\\sin(x)$"
            },
            {
                "question": "Evaluate $\\int x^2 \\, dx$",
                "options": {
                    "A": "$\\frac{x^3}{3} + C$",
                    "B": "$x^3 + C$",
                    "C": "$\\frac{x^3}{2} + C$", 
                    "D": "$2x + C$"
                },
                "answer": "A",
                "explanation": "使用幂规则积分公式：$\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C$，当 $n = 2$ 时，得到 $\\frac{x^3}{3} + C$"
            }
        ]
        
        # 随机选择题目
        st.session_state.questions = random.sample(
            sample_questions, 
            min(num_questions, len(sample_questions))
        )
    
    # 显示题目
    if 'questions' in st.session_state:
        st.markdown("---")
        for i, question in enumerate(st.session_state.questions, 1):
            display_question_with_latex(question, i)
            if i < len(st.session_state.questions):
                st.markdown("---")
        
        # 更多题目按钮
        if st.button("🔄 更多题目?", type="secondary"):
            st.rerun()

if __name__ == "__main__":
    main()

