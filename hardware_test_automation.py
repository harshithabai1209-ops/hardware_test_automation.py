"""
PDN Automated Test Script
Target: Digantara Satellite Payload PDN Validation
Author: Harshitha Bai C
Description: Automates the verification of +3.6V, +1.8V, +3.3V, and +2.5V 
             voltage rails and logs average DC values via PyVISA.
"""

import pyvisa
import time
import csv
from datetime import datetime

# Define rail specifications and tolerances
RAIL_SPECS = {
    "+3V6": {"nominal": 3.6, "tolerance": 0.05},
    "+1V8": {"nominal": 1.8, "tolerance": 0.05},
    "+3V3": {"nominal": 3.3, "tolerance": 0.05},
    "+2V5": {"nominal": 2.5, "tolerance": 0.05}
}

def run_pdn_validation():
    print("Initializing Automated PDN Test Sequence...")
    rm = pyvisa.ResourceManager()
    
    # Update resource strings based on your actual lab equipment addresses
    try:
        psu = rm.open_resource('USB0::0x0957::0x0707::MY53000101::INSTR') # Example PSU address
        scope = rm.open_resource('USB0::0x2A8D::0x0101::MY60000102::INSTR') # Example Scope address
    except pyvisa.VisaIOError as e:
        print(f"Connection Error: Could not connect to instruments. Details: {e}")
        return

    # Configure Input Power Supply (+5V Regulated Input)
    print("Configuring DC Power Supply to 5.0V...")
    psu.write("OUTPUT OFF")
    psu.write("APPLy CH1, 5.0, 1.0") # Set 5V with a 1A current limit safety threshold
    psu.write("OUTPUT ON")
    time.sleep(2) # Allow power rail setup to stabilize

    # Prepare CSV file for telemetry logging
    csv_filename = f"PDN_Validation_Log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Rail Name", "Measured Voltage (V)", "Status"])
        
        # Iterate and validate each individual rail sequentially
        # Channel mappings correspond to instrument probe setup configurations
        channels = {"+3V6": "CHAN1", "+1V8": "CHAN2", "+3V3": "CHAN3", "+2V5": "CHAN4"}
        
        for rail, chan in channels.items():
            # Query the average DC voltage from the oscilloscope
            scope.write(f"MEASure:VAVerage {chan}")
            measured_val = float(scope.query(f"MEASure:VAVerage? {chan}"))
            
            # Calculate acceptable boundary limits
            nominal = RAIL_SPECS[rail]["nominal"]
            tol = RAIL_SPECS[rail]["tolerance"]
            v_min = nominal * (1 - tol)
            v_max = nominal * (1 + tol)
            
            status = "PASS" if v_min <= measured_val <= v_max else "FAIL"
            
            print(f"Rail {rail}: Measured {measured_val:.3f}V | Criterion: {v_min:.2f}V - {v_max:.2f}V -> {status}")
            writer.writerow([datetime.now().isoformat(), rail, f"{measured_val:.3f}", status])
            
    # Safe shutdown profile
    psu.write("OUTPUT OFF")
    print(f"Test Complete. Telemetry successfully written to {csv_filename}")

if __name__ == "__main__":
    run_pdn_validation()
