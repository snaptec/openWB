#!/usr/bin/env python3

import logging
from typing import List

import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.scale_metric import scale_metric

log = logging.getLogger("FEMS")


def write_ramdisk(val, file):
	try:
		with open('/var/www/html/openWB/ramdisk/'+file, 'w') as f:
			f.write(str(val))
	except:
		traceback.print_exc()


def get_value(url, file):
	try:
		response = requests.get(url, timeout=2).json()
		val = response["value"]
		with open('/var/www/html/openWB/ramdisk/'+file, 'w') as f:
			f.write(str(val))
	except:
		traceback.print_exc()


def update(password: str, ip_address: str):
	try:
		# Grid meter values
		response = requests.get('http://x:' + password + '@' + ip_address +
								':8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)', timeout=1).json()

		# ATTENTION: Recent FEMS versions started using the "unit" field (see example response below) and
		#            kind-of arbitrarily return either Volts, Kilowatthours or Hz or Millivolts, Watthours or Millihertz
		#            Others units (kW, kV) have not yet been observed but are coded just to be future-proof.
		v1, v2, v3 = 0, 0, 0
		p1, p2, p3 = 0, 0, 0
		for singleValue in response:
			address = singleValue['address']
			if (address == 'meter0/Frequency'):
				frequency = scale_metric(singleValue['value'], singleValue.get('unit'), 'Hz')
				write_ramdisk(frequency, 'evuhz')
			elif (address == 'meter0/ActivePower'):
				power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
				write_ramdisk(power, 'wattbezug')
			elif (address == 'meter0/ActivePowerL1'):
				power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
				write_ramdisk(power, 'bezugw1')
				p1 = power
			elif (address == 'meter0/ActivePowerL2'):
				power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
				write_ramdisk(power, 'bezugw2')
				p2 = power
			elif (address == 'meter0/ActivePowerL3'):
				power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
				write_ramdisk(power, 'bezugw3')
				p3 = power
			elif (address == 'meter0/VoltageL1'):
				voltage = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
				write_ramdisk(voltage, 'evuv1')
				v1 = voltage
			elif (address == 'meter0/VoltageL2'):
				voltage = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
				write_ramdisk(voltage, 'evuv2')
				v2 = voltage
			elif (address == 'meter0/VoltageL3'):
				voltage = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
				write_ramdisk(voltage, 'evuv3')
				v3 = voltage

		if (v1 != 0):
			a1 = p1 / v1
			write_ramdisk(a1, 'bezuga1')
		if (v2 != 0):
			a2 = p2 / v2
			write_ramdisk(a2, 'bezuga2')
		if (v3 != 0):
			a3 = p3 / v3
			write_ramdisk(a3, 'bezuga3')

		# Grid total energy sums
		try:
			response = requests.get(
				'http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/Grid.+ActiveEnergy', timeout=1).json()
		except:
			traceback.print_exc()

		# ATTENTION: Even though the ramdisk file name contains "k"wh, it seems the values must be given in Watthours (Wh)
		for singleValue in response:
			address = singleValue['address']
			if (address == '_sum/GridBuyActiveEnergy'):
				energy = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
				write_ramdisk(energy, 'bezugkwh')
			elif (address == '_sum/GridSellActiveEnergy'):
				energy = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
				write_ramdisk(energy, 'einspeisungkwh')
	except ValueError:  # includes simplejson.decoder.JSONDecodeError
		# nicht alle FEMS-Module unterstützen Regex-Requests
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/ActivePower', 'wattbezug')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/GridBuyActiveEnergy', 'bezugkwh')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/GridSellActiveEnergy', 'einspeisungkwh')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/VoltageL1', 'evuv1')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/VoltageL2', 'evuv2')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/VoltageL3', 'evuv3')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/CurrentL1', 'bezuga1')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/CurrentL2', 'bezuga2')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/CurrentL3', 'bezuga3')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/ActivePowerL1', 'bezugw1')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/ActivePowerL2', 'bezugw2')
		get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/ActivePowerL3', 'bezugw3')


def main(argv: List[str]):
	run_using_positional_cli_args(update, argv)

# example FEMS response on rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)
# [
#     {
#         "address": "meter0/ActivePowerL3",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "Negative values for Consumption; positive for Production",
#         "unit": "W",
#         "value": -547
#     },
#     {
#         "address": "meter0/ActivePower",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "W",
#         "value": -44
#     },
#     {
#         "address": "meter0/ActivePowerL1",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "Negative values for Consumption; positive for Production",
#         "unit": "W",
#         "value": 0
#     },
#     {
#         "address": "meter0/ActivePowerL2",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "Negative values for Consumption; positive for Production",
#         "unit": "W",
#         "value": 503
#     },
#     {
#         "address": "meter0/VoltageL1",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "mV",
#         "value": 229800
#     },
#     {
#         "address": "meter0/VoltageL2",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "mV",
#         "value": 230400
#     },
#     {
#         "address": "meter0/VoltageL3",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "mV",
#         "value": 232900
#     },
#     {
#         "address": "meter0/Frequency",
#         "type": "INTEGER",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "mHz",
#         "value": 50000
#     }
# ]

# example FEMS response on channel/_sum/Grid.+ActiveEnergy
# [
#     {
#         "address": "_sum/GridSellActiveEnergy",
#         "type": "LONG",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "Wh",
#         "value": 179771
#     },
#     {
#         "address": "_sum/GridBuyActiveEnergy",
#         "type": "LONG",
#         "accessMode": "RO",
#         "text": "",
#         "unit": "Wh",
#         "value": 2183647
#     }
# ]
