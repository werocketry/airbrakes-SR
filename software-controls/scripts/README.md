The Python code in this directory is aimed at parsing data files gathered by the system. It can process three distinct types of files:

- **Flight files from the onboard SD card**: These contain dense data, suitable for display in Excel or other spreadsheets. Setting these up can be time-consuming, and each file is unique. The provided code generates multiple plots of the flight data for further analysis.

- **Telemetry files from the ground station**: While smaller, the code presents all crucial data streams graphically.

- **Bench Test files from the flight computer**: Bench tests evaluate the system's performance by testing all the features specified in the settings file. Reviewing the bench test data before conducting an actual flight is advisable to spot potential issues.
