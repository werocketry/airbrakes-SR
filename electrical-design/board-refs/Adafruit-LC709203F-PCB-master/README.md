## Adafruit LC709203F LiPoly / LiIon Fuel Gauge and Battery Monitor PCB

<a href="http://www.adafruit.com/products/4712"><img src="assets/4712.jpg?raw=true" width="500px"><br/>
Click here to purchase one from the Adafruit shop</a>

PCB files for the Adafruit LC709203F LiPoly / LiIon Fuel Gauge and Battery Monitor.

Format is EagleCAD schematic and board layout
* https://www.adafruit.com/product/4712

### Description

Low cost Lithium Polymer batteries have revolutionized electronics - they're thin, they're light, they can be regulated down to 3.3V and they're easy to charge. On your phone, there's a little image of a battery cell that tells you the percentage of charge - so you know when you absolutely need to plug it in and when you can stay untethered. The Adafruit LC709203F LiPoly / LiIon Fuel Gauge and Battery Monitor does the same thing. Connect it to your Lipoly or LiIon battery and it will let you know the voltage of the cell, it does the annoying math of decoding the non-linear voltage to get you a valid percentage as well!

Since this nice chip is I2C, it works with any and all microcontroller or microcomputer boards, from the Arduino UNO up to the Raspberry Pi. And you don't have to worry about logic level, as the gauge runs with 3.3V or 5.0V power and logic equally fine.

To use, connect the single-cell battery to one of the JST 2 PH ports (either one). Then use the included JST PH jumper cable to connect to your boost converter, Feather, whatever! Use the I2C interface and our Arduino or CircuitPython/Python library code to set the pack size (this helps tune the calculation) and read the voltage and percentage whenever you like. If you connect a 10K thermistor to the THERM pin you can also use it to read the battery pack temperature - our packs do not come with a built in thermistor but many do.

To get you going fast, we spun up a custom made PCB in the STEMMA QT form factor, making it easy to interface with. The STEMMA QT connectors on either side are compatible with the SparkFun Qwiic I2C connectors. This allows you to make solderless connections between your development board and the LC709203 or to chain it with a wide range of other sensors and accessories using a compatible cable.

### License

Adafruit invests time and resources providing this open source design, please support Adafruit and open-source hardware by purchasing products from [Adafruit](https://www.adafruit.com)!

Designed by Limor Fried/Ladyada for Adafruit Industries.

Creative Commons Attribution/Share-Alike, all text above must be included in any redistribution.
See license.txt for additional details.
