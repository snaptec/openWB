"""Log-Modul, dass die KOnfiguration für die Log-Dateien und Funktionen zum Aufruf der einzelnen Handler enthält
"""

from datetime import datetime, timezone
import filelock
import logging
import os
import pathlib
import subprocess
import traceback

debug_logger = None
debug_fhandler = None
debug_lock = None
data_logger = None
data_fhandler = None
data_lock = None
mqtt_logger = None
mqtt_fhandler = None
mqtt_lock = None


def setup_logger():
    """ initialisiert die Logger und Lock-Files für debug-, data- und mqtt-Logging.
    """
    global debug_logger
    global debug_fhandler
    global debug_lock
    # Ordner erstellen, falls nicht vorhanden
    pathlib.Path("/var/www/html/openWB/data/debug").mkdir(parents=True, exist_ok=True)
    debug_logger, debug_fhandler = _config_logger("debug")
    debug_lock = filelock.FileLock('/var/www/html/openWB/data/debug/debug.log.lock')
    global data_logger
    global data_fhandler
    global data_lock
    data_logger, data_fhandler = _config_logger("data")
    data_lock = filelock.FileLock('/var/www/html/openWB/data/debug/data.log.lock')
    global mqtt_logger
    global mqtt_fhandler
    global mqtt_lock
    mqtt_logger, mqtt_fhandler = _config_logger("mqtt", stream = False)
    mqtt_lock = filelock.FileLock('/var/www/html/openWB/data/debug/mqtt.log.lock')


def _config_logger(name, stream = True):
    """ konfiguriert den Logger für das Logging in eine Datei und falls stream = True für das Logging auf der Konsole.

    Parameter
    ---------
    name: str
        Name des Loggers und der Log-Datei
    stream: bool
        Logging auf der Konsole
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('/var/www/html/openWB/data/debug/'+name+'.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if stream == True:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger, fh

def message_debug_log(level, message):
    """ kümmert sich um das Locking der Log-Datei und übergibt die Nachricht an den entsprechenden Log-Handler.

    Parameter
    ---------
    level: str
        Debug-Level
    message: str
        Log-Nachricht
    """
    with debug_lock.acquire(timeout=1):
        _set_message(debug_logger, level, message)
        debug_fhandler.close()

def message_data_log(level, message):
    with data_lock.acquire(timeout=1):
        _set_message(data_logger, level, message)
        data_fhandler.close()
    
def message_mqtt_log(topic, payload):
    with mqtt_lock.acquire(timeout=1):
        _set_message(mqtt_logger, "info", "Topic: "+topic+", Payload: "+payload)
        mqtt_fhandler.close()


def _set_message(logger, level, message):
    """ überibt die Message an die Logger-Methode, die dem übergebenen Level entspricht.

    Paramter
    --------
    logger: logger-handle
        Logger, in dem die Nachricht verarbeitet werden soll
    level: str
        Debug-Level
    message: str
        Log-Nachricht
    """
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)

def exception_logging(exception):
    """ Formatiert Exceptions für die Log-Ausgabe. Vom Traceback wird nur der letzte Eintrag verwendet, damit die Logmeldung nicht zu lang wird.

    Parameters
    ----------
    exception: ecxeption
        raised exception
    """
    tb = exception.__traceback__
    value= str(exception)
    exctype=str(type(exception))
    msg="Exception type: "+exctype+" Traceback: "+str(traceback.format_tb(tb, -1))+" Details: "+value
    message_debug_log("error", msg)

def cleanup_logfiles():
    """ kürzt die Logfiles auf die letzten 1000 Zeilen.
    """
    with data_lock.acquire(timeout=1):
        subprocess.run(["./packages/helpermodules/cleanup_log.sh", "/var/www/html/openWB/data/debug/data.log"])
    with debug_lock.acquire(timeout=1):
        subprocess.run(["./packages/helpermodules/cleanup_log.sh", "/var/www/html/openWB/data/debug/debug.log"])
    with mqtt_lock.acquire(timeout=1):
        subprocess.run(["./packages/helpermodules/cleanup_log.sh", "/var/www/html/openWB/data/debug/mqtt.log"])

def log_1_9(message):
    """ Logging für 1.9
    """
    local_time = datetime.now(timezone.utc).astimezone()
    myPid = str(os.getpid())
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)

def log_exception_comp(exception, ramdisk):
    """ Logging für 1.9 (ramdisk = True) und 2.x (ramdisk = False).
    """
    if ramdisk == False:
        exception_logging(exception)
    else:
        traceback.print_exc()
        exit(1)