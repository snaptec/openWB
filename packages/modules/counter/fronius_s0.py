#!/usr/bin/env python3
# coding: utf8

import re
import requests
import sys

if __name__ == "__main__":
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import set_values
else:
    from ...helpermodules import log
    from . import set_values


class module(set_values.set_values):
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        try:
            # Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
            # Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv)
            # Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
            # Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen
            try:
                response = requests.get('http://'+self.data["config"]["ip_address"]+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', timeout=5).json()
                if self.data["config"]["primo"] == str(1):
                    power_all = int(response["Body"]["Data"]["Site"]["P_Grid"])
                else:
                    power_all = int(response["Body"]["Data"]["PowerReal_P_Sum"])

                # f = open( "ramdisk/pvwatt" , 'r')
                # pvwatt =int(f.read())
                # f.close()
                # wattb=pvwatt + power_all

                # wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
                regex = '^[0-9]+$'
                if re.search(regex, str(power_all)) == None:
                    power_all = 0
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_all = 0

            # Summe der vom Netz bezogene Energie total in Wh
            # nur für Smartmeter  im Einspeisepunkt!
            # bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
            params = (('Scope', 'System'),)

            kwhtmp = requests.get('http://'+self.data["config"]["ip_address"]+'/solar_api/v1/GetMeterRealtimeData.cgi', params=params, timeout=5).json()
            # jq-Funktion funktioniert hier leider nicht,  wegen "0" als Bezeichnung
            try:
                for location in kwhtmp["Body"]["Data"]:
                    imported = str(kwhtmp["Body"]["Data"][location]["EnergyReal_WAC_Minus_Absolute"])
            except:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                imported = 0
            imported = imported.replace(" ", "")
            imported = imported.replace('\"', "")
            imported = imported.replace(':', "")
            imported = imported.replace('}', "")
            imported = imported.replace('\n', "")

            # Eingespeiste Energie total in Wh (für Smartmeter im Einspeisepunkt)
            # bei Smartmeter im Verbrauchsweig immer 0
            try:
                for location in kwhtmp["Body"]["Data"]:
                    exported = str(kwhtmp["Body"]["Data"][location]["EnergyReal_WAC_Plus_Absolute"])
            except:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                exported = 0
            exported = exported.split(",")[0]
            exported = exported.replace(" ", "")
            exported = exported.replace('\"', "")
            exported = exported.replace(':', "")

            values = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [imported, exported],
                      power_all,
                      50]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        primo = str(sys.argv[1])
        mod.data["config"]["primo"] = primo
        ip_address = str(sys.argv[2])
        mod.data["config"]["ip_address"] = ip_address

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module fronius_s0 primo: ' + str(primo))
            log.log_1_9('Counter-Module fronius_s0 ip_address: ' + str(ip_address))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
