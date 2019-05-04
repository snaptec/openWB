#!/usr/bin/python
# coding: utf8

#########################################################
#
# liest aus Wechselrichter Kostal Plenticore Register
# zu PV-Statistik und berechnet PV-Leistung, Speicherleistung
# unter Beachtung angeschlossener Batterie falls vorhanden
#
# 2019 Kevin Wieland, Michael Ortenstein
# This file is part of openWB
#
#########################################################

import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
ipaddress = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient

# Plenticore als Modbus Client einrichhten
client = ModbusTcpClient(ipaddress, port=1502)

# dann zunächst alle relevanten Register auslesen:

# Plenticore Register 100: Total_DC_power [W]
# ist die gesamte DC-seitige Leistung, einschl. ggf.
# angeschlossener Batterie
reg_100 = client.read_holding_registers(100,2,unit=71)
# Plenticore Register 582: Actual_batt_ch_disch_power [W]
# ist Lade-/Entladeleistung des angeschlossenen Speichers
# {charge=negativ, discharge=positiv}
reg_582 = client.read_holding_registers(582,1,unit=71)
# Plenticore Register 320: Total_yield [Wh]
# ist PV Gesamt-Ertrag
reg_320 = client.read_holding_registers(320,2,unit=71)
# Plenticore Register 575: Inverter_generation_power_actual [W]
# ist AC-Leistungsabgabe des Wechselrichters
reg_575 = client.read_holding_registers(575,1,unit=71)
# Plenticore Register 514: Battery_actual_SOC [%]
# ist Ladestand des Speichers
reg_514 = client.read_holding_registers(514,1,unit=71)
# Strom auf Phasen 1-3 EVU aus Kostal Plenticore lesen
# Wechselrichter bekommt Daten von Energy Manager EM300
# Phase 1
# Plenticore Register 222: Current_phase_1_(powermeter) [A]
reg_222 = client.read_holding_registers(222,2,unit=71)
# Phase 2
# Plenticore Register 232: Current_phase_2_(powermeter) [A]
reg_232 = client.read_holding_registers(232,2,unit=71)
# Phase 3
# Plenticore Register 242: Current_phase_3_(powermeter) [A]
reg_242 = client.read_holding_registers(242,2,unit=71)
# Leistung EVU
# Plenticore Register 252: Total_active_power_(powermeter) [W]
# Sensorposition 1 (Hausanschluss): (+)Hausverbrauch (-)Erzeugung
reg_252 = client.read_holding_registers(252,2,unit=71)
#//TODO: weitere Register später hinzufügen für PV-Statistik

# ausgelesene Register dekodieren
FRegister_100 = BinaryPayloadDecoder.fromRegisters(reg_100.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_582 = BinaryPayloadDecoder.fromRegisters(reg_582.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_320 = BinaryPayloadDecoder.fromRegisters(reg_320.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_575 = BinaryPayloadDecoder.fromRegisters(reg_575.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_514 = BinaryPayloadDecoder.fromRegisters(reg_514.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_222 = BinaryPayloadDecoder.fromRegisters(reg_222.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_232 = BinaryPayloadDecoder.fromRegisters(reg_232.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_242 = BinaryPayloadDecoder.fromRegisters(reg_242.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_252 = BinaryPayloadDecoder.fromRegisters(reg_252.registers, byteorder=Endian.Big, wordorder=Endian.Little)

# dekodierte Register in entsprechende Typen umwandeln
Total_DC_power = int(FRegister_100.decode_32bit_float())
Actual_batt_ch_disch_power = int(FRegister_582.decode_16bit_int())
Total_yield = int(FRegister_320.decode_32bit_float())
Inverter_generation_power_actual = int(FRegister_575.decode_16bit_int())
Battery_actual_SOC = int(FRegister_514.decode_16bit_int())
Current_phase_1_powermeter = round(FRegister_222.decode_32bit_float(),2)
Current_phase_2_powermeter = round(FRegister_232.decode_32bit_float(),2)
Current_phase_3_powermeter = round(FRegister_242.decode_32bit_float(),2)
Total_active_power_powermeter = int(FRegister_252.decode_32bit_float())

# AC-Leistung der PV-Module bestimmen
# da ggf. Batterie DC-seitig in Total_DC_power enthalten ist,
# muss deren Lade-/Entladeleistung mitbetrachtet werden,
# wenn man die Leistung der PV-Module bestimmen möchte
# Kostal liefert nur DC-Werte, also DC-Leistung berechnen
PV_power_dc = (Total_DC_power - Actual_batt_ch_disch_power)
# schauen, ob überhaupt PV-Leistung erzeugt wird
# PV-Anlage kann nichts verbrauchen, also ggf. Register-/Rundungsfehler korrigieren
if PV_power_dc < 0:
    PV_power_ac = 0
else:
    # wird PV-DC-Leistung erzeugt, müssen die Wandlungsverluste betrachtet werden
    # Kostal liefert nur DC-seitige Werte
    if Actual_batt_ch_disch_power < 0:
        # wird die Batterie geladen, ist die PV-Leistung die Summe aus
        # verlustbehafteter AC-Leistungsabgabe des WR und der DC-Ladeleistung,
        # die Wandlungsverluste werden also nur in der PV-Leistung ersichtlich
        PV_power_ac = Inverter_generation_power_actual - Actual_batt_ch_disch_power
    else:
        # wird die Batterie entladen, werden die Wandlungsverluste anteilig an der
        # DC-Leistung auf PV und Batterie verteilt
        PV_power_ac = int((PV_power_dc / float(Total_DC_power)) * Inverter_generation_power_actual)
        Actual_batt_ch_disch_power = Inverter_generation_power_actual - PV_power_ac

# Bezug berechnen je nach Position des Energy Managers
Bezug = Total_active_power_powermeter
#//TODO: hier muss noch der Wert aus den Settings für die if-Prüfung gelesen werden
#if int(sys.argv[2]) == 0:
#    Bezug = Bezug - PV_power_ac

# Erzeugung wird als negativer Wert weiter verarbeitet
PV_power = PV_power_ac * -1
Actual_batt_ch_disch_power = Actual_batt_ch_disch_power * -1

# und zur Weiterverarbeitung alle Werte in die ramdisk
# berechnete PV-AC-Leistung
with open('/var/www/html/openWB/ramdisk/pvwatt', 'w') as f:
    f.write(str(PV_power))
# Gesamtertrag in Wattstunden
with open('/var/www/html/openWB/ramdisk/pvkwh', 'w') as f:
    f.write(str(Total_yield))
# Gesamtertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/pvkwhk', 'w') as f:
    f.write(str(Total_yield / 1000))

# Nachfolgende Werte nur in temporäre ramdisk, da die Module
# Speicher und Bezug für die globalen Variablen zuständig sind
# und dort die Übernahme in die entsprechende ramdisk erfolgt
# Speicherleistung
with open('/var/www/html/openWB/ramdisk/temp_speicherleistung', 'w') as f:
    f.write(str(Actual_batt_ch_disch_power))
# Speicher Ladestand
with open('/var/www/html/openWB/ramdisk/temp_speichersoc', 'w') as f:
    f.write(str(Battery_actual_SOC))
# Bezug EVU
with open('/var/www/html/openWB/ramdisk/temp_wattbezug', 'w') as f:
    f.write(str(Bezug))
#Bezug Phase 1
with open('/var/www/html/openWB/ramdisk/temp_bezuga1', 'w') as f:
    f.write(str(Current_phase_1_powermeter))
#Bezug Phase 2
with open('/var/www/html/openWB/ramdisk/temp_bezuga2', 'w') as f:
    f.write(str(Current_phase_2_powermeter))
#Bezug Phase 3
with open('/var/www/html/openWB/ramdisk/temp_bezuga3', 'w') as f:
    f.write(str(Current_phase_3_powermeter))
