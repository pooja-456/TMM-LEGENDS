import os
import json
from app.config import DATA_FOLDER


def get_all_files():
    if not os.path.exists(DATA_FOLDER):
        return []

    return sorted([
        f for f in os.listdir(DATA_FOLDER)
        if f.startswith("tmm_legends_") and f.endswith(".json")
    ])


def save_json(year, records):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    filename = f"tmm_legends_{year}.json"
    filepath = os.path.join(DATA_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    return filepath


def load_json(year=None):
    files = get_all_files()

    if not files:
        return {"file": None, "total": 0, "data": []}

    if year:
        filename = f"tmm_legends_{year}.json"
        if filename not in files:
            return {"file": None, "total": 0, "data": []}
    else:
        filename = files[-1]

    filepath = os.path.join(DATA_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "file": filename,
        "total": len(data),
        "data": data
    }
