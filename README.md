# Well Production Analysis (simulated data)

A small Python/NumPy project that simulates one year of daily oil production
for 20 wells, fits an exponential decline curve to each well, and flags
underperforming wells.

> **Note:** all data is simulated. No real well data is used.

## What it does
1. Simulates daily production rates with noise (`q(t) = q0 * exp(-D * t)`).
2. Fits the decline rate `D` for each well using log-linear regression (`np.polyfit`).
3. Flags wells with an unusually fast decline (above mean + 1 std) or low average output (bottom 25%).
4. Prints a summary table and saves `results.csv`.

## Run
```
pip install numpy
python well_analysis.py
```

## Possible next steps
- Plot production curves with Matplotlib
- Replace simulated data with a real dataset
- Try other decline models (hyperbolic)
