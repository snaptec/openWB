#!/usr/bin/env python3
from typing import List
import RPi.GPIO as GPIO
import time

buttons = [
    {"gpio":  6, "mode": 2, "text": "NurPV"},
    {"gpio": 12, "mode": 0, "text": "SofortLaden"},
    {"gpio": 13, "mode": 3, "text": "Stop"},
    {"gpio": 16, "mode": 1, "text": "Min und PV"},
    {"gpio": 21, "mode": 4, "text": "Standby"},
]


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


print("push button daemon starting")
try:
    init()
    print("push button daemon initialized, running loop")
    last_buttons_state = get_buttons_state()
    while True:
        buttons_state = get_buttons_state()
        # print(str(buttons_state))
        if buttons_state != last_buttons_state:
            num_buttons = button_count(buttons_state)
            if num_buttons > 1:
                print("multiple buttons pressed! doing nothing. " + str(buttons_state))
            elif num_buttons == 1:
                for button in range(len(buttons)):
                    if buttons_state[button]:
                        # print("push button " + str(button) + " pressed: " + buttons[button]["text"] + "(" + str(buttons[button]["mode"]) + ")")
                        with open("/var/www/html/openWB/ramdisk/lademodus", "w") as file:
                            file.write(str(buttons[button]["mode"]))
                        with open("/var/www/html/openWB/ramdisk/ladestatus.log", "a") as file:
                            file.write("Lademodus geaendert durch Ladetaster " + str(button) + " auf " + buttons[button]["text"] + "(" + str(buttons[button]["mode"]) + ")\n")
                        break
        time.sleep(0.2)
        last_buttons_state = buttons_state
except Exception as e:
    print(str(e))
    GPIO.cleanup()

print("push button daemon stoped")
