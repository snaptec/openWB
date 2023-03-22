#!/usr/bin/env python3
import time
import traceback

basePath = "/var/www/html/openWB"
ramdiskPath = basePath + "/ramdisk"
logFilename = ramdiskPath + "/openWB.log"
rse_inputs = [
    {"gpio": 8, "file": "rsestatus"},
    {"gpio": 9, "file": "rse2status"}
]

loglevel = 1


# handling of all logging statements
def log_debug(level: int, msg: str, traceback_str: str = None) -> None:
    if level >= loglevel:
        with open(logFilename, 'a') as log_file:
            log_file.write(time.ctime() + ': rse: ' + msg + '\n')
            if traceback_str is not None:
                log_file.write(traceback_str + '\n')


# write value to file in ramdisk
def write_to_ramdisk(filename: str, content: str) -> None:
    with open(ramdiskPath + "/" + filename, "w") as file:
        file.write(content)


def init():
    GPIO.setmode(GPIO.BCM)
    for rse in rse_inputs:
        GPIO.setup(rse["gpio"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        write_to_ramdisk(rse["file"], "0")


def get_rse_states():
    return [GPIO.input(rse_inputs[rse]["gpio"]) == GPIO.LOW for rse in range(len(rse_inputs))]


try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    exit("Module RPi.GPIO missing! Maybe we are not running on supported hardware?")

log_debug(2, "rse daemon starting")
try:
    init()
    log_debug(1, "rse daemon initialized, running loop")
    last_rse_states = get_rse_states()
    while True:
        rse_states = get_rse_states()
        log_debug(0, "rse state: " + str(rse_states))
        for rse in range(len(rse_inputs)):
            if rse_states[rse] != last_rse_states[rse]:
                write_to_ramdisk(rse_inputs[rse]["file"], str("1" if rse_states[rse] else "0"))
                log_debug(2, "rse input changed: RSE" + str(rse) + ": " + str(last_rse_states[rse]) + "->" +
                          str(rse_states[rse]) + " (" + str("1" if rse_states[rse] else "0") + ">" +
                          rse_inputs[rse]["file"] + ")")
        time.sleep(10.2)
        last_rse_states = rse_states
except Exception as e:
    log_debug(2, "ERROR in rse daemon: " + str(e), traceback.format_exc())
    GPIO.cleanup()

log_debug(2, "rse daemon stopped")
