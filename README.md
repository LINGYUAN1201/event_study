# Event Study Analysis Package

An event study analysis package for conducting financial event studies using various models and statistical tests.

## Overview
This Python package allows users to perform event study analyses on financial data. It supports multiple models, including the Market Model, Market-Adjusted Model, and Fama-French Factor Models (3-Factor, 4-Factor, and 5-Factor models). Users can specify the event window, estimation window, and choose whether to generate visualizations.

## Features
- **Multiple Models**: Supports Market Model, Market-Adjusted Model, and Fama-French 3F, 4F, and 5F models.
- **Statistical Tests**: Performs t-tests, Wilcoxon signed-rank test, Binomial sign test, and Permutation test.
- **Customizable Parameters**: Users can specify models to use, event window size, estimation window size, and more.
- **Visualization**: Optionally generate and save plots of Average Abnormal Returns (AR) over the event window.
- **Output Files**:
    - `event_study_individual_CAR_results_with_tests.xlsx`: Contains average cumulative abnormal returns (CAR) and statistical test results for each event.
    - `event_study_CAR_last_day_tests.xlsx`: Contains CAR on the last day of the event window for each event.
    - `event_study_daily_AR_results_with_tests.xlsx`: Contains average AR and statistical test results for each event day.
    - AR trend plots for each model (e.g., AR_MarketModel.png).

## Installation
### Install via GitHub
You can install the package directly from GitHub using `pip`:

```python
pip install git+https://github.com/your_username/event_study.git
```

### Requirements
- Python 3.6 or higher
- Dependencies:
    - pandas
    - numpy
    - matplotlib
    - seaborn
    - statsmodels
    - scipy
    - xlsxwriter

These dependencies will be installed automatically when you install the package.

## Usage
Ensure you have the following Excel files in your working directory or specify their paths:
- `Event.xlsx`
- `Firm.xlsx`
- `Market.xlsx`
- `FF factor.xlsx`

### Running an Event Study
Create a Python script (e.g., `run_event_study.py`) with the following content:

```python
from event_study.main import run_event_study

# Specify parameters
models_to_use = ['MarketModel', 'MarketAdjusted', '3F', '4F', '5F']  # Models to use
event_window_days = (-1, 4)  # Event window size
estimation_window_days = 250  # Estimation window size
generate_plots = True  # Whether to generate AR trend plots

# Data file paths
event_file = 'Event.xlsx'
firm_file = 'Firm.xlsx'
market_file = 'Market.xlsx'
ff_factors_file = 'FF factor.xlsx'

# Run the event study analysis
run_event_study(
    models_to_use=models_to_use,
    event_window_days=event_window_days,
    estimation_window_days=estimation_window_days,
    generate_plots=generate_plots,
    event_file=event_file,
    firm_file=firm_file,
    market_file=market_file,
    ff_factors_file=ff_factors_file
)
```

## Package Structure
```python
event_study/
├── __init__.py
├── data_loader.py
├── statistical_tests.py
├── regression_models.py
├── car_calculations.py
└── main.py
├─ setup.py
└─ requirements.txt
```

## Contributing
Contributions are welcome! If you have suggestions or find bugs, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
This package is provided for educational and research purposes. The author is not responsible for any decisions made based on the results produced by this package.

## Contact
Author: Ling Yuan

Email: LingYUAN1201@outlook.com
