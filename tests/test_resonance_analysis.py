import numpy as np
import pytest

from analysis.resonance_analysis import (
    analyze_resonance,
    calculate_quality_factor,
    find_resonance_frequency,
    lorentzian_dip,
)


def test_analyze_resonance_recovers_f0_on_clean_data():
    f0 = 5.0
    linewidth = 0.025
    baseline = 1.0
    depth = 0.7
    frequencies = np.linspace(4.8, 5.2, 201)
    responses = lorentzian_dip(frequencies, f0, linewidth, baseline, depth)

    data = [
        {"frequency_ghz": float(f), "response_amplitude": float(r)}
        for f, r in zip(frequencies, responses)
    ]

    fit = analyze_resonance(data)
    assert fit["resonance_frequency_ghz"] == pytest.approx(5.0, abs=0.01)
    assert fit["linewidth_ghz"] == pytest.approx(0.025, abs=0.005)
    assert fit["quality_factor"] == pytest.approx(200.0, rel=0.05)


def test_lorentzian_minimum_at_resonance():
    f0 = 5.0
    response_at_f0 = lorentzian_dip(
        np.array([f0]), f0, 0.025, baseline=1.0, dip_depth=0.7
    )[0]
    response_off_resonance = lorentzian_dip(
        np.array([4.8]), f0, 0.025, baseline=1.0, dip_depth=0.7
    )[0]

    assert response_at_f0 == pytest.approx(0.3)
    assert response_off_resonance > response_at_f0


def test_find_resonance_frequency_uses_minimum():
    data = [
        {"frequency_ghz": 4.9, "response_amplitude": 0.9},
        {"frequency_ghz": 5.0, "response_amplitude": 0.2},
        {"frequency_ghz": 5.1, "response_amplitude": 0.85},
    ]
    assert find_resonance_frequency(data) == 5.0


def test_calculate_quality_factor():
    assert calculate_quality_factor(5.0, 0.025) == pytest.approx(200.0)


def test_analyze_resonance_empty_data_raises():
    with pytest.raises(ValueError, match="no measurement data"):
        analyze_resonance([])
