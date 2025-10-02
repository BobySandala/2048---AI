import json
import os

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")

def save_value(label, value):
    data = {}
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    data[label] = value
    with open(data_path, "w") as f:
        json.dump(data, f, indent=4)

def load_value(label, default=None):
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            try:
                data = json.load(f)
                return data.get(label, default)
            except json.JSONDecodeError:
                return default
    return default
