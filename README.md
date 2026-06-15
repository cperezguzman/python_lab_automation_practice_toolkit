# Python Lab Automation Practice Toolkit

A Python toolkit that simulates instrument-controlled I-V sweep measurements using a mock sourcemeter.

## Overview

This project simulates lab automation workflows commonly used in electronics testing and hardware characterization. It uses a **mock sourcemeter** (no real hardware required) to sweep voltage, measure current using Ohm's law with added noise, save results to CSV, and generate an I-V plot.

The instruments are simulated. The goal is to demonstrate measurement procedure, data handling, and plotting in a structure that could later connect to real instruments (for example via PyVISA).

## Features

- Mock sourcemeter with connect/disconnect, output enable/disable, and safety checks
- Automated I-V sweep over a configurable voltage range
- Gaussian noise model with LOW / MEDIUM / HIGH levels
- Timestamped CSV data logging
- Automatic I-V plot generation with matplotlib
- Resistance estimation from I-V slope
- Safe instrument shutdown using `try` / `finally`
- Modular project layout under `src/`

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

With the virtual environment activated, from the project root:

```bash
python src/main.py --experiment iv
```

Expected terminal output:

```text
Starting I-V sweep...
Connected to sourcemeter.
Enabled sourcemeter output.
Commencing measurement process.
Data saved to data/raw/iv_sweep_2026-05-20_150214.csv
Plot saved to plots/iv/iv_sweep_2026-05-20_150214.png
Estimated resistance: 50.09 ohms
Successfully disabled and disconnected the sourcemeter.
```

**Outputs** (timestamped, generated at runtime):

- `data/raw/iv_sweep_<timestamp>.csv`
- `plots/iv/iv_sweep_<timestamp>.png`

## Example Output

![I-V sweep plot](examples/screenshots/iv_sweep.png)

## Project Structure

```text
python_lab_automation_practice_toolkit/
├── src/
│   ├── main.py                    # CLI entry point
│   ├── instruments/
│   │   ├── base_instrument.py
│   │   └── mock_sourcemeter.py
│   ├── experiments/
│   │   └── iv_sweep.py            # I-V measurement procedure
│   ├── analysis/
│   │   └── iv_analysis.py         # Resistance estimation
│   ├── plotting/
│   │   └── plot_iv.py
│   └── utils/
│       └── file_manager.py        # CSV save, timestamped paths
├── requirements.txt
├── README.md
├── data/raw/                      # CSV output (gitignored)
├── plots/iv/                      # Plot output (gitignored)
└── examples/screenshots/          # Example plot for documentation
```

## Technologies

- Python 3
- NumPy — voltage sweep arrays and linear fit
- Matplotlib — I-V plotting
- CSV (stdlib) — data logging

## Future Improvements

- JSON configuration files for sweep parameters
- Resonance sweep experiment
- Unit tests
- Mock vs real instrument mode (PyVISA)
