import time

import numpy as np

from analysis.iv_analysis import calculate_resistance
from instruments.mock_sourcemeter import MockSourcemeter
from plotting.plot_iv import plot_iv
from utils.file_manager import make_iv_sweep_paths, save_to_csv


def run_iv_sweep(
    config: dict,
    sourcemeter: MockSourcemeter | None = None,
) -> dict:
    """Run a full I-V sweep: measure, save CSV, plot, and estimate resistance."""
    sourcemeter = sourcemeter or MockSourcemeter(
        simulated_resistance=config["resistance_ohms"],
        noise_level=config.get("noise_level", "MEDIUM"),
        shots=config["num_points"],
    )
    sourcemeter.set_voltage_range(
        max(abs(config["start_voltage"]), abs(config["stop_voltage"]))
    )

    settling_time = config.get("settling_time_seconds", 0.1)

    sourcemeter.connect()
    print("Connected to sourcemeter.")

    sourcemeter.enable_output()
    print("Enabled sourcemeter output.")

    try:
        data = []
        voltages = np.linspace(
            config["start_voltage"],
            config["stop_voltage"],
            config["num_points"],
        )

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
