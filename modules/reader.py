# modules/reader.py
import csv
import io

REQUIRED_COLUMNS = {"id", "source", "destination", "port", "action"}

def process_csv(file):
    """
    Reads an uploaded CSV file and returns a list of firewall rule dictionaries.

    Args:
        file: A file-like object (from Flask request.files or FastAPI UploadFile.file)

    Returns:
        List of dicts, e.g. [{'id': 1, 'source': 'Any', 'destination': 'Any', 'port': 80, 'action': 'ALLOW'}]

    Raises:
        ValueError: If the file is empty, missing required columns, or has no valid rows
    """

    # 1. Read and decode raw bytes
    raw = file.read()
    if not raw:
        raise ValueError("Uploaded file is empty.")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")  # handles CSVs exported from Excel/Windows

    # 2. Parse CSV
    reader = csv.DictReader(io.StringIO(text))

    # 3. Normalize column names (strip whitespace, lowercase)
    #    Handles cases like "Port " or "ACTION" from different tools
    if reader.fieldnames is None:
        raise ValueError("CSV has no headers.")

    reader.fieldnames = [col.strip().lower() for col in reader.fieldnames]

    # 4. Validate required columns exist
    missing = REQUIRED_COLUMNS - set(reader.fieldnames)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    # 5. Build the rules list
    rules = []
    for row in reader:
        # Skip completely empty rows (common in Excel exports)
        if not any(row.values()):
            continue

        rules.append({
            "id":          _to_int(row.get("id")),
            "source":      row.get("source", "").strip(),
            "destination": row.get("destination", "").strip(),
            "port":        _to_int(row.get("port")),
            "action":      row.get("action", "").strip().upper(),  # normalize to ALLOW/DENY
        })

    if not rules:
        raise ValueError("CSV has no valid data rows.")

    return rules


def _to_int(value):
    """Safely converts a value to int, returns None if not possible."""
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return None
