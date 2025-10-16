from __future__ import annotations
from pathlib import Path
from copilot.incidents import Incident

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "mock"

def list_incident_files():
    return DATA_DIR.glob("*.json")

def load_incident(slug: str) -> Incident:
    path = DATA_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"No mock incident found for slug: {slug}")
    return Incident.model_validate_json(path.read_text())

def load_all() -> list[Incident]:
    return [Incident.model_validate_json(p.read_text()) for p in list_incident_files()]
