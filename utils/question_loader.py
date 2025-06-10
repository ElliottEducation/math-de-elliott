import json
import os
import random

def load_all_questions():
    """加载所有题目数据从文件夹结构"""
    all_questions = []
    questions_dir = "questions"
    
    if not os.path.exists(questions_dir):
        print(f"错误: 找不到 {questions_dir} 文件夹")
        return []
    
    # 遍历年级文件夹 (year11, year12)
    for year_folder in os.listdir(questions_dir):
        year_path = os.path.join(questions_dir, year_folder)
        
        if not os.path.isdir(year_path):
            continue
            
        # 遍历课程类型文件夹 (extension1, extension2, standard2)
        for course_folder in os.listdir(year_path):
            course_path = os.path.join(year_path, course_folder)
            
            if not os.path.isdir(course_path):
                continue
                
            # 读取所有JSON文件
            for filename in os.listdir(course_path):
                if not filename.endswith('.json'):
                    continue
                    
                file_path = os.path.join(course_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # 确保数据是列表格式
                        if isinstance(data, dict):
                            data = [data]
                        elif not isinstance(data, list):
                            continue
                            
                        # 为每个问题添加元数据
                        for question in data:
                            question['year'] = year_folder
                            question['level'] = course_folder
                            question['chapter'] = filename.replace('.json', '').replace('-', ' ').title()
                            question['source_file'] = filename
                            
                            # 如果没有难度信息，设置默认值
                            if 'difficulty' not in question:
                                question['difficulty'] = 'medium'
                                
                        all_questions.extend(data)
                        
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
                    continue
    
    print(f"成功加载了 {len(all_questions)} 个问题")
    return all_questions

def load_questions(level, section, n=10):
    """兼容旧版本的加载函数"""
    all_questions = load_all_questions()
    
    # 根据级别筛选
    if level:
        filtered = [q for q in all_questions if q.get('level', '').lower() == level.lower()]
    else:
        filtered = all_questions
    
    # 根据章节筛选
    if section:
        filtered = [q for q in filtered if section.lower() in q.get('chapter', '').lower()]
    
    # 随机选择
    return random.sample(filtered, min(n, len(filtered)))

def get_available_options():
    """获取所有可用的选项"""
    all_questions = load_all_questions()
    
    if not all_questions:
        return {
            'years': [],
            'levels': [],
            'chapters': [],
            'difficulties': []
        }
    
    years = sorted(list(set(q.get('year', '') for q in all_questions if q.get('year'))))
    levels = sorted(list(set(q.get('level', '') for q in all_questions if q.get('level'))))
    chapters = sorted(list(set(q.get('chapter', '') for q in all_questions if q.get('chapter'))))
    difficulties = sorted(list(set(q.get('difficulty', '') for q in all_questions if q.get('difficulty'))))
    
    return {
        'years': years,
        'levels': levels,
        'chapters': chapters,
        'difficulties': difficulties
    }

# 测试函数
if __name__ == "__main__":
    # 测试加载
    questions = load_all_questions()
    print(f"加载了 {len(questions)} 个问题")
    
    if questions:
        print("\n示例问题:")
        for i, q in enumerate(questions[:3]):
            print(f"{i+1}. 年级: {q.get('year')}, 级别: {q.get('level')}, 章节: {q.get('chapter')}")
            print(f"   问题: {q.get('question', 'N/A')[:50]}...")
            print()
    
    # 测试选项
    options = get_available_options()
    print("可用选项:")
    for key, values in options.items():
        print(f"{key}: {values}")
