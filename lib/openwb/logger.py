import enum
from datetime import datetime
from enum import Enum, IntEnum
from os.path import join

from .config import Config, RAMDISK_PATH


class LogFile(Enum):
    MAIN = "/var/log/openWB.log"
    EVSOC = join(RAMDISK_PATH, "soc.log")
    PV = join(RAMDISK_PATH, "nurpv.log")
    MQTT = join(RAMDISK_PATH, "mqtt.log")
    RFID = join(RAMDISK_PATH, "rfid.log")
    SMARTHOME = join(RAMDISK_PATH, "smarthome.log")
    CHARGESTAT = join(RAMDISK_PATH, "ladestatus.log")


@enum.unique
class LogLevel(IntEnum):
    INFO = 0
    DEBUG = 1
    TRACE = 2


class Logger:
    def __init__(self, log_file: LogFile = LogFile.MAIN, module: str = None, log_level: LogLevel = None):
        if log_level is None:
            try:
                self.logLevel = LogLevel(int(Config()["debug"]))
            except:
                self.logLevel = LogLevel.TRACE
        else:
            self.logLevel = log_level
        self.logFile = log_file
        self.module = "" if str is None else f"{module}: "

    def log(self, level: LogLevel, message: str):
        if level <= self.logLevel:
            with open(self.logFile.value, "a") as fd:
                fd.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {self.module}{message}\n")

    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

    def trace(self, message: str):
        self.log(LogLevel.TRACE, message)
