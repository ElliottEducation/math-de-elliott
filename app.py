import streamlit as st
import json
import random
import os
import re
import inspect

# 临时的数据加载函数，用于调试
def load_all_questions_debug():
    """调试版本的数据加载函数"""
    questions = []
    
    # 检查可能的数据文件位置
    possible_paths = [
        "data",
        "questions",
        ".",
        "utils",
        "json_files"
    ]
    
    st.write("🔍 开始搜索数据文件...")
    
    for path in possible_paths:
        st.write(f"检查路径: {path}")
        if os.path.exists(path):
            st.write(f"✅ 路径存在: {path}")
            files = [f for f in os.listdir(path) if f.endswith('.json')]
            st.write(f"找到 JSON 文件: {files}")
            
            for filename in files:
                try:
                    file_path = os.path.join(path, filename)
                    st.write(f"正在读取: {file_path}")
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        st.write(f"文件 {filename} 数据类型: {type(data)}")
                        
                        if isinstance(data, list):
                            questions.extend(data)
                            st.write(f"从 {filename} 加载了 {len(data)} 个问题")
                        elif isinstance(data, dict):
                            questions.append(data)
                            st.write(f"从 {filename} 加载了 1 个问题")
                        else:
                            st.warning(f"未知数据格式在文件 {filename}")
                            
                except Exception as e:
                    st.error(f"读取文件 {filename} 时出错: {str(e)}")
        else:
            st.write(f"❌ 路径不存在: {path}")
    
    st.write(f"总共加载了 {len(questions)} 个问题")
    return questions

def create_sample_data():
    """创建示例数据用于测试"""
    sample_questions = [
        {
            "chapter": "Differentiation",
            "question": "Find the derivative of f(x) = 3x^2 + 2x - 5",
            "options": {
                "0": "6x + 2",
                "1": "3x + 2", 
                "2": "6x - 2",
                "3": "6x"
            },
            "answer": "6x + 2",
            "solution": "Apply basic rules: f'(x) = d/dx(3x^2) + d/dx(2x) - d/dx(5) = 6x + 2 - 0 = 6x + 2",
            "difficulty": "easy",
            "year": "year11",
            "level": "extension1",
            "source_file": "differentiation.json"
        },
        {
            "chapter": "Integration", 
            "question": "Find ∫(2x + 1)dx",
            "options": {
                "0": "x^2 + x + C",
                "1": "2x^2 + x + C",
                "2": "x^2 + x",
                "3": "2x + C"
            },
            "answer": "x^2 + x + C",
            "solution": "∫(2x + 1)dx = ∫2x dx + ∫1 dx = x^2 + x + C",
            "difficulty": "easy",
            "year": "year12",
            "level": "advanced",
            "source_file": "integration.json"
        },
        {
            "chapter": "Algebra",
            "question": "Solve for x: 2x + 5 = 13",
            "options": {
                "0": "x = 4",
                "1": "x = 8",
                "2": "x = 6", 
                "3": "x = 9"
            },
            "answer": "x = 4",
            "solution": "2x + 5 = 13 → 2x = 8 → x = 4",
            "difficulty": "easy",
            "year": "year10",
            "level": "standard",
            "source_file": "algebra.json"
        }
    ]
    return sample_questions

def extract_options_from_questions(questions):
    """从问题数据中提取可用选项 - 增强调试版本"""
    st.write("🔧 开始分析问题数据...")
    
    years = set()
    levels = set()
    topics = set()
    difficulties = set()
    
    st.write(f"正在处理 {len(questions)} 个问题")
    
    # 显示前几个问题的结构
    if questions:
        st.write("📋 前3个问题的数据结构:")
        for i, question in enumerate(questions[:3]):
            st.json(question)
    
    for i, question in enumerate(questions):
        # 检查年级
        if 'year' in question and question['year']:
            years.add(str(question['year']))
            
        # 检查级别  
        if 'level' in question and question['level']:
            levels.add(str(question['level']))
            
        # 检查主题 (可能是 chapter 或 topic)
        if 'chapter' in question and question['chapter']:
            topics.add(str(question['chapter']))
        elif 'topic' in question and question['topic']:
            topics.add(str(question['topic']))
            
        # 检查难度
        if 'difficulty' in question and question['difficulty']:
            difficulties.add(str(question['difficulty']))
    
    result = {
        'years': sorted(list(years)),
        'levels': sorted(list(levels)), 
        'topics': sorted(list(topics)),
        'difficulties': sorted(list(difficulties))
    }
    
    st.write("✅ 提取的选项:")
    st.json(result)
    
    return result

def display_question_with_latex(question_data, i):
    """显示单个问题，支持LaTeX渲染"""
    st.write(f"**Q{i}:** {question_data.get('question', '')}")
    
    # 显示选项
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
            if 'solution' in question_data:
                st.write(f"**解释:** {question_data['solution']}")
            elif 'explanation' in question_data:
                st.write(f"**解释:** {question_data['explanation']}")

def main():
    st.set_page_config(
        page_title="HSC Math Question Explorer",
        page_icon="🧮",
        layout="wide"
    )
    
    st.title("🧮 HSC Math Question Explorer")
    st.markdown("*A lightweight, elegant HSC math question generator built with Streamlit*")
    
    # 添加调试模式选择
    debug_mode = st.checkbox("🔧 调试模式", value=True)
    use_sample_data = st.checkbox("📝 使用示例数据", value=False)
    
    # 加载问题数据
    if use_sample_data:
        st.info("🔄 使用示例数据进行测试...")
        all_questions = create_sample_data()
        st.success(f"✅ 成功创建 {len(all_questions)} 个示例问题")
    else:
        st.info("🔄 正在加载实际数据...")
        try:
            # 尝试使用原始的加载函数
            try:
                from utils.question_loader import load_all_questions
                all_questions = load_all_questions()
                st.success(f"✅ 通过 utils.question_loader 加载了 {len(all_questions)} 个问题")
            except ImportError as e:
                st.warning(f"⚠️ 无法导入 utils.question_loader: {e}")
                st.info("🔄 使用调试加载函数...")
                all_questions = load_all_questions_debug()
            except Exception as e:
                st.error(f"❌ utils.question_loader 出错: {e}")
                st.info("🔄 使用调试加载函数...")
                all_questions = load_all_questions_debug()
                
        except Exception as e:
            st.error(f"❌ 加载问题时出错: {str(e)}")
            st.info("🔄 切换到示例数据...")
            all_questions = create_sample_data()
    
    if not all_questions:
        st.error("❌ 没有可用的问题数据")
        st.info("💡 建议启用'使用示例数据'选项进行测试")
        return
    
    # 获取可用选项
    try:
        available_options = extract_options_from_questions(all_questions)
    except Exception as e:
        st.error(f"❌ 提取选项时出错: {str(e)}")
        return
    
    # 检查选项是否为空
    if not any(available_options.values()):
        st.error("❌ 没有找到任何可用的筛选选项")
        st.info("请检查数据格式是否正确")
        return
    
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
        if selected_years and str(question.get('year', '')) not in selected_years:
            continue
        
        # 检查级别
        if selected_levels and str(question.get('level', '')) not in selected_levels:
            continue
        
        # 检查主题 (支持 chapter 和 topic)
        question_topic = question.get('chapter') or question.get('topic', '')
        if selected_topics and str(question_topic) not in selected_topics:
            continue
        
        # 检查难度
        if selected_difficulties and str(question.get('difficulty', '')) not in selected_difficulties:
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
        
        if debug_mode:
            st.subheader("🔧 调试信息")
            st.write("当前工作目录:", os.getcwd())
            st.write("目录下的文件:", os.listdir('.'))

if __name__ == "__main__":
    main()
