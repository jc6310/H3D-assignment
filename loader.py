import json
import os
import logging
from db import init_db, insert_record

def send_records_to_db(json_data, db_path="test.db"):
    init_db(db_path)

    insert_record("test.db", json_data)

def add_records_to_folder(json_data, output_folder):
    return _write_to_folder(json_data, output_folder)

def _write_to_folder(json_data, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "output.json"), "w") as f:
        json.dump(json_data, f)

    return True