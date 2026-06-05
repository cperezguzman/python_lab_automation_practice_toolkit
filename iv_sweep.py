# First draft of auto toolkit

import numpy as np
import csv
from pathlib import Path
import time
import random

class MockSourcemeter:
    NOISE_FRAC = {"LOW" : 0.001, "MEDIUM" : 0.009, "HIGH" : 0.02}


    def __init__(self, simulated_resistance=50, noise_level="MEDIUM", shots=25):
        self.connection_status = "OFF"
        self.output_status = "DISABLED"
        self.voltage_range = 10 # -10 V to 10 V
        self.current_limit = 1 # -1 A to 1 A
        self.simulated_resistance = simulated_resistance # 50 Ohms
        self.noise_level = noise_level
        self.voltage_noise_floor = 0.0005 # 0.5 mV
        self.current_noise_floor = 0.0000005 # 0.5 uA
        self.shots = shots
        self.voltage_setpoint = 0

    def connect(self):
        self.connection_status = "ON"

    def disconnect(self):
        self.connection_status = "OFF"

    def enable_output(self):
        self.output_status = "ENABLED"

    def disable_output(self):
        self.output_status = "DISABLED"

    def set_voltage_range(self, volts: float):
        self.voltage_range = volts

    def get_voltage_range(self):
        return self.voltage_range

    def set_voltage(self, volts: float):
        self.voltage_setpoint = volts

    def get_voltage(self):
        return self.voltage_setpoint

    def set_current_limit(self, c_limit: float):
        self.current_limit = c_limit

    def get_current_limit(self):
        return self.current_limit

    def set_resistance(self, ohms: float):
        self.simulated_resistance = ohms

    def get_resistance(self):
        return self.simulated_resistance

    def set_noise_level(self, level: str):
        self.noise_level = level.upper()

    def set_shots(self, shots: int):
        self.shots = shots

    def get_shots(self):
        return self.shots

    def get_noise(self, measurement_type, ideal_value):
        if measurement_type == "VOLTAGE":
            floor = self.voltage_noise_floor
        elif measurement_type == "CURRENT":
            floor = self.current_noise_floor
        else:
            raise ValueError(f"Unknown Measurement Type: {measurement_type}")


        frac = self.NOISE_FRAC[self.noise_level]

        noise_std = floor + (abs(ideal_value) * frac)

        return random.gauss(0, noise_std)

    def measure_voltage(self):
        if self.connection_status == "OFF":
            raise RuntimeError("Cannot measure voltage: instrument is not connected.")
        if self.output_status == "DISABLED":
            raise RuntimeError("Cannot measure voltage: instrument output is disabled.")
        
        ideal_voltage = self.get_voltage()
        noise = self.get_noise("VOLTAGE", ideal_voltage)

        return ideal_voltage + noise

    def measure_current(self):
        if self.connection_status == "OFF":
            raise RuntimeError("Cannot measure current: instrument is not connected.")
        if self.output_status == "DISABLED":
            raise RuntimeError("Cannot measure current: instrument output is disabled.")

        ideal_current = (self.get_voltage() / self.get_resistance())

        if abs(ideal_current) > self.get_current_limit():
            raise RuntimeError("Current limit exceeded.")

        noise = self.get_noise("CURRENT", ideal_current)
        
        return ideal_current + noise


def save_to_csv(data: list[dict], filepath: str | Path) -> None:
    if not data:
        return # nothing to write

    fieldnames = list(data[0].keys())
    

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    sourcemeter1 = MockSourcemeter()

    sourcemeter1.connect()
    print("Connecting to sourcemeter.")

    sourcemeter1.enable_output()
    print("Enabling sourcemeter output.")

    try:
        data = []

        v_range = sourcemeter1.get_voltage_range()
        shots = sourcemeter1.get_shots()
        voltages = np.linspace(-v_range, v_range, shots)

        print("Commencing measurement process.")

        for ideal_voltage in voltages:
            sourcemeter1.set_voltage(ideal_voltage)

            time.sleep(0.1)

            voltage = sourcemeter1.measure_voltage()
            current = sourcemeter1.measure_current()

            data.append({
                "voltage_setpoint": ideal_voltage,
                "measured_voltage": voltage,
                "measured_current": current,
            })

        save_to_csv(data, "iv_sweep_results.csv")
        print("Saved to CSV file.")
    
    except RuntimeError as e:
        print(f"Sweep aborted: {e}")
        raise

    finally:
        sourcemeter1.disable_output()
        sourcemeter1.disconnect()

        print("Successfully disabled and disconnected the sourcemeter.")


if __name__ == "__main__":
    main()
