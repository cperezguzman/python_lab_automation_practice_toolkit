import json
from pathlib import Path

import pytest

from utils.config_loader import DEFAULT_IV_CONFIG, load_config


def test_load_default_iv_config():
    config = load_config(DEFAULT_IV_CONFIG)
    assert config["start_voltage"] == -10.0
    assert config["stop_voltage"] == 10.0
    assert config["num_points"] == 25
    assert config["resistance_ohms"] == 50


def test_load_config_from_temp_file(tmp_path):
    config_path = tmp_path / "custom.json"
    payload = {
        "start_voltage": -2.0,
        "stop_voltage": 2.0,
        "num_points": 5,
        "resistance_ohms": 200,
        "noise_level": "HIGH",
        "settling_time_seconds": 0.05,
    }
    config_path.write_text(json.dumps(payload), encoding="utf-8")

    loaded = load_config(config_path)
    assert loaded == payload


def test_load_config_missing_file_raises():
    missing = Path("config/does_not_exist.json")
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        load_config(missing)
