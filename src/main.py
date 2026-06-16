"""Entry point for lab automation experiments."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from experiments.iv_sweep import run_iv_sweep
from experiments.resonance_sweep import run_resonance_sweep
from utils.config_loader import (
    DEFAULT_IV_CONFIG,
    DEFAULT_RESONANCE_CONFIG,
    load_config,
)


def main():
    parser = argparse.ArgumentParser(
        description="Python lab automation toolkit — mock instrument experiments."
    )
    parser.add_argument(
        "--experiment",
        choices=["iv", "resonance"],
        default="iv",
        help="Experiment to run (default: iv)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to JSON config file (defaults to config/<experiment>_config.json)",
    )
    args = parser.parse_args()

    if args.experiment == "iv":
        config_path = Path(args.config) if args.config else DEFAULT_IV_CONFIG
        config = load_config(config_path)
        print("Starting I-V sweep...")
        run_iv_sweep(config)

    elif args.experiment == "resonance":
        config_path = Path(args.config) if args.config else DEFAULT_RESONANCE_CONFIG
        config = load_config(config_path)
        print("Starting resonance sweep...")
        run_resonance_sweep(config)


if __name__ == "__main__":
    main()
