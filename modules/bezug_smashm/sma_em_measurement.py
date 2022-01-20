#!/usr/bin/env python3
import logging
import socket
import struct
import sys
from math import copysign
from typing import Optional

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import CounterState
from modules.common.store import get_counter_value_store
from speedwiredecoder import decode_speedwire

ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522

log = logging.getLogger("SMA HomeManager")


def run(sma_serials: Optional[str] = None):
    log.debug("Beginning update")
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
    while not process_datagram(sock.recv(608), sma_serials):
        pass
    log.debug("Update completed successfully")


def process_datagram(datagram: bytes, sma_serials: Optional[str] = None):
    # Paket ignorieren, wenn es nicht dem SMA-"energy meter protocol" mit protocol id = 0x6069 entspricht
    if datagram[16:18] != b'\x60\x69':
        return
    sma_data = decode_speedwire(datagram)
    if sma_serials is None or sma_serials == 'none' or str(sma_data['serial']) == sma_serials:
        def get_power(phase_str: str = ""):
            # "consume" and "supply" are always >= 0. Thus we need to check both "supply" and "consume":
            power_import = sma_data["p" + phase_str + "consume"]
            return -sma_data["p" + phase_str + "supply"] if power_import == 0 else power_import

        powers = [get_power(str(phase)) for phase in range(1, 4)]

        get_counter_value_store(1).set(CounterState(
            imported=sma_data['pconsumecounter'] * 1000,
            exported=sma_data['psupplycounter'] * 1000,
            power=get_power(),
            voltages=[sma_data["u" + str(phase)] for phase in range(1, 4)],
            # currents reported are always absolute values. We get the sign from power:
            currents=[copysign(sma_data["i" + str(phase)], powers[phase - 1]) for phase in range(1, 4)],
            powers=powers,
            power_factors=[sma_data["cosphi" + str(phase)] for phase in range(1, 4)],
            frequency=sma_data.get("frequency")
        ))
        return True


if __name__ == '__main__':
    setup_logging_stdout()
    run_using_positional_cli_args(run)
