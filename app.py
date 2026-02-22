#!/usr/bin/env python3
import logging
import os
import signal
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import load_config
from extractor import extract_json_file
from loader import send_records_to_db, add_records_to_folder

shutdown_flag = False


def handle_shutdown(signum, frame):
    global shutdown_flag
    shutdown_flag = True
    logging.info("Graceful shutdown initiated...")


def process_file(file_path, config):
    """Process one JSON file. Returns (success, json_data) or (False, None)."""
    thread_name = threading.current_thread().name
    logging.info(f"[{thread_name}] Processing: {os.path.basename(file_path)}")
    if shutdown_flag:
        return False, None
    json_data = extract_json_file(file_path)
    if shutdown_flag or json_data is None:
        return False, None
    mode = config["mode"]
    if mode == "sqlite":
        ok = send_records_to_db(json_data, config["db_path"])
        return ok, json_data if ok else None
    if mode == "folder":
        return True, json_data
    return False, None


def process_folder(config):
    """Process all .json files using a bounded thread pool."""
    files = [
        os.path.join(config["input"], f)
        for f in os.listdir(config["input"])
        if f.endswith(".json")
    ]
    records = []
    success = failure = 0
    max_workers = config["workers"]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, f, config) for f in files]
        for future in as_completed(futures):
            ok, data = future.result()
            if ok:
                success += 1
                if config["mode"] == "folder":
                    records.append(data)
            else:
                failure += 1
    return success, failure, records


def main():
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    config = load_config()
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Starting Processing.....")
    if shutdown_flag:
        return

    input_path = config["input"]
    if os.path.isdir(input_path):
        success, failure, records = process_folder(config)
        output_records = records if config["mode"] == "folder" else []
    else:
        ok, data = process_file(input_path, config)
        success, failure = (1, 0) if ok else (0, 1)
        output_records = ([data] if data else []) if config["mode"] == "folder" else []

    if output_records:
        add_records_to_folder(output_records, config["output"])

    if os.path.isdir(input_path):
        logging.info("Processing complete. Success: %s, Failed: %s", success, failure)
    elif success:
        logging.info("Processing complete.")
    else:
        logging.error(
            "Processing aborted: Invalid data (invalid file / read error)."
        )


if __name__ == "__main__":
    main()