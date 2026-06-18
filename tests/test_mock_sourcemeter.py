from unittest.mock import patch

import pytest

from instruments.mock_sourcemeter import MockSourcemeter


def test_from_config_maps_json_fields(iv_config):
    sm = MockSourcemeter.from_config(iv_config)
    assert sm.get_simulated_resistance() == 100.0
    assert sm.noise_level == "LOW"
    assert sm.get_shots() == 11
    assert sm.get_voltage_range() == 1.0


def test_measure_current_follows_ohms_law(connected_sourcemeter):
    sm = connected_sourcemeter
    sm.set_voltage(10.0)

    with patch.object(sm, "get_noise", return_value=0.0):
        current = sm.measure_current()

    assert current == pytest.approx(0.1)


def test_measure_voltage_requires_connection():
    sm = MockSourcemeter()
    sm.enable_output()
    sm.set_voltage(1.0)

    with pytest.raises(RuntimeError, match="not connected"):
        sm.measure_voltage()


def test_measure_voltage_requires_output_enabled():
    sm = MockSourcemeter()
    sm.connect()
    sm.set_voltage(1.0)

    with pytest.raises(RuntimeError, match="output is disabled"):
        sm.measure_voltage()


def test_current_limit_raises_runtime_error(connected_sourcemeter):
    sm = connected_sourcemeter
    sm.set_current_limit(0.01)
    sm.set_voltage(10.0)

    with patch.object(sm, "get_noise", return_value=0.0):
        with pytest.raises(RuntimeError, match="Current limit exceeded"):
            sm.measure_current()
