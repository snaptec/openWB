#!/usr/bin/env python
import logging
from socketserver import TCPServer
from collections import defaultdict
import struct
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

log_to_stream(level=logging.DEBUG)
data_store = defaultdict(int)
conf.SIGNED_VALUES = True
TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('0.0.0.0', 502), RequestHandler)


def form_sint32(value, startreg):
    secondreg = startreg + 1
    try:
        with open('/var/www/html/openWB/ramdisk/' + value, 'r') as var:
            readvar = int(float(var.read()))
        print(str(readvar))
        binary32 = struct.pack('>l', readvar)
        high_byte, low_byte = struct.unpack('>hh', binary32)
        data_store[startreg] = high_byte
        data_store[secondreg] = low_byte
    except:
        data_store[startreg] = -1
        data_store[secondreg] = -1


def form_lpkwhsint32(value, startreg):
    secondreg = startreg + 1
    try:
        with open('/var/www/html/openWB/ramdisk/' + value, 'r') as var:
            readvar = int(float(var.read())*1000)
        binary32 = struct.pack('>l', readvar)
        high_byte, low_byte = struct.unpack('>hh', binary32)
        data_store[startreg] = high_byte
        data_store[secondreg] = low_byte
    except:
        data_store[startreg] = -1
        data_store[secondreg] = -1


def form_sint16(value, startreg):
    try:
        with open('/var/www/html/openWB/ramdisk/' + value, 'r') as var:
            readvar = int(float(var.read()))
        if (readvar > 32767 or readvar < -32768):
            raise Exception("Number to big")
        data_store[startreg] = readvar
    except:
        data_store[startreg] = -1


def form_100sint16(value, startreg):
    try:
        with open('/var/www/html/openWB/ramdisk/' + value, 'r') as var:
            readvar = int(float(var.read())*100)
        if (readvar > 32767 or readvar < -32768):
            print("raised")
            raise Exception("Number to big")
        data_store[startreg] = readvar
    except:
        data_store[startreg] = -1


def get_pos(number, n):
    return number // 10**n % 10


@app.route(slave_ids=[1], function_codes=[3, 4], addresses=list(range(0, 32000)))
def read_data_store(slave_id, function_code, address):
    """" Return value of address. """
    if (address == 110):
        form_sint16("rseaktiv", address)
    elif (address == 111):
        form_sint16("ConfiguredChargePoints", address)
    elif (address == 300):
        form_sint32("wattbezug", address)
    elif (address == 302):
        form_100sint16("bezuga1", address)
    elif (address == 303):
        form_100sint16("bezuga2", address)
    elif (address == 304):
        form_100sint16("bezuga3", address)
    elif (address == 305):
        form_100sint16("evuv1", address)
    elif (address == 306):
        form_100sint16("evuv2", address)
    elif (address == 307):
        form_100sint16("evuv3", address)
    elif (address == 308):
        form_sint32("bezugkwh", address)
    elif (address == 310):
        form_sint32("einspeisungkwh", address)
    elif (address == 400):
        form_sint32("pvallwatt", address)
    elif (address == 402):
        form_sint32("pvallwh", address)
    elif (address == 500):
        form_sint32("speicherleistung", address)
    elif (address == 502):
        form_sint16("speichersoc", address)
    elif (address == 503):
        form_sint32("speicherikwh", address)
    elif (address == 505):
        form_sint32("speicherekwh", address)
    elif (address > 10099):
        chargepoint = get_pos(address, 2)
        askedvalue = int(str(address)[-2:])
        if (askedvalue == 00):
            if (chargepoint == 1):
                form_sint32("llaktuell", address)
            elif (chargepoint == 2):
                form_sint32("llaktuells1", address)
            elif (chargepoint == 3):
                form_sint32("llaktuells2", address)
            else:
                form_sint32("llaktuelllp"+str(chargepoint), address)
        if (askedvalue == 2):
            if (chargepoint == 1):
                form_lpkwhsint32("llkwh", address)
            elif (chargepoint == 2):
                form_lpkwhsint32("llkwhs1", address)
            elif (chargepoint == 3):
                form_lpkwhsint32("llkwhs2", address)
            else:
                form_lpkwhsint32("llkwhlp"+str(chargepoint), address)
        if (askedvalue == 4):
            if (chargepoint == 1):
                form_100sint16("llv1", address)
            elif (chargepoint == 2):
                form_100sint16("llvs11", address)
            elif (chargepoint == 3):
                form_100sint16("llvs21", address)
            else:
                form_100sint16("llv1lp"+str(chargepoint), address)
        if (askedvalue == 5):
            if (chargepoint == 1):
                form_100sint16("llv2", address)
            elif (chargepoint == 2):
                form_100sint16("llvs12", address)
            elif (chargepoint == 3):
                form_100sint16("llvs22", address)
            else:
                form_100sint16("llv2lp"+str(chargepoint), address)
        if (askedvalue == 6):
            if (chargepoint == 1):
                form_100sint16("llv3", address)
            elif (chargepoint == 2):
                form_100sint16("llvs13", address)
            elif (chargepoint == 3):
                form_100sint16("llvs23", address)
            else:
                form_100sint16("llv3lp"+str(chargepoint), address)
        if (askedvalue == 7):
            if (chargepoint == 1):
                form_100sint16("lla1", address)
            elif (chargepoint == 2):
                form_100sint16("llas11", address)
            elif (chargepoint == 3):
                form_100sint16("llas21", address)
            else:
                form_100sint16("lla1lp"+str(chargepoint), address)
        if (askedvalue == 8):
            if (chargepoint == 1):
                form_100sint16("lla2", address)
            elif (chargepoint == 2):
                form_100sint16("llas12", address)
            elif (chargepoint == 3):
                form_100sint16("llas22", address)
            else:
                form_100sint16("lla2lp"+str(chargepoint), address)
        if (askedvalue == 9):
            if (chargepoint == 1):
                form_100sint16("lla3", address)
            elif (chargepoint == 2):
                form_100sint16("llas13", address)
            elif (chargepoint == 3):
                form_100sint16("llas23", address)
            else:
                form_100sint16("lla3lp"+str(chargepoint), address)
        if (askedvalue == 10):
            if (chargepoint == 1):
                data_store[address] = 1
            elif (chargepoint == 2):
                form_sint16("mqttlastmanagement", address)
            elif (chargepoint == 3):
                form_sint16("mqttlastmanagements2", address)
            else:
                form_sint16("mqttlastmanagementlp"+str(chargepoint), address)
        if (askedvalue == 11):
            form_sint16("lp"+str(chargepoint)+"enabled", address)
        if (askedvalue == 12):
            form_sint32("rfidlp"+str(chargepoint), address)
        if (askedvalue == 14):
            if (chargepoint == 1):
                form_sint16("plugstat", address)
            elif (chargepoint == 2):
                form_sint16("plugstats1", address)
            elif (chargepoint == 3):
                form_sint16("plugstatlp3", address)
            else:
                form_sint16("plugstatlp"+str(chargepoint), address)
        if (askedvalue == 15):
            if (chargepoint == 1):
                form_sint16("chargestat", address)
            elif (chargepoint == 2):
                form_sint16("chargestats1", address)
            elif (chargepoint == 3):
                form_sint16("chargestatlp3", address)
            else:
                form_sint16("chargestatlp"+str(chargepoint), address)
        if (askedvalue == 16):
            if (chargepoint == 1):
                form_sint16("llsoll", address)
            elif (chargepoint == 2):
                form_sint16("llsolls1", address)
            elif (chargepoint == 3):
                form_sint16("llsolls2", address)
            else:
                form_sint16("llsolllp"+str(chargepoint), address)
    elif (address == 19916):
        form_sint16("llsolllp8", address)

    return data_store[address]


def write_ramdisk(name, value):
    f = open('/var/www/html/openWB/ramdisk/' + str(name), 'w')
    f.write(str(value))
    f.close()


@app.route(slave_ids=[1], function_codes=[6, 16], addresses=list(range(0, 32000)))
def write_data_store(slave_id, function_code, address, value):
    """" Set value for address. """
    if (address == 112):
        write_ramdisk("lademodus", value)
    elif (address == 113):
        write_ramdisk("readtag", value)
    elif (address > 10099):
        chargepoint = get_pos(address, 2)
        askedvalue = int(str(address)[-2:])
        if (askedvalue == 51):
            write_ramdisk("lp"+str(chargepoint)+"enabled", value)
        if (askedvalue == 52):
            if (value >= 6 and value <= 32):
                write_ramdisk("lp"+str(chargepoint)+"sofortll", value)


if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
