#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)


GPIO.setup(29, GPIO.OUT)
GPIO.output(29, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
time.sleep(2)
GPIO.output(29, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
time.sleep(2)
GPIO.output(22, GPIO.LOW)
