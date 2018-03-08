# openWB
Control your simpleEVSEwb with a Raspberry for various purposes

-- noch unvollständig --
derzeitige Version ist noch nicht lauffähig
Wer das fertige stück software nachbauen und nutzen möchte muss sich noch ein paar (wenige) Wochen gedulden


Die Software steht zur nicht kommerziellen Nutzung frei für jeden zur Verfügung.
Spenden gerne an info@snaptec.org
Kommerzielle Anfragen ebenso an info@snaptec.org

# Haftungsausschluss
Es wird mit Kleinspannung aber auch 220V beim Anschluss der EVSE gearbeitet. 
Dies darf nur geschultes Personal. Die Anleitung ist ohne Gewähr und jegliches Handeln basiert auf eigene Gefahr.
Eine Fehlkonfiguration der Software kann höchstens ein nicht geladenes Auto bedeuten.
Falsch zusammengebaute Hardware kann lebensgefährlich sein. Im Zweifel diesen Part von einem Elektriker durchführen lassen.
Keine Gewährleistung für die Software - use at your own RISK!

# Wofür?
Steuerung einer EVSEwb für sofortiges laden, überwachung, pv überschussladung, Lastmanagement mehrerer WB und einiges mehr in Zukunft.


# Was wird benötigt?

Hardware:

- SimpleEVSEwb
- Raspberry pi 3
- 0-5V konverter MCP4725 (0-5V zur Steuerung der Ladestromstaerke an der EVSE)
- Stromzähler zur Ladeleistungsmessung (z.B. SDM630v2)
- USB-RS485 Converter
- Stromzähler zur Überschussmessung (z.b. SDM630v2, Zaehler mit IR Lesekopf und VZLogger usw..)
- Auslesen der PV (entsprechendes Modul fuer den Wechselrichter (Fronius derzeit unterstuetzt), oder z.B. SDM630)
- Relais am RPi zum Ein-/Ausschalten der EVSE
- RPi Netzteil
- Schuetz
- Ladekabel mit Steuerleitung
- Typ1/2 Stecker


# Installation

Hardware:

MCP4725 an Raspberry verkabeln

	Vdd an +5V Pin 2

	GND an GnD Pin 6

	SCL an GPIO3 SCL Pin 5

	SDA an GPIO2 SDA Pin 3



MCP4725 an SimpleEVSE

	A0 an GND EVSE

	Vout an AN EVSE




Raspbian installieren

	https://www.raspberrypi.org/downloads/raspbian/



Den i2c Bus aktivieren.

In der Konsole

        sudo raspi-config

ausführen.

	Punk 5 Interfacing Options auswählen

	P5 I2C auswählen und aktivieren.



In der Shell folgendes eingeben:

	curl -s https://raw.githubusercontent.com/snaptec/openWB/master/openwb-install.sh | sudo sh






In der Shell (nur nach updates erforderlich):

	chmod +x /var/www/html/openWB/modules/* 

	chmod +x /var/www/html/openWB/runs/*



Für den Produktiv betrieb, derzeit in testphase manuell ausführen:
	crontab -e
hier einfügen:

	* * * * /var/www/html/openWB/regel.sh >> /var/www/html/openWB/web/lade.log 2>&1 
	* * * * * sleep 10 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 20 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 30 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 40 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 50 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 

