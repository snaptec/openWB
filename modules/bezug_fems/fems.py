#!/usr/bin/env python3

import logging
from typing import List

import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("FEMS")


def write_ramdisk(val, file):
    try:
        f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
        f.write(str(val))
        f.close()
    except:
        traceback.print_exc()


def get_value(url, file):
    try:
        response = requests.get(url, timeout=2).json()
        val = response["value"]
        f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
        f.write(str(val))
        f.close()
    except:
        traceback.print_exc()


def update(password: str, ip_address: str):
    try:
        # Grid meter values
        response = requests.get('http://x:' + password + '@' + ip_address +
                                ':8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)', timeout=1).json()

        v1, v2, v3 = 0, 0, 0
        p1, p2, p3 = 0, 0, 0
        for singleValue in response:
            address = singleValue['address']
            if (address == 'meter0/Frequency'):
                write_ramdisk(singleValue['value'], 'evuhz')
            elif (address == 'meter0/ActivePower'):
                write_ramdisk(singleValue['value'], 'wattbezug')
            elif (address == 'meter0/ActivePowerL1'):
                write_ramdisk(singleValue['value'], 'bezugw1')
                p1 = singleValue['value']
            elif (address == 'meter0/ActivePowerL2'):
                write_ramdisk(singleValue['value'], 'bezugw2')
                p2 = singleValue['value']
            elif (address == 'meter0/ActivePowerL3'):
                write_ramdisk(singleValue['value'], 'bezugw3')
                p3 = singleValue['value']
            elif (address == 'meter0/VoltageL1'):
                write_ramdisk(singleValue['value'], 'evuv1')
                v1 = singleValue['value']
            elif (address == 'meter0/VoltageL2'):
                write_ramdisk(singleValue['value'], 'evuv2')
                v2 = singleValue['value']
            elif (address == 'meter0/VoltageL3'):
                write_ramdisk(singleValue['value'], 'evuv3')
                v3 = singleValue['value']

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

        for singleValue in response:
            address = singleValue['address']
            if (address == '_sum/GridBuyActiveEnergy'):
                write_ramdisk(singleValue['value'], 'bezugkwh')
            elif (address == '_sum/GridSellActiveEnergy'):
                write_ramdisk(singleValue['value'], 'einspeisungkwh')
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
