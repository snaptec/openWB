#!/usr/bin/python
# coding: utf8

#########################################################
#
# liest aus Wechselrichter Kostal Plenticore Register
# zu PV-Statistik und berechnet PV-Leistung, Speicherleistung
# unter Beachtung angeschlossener Batterie falls vorhanden
#
# WICHTIG: Tagesertrag wird nicht ausgelesen, dieser wird durch openWB berechnet!
# Kostal sieht Ertrag erst, wenn DC-AC-Wandlung erfolgte. Somit entsteht Ertrag in diesem Sinne auch,
# wenn der Speicher Leistung abgibt. PV-Leistung, die in den Speicher geht, sieht Kostal nicht als
# Ertrag. Da openWB den Tagesertrag jedoch als PV-Ertrag interpretiert (also ges. Energiemenge,
# die von der PV erzeugt wurde, einschl. Speicherladung), berechnet openWB selbst.
#
# Speicher nur am WR1 erlaubt! Bei zus. Speicher an WR2 stimmen die Werte nicht mehr!
#
# 2019 Kevin Wieland, Michael Ortenstein
# This file is part of openWB
#
#########################################################
import os
import sys
import time
remotedebug=0
#zukünftige Nutzung ?
#try:
#    import debugpy
#    remotedebug=1
#except ImportError, e:
#remotedebug=0  # module doesn't exist, deal with it.

from datetime import datetime
#from timezone import timezone
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient

class myLogging:
    @staticmethod
    def DebugLog(Pid, message):
        #local_time = datetime.now(timezone.utc).astimezone()
        local_time= datetime.now()
        print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ Pid +": " + message)   
    @staticmethod
    def openWBLog(Pid, message):
        #local_time = datetime.now(timezone.utc).astimezone()
        local_time = datetime.now()
        log = (local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ Pid +": " + 'read_kostalplenticore.py:' +message + '\n')
        try:
            # Versuche in ramdisk log zu schreiben
            with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
                f.write(log)
        except:
            #2. Versuch mit print 
            DebugLog(Pid, message)            
            
class plenticore:
    
    def __init__(self, WRIP, Battery):        
        # Class Variablen
        self._WRIP = WRIP
        self._Battery = Battery
        self._wr = ''   
        # Plenticore als Modbus Client einrichten
        try:
            self._wr = ModbusTcpClient(self._WRIP, port=1502)        
            #self._wr.client.connect()
        except:
            # kein Zugriff auf WR1, also Abbruch und mit Null initialisierte Variablen in die Ramdisk
            myLogging.DebugLog('', 'Wechserrichter IP :' + self._WRIP)
            myLogging.openWBLog('Fehler beim Initialisieren des Modbus-Client WR1: ' + sys.exc_info()[0])
            sys.exit(1)            
    
    def ReadRegister(self, address, count=1, **kwargs):
        return self._wr.read_holding_registers(address,count,**kwargs)

    def ReadBattery(self):
        # dann zunächst alle relevanten Register aus WR 1 auslesen:
        try:
            if self._Battery == 1:
                # Speicher am Planticore 1, dann Leistung String 1+2 auslesen zwecks Berechnungen
                # Plenticore Register 260: Power DC1 [W]
                # ist Leistung String 1
                reg_260 = self._wr.read_holding_registers(260,2,unit=71)
                # Plenticore Register 260: Power DC1 [W]
                # ist Leistung String 1
                reg_270 = self._wr.read_holding_registers(270,2,unit=71)
                # Plenticore Register 582: Actual_batt_ch_disch_power [W]
                # ist Lade-/Entladeleistung des angeschlossenen Speichers
                # {charge=negativ, discharge=positiv}
                reg_582 = self._wr.read_holding_registers(582,1,unit=71)
                # Plenticore Register 514: Battery_actual_SOC [%]
                # ist Ladestand des Speichers
                reg_514 = self._wr.read_holding_registers(514,1,unit=71)              
        except:
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk
            myLogging.openWBLog('Fehler beim Lesen der Modbus-Register Battery:' + self._WRIP + '(falsche IP?)' + sys.exc_info()[0])        
            sys.exit(1)

        self.FRegister_260 = BinaryPayloadDecoder.fromRegisters(reg_260.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_270 = BinaryPayloadDecoder.fromRegisters(reg_270.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_514 = BinaryPayloadDecoder.fromRegisters(reg_514.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_582 = BinaryPayloadDecoder.fromRegisters(reg_582.registers, byteorder=Endian.Big, wordorder=Endian.Little)
                
    def ReadWechselrichter(self):
        try:
            # Plenticore Register 575: Inverter_generation_power_actual [W]
            # ist AC-Leistungsabgabe des Wechselrichters
            reg_575 = self._wr.read_holding_registers(575,1,unit=71)  
            # Plenticore Register 320: Total_yield [Wh]
            # ist PV Gesamtertrag
            reg_320 = self._wr.read_holding_registers(320,2,unit=71)
            # Plenticore Register 324: Yearly_yield [Wh]
            # ist PV Jahresertrag
            reg_324 = self._wr.read_holding_registers(324,2,unit=71)
            # Plenticore Register 326: Monthly_yield [Wh]
            # ist PV Monatsertrag
            reg_326 = self._wr.read_holding_registers(326,2,unit=71)                        
        except:
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk
            myLogging.openWBLog('Fehler beim Lesen der Modbus-Register WR:' + self._WRIP + '(falsche WR-IP?)' + sys.exc_info()[0])        
            sys.exit(1)

        self.FRegister_320 = BinaryPayloadDecoder.fromRegisters(reg_320.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_324 = BinaryPayloadDecoder.fromRegisters(reg_324.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_326 = BinaryPayloadDecoder.fromRegisters(reg_326.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_575 = BinaryPayloadDecoder.fromRegisters(reg_575.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    def ReadKSEM300(self):
        try:
            # Strom auf Phasen 1-3 EVU aus Kostal Plenticore lesen
            # Wechselrichter bekommt Daten von Energy Manager EM300
            # Phase 1
            # Plenticore Register 222: Current_phase_1_(powermeter) [A]
            reg_222 = self._wr.read_holding_registers(222,2,unit=71)
            # Phase 2
            # Plenticore Register 232: Current_phase_2_(powermeter) [A]
            reg_232 = self._wr.read_holding_registers(232,2,unit=71)
            # Phase 3
            # Plenticore Register 242: Current_phase_3_(powermeter) [A]
            reg_242 = self._wr.read_holding_registers(242,2,unit=71)
            # Leistung EVU
            # Plenticore Register 252: Total_active_power_(powermeter) [W]
            # Sensorposition 1 (Hausanschluss): (+)Hausverbrauch (-)Erzeugung
            # Sensorposition 2 (EVU Anschlusspunkt): (+)Bezug (-)Einspeisung
            reg_252 = self._wr.read_holding_registers(252,2,unit=71)
            # Frequenz EVU
            # Plenticore Register 220: Frequency_(powermeter) [Hz]
            reg_220 = self._wr.read_holding_registers(220,2,unit=71)
            # Leistung auf Phasen 1-3 EVU aus Kostal Plenticore lesen
            # Wechselrichter bekommt Daten von Energy Manager EM300
            # Phase 1
            # Plenticore Register 224: Active_power_phase_1_(powermeter) [W]
            reg_224 = self._wr.read_holding_registers(224,2,unit=71)
            # Phase 2
            # Plenticore Register 234: Active_power_phase_2_(powermeter) [W]
            reg_234 = self._wr.read_holding_registers(234,2,unit=71)
            # Phase 3
            # Plenticore Register 244: Active_power_phase_3_(powermeter) [A]
            reg_244 = self._wr.read_holding_registers(244,2,unit=71)
            # Spannung auf Phasen 1-3 EVU aus Kostal Plenticore lesen
            # Wechselrichter bekommt Daten von Energy Manager EM300
            # Phase 1
            # Plenticore Register 230: Voltage_phase_1_(powermeter) [V]
            reg_230 = self._wr.read_holding_registers(230,2,unit=71)
            # Phase 2
            # Plenticore Register 240: Voltage_phase_2_(powermeter) [V]
            reg_240 = self._wr.read_holding_registers(240,2,unit=71)
            # Phase 3
            # Plenticore Register 250: Voltage_phase_3_(powermeter) [V]
            reg_250 = self._wr.read_holding_registers(250,2,unit=71)
            # Plenticore Register 150: Actual_cos_phi []
            # ist Wirkfaktor
            reg_150 = self._wr.read_holding_registers(150,2,unit=71)           
        except:
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk
            myLogging.openWBLog('Fehler beim Lesen der Modbus-Register KSEM300:' + self._WRIP + '(falsche WR-IP?)' + sys.exc_info()[0])        
            sys.exit(1)           
        
        #ausgelesene Register WR 1 dekodieren
        #FRegister_100 = BinaryPayloadDecoder.fromRegisters(reg_100.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_150 = BinaryPayloadDecoder.fromRegisters(reg_150.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_220 = BinaryPayloadDecoder.fromRegisters(reg_220.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_222 = BinaryPayloadDecoder.fromRegisters(reg_222.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_224 = BinaryPayloadDecoder.fromRegisters(reg_224.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_230 = BinaryPayloadDecoder.fromRegisters(reg_230.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_232 = BinaryPayloadDecoder.fromRegisters(reg_232.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_234 = BinaryPayloadDecoder.fromRegisters(reg_234.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_240 = BinaryPayloadDecoder.fromRegisters(reg_240.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_242 = BinaryPayloadDecoder.fromRegisters(reg_242.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_244 = BinaryPayloadDecoder.fromRegisters(reg_244.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_250 = BinaryPayloadDecoder.fromRegisters(reg_250.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        self.FRegister_252 = BinaryPayloadDecoder.fromRegisters(reg_252.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        
def main(argv=None):
    myPid = str(os.getpid()) 
    if len(sys.argv) ==5:
        # IP für Wechselrichter 1
        WR1IP = str(sys.argv[1])
        # IP für Wechselrichter 2
        WR2IP = str(sys.argv[2])
        # Battery vorhanden
        Battery = int(sys.argv[3])
        ## not used
        ARGV4 = str(sys.argv[4])
    else:
        myLogging.openWBLog(myPid, 'Argumente fehlen oder sind fehlerhaft')
        sys.exit(1)
    
    #tdo: how to get openWB debug level
    _strdebug = os.environ.get('debug')
    
    if _strdebug != 'none':
        try:      
            Debug = int(_strdebug)
        except:
            Debug = 0    
          
    # Variablen initialisieren
    # Summenwerte
    PV_power_total = 0
    Total_yield = 0
    Yearly_yield = 0
    Monthly_yield = 0
    # Werte WR1
    PV_power_ac1 = 0
    Total_yield1 = 0
    Yearly_yield1 = 0
    Monthly_yield1 = 0
    Actual_batt_ch_disch_power = 0
    Battery_actual_SOC = 0
    # Werte WR2
    PV_power_ac2 = 0
    Total_yield2 = 0
    Yearly_yield2 = 0
    Monthly_yield2 = 0
    # Werte EVU
    Bezug = 0
    Current_phase_1_powermeter = 0
    Current_phase_2_powermeter = 0
    Current_phase_3_powermeter = 0
    Frequency_powermeter = 0
    Active_power_phase_1_powermeter = 0
    Active_power_phase_2_powermeter = 0
    Active_power_phase_3_powermeter = 0
    Voltage_phase_1_powermeter = 0
    Voltage_phase_2_powermeter = 0
    Voltage_phase_3_powermeter = 0
    Actual_cos_phi = 0    
        
    WR1 = plenticore(WR1IP,Battery)
    # am WR2 darf keine Batterie sein, deswegen hier vereinfacht PV-Leistung = AC-Leistung des WR
    if WR2IP != 'none':
        WR2= plenticore(WR2IP, 0)    
    if remotedebug==1 and Debug >= 2:
        try:
            debugpy.listen(5678)
        except:
          pass
        
    myLogging.openWBLog(myPid, 'Wechselrichter Kostal Plenticore Config - WR1:' + str(WR1IP) + " -WR2:" + str(WR2IP) + " -Battery:" + str(Battery))
    
    WR1.ReadWechselrichter()
    WR1.ReadKSEM300()
        
    # dekodierte Register WR 1 in entsprechende Typen umwandeln
    #Total_DC_power1 = int(FRegister_100.decode_32bit_float())
    Total_yield1 = int(WR1.FRegister_320.decode_32bit_float())
    Yearly_yield1 = round((WR1.FRegister_324.decode_32bit_float()/1000),2)
    Monthly_yield1 = round((WR1.FRegister_326.decode_32bit_float()/1000),2)
    Inverter_generation_power_actual1 = int(WR1.FRegister_575.decode_16bit_int())
    # Werte aus EM300/KSEM
    Current_phase_1_powermeter = round(WR1.FRegister_222.decode_32bit_float(),2)
    Current_phase_2_powermeter = round(WR1.FRegister_232.decode_32bit_float(),2)
    Current_phase_3_powermeter = round(WR1.FRegister_242.decode_32bit_float(),2)
    Total_active_power_powermeter = int(WR1.FRegister_252.decode_32bit_float())
    Frequency_powermeter = round(WR1.FRegister_220.decode_32bit_float(),2)
    Active_power_phase_1_powermeter = round(WR1.FRegister_224.decode_32bit_float(),2)
    Active_power_phase_2_powermeter = round(WR1.FRegister_234.decode_32bit_float(),2)
    Active_power_phase_3_powermeter = round(WR1.FRegister_244.decode_32bit_float(),2)
    Voltage_phase_1_powermeter = round(WR1.FRegister_230.decode_32bit_float(),2)
    Voltage_phase_2_powermeter = round(WR1.FRegister_240.decode_32bit_float(),2)
    Voltage_phase_3_powermeter = round(WR1.FRegister_250.decode_32bit_float(),2)
    Actual_cos_phi = round(WR1.FRegister_150.decode_32bit_float(),3)
    if Battery == 1:
        WR1.ReadBattery()    
        DC1_power1 = int(WR1.FRegister_260.decode_32bit_float())
        DC2_power1 = int(WR1.FRegister_270.decode_32bit_float())
        Actual_batt_ch_disch_power = int(WR1.FRegister_582.decode_16bit_int())
        Battery_actual_SOC = int(WR1.FRegister_514.decode_16bit_int())
    else:
        Actual_batt_ch_disch_power = 0
        Battery_actual_SOC = 0

    # ggf. dekodierte Register WR 2 in entsprechende Typen umwandeln
    if WR2IP != 'none':
        WR2.ReadWechselrichter()
        Total_yield2 = int(WR2.FRegister_320.decode_32bit_float())
        Yearly_yield2 = round((WR2.FRegister_324.decode_32bit_float()/1000),2)
        Monthly_yield2 = round((WR2.FRegister_326.decode_32bit_float()/1000),2)
        Inverter_generation_power_actual2 = int(WR2.FRegister_575.decode_16bit_int())

    # AC-Leistung der PV-Module/des Speichers für WR 1 bestimmen
    if Battery == 0:
        # kein Speicher verbaut, dann ist PV-Leistung = AC-Leistung
        PV_power_ac1 = Inverter_generation_power_actual1
    else:
        # da Batterie DC-seitig angebunden ist,
        # muss deren Lade-/Entladeleistung mitbetrachtet werden
        # wenn man die AC-Leistung der PV-Module und des Speichers bestimmen möchte.
        # Kostal liefert nur DC-Werte, also DC-Leistung berechnen
        PV_power_dc1 = DC1_power1 + DC2_power1 # PV an String 1 und 2

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
            if Actual_batt_ch_disch_power > 0:
                # wird die Batterie entladen, werden die Wandlungsverluste anteilig an der
                # DC-Leistung auf PV und Batterie verteilt
                # dazu muss der Divisor Total_DC_power != 0 sein
                Total_DC_power1 = PV_power_dc1 + Actual_batt_ch_disch_power
                PV_power_ac1 = int((PV_power_dc1 / float(Total_DC_power1)) * Inverter_generation_power_actual1)
                Actual_batt_ch_disch_power = Inverter_generation_power_actual1 - PV_power_ac1
            else:
                # Batterie wird geladen
                # dann ist PV-Leistung die Wechselrichter-AC-Leistung + die Ladeleistung der Batterie (negative because charging)
                PV_power_ac1 = Inverter_generation_power_actual1 - Actual_batt_ch_disch_power

    # am WR2 darf keine Batterie sein, deswegen hier vereinfacht PV-Leistung = AC-Leistung des WR
    if WR2IP != 'none':
        PV_power_ac2 = Inverter_generation_power_actual2

    # Bezug zunächst nur auslesen, Sensorposition wird im Strombezugsmessmodul betrachtet
    Bezug = Total_active_power_powermeter

    # Summe der jeweiligen AC-Leistungen bestimmen
    PV_power_total = PV_power_ac1 + PV_power_ac2

    # Erzeugung wird in openWB als negativer Wert weiter verarbeitet
    PV_power_total *= -1
    Actual_batt_ch_disch_power *= -1
    PV_power_ac1 *= -1
    PV_power_ac2 *= -1

    # Summen der Erträge bestimmen
    Total_yield = Total_yield1 + Total_yield2
    Monthly_yield = Monthly_yield1 + Monthly_yield2
    Yearly_yield = Yearly_yield1 + Yearly_yield2

    # zunächst alle Summenwerte beider WR
    # Gesamtleistung AC PV-Module
    with open('/var/www/html/openWB/ramdisk/pvwatt', 'w') as f:
        f.write(str(PV_power_total))
    #schreibe den Wert nur wenn kein Speicher vorhanden ist. Wenn er da ist nutze die openWB PV Watt beschränkung
    if Battery != 1:
        # Gesamtertrag in Wattstunden
        with open('/var/www/html/openWB/ramdisk/pvkwh', 'w') as f:
            f.write(str(Total_yield))
    # Gesamtertrag in Kilowattstunden
    with open('/var/www/html/openWB/ramdisk/pvkwhk', 'w') as f:
        f.write(str(Total_yield / 1000))
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
    # Jahresertrag in Kilowattstunden
    with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk2', 'w') as f:
        f.write(str(Yearly_yield2))
    # Monatsertrag in Kilowattstunden
    with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk2', 'w') as f:
        f.write(str(Monthly_yield2))

    # Nachfolgende Werte nur in temporäre ramdisk, da die Module
    # Speicher und Bezug für die globalen Variablen zuständig sind
    # und dort die Übernahme in die entsprechende ramdisk erfolgt
    # Speicherleistung WR 1
    with open('/var/www/html/openWB/ramdisk/temp_speicherleistung', 'w') as f:
        f.write(str(Actual_batt_ch_disch_power))
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
        f.write(str(Battery_actual_SOC))                      

if __name__ == "__main__":
    main(sys.argv)
