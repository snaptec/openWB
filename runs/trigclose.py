#!/usr/bin/env python
# coding: utf8

import time
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--chargepoint", type=int, choices=[0, 1, 2],
                    default=0, help="chargepoint to trigger (int), defaults to 0 (1 and 2)")
parser.add_argument("-d", "--duration", type=float, default=2.0, help="duration in seconds (float), defaults to 2.0")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

switchChargepoint1 = (bool)(args.chargepoint == 0 or args.chargepoint == 1)
switchChargepoint2 = (bool)(args.chargepoint == 0 or args.chargepoint == 2)

if(args.verbose):
    print("Wartezeit vor und nach 1p/3p Umschaltung: %fs" % (args.duration))
    print("Zu schaltende Ladepunkte: %d" % (args.chargepoint))
    print("Schalte Ladepunkt 1: %s" % (str(switchChargepoint1)))
    print("Schalte Ladepunkt 2: %s" % (str(switchChargepoint2)))

# setup GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
if(switchChargepoint1):
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(37, GPIO.OUT)
if(switchChargepoint2):
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

# block CP
if(switchChargepoint1):
    GPIO.output(22, GPIO.HIGH)
if(switchChargepoint2):
    GPIO.output(15, GPIO.HIGH)
time.sleep(args.duration)

# switch phases
if(switchChargepoint1):
    GPIO.output(37, GPIO.HIGH)
if(switchChargepoint2):
    GPIO.output(13, GPIO.HIGH)
time.sleep(2)
if(switchChargepoint1):
    GPIO.output(37, GPIO.LOW)
if(switchChargepoint2):
    GPIO.output(13, GPIO.LOW)
time.sleep(args.duration)

# enable CP
if(switchChargepoint1):
    GPIO.output(22, GPIO.LOW)
if(switchChargepoint2):
    GPIO.output(15, GPIO.LOW)
