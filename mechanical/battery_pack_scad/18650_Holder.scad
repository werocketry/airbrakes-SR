// Improved, modular version of the 18650 battery holder script
// Based on https://www.thingiverse.com/thing:3026658

// Constants
diameter = 18.8; // Diameter of 18650 cell
height = 6;      // Height of holder
tab = 1.4;       // Tab height
tolerance = 0.5; // Tolerance to help fit

// Main configuration module
module batteryHolderConfig(cells_x = 2, cells_y = 2, negative = 0, cable_tie = 1) {
    // Generate the grid of cells and connectors
    generateCells(cells_x, cells_y, negative, cable_tie, diameter, height, tab);
    generateGaps(cells_x, cells_y, cable_tie, height);
    generateConnectors(cells_x, cells_y, height, tolerance, cable_tie);
}

// Generates the grid of cells
module generateCells(cells_x, cells_y, negative, cable_tie, diameter, height, tab) {
    for ( y= [1:1:cells_y]) for ( x= [ 1:1:cells_x]) 
        translate ([x*22,y*22,0]) cell(diameter, height, tab, negative);
}

// Fills gaps between cells
module generateGaps(cells_x, cells_y, cable_tie, height) {
    for ( x= [1:1:cells_x]) for ( y= [1:1:cells_y-1])    
        translate([22*x- (cable_tie ==1 ? 7: 12),22*y+10,0]) cube([cable_tie ==1 ? 14 : 22,2,height]);

    for ( x= [1:1:cells_x-1]) for ( y= [1:1:cells_y])    
        translate([22*x+12,22*y-(cable_tie ==1 ? 7: 10),0]) rotate([0,0,90]) cube([cable_tie ==1 ? 14: 22,2,height]);
}

// Adds male and female connectors
module generateConnectors(cells_x, cells_y, height, tolerance, cable_tie) {
    for ( x= [1:1:cells_x]) translate([22*x,22*cells_y+11.4,0]) trapezoid(13, height);
    for ( y= [1:1:cells_y]) translate([22*cells_x+11.4,22*y,0]) rotate([0,0,-90]) trapezoid(13, height);
    
    for ( x= [1:1:cells_x]) difference() {
        translate([22*x,11,height/2])cube([20,2,height],center=true);
        translate([22*x,10.8,0]) trapezoid(13+tolerance, height);
    }
    for ( y= [1:1:cells_y]) difference() {
        rotate([0,0,90]) translate([22*y,-11,height/2])cube([20,2,height],center=true);
        rotate([0,0,90]) translate([22*y,-10.8,0]) rotate([0,0,180]) trapezoid(13+tolerance, height);
    }
}

// Module for trapezoid (connectors)
module trapezoid(length, height) {
    hull() { 
        translate([-length/2, 0, 0]) rotate([0,0,30]) cylinder (r = 2, h=height,  $fn=3); 
        translate([length/2, 0, 0]) rotate([0,0,30]) cylinder (r = 2, h=height,  $fn=3);
    }
}

// Module to create a single cell
module cell(diameter, height, tab, negative) {
    difference() {
        union() {
            translate([0,0,height/2]) cube([20,20,height],center = true);
            if (!negative) for (rotation =[45:90:325]) rotate([0,0,rotation])  
                translate([0,9,0]) hull(){     
                    translate([1,0,height]) cylinder(r=2, h=tab, $fn=16);
                    translate([1,1,height]) cylinder(r=2, h=tab, $fn=16);
                    translate([0,1,height]) cylinder(r=2, h=tab, $fn=16);
                    translate([0,0,height]) cylinder(r=2, h=tab, $fn=16);
                } 
        }
        rotate([0,0,-0.1]) cylinder(r=diameter/2 + tolerance/2, h= height+ 0.2, $fn=64); // Hole for cell
    }
}

// Example usage:
batteryHolderConfig(cells_x = 3, cells_y = 2, negative = 1, cable_tie = 1);
