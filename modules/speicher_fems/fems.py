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


def update(multifems: str, femskacopw: str, femsip: str):
	if multifems == "0":
		try:
			response = requests.get(
				"http://" + femsip + ":8084/rest/channel/ess0/(Soc|DcChargeEnergy|DcDischargeEnergy)",
				auth=("x", femskacopw)).json()
		except:
			traceback.print_exc()
			exit(1)
		for singleValue in response:
			address = singleValue["address"]
			if (address == "ess0/Soc"):
				write_ramdisk(singleValue["value"], "speichersoc")
			elif address == "ess0/DcChargeEnergy":
				energy = adjust_energy_from_unit_to_watthours(singleValue['value'], singleValue['unit'])
				write_ramdisk(energy, "speicherikwh")
			elif address == "ess0/DcDischargeEnergy":
				energy = adjust_energy_from_unit_to_watthours(singleValue['value'], singleValue['unit'])
				write_ramdisk(energy, "speicherekwh")
	else:
		try:
			response = requests.get(
				"http://" + femsip + ":8084/rest/channel/ess2/(Soc|DcChargeEnergy|DcDischargeEnergy)",
				auth=("x", femskacopw)).json()
		except:
			traceback.print_exc()
			exit(1)
		for singleValue in response:
			address = singleValue["address"]
			if (address == "ess2/Soc"):
				write_ramdisk(singleValue["value"], "speichersoc")
			elif address == "ess2/DcChargeEnergy":
				energy = adjust_energy_from_unit_to_watthours(singleValue['value'], singleValue['unit'])
				write_ramdisk(energy, "speicherikwh")
			elif address == "ess2/DcDischargeEnergy":
				energy = adjust_energy_from_unit_to_watthours(singleValue['value'], singleValue['unit'])
				write_ramdisk(energy, "speicherekwh")

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
			grid = adjust_power_from_unit_to_watt(singleValue['value'], singleValue['unit'])
		elif address == "_sum/ProductionActivePower":
			pv = adjust_power_from_unit_to_watt(singleValue['value'], singleValue['unit'])
		elif address == "_sum/ConsumptionActivePower":
			haus = adjust_power_from_unit_to_watt(singleValue['value'], singleValue['unit'])

	leistung = grid + pv - haus

	ra = "^[-+]?[0-9]+.?[0-9]*$"
	if re.search(ra, str(leistung)) is None:
		leistung = "0"
	log.debug('Speicherleistung: ' + str(leistung))
	with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
		f.write(str(leistung))


def main(argv: List[str]):
	run_using_positional_cli_args(update, argv)

# example FEMS response on rest/channel/ess0/(Soc|DcChargeEnergy|DcDischargeEnergy)
# [
#     {
#         "address": "ess0/DcChargeEnergy",
#         "type": "LONG",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "Wh",
#         "value": 456732
#     },
#     {
#         "address": "ess0/Soc",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "%",
#         "value": 67
#     },
#     {
#         "address": "ess0/DcDischargeEnergy",
#         "type": "LONG",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "Wh",
#         "value": 453354
#     }
# ]
