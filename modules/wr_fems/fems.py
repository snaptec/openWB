#!/usr/bin/env python3

import logging
from typing import List

import re
import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.scale_metric import scale_metric

log = logging.getLogger("FEMS")


def update(femskacopw: str, femsip: str):
	log.debug('Wechselrichter FEMS Passwort: ' + femskacopw)
	log.debug('Wechselrichter FEMS IP: ' + femsip)

	response = requests.get('http://'+femsip+':8084/rest/channel/_sum/ProductionActivePower', auth=("x", femskacopw)).json()
	try:
		pvwatt = scale_metric(response["value"], response.get("unit"), 'W') * -1
	except:
		traceback.print_exc()
		exit(1)

	response = requests.get('http://'+femsip+':8084/rest/channel/_sum/ProductionActiveEnergy',
							auth=("x", femskacopw)).json()
	try:
		pvwh = scale_metric(response["value"], response.get("unit"), 'Wh')
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
