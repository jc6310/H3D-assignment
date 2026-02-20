import json
import os
import logging


def extract_json_files(folder_path):
    try:
        with open(folder_path, "r") as f:
            data = json.load(f)

        valid, error = _validate_json(data)
        if not valid:
            logging.error(f"{folder_path} invalid: {error}")
            return None

        logging.info(f"{folder_path} processed successfully")
        return data

    except Exception as e:
        logging.error(f"{folder_path} failed: {str(e)}")
        return None


def _validate_json(json_data):
    if not isinstance(json_data, dict):
        return False, "root must be an object"
    if "id" not in json_data or not isinstance(json_data["id"], str):
        return False, "missing or invalid 'id' (must be string)"
    if "timestamp" not in json_data or not isinstance(json_data["timestamp"], str):
        return False, "missing or invalid 'timestamp' (must be string)"
    if "payload" not in json_data or not isinstance(json_data["payload"], dict):
        return False, "missing or invalid 'payload' (must be object)"
        
    return True, None
