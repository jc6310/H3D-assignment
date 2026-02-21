#!/usr/bin/env python3
import logging
import signal

from config import load_config
from extractor import extract_json_files
from loader import send_records_to_db, add_records_to_folder

shutdown_flag = False


def handle_shutdown(signum, frame):
    global shutdown_flag
    shutdown_flag = True
    logging.info("Graceful shutdown initiated...")


def main():
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    config = load_config()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Processing starting.....")

    if shutdown_flag:
        return
        
    json_data = extract_json_files(config["input"])
    mode = config["mode"]

    if shutdown_flag:
        return
    if json_data is None:
        logging.error("Processing aborted: no valid data (invalid file or read error).")
        return

    if mode == "sqlite":
        send_records_to_db(json_data, config["db_path"])
    elif mode == "folder":
        add_records_to_folder(json_data, config["output"])

    logging.info("Processing complete.")


if __name__ == "__main__":
    main()