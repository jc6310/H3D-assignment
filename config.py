"""Config from CLI args and env vars."""
import argparse
import os


def load_config():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--input", 
        default=os.getenv("INPUT_FOLDER", "./input")
    )
    p.add_argument(
        "--output",
        default=os.getenv("OUTPUT_FOLDER", "./output")
    )
    p.add_argument(
        "--workers",
        type=int,
        default=int(os.getenv("WORKER_COUNT", "5"))
    )
    p.add_argument(
        "--mode",
        choices=["sqlite", "folder"],
        default=os.getenv("OUTPUT_MODE", "folder"),
    )
    p.add_argument(
        "--db-path", dest="db_path", default=os.getenv("DB_PATH", "results.db")
    )
    args = p.parse_args()

    return vars(args)
