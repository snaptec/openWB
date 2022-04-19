#!/usr/bin/env python
# coding: utf8

import time
import RPi.GPIO as GPIO
import argparse


def perform_cp_interruption(duration: int, verbose: bool) -> None:
    if(verbose):
        print("CP-Unterbrechung LP2: %ds" % (duration))

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT)

    GPIO.output(15, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(15, GPIO.LOW)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--duration", type=int, default=4, help="duration in seconds, defaults to 4")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
    args = parser.parse_args()
    perform_cp_interruption(args.duration, args.verbose)
