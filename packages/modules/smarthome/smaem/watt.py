#!/usr/bin/python3
# coding=utf-8

# by Markus Giessen 2021-09-30
# adopted from Florian Wenger
#
# Here we only use a SMA EnergyMeter as SmartHome Device
# Only two values are returned:
# pconsume = current power consumation in Watt
# pconsumecounter = cumulated value of power consumation in kWh
# endless loop (until ctrl+c) displays measurement from SMA Energymeter
#
#  this software is released under GNU General Public License, version 2.
#  This program is free software;
#  you can redistribute it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program;
#  if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# 2018-12-22 Tommi2Day small enhancements
# 2019-08-13 datenschuft run without config
# 2020-01-04 datenschuft changes to tun with speedwiredecoder
# 2020-01-13 Kevin Wieland changes to run with openWB
# 2020-02-03 theHolgi added phase-wise load and power factor
# 2021-09-01 Markus Giessen adoption for usage as Smart Home Device for energy metering
# 2021-12-25 Markus Giessen adoption of PR 1845 due to SMA protocol change

import sys
import os
import datetime
import time
import json
import signal
import socket
import struct
from speedwiredecoder import decode_speedwire

# clean exit


def abortprogram(signal, frame):
    # Housekeeping -> nothing to cleanup
    print('STRG + C = end program')
    sys.exit(0)


# abort-signal
signal.signal(signal.SIGINT, abortprogram)

# read configuration
devicenumber = str(sys.argv[1])  # SmartHomeDevice-Nummer
smaserial = sys.argv[2]  # SMA EnergyMeter Serial number
# Seconds since last metering, useful for handling with more than one EnergyMeter
secondssincelastmetering = int(sys.argv[3])

ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522

returnfile = '/var/www/html/openWB/ramdisk/smarthome_device_ret' + \
    str(devicenumber)  # Return file (.ret) for energy metering
timefile = '/var/www/html/openWB/ramdisk/smarthome_device_ret' + \
    str(devicenumber) + '_time'  # Dummy file needed for timestamp of last metering
# Logfile for additional output beside of the smarthome.log
debugfile = open('/var/www/html/openWB/ramdisk/smaem.log', 'a', newline='\r\n')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
try:
    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except BaseException:
    print('Module SMAEM: Could not connect to multicast group or bind to given interface')
    sys.exit(1)

if os.path.isfile(timefile):
    lastmodificationtime = round(os.path.getmtime(timefile), 0)
    # debugfile.write('We took the time of the returnfile:' + datetime.fromtimestamp(lastmodificationtime) + '\n')
else:
    lastmodificationtime = round(time.time(), 0)
    # debugfile.write('We took the current time\n')

# Processing received messages
# The SMA EnergyMeter does not send any data package if there is no Power Consumption / no data to send
# Therefore we have to do a special processing for this scenario.
# We also have to take care if there are more than one EnergyMeter in the network sending, that's why we
# check the modification time in scenario 2.
# Without this check we would generate a ret-file everytime we receive data from a not desired EnergyMeter.
emparts = {}
sock_data = sock.recv(608)

# Ignore data package if the length is smaller 18 - this should not happen. If length is smaller 18, the
# following check for Protocol ID can't work
if len(sock_data) < 18:
    sys.exit("Module SMAEM: Invalid data package received. The length of the received data package is smaller than 18 "
             + "Byte. This should not happen.")

# Ignore data package if the SMA Protocol ID is not 0x6069 - adoption of PR 1845
if sock_data[16:18] != b'\x60\x69':
    sys.exit("Module SMAEM: Invalid data package received. No need to worry, this is a normal situation if a SMA " +
             "HomeManager (2) is sending in the network.")

emparts = decode_speedwire(sock_data)
debugfile.write(str(datetime.datetime.now()) + ': smaserial: #' + str(smaserial) + '# - Current SMA serial number:#' +
                str(emparts['serial']) + '# - watt:#' + str(int(emparts.get("pconsume"))) + '# - wattc:#' +
                str("{:.3f}".format(int(emparts.get('pconsumecounter')*1000))) + '#\n')

# Remember: We assume that beside of our EnergyMeter there are more SMA devices present (like HomeManager 2.0 or other
# EnergyMeter) - so must not accept any data or smaserial = None
if str(emparts['serial']) == str(smaserial):  # Scenario 1: Our EnergyMeter is sending, so we put the current values in
    # our output variables
    watt = str(int(emparts.get("pconsume")))
    wattc = str("{:.3f}".format(int(emparts.get('pconsumecounter')*1000)))
    debugfile.write(str(datetime.datetime.now()) + ': 1 - Our SMA EM ' + str(smaserial) +
                    ' is sending, everything fine. watt: #' + str(watt) + '# - wattc: #' + str(wattc) + '#\n')
# Scenario 2: Our EnergyMeter is not sending but we have a returnfile which is older than n seconds (parameter
# secondssincelastmetering)
elif ((os.path.isfile(returnfile)) and
      (int((round(time.time(), 0)-lastmodificationtime)) >= int(secondssincelastmetering))):
    # We have a ret-file which is older than n seconds so we create a "fake" ret-file.
    # We set "0" as current Power Consume (pconsume) and (from the existing ret-file) the last value for the Power
    # Consume Counter (pconsumecounter)
    watt = '0'
    ret = open(returnfile, 'r')
    lastvalues = ret.read()
    ret.close()
    timesincelastmetering = int(round(time.time(), 0)-lastmodificationtime)
    wattc = lastvalues[int(lastvalues.rfind('powerc')) + 9:lastvalues.find('}')]
    debugfile.write(str(datetime.datetime.now()) + ': 2 - Debug: time.time(): #' + str(round(time.time(), 0)) +
                    '# - lastmodificationtime: #' + str(lastmodificationtime) +
                    '# - timesincelastmetering: #' + str(timesincelastmetering) +
                    '# - int(secondssincelastmetering): #' + str(int(secondssincelastmetering)) + '#\n')
    debugfile.write(str(datetime.datetime.now()) + ': 2 - We create a fake ret-file. watt: #' + str(watt) +
                    '# - wattc: #' + str(
        wattc) + '# - lastvalues: #' + lastvalues + '# - int-lastvalues.rfind-powerc: #' +
        str((lastvalues.rfind('powerc'))) + '#\n')

# Scenario 3: Our EnergyMeter is not sending but we have a returnfile which is younger than n seconds
# (parameter secondssincelastmetering)
elif ((os.path.isfile(returnfile)) and
        (int((round(time.time(), 0)-lastmodificationtime)) < int(secondssincelastmetering))):
    # We have a ret-file which is younger than n seconds. We do nothing as the existing ret-file is good enough.
    debugfile.write(str(datetime.datetime.now()) +
                    ': 3 - The existing ret-file is fine enough. round(time.time(),0): #' + str(round(time.time(), 0))
                    + '# - lastmodificationtime: #' + str(lastmodificationtime) + '# - secondssincelastmetering: #'
                    + str(secondssincelastmetering) + '#\n')
    sys.exit("Module SMAEM: No data received but we have historical data which is younger than " +
             str(secondssincelastmetering) + " seconds.")
else:
    # Our EnergyMeter is not sending right now and it didn't send any data since boottime
    # In this case we do nothing and we don't create a "fake" returnfile (as we don't know the value for wattc)
    # This will cause error messages in /var/www/html/openWB/ramdisk/smarthome.log:
    # This will cause error messages in /var/www/html/openWB/ramdisk/smarthome.log:
    # This will cause error messages in /var/www/html/openWB/ramdisk/smarthome.log:
    # Module SMAEM: No data received and no historical data since boottime
    # Leistungsmessung smaem [...] Fehlermeldung: [Errno 2] No such file or directory:
    # '/var/www/html/openWB/ramdisk/smarthome_device_ret1'
    debugfile.write(str(datetime.datetime.now()) + ': 4 - No data received and no historical data since boottime\n')
    sys.exit(str(datetime.datetime.now()) + ": Module SMAEM: No data received and no historical data since boottime")

# General output section

answer = '{"power":' + watt + ',"powerc":' + wattc + '}'
f = open(returnfile, 'w')
json.dump(answer, f)
f.close()

t = open(timefile, 'w')
t.write(str(datetime.datetime.now()) +
        ': File is created by Smarthome module SMAEM for validating the timestamp of the last return-file creation.')
t.close()

debugfile.write(str(datetime.datetime.now()) + ': 99 - Output answer: #' + answer + '#\n')
debugfile.close()
