"""Singelton für das Logger-Modul
"""

from datetime import datetime, timezone
import logging
import os
import traceback
from pathlib import Path

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

        def __process_exception(self, exception):
            if exception != None:
                traceback.print_exc()
                exit(1)

        def __write_log(self, message: str):
            """ Logging für 1.9
            """
            try:
                local_time = datetime.now(timezone.utc).astimezone()
                myPid = str(os.getpid())
                print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)
            except:
                traceback.print_exc()

    instance = None

    def __init__(self):
        if not MainLogger.instance:
            ramdisk = Path(str(Path(os.path.abspath(__file__)).parents[2])+"/ramdisk/bootinprogress").is_file()
            if ramdisk == True:
                MainLogger.instance = MainLogger.__Logger()
            else:
                MainLogger.instance = logging.getLogger("main")
                MainLogger.instance.setLevel(logging.DEBUG)
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fh = logging.FileHandler('/var/www/html/openWB/data/debug/main.log')
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
            fh = logging.FileHandler('/var/www/html/openWB/data/debug/mqtt.log')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            MqttLogger.instance.addHandler(fh)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class DataLogger:
    instance = None

    def __init__(self):
        if not DataLogger.instance:
            DataLogger.instance = logging.getLogger("data")
            DataLogger.instance.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler('/var/www/html/openWB/data/debug/data.log')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            DataLogger.instance.addHandler(fh)

    def __getattr__(self, name):
        return getattr(self.instance, name)
