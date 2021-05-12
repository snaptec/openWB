#!/usr/bin/python3
# coding=utf-8
"""
 *
 * by Markus Gießen 2021-05-12
 * adopted from Florian Wenger
 * 
 * Here we only use a SMA EnergyMeter as SmartHome Device
 * Only two values are returned: 
 * pconsume = current power consumation in Watt
 * pconsumecounter = cumulated value of power consumation in kWh
 * endless loop (until ctrl+c) displays measurement from SMA Energymeter
 *
 *  this software is released under GNU General Public License, version 2.
 *  This program is free software;
 *  you can redistribute it and/or modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; version 2 of the License.
 *  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 *  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *  See the GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along with this program;
 *  if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * 2018-12-22 Tommi2Day small enhancements
 * 2019-08-13 datenschuft run without config
 * 2020-01-04 datenschuft changes to tun with speedwiredecoder
 * 2020-01-13 Kevin Wieland changes to run with openWB
 * 2020-02-03 theHolgi added phase-wise load and power factor
 * 2021-05-12 Markus Gießen adoption for usage as Smart Home Device for power consumption
 *
 */
"""
import sys
import os
import time
import getopt
import binascii
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

#read configuration
#default values
devicenumber = str(sys.argv[1]) # SmartHomeDevice-Nummer
smaserial = sys.argv[2] # SMA EnergyMeter Serial number
# TEST
#
smaserial = '1901411846'
#
# TEST
ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
try:
    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except BaseException:
    print('Could not connect to multicast group or bind to given interface')
    sys.exit(1)

# processing received messages
while True:
    emparts = {}
    emparts=decode_speedwire(sock.recv(608))
    if smaserial is None or smaserial == 'none' or str(emparts['serial']) == smaserial:
     watt=str(int(emparts.get("pconsume")))
     wattc=str("{:.3f}".format(emparts.get('pconsumecounter')))
     answer = '{"power":' + watt + ',"powerc":' + wattc + '} '
     f = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
     f.write(answer)
     f.close
