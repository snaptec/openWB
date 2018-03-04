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



Aktuelles Raspberry auf einem RPi3 wird zum testen genutzt

Für das Webinterface:

sudo apt-get install apache2

Für einige Module müssen Abhängigkeiten installiert werden:

sudo apt-get install jq






