# Setting the output voltage of the MCP4725 DAC.
# Read first value passed as the integer for DAC.
import time
import sys
# Import the MCP4725 module.
import Adafruit_MCP4725
# Create a DAC instance.
dac = Adafruit_MCP4725.MCP4725()

# Note you can change the I2C address from its default (0x62), and/or the I2C
# bus by passing in these optional parameters:
#dac = Adafruit_MCP4725.MCP4725(address=0x49, busnum=1)
dac.set_voltage((sys.argv[1]), True)
