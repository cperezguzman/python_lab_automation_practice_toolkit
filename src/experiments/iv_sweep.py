import time

import numpy as np

from analysis.iv_analysis import calculate_resistance
from instruments.mock_sourcemeter import MockSourcemeter
from plotting.plot_iv import plot_iv
from utils.file_manager import make_iv_sweep_paths, save_to_csv


def run_iv_sweep(
    sourcemeter: MockSourcemeter | None = None,
    settling_time: float = 0.1,
) -> dict:
    """Run a full I-V sweep: measure, save CSV, plot, and estimate resistance."""
    sourcemeter = sourcemeter or MockSourcemeter()

    sourcemeter.connect()
    print("Connected to sourcemeter.")

    sourcemeter.enable_output()
    print("Enabled sourcemeter output.")

    try:
        data = []
        v_range = sourcemeter.get_voltage_range()
        shots = sourcemeter.get_shots()
        voltages = np.linspace(-v_range, v_range, shots)

        print("Commencing measurement process.")

        for ideal_voltage in voltages:
            sourcemeter.set_voltage(ideal_voltage)
            time.sleep(settling_time)

            voltage = sourcemeter.measure_voltage()
            current = sourcemeter.measure_current()

            data.append({
                "voltage_setpoint": ideal_voltage,
                "measured_voltage": voltage,
                "measured_current": current,
            })

        csv_path, plot_path = make_iv_sweep_paths()

        save_to_csv(data, csv_path)
        print(f"Data saved to {csv_path}.")

        plot_iv(data, plot_path)
        print(f"Plot saved to {plot_path}.")

        resistance = calculate_resistance(data)
        print(f"Estimated resistance: {resistance:.2f} ohms")

        return {
            "data": data,
            "csv_path": csv_path,
            "plot_path": plot_path,
            "resistance_ohms": resistance,
        }

    except RuntimeError as e:
        print(f"Sweep aborted: {e}")
        raise

    finally:
        sourcemeter.disable_output()
        sourcemeter.disconnect()
        print("Successfully disabled and disconnected the sourcemeter.")
