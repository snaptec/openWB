#!/usr/bin/python3
# coding=utf-8

# by Markus Gießen 2021-09-30
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
# 2021-09-01 Markus Gießen adoption for usage as Smart Home Device for power consumption


import sys
import os
import datetime
import time
import json
import signal
import sys
import socket
import struct
from speedwiredecoder import *

# clean exit
def abortprogram(signal,frame):
    # Housekeeping -> nothing to cleanup
    print('STRG + C = end program')
    sys.exit(0)

# abort-signal
signal.signal(signal.SIGINT, abortprogram)

# read configuration
# default values
devicenumber = str(sys.argv[1]) # SmartHomeDevice-Nummer
smaserial = sys.argv[2] # SMA EnergyMeter Serial number
secondssincelastmetering = sys.argv[3] # Seconds since last metering, useful for handling with more than one EnergyMeter

ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522

returnfile = '/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber)
debugfile = open('/var/www/html/openWB/ramdisk/smaem.log','a',newline='\r\n')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
try:
    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except BaseException:
    print('Module SMAEM: Could not connect to multicast group or bind to given interface')
    sys.exit(1)

if os.path.isfile(returnfile):
	lastmodificationtime=os.path.getmtime(returnfile)
else:
	lastmodificationtime=time.time()

# Processing received messages
# The SMA EnergyMeter does not send any data package if there is no Power Consumption / no data to send
# Therefore we have to do a special processing for this scenario.
# We also have to take care if there are more than one EnergyMeter in the network sending, that's why we check the modification time in scenario 2.
# Without this check we would generate a ret-file everytime we receive data from a not desired EnergyMeter.
emparts={}
emparts=decode_speedwire(sock.recv(608))

# debugfile.write('Current SMA serial number:#' + str(emparts['serial']) + '# - watt:#' + str(int(emparts.get("pconsume"))) + '# - wattc:#' + str("{:.3f}".format(int(emparts.get('pconsumecounter')*1000))) + '#\n')

if smaserial is None or smaserial == 'none' or str(emparts['serial']) == smaserial: # Scenario 1: Our EnergyMeter is sending, so we put the current values in our output variables
 watt=str(int(emparts.get("pconsume")))
 wattc=str("{:.3f}".format(int(emparts.get('pconsumecounter')*1000)))
 debugfile.write(str(datetime.datetime.now()) + ': 1 - Our SMA EM ' + smaserial + ' is sending, everything fine. watt: #' + watt + '# - wattc: #' + wattc + '#\n')
elif (os.path.isfile(returnfile)) and ((time.time()-lastmodificationtime) >= int(secondssincelastmetering)): # Scenario 2: Our EnergyMeter is not sending but we have a returnfile which is older than n seconds (parameter secondssincelastmetering)
 # We have a ret-file which is older than n seconds so we create a "fake" ret-file.
 # We set "0" as current Power Consume (pconsume) and (from the existing ret-file) the last value for the Power Consume Counter (pconsumecounter)
 watt='0'
 ret=open(returnfile, 'r')
 lastvalues = ret.read()
 ret.close()
 wattc = lastvalues[int(lastvalues.rfind('powerc')) + 9:lastvalues.find('}')]
 debugfile.write(str(datetime.datetime.now()) + ': 2 - We create a fake ret-file. lastvalues: #' + lastvalues + '# - int-lastvalues.rfind-powerc: #' + str((lastvalues.rfind('powerc'))) + '#\n')

elif (os.path.isfile(returnfile)) and ((time.time()-lastmodificationtime) < int(secondssincelastmetering)): # Scenario 3: Our EnergyMeter is not sending but we have a returnfile which is younger than n seconds (parameter secondssincelastmetering)
 # We have a ret-file which is younger than n seconds. We do nothing as the existing ret-file is good enough.
 debugfile.write(str(datetime.datetime.now()) + ': 3 - The existing ret-file is fine enough. time.time(): #' + str(time.time()) + '# - lastmodificationtime: #' + str(lastmodificationtime) + '# - secondssincelastmetering: #' + str(secondssincelastmetering) + '#\n')
 sys.exit("Module SMAEM: No data received and no historical data which is older than " + str(secondssincelastmetering) + " seconds.")
else:
 # Our EnergyMeter is not sending right now and it didn't send any data since boottime
 # In this case we do nothing and we don't create a "fake" returnfile
 # This will cause error messages in /var/www/html/openWB/ramdisk/smarthome.log: 
 # Module SMAEM: No data received and no historical data since boottime
 # Leistungsmessung smaem [...] Fehlermeldung: [Errno 2] No such file or directory: '/var/www/html/openWB/ramdisk/smarthome_device_ret1'W
 sys.exit(str(datetime.datetime.now()) + ": Module SMAEM: No data received and no historical data since boottime")

# general output section

answer = '{"power":' + watt + ',"powerc":' + wattc + '}'
f = open(returnfile, 'w')
json.dump(answer,f)
f.close()
debugfile.close()