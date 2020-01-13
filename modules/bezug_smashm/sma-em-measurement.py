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
 *
 */
"""

import signal
import sys
#import smaem
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
#parser = ConfigParser()
#default values
smaserials = ""
ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522
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
emparts = {}
emparts=decode_speedwire(sock.recv(608))
# Output...
# don't know what P,Q and S means:
# http://en.wikipedia.org/wiki/AC_power or http://de.wikipedia.org/wiki/Scheinleistung
# thd = Total_Harmonic_Distortion http://de.wikipedia.org/wiki/Total_Harmonic_Distortion
# cos phi is always positive, no matter what quadrant
ikwh=emparts['pconsumecounter']*1000
ekwh=emparts['psupplycounter']*1000

bezuga1=emparts['i1']
bezuga2=emparts['i2']
bezuga3=emparts['i3']
bezugv1=emparts['u1']
bezugv2=emparts['u2']
bezugv3=emparts['u3']
iw=emparts['pconsume']
ew=emparts['psupply']
if ( iw > 5 ):
    watt=ew*-1
else:
    watt=iw
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(bezugv1))
f.close()
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(bezugv2))
f.close()
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(bezugv3))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(bezuga1))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(bezuga2))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(bezuga3))
f.close()
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(watt))
f.close()
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(ekwh))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(ikwh))
f.close()



#print ('SMA-EM Serial:{}'.format(emparts['serial']))
#print ('----sum----')
#print ('P: consume:{}W {}kWh supply:{}W {}kWh'.format(emparts['pconsume'],emparts['pconsumecounter'],emparts['psupply'],emparts['psupplycounter']))
#print ('S: consume:{}VA {}kVAh supply:{}VA {}VAh'.format(emparts['sconsume'],emparts['sconsumecounter'],emparts['ssupply'],emparts['ssupplycounter']))
#print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['qconsume'],emparts['qconsumecounter'],emparts['qsupply'],emparts['qsupplycounter']))
#print ('cos phi:{}°'.format(emparts['cosphi']))
#if emparts['speedwire-version']=="2.3.4.R|020304":
#    print ('frequency:{}Hz'.format(emparts['frequency']))
#print ('----L1----')
#print ('P: consume:{}W {}kWh supply:{}W {}kWh'.format(emparts['p1consume'],emparts['p1consumecounter'],emparts['p1supply'],emparts['p1supplycounter']))
#print ('S: consume:{}VA {}kVAh supply:{}VA {}kVAh'.format(emparts['s1consume'],emparts['s1consumecounter'],emparts['s1supply'],emparts['s1supplycounter']))
#print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q1consume'],emparts['q1consumecounter'],emparts['q1supply'],emparts['q1supplycounter']))
#print ('U: {}V I:{}A cos phi:{}°'.format(emparts['u1'],emparts['i1'],emparts['cosphi1']))
#print ('----L2----')
#print ('P: consume:{}W {}kWh supply:{}W {}kWh'.format(emparts['p2consume'],emparts['p2consumecounter'],emparts['p2supply'],emparts['p2supplycounter']))
#print ('S: consume:{}VA {}kVAh supply:{}VA {}kVAh'.format(emparts['s2consume'],emparts['s2consumecounter'],emparts['s2supply'],emparts['s2supplycounter']))
#print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q2consume'],emparts['q2consumecounter'],emparts['q2supply'],emparts['q2supplycounter']))
#print ('U: {}V I:{}A cos phi:{}°'.format(emparts['u2'],emparts['i2'],emparts['cosphi2']))
#print ('----L3----')
#print ('P: consume:{}W {}kWh supply:{}W {}kWh'.format(emparts['p3consume'],emparts['p3consumecounter'],emparts['p3supply'],emparts['p3supplycounter']))
#print ('S: consume:{}VA {}kVAh supply:{}VA {}kVAh'.format(emparts['s3consume'],emparts['s3consumecounter'],emparts['s3supply'],emparts['s3supplycounter']))
#print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q3consume'],emparts['q3consumecounter'],emparts['q3supply'],emparts['q3supplycounter']))
#print ('U: {}V I:{}A cos phi:{}°'.format(emparts['u3'],emparts['i3'],emparts['cosphi3']))
#print ('Version: {}'.format(emparts['speedwire-version']))
