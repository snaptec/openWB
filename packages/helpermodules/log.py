"""Singelton für das Logger-Modul
"""

import logging
import os
import traceback
import subprocess
import sys
from datetime import datetime, timezone

try:
    from . import compatibility
except (ImportError, ValueError):
    from helpermodules import compatibility

debug_logger = None
debug_fhandler = None
debug_lock = None
data_logger = None
data_fhandler = None
data_lock = None
mqtt_logger = None
mqtt_fhandler = None
mqtt_lock = None


class MainLogger:
    class __Logger:
        def __init__(self):
            pass

        def info(self, message: str, exception=None):
            self.__process_exception(exception)
            if int(os.environ.get("debug")) >= 1:
                self.__write_log(message)

        def debug(self, message: str, exception=None):
            self.__process_exception(exception)
            if int(os.environ.get("debug")) >= 2:
                self.__write_log(message)

        def error(self, message: str, exception=None):
            self.__process_exception(exception)
            self.__write_log(message)

        def warning(self, message: str, exception=None):
            self.__process_exception(exception)
            self.__write_log(message)

        def critical(self, message: str, exception=None):
            self.__process_exception(exception)
            self.__write_log(message)

        def exception(self, message: str, exception=None):
            exception = str(sys.exc_info())
            self.__process_exception(exception)
            self.__write_log(message)

        def __process_exception(self, exception):
            if exception is not None:
                traceback.print_exc()

        def __write_log(self, message: str):
            """ Logging für 1.9
            """
            try:
                local_time = datetime.now(timezone.utc).astimezone()
                my_pid = str(os.getpid())
                print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + my_pid + ": " + message)
            except Exception:
                traceback.print_exc()

    instance = None

    def __init__(self):
        if not MainLogger.instance:
            ramdisk = compatibility.is_ramdisk_in_use()
            if ramdisk:
                MainLogger.instance = MainLogger.__Logger()
            else:
                MainLogger.instance = logging.getLogger("main")
                MainLogger.instance.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s - {%(pathname)s:%(lineno)s} - %(levelname)s - %(message)s')
                fh = logging.FileHandler('/var/www/html/openWB/ramdisk/main.log')
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                MainLogger.instance.addHandler(fh)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class MqttLogger:
    instance = None

    def __init__(self):
        if not MqttLogger.instance:
            MqttLogger.instance = logging.getLogger("mqtt")
            MqttLogger.instance.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler('/var/www/html/openWB/ramdisk/mqtt.log')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            MqttLogger.instance.addHandler(fh)

    def __getattr__(self, name):
        return getattr(self.instance, name)


def cleanup_logfiles():
    """ ruft das Skript zum Kürzen der Logfiles auf.
    """
    subprocess.run(["./packages/helpermodules/cleanup_log.sh", "/var/www/html/openWB/ramdisk/main.log"])
    subprocess.run(["./packages/helpermodules/cleanup_log.sh", "/var/www/html/openWB/ramdisk/mqtt.log"])
