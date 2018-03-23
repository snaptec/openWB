<html>
<body>
<a href="index.php">Zurück</a>
<?php


$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
//    if(substr($line, 0, 9) == 'sofortll=') {
//	    $sofortllold = substr($line, 9, 2);
//    }

	if(strpos($line, "debug=") !== false) {
		list(, $debugold) = explode("=", $line);
	}
	if(strpos($line, "sofortll=") !== false) {
		list(, $sofortllold) = explode("=", $line);
	}
	if(strpos($line, "minimalstromstaerke=") !== false) {
		list(, $minimalstromstaerkeold) = explode("=", $line);
	}
	if(strpos($line, "maximalstromstaerke=") !== false) {
		list(, $maximalstromstaerkeold) = explode("=", $line);
	}
	if(strpos($line, "evsecon=") !== false) {
		list(, $evseconold) = explode("=", $line);
	}
	if(strpos($line, "dacregister=") !== false) {
		list(, $dacregisterold) = explode("=", $line);
	}

	if(strpos($line, "modbusevsesource=") !== false) {
		list(, $modbusevsesourceold) = explode("=", $line);
	}

	if(strpos($line, "modbusevseid=") !== false) {
		list(, $modbusevseidold) = explode("=", $line);
	}

	if(strpos($line, "wattbezugmodul=") !== false) {
		list(, $wattbezugmodulold) = explode("=", $line);
	}

	if(strpos($line, "vzloggerip=") !== false) {
		list(, $vzloggeripold) = explode("=", $line);
	}

	if(strpos($line, "sdm630modbusbezugid=") !== false) {
		list(, $sdm630modbusbezugidold) = explode("=", $line);
	}

	if(strpos($line, "sdm630modbusbezuglanip=") !== false) {
		list(, $sdm630modbusbezuglanipold) = explode("=", $line);
	}
	if(strpos($line, "sdm630modbusbezugsource=") !== false) {
		list(, $sdm630modbusbezugsourceold) = explode("=", $line);
	}


	if(strpos($line, "pvwattmodul=") !== false) {
		list(, $pvwattmodulold) = explode("=", $line);
	}

	if(strpos($line, "wrfroniusip=") !== false) {
		list(, $wrfroniusipold) = explode("=", $line);
	}
	if(strpos($line, "ladeleistungmodul=") !== false) {
		list(, $ladeleistungmodulold) = explode("=", $line);
	}
	if(strpos($line, "sdm630modbusllid=") !== false) {
		list(, $sdm630modbusllidold) = explode("=", $line);
	}
	if(strpos($line, "sdm630modbusllsource=") !== false) {
		list(, $sdm630modbusllsourceold) = explode("=", $line);
	}
	if(strpos($line, "sdm630modbuslllanip=") !== false) {
		list(, $sdm630modbuslllanipold) = explode("=", $line);
	}
	if(strpos($line, "socmodul=") !== false) {
		list(, $socmodulold) = explode("=", $line);
	}
	if(strpos($line, "nachtladen=") !== false) {
		list(, $nachtladenold) = explode("=", $line);
	}
	if(strpos($line, "nachtll=") !== false) {
		list(, $nachtllold) = explode("=", $line);
	}
	if(strpos($line, "nachtladenabuhr=") !== false) {
		list(, $nachtladenabuhrold) = explode("=", $line);
	}
	if(strpos($line, "nachtladenbisuhr=") !== false) {
		list(, $nachtladenbisuhrold) = explode("=", $line);
	}
	if(strpos($line, "nachtsoc=") !== false) {
		list(, $nachtsocold) = explode("=", $line);
	}
	if(strpos($line, "mindestuberschuss=") !== false) {
		list(, $mindestuberschussold) = explode("=", $line);
	}
	if(strpos($line, "abschaltuberschuss=") !== false) {
		list(, $abschaltuberschussold) = explode("=", $line);
	}

}





?>




<form action="./tools/savesettings.php" method="POST">
	<h1>Konfiguration individuelle Einstellungen</h1>
	<b><label for="minimalstromstaerke">Minimalstromstaerke in A:</label></b>
	<input type="text" name="minimalstromstaerke" id="minimalstromstaerke" value="<?php echo $minimalstromstaerkeold ?>"><br>
	Gültige Werte 6-10. Gibt an mit wieviel Ampere Mindestens geladen wird.<br><br>
	<b><label for="maximalstromstaerke">Maximalstromstaerke in A:</label></b>
	<input type="text" name="maximalstromstaerke" id="maximalstromstaerke" value="<?php echo $maximalstromstaerkeold ?>"><br>
	Gültige Werte 11-32. Gibt an mit wieviel Ampere Maximal geladen wird.<br><br>
	<b><label for="debug">Debugmodus:</label></b>
	<input type="text" name="debug" id="debug" value="<?php echo $debugold ?>"><br>
	Gültige Werte 0-2. 0=Debug aus, 1=Schreibe Regelwerte in das log, 2= Schreibe die Berechnungsgrundlage in das log.<br><br>
	<h2>Nachtlademodus</h2>
	<b><label for="nachtladen">Nachtladen:</label></b>
	<input type="text" name="nachtladen" id="nachtladen" value="<?php echo $nachtladenold ?>"><br>
	Gültiger Wert 0 oder 1. Definiert ob Nachts geladen werden soll. Ist auch bei Lademodus "Stop" aktiv!<br><br>
	<b><label for="nachtll">Nachtladestromstärke:</label></b>
	<input type="text" name="nachtll" id="nachtll" value="<?php echo $nachtllold ?>"><br>
	Gültiger Wert 6-32. Ampere mit der nachts geladen werden soll<br><br>
	<b><label for="nachtladenabuhr">Nachtladen Uhrzeit ab:</label></b>
	<input type="text" name="nachtladenabuhr" id="nachtladenabuhr" value="<?php echo $nachtladenabuhrold ?>"><br>
	Gültiger Wert 17-23. Ab wann Abends geladen werden soll<br><br>
	<b><label for="nachtladenbisuhr">Nachtladen Uhrzeit bis:</label></b>
	<input type="text" name="nachtladenbisuhr" id="nachtladenbisuhr" value="<?php echo $nachtladenbisuhrold ?>"><br>
	Gültiger Wert 1-9. Bis wann morgens geladen werden soll<br><br>
	<b><label for="nachtsoc">Nacht SOC:</label></b>
	<input type="text" name="nachtsoc" id="nachtsoc" value="<?php echo $nachtsocold ?>"><br>
	Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
	<h2>PV Regelung</h2>
	Die Kombination aus Mindestüberschuss und Abschaltüberschuss sollte sinnvoll gewählt werden.<br>
	Ansonsten wird im 10 Sekunden Takt die Ladung gestartet und gestoppt.<br>
	Es macht z.B. 1320 Watt mindestuberschuss und 900 Watt abschaltuberschuss Sinn<br>
	<b><label for="mindestuberschuss">Mindestüberschuss:</label></b>
	<input type="text" name="mindestuberschuss" id="mindestuberschuss" value="<?php echo $mindestuberschussold ?>"><br>
	Gültige Werte 0-9999. Mindestüberschuss in Watt bevor im Lademodus "Nur PV" die Ladung beginnt.<br> Soll wenig bis kein Netzbezug vorhanden sein macht ein Wert um 1300-1600 Sinn.<br><br>
	<b><label for="abschaltuberschuss">Abschaltüberschuss:</label></b>
	<input type="text" name="abschaltuberschuss" id="abschaltuberschuss" value="<?php echo $abschaltuberschussold ?>"><br>
	Gültige Werte 0-2000. Ab wieviel Watt Bezug abgeschaltet werden soll.<br>
Zunächst wird in jedem Zyklus die Ladeleistung Stufenweise bis auf 6A reduziert. Danach greift die Abschaltung.<br>
Sprich bis wieviel Watt soll bei 1320w Ladeleistung Netzbezug erlaubt sein<br>
Beispiel, bei 900 (watt) wird bei 1320w Ladeleistung 420Watt aus dem Netz bezogen. Werden mehr als 420 Watt bezogen, wird die Ladung gestoppt<br>
Der Wert ist für 1phasiges laden. Bei 3phasigem laden verdreifacht sich der Wert(automatisch). z.B. bei 900 Watt ergibt das bei 3960Watt Ladeleistung ein (erlaubter) Netzbezug bis 1260W(420W * 3)<br>
Bei einem abschaltuberschuss von 0 wird erst abgeschaltet wenn Bezug über 1320w bzw 3960w (3phasig) geht<br>
Bei einem abschaltuberschuss von 1320 wird abgeschaltet sobald mehr als 1W aus dem Netz bezogen wird<br>



	<h1>Konfiguration Module</h1>
	<h2> Regelung der EVSE </h2>
	<b><label for="evsecon">Anbindung an EVSE:</label></b>
	<input type="text" name="evsecon" id="evsecon" value="<?php echo $evseconold ?>"><br>
	Gültige Werte dac, modbusevse. Weitere Konfiguration je nach Anbindung erforderlich! Modbus nur mit EVSE DIN getestet. Auf der EVSE muss Register 2003 auf 1 gesetzt werden (Deaktivierung analog Eingang), sonst kein beschreiben möglich<br><br>
	<b><label for="dacregister">Dacregister:</label></b>
	<input type="text" name="dacregister" id="dacregister" value="<?php echo $dacregisterold ?>"><br>
	Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP<br>Rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"<br><br>
	<b><label for="modbusevsesource">ModbusEVSE Source:</label></b>
	<input type="text" name="modbusevsesource" id="modbusevsesource" value="<?php echo $modbusevsesourceold ?>"><br>
	Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.<br><br>
	<b><label for="modbusevseid">ModbusEVSE ID:</label></b>
	<input type="text" name="modbusevseid" id="modbusevseid" value="<?php echo $modbusevseidold ?>"><br>
	Gültige Werte 1-254. Modbus ID der EVSE.<br><br>
	<h2> Strombezug Module </h2>
	<b><label for="wattbezugmodul">Strombezugsmodul:</label></b>
	<input type="text" name="wattbezugmodul" id="wattbezugmodul" value="<?php echo $wattbezugmodulold ?>"><br>
	Gültige Werte vzlogger, sdm630modbusbezug, none. Weitere Einstellungen je nach Modul beachten.<br><br>
	<b><label for="vzloggerip">Vzlogger IP Adresse inkl Port:</label></b>
	<input type="text" name="vzloggerip" id="vzloggerip" value="<?php echo $vzloggeripold ?>"><br>
	Gültige Werte IP:Port z.B. 192.168.0.12:8080. GGf muss die /var/www/html/openWB/modules/vzlogger/main.sh angepasst werden.<br> Ggf. bei Github einen Bug eröffnen!<br><br>
	<b><label for="sdm630modbusbezugid">SDM Modbus Bezug ID:</label></b>
	<input type="text" name="sdm630modbusbezugid" id="sdm630modbusbezugid" value="<?php echo $sdm630modbusbezugidold ?>"><br>
	Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.<br><br>
	<b><label for="sdm630modbusbezugsource">SDM Modbus Bezug Source:</label></b>
	<input type="text" name="sdm630modbusbezugsource" id="sdm630modbusbezugsource" value="<?php echo $sdm630modbusbezugsourceold ?>"><br>
	Gültige Werte /dev/ttyUSB0, /dev/virtualcom. Serieller Port an dem der SDM angeschlossen ist.<br><br>
	<b><label for="sdm630modbusbezuglanip">IP des Modbus/Lan Konverter:</label></b>
	<input type="text" name="sdm630modbusbezuglanip" id="sdm630modbusbezuglanip" value="<?php echo $sdm630modbusbezuglanipold ?>"><br>
	Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.<br><br>
	<h2> PV Module </h2>
	<b><label for="pvwattmodul">PV Modul:</label></b>
	<input type="text" name="pvwattmodul" id="pvwattmodul" value="<?php echo $pvwattmodulold ?>"><br>
	Gültige Werte wr_fronius, none. Weitere Module auf Anfrage.<br><br>
	<b><label for="wrfroniusip">WR Fronius IP:</label></b>
	<input type="text" name="wrfroniusip" id="wrfroniusip" value="<?php echo $wrfroniusipold ?>"><br>
	Gültige Werte IP. IP Adresse Fronius Webinterface.<br><br>
	<h2> Ladeleistungs Module </h2>
	<b><label for="ladeleistungmodul">Ladeleistungmodul:</label></b>
	<input type="text" name="ladeleistungmodul" id="ladeleistungmodul" value="<?php echo $ladeleistungmodulold ?>"><br>
	Gültige Werte sdm630modbusll, none. Weitere Einstellungen je nach Modul beachten.<br><br>
	<b><label for="sdm630modbusllsource">SDM Modbus Ladeleistung Source:</label></b>
	<input type="text" name="sdm630modbusllsource" id="sdm630modbusllsource" value="<?php echo $sdm630modbusllsourceold ?>"><br>
	Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich<br><br>
	<b><label for="sdm630modbusllid">SDM Modbus Ladeleistung ID:</label></b>
	<input type="text" name="sdm630modbusllid" id="sdm630modbusllid" value="<?php echo $sdm630modbusllidold ?>"><br>
	Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.<br><br>
	<b><label for="sdm630modbuslllanip">IP des Modbus/Lan Konverter:</label></b>
	<input type="text" name="sdm630modbuslllanip" id="sdm630modbuslllanip" value="<?php echo $sdm630modbuslllanipold ?>"><br>
	Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.<br><br>
	<h2> SOC Module </h2>
	<b><label for="socmodul">SOC Modul:</label></b>
	<input type="text" name="socmodul" id="socmodul" value="<?php echo $socmodulold ?>"><br>
	Gültige Werte none, soc_from_elastic. Wenn nicht vorhanden auf none setzen! Weitere Einstellungen im Modul selbst nötig. Andere auf Anfrage.<br><br>







<button type="submit" class="btn btn-primary">Save</button>	 
 </form>

<a href="index.php">Zurück</a>
</body></html>

