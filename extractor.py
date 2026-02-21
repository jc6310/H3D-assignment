import json
import logging
from datetime import datetime

REQUIRED_FIELDS = ["id", "timestamp", "payload"]


def extract_json_files(folder_path):
    try:
        with open(folder_path, "r") as f:
            data = json.load(f)

        valid, error = _validate_json(data)
        if not valid:
            logging.error(f"Validation failed: {folder_path} - {error}")
            return None

        logging.info(f"Processed successfully: {folder_path}")
        return data

    except Exception as e:
        logging.error(f"File failed (skipped): {folder_path} - {e}")
        return None


def _validate_json(json_data):
    if not isinstance(json_data, dict):
        return False, "root must be an object"
    for field in REQUIRED_FIELDS:
        if field not in json_data:
            return False, f"Missing field: {field}"
    if not isinstance(json_data["id"], str):
        return False, "id must be string"
    try:
        ts = json_data["timestamp"]
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return False, "timestamp must be ISO-8601 format"
    if not isinstance(json_data["payload"], dict):
        return False, "payload must be object"

    return True, None
