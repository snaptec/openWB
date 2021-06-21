#!/usr/bin/env python
#coding: utf8

import RPi.GPIO as GPIO
import sys

onOff = str(sys.argv[1])

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.OUT)

f = open('/var/www/html/openWB/ramdisk/socketActivated', 'w')

if (onOff == "off"):
    GPIO.output(15, GPIO.HIGH)
    f.write(str(0))
elif (onOff == "on"):
    GPIO.output(15, GPIO.LOW)
    f.write(str(1))
else:
    print("Invalid argument: '" + onOff + "'. Supporting only [on,off]")

f.close()
