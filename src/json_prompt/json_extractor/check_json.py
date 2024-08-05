import json

def is_valid_json(json_string):
    try:
        json.loads(json_string)
    except json.JSONDecodeError:
        return False
    return True