import csv
from unittest.mock import patch

import pytest

from experiments.iv_sweep import run_iv_sweep


def test_run_iv_sweep_returns_expected_row_count(iv_config, tmp_path):
    csv_path = tmp_path / "iv.csv"
    plot_path = tmp_path / "iv.png"

    with patch("experiments.iv_sweep.make_iv_sweep_paths", return_value=(csv_path, plot_path)):
        with patch("experiments.iv_sweep.plot_iv"):
            with patch("experiments.iv_sweep.time.sleep"):
                result = run_iv_sweep(iv_config)

    assert len(result["data"]) == iv_config["num_points"]

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == iv_config["num_points"]


def test_run_iv_sweep_resistance_near_configured_value(iv_config, tmp_path):
    csv_path = tmp_path / "iv.csv"
    plot_path = tmp_path / "iv.png"

    with patch("experiments.iv_sweep.make_iv_sweep_paths", return_value=(csv_path, plot_path)):
        with patch("experiments.iv_sweep.plot_iv"):
            with patch("experiments.iv_sweep.time.sleep"):
                with patch(
                    "instruments.mock_sourcemeter.MockSourcemeter.get_noise",
                    return_value=0.0,
                ):
                    result = run_iv_sweep(iv_config)

    assert result["resistance_ohms"] == pytest.approx(100.0, rel=0.05)
