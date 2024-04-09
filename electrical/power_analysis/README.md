The power supply for the project relies on Lithium-ion (Li-ion) batteries, selected for their high energy density and efficiency. The choice of Li-ion batteries was heavily influenced by competition rules that explicitly ban the use of Lithium Polymer (LiPo) batteries \[4\] and our research showed that this is a common alternative used in the SAC competition. In selection of the battery cells the capacity, max discharge rate, and voltage requirements were considered. The power consumption ratings for each of the relevant components is given in Table 1.

**Table 1: Power Consumption of Relevant Electrical Components.**

| Component                   | Electrical Power         | Details                                                                                      |
|-----------------------------|--------------------------|----------------------------------------------------------------------------------------------|
| Portenta H7                 | 2.6 mA @ 3.7V            | Current consumption in busy loop (@5V) \[max with on board LEDs off\].                       |
| Nicla Sense ME              | 2.5 mA @ 3.7V            | Power consumption advertising with sensor polling at 1Hz \[max consumption state\].          |
| L298N Motor Driver (VEN=L)  | 4 mA @ 12V<br>6mA @ 5V   | Quiescent supply & VSS current of inactive driver \[max value of range taken\].             |
| L298N Motor Driver (VEN=H)  | 22 mA @ 12V<br>36 mA @ 12V | Quiescent supply & VSS current of active driver \[max value of range taken\].               |
| Brushed DC Motor            | 5000 mA @ 12V            | Stall current of the selected motor.                                                         |
| Hall Effect Sensor          | 6.9 mA @ 5V              | Supply current of the IC.                                                                    |

To calculate the required capacity, the 20-hour required standby time given in ER-003 and an active motor time of 10 seconds (approximately a FOS of double the predicted motor action time. This yields a total required capacity of approximately 400 mAh, the calculations are broken down in Table 2. The datasheet for the Arduino Portenta recommends a greater minimum of 700 mAh for battery powered use and this will hence be used as the single cell minimum herein.

**Table 2: Energy Requirement Breakdown.**

| Phase      | Component               | Current (mA) | Voltage (V) | Active Time | Energy Required (mAh) |
|------------|-------------------------|--------------|-------------|-------------|-----------------------|
| Standby    | Portenta H7             | 2.6          | 3.7         | 20h         | 52                    |
|            | Nicla Sense ME          | 2.5          | 3.7         | 20h         | 50                    |
|            | L298N Motor Driver      | 6            | 5           | 20h         | 120                   |
|            | Hall Effect Sensor      | 6.9          | 5           | 20h         | 138                   |
| Standby Subtotal                  |               |             |             |                       | 360                   |
| Active     | Brushed DC Motor        | 5000         | 12          | 20s         | 27.78                 |
|            | L298N Motor Driver (Active) | 36       | 12          | 20s         | 0.2                   |
| Active Subtotal                  |               |             |             |                       | 27.98                 |
| **Total Required Energy**        |               |             |             |                       | 387.98                |

The MCU board is supplied with by a single 3.7V cell which the onboard regulator regulates to 5V to power the 5V components. The DC motor is rated at 12V therefore 3 cells are required to reach the required potential which results in a nominal 11.1V (within 10%). As the cells will be wired in a 3 series (3S) configuration each must independently be capable of supplying the maximum current of the motor, that is 5000 mA which sets the required minimum discharge current.

This gives a selection criterion of three cells rated at least 700 mAh each with a minimum discharge rate of 5000 mA. The Panasonic NCR18650GA 3450mAh 10A Battery was chosen for this application as it meets and exceeds these required specifications while remaining well within budget. It's important to note that most modern lithium-ion cells, even those that are more affordably priced, meet or exceed the required specifications for this project making the exact product selection rather arbitrary. Therefore, the specific selection of the product was primarily driven by the reputable brand name, price point, and supplier accessibility. The power to the microcontroller uses the same model of low-power switch as for the user input and the power switch to enable power to the motor circuit is a power switched rated up to 6A.
