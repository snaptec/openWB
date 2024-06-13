<!DOCTYPE html>
<html lang="de">
<?php
// set number of supported smarthome devices
$numDevices = 9;
?>
	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Kevin Wieland, Michael Ortenstein" />
		<!-- Favicons (created with http://realfavicongenerator.net/)-->
		<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
		<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
		<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
		<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
		<link rel="manifest" href="manifest.json">
		<link rel="shortcut icon" href="img/favicons/favicon.ico">
		<meta name="msapplication-TileColor" content="#00a8ff">
		<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
		<meta name="theme-color" content="#ffffff">

		<!-- Bootstrap -->
		<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
		<!-- Normalize -->
		<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="css/settings_style.css?ver=20200416-a">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">

			<form id="myForm">
				<h1>Einstellungen für SmartHome Geräte</h1>
				<?php for( $devicenum = 1; $devicenum <= $numDevices; $devicenum++ ) { ?>
					<div class="card border-secondary">
						<div class="card-header bg-secondary">
							<div class="form-group mb-0">
								<div class="form-row vaRow mb-0">
									<div class="col-4" id="deviceHeader<?php echo $devicenum; ?>">Gerät <?php echo $devicenum; ?></div>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" id="device_configuredDevices<?php echo $devicenum; ?>" name="device_configured" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<label class="btn btn-sm btn-outline-info">
												<input type="radio" name="device_configuredDevices<?php echo $devicenum; ?>" id="device_configuredDevices<?php echo $devicenum; ?>Off" data-option="0" value="0" checked="checked">Aus
											</label>
											<label class="btn btn-sm btn-outline-info">
												<input type="radio" name="device_configuredDevices<?php echo $devicenum; ?>" id="device_configuredDevices<?php echo $devicenum; ?>On" data-option="1" value="1">An
											</label>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card-body hide" id="device<?php echo $devicenum; ?>options">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="device_nameDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Name</label>
									<div class="col">
										<input id="device_nameDevices<?php echo $devicenum; ?>" name="device_name" class="form-control" type="text" required="required" minlength="3" maxlength="12" pattern="[a-zA-Z]*" inputmode="text" value="Name" data-default="Name" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Der Name muss aus 3-12 Zeichen bestehen und darf nur Buchstaben enthalten.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Gerätetyp</label>
									<div class="col">
										<select class="form-control" name="device_type" id="device_typeDevices<?php echo $devicenum; ?>" data-default="none" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<option value="none" data-option="none" selected="selected">Kein Gerät</option>
											<option value="shelly" data-option="shelly">Shelly oder Shelly plus</option>
											<option value="tasmota" data-option="tasmota">Tasmota</option>
											<option value="acthor" data-option="acthor">Acthor oder Elwa2</option>
											<option value="lambda" data-option="lambda">Lambda</option>
											<option value="elwa" data-option="elwa">Elwa</option>
											<option value="idm" data-option="idm">Idm</option>
											<option value="NXDACXX" data-option="NXDACXX">DAC 0.01V bis 10.0V</option>
											<option value="stiebel" data-option="stiebel">Stiebel</option>
											<option value="ratiotherm" data-option="ratiotherm">Ratiotherm</option>
											<option value="vampair" data-option="vampair">Vampair</option>
											<option value="http" data-option="http">Http</option>
											<option value="avm" data-option="avm">AVM</option>
											<option value="mystrom" data-option="mystrom">MyStrom</option>
											<option value="viessmann" data-option="viessmann">Viessmann</option>
											<option value="mqtt" data-option="mqtt">Mqtt</option>
											<option value="askoheat" data-option="askoheat">Askoheat</option>
										</select>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-none hide">
											Dieser Gerätetyp wird nicht in die Regelung eingebunden und es können keine Schalthandlungen ausgeführt oder Sensoren eingelesen werden. Es ist jedoch eine separate Leistungsmessung möglich, um reine Verbraucher zu erfassen.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-acthor hide">
											Heizstab Acthor der Firma my-PV<br>
											Im Web Frontend vom Heizstab muss unter "Steuerungs-Einstellungen" der Parameter "Ansteuerungs-Typ = Modbus TCP" und "Zeitablauf Ansteuerung = 120 Sek" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen.
											Mit dem Parameter Updategerät kann eine abweichende Sekundenzahl angegeben werden.<br>
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Acthor nicht zu stören.
											Wenn Acthor als Gerät 1 oder 2 definiert ist, wird die Warmwassertemperatur als Temp1 angezeigt (Modbusadresse 1001). Ebenso wird Temp2 (Modbusadresse 1030) und Temp3 (Modbusadresse 1031) angezeigt (falls angeschlossen).
											Elwa2 hat fast die gleich Schnittstelle wie Acthor.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-lambda hide">
											Wp der Firma lambda<br>
											Im Web Frontend der WP muss unter "Steuerungs-Einstellungen" der Parameter "Ansteuerungs-Typ = Modbus TCP" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen.
											Mit dem Parameter Updategerät kann eine abweichende Sekundenzahl angegeben werden.<br>
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.<br>
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Lambda nicht zu stören.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-mqtt hide">
											Generisches MQTT modul<br>
											Wenn Einschaltbedingung erreicht (Beispiel hier mit Device 4)<br>
											openWB/SmartHome/set/Devices/4/ReqRelay = 1<br>
											openWB/SmartHome/set/Devices/4/Ueberschuss = in Watt<br>
											Wenn Ausschaltbedingung erreicht<br>
											openWB/SmartHome/set/Devices/4/ReqRelay = 0<br>
											openWB/SmartHome/set/Devices/4/Ueberschuss = in Watt<br>
											ReqRelay gibt den Status vom Gerät aus Sicht openWb an (1 = eingeschaltet, 0 = ausgeschaltet)<br>
											Bei der periodischen Abfrage wird die aktuelle Leistung<br>
											openWB/SmartHome/set/Devices/4/Aktpower = in Watt erwartet<br>
											und der aktuelle Zähler in Wattstunden wird hier erwartet<br>
											openWB/SmartHome/set/Devices/4/Powerc<br>
											wenn kein Zähler übergeben oder 0 übergeben wird, wird der Zähler selber gerechnet<br>
											openWB/SmartHome/set/Devices/4/Ueberschuss = in Watt<br>
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-NXDACXX hide">
											DAC angesteuert über Lan. Der anliegende Überschuss wird in eine Voltzahl zwischen 0.01V und 10.0V umgewandelt. Bezug wird als 0 Volt übertragen.
											Wenn die Einschaltbedingung erreicht ist, wird alle 30 Sekunden der gerechnete Überschuss übertragen.<br>
											Der konkrete DAC Typ wird im Type definiert.<br>
											Mit dem Parameter Updategerät kann eine abweichende Sekundenzahl angegeben werden.<br>
											</span>
											<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-ratiotherm hide">
											Ratiothem Wärmepumpe. Anschluss via Modbus RTU (Elfin-EE11) auf CAN-EZ3.
											<span class="form-text small text-danger">Das Feature befindet sich noch in der Entwicklung!</span>
											</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-viessmann hide">
											Vitalcal 200-s Wärmepumpe mit LON Kommunikationsmodul und Vitogate 300. Wenn die Einschaltbedingung erreicht ist wird Komfortfunktion "Einmalige Warmwasserbereitung" außerhalb des Zeitprogramms gestartet. Für die "Einmalige Warmwasserbereitung" wird der Warmwassertemperatur-Sollwert 2 genutzt. In der Wp kann eingestellt werden, ob für diese Funktion  die Elektroheizung (Heizstab) benutzt werden soll.
											siehe auch https://openwb.de/forum/viewtopic.php?t=6593 für alternative Ansteuerungen 
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-elwa hide">
											Heizstab ELWA-E  der Firma my-PV<br>
											Im Web Frontend vom Heizstab muss unter Steuerungs-Einstellungen der Parameter "Ansteuerungs-Typ = Modbus TCP" und "Power Timeout = 120 Sek" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen.
											Mit dem Parameter Updategerät kann eine abweichende Sekundenzahl angegeben werden.
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Elwa nicht zu stören.
											Die Warmwassersicherstellung in Elwa kann genutzt werden. OpenWB erkennt dieses am Status und überträgt dann keinen Überschuss.
											Wenn Elwa als Gerät 1 oder 2 definiert ist, wird die Warmwassertemperatur als Temp1 angezeigt (Modbusadresse 1001).
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-askoheat hide">
											Heizstab Askoheat+ der Firma ASKOMA AG<br>
											Im web Frontend vom Heizstab muss unter Expertsetup / Setup 3 eine Statische IP Adresse und der Modbus TCP Port 502 (nicht 520) erfasst werden.
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen.
											Mit dem Parameter Updategerät kann eine abweichende Sekundenzahl angegeben werden.
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Askoheat+ nicht zu stören.
											Wenn Askoheat+ als Gerät 1 oder 2 definiert ist, wird die Temperatur von internen Sensort als Temp1 angezeigt (Modbusadresse 638).
										</span>										
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-idm hide">
											Wärmepumpe der Firma IDM mit Navigatorregelung 1.7/2.0<br>
											Im Web Frontend muss unter "Heizungsbauerebene / Konfiguration / PV-Signal": Auswahl "Gebäudeleittechnik / Smartfox" und unter "Heizungsbauerebene / Gebäudeleittechnik" der Parameter "Modbus TCP = Ein" und unter "Einstellungen / Photovoltaik" der Parameter "PV Überschuss = 0" gesetzt werden
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von IDM nicht zu stören.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-stiebel hide">
											Wärmepumpe der Firma Stiebel mit ISG (Servicewelt über Modbus) und SG Ready Eingang.<br>
											Im ISG web muss unter "Einstellungen / Energiemanagement" der Parameter "SGREADY = Ein" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird der Sg Ready Eingang von Betriebszustand 2 auf Betriebszustand 3 geschaltet.
											Wenn die Ausbedingung erreicht ist wird der Sg Ready Eingang von Betriebszustand 3 auf Betriebszustand 2 geschaltet.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-vampair hide">
											Wärmepumpe der Firma Solarfocus. Der aktuelle Überschuss wird übertragen.
											Im Servicemenü muss (durch eine Fachkraft) die Überstromnutzung aktiviert und auf Modbus TCP gestellt werden.
											Danach muss lediglich eine Ein- und Ausschaltschwelle für die Überstromnutzung eingestellt werden.
											Eine negative Ausschaltschwelle bedeutet, dass die Wärmepumpe die fehlende Leistung aus dem Netz bezieht.
											Die hier hinterlegte Ein- und Ausschaltschwelle sollte dann 1:1 in die openWB übertragen werden.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-http hide">
											Mit diesem Typ werden alle Geräte unterstützt, welche sich durch einfache Http-Aufrufe schalten lassen.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-avm hide">
											Mit diesem Typ werden SmartHome Geräte von AVM unterstützt, welche über eine Fritz!Box verbunden sind.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-mystrom hide">
											Mit diesem Typ werden SmartHome Geräte des Herstellers MyStrom unterstützt.<br>
										</span>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly hide">
									<!-- Shelly -->
								<div class="form-group">
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Shelly mit Authentication</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" id="device_shauthDevices<?php echo $devicenum; ?>" name="device_shauth" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<label class="btn btn-outline-info">
													<input type="radio" name="device_shauthDevices<?php echo $devicenum; ?>" id="device_shauth<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
												</label>
												<label class="btn btn-outline-info">
													<input type="radio" name="device_shauthDevices<?php echo $devicenum; ?>" id="device_shauth<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
												</label>
											</div>
										</div>
										<span class="form-text small">Wenn diese Option aktiviert wird, wird für den Shelly eine Userid und ein Password verlangt. Läuft momentan nur für shell ohne plus.</span>
									</div>	
									<div class="device<?php echo $devicenum; ?>shauth hide">
										<div class="form-row mb-1">
											<label for="device_shusernameDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Benutzername</label>
												<div class="col">
													<input id="device_shusernameDevices<?php echo $devicenum; ?>" name="device_shusername" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_shpasswordDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Passwort</label>
												<div class="col">
													<input id="device_shpasswordDevices<?php echo $devicenum; ?>" name="device_shpassword" class="form-control" type="password" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												</div>
										</div>
									</div>									
								</div>									
									<!-- Shellyend -->
								<hr class="border-secondary">
								<div class="form-row mb-1">
									<label for="device_chanDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Kanal- / Meter-Auswahl</label>
									<div class="col">
										<select class="form-control" name="device_chan" id="device_chanDevices<?php echo $devicenum; ?>" data-default="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<option value="0" data-option="0" selected="selected">Kanal 0 / alle Meter summiert</option>
											<option value="1" data-option="1">Kanal 0 / Meter 1</option>
											<option value="2" data-option="2">Kanal 1 / Meter 2</option>
											<option value="3" data-option="3">Kanal 2 / Meter 3</option>
											<option value="4" data-option="4">Kanal 3 / Meter 4</option>
											<option value="5" data-option="5">Kanal 4 / Meter 5</option>
											<option value="6" data-option="6">Kanal 5 / Meter 6</option>
										</select>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-none hide">
								<hr class="border-secondary">
								<div class="form-row mb-1">
									<label for="device_nonewattDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Separate Leistungsaufnahme in Watt</label>
									<div class="col">
										<input id="device_nonewattDevices<?php echo $devicenum; ?>" name="device_nonewatt" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="10000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Wenn separate Leistungsaufnahme in Watt kleiner/gleich ist, wird das Gerät als ausgeschaltet (rot) gezeigt, anderenfalls grün .</span>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-idm hide">
								<hr class="border-secondary">
								<div class="form-row mb-1">
									<label for="device_idmnavDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Navigator Version</label>
									<div class="col">
										<input id="device_idmnavDevices<?php echo $devicenum; ?>" name="device_idmnav" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="2" data-default="2" value="2" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Hauptversion vom Navigator 1 oder 2</span>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-NXDACXX hide">
								<hr class="border-secondary">
								<div class="form-row mb-1">
									<label for="device_nxdacxxuebDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Maximaler Überschuss</label>
									<div class="col">
										<input id="device_nxdacxxuebDevices<?php echo $devicenum; ?>" name="device_nxdacxxueb" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="32000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Maximal verwertbarer Überschuss des hier gewählten Gerät in Watt = v10.0. Es wird kein grösserer Wert übertragen.</span>
									</div>
								</div>
									<div class="form-row mb-1">
										<label for="device_nxdacxxtypeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">DAC Typ</label>
										<div class="col">
											<select class="form-control" name="device_nxdacxxtype" id="device_nxdacxxtypeDevices<?php echo $devicenum; ?>" data-default="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<option value="0" data-option="0">N4Dac02</option>
												<option value="1" data-option="1">DA02</option>
												<option value="2" data-option="2">M120T von Pigeon</option>
												<option value="3" data-option="3">AA02B</option>												
											</select>
											<span class="form-text small">
												Hier ist das installierte Modell auszuwählen.
											</span>
										</div>
									</div>
								<div class="form-row mb-1">
									<label for="device_dacportDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Modbusport des DAC</label>
									<div class="col">
										<input id="device_dacportDevices<?php echo $devicenum; ?>" name="device_dacport" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="9999" data-default="8899" value="8899"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Standardeinstellungen:8899 <br>
										</span>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-acthor device<?php echo $devicenum; ?>-option-lambda device<?php echo $devicenum; ?>-option-elwa device<?php echo $devicenum; ?>-option-idm device<?php echo $devicenum; ?>-option-stiebel device<?php echo $devicenum; ?>-option-avm device<?php echo $devicenum; ?>-option-mystrom device<?php echo $devicenum; ?>-option-vampair device<?php echo $devicenum;  ?>-option-viessmann device<?php echo $devicenum;  ?>-option-ratiotherm device<?php echo $devicenum;  ?>-option-askoheat device<?php echo $devicenum;  ?>-option-NXDACXX hide">
								<hr class="border-secondary">
								<div class="form-row mb-1">
									<label for="device_ipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input id="device_ipDevices<?php echo $devicenum; ?>" name="device_ip" class="form-control" type="text" required="required" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-avm hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_usernameDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input id="device_usernameDevices<?php echo $devicenum; ?>" name="device_username" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="device_passwordDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input id="device_passwordDevices<?php echo $devicenum; ?>" name="device_password" class="form-control" type="password" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="device_actorDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Aktor</label>
										<div class="col">
											<input id="device_actorDevices<?php echo $devicenum; ?>" name="device_actor" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">Hier ist der Name des Gerätes einzutragen, wie er in der Fritz!Box angezeigt wird.</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-http hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_leistungurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Leistungs-URL</label>
										<div class="col">
											<input id="device_leistungurlDevices<?php echo $devicenum; ?>" name="device_leistungurl" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">
												Die hier angegebene URL wird aufgerufen, um die aktuelle Leistung des Geräts zu erhalten.<br>
												<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span><br>
												Falls keine URL vorhanden ist, kann eine der folgenden angegeben werden:<br>
												127.0.0.1/openWB/packages/modules/smarthome/http/dummyurl.php. Diese URL gibt immer den Wert 0 zurück.(Device immer aus)<br>
												127.0.0.1/openWB/packages/modules/smarthome/http/dummyurl1.php?d=nummerdevice. Diese URL gibt den Wert 0 oder 100 zurück. Je nachdem ob das Smarthomedevice gerade läuft<br>
												127.0.0.1/openWB/packages/modules/smarthome/http/dummyurl2.php. Diese URL gibt immer den Wert 100 zurück. (Device immer an)<br>
												In der URL kann ein Parameter angegeben werden, der den aktuellen Überschuss an das Gerät übermittelt. Hierzu ist folgender Platzhalter in der URL zu verwenden (inklusive der spitzen Klammern):<br>
												<span class="text-info">&lt;openwb-ueberschuss&gt;</span>
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="device_stateurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Status-URL</label>
										<div class="col">
											<input id="device_stateurlDevices<?php echo $devicenum; ?>" name="device_stateurl" class="form-control" type="text" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">
												Die hier angegebene URL wird aufgerufen, um den aktuellen Status (1 = an, 0 = aus) des Geräts zu erhalten. <br>
												Der Parameter ist optional und kann somit auch leer gelassen werden. In diesem Fall wird der Parameter mit "none" vorbelegt und
												die Erkennung, ob das Gerät angeschaltet ist, wird weiterhin über die Leistung ermittelt. <br>
											</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-elwa hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_manwattDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Manuelle Leistung</label>
										<div class="col">
											<input id="device_manwattDevices<?php echo $devicenum; ?>" name="device_manwatt" class="form-control" type="number" min="0" max="30000" step="1" required="required" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">
												Hier die Leistung angebenen, die beim manuellen Modus beim EInschalten vom Gerät fest übertragen wird. Funktion noch in Entwicklung.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-idm hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_maxuebDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Maximale Leistungsaufnahme/Überschuss bei PV Betrieb</label>
										<div class="col">
											<input id="device_maxuebDevices<?php echo $devicenum; ?>" name="device_maxueb" class="form-control" type="number" min="0" max="30000" step="1" required="required" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">
												Hier ist die maximale Leistungsaufnahme anzugeben, die idm bei PV Betrieb nicht überschreiten soll. Bei 0 gibt es keine Limitierung bezüglich dem maximal zu übergebenen Überschuss. <br>
												Sonst wird der zu übergebene Überschuss wie folgt gerechnet: 										
												maximal zu übergeber Überschuss = maximale Leistungsaufnahme - aktuelle Leistungsaufnahme
												<br>
												Sofern die aktuelle Leistungsaufnahme bereits grösser als die maximale Leistungsaufnahme ist, wird gar kein Überschuss mehr übergeben im PV Betrieb.

											</span>
										</div>
									</div>
								</div>
							</div>

							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-acthor hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_acthortypeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Modell</label>
										<div class="col">
											<select class="form-control" name="device_acthortype" id="device_acthortypeDevices<?php echo $devicenum; ?>" data-default="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<option value="M1" data-option="M1">Acthor M1</option>
												<option value="M3" data-option="M3">Acthor M3</option>
												<option value="E2M1" data-option="E2M1">Elwa2 M1</option>
												<option value="E2M3" data-option="E2M3">Elwa2 M3</option>
												<option value="9s" data-option="9s">Acthor 9s</option>
												<option value="9s18" data-option="9s18">Acthor 9s Dual 18k</option>
												<option value="9s27" data-option="9s27">Acthor 9s boost 27k</option>
												<option value="9s45" data-option="9s45">Acthor 9s boost 45k</option>
											</select>
											<span class="form-text small">
												Hier ist das installierte Modell auszuwählen.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="device_acthorpowerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Installierte Leistung</label>
										<div class="col">
											<input id="device_acthorpowerDevices<?php echo $devicenum; ?>" name="device_acthorpower" class="form-control" type="number" min="0" max="50000" step="100" required="required" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">
												Hier bitte die an den Acthor angeschlossene Leistung in Watt angeben.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-lambda hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_lambdauebDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Überschuss...</label>
										<div class="col">
											<select class="form-control" name="device_lambdaueb" id="device_lambdauebDevices<?php echo $devicenum; ?>" data-default="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<option value="UP" data-option="UP">Überschuss als positive Zahl übertragen, Bezug negativ</option>
												<option value="UN" data-option="UN">Überschuss als negative Zahl übertragen, Bezug positiv</option>
												<option value="UZ" data-option="UZ">Überschuss als positive Zahl übertragen, Bezug als 0</option>
											</select>
											<span class="form-text small">
												Bezieht sich auf die Modbusadresse 102, wie ist Überschuss zu übertragen.Muss in der WP (Konfiguration E-Manager) genau gleich eingestellt sein.<br>
												Lambda -> OpenWb<br>
												Pos E-überschuss -> Überschuss als positive Zahl übertragen, Bezug negativ <br>
												Neg E-überschuss -> Überschuss als negative Zahl übertragen, Bezug positiv <br>
												E-Eintrag -> Überschuss als positive Zahl übertragen, Bezug als 0<br>
											</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-idm hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="device_idmuebDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Überschuss...</label>
										<div class="col">
											<select class="form-control" name="device_idmueb" id="device_idmuebDevices<?php echo $devicenum; ?>" data-default="UZ" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<option value="UP" data-option="UP">Überschuss als positive Zahl übertragen, Bezug negativ</option>
												<option value="UZ" data-option="UZ">Überschuss als positive Zahl übertragen, Bezug als 0</option>
											</select>
											<span class="form-text small">
												Bezieht sich auf die Modbusadresse 74, wie ist Überschuss zu übertragen.<br>
												Neue Möglichkeit  -> Überschuss als positive Zahl übertragen, Bezug negativ <br>
												bisheriges Verhalten -> Überschuss als positive Zahl übertragen, Bezug als 0<br>
											</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-acthor device<?php echo $devicenum; ?>-option-lambda device<?php echo $devicenum; ?>-option-elwa device<?php echo $devicenum; ?>-option-idm device<?php echo $devicenum; ?>-option-stiebel device<?php echo $devicenum; ?>-option-vampair device<?php echo $devicenum; ?>-option-avm device<?php echo $devicenum; ?>-option-mystrom device<?php echo $devicenum; ?>-option-http device<?php echo $devicenum; ?>-option-mqtt device<?php echo $devicenum;  ?>-option-askoheat device<?php echo $devicenum;  ?>-option-ratiotherm device<?php echo $devicenum;  ?>-option-NXDACXX device<?php echo $devicenum; ?>-option-viessmann hide">
								<hr class="border-secondary">
								<div class="form-group">
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Gerät kann schalten</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" id="device_canSwitchDevices<?php echo $devicenum; ?>" name="device_canSwitch" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<label class="btn btn-outline-info">
													<input type="radio" name="device_canSwitchDevices<?php echo $devicenum; ?>" id="device_canSwitch<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
												</label>
												<label class="btn btn-outline-info">
													<input type="radio" name="device_canSwitchDevices<?php echo $devicenum; ?>" id="device_canSwitch<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
												</label>
											</div>
											<span class="form-text small">Ist diese Option aktiviert, dann wird das Gerät anhand des Überschusses automatisch oder manuell geschaltet.</span>
										</div>
									</div>
								</div>
								<div class="device<?php echo $devicenum; ?>canSwitch">
									<hr class="border-secondary">
									<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-http hide">
										<div class="form-group">
											<div class="form-row mb-1">
												<label for="device_einschalturlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Einschalt-URL</label>
												<div class="col">
													<input id="device_einschalturlDevices<?php echo $devicenum; ?>" name="device_einschalturl" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<span class="form-text small">
														Die hier angegebene URL wird aufgerufen, um das Gerät einzuschalten.<br>
														<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="device_ausschalturlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschalt-URL</label>
												<div class="col">
													<input id="device_ausschalturlDevices<?php echo $devicenum; ?>" name="device_ausschalturl" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<span class="form-text small">
														Die hier angegebene URL wird aufgerufen, um das Gerät auszuschalten.<br>
														<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
													</span>
												</div>
											</div>
										</div>
									</div>
									<div class="form-group">
										<div class="form-row mb-1">
											<label for="device_mineinschaltdauerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Mindesteinschaltdauer</label>
											<div class="col">
												<input id="device_mineinschaltdauerDevices<?php echo $devicenum; ?>" name="device_mineinschaltdauer" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="10000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Parameter in Minuten, wie lange das Gerät nach Einschalten mindestens aktiviert bleibt.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_mindayeinschaltdauerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Mindesteinschaltdauer pro Tag</label>
											<div class="col">
												<input id="device_mindayeinschaltdauerDevices<?php echo $devicenum; ?>" name="device_mindayeinschaltdauer" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="10000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Parameter in Minuten, wie lange das Gerät pro Tag mindestens aktiviert bleibt. Siehe auch "Spätestens fertig um"</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_maxeinschaltdauerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Maximaleinschaltdauer</label>
											<div class="col">
												<input id="device_maxeinschaltdauerDevices<?php echo $devicenum; ?>" name="device_maxeinschaltdauer" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1500" data-default="1440" value="1440" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Parameter in Minuten, wie lange das Gerät pro Tag maximal aktiviert sein darf. Der Zähler wird nächtlich zurückgesetzt. 1440 Minuten sind 24 Stunden.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_startTimeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Frühster Start um</label>
											<div class="col">
												<input id="device_startTimeDevices<?php echo $devicenum; ?>" name="device_startTime" class="form-control" type="text" pattern="^([01]{0,1}\d|2[0-3]):[0-5]\d" maxlength="5" required data-default="00:00" value="00:00" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Einschaltbedingungen gelten erst ab der definierten Uhrzeit. Ausschaltbedingungen gelten den ganzen Tag. Gilt nur für Einschaltbedingung.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_endTimeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Spätester Start um</label>
											<div class="col">
												<input id="device_endTimeDevices<?php echo $devicenum; ?>" name="device_endTime" class="form-control" type="text" pattern="^([01]{0,1}\d|2[0-3]):[0-5]\d" maxlength="5" required data-default="00:00" value="00:00" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Einschaltbedingungen gelten nur bis zu der definierten Uhrzeit.Ausschaltbedingungen gelten den ganzen Tag.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_finishTimeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Spätestens fertig um</label>
											<div class="col">
												<input id="device_finishTimeDevices<?php echo $devicenum; ?>" name="device_finishTime" class="form-control" type="text" pattern="^([01]{0,1}\d|2[0-3]):[0-5]\d" maxlength="5" required data-default="00:00" value="00:00" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Wenn das Gerät heute noch nicht eingeschaltet wurde, wird es unabhängig vom Überschuss eingeschaltet unter Berücksichtigung der Mindesteinschaltdauer pro Tag oder der Mindesteinschaltdauer, so dass es zur angegebenen Uhrzeit fertig ist.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_onuntilTimeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Immer an vor</label>
											<div class="col">
												<input id="device_onuntilTimeDevices<?php echo $devicenum; ?>" name="device_onuntilTime" class="form-control" type="text" pattern="^([01]{0,1}\d|2[0-3]):[0-5]\d" maxlength="5" required data-default="00:00" value="00:00" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Das Gerät wird bis zu dieser Uhrzeit eingeschaltet, unabhängig vom Überschuss unter Berücksichtigung der maximalen Einschaltdauer.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_onTimeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Immer an nach</label>
											<div class="col">
												<input id="device_onTimeDevices<?php echo $devicenum; ?>" name="device_onTime" class="form-control" type="text" pattern="^([01]{0,1}\d|2[0-3]):[0-5]\d" maxlength="5" required data-default="00:00" value="00:00" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Das Gerät wird ab dieser Uhrzeit eingeschaltet, unabhängig vom Überschuss unter Berücksichtigung der maximalen Einschaltdauer.</span>
											</div>
										</div>

										<div class="form-row mb-1">
											<label for="device_offTimeDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Immer aus nach</label>
											<div class="col">
												<input id="device_offTimeDevices<?php echo $devicenum; ?>" name="device_offTime" class="form-control" type="text" pattern="^([01]{0,1}\d|2[0-3]):[0-5]\d" maxlength="5" required data-default="00:00" value="00:00" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Das Gerät wird ab dieser Uhrzeit ausgeschaltet, und für den laufenden Tag nicht mehr eingeschaltet.</span>
											</div>
										</div>
									</div>
									<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-mqtt device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-http device<?php echo $devicenum; ?>-option-avm device<?php echo $devicenum; ?>-option-mystrom hide">
										<hr class="border-secondary">
										<div class="form-group">
											<div class="form-row mb-1">
												<label class="col-md-4 col-form-label">Anlauferkennung</label>
												<div class="col">
													<div class="btn-group btn-group-toggle btn-block" id="device_startupDetectionDevices<?php echo $devicenum; ?>" name="device_startupDetection" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
														<label class="btn btn-outline-info">
															<input type="radio" name="device_startupDetectionDevices<?php echo $devicenum; ?>" id="device_startupDetection<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
														</label>
														<label class="btn btn-outline-info">
															<input type="radio" name="device_startupDetectionDevices<?php echo $devicenum; ?>" id="device_startupDetection<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
														</label>
													</div>
													<span class="form-text small">
														Durch diese Option wird das angeschlossene Gerät täglich um 0:01 Uhr eingeschaltet. Wenn erkannt wird, dass das Gerät aktiviert wird (Leistungsaufnahme ist länger als "Zeit im Standby" größer als eingetragener "Verbrauch im Standby"), wird das Gerät direkt ausgeschaltet, falls die Einschaltschwelle nicht erreicht ist. Sobald die Einschaltschwelle erreicht wird, wird das Gerät erneut aktiviert.<br>
														Somit kann z. B. eine Waschmaschine am Morgen im Standby befüllt und eingeschaltet werden. Sie läuft aber erst richtig an, wenn genügend Überschuss vorhanden ist.
												</div>
											</div>
											<div class="device<?php echo $devicenum; ?>startupDetection hide">
												<div class="form-row mb-1">
													<label for="device_standbyPowerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Verbrauch im Standby</label>
													<div class="col">
														<input id="device_standbyPowerDevices<?php echo $devicenum; ?>" name="device_standbyPower" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
														<span class="form-text small">Leistungsaufnahme in Watt, wenn das Gerät nicht läuft.</span>
													</div>
												</div>
												<div class="form-row mb-1">
													<label for="device_standbyDurationDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Zeit im Standby</label>
													<div class="col">
														<input id="device_standbyDurationDevices<?php echo $devicenum; ?>" name="device_standbyDuration" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="86400" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
														<span class="form-text small">Dauer in Sekunden.</span>
													</div>
												</div>
												<div class="form-row mb-1">
													<label class="col-md-4 col-form-label">Anlauferkennung mehrmals pro Tag durchführen</label>
													<div class="col">
														<div class="btn-group btn-group-toggle btn-block" id="device_startupMulDetectionDevices<?php echo $devicenum; ?>" name="device_startupMulDetection" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
															<label class="btn btn-outline-info">
																<input type="radio" name="device_startupMulDetectionDevices<?php echo $devicenum; ?>" id="device_startupMulDetection<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
															</label>
															<label class="btn btn-outline-info">
																<input type="radio" name="device_startupMulDetectionDevices<?php echo $devicenum; ?>" id="device_startupMulDetection<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
															</label>
														</div>
														<span class="form-text small">Diese Option sorgt dafür, dass das Gerät nach absolvieren der Mindesteinschaltdauer sofort wieder in den Standby schaltet. Wenn die Option nicht gesetzt ist, bleibt das Gerät an und wird erst beim Erreichen der Ausschaltbedingung abgestellt.</span>
														</span>
														<span class="form-text small text-danger">Das Feature befindet sich noch in der Entwicklung!</span>
													</div>
												</div>
											</div>
										</div>
									</div>
									<hr class="border-secondary">
									<div class="form-group">
										<div class="form-row mb-1">
											<label class="col-md-4 col-form-label">Bei Autoladen...</label>
											<div class="col">
												<div class="btn-group btn-group-toggle btn-block" id="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" name="device_deactivateWhileEvCharging" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" id="device_deactivateWhileEvCharging<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">nichts tun
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" id="device_deactivateWhileEvCharging<?php echo $devicenum; ?>1" data-option="1" value="1">Ausschaltschwelle anpassen
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateWhileEvChargingDevices<?php echo $devicenum; ?>" id="device_deactivateWhileEvCharging<?php echo $devicenum; ?>2" data-option="2" value="2">ausschalten/nicht einschalten
													</label>
												</div>
												<span class="form-text small">Diese Option (bei Auschaltschwelle anpassen oder auschalten/nicht einschalten) sorgt dafür, dass die aktuelle Leistungsaufnahme von diesem Gerät in den die Pv Überschussberechnung miteinbezogen wird. Wenn dann ein Auto geladen wird (> 1000 Watt Leistungsaufnahme),<br>
												wird bei Ausschaltschwelle anpassen: Die Ausschaltverzögerung auf 0 gesetzt und die Ausschaltschwelle (sofern eine Bezugsschwelle definiert ist) auf 0 gesetzt. Dadurch werden diese Geräte als erstes abgeschaltet, wenn das Auto lädt und der Überschuss nicht ausreicht.
												<br>
												wird bei ausschalten/nicht einschalten: Das Gerät abgeschaltet.		Dann steht die aktuelle Leistungsaufnahme sofort für die Autoladung zur Verfügung.
												</span>
											</div>
										</div>
									</div>
									<hr class="border-secondary">
									<div class="form-group">
										<div class="form-row mb-1">
											<label class="col-md-4 col-form-label">Um 23:59...</label>
											<div class="col">
												<div class="btn-group btn-group-toggle btn-block" id="device_setautoDevices<?php echo $devicenum; ?>" name="device_setauto" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<label class="btn btn-outline-info">
														<input type="radio" name="device_setautoDevices<?php echo $devicenum; ?>" id="device_setauto<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">nichts tun
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_setautoDevices<?php echo $devicenum; ?>" id="device_setauto<?php echo $devicenum; ?>1" data-option="1" value="1">in den automatischen Modus stellen
													</label>
												</div>
												<span class="form-text small">Diese Option bewirkt, dass ein Gerät um 23:59 immer in den automaischen Modus geschaltet wird.
												</span>
											</div>
										</div>
									</div>
									<hr class="border-secondary">
									<div class="form-group">
										<div class="form-row mb-1">
											<label class="col-md-4 col-form-label">Einschalt/Ausschaltgruppe...</label>
											<div class="col">
												<div class="btn-group btn-group-toggle btn-block" id="device_deactivateperDevices<?php echo $devicenum; ?>" name="device_deactivateper" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateperDevices<?php echo $devicenum; ?>" id="device_deactivateper<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">nie
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateperDevices<?php echo $devicenum; ?>" id="device_deactivateper<?php echo $devicenum; ?>1" data-option="1" value="1">jede volle Stunde prüfen oder ausschalten
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateperDevices<?php echo $devicenum; ?>" id="device_deactivateper<?php echo $devicenum; ?>2" data-option="2" value="2">jede volle Stunde / jede halbe Stunde prüfen oder ausschalten
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_deactivateperDevices<?php echo $devicenum; ?>" id="device_deactivateper<?php echo $devicenum; ?>100" data-option="100" value="100">gehört zu Einschaltgruppe
													</label>
												</div>
												<span class="form-text small">Diese Option (bei jeder vollen Stunde / jede halbe Stunde) sorgt dafür, dass dieses Gerät periodisch ausgestellt wird ohne Ausschaltschwelle / Ausschaltverzögerung zu berücksichtigen (=Auschaltgruppe). Dann können andere Geräte mit dem freiwerden Überschuss eingeschaltet werden. Sofern andere Geräte zuätzlich in der Einschaltgrupppe definiert werden, werden die Geräte in der Auschaltgruppe nur dann abgestellt wenn genug Überschuss dann da ist um die ganze Einschaltgrupppe anzustellen.
												</span>
												<span class="text-danger">Diese Funktion ist in der Entwicklung.</span>
											</div>
										</div>
									</div>
									<hr class="border-secondary">
									<div class="form-group">
										<div class="form-row mb-1">
											<label for="device_einschaltschwelleDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Einschaltschwelle</label>
											<div class="col">
												<div class="form-row vaRow">
													<div class="col-auto">
														<div class="custom-control custom-checkbox">
															<input class="custom-control-input" type="checkbox" id="device_einschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
															<label class="custom-control-label" for="device_einschaltschwelleDevices<?php echo $devicenum; ?>PosNeg">
																negativ
															</label>
														</div>
													</div>
													<div class="col">
														<input id="device_einschaltschwelleDevices<?php echo $devicenum; ?>" name="device_einschaltschwelle" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="50000" data-default="1500" value="0" data-signcheckbox="device_einschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													</div>
												</div>
												<span class="form-text small">Parameter in Watt [W] für das Einschalten des Gerätes. Steigt die <b>Einspeisung</b> über den Wert Einschaltschwelle, startet das Gerät.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_einschaltverzoegerungDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Einschaltverzögerung</label>
											<div class="col">
												<input id="device_einschaltverzoegerungDevices<?php echo $devicenum; ?>" name="device_einschaltverzoegerung" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Parameter in Minuten, der bestimmt, wie lange die Einschaltschwelle <b>am Stück</b> überschritten werden muss, bevor das Gerät eingeschaltet wird.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_updatesecDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Updategerät</label>
											<div class="col">
												<input id="device_updatesecDevices<?php echo $devicenum; ?>" name="device_updatesec" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="180" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Parameter in Sekunden (von 0 bis 180), in was für einen Abstand openWB das Gerät updatet. 0 Sekunden bedeutet Defaultverhalten. Das Defaultverhalten ist pro Typ definiert und eher konservativ (langsam).</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_ausschaltschwelleDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschaltschwelle</label>
											<div class="col">
												<div class="form-row vaRow">
													<div class="col-auto">
														<div class="custom-control custom-checkbox">
															<input class="custom-control-input" type="checkbox" id="device_ausschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
															<label class="custom-control-label" for="device_ausschaltschwelleDevices<?php echo $devicenum; ?>PosNeg">
																negativ
															</label>
														</div>
													</div>
													<div class="col">
														<input id="device_ausschaltschwelleDevices<?php echo $devicenum; ?>" name="device_ausschaltschwelle" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="50000" data-default="1500" value="1500" data-signcheckbox="device_ausschaltschwelleDevices<?php echo $devicenum; ?>PosNeg" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													</div>
												</div>
												<span class="form-text small">Parameter in Watt [W] für das Ausschalten des Gerätes. Steigt der <b>Bezug</b> über den Wert Ausschaltschwelle, stoppt das Gerät.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="device_ausschaltverzoegerungDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschaltverzögerung</label>
											<div class="col">
												<input id="device_ausschaltverzoegerungDevices<?php echo $devicenum; ?>" name="device_ausschaltverzoegerung" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1000" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
												<span class="form-text small">Parameter in Minuten, der bestimmt, wie lange die Ausschaltschwelle <b>am Stück</b> überschritten werden muss, bevor das Gerät ausgeschaltet wird.</span>
											</div>
										</div>
									</div>
									<div class="device-option-housebattery hide">
										<hr class="border-secondary">
										<div class="form-group">
											<div class="form-row mb-1">
												<label for="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Speicherbeachtung beim Einschalten</label>
												<div class="col-md-8">
													<div class="form-row vaRow mb-1">
														<label for="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" class="col-2 col-form-label valueLabel" suffix="%">0 %</label>
														<div class="col-10">
															<input type="range" class="form-control-range rangeInput" id="device_speichersocbeforestartDevices<?php echo $devicenum; ?>" name="device_speichersocbeforestart" min="0" max="100" step="5" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
														</div>
													</div>
													<span class="form-text small">Parameter in % Ladezustand. 0% deaktiviert die Funktion. Bei deaktivierter Funktion oder wenn der Ladezustand grösser gleich dem Parameter ist, wird die Speicherleistung bei der Berechnung der Ein- und Ausschaltschwelle berücksichtigt<br> Uberschuss = evu + speicherleistung, wobei evu - > Bezug(-)/Einspeisung(+) und speicherleistung Entladung(-)/Ladung(+) ist .<br>
													Unterhalb dieses Wertes ist für die Berechnung der obige Überschuss und die maximal mögliche Speicherladung (als Offset) relevant <br>Uberschussoffset = Uberschuss - maxspeicher<br>
													Bei überschussgesteuerten Geräten wird dann der Ueberschuss oder der Ueberschuss mit Offset übertragen.
																								</span>
												</div>
											</div>
										</div>
										<div class="form-group">
											<div class="form-row mb-1">
												<label for="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Speicherbeachtung beim Ausschalten</label>
												<div class="col-md-8">
													<div class="form-row vaRow mb-1">
														<label for="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" class="col-2 col-form-label valueLabel" suffix="%">100 %</label>
														<div class="col-10">
															<input type="range" class="form-control-range rangeInput" id="device_speichersocbeforestopDevices<?php echo $devicenum; ?>" name="device_speichersocbeforestop" min="0" max="100" step="5" data-default="100" value="100" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
														</div>
													</div>
													<span class="form-text small">Parameter in % Ladezustand. Überhalb dieses Wertes wird das Gerät nicht abgeschaltet. 100% deaktiviert die Funktion.</span>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="form-group device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly hide">
								<hr class="border-secondary">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Temperatursensoren</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>" name="device_temperatur_configured" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<label class="btn btn-outline-info">
												<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">0
											</label>
											<label class="btn btn-outline-info">
												<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>1" data-option="1" value="1">1
											</label>
											<label class="btn btn-outline-info">
												<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>2" data-option="2" value="2">2
											</label>
											<label class="btn btn-outline-info">
												<input type="radio" name="device_temperatur_configuredDevices<?php echo $devicenum; ?>" id="device_temperatur_configuredDevices<?php echo $devicenum; ?>3" data-option="3" value="3">3
											</label>
										</div>
										<span class="form-text small">Anzahl der Temperatursensoren die an einem Shelly Unterputzgerät anschließbar sind. Für shelly plus müssen die IDs ab 100 beginnen.</span>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">In Hausverbrauch einrechnen</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" id="device_homeConsumtionDevices<?php echo $devicenum; ?>" name="device_homeConsumtion" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<label class="btn btn-outline-info">
												<input type="radio" name="device_homeConsumtionDevices<?php echo $devicenum; ?>" id="device_homeConsumtion<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
											</label>
											<label class="btn btn-outline-info">
												<input type="radio" name="device_homeConsumtionDevices<?php echo $devicenum; ?>" id="device_homeConsumtion<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
											</label>
										</div>
										<span class="form-text small">Bei Nein wird dass das Gerät vom Hausverbrauch abgezogen, bei Ja ist es im Hausverbrauch eingerechnet. (Startseite, neues logging).</span>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Steuerung über Smart Button</label>
									<div class="col">
										<select class="form-control" name="device_pbtype" id="device_pbtypeDevices<?php echo $devicenum; ?>" data-default="none" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<option value="none" data-option="none" selected="selected">Kein Button</option>
											<option value="shellypb" data-option="shellypb">Shelly Button 1</option>
										</select>
										<span class="form-text small">
											Wenn Shelly Button gewählt wird, zeigt Shelly button den Modus (automatisch / manuell) und den an / aus Status vom Gerät an.
											Shelly Button nur mit Netzteil betreiben.<br>
											Wenn Gerät im automatische Modus ist der Leuchtring aus.<br>
											Wenn Gerät im manuellem Modus ist:<br>
												- Ist das Gerät aus ist der Leuchtring an.<br>
												- Ist das Gerät an blinked der Leuchtring langsam.<br>
											<br>Einmal drücken schaltet das Gerät von dem automatischen Modus in den manuellen Modus.<br>
											Einmal drücken im manuellen Modus schaltet das Gerät zwischen an und aus hin und her.<br>
											Zweimal drücken im manuellen Modus schaltet das Gerät in den automatischen Modus.<br>
										</span>
									</div>
								</div>
								<div class="device_pbtypeDevices<?php echo $devicenum; ?>-option device_pbtypeDevices<?php echo $devicenum; ?>-option-shellypb hide">
									<label for="device_pbipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse vom Button</label>
									<div class="col">
										<input id="device_pbipDevices<?php echo $devicenum; ?>" name="device_pbip" class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Separate Leistungsmessung für das Gerät</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" id="device_differentMeasurementDevices<?php echo $devicenum; ?>" name="device_differentMeasurement" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<label class="btn btn-outline-info">
												<input type="radio" name="device_differentMeasurementDevices<?php echo $devicenum; ?>" id="device_differentMeasurement<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
											</label>
											<label class="btn btn-outline-info">
												<input type="radio" name="device_differentMeasurementDevices<?php echo $devicenum; ?>" id="device_differentMeasurement<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
											</label>
										</div>
										<span class="form-text small">Wenn diese Option aktiviert wird, wird für die Leistungserfassung ein separates Gerät abgefragt. Das kann genutzt werden, wenn z. B. ein Gerät über keine Leistungsmessung verfügt, jedoch ein Zwischenstecker mit Messung eingesetzt wird.</span>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>differentMeasurement hide">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Gerätetyp</label>
									<div class="col">
										<select class="form-control" name="device_measureType" id="device_measureTypeDevices<?php echo $devicenum; ?>" data-default="sdm630" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<option value ="" data-option="" disabled="disabled" selected="selected">-- Bitte auswählen --</option>
											<option value="fronius" data-option="fronius">Fronius</option>
											<option value="http" data-option="http">Http</option>
											<option value="json" data-option="json">Json</option>
											<option value="mystrom" data-option="mystrom">MyStrom</option>
											<option value="sdm630" data-option="sdm630">SDM630</option>
											<option value="b23" data-option="b23">b23</option>											
											<option value="shelly" data-option="shelly">Shelly oder Shelly plus</option>
											<option value="tasmota" data-option="tasmota">tasmota</option>
											<option value="we514" data-option="we514">WE514</option>
											<option value="avm" data-option="avm">AVM</option>
											<option value="mqtt" data-option="mqtt">Mqtt</option>
											<option value="smaem" data-option="smaem">SMA Energy Meter</option>
											<option value="sdm120" data-option="sdm630">SDM120</option>
											<option value="lovato" data-option="lovato">Lovato</option>											
										</select>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-shelly deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-tasmota deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-b23 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-lovato deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm120 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-we514 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-mystrom deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-fronius deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-avm hide">
									<label for="device_measureipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input id="device_measureipDevices<?php echo $devicenum; ?>" name="device_measureip" class="form-control" type="text" required="required" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
								<div class="form-group mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-shelly hide">
									<!-- Shelly measure -->
									<hr class="border-secondary">
									<div class="form-group">
									<div class="form-row mb-1">
											<label class="col-md-4 col-form-label">Shelly mit Authentication</label>
											<div class="col">
												<div class="btn-group btn-group-toggle btn-block" id="device_measureshauthDevices<?php echo $devicenum; ?>" name="device_measureshauth" data-toggle="buttons" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<label class="btn btn-outline-info">
														<input type="radio" name="device_measureshauthDevices<?php echo $devicenum; ?>" id="device_measureshauth<?php echo $devicenum; ?>0" data-option="0" value="0" checked="checked">Nein
													</label>
													<label class="btn btn-outline-info">
														<input type="radio" name="device_measureshauthDevices<?php echo $devicenum; ?>" id="device_measureshauth<?php echo $devicenum; ?>1" data-option="1" value="1">Ja
													</label>
												</div>
											</div>
											<span class="form-text small">Wenn diese Option aktiviert wird, wird für den Shelly eine Userid und ein Password verlangt.Läuft momentan nur für shell ohne plus.</span>
										</div>	
										<div class="device<?php echo $devicenum; ?>measureshauth hide">
											<div class="form-row mb-1">
												<label for="device_measureshusernameDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Benutzername</label>
													<div class="col">
														<input id="device_measureshusernameDevices<?php echo $devicenum; ?>" name="device_measureshusername" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													</div>
											</div>
											<div class="form-row mb-1">
												<label for="device_measureshpasswordDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Passwort</label>
													<div class="col">
														<input id="device_measureshpasswordDevices<?php echo $devicenum; ?>" name="device_measureshpassword" class="form-control" type="password" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													</div>
											</div>
										</div>									
									</div>		
										<!-- Shellyend -->
									<hr class="border-secondary">
									<div class="form-row mb-1">
										<label for="device_measchanDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Meter Auswahl</label>
										<select class="form-control" name="device_measchan" id="device_measchanDevices<?php echo $devicenum; ?>" data-default="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<option value="0" data-option="0" selected="selected">alle Meter summiert</option>
											<option value="1" data-option="1">Meter 1</option>
											<option value="2" data-option="2">Meter 2</option>
											<option value="3" data-option="3">Meter 3</option>
											<option value="4" data-option="4">Meter 4</option>
											<option value="5" data-option="5">Meter 5</option>
											<option value="6" data-option="6">Meter 6</option>
										</select>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-b23 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-lovato deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm120 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-we514 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-fronius hide">
									<label for="device_measureidDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">ID des Zählers</label>
									<div class="col">
										<input id="device_measureidDevices<?php echo $devicenum; ?>" name="device_measureid" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="255" data-default="1" value="1"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm120 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-lovato deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-b23 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 hide">
									<label for="device_measurePortSdmDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Modbusport des Zählers</label>
									<div class="col">
										<input id="device_measurePortSdmDevices<?php echo $devicenum; ?>" name="device_measurePortSdm" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="9999" data-default="8899" value="8899"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Standardeinstellungen verschiedener Geräte:<br>
											SDM630/Lovato: 8899<br>
											Elgris: 502
											b23: ???
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-http hide">
									<label for="device_measureurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Leistungs-URL</label>
									<div class="col">
										<input id="device_measureurlDevices<?php echo $devicenum; ?>" name="device_measureurl" class="form-control" type="text" required="required" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-http hide">
									<label for="device_measureurlcDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Zähler-URL</label>
									<div class="col">
										<input id="device_measureurlcDevices<?php echo $devicenum; ?>" name="device_measureurlc" class="form-control" type="text" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Hier bitte eine URL angeben, die einen absoluten Zählerstand übermittelt. Diese Einstellung ist optional. Wird das Feld leer gelassen, dann wird intern ein Zähler simuliert.<br>
											<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-json hide">
									<label for="device_measurejsonurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">JSON-URL</label>
									<div class="col">
										<input id="device_measurejsonurlDevices<?php echo $devicenum; ?>" name="device_measurejsonurl" class="form-control" type="url" required="required" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Hier bitte eine URL angeben, deren Antwort die aktuelle Leistung sowie den Zählerstand übermittelt.<br>
											<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-json hide">
									<label for="device_measurejsonpowerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Abfrage Leistung</label>
									<div class="col">
										<input id="device_measurejsonpowerDevices<?php echo $devicenum; ?>" name="device_measurejsonpower" class="form-control" type="text" required="required" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Hier bitte den Ausdruck angeben, mit dem die aktuelle Leistung aus der Antwort ermittelt werden kann.<br>
											<span class="text-info">Wenn der Parameter ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-json hide">
									<label for="device_measurejsoncounterDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Abfrage Zählerstand</label>
									<div class="col">
										<input id="device_measurejsoncounterDevices<?php echo $devicenum; ?>" name="device_measurejsoncounter" class="form-control" type="text" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Hier bitte den Ausdruck angeben, mit dem der aktuelle Zählerstand aus der Antwort ermittelt werden kann. Diese Einstellung ist optional. Wird das Feld leer gelassen, dann wird intern ein Zähler simuliert.
											<span class="text-info">Wenn der Parameter ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-avm hide">
									<label for="device_measureavmusernameDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<input id="device_measureavmusernameDevices<?php echo $devicenum; ?>" name="device_measureavmusername" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-avm hide">
									<label for="device_measureavmpasswordDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Passwort</label>
									<div class="col">
										<input id="device_measureavmpasswordDevices<?php echo $devicenum; ?>" name="device_measureavmpassword" class="form-control" type="password" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-avm hide">
									<label for="device_measureavmactorDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Aktor</label>
									<div class="col">
										<input id="device_measureavmactorDevices<?php echo $devicenum; ?>" name="device_measureavmactor" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Hier ist der Name des Gerätes einzutragen, wie er in der Fritz!Box angezeigt wird.</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-smaem hide">
									<label for="device_measuresmaserDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">SMA Seriennummer</label>
									<div class="col">
										<input id="device_measuresmaserDevices<?php echo $devicenum; ?>" name="device_measuresmaser" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Seriennummer des Sma Energy Meter.</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-smaem hide">
									<label for="device_measuresmaageDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Alter Datendatei </label>
									<div class="col">
										<input id="device_measuresmaageDevices<?php echo $devicenum; ?>" name="device_measuresmaage" class="form-control naturalNumber" type="number" inputmode="decimal" required min="0" max="1000" data-default="15" value="15" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">Parameter in Sekunden, der bestimmt, wie alt die Datendatei sein darf .</span>
									</div>
								</div>
							</div>
						</div>  <!-- end card body Allgemeine Einstellungen Gerät <?php echo $devicenum; ?> -->
					</div>  <!-- end card Allgemeine Einstellungen Gerät <?php echo $devicenum; ?> -->
				<?php } ?>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Übergreifende Einstellungen
					</div>
					<div class="card-body">
						<div  class="device-option-housebattery hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="maxBatteryPower" class="col-md-4 col-form-label">maximale Speicherladung in W</label>
									<div class="col">
										<input id="maxBatteryPower" name="maxBatteryPower" class="form-control naturalNumber" type="number" required="required" min="0" max="30000" value="0" data-default="0" data-topicprefix="openWB/config/get/SmartHome/">
									</div>
								</div>
							</div>
							<hr>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="logLevel" class="col-md-4 col-form-label">SmartHome Loglevel</label>
								<div class="col">
									<select name="logLevel" id="logLevel" class="form-control" data-default="2" data-topicprefix="openWB/config/get/SmartHome/">
										<option value="0" data-option="0">0</option>
										<option value="1" data-option="1">1</option>
										<option value="2" data-option="2">2</option>
									</select>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="row justify-content-center">
					<div class="col-3">
						<button id="saveSettingsBtn" type="button" class="btn btn-success">speichern</button>
					</div>
					<div class="col-1">
						&nbsp;
					</div>
					<div class="col-3">
						<button id="modalDefaultsBtn" type="button" class="btn btn-danger">Werkseinstellungen</button>
					</div>
				</div>
			</form>

			<!-- modal set-defaults-confirmation window -->
			<div class="modal fade" id="setDefaultsConfirmationModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-danger">
							<h4 class="modal-title text-light">Achtung</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Sollen für die Geräte wirklich die Werkseinstellungen eingestellt werden?
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-success" data-dismiss="modal" id="saveDefaultsBtn">Fortfahren</button>
							<button type="button" class="btn btn-danger" data-dismiss="modal">Abbruch</button>
						</div>
					</div>
				</div>
			</div>

			<!-- modal form-not-valid window -->
			<div class="modal fade" id="formNotValidModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-danger">
							<h4 class="modal-title text-light">Fehler</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Es wurden fehlerhafte Eingaben gefunden, speichern ist nicht möglich! Bitte überprüfen Sie alle Eingaben.
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-primary" data-dismiss="modal">Schließen</button>
						</div>
					</div>
				</div>
			</div>

			<!-- modal no-values-changed window -->
			<div class="modal fade" id="noValuesChangedInfoModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-info">
							<h4 class="modal-title text-light">Info</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Es wurden keine geänderten Einstellungen gefunden.
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-success" data-dismiss="modal">Ok</button>
						</div>
					</div>
				</div>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Ladeeinstellungen/Smart Home 2.0</small>
			</div>
		</footer>

		<!-- load mqtt library -->
		<script src = "js/mqttws31.js" ></script>
		<!-- load topics -->
		<script src = "settings/topicsToSubscribe_smarthomeconfig.js?ver=20210215" ></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210215" ></script>
		<!-- load service -->
		<script src = "settings/setupMqttServices.js?ver=20201207" ></script>
		<!-- load mqtt handler-->
		<script src = "settings/processAllMqttMsg.js?ver=20210104" ></script>

		<script>
			<?php for( $devicenum = 1; $devicenum <= $numDevices; $devicenum++ ) { ?>
				function visibility_device_configuredDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('input[name=device_configuredDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					if( data == 0 ){
						hideSection('#device<?php echo $devicenum; ?>options');
					} else {
						showSection('#device<?php echo $devicenum; ?>options');
					}
				}

				function visibility_device_typeDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('#device_typeDevices<?php echo $devicenum; ?>').val();
					}
					hideSection(".device<?php echo $devicenum; ?>-option");
					showSection(".device<?php echo $devicenum; ?>-option-"+data);
				}

				function visibility_device_pbtypeDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('#device_pbtypeDevices<?php echo $devicenum; ?>').val();
					}
					hideSection(".device_pbtypeDevices<?php echo $devicenum; ?>-option");
					showSection(".device_pbtypeDevices<?php echo $devicenum; ?>-option-"+data);
				}

				function visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('input[name=device_differentMeasurementDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>differentMeasurement');
						showSection('.device<?php echo $devicenum; ?>noDifferentMeasurement');
					} else {
						showSection('.device<?php echo $devicenum; ?>differentMeasurement');
						hideSection('.device<?php echo $devicenum; ?>noDifferentMeasurement');
					}
				}

				function visibility_device_measureTypeDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('#device_measureTypeDevices<?php echo $devicenum; ?>').val();
					}
					hideSection(".deviceMeasureTypeDevices<?php echo $devicenum; ?>-option");
					showSection(".deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-"+data);
				}

				function visibility_device_measureshauthDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('input[name=device_measureshauthDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>measureshauth');
					} else {
						showSection('.device<?php echo $devicenum; ?>measureshauth');
					}
				}

				function visibility_device_shauthDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('input[name=device_shauthDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>shauth');
					} else {
						showSection('.device<?php echo $devicenum; ?>shauth');
					}
				}


				function visibility_device_canSwitchDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('input[name=device_canSwitchDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>canSwitch');
					} else {
						showSection('.device<?php echo $devicenum; ?>canSwitch');
					}
				}

				function visibility_device_startupDetectionDevices<?php echo $devicenum; ?>( data ){
					if( typeof data == 'undefined' ){
						data = $('input[name=device_startupDetectionDevices<?php echo $devicenum; ?>]:checked').attr("data-option");
					}
					if( data == 0 ){
						hideSection('.device<?php echo $devicenum; ?>startupDetection');
					} else {
						showSection('.device<?php echo $devicenum; ?>startupDetection');
					}
				}

				function visibility_device_nameDevices<?php echo $devicenum; ?>( data ){
					if( typeof data =='undefined' ){
						data = $('#device_nameDevices<?php echo $devicenum; ?>').val();
					}
					if ( data != "Name" ) {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?> ('+data+')');
					} else {
						$('#deviceHeader<?php echo $devicenum; ?>').text('Gerät <?php echo $devicenum; ?>');
					}
				}
			<?php } ?>

			function visibility_housebatteryConfigured( data ) {
				if ( data == 1 ) {
					showSection('.device-option-housebattery');
				} else {
					hideSection('.device-option-housebattery');
				}
			}

			function visibiltycheck(elementId, mqttpayload) {
				<?php for( $devicenum = 1; $devicenum <= $numDevices; $devicenum++ ) { ?>
					if ( elementId == 'device_configuredDevices<?php echo $devicenum; ?>') {
						visibility_device_configuredDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_typeDevices<?php echo $devicenum; ?>') {
						visibility_device_typeDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_pbtypeDevices<?php echo $devicenum; ?>') {
						visibility_device_pbtypeDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_differentMeasurementDevices<?php echo $devicenum; ?>') {
						visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_measureshauthDevices<?php echo $devicenum; ?>') {
						visibility_device_measureshauthDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_shauthDevices<?php echo $devicenum; ?>') {
						visibility_device_shauthDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_measureTypeDevices<?php echo $devicenum; ?>') {
						visibility_device_measureTypeDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_canSwitchDevices<?php echo $devicenum; ?>') {
						visibility_device_canSwitchDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_startupDetectionDevices<?php echo $devicenum; ?>') {
						visibility_device_startupDetectionDevices<?php echo $devicenum; ?>( mqttpayload );
					}

					if ( elementId == 'device_nameDevices<?php echo $devicenum; ?>') {
						visibility_device_nameDevices<?php echo $devicenum; ?>( mqttpayload );
					}
				<?php } ?>

				if ( elementId == 'boolHouseBatteryConfigured' ) {
						visibility_housebatteryConfigured( mqttpayload );
					}
			}

			$(function() {
				<?php for( $devicenum = 1; $devicenum <= $numDevices; $devicenum++ ) { ?>
					$('#device_configuredDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_configuredDevices<?php echo $devicenum; ?>();
					});

					$('#device_typeDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_typeDevices<?php echo $devicenum; ?>();
					});

					$('#device_pbtypeDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_pbtypeDevices<?php echo $devicenum; ?>();
					});

					$('#device_differentMeasurementDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>();
					});

					$('#device_measureshauthDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_measureshauthDevices<?php echo $devicenum; ?>();
					});

					$('#device_shauthDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_shauthDevices<?php echo $devicenum; ?>();
					});

					$('#device_measureTypeDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_measureTypeDevices<?php echo $devicenum; ?>();
					});

					$('#device_canSwitchDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_canSwitchDevices<?php echo $devicenum; ?>();
					});

					$('#device_startupDetectionDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_startupDetectionDevices<?php echo $devicenum; ?>();
					});

					$('#device_nameDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_nameDevices<?php echo $devicenum; ?>( $(this).val() );
					})
				<?php } ?>
			});

			$.get(
				{ url: 'settings/navbar.html', cache: false },
				function(data){
					$('#nav').replaceWith(data);
					// disable navbar entry for current page
					$('#navSmartHome2').addClass('disabled');
				}
			);

			function saveSettings() {
				// sends all changed values by mqtt if valid
				var formValid = $("#myForm")[0].checkValidity();
				if ( !formValid ) {
					$('#formNotValidModal').modal();
					return;
				};
				getChangedValues();
				sendValues();
			}

			function initForm() {
				<?php for( $devicenum = 1; $devicenum <= $numDevices; $devicenum++ ) { ?>
					visibility_device_configuredDevices<?php echo $devicenum; ?>();
					visibility_device_typeDevices<?php echo $devicenum; ?>();
					visibility_device_pbtypeDevices<?php echo $devicenum; ?>();
					visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>();
					visibility_device_measureshauthDevices<?php echo $devicenum; ?>();										
					visibility_device_shauthDevices<?php echo $devicenum; ?>();															
					visibility_device_measureTypeDevices<?php echo $devicenum; ?>();
					visibility_device_canSwitchDevices<?php echo $devicenum; ?>();
					visibility_device_nameDevices<?php echo $devicenum; ?>();
				<?php } ?>
			}

			$(document).ready(function(){

				$('input').blur(function(event) {
					// check input field on blur if value is valid
					if ( event.target.checkValidity() == false ) {
						$(this).addClass('is-invalid');
					} else {
						$(this).removeClass('is-invalid');
					}
				});

				$('#saveSettingsBtn').on("click",function() {
					saveSettings();
				});

				$('#modalDefaultsBtn').on("click",function() {
					$('#setDefaultsConfirmationModal').modal();
				});

				$('#saveDefaultsBtn').on("click",function() {
					// shown in confirmation modal
					// resets all values to defaults and sends all changed values by mqtt
					setToDefaults();
					getChangedValues();
					sendValues();
				});

				$('.rangeInput').on('input', function() {
					// show slider value in label of class valueLabel
					updateLabel($(this).attr('id'));
				});

				$('input.naturalNumber').on('input', function() {
					// on the fly input validation
					formatToNaturalNumber(this);
				});

				initForm();
			});  // end document ready function

		</script>

	</body>
</html>
