from pathlib import Path

import matplotlib.pyplot as plt


def plot_iv(data: list[dict], filepath: str | Path) -> None:
    voltages = [row["measured_voltage"] for row in data]
    currents = [row["measured_current"] for row in data]

    plt.figure(figsize=(8, 5))
    plt.plot(voltages, currents, marker="o", markersize=3, linewidth=1)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.title("I-V Sweep")
    plt.grid(True)

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
