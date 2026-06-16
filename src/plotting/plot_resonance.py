from pathlib import Path

import matplotlib.pyplot as plt


def plot_resonance(data: list[dict], filepath: str | Path, fit: dict | None = None) -> None:
    frequencies = [row["frequency_ghz"] for row in data]
    responses = [row["response_amplitude"] for row in data]

    plt.figure(figsize=(8, 5))
    plt.plot(frequencies, responses, marker=".", markersize=2, linewidth=1, label="Measured")

    if fit is not None:
        plt.axvline(
            fit["resonance_frequency_ghz"],
            color="red",
            linestyle="--",
            linewidth=1,
            label=f"f0 = {fit['resonance_frequency_ghz']:.4f} GHz",
        )

    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Response Amplitude")
    plt.title("Resonance Sweep")
    plt.grid(True)
    plt.legend()

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
