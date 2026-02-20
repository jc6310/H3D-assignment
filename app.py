#!/usr/bin/env python3
import logging
from extractor import extract_json_files
from loader import send_records_to_db, add_records_to_folder

def main():
    mode = "sqlite"
    logging.info(f"Processing starting.....")
    json_data = extract_json_files("test.json")

    if json_data is None:
        logging.error("No data to write (validation failed or error).")
        return
    if mode == "sqlite":
        send_records_to_db(json_data)
    elif mode == "folder":
        add_records_to_folder(json_data, "output")

    logging.info(f"Processing complete.")

if __name__ == "__main__":
    main()