import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)