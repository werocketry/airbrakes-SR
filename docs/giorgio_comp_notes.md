## Rocketry Advice from Canterbury and Maryland

### Canterbury's Advice:
- **Static Ports Placement:** Do not position the rocket's static ports directly above the airbrakes.
- **Deployment System:** Utilize a single motor to drive all flaps (either 3 or 4). Partial deployment, such as only 2 flaps deploying, can turn a rocket into a ballistic missile.
- **Control System:** PID (Proportional-Integral-Derivative) control works well for airbrake systems; there's no need for more complex solutions.
- **Design For Assembly (DFA):** Consider ease of assembly in the design process.

### Maryland's Advice:
- **Flap Design:** Opting for flaps is safer because, in case of failure, they tend to fail inwards, minimizing risk.
- **System Separation:** It's advisable to keep the airbrake system entirely separate from the avionics bay for simplicity. Consider equipping it with its own barometer and accelerometer.
- **Sensor Readings:** Barometer readings can be affected by flap deployment. This can be corrected through characterization from wind tunnel testing, which tends to be very effective. Alternatively, a well-developed CFD model could also provide accurate predictions.
- **Simulation Considerations:** Include the deployment time of airbrakes in flight simulations, and consider how angle of attack might affect induced drag and vertical velocity.

### Terrapin Rocket Team's Rockets at Spaceport America Cup:
- **2022**: [Terrapin Rocket Team - Spaceport America Cup 2022](https://www.terprockets.com/spaceport-america-cup-2022)
- **2023**: [Terrapin Rocket Team - Spaceport America Cup 2023](https://www.terprockets.com/spaceport-america-cup-2023)

### Common Parts and Material Choices:
- **Actuators:** Linear actuators or stepper motors are commonly used.
- **Materials for Blades:** Blades are often made from aluminum or carbon forged materials.
- **Example Specification:** For smaller rockets, such as those with a 3-inch diameter airframe, an LA-T8 6V 1mm/s 50mm 128N linear actuator is suitable.
