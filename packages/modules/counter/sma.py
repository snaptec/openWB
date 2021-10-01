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
 * 2021-09-30 Lena K changes to run with openWB2
 *
 */
"""

import signal
import sys
#import smaem
import socket
import struct
from sma_lib import decode_speedwire
import time
import sys
import struct

if __name__ == "__main__":
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import set_values
else:
    from ...helpermodules import log
    from . import set_values


class module(set_values.set_values):
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        try:
            # abort-signal
            signal.signal(signal.SIGALRM, self.abortprogram)
            signal.alarm(3)
            try:
                # read configuration
                #parser = ConfigParser()
                # default values
                smaserials = self.data["config"]["id"]
                ipbind = '0.0.0.0'
                MCAST_GRP = '239.12.255.254'
                MCAST_PORT = 9522

                # try:
                #    smaemserials=parser.get('SMA-EM', 'serials')
                #    ipbind=parser.get('DAEMON', 'ipbind')
                #    MCAST_GRP = parser.get('DAEMON', 'mcastgrp')
                #    MCAST_PORT = int(parser.get('DAEMON', 'mcastport'))
                # except:
                #    print('Cannot find config /etc/smaemd/config... using defaults')
                print("1")
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                print("2")
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                print("3")
                sock.bind(('', MCAST_PORT))
                try:
                    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
                    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                    print("4")
                except BaseException:
                    log.log_comp("error", 'SMA'+str(self.counter_num)+' could not connect to mulicast group or bind to given interface', self.ramdisk)
                    return
                # processing received messages
                counter = 0
                # Endlosschleife vermeiden
                print("counter")
                while counter < 3:
                    emparts = {}
                    emparts = decode_speedwire(sock.recv(608))
                    # Output...
                    # don't know what P,Q and S means:
                    # http://en.wikipedia.org/wiki/AC_power or http://de.wikipedia.org/wiki/Scheinleistung
                    # thd = Total_Harmonic_Distortion http://de.wikipedia.org/wiki/Total_Harmonic_Distortion
                    # cos phi is always positive, no matter what quadrant
                    positive = [1, 1, 1, 1]
                    if smaserials is None or smaserials == 'none' or str(emparts['serial']) == smaserials:
                        # Special treatment for positive / negative power

                        power_all = int(emparts['pconsume'])
                        if power_all < 5:
                            power_all = -int(emparts['psupply'])
                            positive[0] = -1
                        try:
                            exported = emparts['psupplycounter'] * 1000
                        except Exception as e:
                            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                            exported = 0
                        try:
                            imported = emparts['pconsumecounter'] * 1000
                        except Exception as e:
                            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                            exported = 0
                        # Power per phase
                        power_phases = []*3
                        for phase in [1, 2, 3]:
                            power = int(emparts['p%iconsume' % phase])
                            if power < 5:
                                power = -int(emparts['p%isupply' % phase])
                                positive[phase] = -1
                            power_phases[phase] = power
                        # Voltage
                        voltage = []*3
                        for phase in [1, 2, 3]:
                            try:
                                if 'u%i' % phase in emparts:
                                    value = emparts['u%i' % phase]
                                    voltage[phase] = value
                            except Exception as e:
                                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                                voltage[phase] = 0
                        # Current
                        current = []*3
                        for phase in [1, 2, 3]:
                            try:
                                if 'i%i' % phase in emparts:
                                    value = emparts['i%i' % phase]
                                    value *= positive[phase]
                                    current[phase] = value
                            except Exception as e:
                                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                                current[phase] = 0
                        # Power-Factor
                        power_factor = []*3
                        for phase in [1, 2, 3]:
                            try:
                                if 'cosphi%i' % phase in emparts:
                                    value = emparts['cosphi%i' % phase]
                                    power_factor[phase] = value
                            except Exception as e:
                                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                                power_factor[phase] = 0
                        try:
                            frequency = emparts['frequency']
                        except Exception as e:
                            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                            frequency = 0
                        break

                    time.sleep(1)
                    counter = counter + 1
                    print(str(counter))

                if counter < 3:
                    values = [voltage,
                            current,
                            power_phases,
                            power_factor,
                            [imported, exported],
                            power_all,
                            frequency]
                    self.set(self.counter_num, values, self.ramdisk)
                else:
                    log.log_comp("error", "SMA"+str(self.counter_num)+": Es wurden keine Daten empfangen.", self.ramdisk)
            except Exception:
                pass
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

    # clean exit
    def abortprogram(self, signal, frame):
        # Housekeeping -> nothing to cleanup
        log.log_comp("error", "Timeout")
        raise Exception


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        id = str(sys.argv[1])
        mod.data["config"]["id"] = id

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module sma id: ' + str(id))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
