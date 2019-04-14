#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.OUT)
GPIO.output(37, GPIO.HIGH)
time.sleep(2)
GPIO.output(37, GPIO.LOW)
