# H3D-assignment
H3D assignment

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
