"""Entry point for lab automation experiments."""

import argparse
import sys
from pathlib import Path

# Allow imports from src/ when running as `python src/main.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))

from experiments.iv_sweep import run_iv_sweep


def main():
    parser = argparse.ArgumentParser(
        description="Python lab automation toolkit — mock instrument experiments."
    )
    parser.add_argument(
        "--experiment",
        choices=["iv"],
        default="iv",
        help="Experiment to run (default: iv)",
    )
    args = parser.parse_args()

    if args.experiment == "iv":
        print("Starting I-V sweep...")
        run_iv_sweep()


if __name__ == "__main__":
    main()
