#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)
time.sleep(4)
GPIO.output(22, GPIO.LOW)
