#!/usr/bin/env python
#coding: utf8
import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
action = str(sys.argv[1])
#GPIO.setup(26, GPIO.OUT)
#GPIO.output(26, GPIO.LOW)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

if action == "auf":
    GPIO.output(11, GPIO.LOW)
    GPIO.output(7, GPIO.HIGH)
    print( "7 low 11 high" )
    time.sleep(3)
    GPIO.output(7, GPIO.LOW)
if action == "zu":
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(7, GPIO.HIGH)
    print( "11 high, 7 high" )
    time.sleep(3)
    GPIO.output(7, GPIO.LOW)

