#!/usr/bin/env python3
import subprocess
from importlib import util

PIP_MODULES = [
    "evdev",
    "paho.mqtt",
    "docopt",
    "certifi",
    "aiohttp",
    "pymodbus",
    "requests",
    "jq",
    "ipparser",
    "bs4",
    "pkce",
]

if __name__ == '__main__':
    missing_pip_modules = [m.replace(".", "-") for m in PIP_MODULES if not util.find_spec(m)]
    if missing_pip_modules:
        command = ["sudo", "pip3", "install"] + missing_pip_modules
        print("Running " + str(command))
        subprocess.call(command)
    else:
        print("all required modules are installed")
