"""A server that receives and executes commands via file socket

The server expects to receive JSON arrays via a file socket. The first element in the array is the module to call.
That module must have a function with name `main`. That function is called with the remaining array elements as
parameter.

Thanks to the server running continuously this means that python code can be executed without bootstrapping the python
environment first.
"""
import contextlib
import fcntl
import importlib
import io
import json
import logging
import os
import re
import signal
import socket
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable

from helpermodules.log import setup_logging_stdout

log = logging.getLogger("legacy run server")
debug_dirty = True


def read_all_bytes(connection: socket.socket):
    buffer = bytes()
    while True:
        tmp = connection.recv(1024)
        if tmp:
            buffer += tmp
        else:
            return buffer


@contextmanager
def redirect_stdout_stderr_exceptions_to_log():
    with contextlib.redirect_stderr(io.StringIO()) as io_stderr:
        with contextlib.redirect_stdout(io.StringIO()) as io_stdout:
            unhandled_exception = None
            try:
                yield
            except Exception as e:
                unhandled_exception = e
            except SystemExit:
                # e.g. ArgumentParser attempts to exit. Since we are in a separate thread this is ignored anyway,
                # but we still want to print stderr and stdout
                pass
            stderr = io_stderr.getvalue().strip()
            stdout = io_stdout.getvalue().strip()
            if stderr:
                log.warning(stderr)
            if stdout:
                log.info(stdout)
            if unhandled_exception:
                log.error("Unhandled exception", exc_info=unhandled_exception)


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
                    with redirect_stdout_stderr_exceptions_to_log():
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


def try_update_log_level_from_config():
    try:
        config_file_contents = (Path(__file__).parents[1] / "openwb.conf").read_text("utf-8")
    except Exception as e:
        # In case we cannot read the config file (maybe due to some lock, race conditions or someone moved the file
        # temporarily), we just ignore the change
        log.debug("Could not read openwb.conf. Ignoring.", exc_info=e)
        return
    match = re.search("^debug=([012])", config_file_contents, re.MULTILINE)
    if match is None:
        logging.getLogger().setLevel(logging.DEBUG)
        log.warning("Debug setting not found in config. Assuming log-level DEBUG")
        return
    log_level_new = [logging.WARNING, logging.INFO, logging.DEBUG][int(match.group(1))]
    log_level_old = logging.getLogger().level
    if log_level_new != log_level_old:
        # Emit log message before AND after changing the level so that in case the level WAS or WILL BE >= INFO this
        # is logged:
        log_level_names = logging.getLevelName(log_level_old), logging.getLevelName(log_level_new)
        log.info("Changing log level %s -> %s", *log_level_names)
        logging.getLogger().setLevel(log_level_new)
        log.info("Log level changed %s -> %s", *log_level_names)


def update_log_level_from_config():
    global debug_dirty
    try:
        try_update_log_level_from_config()
    except Exception as e:
        log.error("Could not update log level from openwb.conf", exc_info=e)
    debug_dirty = False


def handle_message(message: bytes):
    message_str = message.decode("utf-8").strip()
    time_start = time.time()
    if debug_dirty:
        update_log_level_from_config()
    log.debug("Received command %.100s", message_str)
    parsed = json.loads(message_str)
    importlib.import_module(parsed[0]).main(parsed[1:])
    log.debug("Completed running command in %.2fs: %.100s", time.time() - time_start, message_str)


def watch_config():
    """This function watches the openwb.conf file for modifications. If it is modified, the log level is refreshed

    The function uses the F_NOTIFY Linux kernel feature to receive a notification if a file in the directory where
    openwb.conf is stored changes.
    """

    def signal_handler(_signum, _frame):
        global debug_dirty
        debug_dirty = True

    signal.signal(signal.SIGIO, signal_handler)
    file_descriptor = os.open(str(Path(__file__).parents[1]), os.O_RDONLY)
    fcntl.fcntl(file_descriptor, fcntl.F_SETSIG, 0)
    fcntl.fcntl(file_descriptor, fcntl.F_NOTIFY, fcntl.DN_MODIFY | fcntl.DN_MULTISHOT)


if __name__ == '__main__':
    setup_logging_stdout()
    sys.excepthook = exception_handler
    update_log_level_from_config()
    watch_config()
    log.info("Starting legacy run server")
    SocketListener(Path(__file__).parent / "legacy_run_server.sock", handle_message).handle_connections()
