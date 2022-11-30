#!/usr/bin/env python
# coding: utf8

import time
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--duration", type=float, default=2.0, help="duration in seconds (float), defaults to 2.0")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("Wartezeit vor und nach 1p/3p Umschaltung: %fs" % (args.duration))

# setup GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

# block CP
GPIO.output(22, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
time.sleep(float(args.duration))

# init phases
GPIO.output(37, GPIO.LOW)
GPIO.output(29, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
time.sleep(float(args.duration))

# enable CP
GPIO.output(22, GPIO.LOW)
GPIO.output(15, GPIO.LOW)

# Socket: power to lock motor
GPIO.setup(26, GPIO.OUT)
# set pin to low to prevent the motor from burning out
GPIO.output(26, GPIO.LOW)
