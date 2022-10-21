#!/usr/bin/env python3

import logging
from typing import List

import re
import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("FEMS")


def write_ramdisk(value, file):
    try:
        if file == "speichersoc":
            if re.search("^[-+]?[0-9]+.?[0-9]*$", str(value)) is None:
                value = "0"
        log.debug(file+': ' + str(value))
        with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
            f.write(str(value))
    except:
        traceback.print_exc()
        exit(1)


def update(multifems: str, femskacopw: str, femsip: str):
    if multifems == "0":
        try:
            response = requests.get(
                "http://" + femsip + ":8084/rest/channel/ess0/(Soc|ActiveChargeEnergy|ActiveDischargeEnergy)",
                auth=("x", femskacopw)).json()
        except:
            traceback.print_exc()
            exit(1)
        for singleValue in response:
            address = singleValue["address"]
            if (address == "ess0/Soc"):
                write_ramdisk(singleValue["value"], "speichersoc")
            elif address == "ess0/ActiveChargeEnergy":
                write_ramdisk(singleValue["value"], "speicherikwh")
            elif address == "ess0/ActiveDischargeEnergy":
                write_ramdisk(singleValue["value"], "speicherekwh")
    else:
        try:
            response = requests.get(
                "http://" + femsip + ":8084/rest/channel/ess2/(Soc|ActiveChargeEnergy|ActiveDischargeEnergy)",
                auth=("x", femskacopw)).json()
        except:
            traceback.print_exc()
            exit(1)
        for singleValue in response:
            address = singleValue["address"]
            if (address == "ess2/Soc"):
                write_ramdisk(singleValue["value"], "speichersoc")
            elif address == "ess2/ActiveChargeEnergy":
                write_ramdisk(singleValue["value"], "speicherikwh")
            elif address == "ess2/ActiveDischargeEnergy":
                write_ramdisk(singleValue["value"], "speicherekwh")

    try:
        response = requests.get(
            "http://" + femsip + ":8084/rest/channel/_sum/(GridActivePower|ProductionActivePower|ConsumptionActivePower)",
            auth=("x", femskacopw)).json()
    except:
        traceback.print_exc()
        exit(1)
    for singleValue in response:
        address = singleValue["address"]
        if (address == "_sum/GridActivePower"):
            grid = singleValue["value"]
        elif address == "_sum/ProductionActivePower":
            pv = singleValue["value"]
        elif address == "_sum/ConsumptionActivePower":
            haus = singleValue["value"]

    leistung = grid + pv - haus

    ra = "^[-+]?[0-9]+.?[0-9]*$"
    if re.search(ra, str(leistung)) is None:
        leistung = "0"
    log.debug('Speicherleistung: ' + str(leistung))
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write(str(leistung))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
