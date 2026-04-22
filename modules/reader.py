# modules/reader.py
import csv
import io

# These exactly match the headers in your uploaded firewall-rules.csv
REQUIRED_COLUMNS = {"id", "source", "destination", "port", "action"}

def process_csv(file):
    """
    Reads the uploaded firewall-rules.csv and converts it into a clean list of dictionaries.
    """
    # 1. Read and decode the raw file
    raw = file.read()
    if not raw:
        raise ValueError("Uploaded file is empty.")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")  # Fallback for some Windows Excel exports

    # 2. Parse the CSV text
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV has no headers. Please ensure the first row contains column names.")

    # 3. Clean the headers (removes accidental spaces and makes them lowercase)
    reader.fieldnames = [str(col).strip().lower() for col in reader.fieldnames]

    # 4. Check if the uploaded file has the exact columns we need
    missing = REQUIRED_COLUMNS - set(reader.fieldnames)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}. Found: {reader.fieldnames}")

    # 5. Build the clean list of rules
    rules = []
    for row in reader:
        # Skip completely empty rows (common if user left blank lines at the bottom of the CSV)
        if not any(row.values()):
            continue

        rules.append({
            "id":          _to_int(row.get("id")),
            # Keep IPs and subnets intact, but standardize spacing
            "source":      str(row.get("source", "")).strip(),
            "destination": str(row.get("destination", "")).strip(),
            "port":        _to_int(row.get("port")),
            # Force ALLOW/DENY to be uppercase so the analyzer never gets confused
            "action":      str(row.get("action", "")).strip().upper(),
        })

    if not rules:
        raise ValueError("CSV has headers but no actual rule data.")

    return rules


def _to_int(value):
    """
    Safely converts a port or ID to an integer. 
    If the cell is blank or has weird text, it returns None instead of crashing.
    """
    if value is None:
        return None
        
    try:
        # Strip decimals just in case Excel exported '80.0' instead of '80'
        clean_value = str(value).strip().split('.')[0]
        return int(clean_value)
    except (ValueError, TypeError):
        return None

# --- Quick Test Block (Delete before final integration) ---
if __name__ == "__main__":
    # You can test this locally by pointing it to your actual file
    class MockFile:
        def read(self):
            with open("firewall-rules.csv", "rb") as f:
                return f.read()
                
    try:
        parsed_rules = process_csv(MockFile())
        import json
        print(json.dumps(parsed_rules[:3], indent=2)) # Print first 3 rules to verify
        print(f"\nSuccessfully loaded {len(parsed_rules)} rules!")
    except Exception as e:
        print(f"Error: {e}")
