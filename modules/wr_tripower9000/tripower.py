#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import struct
import traceback
from pymodbus.client.sync import ModbusTcpClient

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wrsmawebbox = int(sys.argv[1])
tri9000ip = str(sys.argv[2])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter Tripower Webbox: ' + str(wrsmawebbox))
    DebugLog('Wechselrichter Tripower IP: ' + tri9000ip)

if wrsmawebbox == 1:
    headers = {'Content-Type': 'application/json', }
    data = {'RPC': '{"version": "1.0","proc": "GetPlantOverview","id": "1","format": "JSON"}'}
    response = requests.post('http://'+tri9000ip+'/rpc', headers=headers, data=data, timeout=3).json()
    rekwh = '^[-+]?[0-9]+\.?[0-9]*$'
    try:
        pvwatt = int(response["result"]["overview"][0]["value"])
        pvwatt = pvwatt * -1
        if re.search(rekwh, pvwatt):
            if Debug >= 1:
                DebugLog('WR Leistung: ' + str(pvwatt))
            with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
                f.write(str(pvwatt))
    except:
        traceback.print_exc()
        exit(1)

    try:
        pvkwh = response["result"]["overview"][2]["value"]
        pvwh = int(pvkwh) * 1000
        if re.search(rekwh, pvwh) != None:
            if Debug >= 1:
                DebugLog('WR Energie: ' + str(pvkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                f.write(str(pvwh))
    except:
        traceback.print_exc()
        exit(1)
else:

    power = 0
    counter = 0

    # Länge von sys.argv = Dateiname + Webbox + IP-Adressen
    for i in len(sys.argv)-2:
        try:
            ipaddress = str(sys.argv[i+2])
            if Debug >= 2:
                DebugLog('Wechselrichter Tripower IP'+str(i+2)+': ' + ipaddress)
            client = ModbusTcpClient(ipaddress, port=502)

            # pv watt
            resp = client.read_holding_registers(30775, 2, unit=3)
            value1 = resp.registers[0]
            value2 = resp.registers[1]
            all = format(value1, '04x') + format(value2, '04x')
            power = power + int(struct.unpack('>i', all.decode('hex'))[0])

            # pv Wh
            resp = client.read_holding_registers(30529, 2, unit=3)
            value1 = resp.registers[0]
            value2 = resp.registers[1]
            all = format(value1, '04x') + format(value2, '04x')
            counter = counter + int(struct.unpack('>i', all.decode('hex'))[0])
        except:
            traceback.print_exc()
            exit(1)

    if power < 0:
        power = 0
    power = power * -1
    if Debug >= 1:
        DebugLog('WR Leistung: ' + str(power))
    f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
    f.write(str(power))
    f.close()

    if Debug >= 1:
        DebugLog('WR Energie: ' + str(counter))
    f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
    f.write(str(counter))
    f.close()


exit(0)
