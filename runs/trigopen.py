#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--duration", type=int, default=2, help="duration in seconds, defaults to 2")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("Wartezeit nach 1p/3p Umschaltung: %ds"%(args.duration))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

GPIO.output(22, GPIO.HIGH)

GPIO.output(29, GPIO.HIGH)
GPIO.output(11, GPIO.HIGH)
time.sleep(2)
GPIO.output(29, GPIO.LOW)
GPIO.output(11, GPIO.LOW)

time.sleep(args.duration)
GPIO.output(22, GPIO.LOW)
