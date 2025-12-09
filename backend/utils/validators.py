import json

def ensure_json_serializable(obj):
    try:
        json.dumps(obj)
    except Exception as e:
        raise ValueError("Returned object is not JSON serializable: " + str(e))
