import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# === Folder and file names for capacitor charging data ===
folder = '/home/kami/Desktop/Python2/malakies'
files = [
    '26-06-2025 PTFE NYLON 5x5 2 Hz 1 uF.xls',
    '26-06-2025 PTFE NYLON 5x5 2 Hz 10 uF.xls',
]

labels = ['1µF', '10µF', '3Hz', '4Hz']
colors = ['blue', 'red', 'green', 'purple']

# === Plot setup ===
plt.figure(figsize=(12, 6))

for i, filename in enumerate(files):
    path = os.path.join(folder, filename)

    # === Read file with space separator and comma as decimal ===
    df = pd.read_csv(
        path,
        sep=r'\s+',
        header=None,
        names=['Time', 'Voltage'],
        decimal=','
    )

    # === Clean and filter data ===
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df['Voltage'] = pd.to_numeric(df['Voltage'], errors='coerce')
    df = df.dropna()

    # === Remove early noise (optional threshold in ms) ===
    time_threshold_ms = 500
    df = df[df['Time'] >= time_threshold_ms].reset_index(drop=True)

    # === Time reset and unit conversion ===
    df['Time'] = df['Time'] - df['Time'].iloc[0]
    time_s = df['Time'].to_numpy() / 1000  # ms to s
    voltage = df['Voltage'].to_numpy()

    # === Find max voltage and 90% point ===
    max_voltage = voltage.max()
    max_idx = voltage.argmax()
    time_at_max = time_s[max_idx]

    target_voltage = 0.9 * max_voltage
    above_90 = np.where(voltage >= target_voltage)[0]
    if len(above_90) > 0:
        idx_90 = above_90[0]
        time_90 = time_s[idx_90]
    else:
        time_90 = np.nan

    # === Plot all starting from time zero ===
    plt.plot(time_s, voltage, label=labels[i], color=colors[i])
    plt.scatter(time_s[max_idx], max_voltage, color='black', marker='x')
    #plt.axvline(time_90, color=colors[i], linestyle='--', alpha=0.4, label=f'{labels[i]} @90%' if i == 0 else "")

# === Final formatting ===
plt.xlabel('Time (s)', fontsize= 30)
plt.ylabel('Voltage (V)', fontsize = 30 )
plt.tick_params(labelsize =20)
#plt.title(' Capacitor Charging Curves (External Vibration Frequency : 2 Hz)')
plt.grid(True)
plt.ylim(bottom=0)
plt.legend(prop={'size': 15})
plt.tight_layout()
plt.show()
