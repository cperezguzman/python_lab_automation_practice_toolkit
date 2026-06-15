import numpy as np


def calculate_resistance(data: list[dict]) -> float:
    """Estimate resistance (ohms) from I-V data via linear fit: V = R * I."""
    if not data:
        raise ValueError("Cannot estimate resistance: no measurement data.")

    voltages = np.array([row["measured_voltage"] for row in data])
    currents = np.array([row["measured_current"] for row in data])

    resistance, _ = np.polyfit(currents, voltages, 1)
    return resistance
