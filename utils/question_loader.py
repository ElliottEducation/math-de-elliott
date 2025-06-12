import json

def load_questions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON in file: {file_path}")
        return []
