from instruments.mock_network_analyzer import MockNetworkAnalyzer
from analysis.resonance_analysis import analyze_resonance
from plotting.plot_resonance import plot_resonance
from utils.file_manager import make_resonance_sweep_paths, save_to_csv


def run_resonance_sweep(
    config: dict,
    analyzer: MockNetworkAnalyzer | None = None,
) -> dict:
    """Run a frequency sweep, save CSV, plot, and analyze resonance parameters."""
    analyzer = analyzer or MockNetworkAnalyzer.from_config(config)

    analyzer.connect()
    print("Connected to MockNetworkAnalyzer.")

    try:
        start = config["start_frequency_ghz"]
        stop = config["stop_frequency_ghz"]
        print(f"Sweeping {start} GHz to {stop} GHz...")

        data = analyzer.run_sweep()
        print("Sweep complete.")

        csv_path, plot_path = make_resonance_sweep_paths()

        save_to_csv(data, csv_path)
        print(f"Data saved to {csv_path}.")

        fit = analyze_resonance(data)
        plot_resonance(data, plot_path, fit=fit)
        print(f"Plot saved to {plot_path}.")

        print(f"Estimated resonance frequency: {fit['resonance_frequency_ghz']:.4f} GHz")
        print(f"Estimated linewidth: {fit['linewidth_ghz']:.4f} GHz")
        print(f"Estimated Q: {fit['quality_factor']:.1f}")

        return {
            "data": data,
            "csv_path": csv_path,
            "plot_path": plot_path,
            "analysis": fit,
        }

    finally:
        analyzer.disconnect()
        print("Disconnected from MockNetworkAnalyzer.")
