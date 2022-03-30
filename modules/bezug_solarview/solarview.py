#!/usr/bin/env python3

#
# OpenWB-Modul für die Anbindung von SolarView über den integrierten TCP-Server
# Details zur API: https://solarview.info/solarview-fb_Installieren.pdf
#
from typing import List, Optional
import logging
import socket
import sys
import traceback

from helpermodules.cli import run_using_positional_cli_args


log = logging.getLogger("Solarview EVU")

def write_value(value, file):
    try:
        with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
            f.write(str(value))
    except:
        traceback.print_exc()


def request(solarview_hostname: str, solarview_port: int, solarview_timeout: int, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(solarview_timeout)
            s.connect((solarview_hostname, solarview_port))
            s.sendall(command.encode("ascii"))
            response = s.recv(1024)
            message = response[:-2]
            checksum = int.from_bytes(response[-1:], "big", signed=False)
            calculated_checksum = int(sum(message)) % 256
            log.debug("message: " + str(message))
            log.debug("checksum: " + str(checksum) + " calculated: " + str(calculated_checksum))
    except Exception as e:
        log.debug("Error: request to SolarView failed. Details: return-code: " + str(e) + ", host: " + str(solarview_hostname) +
            ", port: " + str(solarview_port) + ", timeout: " + str(solarview_timeout))
        traceback.print_exc()
        sys.exit(0)

    log.debug("Raw response: "+response)
    #
    # Format:    {WR,Tag,Monat,Jahr,Stunde,Minute,KDY,KMT,KYR,KT0,PAC,UDC,IDC,UDCB,IDCB,UDCC,IDCC,UDCD,IDCD,TKK},Checksum
    # Beispiele: {22,09,09,2019,10,37,0001.2,00024,000903,00007817,01365,000,000.0,000,000.0,000,000.0,000,000.0,00},:
    #            {21,09,09,2019,10,37,0002.3,00141,004233,00029525,01365,000,000.0,000,000.0,000,000.0,000,000.0,00},;
    #
    # Bedeutung (siehe SolarView-Dokumentation):
    #  KDY= Tagesertrag (kWh)
    #  KMT= Monatsertrag (kWh)
    #  KYR= Jahresertrag (kWh)
    #  KT0= Gesamtertrag (kWh)
    #  PAC= Generatorleistung in W
    #  UDC, UDCB, UDCC, UDCD= Generator-Spannungen in Volt pro MPP-Tracker
    #  IDC, IDCB, IDCC, IDCD= Generator-Ströme in Ampere pro MPP-Tracker
    #  TKK= Temperatur Wechselrichter

    # Auszug aus der Doku vom 02.12.2020:
    # WR, Tag, Monat, Jahr, Stunde, Minute, KDY, KMT, KYR, KT0,PAC, UDC, IDC, UDCB, IDCB, UDCC, IDCC, UDCD, IDCD, UL1, IL1, UL2, IL2, UL3, IL3, TKK
    # KDY= Tagesertrag (kWh)
    # KMT= Monatsertrag (kWh)
    # KYR= Jahresertrag (kWh)
    # KT0= Gesamtertrag (kWh)
    # PAC= Generatorleistung in W
    # UDC, UDCB, UDCC, UDCD = Generator-Spannungen in Volt pro MPP-Tracker
    # IDC, IDCB, IDCC, IDCD = Generator-Ströme in Ampere pro MPP-Tracker
    # UL1, IL1 = Netzspannung, Netzstrom Phase 1
    # UL2, IL2 = Netzspannung, Netzstrom Phase 2
    # UL3, IL3 = Netzspannung, Netzstrom Phase 3
    # TKK= Temperatur Wechselrichter#

    # Geschweifte Klammern entfernen
    values = message.decode("ascii")[1:-1].split(",")

    # Werte formatiert in Variablen speichern
    id = values[0]
    timestamp = str(values[3]) + "-" + str(values[2]) + "-" + str(values[1]) + " " + str(values[4]) + ":" + str(values[5])
    #  PAC = '-0357' bedeutet: 357 W Bezug, 0 W Einspeisung
    #  PAC =  '0246' bedeutet: 0 W Bezug, 246 W Einspeisung
    power = -1 * int(values[10])
    energy_day = 1000 * float(values[6])
    energy_month = 1000 * int(values[7])
    energy_year = 1000 * int(values[8])
    energy_total = 1000 * int(values[9])
    mpptracker1_voltage = int(values[11])
    mpptracker1_current = round(float(values[12]), 1)
    mpptracker2_voltage = int(values[13])
    mpptracker2_current = round(float(values[14]), 1)
    mpptracker3_voltage = int(values[15])
    mpptracker3_current = round(float(values[16]), 1)
    mpptracker4_voltage = int(values[17])
    mpptracker4_current = round(float(values[18]), 1)
    # Kompatibilität für neue und alte Doku
    try:
        grid1_voltage = int(values[19])
        grid1_current = round(float(values[20]), 1)
        grid2_voltage = int(values[21])
        grid2_current = round(float(values[22]), 1)
        grid3_voltage = int(values[23])
        grid3_current = round(float(values[24]), 1)
        temperature = int(values[25])
    except:
        temperature = int(values[19])

    # Werte ausgeben
    log.debug("ID: "+str(id))
    log.debug("Zeitpunkt: "+str(timestamp))
    log.debug("Temperatur: "+str(temperature)+" °C")
    log.debug("Leistung: "+str(power)+" W")
    log.debug("Energie:")
    log.debug("  Tag:    "+str(energy_day)+" Wh")
    log.debug("  Monat:  "+str(energy_month)+" Wh")
    log.debug("  Jahr:   "+str(energy_year)+" Wh")
    log.debug("  Gesamt: "+str(energy_total)+" Wh")
    log.debug("Generator-MPP-Tracker-1")
    log.debug("  Spannung: "+str(mpptracker1_voltage)+" V")
    log.debug("  Strom:    "+str(mpptracker1_current)+" A")
    log.debug("Generator-MPP-Tracker-2")
    log.debug("  Spannung: "+str(mpptracker2_voltage)+" V")
    log.debug("  Strom:    "+str(mpptracker2_current)+" A")
    log.debug("Generator-MPP-Tracker-3")
    log.debug("  Spannung: "+str(mpptracker3_voltage)+" V")
    log.debug("  Strom:    "+str(mpptracker3_current)+" A")
    log.debug("Generator-MPP-Tracker-4")
    log.debug("  Spannung: "+str(mpptracker4_voltage)+" V")
    log.debug("  Strom:    "+str(mpptracker4_current)+" A")
    log.debug("Netz:")
    log.debug("  Phase 1:")
    log.debug("    Spannung: "+str(grid1_voltage)+" V")
    log.debug("    Strom:    "+str(grid1_current)+" A")
    log.debug("  Phase 2:")
    log.debug("    Spannung: "+str(grid2_voltage)+" V")
    log.debug("    Strom:    "+str(grid2_current)+" A")
    log.debug("  Phase 3:")
    log.debug("    Spannung: "+str(grid3_voltage)+" V")
    log.debug("    Strom:    "+str(grid3_current)+" A")

    # Werte speichern
    if command == '21*':
        write_value(energy_total, "einspeisungkwh")
    elif command == '22*':
        write_value(power, "wattbezug")
        write_value(energy_total, "bezugkwh")
        # Kompatibilität für neue und alte Doku
        try:
            write_value(grid1_current, "bezuga1")
            write_value(grid2_current, "bezuga2")
            write_value(grid3_current, "bezuga3")
            write_value(grid1_voltage, "evuv1")
            write_value(grid2_voltage, "evuv2")
            write_value(grid3_voltage, "evuv3")
        except:
            pass

def update(solarview_hostname: str, solarview_port: Optional[int] = 15000, solarview_timeout: Optional[int] = 1):
    # Checks
    if solarview_hostname == None or solarview_hostname == "":
        log.debug("Missing required variable 'solarview_hostname'")
        sys.exit(1)
    if solarview_port:
        if solarview_port < 1 or solarview_port > 65535:
            log.debug("Invalid value "+str(solarview_port)+" for variable 'solarview_port'")
            sys.exit(1)

    command_bezug = '22*'
    command_einspeisung = '21*'

    request(solarview_hostname, solarview_port, solarview_timeout, command_einspeisung)
    request(solarview_hostname, solarview_port, solarview_timeout, command_bezug)

def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
