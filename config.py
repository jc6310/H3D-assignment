"""Config from CLI args and env vars."""
import argparse
import os


def _parse_workers():
    raw = os.getenv("WORKER_COUNT", "4")
    try:
        n = int(raw)
        return max(1, n) if n > 0 else 1
    except (ValueError, TypeError):
        return 4


def load_config():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--input",
        default=os.getenv("INPUT_FOLDER", "./input"),
    )
    p.add_argument(
        "--output",
        default=os.getenv("OUTPUT_FOLDER", "./output"),
    )
    p.add_argument(
        "--workers",
        type=int,
        default=_parse_workers(),
    )
    p.add_argument(
        "--mode",
        choices=["sqlite", "folder"],
        default=os.getenv("OUTPUT_MODE", "folder"),
    )
    p.add_argument(
        "--db-path",
        dest="db_path",
        default=os.getenv("DB_PATH", "results.db"),
    )
    args = p.parse_args()
    args.workers = max(1, args.workers)

    return vars(args)
