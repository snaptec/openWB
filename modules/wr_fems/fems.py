#!/usr/bin/env python3

import logging
from typing import List

import re
import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("FEMS")


def adjust_energy_from_unit_to_watthours(energy, unit):
	try:
		if (unit.lower() == 'kwh'):
			energy = energy * 1000.0
		elif (unit == 'MWh'):
			energy = energy * 1000000.0
		elif (unit == 'mWh'):
			energy = energy / 1000.0

		return energy
	except:
		traceback.print_exc()


def adjust_power_from_unit_to_watt(power, unit):
	try:
		if (unit == 'mW'):
			power = power / 1000.0
		elif (unit == 'MW'):
			power = power * 1000000.0
		elif (unit.lower() == 'kW'):
			power = power * 1000.0

		return power
	except:
		traceback.print_exc()


def update(femskacopw: str, femsip: str):
	log.debug('Wechselrichter FEMS Passwort: ' + femskacopw)
	log.debug('Wechselrichter FEMS IP: ' + femsip)

	response = requests.get('http://'+femsip+':8084/rest/channel/_sum/ProductionActivePower', auth=("x", femskacopw)).json()
	try:
		pvwatt = adjust_power_from_unit_to_watt(response["value"], response["unit"]) * -1
	except:
		traceback.print_exc()
		exit(1)

	response = requests.get('http://'+femsip+':8084/rest/channel/_sum/ProductionActiveEnergy',
							auth=("x", femskacopw)).json()
	try:
		pvwh = adjust_energy_from_unit_to_watthours(response["value"], response["unit"])
	except:
		traceback.print_exc()
		exit(1)

	regex = '^-?[0-9]+$'
	if re.search(regex, str(pvwatt)) is None:
		pvwatt = "0"
	if re.search(regex, str(pvwh)) is not None:
		log.debug('WR Energie: ' + str(pvwh))
		with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
			f.write(str(pvwh))
	log.debug('WR Leistung: ' + str(pvwatt))
	with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
		f.write(str(pvwatt))


def main(argv: List[str]):
	run_using_positional_cli_args(update, argv)


# example FEMS response on rest/channel/_sum/ProductionActivePower
# {
#     "address": "_sum/ProductionActivePower",
#     "type": "INTEGER",
#     "accessMode": "RO",
#     "text": "Total production; always positive",
#     "unit": "W",
#     "value": 920
# }
