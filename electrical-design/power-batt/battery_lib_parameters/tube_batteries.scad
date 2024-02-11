BATTERYLIB_TYPE_TUBE = "tube";



// Tube battery dimensions
//
// |<-->| Body Diameter
//  >||<- Anode Diameter
//  _--_  === Anode Height
// |    |  ^
// |    |  |
// |    | Body Height
// |    |  |
// |____|  V
//   --   === Cathode Height
//  >||<- Cathode Diameter


BatteryLib_Tube_Battery_Parameters = 
[
    // Based on my own measurements
    [
        "18650",
        [
            ["type", "tube"],
            ["diameter", 18.30],
            ["height", 64.80],
            ["cathode diameter", 13.30],
            ["cathode height", 0.00],
            ["anode diameter", 10.50],
            ["anode height", 0.00],
        ],
    ],

    // Measurements provided by "rowdypants" on Thingiverse
    [
        "26650",
        [
            ["type", "tube"],
            ["diameter", 26.50],
            ["height", 66.00],
            ["cathode diameter", 20.00],
            ["cathode height", 1.00],
            ["anode diameter", 13.00],
            ["anode height", 2.00],
        ],
    ],

    [
        "AAAA",
        [
            ["type", "tube"],
            ["diameter", 8.30], // Official value from Wikipedia (https://en.wikipedia.org/wiki/AAAA_battery)
            ["height", 40.00],
            ["cathode diameter", 4.91],
            ["cathode height", 0.50],
            ["anode diameter", 3.37],
            ["anode height", 1.77],
        ],
    ],

    [
        "AAA",
        [
            ["type", "tube"],
            ["diameter", 10.50],
            ["height", 43.50],
            ["cathode diameter", 6.30],
            ["cathode height", 0.40],
            ["anode diameter", 3.80],
            ["anode height", 0.80],
        ],
    ],

    [
        "AA",
        [
            ["type", "tube"],
            ["diameter", 14.50],
            ["height", 49.50],
            ["cathode diameter", 9.10],
            ["cathode height", 0.40],
            ["anode diameter", 5.50],
            ["anode height", 1.00],
        ],
    ],

    [
        "C",
        [
            ["type", "tube"],
            ["diameter", 26.20],
            ["height", 47.60],
            ["cathode diameter", 18.00],
            ["cathode height", 0.40],
            ["anode diameter", 6.00],
            ["anode height", 2.00],
        ],
    ],

    [
        // Dimensions courtesy of "enriqueeeee" on Thingiverse
        "CR123A",
        [
            ["type", "tube"],
            ["diameter", 16.71],
            ["height", 33.30],
            ["cathode diameter", 16.71],
            ["cathode height", 0.00],
            ["anode diameter", 6.21],
            ["anode height", 0.50],
        ],
    ],

    [
        // Dimensions courtesy of "majorsl" on Thingiverse
        "CR2",
        [
            ["type", "tube"],
            ["diameter", 15.10],
            ["height", 26.70],
            ["cathode diameter", 15.10],
            ["cathode height", 0.00],
            ["anode diameter", 6.30],
            ["anode height", 0.90],
        ],
    ],

    [
        "D",
        [
            ["type", "tube"],
            ["diameter", 34.20],
            ["height", 59.60],
            ["cathode diameter", 18.00],
            ["cathode height", 0.40],
            ["anode diameter", 9.50],
            ["anode height", 1.50],
        ],
    ],

    [
        // Dimensions courtesy of "enriqueeeee" on Thingiverse
        "ER14250V",
        [
            ["type", "tube"],
            ["diameter", 14.32],
            ["height", 24.10],
            ["cathode diameter", 14.32],
            ["cathode height", 0.00],
            ["anode diameter", 4.28],
            ["anode height", 0.77],
        ],
    ],
];



BatteryLib_Valid_Tube_Battery_Names = [ for (x = BatteryLib_Tube_Battery_Parameters) x[0] ];



//-----------------------------------------------------------------------------
// "Private" modules



// Generate a specified tube style battery
module _BatteryLib_GenerateTubeBattery(battery_name)
{
    if (BatteryLib_Type(battery_name) != BATTERYLIB_TYPE_TUBE)
        assert(false, str(battery_name, " is not a tube battery"));

    body_diameter = BatteryLib_BodyDiameter(battery_name);
    body_height = BatteryLib_BodyHeight(battery_name);
    cathode_diameter = BatteryLib_CathodeDiameter(battery_name);
    cathode_height = BatteryLib_CathodeHeight(battery_name);
    anode_diameter = BatteryLib_AnodeDiameter(battery_name);
    anode_height = BatteryLib_AnodeHeight(battery_name);

    translate([0, 0, cathode_height])
    {
        cylinder(d=body_diameter, body_height);
        translate([0, 0, body_height])
            cylinder(d=anode_diameter, anode_height);
        translate([0, 0, -cathode_height])
            cylinder(d=cathode_diameter, cathode_height);
    }
}
