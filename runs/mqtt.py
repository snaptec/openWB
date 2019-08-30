import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
#config variablen später durch variablen ersetzen im Webinterface einstellbar
broker="localhost"
client_name="openWB"
port=1883
#verbindung zum Broker aufbauen
client =mqtt.Client(client_name)
client.connect(broker)
#initialwerte auf 0 setzen
oldlademodus="0"
oldpvwatt=0
oldevuwatt=0
oldnewwert=0
oldllaktuell=0
oldhausverbrauch=0
oldllkombiniert=0
oldllaktuells1=0
oldllaktuells2=0
oldllsoll=0
oldllsolls1=0
oldllsolls2=0
oldladestatus=0
oldsoc=0
oldsoc1=0
oldspeichersoc=0
oldspeicherleistung=0
oldplugstat=0
oldplugstats1=0
oldchargestat=0
oldchargestats1=0
def publishdata(einheit, wert, oldwert):
    newwert=open("/var/www/html/openWB/ramdisk/" + wert + "", "r").read().rstrip()
    #prüfen ob sich der Wert zum letzten geändert hat
    if oldwert != newwert:
        #ohne retain flag senden da er sich ständig ändert
        client.publish('openWB/'+ einheit + wert +'', newwert)
        time.sleep(0.05)
    return newwert
def publishdataretain(einheit, wert, oldwert):
    newwert=open("/var/www/html/openWB/ramdisk/" + wert + "", "r").read().rstrip()
    #prüfen ob sich der Wert zum letzten geändert hat
    if oldwert != newwert:
        #ohne retain flag senden da er sich ständig ändert
        client.publish('openWB/'+ einheit + wert +'', newwert, 1, retain=True)
        time.sleep(0.05)
    return newwert
#main loop
while True:

    #abfragen des aktuellen wertes
    oldpvwatt=publishdata("W", "pvwatt", oldpvwatt)
    oldevuwatt=publishdata("W", "wattbezug",oldevuwatt)
    oldllaktuell=publishdata("W", "llaktuell",oldllaktuell)
    oldhausverbrauch=publishdata("W", "hausverbrauch",oldhausverbrauch)
    oldllkombiniert=publishdata("W", "llkombiniert",oldllkombiniert)
    oldllaktuells1=publishdata("W", "llaktuells1",oldllaktuells1)
    oldllaktuells2=publishdata("W", "llaktuells2",oldllaktuells2)
    oldspeicherleistung=publishdataretain("W", "speicherleistung",oldspeicherleistung)

    oldllsoll=publishdataretain("A", "llsoll",oldllsoll)
    oldllsolls1=publishdataretain("A", "llsolls1",oldllsolls1)
    oldllsolls2=publishdataretain("A", "llsolls2",oldllsolls2)
    oldladestatus=publishdataretain("bool", "ladestatus",oldladestatus)
    oldsoc=publishdataretain("%", "soc",oldsoc)
    oldsoc1=publishdataretain("%", "soc1",oldsoc1)
    oldspeichersoc=publishdataretain("%", "speichersoc",oldspeichersoc)
    oldlademodus=publishdataretain("", "lademodus", oldlademodus)
    oldplugstat=publishdataretain("bool", "plugstat",oldplugstat)
    oldplugstats1=publishdataretain("bool", "plugstats1",oldplugstats1)
    oldchargestat=publishdataretain("bool", "chargestat",oldchargestat)
    oldchargestats1=publishdataretain("bool", "chargestat",oldchargestats1)

    time.sleep(0.5)
