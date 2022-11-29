import logging
import os
import sys
from pathlib import Path


def get_log_level_from_environment():
    try:
        return [logging.WARNING, logging.INFO, logging.DEBUG][int(os.environ.get('debug'))]
    except (ValueError, TypeError, IndexError):
        # TypeError if "debug" is not set (os.environ.get returns None)
        # ValueError if `debug` is not an int
        # IndexError if `debug` is not between 0 and 2
        return logging.DEBUG


def filter_soc_neg(record) -> bool:
    if "soc" in record.threadName:
        return False
    return True


def filter_soc_pos(record) -> bool:
    if "soc" in record.threadName:
        return True
    return False


def setup_logging_stdout():
    format_str_short = '%(asctime)s - %(message)s'
    root_logger = logging.getLogger()
    # Only do something if logging is not yet initialized.
    # It may not be initialized if this function is called multiple times or of logging is set up while unit testing
    if not root_logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(u"%(asctime)s: PID: %(process)d: %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        )
        root_logger.addHandler(handler)
        root_logger.setLevel(get_log_level_from_environment())
        logging.getLogger().handlers[0].addFilter(filter_soc_neg)

    mqtt_log = logging.getLogger("mqtt")
    mqtt_log.propagate = False
    mqtt_file_handler = logging.FileHandler(str(Path(__file__).resolve().parents[2] / 'ramdisk' / ('mqtt.log')))
    mqtt_file_handler.setFormatter(logging.Formatter(format_str_short))
    mqtt_log.addHandler(mqtt_file_handler)

    soc_log = logging.getLogger("soc")
    soc_log.propagate = True
    soc_file_handler = logging.FileHandler(str(Path(__file__).resolve().parents[2] / 'ramdisk' / ('soc.log')))
    soc_file_handler.setFormatter(logging.Formatter(
        u"%(asctime)s: PID: %(process)d: %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    soc_file_handler.addFilter(filter_soc_pos)
    soc_log.addHandler(soc_file_handler)

    urllib3_log = logging.getLogger("urllib3.connectionpool")
    urllib3_log.propagate = True
    urllib3_file_handler = logging.FileHandler(str(Path(__file__).resolve().parents[2] / 'ramdisk' / ('soc.log')))
    urllib3_file_handler.setFormatter(logging.Formatter(
        u"%(asctime)s: PID: %(process)d: %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    urllib3_file_handler.addFilter(filter_soc_pos)
    urllib3_log.addHandler(urllib3_file_handler)

    logging.getLogger("pymodbus").setLevel(logging.WARNING)


class MainLogger:
    class __Logger:
        logger = logging.getLogger()

        def __init__(self):
            pass

        def info(self, message: str, exception=None):
            self.logger.info(message, exc_info=exception)

        def debug(self, message: str, exception=None):
            self.logger.debug(message, exc_info=exception)

        def error(self, message: str, exception=None):
            self.logger.error(message, exc_info=exception)

        def warning(self, message: str, exception=None):
            self.logger.warning(message, exc_info=exception)

        def critical(self, message: str, exception=None):
            self.logger.critical(message, exc_info=exception)

        def exception(self, message: str):
            self.logger.exception(message)

    instance = None

    def __new__(cls):
        if not MainLogger.instance:
            setup_logging_stdout()
            MainLogger.instance = MainLogger.__Logger()
        return MainLogger.instance
