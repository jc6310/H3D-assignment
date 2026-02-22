import json
import logging
from datetime import datetime

REQUIRED_FIELDS = ["id", "timestamp", "payload"]


def extract_json_file(file_path):
    """Read and validate a single JSON file. Returns validated data dict or None."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        valid, error = _validate_json(data)
        if not valid:
            logging.error("Validation failed: %s - %s", file_path, error)
            return None

        logging.info("Processed successfully: %s", file_path)
        return data

    except Exception as e:
        logging.error("File failed (skipped): %s - %s", file_path, e)
        return None


def _validate_json(json_data):
    """Validate json data. Returns isValid, message"""
    if not isinstance(json_data, dict):
        return False, "root must be an object"
    for field in REQUIRED_FIELDS:
        if field not in json_data:
            return False, f"Missing field: {field}"
    if not isinstance(json_data["id"], str):
        return False, "id must be string"
    ts = json_data["timestamp"]
    if not isinstance(ts, str):
        return False, "timestamp must be ISO-8601 format (string)"
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return False, "timestamp must be ISO-8601 format"
    if not isinstance(json_data["payload"], dict):
        return False, "payload must be object"

    return True, None


def validate_json(json_data):
    """Public validation for testing. Returns (valid, error) tuple."""
    return _validate_json(json_data)
