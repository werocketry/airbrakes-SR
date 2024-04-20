use <18650_Holder.scad>;
use <battery_lib.scad>

translate([0, 0, 10]) {
// Generate a model of a tube battery 
translate([22, 22, 0]) 
color("DodgerBlue") BatteryLib_GenerateBatteryModel("18650");


translate([0, 44, 6]) 
rotate([180, 0, 0]) 
batteryHolderConfig(cells_x = 1, cells_y = 1, negative = 0, cable_tie = 1);

translate([0, 0, 59]) 
batteryHolderConfig(cells_x = 1, cells_y = 1, negative = 0, cable_tie = 1);
}