/* [General Parameters] */
// Display all supported battery names?
Display_Battery_Names = true;



/* [Advanced] */
// The value to use for creating the model preview (lower is faster)
Preview_Quality_Value = 32;

// The value to use for creating the final model render (higher is more detailed)
Render_Quality_Value = 128;



include<../battery_lib.scad>



module Generate(index=0)
{
    battery_name = Battery_Names[index];

    supported = BatteryLib_BatteryNameIsValid(battery_name);
    if (supported)
    {
        x_offset = BatteryLib_TotalWidth(battery_name)/2;
        translate([x_offset, 0, 0])
            BatteryLib_GenerateBatteryModel(battery_name);

        if (Display_Battery_Names)
        {
            translate([x_offset, -BatteryLib_BodyLength(battery_name)/2])
            rotate([0, 0, 90])
            text(battery_name, valign="center", halign="right");
        }
    }
    
    else
    {
        echo(str ("'", battery_name, "; is not a supported battery name"));
    }
    
    if (index < len(Battery_Names) - 1)
    {
        x_offset = BatteryLib_TotalWidth(battery_name) + 10;
        translate([x_offset, 0, 0])
        Generate(index + 1);
    }
}



// Global parameters
iota = 0.001;
$fn = $preview ? Preview_Quality_Value : Render_Quality_Value;

Battery_Names = BatteryLib_Valid_Battery_Names;



// Generate the model
Generate();
    
if (Display_Battery_Names)
{
    echo(str("All supported rectangular battery names: ", BatteryLib_Valid_Rectangle_Battery_Names));
    echo(str("All supported tube battery names: ", BatteryLib_Valid_Tube_Battery_Names));
    echo(str("All supported button battery names: ", BatteryLib_Valid_Button_Battery_Names));
}
