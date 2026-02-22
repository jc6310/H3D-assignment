import json
import os
import logging
from db import init_db, insert_record


def send_records_to_db(json_data, db_path):
    """Write record(s) to db."""
    if not init_db(db_path):
        logging.error("Database init failed; skipping insert.")
        return False
    if not insert_record(db_path, json_data):
        return False
    logging.info("Record %s inserted successfully.", json_data.get("id", "?"))
    return True


def add_records_to_folder(json_data, output_folder, filename=None):
    """Write record(s) to folder. json_data can be a single dict or list of dicts."""
    return _write_to_folder(json_data, output_folder, filename)


def _write_to_folder(json_data, output_folder, filename=None):
    """Write record(s) as a JSON array. Single dict is normalized to [dict]."""
    os.makedirs(output_folder, exist_ok=True)
    records = json_data if isinstance(json_data, list) else [json_data]
    name = filename or "output.json"
    path = os.path.join(output_folder, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return True
