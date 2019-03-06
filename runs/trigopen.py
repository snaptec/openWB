#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.OUT)
GPIO.output(29, GPIO.HIGH)
time.sleep(2)
GPIO.output(29, GPIO.LOW)
