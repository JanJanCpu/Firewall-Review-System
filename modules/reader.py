# modules/reader.py
import csv
import io

REQUIRED_COLUMNS = {"id", "source", "destination", "port", "action"}
ALLOWED_EXTENSIONS = {".csv"}
ALLOWED_MIME_TYPES = {"text/csv", "application/csv", "application/vnd.ms-excel", "text/plain"}

def process_csv(file):
    """
    Reads an uploaded CSV file and returns a list of firewall rule dictionaries.
    Args:
        file: A file-like object (from Flask request.files or FastAPI UploadFile.file)
    Returns:
        List of dicts, e.g. [{'id': 1, 'source': 'Any', 'destination': 'Any', 'port': 80, 'action': 'ALLOW', 'hit_count': 0}]
    Raises:
        ValueError: If the file is not a CSV, is empty, missing required columns, or has no valid rows
    """
    # 1. Validate file type before reading anything
    _validate_file_type(file)

    # 2. Read and decode raw bytes
    raw = file.read()
    if not raw:
        raise ValueError("Uploaded file is empty.")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")  # handles CSVs exported from Excel/Windows

    # 3. Parse CSV
    reader = csv.DictReader(io.StringIO(text))

    # 4. Normalize column names (strip whitespace, lowercase)
    #    Handles cases like "Port " or "ACTION" from different tools
    if reader.fieldnames is None:
        raise ValueError("CSV has no headers.")
    reader.fieldnames = [col.strip().lower() for col in reader.fieldnames]

    # 5. Validate required columns exist
    missing = REQUIRED_COLUMNS - set(reader.fieldnames)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    # 6. Check if hit_count column is present (optional but captured if available)
    has_hit_count = "hit_count" in reader.fieldnames

    # 7. Build the rules list
    rules = []
    for row in reader:
        # Skip completely empty rows (common in Excel exports)
        if not any(row.values()):
            continue

        rule = {
            "id":          _to_int(row.get("id")),
            "source":      row.get("source", "").strip(),
            "destination": row.get("destination", "").strip(),
            "port":        _to_int(row.get("port")),
            "action":      row.get("action", "").strip().upper(),  # normalize to ALLOW/DENY
            "hit_count":   _to_int(row.get("hit_count")) if has_hit_count else 0,
        }
        rules.append(rule)

    if not rules:
        raise ValueError("CSV has no valid data rows.")

    return rules


def _validate_file_type(file):
    """
    Checks the file's extension and MIME type to ensure it is a CSV.
    Raises:
        ValueError: If the file does not appear to be a CSV.
    """
    filename = getattr(file, "filename", "") or getattr(file, "name", "") or ""
    content_type = getattr(file, "content_type", "") or getattr(file, "mimetype", "") or ""

    # Check extension
    if filename:
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Invalid file type '{ext or 'unknown'}'. Only .csv files are accepted."
            )

    # Check MIME type (as a secondary guard when available)
    if content_type and content_type.split(";")[0].strip() not in ALLOWED_MIME_TYPES:
        raise ValueError(
            f"Invalid content type '{content_type}'. Expected a CSV file."
        )

    # If neither hint is available, we let it through and let the CSV parser catch it
    if not filename and not content_type:
        return


def _to_int(value):
    """Safely converts a value to int, returns None if not possible."""
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return None