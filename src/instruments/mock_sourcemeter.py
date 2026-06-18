import random

from instruments.base_instrument import BaseInstrument


class MockSourcemeter(BaseInstrument):
    NOISE_FRAC = {"LOW": 0.001, "MEDIUM": 0.009, "HIGH": 0.02}

    def __init__(self, simulated_resistance=50, noise_level="MEDIUM", shots=25):
        super().__init__()
        self.output_status = "DISABLED"
        self.voltage_range = 10  # -10 V to 10 V
        self.current_limit = 1  # -1 A to 1 A
        self.simulated_resistance = simulated_resistance
        self.noise_level = noise_level.upper()
        self.voltage_noise_floor = 0.0005  # 0.5 mV
        self.current_noise_floor = 0.0000005  # 0.5 uA
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

    def reset(self):
        self.disable_output()
        self.voltage_setpoint = 0

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

    def set_simulated_resistance(self, ohms: float):
        self.simulated_resistance = ohms

    def get_simulated_resistance(self):
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

        ideal_current = self.get_voltage() / self.get_simulated_resistance()

        if abs(ideal_current) > self.get_current_limit():
            raise RuntimeError("Current limit exceeded.")

        noise = self.get_noise("CURRENT", ideal_current)
        return ideal_current + noise

    @classmethod
    def from_config(cls, config: dict) -> "MockSourcemeter":
        sourcemeter = cls(
            simulated_resistance=config["resistance_ohms"],
            noise_level=config.get("noise_level", "MEDIUM"),
            shots=config["num_points"],
        )
        sourcemeter.set_voltage_range(
            max(abs(config["start_voltage"]), abs(config["stop_voltage"]))
        )
        return sourcemeter
