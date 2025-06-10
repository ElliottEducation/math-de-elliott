import json
import os
import streamlit as st

def load_all_questions():
    """加载所有问题数据"""
    questions = []
    
    # 定义可能的数据文件路径
    possible_paths = [
        "data",           # 通常的数据文件夹
        "questions",      # 问题文件夹
        "json_files",     # JSON文件夹
        ".",              # 当前目录
        "utils/data",     # utils下的数据文件夹
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            # 获取所有JSON文件
            json_files = [f for f in os.listdir(path) if f.endswith('.json')]
            
            for filename in json_files:
                try:
                    file_path = os.path.join(path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # 处理不同的数据格式
                        if isinstance(data, list):
                            # 如果是列表，直接扩展
                            questions.extend(data)
                        elif isinstance(data, dict):
                            # 如果是单个对象，添加到列表
                            questions.append(data)
                        else:
                            print(f"警告: 文件 {filename} 包含未知数据格式")
                            
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误 {filename}: {e}")
                except Exception as e:
                    print(f"读取文件 {filename} 时出错: {e}")
    
    return questions

def get_available_options(questions=None):
    """从问题中提取可用选项"""
    if questions is None:
        questions = load_all_questions()
    
    years = set()
    levels = set()
    topics = set()
    difficulties = set()
    
    for question in questions:
        # 提取年级
        if 'year' in question and question['year']:
            years.add(str(question['year']))
        
        # 提取级别
        if 'level' in question and question['level']:
            levels.add(str(question['level']))
        
        # 提取主题 (支持 chapter 和 topic 字段)
        if 'chapter' in question and question['chapter']:
            topics.add(str(question['chapter']))
        elif 'topic' in question and question['topic']:
            topics.add(str(question['topic']))
        
        # 提取难度
        if 'difficulty' in question and question['difficulty']:
            difficulties.add(str(question['difficulty']))
    
    return {
        'years': sorted(list(years)),
        'levels': sorted(list(levels)),
        'topics': sorted(list(topics)),
        'difficulties': sorted(list(difficulties))
    }

def load_questions_by_filters(year=None, level=None, topic=None, difficulty=None):
    """根据筛选条件加载问题"""
    all_questions = load_all_questions()
    filtered_questions = []
    
    for question in all_questions:
        # 检查年级
        if year and str(question.get('year', '')) != str(year):
            continue
        
        # 检查级别
        if level and str(question.get('level', '')) != str(level):
            continue
        
        # 检查主题
        question_topic = question.get('chapter') or question.get('topic', '')
        if topic and str(question_topic) != str(topic):
            continue
        
        # 检查难度
        if difficulty and str(question.get('difficulty', '')) != str(difficulty):
            continue
        
        filtered_questions.append(question)
    
    return filtered_questions

def validate_question_format(question):
    """验证问题格式是否正确"""
    required_fields = ['question']
    optional_fields = ['options', 'answer', 'solution', 'explanation', 'year', 'level', 'chapter', 'topic', 'difficulty']
    
    # 检查必需字段
    for field in required_fields:
        if field not in question:
            return False, f"缺少必需字段: {field}"
    
    # 验证选项格式
    if 'options' in question:
        options = question['options']
        if not isinstance(options, (list, dict)):
            return False, "选项格式不正确，应为列表或字典"
    
    return True, "格式正确"

def get_question_stats():
    """获取问题数据统计"""
    questions = load_all_questions()
    options = get_available_options(questions)
    
    stats = {
        'total_questions': len(questions),
        'years': len(options['years']),
        'levels': len(options['levels']),
        'topics': len(options['topics']),
        'difficulties': len(options['difficulties']),
        'available_options': options
    }
    
    return stats
