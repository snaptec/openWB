import socket
import struct
from typing import Iterator, Optional

from modules.common.fault_state import FaultState
from modules.sma_shm.speedwiredecoder import decode_speedwire


class SpeedwireListener:
    def __init__(self, timeout_seconds: float):
        self.__timeout_seconds = timeout_seconds
        self.__socket = None  # type: Optional[socket.socket]

    def __enter__(self) -> Iterator[dict]:
        ip_bind = "0.0.0.0"
        multicast_group = "239.12.255.254"
        multicast_port = 9522
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            sock.settimeout(self.__timeout_seconds)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', multicast_port))
            mreq = struct.pack("4s4s", socket.inet_aton(multicast_group), socket.inet_aton(ip_bind))
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except BaseException:
            sock.close()
            raise FaultState.error("could not connect to multicast group or bind to given interface")
        self.__socket = sock

        def generator() -> Iterator[dict]:
            while True:
                datagram = sock.recv(608)
                if len(datagram) >= 18 and datagram[16:18] == b'\x60\x69':
                    yield decode_speedwire(datagram)

        return generator()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__socket.close()
