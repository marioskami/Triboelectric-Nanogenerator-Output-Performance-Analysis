TENG Data Analysis Toolkit

This repository contains Python tools for analysing experimental data from Triboelectric Nanogenerators (TENGs).
The scripts allow you to process raw oscilloscope/DAQ measurements, compare capacitor-charging behaviour, detect voltage/current/power peaks, and compute harvested energy per mechanical cycle.

Repository Contents
1. TENG_Comparison_Capacitors.py

This script compares how different capacitors charge when connected to a TENG.

Main Features

Loads voltage–time data from experimental measurements.
Cleans data and removes initial noise.
Detects maximum voltage and time to reach 90% of the maximum.
Plots charging curves for multiple capacitor values.

Useful for studying:

Effect of the connected capacitance to a TENG.
Effect of excitation frequency.
Performance of various material pairs.

2. TENG_Output_Performace_Analysis.py

A complete analysis pipeline for evaluating the output performance of a TENG.

Main Features

Loads oscilloscope CSV data.
Computes current from voltage (for resistive loads).
Computes instantaneous power.
Detects:
1.Voltage peaks,
2.Current peaks,
3.Power peaks.

Calculates:
1.Average peak voltage,
2.Average peak current,
3.Average peak power,
4.Energy under each power peak,
5.Total harvested energy,
6.Average energy per mechanical cycle.

Produces:
Plots for voltage, current, and power

