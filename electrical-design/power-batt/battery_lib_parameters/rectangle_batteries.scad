// Rectangular battery dimensions
// ...well, really, just 9v batteries...
//
// Cathode Diameter
//  |
//  >||< >||<- Anode Diameter
//  _--___--_ ==== Terminal Height
// |         |  ^
// |         |  |
// |         | Body Height
// |         |  |
// |_________|  V
// |<------->|<- Body Width
//
//  __--__
// |      |
// |      |
// |      |
// |      |
// |______|
// |<---->|<- Body Length



BatteryLib_Rectangle_Battery_Parameters =
[
    [
        "9V",
        [
            ["type", "rectangle"],
            ["width", 26.50],
            ["length", 17.50],
            ["height", 44.90],
            ["cathode diameter", 8.52],
            ["cathode height", 2.10],
            ["anode diameter", 5.75],
            ["anode height", 2.10],
            ["terminal distance", 12.70],
        ],
    ],
];



BatteryLib_Valid_Rectangle_Battery_Names = [ for (x = BatteryLib_Rectangle_Battery_Parameters) x[0] ];



//-----------------------------------------------------------------------------
// "Private" modules



// Generate a specified rectangle style battery
module _BatteryLib_GenerateRectangleBattery(battery_name)
{
    if (BatteryLib_Type(battery_name) != "rectangle")
        assert(false, str(battery_name, " is not a rectangle battery"));

    body_width = BatteryLib_BodyWidth(battery_name);
    body_length = BatteryLib_BodyLength(battery_name);
    body_height = BatteryLib_BodyHeight(battery_name);
    cathode_diameter = BatteryLib_CathodeDiameter(battery_name);
    cathode_height = BatteryLib_CathodeHeight(battery_name);
    anode_diameter = BatteryLib_AnodeDiameter(battery_name);
    anode_height = BatteryLib_AnodeHeight(battery_name);
    terminal_distance = BatteryLib_TerminalDistance(battery_name);

    translate([-body_width/2, -body_length/2, 0])
        cube([body_width, body_length, body_height]);
    translate([-terminal_distance/2, 0, body_height])
        cylinder(d=anode_diameter, anode_height);
    translate([terminal_distance/2, 0, body_height])
        cylinder(d=cathode_diameter, cathode_height);
}
