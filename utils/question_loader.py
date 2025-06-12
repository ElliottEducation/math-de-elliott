import json
import os

def load_questions(year, level, module):
    path = os.path.join("questions", year, level, module + ".json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
