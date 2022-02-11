#!/usr/bin/python3

#####
#
# File: dac.py
#
# Copyright 2018 Kevin Wieland, David Meder-Marouelli
#
#  This file is part of openWB.
#
#     openWB is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     openWB is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with openWB.  If not, see <https://www.gnu.org/licenses/>.
#
#####

# Setting the output voltage of the MCP4725 DAC.
# Read first value passed as the integer for DAC.
import sys
# Import the MCP4725 module.
import Adafruit_MCP4725

# translation table current-to-voltage
voltage = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 790,
    7: 908,
    8: 1038,
    9: 1168,
    10: 1298,
    11: 1427,
    12: 1557,
    13: 1687,
    14: 1814,
    15: 1947,
    16: 2077,
    17: 2206,
    18: 2336,
    19: 2466,
    20: 2596,
    21: 2726,
    22: 2855,
    23: 2985,
    24: 3115,
    25: 3245,
    26: 3375,
    27: 3505,
    28: 3634,
    29: 3764,
    30: 3894,
    31: 4024,
    32: 4096
}

# TODO: How precise need the values to be? Maybe the table could be replaced by volt=current*130

# Create a DAC instance.

# dac = Adafruit_MCP4725.MCP4725()
address = int(sys.argv[2], 16)

# Note you can change the I2C address from its default (0x62), and/or the I2C
# bus by passing in these optional parameters:
dac = Adafruit_MCP4725.MCP4725(address, busnum=1)

volt = voltage[int(sys.argv[1])]
dac.set_voltage(volt, True)
