"""Shared pytest fixtures."""

import pytest

from instruments.mock_sourcemeter import MockSourcemeter


@pytest.fixture
def iv_config():
    return {
        "start_voltage": -1.0,
        "stop_voltage": 1.0,
        "num_points": 11,
        "resistance_ohms": 100.0,
        "noise_level": "LOW",
        "settling_time_seconds": 0.0,
    }


@pytest.fixture
def connected_sourcemeter():
    sm = MockSourcemeter(simulated_resistance=100.0, noise_level="LOW")
    sm.connect()
    sm.enable_output()
    yield sm
    sm.disable_output()
    sm.disconnect()
