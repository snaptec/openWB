#!/usr/bin/env python3
from typing import List
import time
import traceback

basePath = "/var/www/html/openWB"
ramdiskPath = basePath + "/ramdisk"
logFilename = ramdiskPath + "/ladestatus.log"
buttons = [
    {"gpio":  6, "mode": 2, "text": "NurPV"},
    {"gpio": 12, "mode": 0, "text": "SofortLaden"},
    {"gpio": 13, "mode": 3, "text": "Stop"},
    {"gpio": 16, "mode": 1, "text": "Min und PV"},
    {"gpio": 21, "mode": 4, "text": "Standby"},
]

loglevel = 1


# handling of all logging statements
def log_debug(level: int, msg: str, traceback_str: str = None) -> None:
    if level >= loglevel:
        with open(logFilename, 'a') as log_file:
            log_file.write(time.ctime() + ': ' + msg + '\n')
            if traceback_str is not None:
                log_file.write(traceback_str + '\n')


# write value to file in ramdisk
def write_to_ramdisk(filename: str, content: str) -> None:
    with open(ramdiskPath + "/" + filename, "w") as file:
        file.write(content)


def init():
    GPIO.setmode(GPIO.BCM)
    for button in buttons:
        GPIO.setup(button["gpio"], GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_count(buttons: List):
    count = 0
    for button in buttons:
        if button:
            count += 1
    return count


def get_buttons_state():
    return [GPIO.input(buttons[button]["gpio"]) == GPIO.LOW for button in range(len(buttons))]


try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    exit("Module RPi.GPIO missing! Maybe we are not running on supported hardware?")

log_debug(2, "push button daemon starting")
try:
    init()
    log_debug(1, "push button daemon initialized, running loop")
    last_buttons_state = get_buttons_state()
    while True:
        buttons_state = get_buttons_state()
        log_debug(0, "push buttons state: " + str(buttons_state))
        if buttons_state != last_buttons_state:
            num_buttons = button_count(buttons_state)
            if num_buttons > 1:
                log_debug(2, "multiple buttons pressed! doing nothing. " + str(buttons_state))
            elif num_buttons == 1:
                for button in range(len(buttons)):
                    if buttons_state[button]:
                        write_to_ramdisk("lademodus", str(buttons[button]["mode"]))
                        log_debug(2, "Lademodus geändert durch Ladetaster " + str(button) + " auf " +
                                  buttons[button]["text"] + "(" + str(buttons[button]["mode"]) + ")")
                        break
        time.sleep(0.2)
        last_buttons_state = buttons_state
except Exception as e:
    log_debug(2, "ERROR in pushButtonsDaemon: " + str(e), traceback.format_exc())
    GPIO.cleanup()

log_debug(2, "push button daemon stopped")
