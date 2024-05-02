# config.py
import json

def load_config(file_path='keys.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
