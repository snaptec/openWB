#!/usr/bin/python

import struct
import json
import urllib2
import time


ipaddress = "192.168.178.56"
debug = False

#ipaddress = str(sys.argv[1])


def myDecode(stringValue):
# Parameter: 
# stringValue:	String Wert, im Format Typ_Wert 
# 
# Rueckgabe:
# result: 		Floatzahl
    splitValue = stringValue.split('_')

    if splitValue[0] == 'fl':
        #Hex >> Float
        result = struct.unpack('f',struct.pack('I',int('0x'+splitValue[1],0)))[0]
    elif splitValue[0] == 'u3': 
        pass #TBD
    elif splitValue[0] == 'u8':
        pass #TBD
    
    return result

def writeVal(filePath,stringValue,multiplier,decimalpoints,offset):

#Parameter
#filePath: 		Pfad und Dateiname in der ein Wert geschrieben wird
#stringValue: 	Wert der nach dem knonvertieren in die Datei geschrieben wird
#multiplier: 	Wert mit dem die Zahl vor der Rundung multipliziert wird
#decimalpoints:	Anzahl Kommastellen 
#
#Rueckgabe: nichts

    val= myDecode(stringValue)

	# Format anpassen
    if multiplier != 0:
        val = val * multiplier

    #auf 2 Ziffern runden
    if decimalpoints == 0:
        val = int(val)
    elif decimalpoints != 0:
        val = round(val,decimalpoints)

    if offset != 0:
        val = val + offset

    if debug:
        print(filePath + ' ' + str(val))
    else:
        f = open(filePath, 'w')
        f.write(str(val))
        f.close()
    

#go-eCharger Parkplatz
response = urllib2.urlopen('http://192.168.178.77/status')
jsondata = json.load(response)
if not (jsondata["nrg"] is None):
    goe_1 = jsondata["nrg"][11]*10
    if debug == True:
        print("Leistung gesamt go-e1: " +str(goe_1))
    goe_1A1 = jsondata["nrg"][5]/10
    goe_1A2 = jsondata["nrg"][6]/10
    goe_1A3 = jsondata["nrg"][4]/10
    if debug == True:
        print("Ampere auf L1 go-e1: " +str(goe_1A1))
        print("Ampere auf L2 go-e1: " +str(goe_1A2))
        print("Ampere auf L3 go-e1: " +str(goe_1A3))

#go-eCharger Carport
response = urllib2.urlopen('http://192.168.178.111/status')
jsondata = json.load(response)
if not (jsondata["nrg"] is None):
    goe_2 = jsondata["nrg"][11]*10
    if debug == True:
        print("Leistung gesamt go-e2: " +str(goe_2))
    goe_2A1 = jsondata["nrg"][6]/10
    goe_2A2 = jsondata["nrg"][4]/10
    goe_2A3 = jsondata["nrg"][5]/10
    if debug == True:
        print("Ampere auf L1 go-e2: " +str(goe_2A1))
        print("Ampere auf L2 go-e2: " +str(goe_2A2))
        print("Ampere auf L3 go-e2: " +str(goe_2A3))

#EVU Daten
reqdata='{"PM1OBJ1":{"FREQ":"","U_AC":"","I_AC":"","P_AC":"","P_TOTAL":""}}'
response = urllib2.urlopen('http://'+ ipaddress +'/lala.cgi' ,data=reqdata)
jsondata = json.load(response)
#keine Werte gefunden
# echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
# echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
# echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3

#SENEC: Gesamtleistung (W) Werte -3000  >> 3000
if not (jsondata['PM1OBJ1'] ['P_TOTAL'] is None):
    writeVal('/var/www/html/openWB/ramdisk/wattbezug_senec', jsondata['PM1OBJ1'] ['P_TOTAL'],0,0,goe_1 + goe_2)

#SENEC: Frequenz(Hz) Werte 49.00 >> 50.00
if not (jsondata['PM1OBJ1'] ['FREQ'] is None):
    writeVal('/var/www/html/openWB/ramdisk/evuhz',jsondata['PM1OBJ1'] ['FREQ'],0,2,0)

#SENEC: Spannung (V) Werte 219.12 >> 223.43
if not (jsondata['PM1OBJ1'] ['U_AC'] [0] is None):
    writeVal('/var/www/html/openWB/ramdisk/evuv1', jsondata['PM1OBJ1'] ['U_AC'] [0],0,2,0)
if not (jsondata['PM1OBJ1'] ['U_AC'] [1] is None):
    writeVal('/var/www/html/openWB/ramdisk/evuv2', jsondata['PM1OBJ1'] ['U_AC'] [1],0,2,0)
if not (jsondata['PM1OBJ1'] ['U_AC'] [2] is None):
    writeVal('/var/www/html/openWB/ramdisk/evuv3', jsondata['PM1OBJ1'] ['U_AC'] [2],0,2,0)

#SENEC: Leistung (W) Werte -2345 >> 3000
if not (jsondata['PM1OBJ1'] ['P_AC'] [0] is None):
    writeVal('/var/www/html/openWB/ramdisk/bezugw1', jsondata['PM1OBJ1'] ['P_AC'] [0],0,0,0)
if not (jsondata['PM1OBJ1'] ['P_AC'] [1] is None):
    writeVal('/var/www/html/openWB/ramdisk/bezugw2', jsondata['PM1OBJ1'] ['P_AC'] [1],0,0,0)
if not (jsondata['PM1OBJ1'] ['P_AC'] [2] is None):
    writeVal('/var/www/html/openWB/ramdisk/bezugw3', jsondata['PM1OBJ1'] ['P_AC'] [2],0,0,0)

#SENEC: Strom (A) Werte 0.88 >> 1.67 
if not (jsondata['PM1OBJ1'] ['I_AC'] [0] is None):
    writeVal('/var/www/html/openWB/ramdisk/bezuga1_senec', jsondata['PM1OBJ1'] ['I_AC'] [0],0,2,goe_1A1 + goe_2A1)
if not (jsondata['PM1OBJ1'] ['I_AC'] [1] is None):    
    writeVal('/var/www/html/openWB/ramdisk/bezuga2_senec', jsondata['PM1OBJ1'] ['I_AC'] [1],0,2,goe_1A2 + goe_2A2)
if not (jsondata['PM1OBJ1'] ['I_AC'] [2] is None):    
    writeVal('/var/www/html/openWB/ramdisk/bezuga3_senec', jsondata['PM1OBJ1'] ['I_AC'] [2],0,2,goe_1A3 + goe_2A3)

#Batteriedaten:
reqdata='{"ENERGY":{"GUI_BAT_DATA_FUEL_CHARGE":"","GUI_BAT_DATA_POWER":"","GUI_BAT_DATA_VOLTAGE":"","GUI_BAT_DATA_OA_CHARGING":"","GUI_INVERTER_POWER":""}}'
response = urllib2.urlopen('http://'+ ipaddress +'/lala.cgi' ,data=reqdata)
jsondata = json.load(response)

#SENEC: Batterieleistung (W) Werte -345 (Entladen) >> 1200 (laden)
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'] is None):
    writeVal('/var/www/html/openWB/ramdisk/speicherleistung_senec', jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'],0,0,0)

#SENEC: Fuellmenge in Prozent Werte 10 >> 55 >> 100
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'] is None):
    writeVal('/var/www/html/openWB/ramdisk/speichersoc_senec', jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'],0,0,0)

#SENEC: Leistung Wechselrichter in (W) Werte 
if not (jsondata['ENERGY'] ['GUI_INVERTER_POWER'] is None):
    writeVal('/var/www/html/openWB/ramdisk/pvwatt_senec', jsondata['ENERGY'] ['GUI_INVERTER_POWER'],0,0,0)


#Statistik
reqdata='{"STATISTIC":{"LIVE_BAT_CHARGE":"","LIVE_BAT_DISCHARGE":"","LIVE_GRID_EXPORT":"","LIVE_GRID_IMPORT":"","LIVE_HOUSE_CONS":"","LIVE_PV_GEN":""}}'
response = urllib2.urlopen('http://'+ ipaddress +'/lala.cgi' ,data=reqdata)
jsondata = json.load(response)

#SENEC: Gesamtlademenge (Wh) Werte 1692
if not (jsondata['STATISTIC'] ['LIVE_BAT_CHARGE'] is None):
    writeVal('/var/www/html/openWB/ramdisk/speicherikwh_senec', jsondata['STATISTIC'] ['LIVE_BAT_CHARGE'],1000,0,0)

#SENEC: Gesamtentlademenge (Wh) Werte 1590
if not (jsondata['STATISTIC'] ['LIVE_BAT_DISCHARGE'] is None):
    writeVal('/var/www/html/openWB/ramdisk/speicherekwh_senec', jsondata['STATISTIC'] ['LIVE_BAT_DISCHARGE'],1000,0,0)

#SENEC: Gesamtimport (Wh) Werte  1809000
if not (jsondata['STATISTIC'] ['LIVE_GRID_IMPORT'] is None):
    writeVal('/var/www/html/openWB/ramdisk/bezugkwh_senec', jsondata['STATISTIC'] ['LIVE_GRID_IMPORT'],1000,0,0)
    
#SENEC: Gesamteinspeisung Werte (Wh) 7085000
if not (jsondata['STATISTIC'] ['LIVE_GRID_EXPORT'] is None):
    writeVal('/var/www/html/openWB/ramdisk/einspeisungkwh_senec', jsondata['STATISTIC'] ['LIVE_GRID_EXPORT'],1000,0,0)

#SENEC: Gesamt PV Erzeugung (vom WR)  Werte (Wh) 7085000
if not (jsondata['STATISTIC'] ['LIVE_PV_GEN'] is None):
    writeVal('/var/www/html/openWB/ramdisk/pvewh_senec', jsondata['STATISTIC'] ['LIVE_PV_GEN'],1000,0,0)