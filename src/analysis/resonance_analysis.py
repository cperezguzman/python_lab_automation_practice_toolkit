import numpy as np
from scipy.optimize import curve_fit


def lorentzian_dip(
    frequency_ghz: np.ndarray,
    f0: float,
    linewidth_ghz: float,
    baseline: float,
    dip_depth: float,
) -> np.ndarray:
    half_width = linewidth_ghz / 2
    detuning = (frequency_ghz - f0) / half_width
    return baseline - dip_depth / (1 + detuning**2)


def find_resonance_frequency(data: list[dict]) -> float:
    """Return frequency at minimum response amplitude."""
    frequencies = np.array([row["frequency_ghz"] for row in data])
    responses = np.array([row["response_amplitude"] for row in data])
    return float(frequencies[np.argmin(responses)])


def estimate_linewidth(data: list[dict], f0: float, baseline: float, dip_depth: float) -> float:
    """Estimate FWHM linewidth from measured half-depth points."""
    frequencies = np.array([row["frequency_ghz"] for row in data])
    responses = np.array([row["response_amplitude"] for row in data])
    half_level = baseline - dip_depth / 2

    below = frequencies < f0
    above = frequencies > f0

    left_candidates = frequencies[below & (responses <= half_level)]
    right_candidates = frequencies[above & (responses <= half_level)]

    if len(left_candidates) == 0 or len(right_candidates) == 0:
        return float("nan")

    f_left = left_candidates[np.argmin(np.abs(left_candidates - f0))]
    f_right = right_candidates[np.argmin(np.abs(right_candidates - f0))]
    return float(f_right - f_left)


def calculate_quality_factor(resonance_frequency_ghz: float, linewidth_ghz: float) -> float:
    if linewidth_ghz <= 0:
        return float("nan")
    return resonance_frequency_ghz / linewidth_ghz


def analyze_resonance(data: list[dict]) -> dict:
    """Fit a Lorentzian dip and extract resonance parameters."""
    if not data:
        raise ValueError("Cannot analyze resonance: no measurement data.")

    frequencies = np.array([row["frequency_ghz"] for row in data])
    responses = np.array([row["response_amplitude"] for row in data])

    f0_guess = find_resonance_frequency(data)
    baseline_guess = float(np.max(responses))
    dip_depth_guess = float(baseline_guess - np.min(responses))
    linewidth_guess = 0.025

    freq_span = float(frequencies.max() - frequencies.min())

    popt, _ = curve_fit(
        lorentzian_dip,
        frequencies,
        responses,
        p0=[f0_guess, linewidth_guess, baseline_guess, dip_depth_guess],
        bounds=(
            [frequencies.min(), 1e-6, 0.0, 0.0],
            [frequencies.max(), freq_span, 2.0, 2.0],
        ),
        maxfev=10000,
    )

    f0, linewidth, baseline, dip_depth = popt
    q_factor = calculate_quality_factor(f0, linewidth)

    return {
        "resonance_frequency_ghz": float(f0),
        "linewidth_ghz": float(linewidth),
        "baseline": float(baseline),
        "dip_depth": float(dip_depth),
        "quality_factor": float(q_factor),
    }
