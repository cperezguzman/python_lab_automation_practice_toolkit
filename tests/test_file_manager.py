import csv
from pathlib import Path

from utils.file_manager import make_iv_sweep_paths, make_timestamp, save_to_csv


def test_make_timestamp_format():
    ts = make_timestamp()
    assert len(ts) == 17
    assert ts[4] == "-"
    assert ts[7] == "-"
    assert ts[10] == "_"


def test_make_iv_sweep_paths_share_timestamp():
    csv_path, plot_path = make_iv_sweep_paths("2026-06-17_120000")
    assert csv_path == Path("data/raw/iv_sweep_2026-06-17_120000.csv")
    assert plot_path == Path("plots/iv/iv_sweep_2026-06-17_120000.png")
    assert csv_path.stem.split("_")[-1] == plot_path.stem.split("_")[-1]


def test_save_to_csv_creates_file_and_rows(tmp_path):
    data = [
        {"voltage_setpoint": -1.0, "measured_voltage": -1.0, "measured_current": -0.01},
        {"voltage_setpoint": 0.0, "measured_voltage": 0.0, "measured_current": 0.0},
        {"voltage_setpoint": 1.0, "measured_voltage": 1.0, "measured_current": 0.01},
    ]
    outfile = tmp_path / "nested" / "sweep.csv"
    save_to_csv(data, outfile)

    assert outfile.is_file()
    assert outfile.parent.is_dir()

    with open(outfile, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 3
    assert set(rows[0].keys()) == {
        "voltage_setpoint",
        "measured_voltage",
        "measured_current",
    }


def test_save_to_csv_empty_data_does_nothing(tmp_path):
    outfile = tmp_path / "empty.csv"
    save_to_csv([], outfile)
    assert not outfile.exists()
