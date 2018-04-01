<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Kevin Wieland" />
	<!-- Favicons (created with http://realfavicongenerator.net/)-->
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="img/favicons/manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<!-- Owl -->
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<!-- Animate.css -->
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome -->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>
<body>
<?php


$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {

	if(strpos($line, "debug=") !== false) {
		list(, $debugold) = explode("=", $line);
	}
	if(strpos($line, "sofortll=") !== false) {
		list(, $sofortllold) = explode("=", $line);
	}
	if(strpos($line, "sdmids1=") !== false) {
		list(, $sdmids1old) = explode("=", $line);
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
	if(strpos($line, "modbusevselanip=") !== false) {
		list(, $modbusevselanipold) = explode("=", $line);
	}
	if(strpos($line, "evsesources1=") !== false) {
		list(, $evsesources1old) = explode("=", $line);
	}
	if(strpos($line, "evseids1=") !== false) {
		list(, $evseids1old) = explode("=", $line);
	}
	if(strpos($line, "evselanips1=") !== false) {
		list(, $evselanips1old) = explode("=", $line);
	}
	if(strpos($line, "lastmanagement=") !== false) {
		list(, $lastmanagementold) = explode("=", $line);
	}
	if(strpos($line, "lastmmaxw=") !== false) {
		list(, $lastmmaxwold) = explode("=", $line);
	}

	if(strpos($line, "evsecons1=") !== false) {
		list(, $evsecons1old) = explode("=", $line);
	}

	if(strpos($line, "wattbezugmodul=") !== false) {
		list(, $wattbezugmodulold) = explode("=", $line);
	}

	if(strpos($line, "vzloggerip=") !== false) {
		list(, $vzloggeripold) = explode("=", $line);
	}
	if(strpos($line, "vzloggerline=") !== false) {
		list(, $vzloggerlineold) = explode("=", $line);
	}
	if(strpos($line, "vzloggerpvip=") !== false) {
		list(, $vzloggerpvipold) = explode("=", $line);
	}
	if(strpos($line, "vzloggerpvline=") !== false) {
		list(, $vzloggerpvlineold) = explode("=", $line);
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
	if(strpos($line, "sdm630modbuswrid=") !== false) {
		list(, $sdm630modbuswridold) = explode("=", $line);
	}
	if(strpos($line, "sdm630modbuswrsource=") !== false) {
		list(, $sdm630modbuswrsourceold) = explode("=", $line);
	}
	if(strpos($line, "sdm630modbuswrlanip=") !== false) {
		list(, $sdm630modbuswrlanipold) = explode("=", $line);
	}
	if(strpos($line, "socmodul=") !== false) {
		list(, $socmodulold) = explode("=", $line);
	}
	if(strpos($line, "hsocip=") !== false) {
		list(, $hsocipold) = explode("=", $line);
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
	if(strpos($line, "ladeleistungs1modul=") !== false) {
		list(, $ladeleistungs1modulold) = explode("=", $line);
	}
}





?>



<div class="container">

 
<button class="btn btn-primary btn-blue"><a href="index.php" class="btn btn-lg btn-block btn-blue">Zurück</a></button>



<form action="./tools/savesettings.php" method="POST">
<div class="row text-center">
	<h2>Konfiguration individuelle Einstellungen</h2>
</div><hr>
<div class="row">
	<b><label for="minimalstromstaerke">Minimalstromstaerke in A:</label></b>
	<input type="text" name="minimalstromstaerke" id="minimalstromstaerke" value="<?php echo $minimalstromstaerkeold ?>"><br>
</div>
<div class="row">
	Gültige Werte 6-10. Gibt an mit wieviel Ampere Mindestens geladen wird.<br><br>
</div>
<div class="row">
	<b><label for="maximalstromstaerke">Maximalstromstaerke in A:</label></b>
	<input type="text" name="maximalstromstaerke" id="maximalstromstaerke" value="<?php echo $maximalstromstaerkeold ?>"><br>
</div>
<div class="row">
	Gültige Werte 11-32. Gibt an mit wieviel Ampere Maximal geladen wird.<br><br>
</div>
<div class="row">
	<b><label for="debug">Debugmodus:</label></b>
	<input type="text" name="debug" id="debug" value="<?php echo $debugold ?>"><br>
</div>
<div class="row">
	Gültige Werte 0-2. 0=Debug aus, 1=Schreibe Regelwerte in das log, 2= Schreibe die Berechnungsgrundlage in das log.<br><br>
</div>
<div class="row"><hr>
	<h3>Nachtlademodus</h3>
</div>
<div class="row">
	<b><label for="nachtladen">Nachtladen:</label></b>
	<input type="text" name="nachtladen" id="nachtladen" value="<?php echo $nachtladenold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 0 oder 1. Definiert ob Nachts geladen werden soll. Ist auch bei Lademodus "Stop" aktiv!<br><br>
</div>
<div class="row">
	<b><label for="nachtll">Nachtladestromstärke:</label></b>
	<input type="text" name="nachtll" id="nachtll" value="<?php echo $nachtllold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 6-32. Ampere mit der nachts geladen werden soll<br><br>
</div>
<div class="row">
	<b><label for="nachtladenabuhr">Nachtladen Uhrzeit ab:</label></b>
	<input type="text" name="nachtladenabuhr" id="nachtladenabuhr" value="<?php echo $nachtladenabuhrold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 17-23. Ab wann Abends geladen werden soll<br><br>
</div>
<div class="row">
	<b><label for="nachtladenbisuhr">Nachtladen Uhrzeit bis:</label></b>
	<input type="text" name="nachtladenbisuhr" id="nachtladenbisuhr" value="<?php echo $nachtladenbisuhrold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 1-9. Bis wann morgens geladen werden soll<br><br>
</div>
<div class="row">
	<b><label for="nachtsoc">Nacht SOC:</label></b>
	<input type="text" name="nachtsoc" id="nachtsoc" value="<?php echo $nachtsocold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 1-99. Wenn SOC Modul vorhanden wird Nachts bis xx% SOC geladen in dem angegebenen Zeitfenster.<br><br>
</div>
<div class="row"><hr>
	<h3>PV Regelung</h3>
</div>
<div class="row">
	Die Kombination aus Mindestüberschuss und Abschaltüberschuss sollte sinnvoll gewählt werden.<br>
	Ansonsten wird im 10 Sekunden Takt die Ladung gestartet und gestoppt.<br>
	Es macht z.B. 1320 Watt mindestuberschuss und 900 Watt abschaltuberschuss Sinn<br>
</div>
<div class="row">
	<b><label for="mindestuberschuss">Mindestüberschuss:</label></b>
	<input type="text" name="mindestuberschuss" id="mindestuberschuss" value="<?php echo $mindestuberschussold ?>"><br>
</div>
<div class="row">
	Gültige Werte 0-9999. Mindestüberschuss in Watt bevor im Lademodus "Nur PV" die Ladung beginnt.<br> Soll wenig bis kein Netzbezug vorhanden sein macht ein Wert um 1300-1600 Sinn.<br><br>
</div>
<div class="row">
	<b><label for="abschaltuberschuss">Abschaltüberschuss:</label></b>
	<input type="text" name="abschaltuberschuss" id="abschaltuberschuss" value="<?php echo $abschaltuberschussold ?>"><br>
</div>
<div class="row">
	Gültige Werte 0-2000. Ab wieviel Watt Bezug abgeschaltet werden soll.<br>
Zunächst wird in jedem Zyklus die Ladeleistung Stufenweise bis auf 6A reduziert. Danach greift die Abschaltung.<br>
Sprich bis wieviel Watt soll bei 1320w Ladeleistung Netzbezug erlaubt sein<br>
Beispiel, bei 900 (watt) wird bei 1320w Ladeleistung 420Watt aus dem Netz bezogen. Werden mehr als 420 Watt bezogen, wird die Ladung gestoppt<br>
Der Wert ist für 1phasiges laden. Bei 3phasigem laden verdreifacht sich der Wert(automatisch). z.B. bei 900 Watt ergibt das bei 3960Watt Ladeleistung ein (erlaubter) Netzbezug bis 1260W(420W * 3)<br>
Bei einem abschaltuberschuss von 0 wird erst abgeschaltet wenn Bezug über 1320w bzw 3960w (3phasig) geht<br>
Bei einem abschaltuberschuss von 1320 wird abgeschaltet sobald mehr als 1W aus dem Netz bezogen wird<br>


</div>
<div class="text-center row"><hr>
	
	<h2>Konfiguration Module</h2>
</div>
<div class="row"><hr>
	<h3> Regelung der EVSE </h3>
</div>
<div class="row">
	<b><label for="evsecon">Anbindung an EVSE:</label></b>
	<input type="text" name="evsecon" id="evsecon" value="<?php echo $evseconold ?>"><br>
</div>
<div class="row">
	Gültige Werte dac, modbusevse. Weitere Konfiguration je nach Anbindung erforderlich! Modbus nur mit EVSE DIN getestet. Auf der EVSE muss Register 2003 auf 1 gesetzt werden (Deaktivierung analog Eingang), sonst kein beschreiben möglich<br><br>
</div>
<div class="row bg-success">
	<b><label for="dacregister">Dacregister:</label></b>
	<input type="text" name="dacregister" id="dacregister" value="<?php echo $dacregisterold ?>"><br>
</div>
<div class="row bg-success">
	Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP<br>Rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"<br><br>
</div>
<div class="row bg-info">
	<b><label for="modbusevsesource">ModbusEVSE Source:</label></b>
	<input type="text" name="modbusevsesource" id="modbusevsesource" value="<?php echo $modbusevsesourceold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.<br><br>
</div>
<div class="row bg-info">
	<b><label for="modbusevseid">ModbusEVSE ID:</label></b>
	<input type="text" name="modbusevseid" id="modbusevseid" value="<?php echo $modbusevseidold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte 1-254. Modbus ID der EVSE.<br><br>
</div>
<div class="row bg-info">
	<b><label for="modbusevselanip">ModbusEVSE LanIP Konverter:</label></b>
	<input type="text" name="modbusevselanip" id="modbusevselanip" value="<?php echo $modbusevselanipold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte IP. IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.<br><br>
</div>
<div class="row">
	<h4>Lastmanagement</h4>
</div>
<div class="row">
	<b><label for="lastmanagement">Lastmanagement:</label></b>
	<input type="text" name="lastmanagement" id="lastmanagement" value="<?php echo $lastmanagementold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 0 oder 1. Definiert ob es eine zweite WB gibt. Master & Slave werden gleichberechtigt bis Max Stromstaerke geregelt.<br><br>
</div>
<div class="row">
	<b><label for="lastmmaxw">Lastmanagement Max Watt:</label></b>
	<input type="text" name="lastmmaxw" id="lastmmaxw" value="<?php echo $lastmmaxwold ?>"><br>
</div>
<div class="row">
	Gültiger Wert 0 bis 44000. Definiert die maximalen Watt die Master & Slave WB gleichzeitig entnehmen dürfen.<br> Wird der Wert überschritten, werden beide WB gleichmäßig runtergeregelt !!noch nicht implementiert, Max Stromstärke gilt pro WB!!<br><br>
</div>
<div class="row">
	<h4>Slave1 WB</h4>
</div>
<div class="row bg-info">
	<b><label for="evsecons1">Anbindung der Slave 1 EVSE:</label></b>
	<input type="text" name="evsecons1" id="evsecons1" value="<?php echo $evsecons1old ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte modbusevse. Modbus nur mit EVSE DIN getestet. Auf der EVSE muss Register 2003 auf 1 gesetzt werden (Deaktivierung analog Eingang), sonst kein beschreiben möglich<br><br>
</div>
<div class="row bg-info">
	<b><label for="evsesources1">Slave 1 EVSE Source:</label></b>
	<input type="text" name="evsesources1" id="evsesources1" value="<?php echo $evsesources1old ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.<br><br>
</div>
<div class="row bg-info">
	<b><label for="evseids1">Slave 1 EVSE ID:</label></b>
	<input type="text" name="evseids1" id="evseids1" value="<?php echo $evseids1old ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte 1-254. Modbus ID der Slave 1 EVSE.<br><br>
</div>
<div class="row bg-info">
	<b><label for="ladeleistungs1modul">Ladeleistung Slave 1 Modul:</label></b>
	<input type="text" name="ladeleistungs1modul" id="ladeleistungs1modul" value="<?php echo $ladeleistungs1modulold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte sdm630modbuslls1. Modul zur Messung der Ladeleistung in der Slave WB.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdmids1">Slave 1 SDM Zähler ID:</label></b>
	<input type="text" name="sdmids1" id="sdmids1" value="<?php echo $sdmids1old ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte 1-254. Modbus ID des Slave 1 SDM Zählers in der WB.<br><br>
</div>
<div class="row bg-info">
	<b><label for="evselanips1">EVSE LanIP Konverter:</label></b>
	<input type="text" name="evselanips1" id="evselanips1" value="<?php echo $evselanips1old ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte IP. IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der Slave WB.<br><br>

</div>
<div class="row">	<hr>
	<h3> Strombezugsmessmodule (EVU-Übergabepunkt)</h3>
</div>
<div class="row">
	<b><label for="wattbezugmodul">Strombezugsmodul:</label></b>
	<input type="text" name="wattbezugmodul" id="wattbezugmodul" value="<?php echo $wattbezugmodulold ?>"><br>
</div>
<div class="row">
	Gültige Werte vzlogger, sdm630modbusbezug, none. Weitere Einstellungen je nach Modul beachten.<br><br>
</div>
<div class="row bg-success">
	<b><label for="vzloggerip">Vzlogger IP Adresse inkl Port:</label></b>
	<input type="text" name="vzloggerip" id="vzloggerip" value="<?php echo $vzloggeripold ?>"><br>
</div>
<div class="row bg-success">
	Gültige Werte IP:Port z.B. 192.168.0.12:8080. <br><br>
</div>
<div class="row bg-success">
	<b><label for="vzloggerline">Vzlogger Zeile:</label></b>
	<input type="text" name="vzloggerline" id="vzloggerline" value="<?php echo $vzloggerlineold ?>"><br>
</div>
<div class="row bg-success">
	Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br> Nun zählen in welcher Zeile der gewünschte Wert steht und diesen hier eintragen.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbusbezugsource">SDM Modbus Bezug Source:</label></b>
	<input type="text" name="sdm630modbusbezugsource" id="sdm630modbusbezugsource" value="<?php echo $sdm630modbusbezugsourceold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte /dev/ttyUSB0, /dev/virtualcom. Serieller Port an dem der SDM angeschlossen ist.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbusbezugid">SDM Modbus Bezug ID:</label></b>
	<input type="text" name="sdm630modbusbezugid" id="sdm630modbusbezugid" value="<?php echo $sdm630modbusbezugidold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbusbezuglanip">IP des Modbus/Lan Konverter:</label></b>
	<input type="text" name="sdm630modbusbezuglanip" id="sdm630modbusbezuglanip" value="<?php echo $sdm630modbusbezuglanipold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.<br><br>
</div>
<div class="row"><hr>
	<h3> PV Module </h3>
</div>
<div class="row">
	<b><label for="pvwattmodul">PV Modul:</label></b>
	<input type="text" name="pvwattmodul" id="pvwattmodul" value="<?php echo $pvwattmodulold ?>"><br>
</div>
<div class="row">
	Gültige Werte wr_fronius, sdm630modbuswr, vzloggerpv, none. Weitere Module auf Anfrage.<br><br>
</div>
<div class="row">
	<b><label for="wrfroniusip">WR Fronius IP:</label></b>
	<input type="text" name="wrfroniusip" id="wrfroniusip" value="<?php echo $wrfroniusipold ?>"><br>
</div>
<div class="row">
	Gültige Werte IP. IP Adresse Fronius Webinterface.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbuswrsource">SDM Modbus Wechselrichterleistung Source:</label></b>
	<input type="text" name="sdm630modbuswrsource" id="sdm630modbuswrsource" value="<?php echo $sdm630modbuswrsourceold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbuswrid">SDM Modbus Wechselrichterleistung ID:</label></b>
	<input type="text" name="sdm630modbuswrid" id="sdm630modbuswrid" value="<?php echo $sdm630modbuswridold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbuswrlanip">IP des Modbus/Lan Konverter:</label></b>
	<input type="text" name="sdm630modbuswrlanip" id="sdm630modbuswrlanip" value="<?php echo $sdm630modbuswrlanipold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.<br><br>
</div>
<div class="row bg-warning">
	<b><label for="vzloggerpvip">Vzloggerpv IP Adresse inkl Port:</label></b>
	<input type="text" name="vzloggerpvip" id="vzloggerpvip" value="<?php echo $vzloggerpvipold ?>"><br>
</div>
<div class="row bg-warning">
	Gültige Werte IP:Port z.B. 192.168.0.12:8080. <br><br>
</div>
<div class="row bg-warning">
	<b><label for="vzloggerpvline">Vzloggerpv Zeile:</label></b>
	<input type="text" name="vzloggerpvline" id="vzloggerpvline" value="<?php echo $vzloggerpvlineold ?>"><br>
</div>
<div class="row bg-warning">
	Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq ."<br> Nun zählen in welcher Zeile der gewünschte Wert steht und diesen hier eintragen.<br><br>
</div>

<div class="row"><hr>
	<h3> Ladeleistungsmessmodule </h3>
</div>
<div class="row">
	<b><label for="ladeleistungmodul">Ladeleistungmodul:</label></b>
	<input type="text" name="ladeleistungmodul" id="ladeleistungmodul" value="<?php echo $ladeleistungmodulold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte sdm630modbusll, none. Weitere Einstellungen je nach Modul beachten.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbusllsource">SDM Modbus Ladeleistung Source:</label></b>
	<input type="text" name="sdm630modbusllsource" id="sdm630modbusllsource" value="<?php echo $sdm630modbusllsourceold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbusllid">SDM Modbus Ladeleistung ID:</label></b>
	<input type="text" name="sdm630modbusllid" id="sdm630modbusllid" value="<?php echo $sdm630modbusllidold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.<br><br>
</div>
<div class="row bg-info">
	<b><label for="sdm630modbuslllanip">IP des Modbus/Lan Konverter:</label></b>
	<input type="text" name="sdm630modbuslllanip" id="sdm630modbuslllanip" value="<?php echo $sdm630modbuslllanipold ?>"><br>
</div>
<div class="row bg-info">
	Gültige Werte IP. Ist die source "virtualcomX" wird automatisch ein Lan Konverter genutzt.<br><br>
</div>
<div class="row"><hr>
	<h3> SOC Module </h3>
</div>
<div class="row">
	<b><label for="socmodul">SOC Modul:</label></b>
	<input type="text" name="socmodul" id="socmodul" value="<?php echo $socmodulold ?>"><br>
</div>
<div class="row">
	Gültige Werte none, soc_http. Wenn nicht vorhanden auf none setzen! Weitere Einstellungen im Modul selbst nötig. Andere auf Anfrage.<br><br>
</div>
<div class="row">
	<b><label for="hsocip">SOC Http Abfrage URL:</label></b>
	<input type="text" name="hsocip" id="hsocip" value="<?php echo $hsocipold ?>"><br>
</div>
<div class="row">
	Gültige Werte none, "url". URL für die Abfrage des Soc, Antwort muss der reine Zahlenwert sein.<br><br>








<button type="submit" class="btn btn-primary btn-green">Save</button>	 
 </form><br><br />
 
<button class="btn btn-primary btn-blue"><a href="index.php" class="btn btn-lg btn-block btn-blue">Zurück</a></button>

</div>
</body></html>

