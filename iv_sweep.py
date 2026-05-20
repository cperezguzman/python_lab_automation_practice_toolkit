# First draft of auto toolkit

class MockSourcemeter:
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
        self.output_status = "ON"

    def disable_output(self):
        self.output_status = "OFF"

    def set_voltage_range(self, volts: float):
        self.voltage_range = volts

    def get_voltage_range(self):
        return self.voltage_range

    def set_voltage(self, volts: float):
        self.voltages_setpoint = volts

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
        self.noise_level = level

    def set_shots(self, shots: int):
        self.shots = shots

    def get_shots(self):
        return self.shots

    def get_noise(self, measurement_type, ideal_value):
        if measurement_type == "VOLTAGE":
            if noise_level == "LOW":
                noise_std = self.voltage_noise_floor + (abs(ideal_value) * 0.001)
            if noise_level == "MEDIUM":
                noise_std = self.voltage_noise_floor + (abs(ideal_value) * 0.009)
            if noise_level == "HIGH":
                noise_std = self.voltage_noise_floor + (abs(ideal_value) * 0.02)
        
        if measurement_type == "CURRENT":
            if noise_level == "LOW":
                noise_std = self.current_noise_floor + (abs(ideal_value) * 0.001)
            if noise_level == "MEDIUM":
                noise_std = self.current_noise_floor + (abs(ideal_value) * 0.009)
            if noise_level == "HIGH":
                noise_std = self.current_noise_floor + (abs(ideal_value) * 0.02)

        return random.gauss(0, noise_std)

    def measure_voltage(self):
        if self.connection_status == "OFF":
            raise RuntimeError("Cannot measure voltage: instrument is not connected.")
        if self.output_status == "OFF":
            raise RuntimeError("Cannot measure voltage: instrument output is OFF.")
        
        ideal_voltage = self.get_voltage()
        noise = self.get_noise("VOLTAGE", ideal_voltage)

        return ideal_voltage + noise

    def measure_current(self):
        if self.connection_status == "OFF":
            raise RuntimeError("Cannot measure voltage: instrument is not connected.")
        if self.output_status == "OFF":
            raise RuntimeError("Cannot measure voltage: instrument output is OFF.")

        ideal_current = (self.get_voltage() / self.get_resistance())

        if abs(ideal_current) > self.get_current_limit():
            raise RuntimeError("Current limit exceeded.")

        noise = self.get_noise("CURRENT", ideal_current)
        
        return ideal_current + noise



def main():
    sourcemeter1 = MockSourcemeter()

    sourcemeter1.connect()
    sourcemeter1.enable_output()

    data = []

    v_range = sourcemeter1.get_voltage_range()
    shots = sourcemeter1.get_shots()
    voltages = np.linspace(-v_range, v_range, shots)
    currents = [None] * shots

    for ideal_voltage in voltages:
        sourcemeter1.set_voltage(ideal_voltage)

        time.sleep(0.1)

        voltage = sourcemeter1.measure_voltage()
        current = sourcemeter1.measure_current()

        currents.append(current)

        data.append({
            "voltage_setpoint": ideal_voltage
            "measured_voltage": sourcemeter1.measure_voltage()
            "measured_current": sourcemeter1.measure_current()
        })

    sourcemeter1.disable_output()
    sourcemeter1.disconnect()






if __name__ == "__main__":
    main()
