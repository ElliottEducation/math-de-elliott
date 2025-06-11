import os
import json

def load_questions_from_directory(directory: str):
    """
    Recursively loads all questions from JSON files under the given directory.
    Returns a list of questions.
    """
    all_questions = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        questions = json.load(f)
                        if isinstance(questions, list):
                            all_questions.extend(questions)
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    return all_questions
