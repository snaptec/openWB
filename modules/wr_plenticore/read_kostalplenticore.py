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
from pymodbus.client.sync import ModbusTcpClient
# beide übergebene IP-Adressen auslesen
ipaddress = str(sys.argv[1])
ipaddress2 = str(sys.argv[2])
boolspeicher = int(sys.argv[3])

# Plenticore als Modbus Client einrichhten
client = ModbusTcpClient(ipaddress, port=1502)
if ipaddress2 != "none":
    client2 = ModbusTcpClient(ipaddress2, port=1502)
else:
    # kein 2. WR, also alle Werte mit 0 initialisieren da später
    # keine Berechnung aber Verwendung in Summenbildung und Logfiles
    Total_DC_power2 = 0
    Actual_batt_ch_disch_power2 = 0
    Total_yield2 = 0
    Daily_yield2 = 0
    Yearly_yield2 = 0
    Monthly_yield2 = 0
    Inverter_generation_power_actual2 = 0
    Battery_actual_SOC2 = 0

# dann zunächst alle relevanten Register aus WR 1 auslesen:
# Plenticore Register 100: Total_DC_power [W]
# ist die gesamte DC-seitige Leistung, einschl. ggf.
# angeschlossener Batterie
reg_100 = client.read_holding_registers(100,2,unit=71)
# Plenticore Register 582: Actual_batt_ch_disch_power [W]
# ist Lade-/Entladeleistung des angeschlossenen Speichers
# {charge=negativ, discharge=positiv}
reg_582 = client.read_holding_registers(582,1,unit=71)
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
# Sensorposition 2 (EVU Anschlusspunkt): (+)Bezug (-)Einspeisung
reg_252 = client.read_holding_registers(252,2,unit=71)
# Frequenz EVU
# Plenticore Register 220: Frequency_(powermeter) [Hz]
reg_220 = client.read_holding_registers(220,2,unit=71)
# Leistung auf Phasen 1-3 EVU aus Kostal Plenticore lesen
# Wechselrichter bekommt Daten von Energy Manager EM300
# Phase 1
# Plenticore Register 224: Active_power_phase_1_(powermeter) [W]
reg_224 = client.read_holding_registers(224,2,unit=71)
# Phase 2
# Plenticore Register 234: Active_power_phase_2_(powermeter) [W]
reg_234 = client.read_holding_registers(234,2,unit=71)
# Phase 3
# Plenticore Register 244: Active_power_phase_3_(powermeter) [A]
reg_244 = client.read_holding_registers(244,2,unit=71)
# Spannung auf Phasen 1-3 EVU aus Kostal Plenticore lesen
# Wechselrichter bekommt Daten von Energy Manager EM300
# Phase 1
# Plenticore Register 230: Voltage_phase_1_(powermeter) [V]
reg_230 = client.read_holding_registers(230,2,unit=71)
# Phase 2
# Plenticore Register 240: Voltage_phase_2_(powermeter) [V]
reg_240 = client.read_holding_registers(240,2,unit=71)
# Phase 3
# Plenticore Register 250: Voltage_phase_3_(powermeter) [V]
reg_250 = client.read_holding_registers(250,2,unit=71)
# Plenticore Register 150: Actual_cos_phi []
# ist Wirkfaktor
reg_150 = client.read_holding_registers(150,2,unit=71)
# Plenticore Register 320: Total_yield [Wh]
# ist PV Gesamtertrag
reg_320 = client.read_holding_registers(320,2,unit=71)
# Plenticore Register 322: Daily_yield [Wh]
# ist PV Tagesertrag
reg_322 = client.read_holding_registers(322,2,unit=71)
# Plenticore Register 324: Yearly_yield [Wh]
# ist PV Jahresertrag
reg_324 = client.read_holding_registers(324,2,unit=71)
# Plenticore Register 326: Monthly_yield [Wh]
# ist PV Monatsertrag
reg_326 = client.read_holding_registers(326,2,unit=71)

# ggf. WR 2 auslesen, es werden keine Register für Daten vom EM300/KSEM
# gelesen, diese kommen ausschließlich über den WR 1
if ipaddress2 != "none":
    # Plenticore Register 100: Total_DC_power [W]
    # ist die gesamte DC-seitige Leistung, einschl. ggf.
    # angeschlossener Batterie
    reg2_100 = client2.read_holding_registers(100,2,unit=71)
    # Plenticore Register 582: Actual_batt_ch_disch_power [W]
    # ist Lade-/Entladeleistung des angeschlossenen Speichers
    # {charge=negativ, discharge=positiv}
    reg2_582 = client2.read_holding_registers(582,1,unit=71)
    # Plenticore Register 575: Inverter_generation_power_actual [W]
    # ist AC-Leistungsabgabe des Wechselrichters
    reg2_575 = client2.read_holding_registers(575,1,unit=71)
    # Plenticore Register 514: Battery_actual_SOC [%]
    # ist Ladestand des Speichers
    reg2_514 = client2.read_holding_registers(514,1,unit=71)
    # Plenticore Register 320: Total_yield [Wh]
    # ist PV Gesamtertrag
    reg2_320 = client2.read_holding_registers(320,2,unit=71)
    # Plenticore Register 322: Daily_yield [Wh]
    # ist PV Tagesertrag
    reg2_322 = client2.read_holding_registers(322,2,unit=71)
    # Plenticore Register 324: Yearly_yield [Wh]
    # ist PV Jahresertrag
    reg2_324 = client2.read_holding_registers(324,2,unit=71)
    # Plenticore Register 326: Monthly_yield [Wh]
    # ist PV Monatsertrag
    reg2_326 = client2.read_holding_registers(326,2,unit=71)

# ausgelesene Register WR 1 dekodieren
FRegister_100 = BinaryPayloadDecoder.fromRegisters(reg_100.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_150 = BinaryPayloadDecoder.fromRegisters(reg_150.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_220 = BinaryPayloadDecoder.fromRegisters(reg_220.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_222 = BinaryPayloadDecoder.fromRegisters(reg_222.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_224 = BinaryPayloadDecoder.fromRegisters(reg_224.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_230 = BinaryPayloadDecoder.fromRegisters(reg_230.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_232 = BinaryPayloadDecoder.fromRegisters(reg_232.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_234 = BinaryPayloadDecoder.fromRegisters(reg_234.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_240 = BinaryPayloadDecoder.fromRegisters(reg_240.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_242 = BinaryPayloadDecoder.fromRegisters(reg_242.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_244 = BinaryPayloadDecoder.fromRegisters(reg_244.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_250 = BinaryPayloadDecoder.fromRegisters(reg_250.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_252 = BinaryPayloadDecoder.fromRegisters(reg_252.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_320 = BinaryPayloadDecoder.fromRegisters(reg_320.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_322 = BinaryPayloadDecoder.fromRegisters(reg_322.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_324 = BinaryPayloadDecoder.fromRegisters(reg_324.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_326 = BinaryPayloadDecoder.fromRegisters(reg_326.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_514 = BinaryPayloadDecoder.fromRegisters(reg_514.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_575 = BinaryPayloadDecoder.fromRegisters(reg_575.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_582 = BinaryPayloadDecoder.fromRegisters(reg_582.registers, byteorder=Endian.Big, wordorder=Endian.Little)

# ggf. ausgelesene Register WR 2 dekodieren
if ipaddress2 != "none":
    FRegister2_100 = BinaryPayloadDecoder.fromRegisters(reg2_100.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_320 = BinaryPayloadDecoder.fromRegisters(reg2_320.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_322 = BinaryPayloadDecoder.fromRegisters(reg2_322.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_324 = BinaryPayloadDecoder.fromRegisters(reg2_324.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_326 = BinaryPayloadDecoder.fromRegisters(reg2_326.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_514 = BinaryPayloadDecoder.fromRegisters(reg2_514.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_575 = BinaryPayloadDecoder.fromRegisters(reg2_575.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    FRegister2_582 = BinaryPayloadDecoder.fromRegisters(reg2_582.registers, byteorder=Endian.Big, wordorder=Endian.Little)

# dekodierte Register WR 1 in entsprechende Typen umwandeln
Total_DC_power1 = int(FRegister_100.decode_32bit_float())
Actual_batt_ch_disch_power1 = int(FRegister_582.decode_16bit_int())
Total_yield1 = int(FRegister_320.decode_32bit_float())
Daily_yield1 = round((FRegister_322.decode_32bit_float()/1000),2)
Yearly_yield1 = round((FRegister_324.decode_32bit_float()/1000),2)
Monthly_yield1 = round((FRegister_326.decode_32bit_float()/1000),2)
Inverter_generation_power_actual1 = int(FRegister_575.decode_16bit_int())
Battery_actual_SOC1 = int(FRegister_514.decode_16bit_int())
# Werte aus EM300/KSEM
Current_phase_1_powermeter = round(FRegister_222.decode_32bit_float(),2)
Current_phase_2_powermeter = round(FRegister_232.decode_32bit_float(),2)
Current_phase_3_powermeter = round(FRegister_242.decode_32bit_float(),2)
Total_active_power_powermeter = int(FRegister_252.decode_32bit_float())
Frequency_powermeter = round(FRegister_220.decode_32bit_float(),2)
Active_power_phase_1_powermeter = round(FRegister_224.decode_32bit_float(),2)
Active_power_phase_2_powermeter = round(FRegister_234.decode_32bit_float(),2)
Active_power_phase_3_powermeter = round(FRegister_244.decode_32bit_float(),2)
Voltage_phase_1_powermeter = round(FRegister_230.decode_32bit_float(),2)
Voltage_phase_2_powermeter = round(FRegister_240.decode_32bit_float(),2)
Voltage_phase_3_powermeter = round(FRegister_250.decode_32bit_float(),2)
Actual_cos_phi = round(FRegister_150.decode_32bit_float(),3)

# ggf. dekodierte Register WR 2 in entsprechende Typen umwandeln
if ipaddress2 != "none":
    Total_DC_power2 = int(FRegister2_100.decode_32bit_float())
    Actual_batt_ch_disch_power2 = int(FRegister2_582.decode_16bit_int())
    Total_yield2 = int(FRegister2_320.decode_32bit_float())
    Daily_yield2 = round((FRegister2_322.decode_32bit_float()/1000),2)
    Yearly_yield2 = round((FRegister2_324.decode_32bit_float()/1000),2)
    Monthly_yield2 = round((FRegister2_326.decode_32bit_float()/1000),2)
    Inverter_generation_power_actual2 = int(FRegister2_575.decode_16bit_int())
    Battery_actual_SOC2 = int(FRegister2_514.decode_16bit_int())

# AC-Leistung der PV-Module/des Speichers für WR 1 bestimmen
# da ggf. Batterie DC-seitig in Total_DC_power enthalten ist,
# muss deren Lade-/Entladeleistung mitbetrachtet werden,
# wenn man die AC-Leistung der PV-Module und des Speichers bestimmen möchte
# Kostal liefert nur DC-Werte, also DC-Leistung berechnen
PV_power_dc1 = (Total_DC_power1 - Actual_batt_ch_disch_power1)
# schauen, ob überhaupt PV-Leistung erzeugt wird
if PV_power_dc1 < 0:
    # PV-Anlage kann nichts verbrauchen, also ggf. Register-/Rundungsfehler korrigieren
    PV_power_ac1 = 0
else:
    # wird PV-DC-Leistung erzeugt, müssen die Wandlungsverluste betrachtet werden
    # Kostal liefert nur DC-seitige Werte
    # zunächst Annahme, die Batterie wird geladen:
    # die PV-Leistung die Summe aus verlustbehafteter AC-Leistungsabgabe des WR
    # und der DC-Ladeleistung, die Wandlungsverluste werden also nur in der PV-Leistung
    # ersichtlich
    PV_power_ac1 = Inverter_generation_power_actual1 - Actual_batt_ch_disch_power1
    if Actual_batt_ch_disch_power1 > 0 and Total_DC_power1 != 0:
        # wird die Batterie entladen, werden die Wandlungsverluste anteilig an der
        # DC-Leistung auf PV und Batterie verteilt
        # dazu muss der Divisor Total_DC_power != 0 sein
        PV_power_ac1 = int((PV_power_dc1 / float(Total_DC_power1)) * Inverter_generation_power_actual1)
        Actual_batt_ch_disch_power1 = Inverter_generation_power_actual1 - PV_power_ac1

# analog zu WR 1 die AC-Leistung der PV-Module/des Speichers für WR 2 bestimmen
if ipaddress2 != "none":
    PV_power_dc2 = (Total_DC_power2 - Actual_batt_ch_disch_power2)
    # schauen, ob überhaupt PV-Leistung erzeugt wird
    if PV_power_dc2 < 0:
        # PV-Anlage kann nichts verbrauchen, also ggf. Register-/Rundungsfehler korrigieren
        PV_power_ac2 = 0
    else:
        # wird PV-DC-Leistung erzeugt, müssen die Wandlungsverluste betrachtet werden
        # Kostal liefert nur DC-seitige Werte
        # zunächst Annahme, die Batterie wird geladen:
        # die PV-Leistung die Summe aus verlustbehafteter AC-Leistungsabgabe des WR
        # und der DC-Ladeleistung, die Wandlungsverluste werden also nur in der PV-Leistung
        # ersichtlich
        PV_power_ac2 = Inverter_generation_power_actual2 - Actual_batt_ch_disch_power2
        if Actual_batt_ch_disch_power2 > 0 and Total_DC_power2 != 0:
            # wird die Batterie entladen, werden die Wandlungsverluste anteilig an der
            # DC-Leistung auf PV und Batterie verteilt
            # dazu muss der Divisor Total_DC_power != 0 sein
            PV_power_ac2 = int((PV_power_dc2 / float(Total_DC_power2)) * Inverter_generation_power_actual2)
            Actual_batt_ch_disch_power2 = Inverter_generation_power_actual2 - PV_power_ac2
else:
    # kein 2. WR, dann berechnete Werte mit 0 belegen wegen Weiterverwendung
    # in Summenbildung und Logfiles
    PV_power_dc2 = 0
    PV_power_ac2 = 0

# Bezug zunächst nur auslesen, Sensorposition wird im Strombezugsmessmodul betrachtet
Bezug = Total_active_power_powermeter

# Summe der jeweiligen AC-Leistungen bestimmen
PV_power_total = PV_power_ac1 + PV_power_ac2
Actual_batt_ch_disch_power_total = Actual_batt_ch_disch_power1 + Actual_batt_ch_disch_power2

# Erzeugung wird in openWB als negativer Wert weiter verarbeitet
PV_power_total = PV_power_total * -1
Actual_batt_ch_disch_power_total = Actual_batt_ch_disch_power_total * -1
PV_power_ac1 = PV_power_ac1 * -1
PV_power_ac2 = PV_power_ac2 * -1
Actual_batt_ch_disch_power1 = Actual_batt_ch_disch_power1 * -1
Actual_batt_ch_disch_power2 = Actual_batt_ch_disch_power2 * -1

# Summen der Erträge bestimmen
Total_yield = Total_yield1 + Total_yield2
Daily_yield = Daily_yield1 + Daily_yield2
Monthly_yield = Monthly_yield1 + Monthly_yield2
Yearly_yield = Yearly_yield1 + Yearly_yield2

# und zur Weiterverarbeitung alle Werte in die ramdisk
# zunächst alle Summenwerte beider WR
# Gesamtleistung AC PV-Module
with open('/var/www/html/openWB/ramdisk/pvwatt', 'w') as f:
    f.write(str(PV_power_total))
#schreibe den Wert nur wenn kein Speicher vorhanden ist. Wenn er da ist nutze die openWB PV Watt beschränkung
if boolspeicher != 1:
    # Gesamtertrag in Wattstunden
    with open('/var/www/html/openWB/ramdisk/pvkwh', 'w') as f:
        f.write(str(Total_yield))
# Gesamtertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/pvkwhk', 'w') as f:
    f.write(str(Total_yield / 1000))
# Tagesertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/daily_pvkwhk', 'w') as f:
    f.write(str(Daily_yield))
# Jahresertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk', 'w') as f:
    f.write(str(Yearly_yield))
# Monatsertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk', 'w') as f:
    f.write(str(Monthly_yield))

# Werte WR 1
# Leistung AC PV-Module
with open('/var/www/html/openWB/ramdisk/pvwatt1', 'w') as f:
    f.write(str(PV_power_ac1))
# Gesamtertrag in Wattstunden
with open('/var/www/html/openWB/ramdisk/pvkwh1', 'w') as f:
    f.write(str(Total_yield1))
# Gesamtertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/pvkwhk1', 'w') as f:
    f.write(str(Total_yield1 / 1000))
# Tagesertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/daily_pvkwhk1', 'w') as f:
    f.write(str(Daily_yield1))
# Jahresertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk1', 'w') as f:
    f.write(str(Yearly_yield1))
# Monatsertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk1', 'w') as f:
    f.write(str(Monthly_yield1))

# Werte WR 2
# Leistung AC PV-Module
with open('/var/www/html/openWB/ramdisk/pvwatt2', 'w') as f:
    f.write(str(PV_power_ac2))
# Gesamtertrag in Wattstunden
with open('/var/www/html/openWB/ramdisk/pvkwh2', 'w') as f:
    f.write(str(Total_yield2))
# Gesamtertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/pvkwhk2', 'w') as f:
    f.write(str(Total_yield2 / 1000))
# Tagesertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/daily_pvkwhk2', 'w') as f:
    f.write(str(Daily_yield2))
# Jahresertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk2', 'w') as f:
    f.write(str(Yearly_yield2))
# Monatsertrag in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk2', 'w') as f:
    f.write(str(Monthly_yield2))

# Nachfolgende Werte nur in temporäre ramdisk, da die Module
# Speicher und Bezug für die globalen Variablen zuständig sind
# und dort die Übernahme in die entsprechende ramdisk erfolgt
# Speicherleistung WR 1 + 2
with open('/var/www/html/openWB/ramdisk/temp_speicherleistung', 'w') as f:
    f.write(str(Actual_batt_ch_disch_power_total))
# Speicherleistung WR 1
with open('/var/www/html/openWB/ramdisk/temp_speicherleistung1', 'w') as f:
    f.write(str(Actual_batt_ch_disch_power1))
# Speicherleistung WR 2
with open('/var/www/html/openWB/ramdisk/temp_speicherleistung2', 'w') as f:
    f.write(str(Actual_batt_ch_disch_power2))
# Bezug EVU
with open('/var/www/html/openWB/ramdisk/temp_wattbezug', 'w') as f:
    f.write(str(Bezug))
# Bezug Strom Phase 1
with open('/var/www/html/openWB/ramdisk/temp_bezuga1', 'w') as f:
    f.write(str(Current_phase_1_powermeter))
# Bezug Strom Phase 2
with open('/var/www/html/openWB/ramdisk/temp_bezuga2', 'w') as f:
    f.write(str(Current_phase_2_powermeter))
# Bezug Strom Phase 3
with open('/var/www/html/openWB/ramdisk/temp_bezuga3', 'w') as f:
    f.write(str(Current_phase_3_powermeter))
# Netzfrequenz
with open('/var/www/html/openWB/ramdisk/temp_evuhz', 'w') as f:
    f.write(str(Frequency_powermeter))
# Bezug Leistung Phase 1
with open('/var/www/html/openWB/ramdisk/temp_bezugw1', 'w') as f:
    f.write(str(Active_power_phase_1_powermeter))
# Bezug Leistung Phase 2
with open('/var/www/html/openWB/ramdisk/temp_bezugw2', 'w') as f:
    f.write(str(Active_power_phase_2_powermeter))
# Bezug Leistung Phase 3
with open('/var/www/html/openWB/ramdisk/temp_bezugw3', 'w') as f:
    f.write(str(Active_power_phase_3_powermeter))
# Spannung Phase 1
with open('/var/www/html/openWB/ramdisk/temp_evuv1', 'w') as f:
    f.write(str(Voltage_phase_1_powermeter))
# Spannung Phase 2
with open('/var/www/html/openWB/ramdisk/temp_evuv2', 'w') as f:
    f.write(str(Voltage_phase_2_powermeter))
# Spannung Phase 3
with open('/var/www/html/openWB/ramdisk/temp_evuv3', 'w') as f:
    f.write(str(Voltage_phase_3_powermeter))
# Wirkfaktor, wird nur einmal vom Wechselrichter ausgegeben,
# und ist demnach für alle Phasen identisch
with open('/var/www/html/openWB/ramdisk/temp_evupf1', 'w') as f:
    f.write(str(Actual_cos_phi))
with open('/var/www/html/openWB/ramdisk/temp_evupf2', 'w') as f:
    f.write(str(Actual_cos_phi))
with open('/var/www/html/openWB/ramdisk/temp_evupf3', 'w') as f:
    f.write(str(Actual_cos_phi))

# Speicher Ladestand von Speicher am WR 1
with open('/var/www/html/openWB/ramdisk/temp_speichersoc', 'w') as f:
    f.write(str(Battery_actual_SOC1))
# Speicher Ladestand von Speicher am WR 2
with open('/var/www/html/openWB/ramdisk/temp_speichersoc2', 'w') as f:
    f.write(str(Battery_actual_SOC2))
