"""
Well Production Analysis (simulated data)
-----------------------------------------
Simulates one year of daily oil production for 20 wells, fits an
exponential decline curve to each well with NumPy, and flags
underperforming wells.

Model: q(t) = q0 * exp(-D * t)
Taking logs:  ln q = ln q0 - D * t   -> a straight line, so np.polyfit works.
"""
import numpy as np

rng = np.random.default_rng(42)

N_WELLS = 20
DAYS = 365
t = np.arange(DAYS)

# ---- 1. Simulate data (barrels per day) ----
q0_true = rng.uniform(80, 200, N_WELLS)        # initial rate
D_true = rng.uniform(0.0005, 0.003, N_WELLS)   # daily decline rate
D_true[[3, 11, 16]] *= 3                       # a few wells decline much faster

noise = rng.normal(1.0, 0.05, (N_WELLS, DAYS))
rates = q0_true[:, None] * np.exp(-D_true[:, None] * t) * noise

# ---- 2. Fit decline curve for each well ----
avg_rate = rates.mean(axis=1)
final_rate = rates[:, -30:].mean(axis=1)       # average of last 30 days
D_fit = np.empty(N_WELLS)
for i in range(N_WELLS):
    slope, intercept = np.polyfit(t, np.log(rates[i]), 1)
    D_fit[i] = -slope

# ---- 3. Flag underperforming wells ----
D_threshold = D_fit.mean() + D_fit.std()       # unusually fast decline
rate_threshold = np.percentile(avg_rate, 25)   # bottom 25% by average rate
flag_decline = D_fit > D_threshold
flag_low = avg_rate < rate_threshold
flagged = flag_decline | flag_low

# ---- 4. Report ----
print(f"{'Well':<6}{'Avg rate':>10}{'Last 30d':>10}{'Decline/day':>13}  Flag")
for i in range(N_WELLS):
    reason = []
    if flag_decline[i]:
        reason.append("fast decline")
    if flag_low[i]:
        reason.append("low output")
    print(f"W{i+1:<5}{avg_rate[i]:>10.1f}{final_rate[i]:>10.1f}{D_fit[i]:>13.5f}  {', '.join(reason)}")

print(f"\nFlagged wells: {flagged.sum()} of {N_WELLS}")

# ---- 5. Save results ----
header = "well,avg_rate,last30_rate,decline_per_day,flagged"
table = np.column_stack([np.arange(1, N_WELLS + 1), avg_rate, final_rate, D_fit, flagged.astype(int)])
np.savetxt("results.csv", table, delimiter=",", header=header, comments="", fmt=["%d", "%.2f", "%.2f", "%.6f", "%d"])
print("Results saved to results.csv")
