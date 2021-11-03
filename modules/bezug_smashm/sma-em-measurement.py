#!/usr/bin/env python3
# coding=utf-8
"""
 *
 * by Wenger Florian 2015-09-02
 * wenger@unifox.at
 *
 * endless loop (until ctrl+c) displays measurement from SMA Energymeter
 *
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
 *
 */
"""

import signal
import sys
#import smaem
import socket
import struct
from speedwiredecoder import decode_speedwire

# clean exit
def abortprogram(signal,frame):
    # Housekeeping -> nothing to cleanup
    print('STRG + C = end program')
    sys.exit(0)

def writeToFile(filename, content):
    """Write content to file"""
    with open(filename, 'w') as f:
        f.write(str(content))

# abort-signal
signal.signal(signal.SIGINT, abortprogram)


#read configuration
#parser = ConfigParser()
#default values
smaserials = sys.argv[1] if len(sys.argv) > 1 else None
ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522

basepath = '/var/www/html/openWB/ramdisk/'
#                filename:  channel
mappingdict      = { 'evuhz':   'frequency' }
phasemappingdict = { 'bezuga%i': { 'from': 'i%i', 'sign': True },
                     'evuv%i':   { 'from': 'u%i'   },
                     'evupf%i':  { 'from': 'cosphi%i' }
                   }
#try:
#    smaemserials=parser.get('SMA-EM', 'serials')
#    ipbind=parser.get('DAEMON', 'ipbind')
#    MCAST_GRP = parser.get('DAEMON', 'mcastgrp')
#    MCAST_PORT = int(parser.get('DAEMON', 'mcastport'))
#except:
#    print('Cannot find config /etc/smaemd/config... using defaults')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
try:
    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except BaseException:
    print('could not connect to mulicast group or bind to given interface')
    sys.exit(1)
# processing received messages
while True:
    emparts = {}
    emparts=decode_speedwire(sock.recv(608))
    # Output...
    # don't know what P,Q and S means:
    # http://en.wikipedia.org/wiki/AC_power or http://de.wikipedia.org/wiki/Scheinleistung
    # thd = Total_Harmonic_Distortion http://de.wikipedia.org/wiki/Total_Harmonic_Distortion
    # cos phi is always positive, no matter what quadrant
    positive = [ 1,1,1,1 ]
    if smaserials is None or smaserials == 'none' or str(emparts['serial']) == smaserials:
        # Special treatment for positive / negative power
        
        try:
            watt=int(emparts['pconsume'])
            if watt < 5:
                watt=-int(emparts['psupply'])
                positive[0] = -1
            writeToFile(basepath + 'wattbezug', watt)
        except:
            pass
        try:
            if ( emparts['psupplycounter'] < 900000 ):
                writeToFile(basepath + 'einspeisungkwh', emparts['psupplycounter'] * 1000)
        except:
            pass
        try:
            writeToFile(basepath + 'bezugkwh', emparts['pconsumecounter'] * 1000)
        except:
            pass
        for phase in [1,2,3]:
            power = int(emparts['p%iconsume' % phase])
            if power < 5:
                power = -int(emparts['p%isupply' % phase])
                positive[phase] = -1
            writeToFile(basepath + 'bezugw%i' % phase, power)
        for filename, mapping in phasemappingdict.items():
            for phase in [1,2,3]:
                if mapping['from'] % phase in emparts:
                    value = emparts[mapping['from'] % phase]
                    if 'sign' in mapping and mapping['sign']:
                       value *= positive[phase]
                    writeToFile(basepath + filename % phase, value)
        for filename, key in mappingdict.items():
            if key in emparts:
                writeToFile(basepath + filename, emparts[key])
        sys.exit(0)
