# 🌕 Lunar Rover Sensor Data Simulation  

This project simulates **lunar environmental data** collected by a **rover** during different scenarios.  
Each dataset represents **1 hour (3600 seconds)** of recorded sensor readings.  

## 📁 Available Datasets  
These Files uploaded fill be used in different simulation scnearios:
- **`Scenario 1: Correct Collection of Data During Daytime`** ☀️  
  - **File: `lunar_rover_sunny_daytime_data.csv`**.  
  - **Temperature:** ~100°C with normal fluctuations.  
  - **Radiation Level:** Moderate due to **direct sunlight**.  
  - **Lunar Dust Activity:** Low, as dust settles in calm conditions.  
  - **Magnetic Field Variation:** Minimal changes.  
  - **Explanation:** The Lunar Rover collects data represented in the file without any interference of errors.

- **`Scenario 2: Correct Collection of Data During Nighttime`** 🌙  
  - **File:** `lunar_rover_nighttime_data.csv`.  
  - **Temperature:** ~ -170°C, extreme cold.  
  - **Radiation Level:** Lower than daytime, but still present.  
  - **Lunar Dust Activity:** **Higher** due to electrostatic charging.  
  - **Magnetic Field Variation:** Minimal.  
  - **Explanation:** The Lunar Rover collects data represented in the file without any interference of errors.

- **`Scenario 3.1: Rover experiences Hardware error`** ⚠️  
  - **File1:** `lunar_rover_day_hardware_error.csv`  
  - **Temperature Data:** Normal until failure, then **zeros recorded**.  
  - **Other Sensors:** Normal → then all **drop to zero** after failure.  
  - **Explanation:** The Lunar Rover is collecting normal DAYTIME data when it suddenly experiences a hardware error (0s) and we get notified (We can tell the rover to stop reading/pull put backup sensor-> 3.2.
- **`Scenario 3.2: Backup Sensor`** 🔄  
  - **File2:**`lunar_rover_with_backup_recovery.csv`
  - **Temperature Data:** Normal → Failure (zeros) → **Restored with backup sensor**.  
  - **Other Sensors:** Follow the same pattern.  
  - **Explanation:** After the hardware failure, we can **activate a backup sensor** which print the mentioned file. 

- **`Scenario 4.1: Rover out of sight (no signal)`** 🚨 
  - **Files:**`lunar_rover_no_signal.csv`
  - **All sensor values are 0** for the full duration (temperature, radiation, dust, magnetic field).  
  - **Explanation:** Rover goes **completely out of sight**, thus there is no communication (0s).  
- **`Scenario 4.2: Rover is told to move`** 🌑  
  - **Files:** `lunar_rover_shadowy_daytime_data.csv`.  
  - **Temperature:** ~ -50°C, lower due to shade.  
  - **Radiation Level:** Reduced due to limited sun exposure.  
  - **Lunar Dust Activity:** Moderate due to occasional disturbances.  
  - **Magnetic Field Variation:** Slightly higher in shadowed areas.  
  - **Explanation:** During daytime, we tell the rover to move so he can be on sight, and it moves to a more shadowy lunar area providing us the the file without any interference of errors.
