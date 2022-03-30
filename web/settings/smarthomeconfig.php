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
											<option value="acthor" data-option="acthor">Acthor</option>
											<option value="elwa" data-option="elwa">Elwa</option>
											<option value="idm" data-option="idm">Idm</option>
											<option value="stiebel" data-option="stiebel">Stiebel</option>
											<option value="http" data-option="http">Http</option>
											<option value="avm" data-option="avm">AVM</option>
											<option value="mystrom" data-option="mystrom">MyStrom</option>
											<option value="viessmann" data-option="viessmann">Viessmann</option>
											<option value="mqtt" data-option="mqtt">Mqtt</option>
											<option value="pyt" data-option="pyt">Pyt (veraltet, bitte andere Option wählen)</option>
										</select>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-none hide">
											Dieser Gerätetyp wird nicht in die Regelung eingebunden und es können keine Schalthandlungen ausgeführt oder Sensoren eingelesen werden. Es ist jedoch eine separate Leistungsmessung möglich, um reine Verbraucher zu erfassen.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-acthor hide">
											Heizstab Acthor der Firma my-PV<br>
											Im Web Frontend vom Heizstab muss unter "Steuerungs-Einstellungen" der Parameter "Ansteuerungs-Typ = Modbus TCP" und "Zeitablauf Ansteuerung = 120 Sek" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen (in 1000 Watt Schritten)
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Acthor nicht zu stören.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-mqtt hide">
											Generisches MQTT modul<br>
											Wenn Einschaltbedingung erreicht (Beispiel hier mit Device 4)<br>
											openWB/SmartHome/set/Devices/4/ReqRelay = 1<br>
											openWB/SmartHome/set/Devices/4/Ueberschuss = in Watt<br>
											Wenn Ausschaltbedingung erreicht<br>
											openWB/SmartHome/set/Devices/4/ReqRelay = 0<br>
											openWB/SmartHome/set/Devices/4/Ueberschuss = in Watt<br>
											Bei der periodischen Abfrage wird die aktuelle Leistung<br>
											openWB/SmartHome/set/Devices/4/Aktpower = in Watt erwartet<br>
											und der aktuelle Zähler in Wattstunden wird hier erwartet<br>
											openWB/SmartHome/set/Devices/4/Powerc<br>
											wenn kein Zähler übergeben oder 0 übergeben wird, wird der Zähler selber gerechnet<br>
											openWB/SmartHome/set/Devices/4/Ueberschuss = in Watt<br>
										</span>

										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-viessmann hide">
											Vitalcal 200-s Wärmepumpe mit LON Kommunikationsmodul und Vitogate 300. Wenn die Einschaltbedingung erreicht ist wird Komfortfunktion "Einmalige Warmwasserbereitung" außerhalb des Zeitprogramms gestartet. Für die "Einmalige Warmwasserbereitung" wird der Warmwassertemperatur-Sollwert 2 genutzt. In der Wp kann eingestellt werden, ob für diese Funktion  die Elektroheizung (Heizstab) benutzt werden soll.
										</span>



										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-elwa hide">
											Heizstab ELWA-E  der Firma my-PV<br>
											Im Web Frontend vom Heizstab muss unter Steuerungs-Einstellungen der Parameter "Ansteuerungs-Typ = Modbus TCP" und "Power Timeout = 120 Sek" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen.
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von Elwa nicht zu stören.
											Die Warmwassersicherstellung in Elwa kann genutzt werden. OpenWB erkennt dieses am Status und überträgt dann keinen Überschuss.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-idm hide">
											Wärmepumpe der Firma IDM mit Navigatorregelung 2.0<br>
											Im Web Frontend muss unter "Heizungsbauerebene / Konfiguration / PV-Signal": Auswahl "Gebäudeleittechnik / Smartfox" und unter "Heizungsbauerebene / Gebäudeleittechnik" der Parameter "Modbus TCP = Ein" und unter "Einstellungen / Photovoltaik" der Parameter "PV Überschuss = 0" gesetzt werden
											Wenn die Einschaltbedingung erreicht ist wird alle 30 Sekunden der gerechnete Überschuss übertragen
											Wenn die Ausschaltbedingung erreicht ist wird einmalig 0 als Überschuss übertragen.
											Die Ausschaltschwelle/ Ausschaltverzögerung in OpenWB ist sinnvoll zu wählen (z.B. 500 / 3) um die Regelung von IDM nicht zu stören.
										</span>
										<span class="form-text small device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-stiebel hide">
											Wärmepumpe der Firma Stiebel mit ISG Plus (Servicewelt über Modbus) und SG Ready Eingang.<br>
											Im ISG web muss unter "Einstellungen / Energiemanagement" der Parameter "SGREADY = Ein" gesetzt werden.
											Wenn die Einschaltbedingung erreicht ist wird der Sg Ready Eingang von Betriebszustand 2 auf Betriebszustand 3 geschaltet.
											Wenn die Ausbedingung erreicht ist wird der Sg Ready Eingang von Betriebszustand 3 auf Betriebszustand 2 geschaltet.
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
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-acthor device<?php echo $devicenum; ?>-option-elwa device<?php echo $devicenum; ?>-option-idm device<?php echo $devicenum; ?>-option-stiebel device<?php echo $devicenum; ?>-option-avm device<?php echo $devicenum; ?>-option-mystrom device<?php echo $devicenum; ?>-option-viessmann device<?php echo $devicenum; ?>-option-pyt hide">
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
												Die hier angegebene URL wird aufgerufen, um die aktuelle Leistung des Geräts zu erhalten.<br />
												<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span><br />
												Falls keine URL vorhanden ist, kann eine der folgenden angegeben werden:<br />
												127.0.0.1/openWB/modules/smarthome/http/dummyurl.php. Diese URL gibt immer den Wert 0 zurück.(Device immer aus)<br />
												127.0.0.1/openWB/modules/smarthome/http/dummyurl1.php?d=nummerdevice. Diese URL gibt den Wert 0 oder 100 zurück. Je nachdem ob das Smarthomedevice gerade läuft<br />
												127.0.0.1/openWB/modules/smarthome/http/dummyurl2.php. Diese URL gibt immer den Wert 100 zurück. (Device immer an)<br />
												In der URL kann ein Parameter angegeben werden, der den aktuellen Überschuss an das Gerät übermittelt. Hierzu ist folgender Platzhalter in der URL zu verwenden (inklusive der spitzen Klammern):<br />
												<span class="text-info">&lt;openwb-ueberschuss&gt;</span>
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
												<option value="9s" data-option="9s">Acthor 9s</option>
											</select>
											<span class="form-text small">
												Hier ist das installierte Modell auszuwählen.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="device_acthorpowerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Installierte Leistung</label>
										<div class="col">
											<input id="device_acthorpowerDevices<?php echo $devicenum; ?>" name="device_acthorpower" class="form-control" type="number" min="0" max="9000" step="100" required="required" data-default="0" value="0" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
											<span class="form-text small">
												Hier bitte die an den Acthor angeschlossene Leistung in Watt angeben.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-acthor device<?php echo $devicenum; ?>-option-elwa device<?php echo $devicenum; ?>-option-idm device<?php echo $devicenum; ?>-option-stiebel device<?php echo $devicenum; ?>-option-avm device<?php echo $devicenum; ?>-option-mystrom device<?php echo $devicenum; ?>-option-http device<?php echo $devicenum; ?>-option-mqtt device<?php echo $devicenum; ?>-option-viessmann device<?php echo $devicenum; ?>-option-pyt hide">
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
														Die hier angegebene URL wird aufgerufen, um das Gerät einzuschalten.<br />
														<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="device_ausschalturlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Ausschalt-URL</label>
												<div class="col">
													<input id="device_ausschalturlDevices<?php echo $devicenum; ?>" name="device_ausschalturl" class="form-control" type="text" required="required" data-default="" value="" data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
													<span class="form-text small">
														Die hier angegebene URL wird aufgerufen, um das Gerät auszuschalten.<br />
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
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Einschaltbedingungen gelten erst ab der definierten Uhrzeit. Ausschaltbedingungen gelten den ganzen Tag.</span>
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
												<span class="form-text small">Uhrzeit im 24 Stunden-Format, z.B. "14:45". Der Wert "00:00" schaltet die Funktion ab. Wenn das Gerät heute noch nicht eingeschaltet wurde, wird es unabhängig vom Überschuss eingeschaltet unter Berücksichtigung der Mindestlaufzeit, so dass es zur angegebenen Uhrzeit fertig ist.</span>
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

									</div>
									<div class="device<?php echo $devicenum; ?>-option device<?php echo $devicenum; ?>-option-shelly device<?php echo $devicenum; ?>-option-tasmota device<?php echo $devicenum; ?>-option-http device<?php echo $devicenum; ?>-option-avm device<?php echo $devicenum; ?>-option-mystrom hide">
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
													<span class="form-text small">Parameter in % Ladezustand. 0% deaktiviert die Funktion. Bei deaktivierter Funktion oder wenn der Ladezustand grösser gleich dem Parameter ist, wird die Speicherleistung bei der Berechnung der Ein- und Ausschaltschwelle berücksichtigt.<br>
													Unterhalb dieses Wertes ist für die Berechnung der Ein und Ausschaltschwelle nur die aktuelle Leisung am EVU Punkt und die maximal mögliche Speicherladung (als Offset) relevant.</span>
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
										<span class="form-text small">Anzahl der Temperatursensoren die an einem Shelly Unterputzgerät anschließbar sind.</span>
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
										<span class="form-text small">Diese Option sorgt dafür, dass das Gerät zusätzlich in den Hausverbrauch eingerechnet wird (Startseite, neues logging).</span>
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
											<option value="shelly" data-option="shelly">Shelly oder Shelly plus</option>
											<option value="we514" data-option="we514">WE514</option>
											<option value="avm" data-option="avm">AVM</option>
											<option value="mqtt" data-option="mqtt">Mqtt</option>
											<option value="smaem" data-option="smaem">SMA Energy Meter</option>
											<option value="sdm120" data-option="sdm630">SDM120</option>
										</select>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-shelly deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm120 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-we514 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-mystrom deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-fronius deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-avm hide">
									<label for="device_measureipDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input id="device_measureipDevices<?php echo $devicenum; ?>" name="device_measureip" class="form-control" type="text" required="required" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" data-default="192.168.1.1" value="192.168.1.1" inputmode="text"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 hide; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm120 hide; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-we514 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-fronius hide">
									<label for="device_measureidDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">ID des Zählers</label>
									<div class="col">
										<input id="device_measureidDevices<?php echo $devicenum; ?>" name="device_measureid" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="255" data-default="1" value="1"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm120 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-sdm630 hide">
									<label for="device_measurePortSdmDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Modbusport des Zählers</label>
									<div class="col">
										<input id="device_measurePortSdmDevices<?php echo $devicenum; ?>" name="device_measurePortSdm" class="form-control naturalNumber" type="number" inputmode="decimal" required min="1" max="9999" data-default="8899" value="8899"  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Standardeinstellungen verschiedener Geräte:<br />
											SDM630: 8899<br />
											Elgris: 502
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
											Hier bitte eine URL angeben, die einen absoluten Zählerstand übermittelt. Diese Einstellung ist optional. Wird das Feld leer gelassen, dann wird intern ein Zähler simuliert.<br />
											<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-json hide">
									<label for="device_measurejsonurlDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">JSON-URL</label>
									<div class="col">
										<input id="device_measurejsonurlDevices<?php echo $devicenum; ?>" name="device_measurejsonurl" class="form-control" type="url" required="required" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Hier bitte eine URL angeben, deren Antwort die aktuelle Leistung sowie den Zählerstand übermittelt.<br />
											<span class="text-info">Wenn in der URL ein Prozentzeichen "%" enthalten ist, muss dieses durch ein weiteres "%" ergänzt werden ("%" -> "%%"), da ansonsten die Daten nicht gespeichert werden können.</span>
										</span>
									</div>
								</div>
								<div class="form-row mb-1 deviceMeasureTypeDevices<?php echo $devicenum; ?>-option deviceMeasureTypeDevices<?php echo $devicenum; ?>-option-json hide">
									<label for="device_measurejsonpowerDevices<?php echo $devicenum; ?>" class="col-md-4 col-form-label">Abfrage Leistung</label>
									<div class="col">
										<input id="device_measurejsonpowerDevices<?php echo $devicenum; ?>" name="device_measurejsonpower" class="form-control" type="text" required="required" data-default="" value=""  data-topicprefix="openWB/config/get/SmartHome/" data-topicsubgroup="Devices/<?php echo $devicenum; ?>/">
										<span class="form-text small">
											Hier bitte den Ausdruck angeben, mit dem die aktuelle Leistung aus der Antwort ermittelt werden kann.<br />
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
										<input id="maxBatteryPower" name="maxBatteryPower" class="form-control naturalNumber" type="number" required="required" min="0" max="10000" value="0" data-default="0" data-topicprefix="openWB/config/get/SmartHome/">
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

					if ( elementId == 'device_differentMeasurementDevices<?php echo $devicenum; ?>') {
						visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>( mqttpayload );
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

					$('#device_differentMeasurementDevices<?php echo $devicenum; ?>').change(function(){
						visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>();
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
					visibility_device_differentMeasurementDevices<?php echo $devicenum; ?>();
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
