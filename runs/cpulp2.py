#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)
time.sleep(4)
GPIO.output(15, GPIO.LOW)
