import json
import os
import random

def load_questions(level, section, n=10):
    filename = f"questions/{level.lower()}.json"
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        all_qs = json.load(f)
    filtered = [q for q in all_qs if q["section"] == section]
    return random.sample(filtered, min(n, len(filtered)))
