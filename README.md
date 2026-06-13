# Python Lab Automation Practice Toolkit

A Python toolkit that simulates instrument-controlled I-V sweep measurements using a mock sourcemeter.

## Overview

This project simulates lab automation workflows commonly used in electronics testing and hardware characterization. It uses a **mock sourcemeter** (no real hardware required) to sweep voltage, measure current using Ohm's law with added noise, save results to CSV, and generate an I-V plot.

The instruments are simulated. The goal is to demonstrate measurement procedure, data handling, and plotting in a structure that could later connect to real instruments (for example via PyVISA).

## Features

- Mock sourcemeter with connect/disconnect, output enable/disable, and safety checks
- Automated I-V sweep over a configurable voltage range
- Gaussian noise model with LOW / MEDIUM / HIGH levels
- CSV data logging
- Automatic I-V plot generation with matplotlib
- Safe instrument shutdown using `try` / `finally`

## Installation

**Requirements:** Python 3.10+

```bash
git clone https://github.com/cperezguzman/python_lab_automation_practice_toolkit.git
cd python_lab_automation_practice_toolkit

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

On Ubuntu/Debian, if `pip install` fails with an `externally-managed-environment` error, use the virtual environment steps above instead of installing packages system-wide.

## Usage

With the virtual environment activated:

```bash
python iv_sweep.py
```

Expected terminal output:

```text
Connected to sourcemeter.
Enabled sourcemeter output.
Commencing measurement process.
Saved to CSV file.
Saved plot to PNG file.
Successfully disabled and disconnected the sourcemeter.
```

**Outputs:**

- `data/raw/iv_sweep_results.csv` — voltage and current measurements
- `plots/iv/iv_sweep_results_graph.png` — I-V curve plot

## Example Output

![I-V sweep plot](examples/screenshots/iv_sweep.png)

## Project Structure

```text
python_lab_automation_practice_toolkit/
├── iv_sweep.py              # Mock sourcemeter, sweep, CSV export, plotting
├── requirements.txt
├── README.md
├── data/raw/                # CSV output (generated at runtime)
├── plots/iv/                # Plot output (generated at runtime)
└── examples/screenshots/    # Example plot for documentation
```

## Technologies

- Python 3
- NumPy — voltage sweep arrays
- Matplotlib — I-V plotting
- CSV (stdlib) — data logging

## Future Improvements

- Timestamped output filenames
- JSON configuration files for sweep parameters
- Modular package layout (`src/instruments/`, `src/experiments/`, etc.)
- Resonance sweep experiment
- Resistance estimation from I-V slope
- Unit tests
