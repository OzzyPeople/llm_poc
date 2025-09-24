import json
from pathlib import Path

def load_evidence(filename: str = "evidence.json") -> dict:
    """
    Load compliance evidence base from the data/ folder.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    print (base_dir)
    data_path = base_dir / "data" / filename

    if not data_path.exists():
        raise FileNotFoundError(f"Evidence base not found: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)
