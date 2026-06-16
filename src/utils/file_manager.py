import csv
from datetime import datetime
from pathlib import Path


def make_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def make_iv_sweep_paths(timestamp: str | None = None) -> tuple[Path, Path]:
    if timestamp is None:
        timestamp = make_timestamp()
    csv_path = Path(f"data/raw/iv_sweep_{timestamp}.csv")
    plot_path = Path(f"plots/iv/iv_sweep_{timestamp}.png")
    return csv_path, plot_path


def make_resonance_sweep_paths(timestamp: str | None = None) -> tuple[Path, Path]:
    if timestamp is None:
        timestamp = make_timestamp()
    csv_path = Path(f"data/raw/resonance_sweep_{timestamp}.csv")
    plot_path = Path(f"plots/resonance/resonance_sweep_{timestamp}.png")
    return csv_path, plot_path


def save_to_csv(data: list[dict], filepath: str | Path) -> None:
    if not data:
        return

    fieldnames = list(data[0].keys())
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
