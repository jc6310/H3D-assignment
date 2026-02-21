# H3D-assignment

## Candidate Instructions

### Requirements
- **Language:** Python / Node / Java (your choice)
- **CLI or small service** (no UI required)
- **Input:** a folder path provided via argument or environment variable
- **Output:** either
  - Write results into SQLite/Postgres, or
  - Write processed JSON into an output folder

### Validation Rules
Each input JSON file must contain at minimum:

```json
{
  "id": string,
  "timestamp": string (ISO-8601),
  "payload": object
}
```

Invalid files should:
- not crash the service
- be logged clearly as failures

### Concurrency
- Process files using multiple workers (threads, goroutines, async tasks, etc.)
- Limit concurrency to avoid CPU thrashing (bounded pool)

### Additional Expectations
- Logging with timestamps and result summaries
- Configurable paths and worker count via env or CLI flag
- Graceful shutdown (finish processing in-flight files)
- Unit tests for validation / transformation logic (not required for I/O)

## Requirements Checklist

| Requirement | Status | Implementation |
|-------------|--------|-----------------|
| **Language: Python** | Done | Python 3 |
| **CLI (no UI)** | Done | `python3 app.py` with args |
| **Input via argument or env** | Done | `--input`, `INPUT_FOLDER` |
| **Output: SQLite** | Done | `--mode sqlite`, `db.py` |
| **Output: JSON folder** | Done | `--mode folder`, `loader.add_records_to_folder` |
| **Schema: id, timestamp, payload** | Done | `extractor._validate_json` |
| **Timestamp ISO-8601** | Done | `datetime.fromisoformat` (+ Z→+00:00) |
| **Invalid files don't crash** | Done | try/except, return None |
| **Invalid files logged** | Done | `logging.error("Validation failed: ...")` |
| **Multiple workers** | Done | `ThreadPoolExecutor` |
| **Bounded pool** | Done | `max_workers=config["workers"]` |
| **Logging with timestamps** | Done | `%(asctime)s [%(levelname)s]` |
| **Result summaries** | Done | "Success: N, Failed: M" |
| **Configurable via env/CLI** | Done | `config.py` |
| **Graceful shutdown** | Done | `handle_shutdown`, SIGINT/SIGTERM |
| **Unit tests** | Done | `tests/test_json_processor.py` |

## Run

```bash
pip3 install -r requirements.txt   # if needed
python3 app.py
```

### CLI arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input file or folder path | `./input` |
| `--output` | Output folder (when `--mode folder`) | `./output` |
| `--workers` | Number of worker threads | `4` |
| `--mode` | Output mode: `sqlite` or `folder` | `folder` |
| `--db-path` | SQLite database path (when `--mode sqlite`) | `results.db` |

### Environment variables

| Variable | Maps to |
|----------|---------|
| `INPUT_FOLDER` | `--input` |
| `OUTPUT_FOLDER` | `--output` |
| `WORKER_COUNT` | `--workers` |
| `OUTPUT_MODE` | `--mode` |
| `DB_PATH` | `--db-path` |

### Example commands

```bash
# Process folder, write JSON to ./output
python3 app.py --input ./input --mode folder

# Process folder, write to SQLite
python3 app.py --input ./input --mode sqlite --db-path results.db

# Single file
python3 app.py --input test.json

# Use 8 workers
python3 app.py --input ./input --workers 8

# With env vars
INPUT_FOLDER=./input OUTPUT_MODE=sqlite python3 app.py
```

## Tests

```bash
python3 tests/test_json_processor.py -v
# or with pytest
python3 -m pytest tests/test_json_processor.py -v
```
