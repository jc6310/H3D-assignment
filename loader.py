import json
import os
import logging
from db import init_db, insert_record

def send_records_to_db(json_data, db_path="test.db"):
    if not init_db(db_path):
        logging.error("Database init failed; skipping insert.")
        return False
    if not insert_record(db_path, json_data):
        return False
    logging.info(f"Record {json_data.get('id', '?')} inserted successfully.")
    return True

def add_records_to_folder(json_data, output_folder, filename=None):
    """Write record(s) to folder. json_data can be a single dict or list of dicts."""
    return _write_to_folder(json_data, output_folder, filename)

def _write_to_folder(json_data, output_folder, filename=None):
    os.makedirs(output_folder, exist_ok=True)
    name = filename or "output.json"
    with open(os.path.join(output_folder, name), "w") as f:
        json.dump(json_data, f)
    return True