import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks, peak_widths

# === LOAD DATA ===
plotting = pd.read_csv('/home/kami/Desktop/Python2/CFT_PTFE_Al 1.5mm_10x10_2Hz_5mm/F1Trace00005.csv', delimiter=',')

TIME = plotting.iloc[:, 0].to_numpy()
VOLTAGE = plotting.iloc[:, 1].to_numpy()

# === COMPUTE CURRENT AND POWER ===
R = 40e6  #  Resistance
CURRENT = VOLTAGE / R
POWER = VOLTAGE * CURRENT  # Always positive for resistive load

# === PEAK DETECTION ===
# Voltage
v_pos_peaks, _ = find_peaks(VOLTAGE, height=50, distance=2000)
v_neg_peaks, _ = find_peaks(-VOLTAGE, height=40, distance=2000)
v_pos_vals = VOLTAGE[v_pos_peaks]
v_neg_vals = VOLTAGE[v_neg_peaks]

# Current
i_pos_peaks, _ = find_peaks(CURRENT, height=0.7e-6, distance=2000)
i_neg_peaks, _ = find_peaks(-CURRENT, height=0.7e-6, distance=2000)
i_pos_vals = CURRENT[i_pos_peaks]
i_neg_vals = CURRENT[i_neg_peaks]

# Power (only positive peaks)
p_peaks, _ = find_peaks(POWER, height=5e-5, distance=1200)
p_vals = POWER[p_peaks]

# === AVERAGE PEAK VALUES ===
if len(v_pos_vals) == len(v_neg_vals):
    V_avg = (np.sum(v_pos_vals) + np.sum(np.abs(v_neg_vals))) / len(v_pos_vals)
else:
    V_avg = np.nan

if len(i_pos_vals) == len(i_neg_vals):
    I_avg = (np.sum(i_pos_vals) + np.sum(np.abs(i_neg_vals))) / len(i_pos_vals)
else:
    I_avg = np.nan

# Power: average of all peak values divided by (number of peaks / 2)
if len(p_vals) > 0:
    P_avg = np.sum(p_vals) / (len(p_vals) / 2)
else:
    P_avg = np.nan

# === INTEGRATE AREA UNDER EACH POWER PEAK ===
peak_areas = []
peak_durations = []
widths, _, left_ips, right_ips = peak_widths(POWER, p_peaks, rel_height=0.98)

for i in range(len(p_peaks)):
    left = int(max(np.floor(left_ips[i]), 0))
    right = int(min(np.ceil(right_ips[i]), len(POWER)-1))
    t_segment = TIME[left:right]
    p_segment = POWER[left:right]
    area = np.trapz(p_segment, t_segment)
    duration = TIME[right] - TIME[left]
    peak_areas.append(area)
    peak_durations.append(duration)

# === PLOTTING ===
fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# Voltage
ax[0].plot(TIME, VOLTAGE, label='Voltage', color='blue')
ax[0].scatter(TIME[v_pos_peaks], v_pos_vals, color='red', label='Max Peaks')
ax[0].scatter(TIME[v_neg_peaks], v_neg_vals, color='green', label='Min Peaks')
ax[0].set_ylabel('Voltage (V)', fontsize = 20)
ax[0].tick_params(axis='y', labelsize =15)
ax[0].legend()
ax[0].grid(True)

# === CURRENT PLOT WITH AREA UNDER EACH PEAK ===
ax[1].plot(TIME, CURRENT*1e6, label='Current', color='purple')

# Scatter the peaks
ax[1].scatter(TIME[i_pos_peaks], i_pos_vals*1e6, color='red', label='Max Peaks')
ax[1].scatter(TIME[i_neg_peaks], i_neg_vals*1e6, color='green', label='Min Peaks')

# Fill area under positive current peaks
#widths_pos, _, left_ips_pos, right_ips_pos = peak_widths(CURRENT, i_pos_peaks, rel_height=0.98)
#for i in range(len(i_pos_peaks)):
#    left = int(max(np.floor(left_ips_pos[i]), 0))
#    right = int(min(np.ceil(right_ips_pos[i]), len(CURRENT)-1))
#    t_segment = TIME[left:right]
#    i_segment = CURRENT[left:right]
#    i_segment = np.copy(CURRENT[left:right])
#    i_segment[i_segment < 0] = 0  # for positive peaks
#    ax[1].fill_between(t_segment, i_segment, 0, color='orange', alpha=0.5)

# Fill area under negative current peaks
#widths_neg, _, left_ips_neg, right_ips_neg = peak_widths(-CURRENT, i_neg_peaks, rel_height=0.98)
#for i in range(len(i_neg_peaks)):
#    left = int(max(np.floor(left_ips_neg[i]), 0))
#    right = int(min(np.ceil(right_ips_neg[i]), len(CURRENT)-1))
#    t_segment = TIME[left:right]
##    i_segment = CURRENT[left:right]
 #   i_segment = np.copy(CURRENT[left:right])
 #   i_segment[i_segment > 0] = 0
 #   ax[1].fill_between(t_segment, i_segment, 0, color='cyan', alpha=0.5)

ax[1].set_ylabel('Current ($\mu$A)', fontsize = 20)
ax[1].tick_params(axis='y', labelsize = 15)
ax[1].legend()
ax[1].grid(True)


# Power
ax[2].plot(TIME, POWER*1e6, label='Power', color='darkgreen')
ax[2].scatter(TIME[p_peaks], p_vals*1e6, color='red', label= 'Max Peaks')
for i in range(len(p_peaks)):
    left = int(max(np.floor(left_ips[i]), 0))
    right = int(min(np.ceil(right_ips[i]), len(POWER)-1))
    t_segment = TIME[left:right]
    p_segment = POWER[left:right]
    ax[2].fill_between(t_segment, p_segment*1e6, 0, color='orange', alpha=0.3)
ax[2].set_ylabel('Power ($\mu$W)', fontsize =20)
ax[2].tick_params(axis = 'y', labelsize =15)
ax[2].legend()
ax[2].grid(True)

plt.xlabel('Time (s)', fontsize = 20)
plt.tick_params(axis='x', labelsize=15)
plt.tight_layout()
plt.show()

# === PRINT SUMMARY ===
print("\n--- Peak Summary ---")
print(f"Voltage peaks: {len(v_pos_peaks)} max, {len(v_neg_peaks)} min")
print(f"Average peak voltage: {V_avg:.3f} V")

print(f"\nCurrent peaks: {len(i_pos_peaks)} max, {len(i_neg_peaks)} min")
print(f"Average peak current: {I_avg:.3e} A")

print(f"\nPower peaks: {len(p_peaks)} positive only")
print(f"Average power peak (adjusted): {P_avg:.3e} W")

# === ENERGY INTEGRATION ===
print("\n--- Power Peak Integration ---")
for i, (area, duration) in enumerate(zip(peak_areas, peak_durations)):
    print(f"Power Peak {i+1}: Energy = {area:.2e} J, Duration = {duration:.4f} s")

total_energy = np.sum(peak_areas)
print(f"\nTotal energy from power peaks: {total_energy:.2e} J")

# === AVERAGE ENERGY PER CYCLE ===
# Each cycle is made of two consecutive power peaks (contact + separation)
cycle_areas = []

# Only process if there's an even number of power peaks
num_cycles = len(peak_areas) // 2
for i in range(0, 2 * num_cycles, 2):
    cycle_energy = peak_areas[i] + peak_areas[i + 1]
    cycle_areas.append(cycle_energy)
    print(f"Cycle {i//2 + 1}: Energy = {cycle_energy:.2e} J")


if cycle_areas:
    avg_cycle_energy = np.mean(cycle_areas)
    print(f"\nAverage energy per cycle (2 peaks): {avg_cycle_energy:.2e} J")
else:
    print("\nNot enough power peaks to compute energy per cycle.")

