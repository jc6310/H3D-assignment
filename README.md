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
