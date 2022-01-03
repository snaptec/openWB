"""A server that receives and executes commands via file socket

The server expects to receive JSON arrays via a file socket. The first element in the array is the module to call.
That module must have a function with name `main`. That function is called with the remaining array elements as
parameter.

Thanks to the server running continuously this means that python code can be executed without bootstrapping the python
environment first.
"""
import importlib
import json
import logging
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Callable

from helpermodules.log import setup_logging_stdout

log = logging.getLogger("legacy run server")


def read_all_bytes(connection: socket.socket):
    buffer = bytes()
    while True:
        tmp = connection.recv(1024)
        if tmp:
            buffer += tmp
        else:
            return buffer


class SocketListener:
    def __init__(self, path: Path, callback: Callable):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        self.__sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__sock.bind(str(path))
        self.__sock.listen(5)
        self.__path = path
        self.__callback = callback

    def handle_connections(self):
        while True:
            try:
                connection = self.__sock.accept()[0]

                def handle_connection():
                    # We keep the connection open during `callback`. Closing the connection is the signal to the
                    # caller that processing completed
                    with connection:
                        self.__callback(read_all_bytes(connection))

                threading.Thread(target=handle_connection).start()
            except Exception as e:
                log.error("Error while handling legacy run server connection", exc_info=e)
                if self.__sock.fileno() == -1:
                    return

    def close(self):
        self.__sock.close()


def exception_handler(_type, value, _traceback):
    log.error("Unhandled Exception", exc_info=value)


def handle_message(message: bytes):
    message_str = message.decode("utf-8").strip()
    time_start = time.time()
    log.debug("Received command %.100s", message_str)
    parsed = json.loads(message_str)
    importlib.import_module(parsed[0]).main(parsed[1:])
    log.debug("Completed running command in %.2fs: %.100s", time.time() - time_start, message_str)


if __name__ == '__main__':
    setup_logging_stdout()
    sys.excepthook = exception_handler
    log.info("Starting legacy run server")
    SocketListener(Path(__file__).parent / "legacy_run_server.sock", handle_message).handle_connections()
