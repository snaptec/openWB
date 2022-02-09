import logging
import os
import sys


def get_log_level_from_environment():
    try:
        return [logging.WARNING, logging.INFO, logging.DEBUG][int(os.environ.get('debug'))]
    except (ValueError, TypeError, IndexError):
        # TypeError if "debug" is not set (os.environ.get returns None)
        # ValueError if `debug` is not an int
        # IndexError if `debug` is not between 0 and 2
        return logging.DEBUG


def setup_logging_stdout():
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
