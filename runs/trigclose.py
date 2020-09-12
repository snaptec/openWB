#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)


GPIO.setup(37, GPIO.OUT)
GPIO.output(37, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
time.sleep(2)
GPIO.output(37, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
time.sleep(2)
GPIO.output(22, GPIO.LOW)
