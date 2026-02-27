from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"


def load_data() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_PATH}")
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_data(data: Dict[str, Any]) -> None:
    DATA_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
