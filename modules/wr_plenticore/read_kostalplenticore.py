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
# 01.09.2021   skl     Überarbeitung Klassen basiert   
#########################################################
import os
import sys
#import time
remotedebug=0
#zukünftige Nutzung ?
#try:
#    import debugpy
#    remotedebug=1
#except ImportError, e:
#remotedebug=0  # module doesn't exist, deal with it.

from datetime import datetime
#only in pyhton >3 available
#from packaging import version
#from timezone import timezone
from ipparser import ipparser
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient

class myLogging:
    @staticmethod
    def DebugLog(Pid, message):
        #local_time = datetime.now(timezone.utc).astimezone()
        local_time= datetime.now()
        #print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ Pid +": " + message)   
    @staticmethod
    def openWBLog(Pid, message):
        #local_time = datetime.now(timezone.utc).astimezone()
        local_time = datetime.now()
        log = (local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ Pid +": " + 'read_kostalplenticore.py:' +message + '\n')
        try:
            #print(log)
            # Versuche in ramdisk log zu schreiben
            with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
                f.write(log)
        except:
            #2. Versuch mit print 
            myLogging.DebugLog(Pid, message)            

class modbus:
    def __init__(self, Pid, IP):        
        # Class Variablen
        self._IP = IP        
        self._client = ''
        self._pid= Pid
        # Plenticore als Modbus Client einrichten       
        self._client = ModbusTcpClient(self._IP, port=1502)        
        #self._wr.client.connect()       
            
    def ReadRegister(self, address, count=1, **kwargs):
        return self._client.read_holding_registers(address,count,**kwargs)

    def ReadUInt16(self,addr):
        data=self._client.read_holding_registers(addr, 1, unit=71)
        UInt16register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = UInt16register.decode_16bit_uint()
        return(result)
    
    def ReadInt16(self,addr):
        data=self._client.read_holding_registers(addr, 1, unit=71)
        Int16register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = Int16register.decode_16bit_int()
        return(result)
    
    def ReadUInt32(self,addr):
        data=self._client.read_holding_registers(addr, 2, unit=71)
        UInt32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = UInt32register.decode_32bit_uint()
        return(result)

    def ReadInt32(self,addr):
        data=self._client.read_holding_registers(addr, 2, unit=71)
        Int32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = Int32register.decode_32bit_int()
        return(result)

    def ReadFloat32(self,addr):
        data=self._client.read_holding_registers(addr, 2, unit=71)
        Float32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = Float32register.decode_32bit_float()
        return(result)
    
    def ReadUInt64(self,addr):
        data=self._client.read_holding_registers(addr,4,unit=71)
        UInt64register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = UInt64register.decode_64bit_uint()
        return(result)
    
    def ReadString(self,addr):
        data=self._client.read_holding_registers(addr,8,unit=71)
        Stringregister = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result = Stringregister.decode_string(8)
        return(result)

class plenticore_KSEM:
    def __init__(self):
        # Phase 1
        self.I_P1_A = 0
        # Phase 2
        self.I_P2_A = 0
        # Phase 3
        self.I_P3_A = 0
        #EVU Gesamt
        self.P_active_total = 0
        #Frequenz
        self.Freq = 0
        #Leistung P1-3
        self.P_P1_W = 0
        self.P_P2_W = 0
        self.P_P3_W = 0
        #Spannung P1-3
        self.U_P1_V = 0
        self.U_P2_V = 0
        self.U_P3_V = 0
        #cosphi
        self.cosphi_actual = 0
        
class plenticore_inverter:   
    def __init__(self):
        self.MC_Version = ""
        self.String_Count = 0
        self.P_DC_total = 0
        self.P_DC_S1 = 0
        self.P_DC_S2 = 0
        self.P_DC_S3 = 0
        self.P_DC_in_total =0
        self.P_Generation_actual = 0
        self.P_PV_AC_total = 0
        self.P_Home_Cons_PV = 0
        self.P_Home_Cons_Grid = 0
        self.P_Home_Cons_Bat = 0
        self.Total_yield = 0
        self.Yearly_yield = 0
        self.Monthly_yield = 0
       
class plenticore_battery:
    def __init__(self):
        self.Model = 0
        self.SerialNo= 0
        self.SoC_actual = 0
        self.P_charge_discharge = 0        
        self.Capacity = 0
        
class plenticore(modbus):    
    #Klassen Variablen
    BatMgt = 0    
    def __init__(self, Pid, WRIP, Battery):        
        # Class Variablen
        self._pid= Pid
        self._IP = WRIP                        
        self._Battery = Battery       
         #KSEM
        self.attr_KSEM = plenticore_KSEM()
        #Wechselrichter
        self.attr_WR = plenticore_inverter()    
        #Battery
        self.attr_Bat= plenticore_battery()
        # Plenticore als Modbus Client einrichten
        try:
            modbus.__init__(self, Pid, WRIP)            
        except:
            # kein Zugriff auf WR1, also Abbruch und mit Null initialisierte Variablen in die Ramdisk
            myLogging.DebugLog('', 'Wechserrichter IP :' + self._IP)
            myLogging.openWBLog(self._pid, 'Fehler beim Initialisieren des Modbus-Client WR1: ' + str(sys.exc_info()[0]))            
            #sys.exit(1)  
    def ReadBattery(self):
        # dann zunächst alle relevanten Register aus WR 1 auslesen:
        try:
            if self._Battery == 1:
                # Plenticore Register 514: Battery_actual_SOC [%]
                # ist Ladestand des Speichers
                self.attr_Bat.SoC_actual = int(self.ReadInt16(514))        
                # Plenticore Register 525: Battery_Model ID
                self.attr_Bat.Model =int(self.ReadUInt32(525))
                # Plenticore Register 527: Battery_Serial
                self.attr_Bat.SerialNo =int(self.ReadUInt32(527))
                # Plenticore Register 529: Battery_Capacity
                self.attr_Bat.Capacity =int(self.ReadUInt32(529)) 
                # Plenticore Register 582: Actual_batt_ch_disch_power [W]
                # ist Lade-/Entladeleistung des angeschlossenen Speichers
                # {charge=negativ, discharge=positiv}
                self.attr_Bat.P_charge_discharge = int(self.ReadInt16(582))           
        except:
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk
            myLogging.openWBLog(self._pid, 'Fehler beim Lesen der Modbus-Register Battery:' + str(self._IP) + '(falsche IP?)' + str(sys.exc_info()[0]))        
            #sys.exit(1)                
        
    def ReadWechselrichter(self):
        try:
            # Kostal Anzahl an PV Strings
            self.attr_WR.String_Count = int(self.ReadUInt16(34))            
            # FW Version of Kostal
            self.attr_WR.MC_Version = str(self.ReadString(38))            
            # Plenticore Register 260: Power DC1 [W]
            # ist Leistung String 1
            self.attr_WR.P_DC_total = int(self.ReadFloat32(100))
            # Plenticore Register 106: Power Home Consumption Battery [W]            
            self.attr_WR.P_Home_Cons_Bat = int(self.ReadFloat32(106))
            # Plenticore Register 106: Power Home Consumption Grid [W]            
            self.attr_WR.P_Home_Cons_Grid = int(self.ReadFloat32(108))
            # Plenticore Register 116: Power Home Consumption PV [W]            
            self.attr_WR.P_Home_Cons_PV = int(self.ReadFloat32(116))
            # Plenticore Register 172: Total Active Power AC [W]            
            self.attr_WR.P_AC_Total = int(self.ReadFloat32(172))
            # Plenticore Register 260: Power DC1 [W]
            # ist Leistung String 1
            self.attr_WR.P_DC_S1 = int(self.ReadFloat32(260)) 
            # Plenticore Register 270: Power DC2 [W]
            # ist Leistung String 2
            self.attr_WR.P_DC_S2 = int(self.ReadFloat32(270)) 
            # Plenticore Register 270: Power DC3 [W]
            # ist Leistung String 3
            self.attr_WR.P_DC_S3 = int(self.ReadFloat32(280))             
            # Plenticore Register 320: Total_yield [Wh]
            # ist PV Gesamtertrag
            self.attr_WR.Total_yield = int(self.ReadFloat32(320))
            # Plenticore Register 324: Yearly_yield [Wh]
            # ist PV Jahresertrag
            self.attr_WR.Yearly_yield = round((self.ReadFloat32(324)/1000),2)
            # Plenticore Register 326: Monthly_yield [Wh]
            # ist PV Monatsertrag
            self.attr_WR.Monthly_yield = round((self.ReadFloat32(326)/1000),2)
            # Plenticore Register 575: Inverter_generation_power_actual [W]
            # ist AC-Leistungsabgabe des Wechselrichters
            self.attr_WR.P_Generation_actual = int(self.ReadInt16(575))           
            # nur generierte PV Leistung berechnen, keine BatterieLeistung
            self.attr_WR.P_DC_in_total= self.attr_WR.P_DC_S1 + self.attr_WR.P_DC_S2            
            # im Fall ohne Batterie                   
            if (self._Battery==0):
                # ggf. 3 String zu addieren
                self.attr_WR.P_DC_in_total+= self.attr_WR.P_DC_S3
                self.attr_WR.P_PV_AC_total  = self.attr_WR.P_Generation_actual
            # zur weiter Berechnung im Fall mit Batterie                   
            else:
                # da Batterie DC-seitig angebunden ist,
                # muss deren Lade-/Entladeleistung mitbetrachtet werden
                # wenn man die AC-Leistung der PV-Module und des Speichers bestimmen möchte.
                # Kostal liefert nur DC-Werte, also DC-Leistung berechnen    
                # schauen, ob überhaupt PV-Leistung erzeugt wird
                if  self.attr_WR.P_DC_in_total < 0:
                    # PV-Anlage kann nichts verbrauchen, also ggf. Register-/Rundungsfehler korrigieren
                    self.attr_WR.P_PV_AC_total  = 0
                else:
                    # wird PV-DC-Leistung erzeugt, müssen die Wandlungsverluste betrachtet werden
                    # Kostal liefert nur DC-seitige Werte
                    # zunächst Annahme, die Batterie wird geladen:
                    # die PV-Leistung die Summe aus verlustbehafteter AC-Leistungsabgabe des WR
                    # und der DC-Ladeleistung, die Wandlungsverluste werden also nur in der PV-Leistung
                    # ersichtlich
                    if self.attr_Bat.P_charge_discharge > 0:
                        # wird die Batterie entladen, werden die Wandlungsverluste anteilig an der
                        # DC-Leistung auf PV und Batterie verteilt
                        # dazu muss der Divisor Total_DC_power != 0 sein
                        Total_DC_power1 =  self.attr_WR.P_DC_in_total + self.attr_Bat.P_charge_discharge
                        self.attr_WR.P_PV_AC_total = int((self.attr_WR.P_DC_in_total  / float(Total_DC_power1)) * self.attr_WR.P_Generation_actual)
                        self.attr_Bat.P_charge_discharge = self.attr_WR.P_Generation_actual - self.attr_WR.P_PV_AC_total
                    else:
                        # Batterie wird geladen
                        # dann ist PV-Leistung die Wechselrichter-AC-Leistung + die Ladeleistung der Batterie (negative because charging)
                        self.attr_WR.P_PV_AC_total = self.attr_WR.P_Generation_actual- self.attr_Bat.P_charge_discharge
                        self.attr_WR.P_DC_in_total += self.attr_WR.P_DC_S3 
        except:            
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk
            myLogging.openWBLog(self._pid, "Fehler beim Lesen der Modbus-Register WR:" + str(self._IP) +
                                "(falsche WR-IP?)" + str(sys.exc_info()[0]))        
            #sys.exit(1)  
      
        #Version Check to enable ModBus BatterMgt - not available before this version                
        #print("FW Version BatMgtSupport min=" + str(("1.47")))
        #print("FW Version Ist=" + str(self.attr_WR.MC_Version))        
        #if version.parse(str(self.attr_WR.MC_Version)) >= version.parse("1.47"):
        #    self.BatMgt =1
        #else:
        self.BatMgt =0
        
    def ReadKSEM300(self):
        try:
            # Strom auf Phasen 1-3 EVU aus Kostal Plenticore lesen
            # Wechselrichter bekommt Daten von Energy Manager EM300
            # Phase 1
            # Plenticore Register 222: Current_phase_1_(powermeter) [A]
            self.attr_KSEM.I_P1_A = round(self.ReadFloat32(222),2)
            # Phase 2
            # Plenticore Register 232: Current_phase_2_(powermeter) [A]
            self.attr_KSEM.I_P2_A = round(self.ReadFloat32(232),2)
            # Phase 3
            # Plenticore Register 242: Current_phase_3_(powermeter) [A]
            self.attr_KSEM.I_P3_A = round(self.ReadFloat32(242),2)
            # Leistung EVU
            # Plenticore Register 252: Total_active_power_(powermeter) [W]
            # Sensorposition 1 (Hausanschluss): (+)Hausverbrauch (-)Erzeugung
            # Sensorposition 2 (EVU Anschlusspunkt): (+)Bezug (-)Einspeisung            
            self.attr_KSEM.P_active_total = int(self.ReadFloat32(252))
            # Frequenz EVU
            # Plenticore Register 220: Frequency_(powermeter) [Hz]
            self.attr_KSEM.Freq = round(self.ReadFloat32(220),2)            
            # Leistung auf Phasen 1-3 EVU aus Kostal Plenticore lesen
            # Wechselrichter bekommt Daten von Energy Manager EM300
            # Phase 1
            # Plenticore Register 224: Active_power_phase_1_(powermeter) [W]
            self.attr_KSEM.P_P1_W = round(self.ReadFloat32(224),2)            
            # Phase 2
            # Plenticore Register 234: Active_power_phase_2_(powermeter) [W]
            self.attr_KSEM.P_P2_W = round(self.ReadFloat32(234),2) 
            # Phase 3
            # Plenticore Register 244: Active_power_phase_3_(powermeter) [A]
            self.attr_KSEM.P_P3_W = round(self.ReadFloat32(244),2) 
            # Spannung auf Phasen 1-3 EVU aus Kostal Plenticore lesen
            # Wechselrichter bekommt Daten von Energy Manager EM300
            # Phase 1
            # Plenticore Register 230: Voltage_phase_1_(powermeter) [V]
            self.attr_KSEM.U_P1_V = round(self.ReadFloat32(230),2)            
            # Phase 2
            # Plenticore Register 240: Voltage_phase_2_(powermeter) [V]
            self.attr_KSEM.U_P2_V = round(self.ReadFloat32(240),2)            
            # Phase 3
            # Plenticore Register 250: Voltage_phase_3_(powermeter) [V]
            self.attr_KSEM.U_P3_V = round(self.ReadFloat32(250),2)            
            # Plenticore Register 150: Actual_cos_phi []
            # ist Wirkfaktor            
            self.attr_KSEM.cosphi_actual = round(self.ReadFloat32(150),3)                        
        except:
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk            
            myLogging.openWBLog(self._pid, "Fehler beim Lesen der Modbus-Register KSEM300:" + str(self.IP)
                                + "(falsche WR-IP?)" + str(sys.exc_info()[0]))        
            #sys.exit(1)          

    def BatteryMgt(self):
        # Battery Mgt. relevant Register aus WR 1 auslesen:
        try:
            if self._Battery == 1:
                # Speicher am Planticore 1, erweiterte Control Register
                # Plenticore Register 1068: Battery Work capacity [Wh]
                # Kapazität Batterie
                self.Bat_Capacity = round (self.ReadFloat32(1068),2)
                # Plenticore Register 1070: Battery SerialNumber
                # Seriennumer der Batterie
                self.Bat_Serial = str(self.ReadString(1070))
                #Battery mgt. mode
                self.Bat_ControlMode = int(self.ReadInt32(1080))                                                                      
                #print("mode = " + self.Bat_ControlMode)
                # ist Kostal WR auf Battery Mgt. per Modbus Cfg
                #  0 = intern, 1 = digital IO's, 2= ModBus Extern            
                if self.Bat_ControlMode == 2:
                    # Speicher am Planticore 1, erweiterte Control Register
                    # Plenticore Register 1026 Start Address for Battery Mgt.
                    # Battery charge power (AC) setpoint, absolute [W]
                    self.Bat_AbsSet_AC_ChargePower = round(self.ReadFloat32(1026),2)
                    # Battery charge current (DC) setpoint, relative [%]
                    self.Bat_RelSet_DC_ChargeCurrent = round(self.ReadFloat32(1028),2)
                    # Battery charge power (AC) setpoint, relative [%]
                    self.Bat_RelSet_AC_ChargePower = round(self.ReadFloat32(1030),2)
                    #Battery charge current (DC) setpoint, absolute [A]
                    self.Bat_AbsSet_DC_ChargeCurrent = round(self.ReadFloat32(1032),2)                                
        except:
            # kein Zugriff auf WR1, also Abbruch und mit 0 initialisierte Variablen in die Ramdisk
            myLogging.openWBLog(self._pid, "Fehler beim Lesen der Modbus-Register BatteryMgt.:" + str(self._IP) + "(falsche IP?)" + str(sys.exc_info()[0]))        
            #sys.exit(1)

def main(argv=None):
    #if remotedebug==1 and Debug >= 2:
    #    try:
    #        debugpy.listen(5678)
    #    except:
    #      pass
    myPid = str(os.getpid()) 
    if len(sys.argv) ==5:
        # IP für Wechselrichter 1
        WR1IP = str(sys.argv[1])
        # IP für Wechselrichter 2
        WR2IP = str(sys.argv[2])
        # Battery vorhanden
        Battery = int(sys.argv[3])
        # IP für Wechselrichter 3
        WR3IP = str(sys.argv[4])
        WR4IP = "none"
        WR5IP = "none"
        ips= ipparser(WR3IP)
        #in IP3 kann ein aufeinanderfolgende Liste entalten sein "192.168.0.1-3"        
        if len(ips)>1:
            WR3IP = ips[0]
            WR4IP = ips[1]
            WR5IP = ips[2]
    else:
        myLogging.openWBLog(myPid, "Argumente fehlen oder sind fehlerhaft")
        sys.exit(1)
    
    #tdo: how to get openWB debug level
    _strdebug = os.environ.get("debug")
    
    if _strdebug != "none":
        try:      
            Debug = int(str(_strdebug))            
        except:
            Debug = 0    
    
    # Variablen initialisieren
    # Summenwerte
    PV_power_total = 0
    Total_yield = 0
    Yearly_yield = 0
    Monthly_yield = 0
    WR1=None
    WR2=None
    WR3=None
    WR4=None
    WR5=None
    
    WR1 = plenticore(myPid, WR1IP,Battery)            
    myLogging.openWBLog(myPid, "Wechselrichter Kostal Plenticore Config - WR1:" + str(WR1IP) + " -WR2:" + str(WR2IP) +
                        "\n -Battery:" + str(Battery) + " -WR3:" + str(WR3IP) + "-WR4:" + str(WR4IP) + "-WR5:" + str(WR5IP))
    
    WR1.ReadKSEM300()
    #Battery nur an WR1 erlaubt
    if Battery == 1:
        WR1.ReadBattery()
    
    WR1.ReadWechselrichter()    
    
    #zukünftige Implementierung von Battery Steuerung
    #Battery nur an WR1 erlaubt
    if WR1.BatMgt==1:
        WR1.BatteryMgt()
    
    # am WR2 darf keine Batterie sein, deswegen hier vereinfacht PV-Leistung = AC-Leistung des WR
    if WR2IP != "none":
        WR2= plenticore(myPid,WR2IP, 0)
        
    if WR3IP != "none":
        WR3= plenticore(myPid,WR3IP, 0)
        
    # am WR2 darf keine Batterie sein, deswegen hier vereinfacht PV-Leistung = AC-Leistung des WR
    if WR4IP != "none":
        WR4= plenticore(myPid,WR4IP, 0)
        
    if WR5IP != "none":
        WR5= plenticore(myPid,WR5IP, 0)
    
    # Summen der Erträge bestimmen
    PV_power_total=WR1.attr_WR.P_PV_AC_total
    myLogging.openWBLog(myPid, "WR1 Leistung = " + str(WR1.attr_WR.P_PV_AC_total) + "PV_total = " + str(PV_power_total))
    Total_yield = WR1.attr_WR.Total_yield 
    Monthly_yield = WR1.attr_WR.Monthly_yield 
    Yearly_yield = WR1.attr_WR.Yearly_yield
    
    # ggf. dekodierte Register WR 2 in entsprechende Typen umwandeln
    if WR2 is not None:
        WR2.ReadWechselrichter()
        PV_power_total +=  WR2.attr_WR.P_PV_AC_total
        myLogging.openWBLog(myPid, "WR2 Leistung = " + str(WR2.attr_WR.P_PV_AC_total) + "PV_total = " + str(PV_power_total))
        # Summen der Erträge bestimmen
        Total_yield +=  WR2.attr_WR.Total_yield
        Monthly_yield += WR2.attr_WR.Monthly_yield
        Yearly_yield += WR2.attr_WR.Yearly_yield
        
    # ggf. dekodierte Register WR 3 in entsprechende Typen umwandeln
    if WR3 is not None:
        WR3.ReadWechselrichter()
        PV_power_total +=  WR3.attr_WR.P_PV_AC_total
        myLogging.openWBLog(myPid, "WR3 Leistung = " + str(WR3.attr_WR.P_PV_AC_total) + "PV_total = " + str(PV_power_total))
        # Summen der Erträge bestimmen
        Total_yield +=  WR3.attr_WR.Total_yield
        Monthly_yield += WR3.attr_WR.Monthly_yield
        Yearly_yield += WR3.attr_WR.Yearly_yield
    
    # ggf. dekodierte Register WR 4 in entsprechende Typen umwandeln
    if WR4 is not None:
        WR4.ReadWechselrichter()
        PV_power_total +=  WR4.attr_WR.P_PV_AC_total
        myLogging.openWBLog(myPid, "WR4 Leistung = " + str(WR4.attr_WR.P_PV_AC_total) + "PV_total = " + str(PV_power_total))
        # Summen der Erträge bestimmen
        Total_yield +=  WR4.attr_WR.Total_yield
        Monthly_yield += WR4.attr_WR.Monthly_yield
        Yearly_yield += WR4.attr_WR.Yearly_yield
    
    # ggf. dekodierte Register WR 5 in entsprechende Typen umwandeln
    if WR5 is not None:
        WR5.ReadWechselrichter()
        PV_power_total +=  WR5.attr_WR.P_PV_AC_total
        myLogging.openWBLog(myPid, "WR5 Leistung = " + str(WR5.attr_WR.P_PV_AC_total) + "PV_total = " + str(PV_power_total))
        # Summen der Erträge bestimmen
        Total_yield +=  WR5.attr_WR.Total_yield
        Monthly_yield += WR5.attr_WR.Monthly_yield
        Yearly_yield += WR5.attr_WR.Yearly_yield

    # Batteriewerte Berechnen und übertragen
    if Battery == 1:        
        # Speicherladung muss durch Wandlungsverluste und internen Verbrauch korregiert werden
        # sonst wird ein falscher Hausverbrauch berechnet
        # die Verluste fallen hier unter den Tische, besser wäre auch HomeConsumption direkt zu openWB
        if WR1.attr_Bat.P_charge_discharge >=0:
            P_Charge_corrected = WR1.attr_Bat.P_charge_discharge - (WR1.attr_Bat.P_charge_discharge - WR1.attr_WR.P_Home_Cons_Bat)
            #print("Leistung Speicher Modbus= " + str(WR1.attr_Bat.P_charge_discharge) +
                  #" ,Speicherladung korrigiert= " + str(P_Charge_corrected) +
                  #", Leistung Hausverbrauch Bat actual = " + str(WR1.attr_WR.P_Home_Cons_Bat))          
        else:
            P_Charge_corrected = WR1.attr_Bat.P_charge_discharge            
                
        # Nachfolgende Werte nur in temporäre ramdisk, da die Module
        # Speicher und Bezug für die globalen Variablen zuständig sind
        # und dort die Übernahme in die entsprechende ramdisk erfolgt
        # Speicherleistung WR 1
        with open('/var/www/html/openWB/ramdisk/temp_speicherleistung', 'w') as f:
            f.write(str(P_Charge_corrected*-1))        
        # Speicher Ladestand von Speicher am WR 1
        with open('/var/www/html/openWB/ramdisk/temp_speichersoc', 'w') as f:
            f.write(str(WR1.attr_Bat.SoC_actual))
                
    # zunächst alle Summenwerte beider WR
    # Gesamtleistung AC PV-Module
    with open('/var/www/html/openWB/ramdisk/pvwatt', 'w') as f:
        f.write(str(PV_power_total*-1))
        #print("PV Leistung alle WR =" + str(PV_power_total*-1))    
    
    # Gesamtertrag in Wattstunden
    # schreibe den Wert nur wenn kein Speicher vorhanden ist. Wenn er da ist nutze die openWB PV Watt beschränkung
    if Battery!=1:
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
    # Leistung DC PV-Module
    # die Variablen dürfen nicht der Nomenklatur openWB enstprechen
    # Bsp. pv1watt oder pv2watt, da diese für PV Module 1 und 2 resaviert sind
    # und nicht aus einem Module geschrieben werden dürfen
    with open('/var/www/html/openWB/ramdisk/pvwatt1', 'w') as f:
        f.write(str(WR1.attr_WR.P_PV_AC_total*-1))
    # Gesamtertrag in Wattstunden
    with open('/var/www/html/openWB/ramdisk/pvkwh1', 'w') as f:
        f.write(str(WR1.attr_WR.Total_yield))
    # Gesamtertrag in Kilowattstunden
    with open('/var/www/html/openWB/ramdisk/pvkwhk1', 'w') as f:
        f.write(str(WR1.attr_WR.Total_yield / 1000))
    # Jahresertrag in Kilowattstunden
    with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk1', 'w') as f:
        f.write(str(WR1.attr_WR.Yearly_yield))
    # Monatsertrag in Kilowattstunden
    with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk1', 'w') as f:
        f.write(str(WR1.attr_WR.Monthly_yield))    

    if WR2 is not None:
        # Werte WR 2
        # Leistung DC PV-Module
        with open('/var/www/html/openWB/ramdisk/pvwatt2', 'w') as f:
            f.write(str(WR2.attr_WR.P_PV_AC_total*-1))
        # Gesamtertrag in Wattstunden
        with open('/var/www/html/openWB/ramdisk/pvkwh2', 'w') as f:
            f.write(str(WR2.attr_WR.Total_yield))
        # Gesamtertrag in Kilowattstunden
        with open('/var/www/html/openWB/ramdisk/pvkwhk2', 'w') as f:
            f.write(str(WR2.attr_WR.Total_yield / 1000))
        # Jahresertrag in Kilowattstunden
        with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk2', 'w') as f:
            f.write(str(WR2.attr_WR.Yearly_yield))
        # Monatsertrag in Kilowattstunden
        with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk2', 'w') as f:
            f.write(str(WR2.attr_WR.Monthly_yield))

    if WR3 is not None:
        # Werte WR 3
        # Leistung DC PV-Module
        with open('/var/www/html/openWB/ramdisk/pvwatt3', 'w') as f:
            f.write(str(WR3.attr_WR.P_PV_AC_total*-1))
        # Gesamtertrag in Wattstunden
        with open('/var/www/html/openWB/ramdisk/pvkwh3', 'w') as f:
            f.write(str(WR3.attr_WR.Total_yield))
        # Gesamtertrag in Kilowattstunden
        with open('/var/www/html/openWB/ramdisk/pvkwhk3', 'w') as f:
            f.write(str(WR3.attr_WR.Total_yield / 1000))
        # Jahresertrag in Kilowattstunden
        with open('/var/www/html/openWB/ramdisk/yearly_pvkwhk3', 'w') as f:
            f.write(str(WR3.attr_WR.Yearly_yield))
        # Monatsertrag in Kilowattstunden
        with open('/var/www/html/openWB/ramdisk/monthly_pvkwhk3', 'w') as f:
            f.write(str(WR3.attr_WR.Monthly_yield))
    
    # Bezug EVU
    with open('/var/www/html/openWB/ramdisk/temp_wattbezug', 'w') as f:
        f.write(str(WR1.attr_KSEM.P_active_total))
        #print("KSEM Watt Bezug = " + str(WR1.attr_KSEM.P_active_total))
    # Bezug Strom Phase 1
    with open('/var/www/html/openWB/ramdisk/temp_bezuga1', 'w') as f:
        f.write(str(WR1.attr_KSEM.I_P1_A))
    # Bezug Strom Phase 2
    with open('/var/www/html/openWB/ramdisk/temp_bezuga2', 'w') as f:
        f.write(str(WR1.attr_KSEM.I_P2_A))
    # Bezug Strom Phase 3
    with open('/var/www/html/openWB/ramdisk/temp_bezuga3', 'w') as f:
        f.write(str(WR1.attr_KSEM.I_P3_A))
    # Netzfrequenz
    with open('/var/www/html/openWB/ramdisk/temp_evuhz', 'w') as f:
        f.write(str(WR1.attr_KSEM.Freq))
    # Bezug Leistung Phase 1
    with open('/var/www/html/openWB/ramdisk/temp_bezugw1', 'w') as f:
        f.write(str(WR1.attr_KSEM.P_P1_W))
    # Bezug Leistung Phase 2
    with open('/var/www/html/openWB/ramdisk/temp_bezugw2', 'w') as f:
        f.write(str(WR1.attr_KSEM.P_P2_W))
    # Bezug Leistung Phase 3
    with open('/var/www/html/openWB/ramdisk/temp_bezugw3', 'w') as f:
        f.write(str(WR1.attr_KSEM.P_P3_W))
    # Spannung Phase 1
    with open('/var/www/html/openWB/ramdisk/temp_evuv1', 'w') as f:
        f.write(str(WR1.attr_KSEM.U_P1_V))
    # Spannung Phase 2
    with open('/var/www/html/openWB/ramdisk/temp_evuv2', 'w') as f:
        f.write(str(WR1.attr_KSEM.U_P2_V))
    # Spannung Phase 3
    with open('/var/www/html/openWB/ramdisk/temp_evuv3', 'w') as f:
        f.write(str(WR1.attr_KSEM.U_P3_V))
    # Wirkfaktor, wird nur einmal vom Wechselrichter ausgegeben,
    # und ist demnach für alle Phasen identisch
    with open('/var/www/html/openWB/ramdisk/temp_evupf1', 'w') as f:
        f.write(str(WR1.attr_KSEM.cosphi_actual))
    with open('/var/www/html/openWB/ramdisk/temp_evupf2', 'w') as f:
        f.write(str(WR1.attr_KSEM.cosphi_actual))
    with open('/var/www/html/openWB/ramdisk/temp_evupf3', 'w') as f:
        f.write(str(WR1.attr_KSEM.cosphi_actual))                           

if __name__ == "__main__":
    main(sys.argv)
