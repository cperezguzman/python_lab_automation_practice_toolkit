import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_IV_CONFIG = PROJECT_ROOT / "config" / "iv_sweep_config.json"
DEFAULT_RESONANCE_CONFIG = PROJECT_ROOT / "config" / "resonance_sweep_config.json"


def load_config(path: str | Path) -> dict:
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        return json.load(f)
