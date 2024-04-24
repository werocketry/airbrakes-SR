# Production & Testing


## Testing

### Tube Crushing

The principal concern in meeting the requirement to survive loading at
max-g was whether the portion of the airframe containing the cutouts for
the flaps would be strong enough to transfer thrust through that section
of the rocket. The other components of the airbrakes system don't
transfer thrust along the rocket and are not of concern.

The thrust that needs to be transferred through the part of the airframe
containing the airbrakes is equal to the force required to accelerate
the mass at and above the airbrakes system with the maximum acceleration
that the rocket will experience (which occurs during its motor burn when
the airbrakes are not deployed, specifically at the moment when the
motor hits its peak thrust of 2938 N). As reported in Section 11.4.5,
the maximum acceleration is projected to be 13.58 g. The mass at and
above the airbrakes system is 11.63 kg. The total thrust transferred
through the airbrakes to the upper portion of the rocket is the mass
required to accelerate 11.63 kg at 13.58 g (133 m/s^2^), which by
Newton's Second Law is 1547 N.

A tube manufactured by WE Rocketry's aerostructures team with holes cut
into it where the airbrake flaps would extend through was compression
tested until failure in Western's Tensile Testing Laboratory to
determine if the section of body tube on the final rocket with holes cut
in it for the flaps to go through would be able to withstand the loads
it will experience at the moment of maximum thrust transfer.

![A close up of a machine Description automatically
generated](./media/image37.png)

There was a marked (though not unexpected) difference in the strength of
the tube with the cutouts compared to the tubes without the cutouts. The
tube without the cutouts could withstand a compressive force of 11.16
kN, compared to the tube with the cutouts, which could only withstand a
compressive force of 2.37 kN. The stress-strain curves for the two tubes
are shown below in Figure 33 and Figure 34.

The lower strength of the tube with the cutouts does not pose a risk to
the safety of the system. The factor of safety of 1.53 is sufficient for
several reasons:

1.  The factors that define the expected load used in the factor of
    safety calculation are well defined:

    a.  The thrust curve and mass burn rate of the motor of the rocket.
        The team is using a COTS motor and is confident that the motor
        will be within its specification, with a maximum variation of up
        to a few percent.

    b.  The mass of the components in the rocket may be less than
        currently estimated by the time the rocket is complete. However,
        the rocket's mass incredibly unlikely to change by more than a
        couple of percent between current estimates of the final mass
        and launch.

2.  The tube chosen for the testing was the first and worst-quality tube
    that the WE Rocketry aerostructures team has made this year. It was
    oversaturated with resin and had a poor surface finish with many
    bumps and ridges. The body tube chosen for the final airframe will
    be of significantly better quality, and thus stronger.

3.  The holes cut into the tube were significantly oversized compared to
    the holes that will be cut into the actual body tube that flies on
    the rocket. This was done because the final flap size had not been
    settled on at the time of the compression testing, so larger holes
    were chosen as a worst-case scenario.

### Actuation Testing

The actuation of the mechanism was tested after electromechanical
integration to assess the motion and performance. The motor was
successfully able to drive the unloaded mechanism well within the
required time taking only 1.51 seconds from top to bottom. However,
during the loaded testing discussed in the following section, the motor
could only actuate in the approximate upper and lower 30% of the lead
screw and stalled at the center point. This indicates that the force
model and subsequent motor selection should be revisited and the motor
selection reassessed. An analogous model of motor from the same
manufacturer has been ordered in the size up for future preliminary
testing.

### Loaded Testing

The system was tested with the flaps loaded to the maximum expected
loads they would see during flight. The mechanical assembly successfully
supported the maximum expected flight loads, as can be seen in Figure
35:

![No description
available.](./media/image38.jpeg)