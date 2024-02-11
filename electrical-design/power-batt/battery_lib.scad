// Battery modeling library
//
// Simplifies (for me, anyway) generating models of and for common battery types.
// https://github.com/kartchnb/battery_lib
// Share and enjoy!
//
// 27 Mar 2021 - Brad Kartchner - v1.0
//  Supports standard tube and rectangle batteries.
//
// 18 Apr 2021 - Brad Kartchner - v1.0.1
// Added support for many common button batteries and cleaned up the implementation
//
// 21 Feb 2022 - Brad Kartchner - V2.0.0
// Made one breaking change by changing BatteryLib_Diameter() to BatteryLib_TotalDiameter.
// Added other "BatteryLib_Total" functions.
// Fixed some errors that had gone unnoticed.
// Removed the dependency on my ill-concieved TableToolsLib library.

BatteryLib_Version = "2.0.0";



// Include battery parameter files
include<battery_lib_parameters/button_batteries.scad>
include<battery_lib_parameters/rectangle_batteries.scad>
include<battery_lib_parameters/tube_batteries.scad>


// These battery dimensions are based mostly on dimensions found in Wikipedia
// articles for each battery, along with some actual measurements.  They're
// accurate for the batteries I have, but may need some tweaking to account
// for variations between manufacturers.
BatteryLib_Battery_Parameters =
concat
(
    BatteryLib_Tube_Battery_Parameters,
    BatteryLib_Rectangle_Battery_Parameters,
    BatteryLib_Button_Battery_Parameters
);

BatteryLib_Valid_Battery_Names = [ for (x = BatteryLib_Battery_Parameters) x[0] ];

// This is a bit of a hack.  It would be nice if this was calculated 
// automatically, but I'm not smart enough to figure that out
BatteryLib_Valid_Battery_Types = 
[
    "button",
    "rectangle",
    "tube",
];



// Checks if a given battery name is recognized by the library
// Returns true if it is, false otherwise
function BatteryLib_BatteryNameIsValid(battery_name) =
    let
    (
        battery_name_index = search([battery_name], BatteryLib_Battery_Parameters)[0]
    )
    battery_name_index != [];



// Generate a model of a specified battery
module BatteryLib_GenerateBatteryModel(battery_name)
{
    // Tube batteries
    if (BatteryLib_Type(battery_name) == "tube")
        _BatteryLib_GenerateTubeBattery(battery_name);
    
    // Rectangle batteries
    else if (BatteryLib_Type(battery_name) == "rectangle")
        _BatteryLib_GenerateRectangleBattery(battery_name);

    // Anything else is assumed to be a button battery
    // (invalid battery types will automatically be caught and reported)
    else
        _BatteryLib_GenerateButtonBattery(battery_name);
}



// Retrieve the type of a specified battery
function BatteryLib_Type(battery_name) =
    let
    (
        battery_type = _BatteryLib_RetrieveParameter(battery_name, "type")
    )
    _BatteryLib_ReturnIfBatteryNameIsValid(battery_name, battery_type);



// Retrieve the body diameter of a specified battery
// This really only applies to tube and button batteries
// For rectangle batteries, the larger of the width and length dimensions is
// returned
function BatteryLib_BodyDiameter(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "button"
        ? _BatteryLib_RetrieveParameter(battery_name, "diameter")
        : max(BatteryLib_BodyWidth(battery_name), BatteryLib_BodyLength(battery_name));



// Retrieve the total diameter of a specified battery
// Currently, this is simply a synonym of BatteryLib_BodyDiameter()
function BatteryLib_TotalDiameter(battery_name) =
    BatteryLib_BodyDiameter(battery_name);



// Retrieve the width of a specified battery
function BatteryLib_BodyWidth(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "button" 
        ? _BatteryLib_RetrieveParameter(battery_name, "diameter")
        : _BatteryLib_RetrieveParameter(battery_name, "width");



// Retrieve the total width of a specified battery
// Currently, this is simply a synonym of BatteryLib_BodyWidth()
function BatteryLib_TotalWidth(battery_name) =
    BatteryLib_BodyWidth(battery_name);



// Retrieve the length (in the y dimension) of a specified battery
function BatteryLib_BodyLength(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "button"
        ? _BatteryLib_RetrieveParameter(battery_name, "diameter") 
        : _BatteryLib_RetrieveParameter(battery_name, "length");



// Retrieve the total length of a specified battery
// Currently, this is simply a synonym of BatteryLib_BodyLength()
function BatteryLib_TotalLength(battery_name) = 
    BatteryLib_BodyLength(battery_name);



// Retrieve the body height (in the z dimension) of a specified battery
function BatteryLib_BodyHeight(battery_name) =
        _BatteryLib_RetrieveParameter(battery_name, "height");



// Retrieve the total height of a specified battery (including the anode and
// cathode)
function BatteryLib_TotalHeight(battery_name) =
    BatteryLib_Type(battery_name) == "tube" 
        ? BatteryLib_BodyHeight(battery_name) + BatteryLib_AnodeHeight(battery_name) + BatteryLib_CathodeHeight(battery_name) 
        : BatteryLib_Type(battery_name) == "rectangle" 
            ? BatteryLib_BodyHeight(battery_name) + max(BatteryLib_AnodeHeight(battery_name), BatteryLib_CathodeHeight(battery_name))
            : BatteryLib_BodyHeight(battery_name);



// Retrieve the diameter of the cathode of a specified battery
function BatteryLib_CathodeDiameter(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "rectangle" 
        ? _BatteryLib_RetrieveParameter(battery_name, "cathode diameter") 
        : _BatteryLib_RetrieveParameter(battery_name, "diameter");



// Retrieve the height of the cathode of a specified battery
function BatteryLib_CathodeHeight(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "rectangle" 
        ? _BatteryLib_RetrieveParameter(battery_name, "cathode height") 
        : 0;



// Retrieve the diameter of the anode of a specified battery
function BatteryLib_AnodeDiameter(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "rectangle" 
        ? _BatteryLib_RetrieveParameter(battery_name, "anode diameter") 
        : _BatteryLib_RetrieveParameter(battery_name, "diameter");



// Retrieve the height of the anode of a specified battery
function BatteryLib_AnodeHeight(battery_name) =
    BatteryLib_Type(battery_name) == "tube" || BatteryLib_Type(battery_name) == "rectangle" 
        ? _BatteryLib_RetrieveParameter(battery_name, "anode height") 
        : 0;



// Retrieve the horizontal distance between the anode and cathode of a
// specified battery
// This really only applies to rectangle (e.g. 9V) batteries
// For tube and button batteries, this just returns the body height as a sort of sane
// alternative
function BatteryLib_TerminalDistance(battery_name) =
    BatteryLib_Type(battery_name) == "rectangle"
        ? _BatteryLib_RetrieveParameter(battery_name, "terminal distance")
        : BatteryLib_BodyHeight(battery_name);



// Retrieve the dimensions of the dimensions of a cube completely enveloping
// a specified battery [x, y, z]
function BatteryLib_Envelope(battery_name) =
    [BatteryLib_TotalWidth(battery_name), BatteryLib_TotalLength(battery_name), BatteryLib_TotalHeight(battery_name)];






//-----------------------------------------------------------------------------
// "Private" functions



// Retrieve the parameters for a specified battery
function _BatteryLib_RetrieveParameter(battery_name, key) =
    let
    (
        battery_specific_table_index = search([battery_name], BatteryLib_Battery_Parameters) [0],
        battery_specific_table = BatteryLib_Battery_Parameters [battery_specific_table_index] [1],
        parameter_index = search([key], battery_specific_table) [0],
        parameter = battery_specific_table [parameter_index] [1]
    )
    _BatteryLib_ReturnIfBatteryNameIsValid(battery_name, parameter);



// Return the specified value if the battery name is valid
function _BatteryLib_ReturnIfBatteryNameIsValid(battery_name, value) =
    BatteryLib_BatteryNameIsValid(battery_name)
    ? value
    : assert(false, str("Battery name \"", battery_name, "\" is not currently supported by battery_lib"));