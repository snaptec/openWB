#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--duration", type=float, default=2.0, help="duration in seconds (float), defaults to 2.0")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("Wartezeit vor und nach 1p/3p Umschaltung: %fs"%(args.duration))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

GPIO.output(22, GPIO.HIGH)
time.sleep(float(args.duration))

GPIO.output(37, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(29, GPIO.LOW)
GPIO.output(11, GPIO.LOW)

time.sleep(float(args.duration))
GPIO.output(22, GPIO.LOW)
