# hardware_test_automation.py
Satellite Payload Power Distribution Network (PDN) Validation and Test Automation
# PDN Automated Test Automation Framework

This repository contains the automated test script used to qualify the Power Distribution Network (PDN) designed for satellite payload subsystems. 

## Overview
The framework connects directly to programmable lab instrumentation to execute automated cross-rail voltage sequencing checks and measure baseline rail telemetry.

### Supported Lab Instrumentation
* **Programmable DC Power Supply:** Keithley 2230-30-1
* **Digital Oscilloscope:** Keysight DSOX6004A
* **Digital Multimeter:** Keithley DMM6500

## Script Capabilities
* **Automated Instrumentation Control:** Uses SCPI commands via `PyVISA` to control input power grids.
* **Tolerance Validation:** Dynamically checks output levels against the designated strict $\pm5\%$ flight hardware parameter limits.
* **Telemetric Data Logging:** Auto-saves time-stamped metrics to a shareable structured CSV profile for validation compliance.

## Getting Started

### Prerequisites
Ensure your local testing terminal environment includes the national instruments VISA layer and the Python dependencies:
```bash
pip install pyvisa
