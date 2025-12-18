# ===========================================================
# HORIZONTAL TANK CALIBRATION: Geometric vs Measured Volume
# ===========================================================
# Features:
#   - Prompts user for tank dimensions (R, L)
#   - Reads input_data.csv (columns: height [cm], volume [L])
#   - Calculates theoretical volumes using geometric relation
#   - Exports a CSV of results
#   - Plots measured vs theoretical volume with zoomed deviation
# ===========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 1. User Inputs
# -----------------------------------------------------------
print("Enter tank parameters (use consistent units, e.g., cm for R & L):")
R = float(input("Enter internal radius R (cm): "))
L = float(input("Enter cylindrical length L (cm): "))

# Conversion: 1 L = 1000 cm³
CM3_TO_L = 1 / 1000

# -----------------------------------------------------------
# 2. Load measured data
# -----------------------------------------------------------
df = pd.read_csv("input_data.csv")
df.columns = ["height", "V_measured"]

h_measured = df["height"].values

# -----------------------------------------------------------
# 3. Compute Theoretical Volumes from Geometric Height Relation
# -----------------------------------------------------------
h_geo = np.clip(h_measured, 0, 2 * R)

# Horizontal cylindrical tank (flat ends)
V_theoretical_cm3 = L * (
    R**2 * np.arccos((R - h_geo) / R)
    - (R - h_geo) * np.sqrt(2 * R * h_geo - h_geo**2)
)
V_theoretical_L = V_theoretical_cm3 * CM3_TO_L

df["V_theoretical"] = V_theoretical_L
df["deviation"] = df["V_measured"] - df["V_theoretical"]

# -----------------------------------------------------------
# 4. Identify Deviation Extremes
# -----------------------------------------------------------
max_dev_idx = np.argmax(np.abs(df["deviation"]))
min_dev_idx = np.argmin(np.abs(df["deviation"]))

max_dev_h = df.loc[max_dev_idx, "height"]
min_dev_h = df.loc[min_dev_idx, "height"]

# -----------------------------------------------------------
# 5. Export Results
# -----------------------------------------------------------
output_file = "geometric_calibration_comparison.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ Results saved to '{output_file}'")

# -----------------------------------------------------------
# 6. Plot: Measured vs Theoretical + Deviation (Zoomed)
# -----------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 6))

# Primary plot (Measured vs Theoretical)
ax1.plot(df["height"], df["V_measured"], 'r-', linewidth=2, label=r'Measured Volume $V_{measured}(h)$')
ax1.plot(df["height"], df["V_theoretical"], 'b--', linewidth=2, label=r'Theoretical Volume $V_{theoretical}(h)$')

# Highlight deviation points
ax1.scatter(max_dev_h, df.loc[max_dev_idx, "V_measured"], color='darkred', s=80, zorder=5,
            label=fr'Max deviation at $h = {max_dev_h:.1f}$ cm')
ax1.scatter(min_dev_h, df.loc[min_dev_idx, "V_measured"], color='green', s=80, zorder=5,
            label=fr'Min deviation at $h = {min_dev_h:.1f}$ cm')

ax1.set_xlabel("Height h (cm)", fontsize=12)
ax1.set_ylabel("Volume V (L)", fontsize=12)
ax1.set_title("Measured vs Theoretical Volume (Horizontal Cylindrical Tank)", fontsize=13)
ax1.grid(alpha=0.4)
ax1.legend(loc="upper left")

# Secondary Y-axis: deviation (zoomed scale)
ax2 = ax1.twinx()
ax2.plot(df["height"], df["deviation"], 'k:', linewidth=1.5, label=r'Deviation $\Delta V(h)$')
ax2.set_ylabel("Deviation ΔV (L)", fontsize=12, color='k')
ax2.tick_params(axis='y', labelcolor='k')

# Annotate max/min deviation on secondary axis
ax2.scatter(max_dev_h, df.loc[max_dev_idx, "deviation"], color='darkred', marker='x', s=80)
ax2.scatter(min_dev_h, df.loc[min_dev_idx, "deviation"], color='green', marker='x', s=80)
ax2.text(max_dev_h, df.loc[max_dev_idx, "deviation"]*1.05,
         f"ΔVₘₐₓ = {df.loc[max_dev_idx, 'deviation']:.2f} L", color='darkred', fontsize=9)
ax2.text(min_dev_h, df.loc[min_dev_idx, "deviation"]*1.05,
         f"ΔVₘᵢₙ = {df.loc[min_dev_idx, 'deviation']:.2f} L", color='green', fontsize=9)

fig.tight_layout()
plt.savefig("Measured_vs_Theoretical_with_Zoomed_Deviation.png", dpi=300)
plt.show()

# -----------------------------------------------------------
# END OF SCRIPT
# -----------------------------------------------------------
