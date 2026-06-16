import random

import numpy as np

from instruments.base_instrument import BaseInstrument


class MockNetworkAnalyzer(BaseInstrument):
    """Simulates a microwave network analyzer measuring resonator response."""

    def __init__(
        self,
        start_frequency_ghz: float = 4.8,
        stop_frequency_ghz: float = 5.2,
        num_points: int = 401,
        resonance_frequency_ghz: float = 5.0,
        linewidth_ghz: float = 0.025,
        noise_std: float = 0.01,
        dip_depth: float = 0.7,
        baseline: float = 1.0,
    ):
        super().__init__()
        self.start_frequency_ghz = start_frequency_ghz
        self.stop_frequency_ghz = stop_frequency_ghz
        self.num_points = num_points
        self.resonance_frequency_ghz = resonance_frequency_ghz
        self.linewidth_ghz = linewidth_ghz
        self.noise_std = noise_std
        self.dip_depth = dip_depth
        self.baseline = baseline

    def connect(self):
        self.connection_status = "ON"

    def disconnect(self):
        self.connection_status = "OFF"

    def ideal_response(self, frequency_ghz: float) -> float:
        """Lorentzian dip: near 1.0 away from resonance, minimum at f0."""
        half_width = self.linewidth_ghz / 2
        detuning = (frequency_ghz - self.resonance_frequency_ghz) / half_width
        return self.baseline - self.dip_depth / (1 + detuning**2)

    def measure_response(self, frequency_ghz: float) -> float:
        if self.connection_status == "OFF":
            raise RuntimeError("Cannot measure: network analyzer is not connected.")

        ideal = self.ideal_response(frequency_ghz)
        noise = random.gauss(0, self.noise_std)
        return max(0.0, ideal + noise)

    def run_sweep(self) -> list[dict]:
        if self.connection_status == "OFF":
            raise RuntimeError("Cannot sweep: network analyzer is not connected.")

        frequencies = np.linspace(
            self.start_frequency_ghz,
            self.stop_frequency_ghz,
            self.num_points,
        )

        data = []
        for frequency_ghz in frequencies:
            data.append({
                "frequency_ghz": frequency_ghz,
                "response_amplitude": self.measure_response(frequency_ghz),
            })
        return data

    @classmethod
    def from_config(cls, config: dict) -> "MockNetworkAnalyzer":
        return cls(
            start_frequency_ghz=config["start_frequency_ghz"],
            stop_frequency_ghz=config["stop_frequency_ghz"],
            num_points=config["num_points"],
            resonance_frequency_ghz=config["resonance_frequency_ghz"],
            linewidth_ghz=config["linewidth_ghz"],
            noise_std=config.get("noise_std", 0.01),
            dip_depth=config.get("dip_depth", 0.7),
        )
