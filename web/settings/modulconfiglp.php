<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Einstellungen</title>
		<meta name="description" content="Control your charge" />
		<meta name="author" content="Michael Ortenstein" />
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

		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>

		<?php
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Modulkonfiguration Ladepunkte</h1>
			<form action="./settings/saveconfig.php" method="POST">

				<!-- Ladepunkt 1 -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						Ladepunkt 1
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="lp1name" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="lp1name" id="lp1name" value="<?php echo $lp1nameold ?>">
								</div>
							</div>
						</div>
						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="evsecon" class="col-md-4 col-form-label">Anbindung</label>
							<div class="col">
								<select name="evsecon" id="evsecon" class="form-control">
									<optgroup label="openWB">
										<option <?php if($evseconold == "daemon") echo "selected" ?> value="daemon">openWB Daemon</option>
										<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/ttyUSB0" && $mpm3pmllidold == "0") echo "selected" ?> value="modbusevse" data-id="openwb auto">Series1/2 Autoerkennung</option>
										<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/ttyUSB0" && $mpm3pmllidold == "5") echo "selected" ?> value="modbusevse" data-id="openwb series1/2">Series1/2</option>
										<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/ttyUSB0" && $mpm3pmllidold == "105") echo "selected" ?> value="modbusevse" data-id="openwb series1/2 mid v1">Series1/2 mit geeichtem Zähler Variante 1</option>
										<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/serial0" && $mpm3pmllidold == "105") echo "selected" ?> value="modbusevse" data-id="openwb series1/2 mid v2">Series1/2 mit geeichtem Zähler Variante 2</option>
										<option <?php if($evseconold == "buchse") echo "selected" ?> value="buchse">Buchse</option>
										<option <?php if($evseconold == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
										<option <?php if($evseconold == "owbpro") echo "selected" ?> value="owbpro">openWB Pro</option>
										<option <?php if($evseconold == "masterethframer") echo "selected" ?> value="masterethframer">Ladepunkt in Verbindung mit Standalone</option>
										<option <?php if($evseconold == "ipevse") echo "selected" ?> value="ipevse">Satellit </option>
									</optgroup>
									<optgroup label="andere Ladepunkte">
										<option <?php if($evseconold == "goe") echo "selected" ?> value="goe">Go-e</option>
										<option <?php if($evseconold == "keba") echo "selected" ?> value="keba">Keba</option>
										<option <?php if($evseconold == "nrgkick") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
										<option <?php if($evseconold == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi / smartWB</option>
										<option <?php if($evseconold == "twcmanager") echo "selected" ?> value="twcmanager">Tesla TWC mit TWCManager</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($evseconold == "dac") echo "selected" ?> value="dac">DAC</option>
										<option <?php if($evseconold == "httpevse") echo "selected" ?> value="httpevse">HTTP</option>
										<option <?php if($evseconold == "modbusevse" && !($ladeleistungmodulold == "mpm3pmll" && ($mpm3pmllsourceold == "/dev/ttyUSB0" || $mpm3pmllsourceold == "/dev/serial0") && ($mpm3pmllidold == "0" || $mpm3pmllidold == "5" || $mpm3pmllidold == "105"))) echo "selected" ?> value="modbusevse">Modbusevse</option>
										<option <?php if($evseconold == "mqttevse") echo "selected" ?> value="mqttevse">MQTT</option>
									</optgroup>
								</select>
							</div>
						</div>
						<div id="evseconmastereth" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="mpm3pmethllframer">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="openwb12" class="hide">
							<!-- default values for openwb12 -->
							<input type="hidden" name="modbusevseid" value="1">
							<input type="hidden" name="ladeleistungmodul" value="mpm3pmll">
							<input type="hidden" name="mpm3pmllsource" value="/dev/ttyUSB0">
							<input type="hidden" name="modbusevsesource" value="/dev/ttyUSB0">
							<input type="hidden" name="mpm3pmllid" value="5">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2.
							</div>
						</div>
						<div id="openwbauto" class="hide">
							<!-- default values for openwbauto -->
							<input type="hidden" name="modbusevseid" value="0">
							<input type="hidden" name="ladeleistungmodul" value="mpm3pmll">
							<input type="hidden" name="mpm3pmllsource" value="/dev/ttyUSB0">
							<input type="hidden" name="modbusevsesource" value="/dev/ttyUSB0">
							<input type="hidden" name="mpm3pmllid" value="0">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option für fertige openWB series1 oder series2.<br>
							</div>
						</div>
						<div id="openwbbuchse" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="llbuchse">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option für die openWB mit Buchse.
							</div>
						</div>
						<div id="openwbdaemon" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="lldaemonlp1">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option für eine fertige openWB und bietet eine optimale und schnelle Auslesung.
							</div>
						</div>

						<div id="openwb12mid" class="hide">
							<!-- default values for openwb12mid -->
							<input type="hidden" name="modbusevseid" value="1">
							<input type="hidden" name="ladeleistungmodul" value="mpm3pmll">
							<input type="hidden" name="mpm3pmllsource" value="/dev/ttyUSB0">
							<input type="hidden" name="modbusevsesource" value="/dev/ttyUSB0">
							<input type="hidden" name="mpm3pmllid" value="105">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="openwb12v2mid" class="hide">
							<!-- default values for openwb12v2mid -->
							<input type="hidden" name="modbusevseid" value="1">
							<input type="hidden" name="ladeleistungmodul" value="mpm3pmll">
							<input type="hidden" name="mpm3pmllsource" value="/dev/serial0">
							<input type="hidden" name="modbusevsesource" value="/dev/serial0">
							<input type="hidden" name="mpm3pmllid" value="105">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="evsecondac" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="dacregister" class="col-md-4 col-form-label">Dacregister</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="99" step="1" name="dacregister" id="dacregister" value="<?php echo $dacregisterold ?>">
										<span class="form-text small">
											Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP.
											Der benötigte Wert sollte <a href="/openWB/ramdisk/i2csearch">HIER</a> zu finden sein.
											Alternativ herauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconswifi" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="simpleevsewifi">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsewifiiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evsewifiiplp1" id="evsewifiiplp1" value="<?php echo $evsewifiiplp1old ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evsewifitimeoutlp1" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="evsewifitimeoutlp1" id="evsewifitimeoutlp1" value="<?php echo $evsewifitimeoutlp1old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconextopenwb" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="extopenwblp1">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="chargep1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep1ip" id="chargep1ip" value="<?php echo $chargep1ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="chargep1cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="2" step="1" name="chargep1cp" id="chargep1cp" value="<?php echo $chargep1cpold ?>">
										<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconowbpro" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="owbprolp1">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="chargep1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="owbpro1ip" id="owbpro1ip" value="<?php echo $owbpro1ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="evseconmod" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="modbusevsesource" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="modbusevsesource" id="modbusevsesource" value="<?php echo $modbusevsesourceold ?>">
										<span class="form-text small">Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="modbusevseid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="modbusevseid" id="modbusevseid" value="<?php echo $modbusevseidold ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="modbusevselanip" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="modbusevselanip" id="modbusevselanip" value="<?php echo $modbusevselanipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconipevse" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evseiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp1" id="evseiplp1" value="<?php echo $evseiplp1old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Aufgedruckt auf dem Label der openWB.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseidlp1" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp1" id="evseidlp1" value="<?php echo $evseidlp1old ?>">
										<span class="form-text small">Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconkeba" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="keballlp1">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="kebaiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="kebaiplp1" id="kebaiplp1" value="<?php echo $kebaiplp1old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Erforder eine Keba C- oder X- Series. Die Smart Home Funktion (UDP Schnittstelle) muss per DIP Switch in der Keba aktiviert sein!
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconhttp" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="httpevseip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="httpevseip" id="httpevseip" value="<?php echo $httpevseipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Der Ampere sollwert wird an http://$IP/setcurrent?current=$WERT gesendet.
											Für eine korrekte Funktion ist als Ladeleistungsmodul HTTP zu wählen.
											WERT kann sein: 0 = keine Ladung erlaubt, 6-32 = x Ampere erlaubt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu lesen:<br>
								<span class="text-info">openWB/lp/1/AConfigured</span> Stromvorgabe in A<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/lp/1/plugStat</span> Status, ob ein Fahrzeug angesteckt ist, nur 0 (nein) oder 1 (ja)<br>
								<span class="text-info">openWB/set/lp/1/chargeStat</span> Status, ob gerade geladen wird, nur 0 (nein) oder 1 (ja)
							</div>
						</div>
						<div id="evsecontwcmanager" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="twcmanagerlp1">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col-md-4">
										HTTPControl / Ngardiner Fork
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($twcmanagerlp1httpcontrolold == 0) echo " active" ?>">
											<input type="radio" name="twcmanagerlp1httpcontrol" id="twcmanagerlp1httpcontrolOff" value="0"<?php if($twcmanagerlp1httpcontrolold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($twcmanagerlp1httpcontrolold == 1) echo " active" ?>">
											<input type="radio" name="twcmanagerlp1httpcontrol" id="twcmanagerlp1httpcontrolOn" value="1"<?php if($twcmanagerlp1httpcontrolold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="twcmanagerlp1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="twcmanagerlp1ip" id="twcmanagerlp1ip" value="<?php echo $twcmanagerlp1ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1 input-port">
									<label for="twcmanagerlp1port" class="col-md-4 col-form-label">Port</label>
									<div class="col">
										<input class="form-control" type="number" min="80" max="10000" step="1" name="twcmanagerlp1port" id="twcmanagerlp1port" value="<?php echo $twcmanagerlp1portold ?>">
										<span class="form-text small">Port des HTTP Control Interface. Standard: 8080</span>
									</div>
								</div>
								<div class="form-row mb-1 input-phases">
									<label for="twcmanagerlp1phasen" class="col-md-4 col-form-label">Anzahl Phasen</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="3" step="1" name="twcmanagerlp1phasen" id="twcmanagerlp1phasen" value="<?php echo $twcmanagerlp1phasenold ?>">
										<span class="form-text small">Definiert die genutzte Anzahl der Phasen zur korrekten Errechnung der Ladeleistung (BETA).</span>
									</div>
								</div>
							</div>
						</div>
						<script>
							$(function() {
								function visibility_twcmanagerlp1_connection() {
									if($('#twcmanagerlp1httpcontrolOff').prop("checked")) {
										hideSection('#evsecontwcmanager .input-port');
										showSection('#evsecontwcmanager .input-phases');
									} else {
										showSection('#evsecontwcmanager .input-port');
										hideSection('#evsecontwcmanager .input-phases');
									}
								}

								$('input[type=radio][name=twcmanagerlp1httpcontrol]').change(function(){
									visibility_twcmanagerlp1_connection();
								});

	       							visibility_twcmanagerlp1_connection();
							});
						</script>

						<div id="evsecongoe" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="goelp1">
							<div class="form-group">
								<div class="alert alert-info">
									Seit Firmware Version 0.40 wird PV-Laden besser unterstützt. 
									<span class="text-danger">
										Bitte halten Sie die go-e Firmware auf einem aktuellen Stand.
									</span>
								</div>
								<div class="form-row mb-1">
									<label for="goeiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="goeiplp1" id="goeiplp1" value="<?php echo $goeiplp1old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="goetimeoutlp1" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="goetimeoutlp1" id="goetimeoutlp1" value="<?php echo $goetimeoutlp1old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconnrgkick" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="nrgkicklp1">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="nrgkickiplp1" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="nrgkickiplp1" id="nrgkickiplp1" value="<?php echo $nrgkickiplp1old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Zu finden in der NRGKick App unter Einstellungen -> Info -> NRGkick Connect Infos.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkicktimeoutlp1" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="nrgkicktimeoutlp1" id="nrgkicktimeoutlp1" value="<?php echo $nrgkicktimeoutlp1old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des NRGKick Connect gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der NRGKick z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickmaclp1" class="col-md-4 col-form-label">MAC Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$" name="nrgkickmaclp1" id="nrgkickmaclp1" value="<?php echo $nrgkickmaclp1old ?>">
										<span class="form-text small">
											Gültige Werte MAC Adresse im Format: 11:22:33:AA:BB:CC<br>
											Zu finden In der NRGKick App unter Einstellungen -> BLE-Mac.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickpwlp1" class="col-md-4 col-form-label">Password</label>
									<div class="col">
										<input class="form-control" type="password" name="nrgkickpwlp1" id="nrgkickpwlp1" value="<?php echo $nrgkickpwlp1old ?>">
										<span class="form-text small">
											Password, welches in der NRGKick App festgelegt wurde.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="llmodullp1" class="hide">
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="ladeleistungmodul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungmodul" id="ladeleistungmodul" class="form-control">
										<option <?php if($ladeleistungmodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
										<optgroup label="openWB">
											<option <?php if($ladeleistungmodulold == "mpm3pmlllp1") echo "selected" ?> value="mpm3pmlllp1">openWB Satellit</option>
											<option <?php if($ladeleistungmodulold == "mpm3pmtripple") echo "selected" ?> value="mpm3pmtripple">openWB Tripple</option>
										</optgroup>
										<optgroup label="andere Messgeräte">
											<option <?php if($ladeleistungmodulold == "fsm63a3modbusll") echo "selected" ?> value="fsm63a3modbusll">FSM63A3 Modbus</option>
											<option <?php if($ladeleistungmodulold == "mpm3pmll") echo "selected" ?> value="mpm3pmll">MPM3PM</option>
											<option <?php if($ladeleistungmodulold == "sdm120modbusll") echo "selected" ?> value="sdm120modbusll">SDM 120 Modbus</option>
											<option <?php if($ladeleistungmodulold == "sdm630modbusll") echo "selected" ?> value="sdm630modbusll">SDM 630 Modbus</option>
											<option <?php if($ladeleistungmodulold == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">Simple EVSE Wifi</option>
										</optgroup>
										<optgroup label="generische Module">
											<option <?php if($ladeleistungmodulold == "httpll") echo "selected" ?> value="httpll">HTTP</option>
											<option <?php if($ladeleistungmodulold == "mqttll") echo "selected" ?> value="mqttll">MQTT</option>
										</optgroup>
									</select>
								</div>
							</div>
							<div id="llmnone" class="hide">
							</div>
							<div id="mpm3pmlllp1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpmlp1ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp1ip" id="mpmlp1ip" value="<?php echo $mpmlp1ipold ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse des Modbus Ethernet Konverters im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp1id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp1id" id="mpmlp1id" value="<?php echo $mpmlp1idold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="httpll" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="httpll_w_url" class="col-md-4 col-form-label">URL Ladeleistung in Watt</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_w_url" id="httpll_w_url" value="<?php echo htmlspecialchars($httpll_w_urlold) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Watt sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_kwh_url" class="col-md-4 col-form-label">URL Zählerstand in kWh</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_kwh_url" id="httpll_kwh_url" value="<?php echo htmlspecialchars($httpll_kwh_urlold) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in kWh mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_a1_url" class="col-md-4 col-form-label">URL Stromstärke Phase 1</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_a1_url" id="httpll_a1_url" value="<?php echo htmlspecialchars($httpll_a1_urlold) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Ampere mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_a2_url" class="col-md-4 col-form-label">URL Stromstärke Phase 2</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_a2_url" id="httpll_a2_url" value="<?php echo htmlspecialchars($httpll_a2_urlold) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Ampere mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_a3_url" class="col-md-4 col-form-label">URL Stromstärke Phase 3</label>
										<div class="col">
											<input class="form-control" type="text" name="httpll_a3_url" id="httpll_a3_url" value="<?php echo htmlspecialchars($httpll_a3_urlold) ?>">
											<span class="form-text small">
												Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes, wird der Wert auf null gesetzt.
												Der Wert muss in Ampere mit einem Punkt als Trennzeichen für Nachkommastellen sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="httpll_ip" class="col-md-4 col-form-label">IP Adresse Plug/Charge Status</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="httpll_ip" id="httpll_ip" value="<?php echo $httpll_ipold ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12<br>
												Abgerufene werden die Urls <span class="text-info">http://IP/plugstat</span> und <span class="text-info">http://IP/chargestat</span>.
												Rückgabe ist jeweils 0 oder 1. Plugstat gibt an ob ein Stecker steckt, Chargestat gibt an, ob EVSEseitig die Ladung aktiv ist
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llmpm3pm" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpm3pmllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="mpm3pmllsource" id="mpm3pmllsource" value="<?php echo $mpm3pmllsourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das MPM3PM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpm3pmllid" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmllid" id="mpm3pmllid" value="<?php echo $mpm3pmllidold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llmfsm" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="fsm63a3modbusllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="fsm63a3modbusllsource" id="fsm63a3modbusllsource" value="<?php echo $fsm63a3modbusllsourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das fsm63a3 angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="fsm63a3modbusllid" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="fsm63a3modbusllid" id="fsm63a3modbusllid" value="<?php echo $fsm63a3modbusllidold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des fsm63a3.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llmsdm" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630modbusllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm630modbusllsource" id="sdm630modbusllsource" value="<?php echo $sdm630modbusllsourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm630modbusllid" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm630modbusllid" id="sdm630modbusllid" value="<?php echo $sdm630modbusllidold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="sdm120div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm120modbusllsource" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm120modbusllsource" id="sdm120modbusllsource" value="<?php echo $sdm120modbusllsourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid1" class="col-md-4 col-form-label">ID Phase 1</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid1" id="sdm120modbusllid1" value="<?php echo $sdm120modbusllid1old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der ersten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid2" class="col-md-4 col-form-label">ID Phase 2</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid2" id="sdm120modbusllid2" value="<?php echo $sdm120modbusllid2old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase. Wenn nicht vorhanden 254 eintragen.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3" id="sdm120modbusllid3" value="<?php echo $sdm120modbusllid3old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase. Wenn nicht vorhanden 254 eintragen.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="rs485lanlp1" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630modbuslllanip" class="col-md-4 col-form-label">IP Adresse RS485/Lan-Konverter</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sdm630modbuslllanip" id="sdm630modbuslllanip" value="<?php echo $sdm630modbuslllanipold ?>">
											<span class="form-text small">
												Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
												Gültige Werte IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="llswifi" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="mqttll" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/1/W</span> Ladeleistung in Watt, int, positiv<br>
									<span class="text-info">openWB/set/lp/1/kWhCounter</span> Zählerstand in kWh, float, Punkt als Trenner, nur positiv<br>
									Optional zusätzlich:<br>
									<span class="text-info">openWB/set/lp/1/VPhase1</span> Spannung Phase 1, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/1/VPhase2</span> Spannung Phase 2, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/1/VPhase3</span> Spannung Phase 3, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/1/APhase1</span> Strom Phase 1, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/1/APhase2</span> Strom Phase 2, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/1/APhase3</span> Strom Phase 3, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/1/HzFrequenz</span> Netzfrequenz, float, Punkt als Trenner, nur positiv
								</div>
							</div>
						</div>

						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="socmodul" class="col-md-4 col-form-label">SOC Modul</label>
							<div class="col">
								<select name="socmodul" id="socmodul" class="form-control">
									<option <?php if($socmodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<optgroup label="universelle Module">
										<option <?php if($socmodulold == "soc_evcc") echo "selected" ?> value="soc_evcc">EVCC</option>
										<option <?php if($socmodulold == "soc_evnotify") echo "selected" ?> value="soc_evnotify">EVNotify</option>
										<option <?php if($socmodulold == "soc_http") echo "selected" ?> value="soc_http">HTTP</option>
										<option <?php if($socmodulold == "soc_manual") echo "selected" ?> value="soc_manual">Manuell + Berechnung</option>
										<option <?php if($socmodulold == "soc_mqtt") echo "selected" ?> value="soc_mqtt">MQTT</option>
										<option <?php if($socmodulold == "soc_tronity") echo "selected" ?> value="soc_tronity">Tronity</option>
									</optgroup>
									<optgroup label="Fahrzeughersteller">
										<option <?php if($socmodulold == "soc_aiways") echo "selected" ?> value="soc_aiways">Aiways</option>
										<option <?php if($socmodulold == "soc_audi") echo "selected" ?> value="soc_audi">Audi</option>
										<option <?php if($socmodulold == "soc_i3") echo "selected" ?> value="soc_i3">BMW &amp; Mini</option>
										<option <?php if($socmodulold == "soc_kia") echo "selected" ?> value="soc_kia">Kia / Hyundai</option>
										<option <?php if($socmodulold == "soc_eq") echo "selected" ?> value="soc_eq">Mercedes EQ</option>
										<option <?php if($socmodulold == "soc_myopel") echo "selected" ?> value="soc_myopel">MyOpel</option>
										<option <?php if($socmodulold == "soc_mypeugeot") echo "selected" ?> value="soc_mypeugeot">MyPeugeot</option>
										<option <?php if($socmodulold == "soc_myrenault") echo "selected" ?> value="soc_myrenault">MyRenault</option>
										<option <?php if($socmodulold == "soc_leaf") echo "selected" ?> value="soc_leaf">Nissan Leaf</option>
										<option <?php if($socmodulold == "soc_psa") echo "selected" ?> value="soc_psa">PSA (Peugeot/Citroen/DS/Opel/Vauxhall)</option>
										<option <?php if($socmodulold == "soc_zoe") echo "selected" ?> value="soc_zoe">Renault Zoe (alt)</option>
										<option <?php if($socmodulold == "soc_tesla") echo "selected" ?> value="soc_tesla">Tesla</option>
										<option <?php if($socmodulold == "soc_vag") echo "selected" ?> value="soc_vag">VAG</option>
										<option <?php if($socmodulold == "soc_volvo") echo "selected" ?> value="soc_volvo">Volvo</option>
										<option <?php if($socmodulold == "soc_carnet") echo "selected" ?> value="soc_carnet">VW Carnet</option>
										<option <?php if($socmodulold == "soc_id") echo "selected" ?> value="soc_id">VW ID-alt</option>
										<option <?php if($socmodulold == "soc_vwid") echo "selected" ?> value="soc_vwid">VW ID</option>
										<option <?php if($socmodulold == "soc_zerong") echo "selected" ?> value="soc_zerong">Zero NG</option>
									</optgroup>
								</select>
								<div id="socoldevccwarning" class="mt-1 alert alert-danger hide">
									Dieses Modul nutzt eine nicht mehr unterstützte Version von EVCC-SOC und wird nicht weiter gepflegt.
								</div>
								<div id="socsupportinfo" class="mt-1 alert alert-success hide">
									Support für dieses Modul gibt es im <a id="socsuportlink" href="#" target="_blank" rel="noopener noreferrer">openWB Forum</a>.
								</div>
								<div id="socnosupportinfo" class="mt-1 alert alert-warning hide">
									Dieses Modul wird nicht aktiv gepflegt.
								</div>
							</div>
						</div>
						<div id="socmodullp1" class="hide">
							<div id="stopsocnotpluggedlp1" class="form-group hide">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">SoC nur Abfragen wenn Auto angesteckt</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($stopsocnotpluggedlp1old == 0) echo " active" ?>">
												<input type="radio" name="stopsocnotpluggedlp1" id="stopsocnotpluggedlp1Off" value="0"<?php if($stopsocnotpluggedlp1old == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($stopsocnotpluggedlp1old == 1) echo " active" ?>">
												<input type="radio" name="stopsocnotpluggedlp1" id="stopsocnotpluggedlp1On" value="1"<?php if($stopsocnotpluggedlp1old == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
										<span class="form-text small">
											Wenn Ja gewählt wird der SoC nur abgefragt während ein Auto angesteckt ist.
											Bei Nein wird immer entsprechend der SoC Modul Konfiguration abgefragt.
											Funktioniert nur wenn der "steckend" Status korrekt angezeigt wird.
										</span>
									</div>
								</div>
							</div>
							<div id="socmnone" class="hide">
								<!-- nothing here -->
							</div>
							<div id="socmanual" class="hide">
								<div class="alert alert-info">
									Beim Anstecken des Fahrzeugs muss der aktuelle SoC (am Display oder über einen Browser) angegeben werden.
									Anhand des Zählers im Ladepunkt wird dann der aktuelle SoC errechnet. Ausschlaggebend für die Qualität dieses Moduls sind die beiden Einstellungen "Akkugröße" und "Wirkungsgrad".<br>
								</div>
								<div class="form-row mb-1">
									<label for="akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="akkuglp1" value="<?php echo $akkuglp1old ?>">
										<span class="form-text small">
											Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
											Die Netto-Kapazität unterscheidet sich meist von den Angaben der Fahrzeughersteller. So besitzt ein Tesla Model S 90 z. B. nur ca. 83kWh und nicht die durch die Typenbezeichnung suggerierten 90kWh.
											Andere Hersteller begrenzen die nutzbare Kapazität absichtlich, um eine höhere Lebensdauer der Akkus zu erreichen. Gängig sind eine Drosselung auf 90% der angegebenen Brutto-Kapazität.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="wirkungsgradlp1" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp1" id="wirkungsgradlp1" value="<?php echo $wirkungsgradlp1old ?>">
										<span class="form-text small">
											Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
											Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
											Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
											Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
											SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
											SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
										</span>
									</div>
								</div>
							</div>
							<div id="socmqtt" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/1/%Soc</span> Ladezustand in %, int, 0-100
								</div>
							</div>
							<div id="socmtesla" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_tesla_username" class="col-md-4 col-form-label">E-Mail</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_tesla_username" id="soc_tesla_username" value="<?php echo $soc_tesla_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Tesla Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tesla_login_btn" class="col-md-4 col-form-label">Anmeldedaten prüfen</label>
										<div class="col">
											<button type="button" class="btn btn-success soc-tesla-login-btn" data-email="#soc_tesla_username" value="1">Bei Tesla anmelden</button>
											<button type="button" class="btn btn-danger soc-tesla-clear-btn" value="1">Anmeldedaten entfernen</button>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tesla_carnumber" class="col-md-4 col-form-label">Auto im Account</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_tesla_carnumber" id="soc_tesla_carnumber" value="<?php echo $soc_tesla_carnumberold ?>">
											<span class="form-text small">
												Im Normalfall hier 0 eintragen. Sind mehrere Teslas im Account für den zweiten Tesla eine 1 eintragen.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tesla_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_tesla_intervall" id="soc_tesla_intervall" value="<?php echo $soc_tesla_intervallold ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos abgefragt werden soll, wenn nicht geladen wird.<br>
												Damit das Auto in den Standby gehen kann und die Energieverluste gering bleiben, sollte das Intervall mindestens eine Stunde ("60") betragen, besser 12 Stunden ("720") oder mehr.<br>
												Zu Beginn einer Ladung wird das Auto immer geweckt, um den aktuellen SoC zu erhalten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tesla_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_tesla_intervallladen" id="soc_tesla_intervallladen" value="<?php echo $soc_tesla_intervallladenold ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos während des Ladens abgefragt werden soll.<br>
												Je nach Ladeleistung werden 5 - 10 Minuten empfohlen, damit eventuell eingestellte SoC-Grenzen rechtzeitig erkannt werden können.
											</span>
										</div>
									</div>
								</div>
								<script>
									$(function() {
										var teslaUrl = "/openWB/modules/soc_tesla/tesla.php";

										$('.soc-tesla-login-btn').click(function(){
											var chargepoint = $(this).val();
											var email = $($(this).attr('data-email')).val();
											var teslaLoginUrl = teslaUrl+"?chargepoint="+chargepoint+"&email="+email;
											// console.log("chargepoint: "+chargepoint+" email: "+email+" url: "+teslaLoginUrl);
											window.open(teslaLoginUrl, '_tesla_login').focus();
										});

										$('.soc-tesla-clear-btn').click(function(){
											var chargepoint = $(this).val();
											var teslaCleanupUrl = teslaUrl+"?chargepoint="+chargepoint+"&go=cleanup";
											// console.log("chargepoint: "+chargepoint+" email: "+email+" url: "+teslaLoginUrl);
											window.open(teslaCleanupUrl, '_tesla_login').focus();
										});
									});
								</script>
							</div>
							<div id="socmkia" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_bluelink_email" class="col-md-4 col-form-label">E-Mail</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_bluelink_email" id="soc_bluelink_email" value="<?php echo $soc_bluelink_emailold ?>">
											<span class="form-text small">
												Email Adresse des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_bluelink_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_bluelink_password" id="soc_bluelink_password" value="<?php echo $soc_bluelink_passwordold ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_bluelink_interval" class="col-md-4 col-form-label">Abfrageintervall</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_bluelink_interval" id="soc_bluelink_interval" value="<?php echo $soc_bluelink_intervalold ?>">
											<span class="form-text small">
												Wie oft abgefragt wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_bluelink_pin" class="col-md-4 col-form-label">PIN</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_bluelink_pin" id="soc_bluelink_pin" value="<?php echo $soc_bluelink_pinold ?>">
											<span class="form-text small">
												PIN des Accounts.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_vin" id="soc_vin" value="<?php echo $soc_vinold ?>">
											<span class="form-text small">
												VIN des Autos.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($kia_soccalclp1old == 0) echo " active" ?>">
													<input type="radio" name="kia_soccalclp1" id="kia_soccalclp1Off" value="0"<?php if($kia_soccalclp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($kia_soccalclp1old == 1) echo " active" ?>">
													<input type="radio" name="kia_soccalclp1" id="kia_soccalclp1On" value="1"<?php if($kia_soccalclp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Wenn Ja gewählt wird, wird der SoC regelmäßig über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet.<br>
												Bei Nein wird immer der SoC über die API abgefragt.
											</span>
										</div>
									</div>
									<div id="kiamanualcalcdiv" class="hide">
										<div class="form-row mb-1">
											<label for="kia_akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
											<div class="col">
												<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="kia_akkuglp1" value="<?php echo $akkuglp1old ?>">
												<span class="form-text small">
													Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_wirkungsgradlp1" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
											<div class="col">
												<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp1" id="kia_wirkungsgradlp1" value="<?php echo $wirkungsgradlp1old ?>">
												<span class="form-text small">
													Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
													Für Kia e-niro (11 kWh Lader): 85-90 Prozent<br>
													Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
													Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%.<br>
													Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
													SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
													SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
												</span>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Push-Funktion für ABRP</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($kia_abrp_enableold == 0) echo " active" ?>">
													<input type="radio" name="kia_abrp_enable" id="kia_abrp_enableOff" value="0"<?php if($kia_abrp_enableold == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($kia_abrp_enableold == 1) echo " active" ?>">
													<input type="radio" name="kia_abrp_enable" id="kia_abrp_enableOn" value="1"<?php if($kia_abrp_enableold == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Wenn Ja gew&auml;hlt wird, wird der SoC regelm&auml;&szlig;ig an ABRP &uuml;bermittelt.<br>
											</span>
										</div>
									</div>
									<div id="kia_abrp_enablediv" class="hide">
										<div class="form-row mb-1">
											<label for="kia_abrp_token" class="col-md-4 col-form-label">ABRP Token</label>
											<div class="col">
												<input class="form-control" type="text" name="kia_abrp_token" id="kia_abrp_token_text" value="<?php echo $kia_abrp_tokenold ?>">
												<span class="form-text small">
													Token vom Typ "Generic" aus den Fahrzeug-Einstellungen (mehrere Tokens per Semikolon trennen)<br>
												</span>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Erweiterte Einstellungen</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($kia_advancedold == 0) echo " active" ?>">
													<input type="radio" name="kia_advanced" id="kia_advancedOff" value="0"<?php if($kia_advancedold == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($kia_advancedold == 1) echo " active" ?>">
													<input type="radio" name="kia_advanced" id="kia_advancedOn" value="1"<?php if($kia_advancedold == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												<br>
											</span>
										</div>
									</div>
									<div id="kia_advanceddiv" class="hide">
										<div class="form-row mb-1">
											<label for="kia_adv_cachevalid" class="col-md-4 col-form-label">Cache G&uuml;ltigkeit</label>
											<div class="col">
												<input class="form-control" type="number" min="-15" step="1" name="kia_adv_cachevalid" id="kia_adv_cachevalid" value="<?php echo $kia_adv_cachevalidold ?>">
												<span class="form-text small">
													Gültigkeitsdauer des letzten Status in Minuten, z.B. nach Abstellen des Autos oder Abruf in der App (0: Abruf immer vom Auto; Default: 10)<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_adv_12v" class="col-md-4 col-form-label">12V SoC Limit</label>
											<div class="col">
												<input class="form-control" type="number" min="0" max="100" step="1" name="kia_adv_12v" id="kia_adv_12v" value="<?php echo $kia_adv_12vold ?>">
												<span class="form-text small">
													Minimaler SoC der 12V-Batterie für Abrufe in Prozent (Default: 20)<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_adv_interval_unplug" class="col-md-4 col-form-label">Abrufintervall abgesteckt</label>
											<div class="col">
												<input class="form-control" type="number" min="0" step="1" name="kia_adv_interval_unplug" id="kia_adv_interval_unplug" value="<?php echo $kia_adv_interval_unplugold ?>">
												<span class="form-text small">
													Abrufintervall bei abgestecktem Auto in Minuten (sofern freigegeben)<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_adv_ratelimit" class="col-md-4 col-form-label">Abrufsperre</label>
											<div class="col">
												<input class="form-control" type="number" min="0" step="1" name="kia_adv_ratelimit" id="kia_adv_ratelimit" value="<?php echo $kia_adv_ratelimitold ?>">
												<span class="form-text small">
													Minimaler Abstand zwischen Abrufen in Minuten (default: 15)<br>
												</span>
											</div>
										</div>
									</div>
								</div>
								<script>
									$(function() {
										function visibility_kia_soccalclp1() {
											if($('#kia_soccalclp1Off').prop("checked")) {
												hideSection('#kiamanualcalcdiv');
											} else {
												showSection('#kiamanualcalcdiv');
											}
										}
										function visibility_kia_abrp_enable() {
											if($('#kia_abrp_enableOff').prop("checked")) {
												hideSection('#kia_abrp_enablediv');
											} else {
												showSection('#kia_abrp_enablediv');
											}
										}
										function visibility_kia_advanced() {
											if($('#kia_advancedOff').prop("checked")) {
												hideSection('#kia_advanceddiv');
											} else {
												showSection('#kia_advanceddiv');
											}
										}

										$('input[type=radio][name=kia_soccalclp1]').change(function(){
											visibility_kia_soccalclp1();
										});
										$('input[type=radio][name=kia_abrp_enable]').change(function(){
											visibility_kia_abrp_enable();
										});
										$('input[type=radio][name=kia_advanced]').change(function(){
											visibility_kia_advanced();
										});

										visibility_kia_soccalclp1();
										visibility_kia_abrp_enable();
										visibility_kia_advanced();
									});
								</script>
							</div>
							<div id="socmzerong" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_zerong_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_zerong_username" id="soc_zerong_username" value="<?php echo $soc_zerong_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Zero Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zerong_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_zerong_password" id="soc_zerong_password" value="<?php echo $soc_zerong_passwordold ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zerong_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zerong_intervall" id="soc_zerong_intervall" value="<?php echo $soc_zerong_intervallold ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zerong_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zerong_intervallladen" id="soc_zerong_intervallladen" value="<?php echo $soc_zerong_intervallladenold ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird während geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socaiways" class="hide">
                                <div class="form-group">
                                    <div class="alert alert-info">
                                        Anmeldedaten fuer den Aiways U5
                                    </div>
                                    <div class="form-row mb-1">
                                        <label for="soc_aiways_user" class="col-md-4 col-form-label">Benutzername</label>
                                        <div class="col">
                                            <input class="form-control" type="text" name="soc_aiways_user" id="soc_aiways_user" value="<?php echo $soc_aiways_userold ?>">
                                            <span class="form-text small">
                                                Aiways Account Name (nicht die E-Mail-Adresse)
                                            </span>
                                        </div>
                                    </div>
                                    <div class="form-row mb-1">
                                        <label for="soc_aiways_pass" class="col-md-4 col-form-label">Passwort</label>
                                        <div class="col">
											<input class="form-control" type="password" name="soc_aiways_pass" id="soc_aiways_pass" value="<?php echo $soc_aiways_passold ?>">
                                            <span class="form-text small">
                                                Aiways Passwort
                                            </span>
                                        </div>
                                    </div>
									<div class="form-row mb-1">
                                        <label for="soc_aiways_vin" class="col-md-4 col-form-label">VIN</label>
                                        <div class="col">
                                            <input class="form-control" type="text" name="soc_aiways_vin" id="soc_aiways_vin" value="<?php echo $soc_aiways_vinold ?>">
                                            <span class="form-text small">
                                                 VIN des Fahrzeugs
                                            </span>
                                        </div>
                                    </div>
                                    <div class="form-row mb-1">
                                        <label for="soc_aiways_intervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
                                        <div class="col">
											<input class="form-control" type="text" name="soc_aiways_intervall" id="soc_aiways_intervall" value="<?php echo $soc_aiways_intervallold ?>">
                                            <span class="form-text small">
                                                Verkürzt das Abfrageintervall beim Laden auf xx Minuten
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>						
							<div id="socmaudi" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_audi_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_audi_username" id="soc_audi_username" value="<?php echo $soc_audi_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_audi_passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_audi_passwort" id="soc_audi_passwort" value="<?php echo $soc_audi_passwortold ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_audi_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_audi_vin" id="soc_audi_vin" value="<?php echo $soc_audi_vinold ?>">
											<span class="form-text small">
												VIN des Fahrzeugs.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmid" class="hide">
								<div class="form-group">
									<div class="alert alert-info">
										Dieses ID Modul ist redundant und wird in zukünftigen Versionen entfernt. Bitte das VAG Modul auswählen.
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_id_username" id="soc_id_username" value="<?php echo $soc_id_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_id_passwort" id="soc_id_passwort" value="<?php echo $soc_id_passwortold ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_id_vin" id="soc_id_vin" value="<?php echo $soc_id_vinold ?>">
											<span class="form-text small">
												Vollständige VIN des Fahrzeugs.
											</span>
										</div>
									</div>

								</div>
							</div>
							<div id="socmvwid" class="hide">
								<div class="form-group">
									<div class="alert alert-info">
										Für VW Fahrzeuge. Es wird benötigt:<br>
										- We Connect (ID) Account aktiv<br>
										- We Connect ID App eingerichtet - auch für nicht-ID!<br>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_id_username" id="soc_id_username" value="<?php echo $soc_id_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_id_passwort" id="soc_id_passwort" value="<?php echo $soc_id_passwortold ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_id_vin" id="soc_id_vin" value="<?php echo $soc_id_vinold ?>">
											<span class="form-text small">
												Vollständige VIN des Fahrzeugs.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_id_intervall" id="soc_id_intervall" value="<?php echo $soc_id_intervallold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_id_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Ladevorgang</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_id_intervallladen" id="soc_id_intervallladen" value="<?php echo $soc_id_intervallladenold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socvag" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Fahrzeugtyp</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($soc_vag_typeold == 'vw') echo " active" ?>">
													<input type="radio" name="soc_vag_type" id="soc_vag_type_vw" value="vw"<?php if($soc_vag_typeold == 'vw') echo " checked=\"checked\"" ?>>VW
												</label>
												<label class="btn btn-outline-info<?php if($soc_vag_typeold == 'id') echo " active" ?>">
													<input type="radio" name="soc_vag_type" id="soc_vag_type_id" value="id"<?php if($soc_vag_typeold == 'id') echo " checked=\"checked\"" ?>>ID
												</label>
												<label class="btn btn-outline-info<?php if($soc_vag_typeold == 'porsche') echo " active" ?>">
													<input type="radio" name="soc_vag_type" id="soc_vag_type_porsche" value="porsche"<?php if($soc_vag_typeold == 'porsche') echo " checked=\"checked\"" ?>>Porsche
												</label>
											</div>
											<span class="form-text small">Auswahl Fahrzeugtyp</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_vag_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_vag_username" id="soc_vag_username" value="<?php echo $soc_vag_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_vag_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_vag_password" id="soc_vag_password" value="<?php echo $soc_vag_passwordold ?>">
											<span class="form-text small">
												Passwort des Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_vag_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_vag_vin" id="soc_vag_vin" value="<?php echo $soc_vag_vinold ?>">
											<span class="form-text small">
												Vollständige VIN des Fahrzeugs
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_vag_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_vag_intervall" id="soc_vag_intervall" value="<?php echo $soc_vag_intervallold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_vag_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Ladevorgang</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_vag_intervallladen" id="soc_vag_intervallladen" value="<?php echo $soc_vag_intervallladenold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socevcc" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_evcc_select_vehicle_lp1" class="col-md-4 col-form-label">Unterstützte Fahrzeuge</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend clickable">
													<div id="soc_evcc_load_vehicles_lp1" class="input-group-text">
														<i class="fas fa-sync"></i>
													</div>
												</div>
												<select id="soc_evcc_select_vehicle_lp1" class="form-control" readonly>
													<option value="">-- Bitte aktualisieren --</option>
												</select>
											</div>
											<span class="form-text small">
												Die Auswahlliste dient nur der einfachen Eingabe des Fahrzeugtyps.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_vehicle_id_lp1" class="col-md-4 col-form-label">Fahrzeug Typ</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														<i class="fas fa-car"></i>
													</div>
												</div>
												<input required readonly class="form-control" type="text" name="soc_evcc_type_lp1" id="soc_evcc_type_lp1" value="<?php echo $soc_evcc_type_lp1old ?>">
											</div>
											<span class="form-text small">
												Dies ist der intern verwendete Typ, nicht der lesbare Name aus der Auswahlliste.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_username_lp1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_evcc_username_lp1" id="soc_evcc_username_lp1" value="<?php echo $soc_evcc_username_lp1old ?>">
											<span class="form-text small">
												Email Adresse des Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_password_lp1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_evcc_password_lp1" id="soc_evcc_password_lp1" value="<?php echo $soc_evcc_password_lp1old ?>">
											<span class="form-text small">
												Passwort des Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_vin_lp1" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_evcc_vin_lp1" id="soc_evcc_vin_lp1" value="<?php echo $soc_evcc_vin_lp1old ?>">
											<span class="form-text small">
												Vollständige VIN des Fahrzeugs
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_token_lp1" class="col-md-4 col-form-label">Token</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_evcc_token_lp1" id="soc_evcc_token_lp1" value="<?php echo $soc_evcc_token_lp1old ?>">
											<span class="form-text small">
												EVCC Abo Token, zu beziehen unter https://cloud.evcc.io
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_evcc_intervall" id="soc_evcc_intervall" value="<?php echo $soc_evcc_intervallold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Ladevorgang</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_evcc_intervallladen" id="soc_evcc_intervallladen" value="<?php echo $soc_evcc_intervallladenold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
								<script>
									$('#soc_evcc_select_vehicle_lp1').change(function(){
										$('#soc_evcc_type_lp1').val($(this).val());
									});

									$('#soc_evcc_load_vehicles_lp1').click(function(){
										$('#soc_evcc_load_vehicles_lp1').removeClass("bg-danger");
										$('#soc_evcc_load_vehicles_lp1').removeClass("bg-success");
										$('#soc_evcc_load_vehicles_lp1').addClass("bg-warning");
										$(this).find('.fa-sync').addClass('fa-spin');
										$("#soc_evcc_select_vehicle_lp1").empty();
										$.ajax({
											type: "GET",
											url: "https://cloud.evcc.io/api/vehicles",
											success: function(vehicledata){
												$('#soc_evcc_load_vehicles_lp1').removeClass("bg-warning");
												$('#soc_evcc_load_vehicles_lp1').addClass("bg-success");
												var vehicleid = $('#soc_evcc_type_lp1').val();
												$("<option/>").val('').text("-- Bitte auswählen --").appendTo('#soc_evcc_select_vehicle_lp1');
												vehicledata.forEach(function(vehicle){
													newVehicle = $("<option/>").val(vehicle.id).text(vehicle.name);
													if( vehicleid == vehicle.id ){
														newVehicle.attr('selected','selected');
													}
													newVehicle.appendTo('#soc_evcc_select_vehicle_lp1');
												});
												$('#soc_evcc_select_vehicle_lp1').attr('readonly', false);
											},
											error: function(errMsg) {
												$('#soc_evcc_load_vehicles_lp1').removeClass("bg-warning");
												$('#soc_evcc_load_vehicles_lp1').addClass("bg-danger");
												alert("Fahrzeuge konnten nicht abgerufen werden!");
											},
											complete: function(){
												$('#soc_evcc_load_vehicles_lp1').find('.fa-sync').removeClass('fa-spin');
											}
										});
									});
								</script>
							</div>
							<div id="socmhttp" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="hsocip" class="col-md-4 col-form-label">Abfrage URL</label>
										<div class="col">
											<input class="form-control" type="text" name="hsocip" id="hsocip" value="<?php echo htmlspecialchars($hsocipold) ?>">
											<span class="form-text small">
												Gültige Werte none, "url". URL für die Abfrage des Soc, Antwort muss der reine Zahlenwert sein.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_http_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_http_intervall" id="soc_http_intervall" value="<?php echo $soc_http_intervallold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_http_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Ladevorgang</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_http_intervallladen" id="soc_http_intervallladen" value="<?php echo $soc_http_intervallladenold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmuser" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="socuser" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="socuser" id="socuser" value="<?php echo $socuserold ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="socmpass" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="socpass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="socpass" id="socpass" value="<?php echo $socpassold ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="soczoe" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="zoeusername" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="zoeusername" id="zoeusername" value="<?php echo $zoeusernameold ?>">
											<span class="form-text small">
												Renault Zoe Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="zoepasswort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="zoepasswort" id="zoepasswort" value="<?php echo $zoepasswortold ?>">
											<span class="form-text small">
											Renault Zoe Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupzoelp1old == 0) echo " active" ?>">
													<input type="radio" name="wakeupzoelp1" id="wakeupzoelp1Off" value="0"<?php if($wakeupzoelp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupzoelp1old == 1) echo " active" ?>">
													<input type="radio" name="wakeupzoelp1" id="wakeupzoelp1On" value="1"<?php if($wakeupzoelp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmyrenault" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="myrenault_userlp1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_userlp1" id="myrenault_userlp1" value="<?php echo $myrenault_userlp1old ?>">
											<span class="form-text small">
												MyRenault Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_passlp1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="myrenault_passlp1" id="myrenault_passlp1" value="<?php echo $myrenault_passlp1old ?>">
											<span class="form-text small">
												MyRenault Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_locationlp1" class="col-md-4 col-form-label">Standort</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_locationlp1" id="myrenault_locationlp1" value="<?php echo $myrenault_locationlp1old ?>">
											<span class="form-text small">
												MyRenault Standort, z.B. de_DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_countrylp1" class="col-md-4 col-form-label">Land</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_countrylp1" id="myrenault_countrylp1" value="<?php echo $myrenault_countrylp1old ?>">
											<span class="form-text small">
												MyRenault Land, z.B. CH, AT, DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soclp1_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soclp1_vin" id="soclp1_vin" value="<?php echo $soclp1_vinold ?>">
											<span class="form-text small">
												VIN des Autos. Ist nur nötig wenn es sich um ein Importfahrzeug handelt. Kann auf none belassen werden wenn die Auslesung funktioniert.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp1old == 0) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp1" id="wakeupmyrenaultlp1Off" value="0"<?php if($wakeupmyrenaultlp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp1old == 1) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp1" id="wakeupmyrenaultlp1On" value="1"<?php if($wakeupmyrenaultlp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socevnotify" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="evnotifyakey" class="col-md-4 col-form-label">Akey</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifyakey" id="evnotifyakey" value="<?php echo $evnotifyakeyold ?>">
											<span class="form-text small">
												Akey des EVNotify Kontos
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="evnotifytoken" class="col-md-4 col-form-label">Token</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifytoken" id="evnotifytoken" value="<?php echo $evnotifytokenold ?>">
											<span class="form-text small">
												Token des Kontos
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socleaf" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="leafusername" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="leafusername" id="leafusername" value="<?php echo $leafusernameold ?>">
											<span class="form-text small">
												Nissan Connect Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="leafpasswort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="leafpasswort" id="leafpasswort" value="<?php echo $leafpasswortold ?>">
											<span class="form-text small">
												Nissan Connect Passwort
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soci3" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="i3username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="i3username" id="i3username" value="<?php echo $i3usernameold ?>">
											<span class="form-text small">
												BMW Services Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="i3passwort" id="i3passwort" value="<?php echo $i3passwortold ?>">
											<span class="form-text small">
												BMW Services Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="i3vin" id="i3vin" value="<?php echo $i3vinold ?>">
											<span class="form-text small">
												BMW VIN. Sie ist in voller Länge anzugeben.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soci3intervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soci3intervall" id="soci3intervall" value="<?php echo $soci3intervallold ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soccarnet" class="hide">
								<div class="form-group">
									<div class="alert alert-info">
										Das VAG Modul kann alternativ genutzt werden und ruft den SoC in 1-Prozent Schritten ab.
									</div>
									<div class="form-row mb-1">
										<label for="carnetuser" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="carnetuser" id="carnetuser" value="<?php echo $carnetuserold ?>">
											<span class="form-text small">
												VW Carnet Benutzername. Wenn der SoC nicht korrekt angezeigt wird, z.B. weil AGB von VW geändert wurden, ist es nötig sich auf https://www.portal.volkswagen-we.com anzumelden.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="carnetpass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="carnetpass" id="carnetpass" value="<?php echo $carnetpassold ?>">
											<span class="form-text small">
												VW Carnet Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soccarnetintervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soccarnetintervall" id="soccarnetintervall" value="<?php echo $soccarnetintervallold ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmypeugeot" class="hide">
								<div class="form-group">
									<div class="card-text alert alert-info">
										Die notwendige <a href="https://developer.groupe-psa.io/webapi/b2c/quickstart/connect/#connect-your-app" target="_blank" rel="noopener noreferrer">API</a> ist derzeit von PSA noch nicht freigegeben, daher funktionieren über den dokumentierten Weg erstellte Client-IDs und Client-Secrets leider noch nicht.<br>
										Auf eigenes Risiko kann diese Anleitung genutzt werden, dies hat bisher zu guten Ergebnissen geführt und wird durch die openWB Community (nicht openWB selbst) gepflegt. <a href="https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden" target="_blank" rel="noopener noreferrer">https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden</a><br> 
										Weitere Diskussion zu diesem Thema findet sich <a href="https://openwb.de/forum/viewtopic.php?f=5&t=1206" target="_blank" rel="noopener noreferrer">im Forum.</a>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_userlp1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="mypeugeot_userlp1" id="mypeugeot_userlp1" value="<?php echo $mypeugeot_userlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_passlp1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="mypeugeot_passlp1" id="mypeugeot_passlp1" value="<?php echo $mypeugeot_passlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_clientidlp1" class="col-md-4 col-form-label">Client-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="mypeugeot_clientidlp1" id="mypeugeot_clientidlp1" value="<?php echo $mypeugeot_clientidlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_clientsecretlp1" class="col-md-4 col-form-label">Client-Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="mypeugeot_clientsecretlp1" id="mypeugeot_clientsecretlp1" value="<?php echo $mypeugeot_clientsecretlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere Peugeot SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($mypeugeot_soccalclp1old == 0) echo " active" ?>">
													<input type="radio" name="mypeugeot_soccalclp1" id="mypeugeot_soccalclp1Off" value="0"<?php if($mypeugeot_soccalclp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($mypeugeot_soccalclp1old == 1) echo " active" ?>">
													<input type="radio" name="mypeugeot_soccalclp1" id="mypeugeot_soccalclp1On" value="1"<?php if($mypeugeot_soccalclp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Aktuell liefert die Peugeot API keine SoC Aktualisierung während des Ladevorgangs.<br>
												Wenn Ja gewählt wird, wird der SoC vor dem Laden über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet. Dies erlaubt eine SoC-gesteuerte Ladung.<br>
												Bei Nein wird immer der SoC über die API abgefragt. SoC gesteuerte Ladung ist erst möglich nachdem PSA den SoC auch während des Ladens übermittelt.
											</span>
										</div>
										<div id="peugeotmanualcalcdiv" class="hide">
											<div class="form-row mb-1">
												<label for="peugeot_akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="peugeot_akkuglp1" value="<?php echo $akkuglp1old ?>">
													<span class="form-text small">
														Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>Für Peugeot e208 und e2008: 45-46kWh
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="peugeot_wirkungsgradlp1" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp1" id="peugeot_wirkungsgradlp1" value="<?php echo $wirkungsgradlp1old ?>">
													<span class="form-text small">
														Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
														Für Peugeot e208 und e2008: 96-98 Prozent<br>
														Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
														Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
														Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
														SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
														SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<script>
								$(function() {
									function visibility_mypeugeot_soccalclp1() {
										if($('#mypeugeot_soccalclp1Off').prop("checked")) {
											hideSection('#peugeotmanualcalcdiv');
										} else {
											showSection('#peugeotmanualcalcdiv');
										}
									}

									$('input[type=radio][name=mypeugeot_soccalclp1]').change(function(){
										visibility_mypeugeot_soccalclp1();
									});

									visibility_mypeugeot_soccalclp1();
								});
								</script>
							</div>
							<div id="socmyopel" class="hide">
								<div class="form-group">
									<div class="card-text alert alert-info">
										Die notwendige <a href="https://developer.groupe-psa.io/webapi/b2c/quickstart/connect/#connect-your-app" target="_blank" rel="noopener noreferrer">API</a> ist derzeit von PSA noch nicht freigegeben, daher funktionieren über den dokumentierten Weg erstellte Client-IDs und Client-Secrets leider noch nicht.<br>
										Auf eigenes Risiko kann diese Anleitung genutzt werden, dies hat bisher zu guten Ergebnissen geführt und wird durch die openWB Community (nicht openWB selbst) gepflegt. <a href="https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden" target="_blank" rel="noopener noreferrer">https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden</a><br> 
										Weitere Diskussion zu diesem Thema findet sich <a href="https://openwb.de/forum/viewtopic.php?f=5&t=1206" target="_blank" rel="noopener noreferrer">im Forum.</a>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_userlp1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="myopel_userlp1" id="myopel_userlp1" value="<?php echo $myopel_userlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_passlp1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="myopel_passlp1" id="myopel_passlp1" value="<?php echo $myopel_passlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_clientidlp1" class="col-md-4 col-form-label">Client-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="myopel_clientidlp1" id="myopel_clientidlp1" value="<?php echo $myopel_clientidlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_clientsecretlp1" class="col-md-4 col-form-label">Client-Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="myopel_clientsecretlp1" id="myopel_clientsecretlp1" value="<?php echo $myopel_clientsecretlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere MyOpel SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($myopel_soccalclp1old == 0) echo " active" ?>">
													<input type="radio" name="myopel_soccalclp1" id="myopel_soccalclp1Off" value="0"<?php if($myopel_soccalclp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($myopel_soccalclp1old == 1) echo " active" ?>">
													<input type="radio" name="myopel_soccalclp1" id="myopel_soccalclp1On" value="1"<?php if($myopel_soccalclp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Aktuell liefert die Opel API keine SoC Aktualisierung während des Ladevorgangs.<br>
												Wenn Ja gewählt wird, wird der SoC vor dem Laden über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet. Dies erlaubt eine SoC-gesteuerte Ladung.<br>
												Bei Nein wird immer der SoC über die API abgefragt. SoC gesteuerte Ladung ist erst möglich nachdem Opel/PSA den SoC auch während des Ladens übermittelt.
											</span>
										</div>
										<div id="opelmanualcalclp1div" class="hide">
											<div class="form-row mb-1">
												<label for="opel_akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="opel_akkuglp1" value="<?php echo $akkuglp1old ?>">
													<span class="form-text small">
														Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
														Für Corsa-e: 45-46kWh
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="opel_wirkungsgradlp1" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp1" id="opel_wirkungsgradlp1" value="<?php echo $wirkungsgradlp1old ?>">
													<span class="form-text small">
														Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
														Für Corsa-e: 96-98 Prozent<br>
														Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
														Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
														Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
														SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
														SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<script>
								$(function() {
									function visibility_myopel_soccalclp1() {
										if($('#myopel_soccalclp1Off').prop("checked")) {
											hideSection('#opelmanualcalclp1div');
										} else {
											showSection('#opelmanualcalclp1div');
										}
									}

									$('input[type=radio][name=myopel_soccalclp1]').change(function(){
										visibility_myopel_soccalclp1();
									});

									visibility_myopel_soccalclp1();
								});
								</script>
							</div>
							<div id="socpsa" class="hide">
								<div class="form-group">
									<div class="card-text alert alert-info">
										Die notwendige <a href="https://developer.groupe-psa.io/webapi/b2c/quickstart/connect/#connect-your-app" target="_blank" rel="noopener noreferrer">API</a> ist derzeit von PSA noch nicht freigegeben, daher funktionieren über den dokumentierten Weg erstellte Client-IDs und Client-Secrets leider noch nicht.<br>
										Auf eigenes Risiko kann diese Anleitung genutzt werden, dies hat bisher zu guten Ergebnissen geführt und wird durch die openWB Community (nicht openWB selbst) gepflegt. <a href="https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden" target="_blank" rel="noopener noreferrer">https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden</a><br> 
										Weitere Diskussion zu diesem Thema findet sich <a href="https://openwb.de/forum/viewtopic.php?f=5&t=1206" target="_blank" rel="noopener noreferrer">im Forum.</a>
									</div>
									<div class="form-row mb-1">
										<label for="psa_manufacturerlp1" class="col-md-4 col-form-label">Hersteller</label>
										<div class="col">
											<select name="psa_manufacturerlp1" id="psa_manufacturerlp1" class="form-control">
												<option <?php if($psa_manufacturerlp1old == "Peugeot") echo "selected" ?> value="Peugeot">Peugeot</option>
												<option <?php if($psa_manufacturerlp1old == "Citroen") echo "selected" ?> value="Citroen">Citroen</option>
												<option <?php if($psa_manufacturerlp1old == "DS") echo "selected" ?> value="DS">DS</option>
												<option <?php if($psa_manufacturerlp1old == "Opel") echo "selected" ?> value="Opel">Opel</option>
												<option <?php if($psa_manufacturerlp1old == "Vauxhall") echo "selected" ?> value="Vauxhall">Vauxhall</option>
											</select>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_userlp1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="psa_userlp1" id="psa_userlp1" value="<?php echo $psa_userlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_passlp1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="psa_passlp1" id="psa_passlp1" value="<?php echo $psa_passlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_clientidlp1" class="col-md-4 col-form-label">Client-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="psa_clientidlp1" id="psa_clientidlp1" value="<?php echo $psa_clientidlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_clientsecretlp1" class="col-md-4 col-form-label">Client-Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="psa_clientsecretlp1" id="psa_clientsecretlp1" value="<?php echo $psa_clientsecretlp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_intervallp1" class="col-md-4 col-form-label">Abfrageintervall</label>
										<div class="col">
											<input class="form-control" type="number" min="1" step="1" name="psa_intervallp1" id="psa_intervallp1" value="<?php echo $psa_intervallp1old ?>">
											<span class="form-text small">
												Wie oft abgefragt wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere PSA SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($psa_soccalclp1old == 0) echo " active" ?>">
													<input type="radio" name="psa_soccalclp1" id="psa_soccalclp1Off" value="0"<?php if($psa_soccalclp1old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($psa_soccalclp1old == 1) echo " active" ?>">
													<input type="radio" name="psa_soccalclp1" id="psa_soccalclp1On" value="1"<?php if($psa_soccalclp1old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Aktuell liefert die PSA API keine SoC Aktualisierung während des Ladevorgangs.<br>
												Wenn Ja gewählt wird, wird der SoC vor dem Laden über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet. Dies erlaubt eine SoC-gesteuerte Ladung.<br>
												Bei Nein wird immer der SoC über die API abgefragt. SoC gesteuerte Ladung ist erst möglich nachdem PSA den SoC auch während des Ladens übermittelt.
											</span>
										</div>
										<div id="psamanualcalcdiv" class="hide">
											<div class="form-row mb-1">
												<label for="psa_akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="psa_akkuglp1" value="<?php echo $akkuglp1old ?>">
													<span class="form-text small">
														Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
														Für Opel Corsa-e und Peugeot e208/e2008: 45-46kWh
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="psa_wirkungsgradlp1" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp1" id="psa_wirkungsgradlp1" value="<?php echo $wirkungsgradlp1old ?>">
													<span class="form-text small">
														Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
														Für Opel Corsa-e und Peugeot e208/e2008: 96-98 Prozent<br>
														Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
														Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
														Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
														SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
														SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<script>
									$(function() {
										function visibility_psa_soccalclp1() {
											if($('#psa_soccalclp1Off').prop("checked")) {
												hideSection('#psamanualcalcdiv');
											} else {
												showSection('#psamanualcalcdiv');
											}
										}

										$('input[type=radio][name=psa_soccalclp1]').change(function(){
											visibility_psa_soccalclp1();
										});

										visibility_psa_soccalclp1();
									});
								</script>
							</div>
							<div id="socmeq" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label"></label>
										<div class="col">
											<span class="form-text small font-weight-bold">
												Das Mercedes EQ SoC Modul basiert auf der Electric Vehicle Status API des Mercedes Developer Programms. Um die API zu nutzen, muss ein eigener Developer Zugang bei Mercedes beantragt werden. <br/>
												<a href="https://github.com/snaptec/openWB/wiki/EV-SoC-Modul-Mercedes-EQ" target="_blank" rel="noopener noreferrer">Eine Step-by-Step Anleitung findet ihr hier</a>
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_client_id_lp1" class="col-md-4 col-form-label">Client ID</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_client_id_lp1" id="soc_eq_client_id_lp1" value="<?php echo $soc_eq_client_id_lp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_client_secret_lp1" class="col-md-4 col-form-label">Client Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_client_secret_lp1" id="soc_eq_client_secret_lp1" value="<?php echo $soc_eq_client_secret_lp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_vin_lp1" class="col-md-4 col-form-label">Fahrzeug ident</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_vin_lp1" id="soc_eq_vin_lp1" value="<?php echo $soc_eq_vin_lp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_cb_lp1" class="col-md-4 col-form-label">Callback</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_cb_lp1" id="soc_eq_cb_lp1" value="<?php echo $soc_eq_cb_lp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label"></label>
										<div class="col">
											<span class="form-text small">
												<b>Wichtig: Nach dem Eintragen der Werte müssen diese gespeichert werden und danach einmalig der folgende Link aufgerufen werden:
												<a href="<?php echo "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&state=lp1&client_id=" . $soc_eq_client_id_lp1old . "&redirect_uri=" . $soc_eq_cb_lp1old . "&scope=mb:vehicle:mbdata:evstatus%20offline_access"?>" target="_blank" rel="noopener noreferrer">HIER bei Mercedes Me anmelden</a></b>
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soctronity" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<div class="alert alert-info">
											Für dieses Modul wird ein Konto bei <a href="https://www.tronity.io/" target="_blank" rel="noopener noreferrer">TRONITY</a> benötigt. Über <a href="https://app.tronity.io/signup/7e_-r_uXh" target="_blank" rel="noopener noreferrer">diesen Empfehlungs-Link</a> wird der kostenlose Testzeitraum auf 4 Wochen verlängert. Wie man an die benötigten Zugangsdaten für die openWB kommt, ist <a href="https://help.tronity.io/hc/de-de/articles/360020836760" target="_blank" rel="noopener noreferrer">hier erklärt</a>.
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_client_id_lp1" class="col-md-4 col-form-label">Client ID</label>
										<div class="col">
											<input class="form-control" type="text" required placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" pattern="[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}" name="soc_tronity_client_id_lp1" id="soc_tronity_client_id_lp1" value="<?php echo $soc_tronity_client_id_lp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_client_secret_lp1" class="col-md-4 col-form-label">Client Secret</label>
										<div class="col">
											<input class="form-control" type="text" required placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" pattern="[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}" name="soc_tronity_client_secret_lp1" id="soc_tronity_client_secret_lp1" value="<?php echo $soc_tronity_client_secret_lp1old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_select_vehicle_lp1" class="col-md-4 col-form-label">Fahrzeug</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend clickable">
													<div id="soc_tronity_load_vehicles_lp1" class="input-group-text">
														<i class="fas fa-sync"></i>
													</div>
												</div>
												<select id="soc_tronity_select_vehicle_lp1" class="form-control" readonly>
													<option value="">Bitte aktualisieren</option>
												</select>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_vehicle_id_lp1" class="col-md-4 col-form-label">Fahrzeug ID</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														<i class="fas fa-car"></i>
													</div>
												</div>
												<input required readonly class="form-control" type="text" name="soc_tronity_vehicle_id_lp1" id="soc_tronity_vehicle_id_lp1" value="<?php echo $soc_tronity_vehicle_id_lp1old ?>">
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_tronity_intervall" id="soc_tronity_intervall" value="<?php echo $soc_tronity_intervallold ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall in Minuten der Ladestand des Autos abgefragt werden soll, wenn nicht geladen wird.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_tronity_intervallladen" id="soc_tronity_intervallladen" value="<?php echo $soc_tronity_intervallladenold ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall in Minuten der Ladestand des Autos während des Ladens abgefragt werden soll.
											</span>
										</div>
									</div>
								</div>
								<script>
									var TronityClientPattern = /^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$/
									$('#soc_tronity_select_vehicle_lp1').change(function(){
										$('#soc_tronity_vehicle_id_lp1').val($(this).val());
									});

									$('#soc_tronity_load_vehicles_lp1').click(function(){
										if( ! $('#soc_tronity_client_id_lp1').val().match(TronityClientPattern) || ! $('#soc_tronity_client_secret_lp1').val().match(TronityClientPattern) ){
											alert("Bitte geben Sie eine gültige Client ID und ein Client Secret an.");
										} else {
											$('#soc_tronity_load_vehicles_lp1').removeClass("bg-warning");
											$('#soc_tronity_load_vehicles_lp1').removeClass("bg-success");
											$(this).find('.fa-sync').addClass('fa-spin');
											$("#soc_tronity_select_vehicle_lp1").empty();
											$.ajax({
												type: "POST",
												url: "https://api-eu.TRONITY.io/oauth/authentication",
												data: JSON.stringify( { "client_id": $('#soc_tronity_client_id_lp1').val(), "client_secret": $('#soc_tronity_client_secret_lp1').val(), "grant_type": "app" } ),
												contentType: "application/json",
												dataType: "json",
												success: function(authdata){
													$('#soc_tronity_load_vehicles_lp1').addClass("bg-warning");
													$.ajax({
														type: "GET",
														url: "https://api-eu.TRONITY.io/v1/vehicles",
														headers: {
															Authorization: 'Bearer '+authdata.access_token
														},
														success: function(vehicledata){
															$('#soc_tronity_load_vehicles_lp1').removeClass("bg-warning");
															$('#soc_tronity_load_vehicles_lp1').addClass("bg-success");
															var vehicleid = $('#soc_tronity_vehicle_id_lp1').val();
															$("<option/>").val('').text("-- Bitte auswählen --").appendTo('#soc_tronity_select_vehicle_lp1');
															vehicledata.data.forEach(function(vehicle){
																newVehicle = $("<option/>").val(vehicle.id).text(vehicle.displayName);
																if( vehicleid == vehicle.id ){
																	newVehicle.attr('selected','selected');
																}
																newVehicle.appendTo('#soc_tronity_select_vehicle_lp1');
															});
															$('#soc_tronity_select_vehicle_lp1').attr('readonly', false);
														},
														error: function(errMsg) {
															alert("Fahrzeuge konnten nicht abgerufen werden!");
														}
													});
												},
												error: function(errMsg) {
													alert("Anmeldung gescheitert!");
												},
												complete: function(){
													$('#soc_tronity_load_vehicles_lp1').find('.fa-sync').removeClass('fa-spin');
												}
											});
										};
									});
								</script>
							</div>
						</div>
					</div>
					<script>
						// visibility of charge point types
						function display_lp1() {
							hideSection('#llmodullp1');
							hideSection('#evsecondac');
							hideSection('#evseconmod');
							hideSection('#evseconswifi');
							hideSection('#evsecongoe');
							hideSection('#evseconnrgkick');
							hideSection('#evseconmastereth');
							hideSection('#evseconkeba');
							hideSection('#openwb12');
							hideSection('#openwbauto');
							hideSection('#openwb12mid');
							hideSection('#openwb12v2mid');
							hideSection('#evseconhttp');
							hideSection('#evsecontwcmanager');
							hideSection('#evseconipevse');
							hideSection('#openwbbuchse');
							hideSection('#openwbdaemon');
							hideSection('#evseconextopenwb');
							hideSection('#evseconowbpro');
							hideSection('#evseconmqtt');

							if($('#evsecon').val() == 'modbusevse') {
								switch( $("#evsecon option:selected").attr('data-id') ){
									case "openwb series1/2":
										showSection('#openwb12');
									break;
									case "openwb auto":
										showSection('#openwbauto');
									break;
									case "openwb series1/2 mid v1":
										showSection('#openwb12mid');
									break;
									case "openwb series1/2 mid v2":
										showSection('#openwb12v2mid');
									break;
									default:
										showSection('#evseconmod');
										showSection('#llmodullp1');
										display_llmp1();
								}
							}
							if($('#evsecon').val() == 'ipevse') {
								showSection('#evseconipevse');
								showSection('#llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'extopenwb') {
								showSection('#evseconextopenwb');
							}
							if($('#evsecon').val() == 'owbpro') {
								showSection('#evseconowbpro');
							}
							if($('#evsecon').val() == 'daemon') {
								showSection('#openwbdaemon');
							}
							if($('#evsecon').val() == 'buchse') {
								showSection('#openwbbuchse');
							}
							if($('#evsecon').val() == 'dac') {
								showSection('#evsecondac');
								showSection('#llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'simpleevsewifi') {
								showSection('#evseconswifi');
							}
							if($('#evsecon').val() == 'httpevse') {
								showSection('#evseconhttp');
								showSection('#llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'mqttevse') {
								showSection('#evseconmqtt');
								showSection('#llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'goe') {
								showSection('#evsecongoe');
							}
							if($('#evsecon').val() == 'masterethframer') {
								showSection('#evseconmastereth');
							}
							if($('#evsecon').val() == 'nrgkick') {
								showSection('#evseconnrgkick');
							}
							if($('#evsecon').val() == 'keba') {
								showSection('#evseconkeba');
							}
							if($('#evsecon').val() == 'twcmanager') {
								showSection('#evsecontwcmanager');
							}
							if($('#evsecon').val() == 'ipevse') {
								showSection('#evseconipevse');
							}
						}

						// visibility of meter modules
						function display_llmp1() {
							hideSection('#llmnone');
							hideSection('#llmsdm');
							hideSection('#llmpm3pm');
							hideSection('#llswifi');
							hideSection('#sdm120div');
							hideSection('#rs485lanlp1');
							hideSection('#llmfsm');
							hideSection('#httpll');
							hideSection('#mpm3pmlllp1div');
							hideSection('#mqttll');

							if($('#ladeleistungmodul').val() == 'mpm3pmlllp1') {
								showSection('#mpm3pmlllp1div');
								hideSection('#rs485lanlp1'); // BUG hide/show typo?
							}
							if($('#ladeleistungmodul').val() == 'none') {
								showSection('#llmnone');
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmtripple') {
								showSection('#llmnone');
							}
							if($('#ladeleistungmodul').val() == 'httpll') {
								showSection('#httpll');
							}
							if($('#ladeleistungmodul').val() == 'sdm630modbusll') {
								showSection('#llmsdm');
								showSection('#rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'sdm120modbusll') {
								showSection('#sdm120div');
								showSection('#rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'simpleevsewifi') {
								showSection('#llswifi');
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmll') {
								showSection('#llmpm3pm');
								showSection('#rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'fsm63a3modbusll') {
								showSection('#rs485lanlp1');
								showSection('#llmfsm');
							}
							if($('#ladeleistungmodul').val() == 'mqttll') {
								showSection('#mqttll');
							}
						}

						// visibility of soc modules
						function display_socmodul() {

							hideSection('#socmodullp1');
							hideSection('#socmnone');
							hideSection('#socmhttp');
							hideSection('#socleaf');
							hideSection('#soci3');
							hideSection('#soczoe');
							hideSection('#socevnotify');
							hideSection('#socmtesla');
							hideSection('#soccarnet');
							hideSection('#socmzerong');
							hideSection('#socmeq');
							hideSection('#socaiways');
							hideSection('#socmaudi');
							hideSection('#socmid');
							hideSection('#socmvwid');
							hideSection('#socvag');
							hideSection('#socevcc');
							hideSection('#socmqtt');
							hideSection('#socmkia');
							hideSection('#socmuser');
							hideSection('#socmpass');
							hideSection('#socmyrenault');
							hideSection('#socmypeugeot');
							hideSection('#socmyopel');
							hideSection('#socpsa');
							hideSection('#socmanual');
							hideSection('#soctronity');
							hideSection('#socoldevccwarning');
							hideSection('#socsupportinfo');
							hideSection('#socnosupportinfo');

							if($('#socmodul').val() == 'none') {
								showSection('#socmnone');
							} else {
								showSection('#socmodullp1', false); // do not enable all input child-elements!
								showSection('#stopsocnotpluggedlp1');
							}
							if($('#socmodul').val() == 'soc_volvo') {
								showSection('#socmuser');
								showSection('#socmpass');
							}
							if($('#socmodul').val() == 'soc_mqtt') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3145')
								showSection('#socsupportinfo');
								showSection('#socmqtt');
							}
							if($('#socmodul').val() == 'soc_id') {
								showSection('#socoldevccwarning');
								showSection('#socmid');
							}
							if($('#socmodul').val() == 'soc_vwid') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&p=58178')
								showSection('#socsupportinfo');
								showSection('#socmvwid');
							}
							if($('#socmodul').val() == 'soc_vag') {
								showSection('#socoldevccwarning');
								showSection('#socvag');
							}
							if($('#socmodul').val() == 'soc_evcc') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3134')
								showSection('#socsupportinfo');
								showSection('#socevcc');
							}
							if($('#socmodul').val() == 'soc_kia') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3137')
								showSection('#socsupportinfo');
								showSection('#socmkia');
							}
							if($('#socmodul').val() == 'soc_aiways') {
                                showSection('#socaiways');
                            }
							if($('#socmodul').val() == 'soc_audi') {
								showSection('#socoldevccwarning');
								showSection('#socmaudi');
							}
							if($('#socmodul').val() == 'soc_myrenault') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3139')
								showSection('#socsupportinfo');
								showSection('#socmyrenault');
							}
							if($('#socmodul').val() == 'soc_http') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3143')
								showSection('#socsupportinfo');
								showSection('#socmhttp');
							}
							if($('#socmodul').val() == 'soc_zerong') {
								showSection('#socmzerong');
							}
							if($('#socmodul').val() == 'soc_eq') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3135')
								showSection('#socsupportinfo');
								showSection('#socmeq');
							}
							if($('#socmodul').val() == 'soc_leaf') {
								showSection('#socleaf');
							}
							if($('#socmodul').val() == 'soc_i3') {
								showSection('#soci3');
							}
							if($('#socmodul').val() == 'soc_zoe') {
								showSection('#soczoe');
							}
							if($('#socmodul').val() == 'soc_evnotify') {
								showSection('#socevnotify');
							}
							if($('#socmodul').val() == 'soc_tesla') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3141')
								showSection('#socsupportinfo');
								showSection('#socmtesla');
							}
							if($('#socmodul').val() == 'soc_carnet') {
								showSection('#soccarnet');
							}
							if($('#socmodul').val() == 'soc_mypeugeot') {
								showSection('#socmypeugeot');
							}
							if($('#socmodul').val() == 'soc_myopel') {
								showSection('#socmyopel');
							}
							if($('#socmodul').val() == 'soc_psa') {
								showSection('#socpsa');
							}
							if($('#socmodul').val() == 'soc_manual') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3144')
								showSection('#socsupportinfo');
								showSection('#socmanual');
							}
							if($('#socmodul').val() == 'soc_tronity') {
								$('#socsuportlink').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3142')
								showSection('#socsupportinfo');
								showSection('#soctronity');
							}
						}

						$(function() {
							display_llmp1();
							display_socmodul();
							display_lp1();

							$('#ladeleistungmodul').change(function(){
								display_llmp1();
							});

							$('#evsecon').change(function(){
								display_lp1();
							});

							$('#socmodul').change( function(){
								display_socmodul();
							});
						});
					</script>
				</div>

				<!-- Ladepunkt 2 -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Ladepunkt 2</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagementold == 0) echo " active" ?>">
											<input type="radio" name="lastmanagement" id="lastmanagementOff" value="0"<?php if($lastmanagementold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagementold == 1) echo " active" ?>">
											<input type="radio" name="lastmanagement" id="lastmanagementOn" value="1"<?php if($lastmanagementold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body hide" id="lastmman">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="lp2name" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="lp2name" id="lp2name" value="<?php echo $lp2nameold ?>">
								</div>
							</div>
						</div>
						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="evsecons1" class="col-md-4 col-form-label">Anbindung</label>
							<div class="col">
								<select name="evsecons1" id="evsecons1" class="form-control">
									<optgroup label="openWB">
										<option <?php if($evsecons1old == "modbusevse" && $evseids1old == "1" && $ladeleistungs1modulold == "mpm3pmlls1" && $mpm3pmlls1sourceold == "/dev/ttyUSB1" && $mpm3pmlls1idold == "6" && $evsesources1old == "/dev/ttyUSB1") echo "selected" ?> value="modbusevse" data-id="openwb series1/2 duo v1">Series1/2 Duo 1. Version</option>
										<option <?php if($evsecons1old == "modbusevse" && $evseids1old == "2" && $ladeleistungs1modulold == "mpm3pmlls1" && $mpm3pmlls1sourceold == "/dev/ttyUSB0" && $mpm3pmlls1idold == "106" && $evsesources1old == "/dev/ttyUSB0") echo "selected" ?> value="modbusevse" data-id="openwb series1/2 duo v2">Series1/2 Duo (ab Herbst 2020)</option>
										<option <?php if($evsecons1old == "owbpro") echo "selected" ?> value="owbpro">openWB Pro</option>
										<option <?php if($evsecons1old == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
										<option <?php if($evsecons1old == "daemon") echo "selected" ?> value="daemon">openWB Duo Daemon </option>
										<option <?php if($evsecons1old == "slaveeth") echo "selected" ?> value="slaveeth">Slave</option>
										<option <?php if($evsecons1old == "ipevse") echo "selected" ?> value="ipevse">Satellit</option>
									</optgroup>
									<optgroup label="andere Ladepunkte">
										<option <?php if($evsecons1old == "goe") echo "selected" ?> value="goe">Go-e</option>
										<option <?php if($evsecons1old == "keba") echo "selected" ?> value="keba">Keba</option>
										<option <?php if($evsecons1old == "nrgkick") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
										<option <?php if($evsecons1old == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
										<option <?php if($evsecons1old == "twcmanager") echo "selected" ?> value="twcmanager">Tesla TWC mit TWCManager</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($evsecons1old == "dac") echo "selected" ?> value="dac">DAC</option>
										<option <?php if($evsecons1old == "modbusevse" && !($evseids1old == "1" && $ladeleistungs1modulold == "mpm3pmlls1" && $mpm3pmlls1sourceold == "/dev/ttyUSB1" && $mpm3pmlls1idold == "6" && $evsesources1old == "/dev/ttyUSB1") && !($evseids1old == "2" && $ladeleistungs1modulold == "mpm3pmlls1" && $mpm3pmlls1sourceold == "/dev/ttyUSB0" && $mpm3pmlls1idold == "106" && $evsesources1old == "/dev/ttyUSB0") ) echo "selected" ?> value="modbusevse">Modbus</option>
										<option <?php if($evsecons1old == "mqttevse") echo "selected" ?> value="mqttevse">MQTT</option>
									</optgroup>
								</select>
							</div>
						</div>
						<div id="evseconextopenwblp2" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="extopenwblp2">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="chargep2ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep2ip" id="chargep2ip" value="<?php echo $chargep2ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="chargep2cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="2" step="1" name="chargep2cp" id="chargep2cp" value="<?php echo $chargep2cpold ?>">
										<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconowbprolp2" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="owbprolp2">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="owbpro2ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="owbpro2ip" id="owbpro2ip" value="<?php echo $owbpro2ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="evsecondaemonlp2" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="lldaemonlp2">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option für eine fertige openWB Duo und bietet eine optimale und schnelle Auslesung.
							</div>
						</div>
						<div id="evseconipevselp2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evseiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp2" id="evseiplp2" value="<?php echo $evseiplp2old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Aufgedruckt auf dem Label der openWB.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseidlp2" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp2" id="evseidlp2" value="<?php echo $evseidlp2old ?>">
										<span class="form-text small">Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="openwb12s1v1" class="hide">
							<input type="hidden" name="evseids1" value="1">
							<input type="hidden" name="ladeleistungs1modul" value="mpm3pmlls1">
							<input type="hidden" name="mpm3pmlls1source" value="/dev/ttyUSB1">
							<input type="hidden" name="mpm3pmlls1id" value="6">
							<input type="hidden" name="evsesources1" value="/dev/ttyUSB1">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option sowohl für den Bausatz als auch für fertige openWB series1 oder series2.
							</div>
						</div>
						<div id="openwb12s1v2" class="hide">
							<input type="hidden" name="evseids1" value="2">
							<input type="hidden" name="ladeleistungs1modul" value="mpm3pmlls1">
							<input type="hidden" name="mpm3pmlls1source" value="/dev/ttyUSB0">
							<input type="hidden" name="mpm3pmlls1id" value="106">
							<input type="hidden" name="evsesources1" value="/dev/ttyUSB0">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option sowohl für den Bausatz als auch für fertige openWB series1 oder series2, wenn Sie diese ab Herbst 2020 erworben haben.
							</div>
						</div>
						<div id="evseconnrgkicks1" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="nrgkicklp2">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="nrgkickiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="nrgkickiplp2" id="nrgkickiplp2" value="<?php echo $nrgkickiplp2old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Zu finden in der NRGKick App unter Einstellungen -> Info -> NRGkick Connect Infos.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkicktimeoutlp2" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="nrgkicktimeoutlp2" id="nrgkicktimeoutlp2" value="<?php echo $nrgkicktimeoutlp2old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des NRGKick Connect gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der NRGKick z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickmaclp2" class="col-md-4 col-form-label">MAC Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$" name="nrgkickmaclp2" id="nrgkickmaclp2" value="<?php echo $nrgkickmaclp2old ?>">
										<span class="form-text small">
											Gültige Werte MAC Adresse im Format: 11:22:33:AA:BB:CC<br>
											Zu finden In der NRGKick App unter Einstellungen -> BLE-Mac.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nrgkickpwlp2" class="col-md-4 col-form-label">Password</label>
									<div class="col">
										<input class="form-control" type="password" name="nrgkickpwlp2" id="nrgkickpwlp2" value="<?php echo $nrgkickpwlp2old ?>">
										<span class="form-text small">
											Password, welches in der NRGKick App festgelegt wurde.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconkebas1" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="keballlp2">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="kebaiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="kebaiplp2" id="kebaiplp2" value="<?php echo $kebaiplp2old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Erforder eine Keba C- oder X- Series. Die Smart Home Funktion (UDP Schnittstelle) muss per DIP Switch in der Keba aktiviert sein!
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmbs1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsesources1" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="evsesources1" id="evsesources1" value="<?php echo $evsesources1old ?>">
										<span class="form-text small">Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseids1" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseids1" id="evseids1" value="<?php echo $evseids1old ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evselanips1" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evselanips1" id="evselanips1" value="<?php echo $evselanips1old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecondacs1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="dacregisters1" class="col-md-4 col-form-label">Dacregister</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="99" step="1" name="dacregisters1" id="dacregisters1" value="<?php echo $dacregisters1old ?>">
										<span class="form-text small">
											Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP.
											Der benötigte Wert sollte <a href="/openWB/ramdisk/i2csearch">HIER</a> zu finden sein.
											Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmqtts1" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu lesen:<br>
								<span class="text-info">openWB/lp/2/AConfigured</span> Stromvorgabe in A<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/lp/2/plugStat</span> Status, ob ein Fahrzeug angesteckt ist, nur 0 (nein) oder 1 (ja)<br>
								<span class="text-info">openWB/set/lp/2/chargeStat</span> Status, ob gerade geladen wird, nur 0 (nein) oder 1 (ja)
							</div>
						</div>
						<div id="evsecontwcmanagers1" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="twcmanagerlp2">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col-md-4">
										HTTPControl / Ngardiner Fork
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($twcmanagerlp2httpcontrolold == 0) echo " active" ?>">
											<input type="radio" name="twcmanagerlp2httpcontrol" id="twcmanagerlp2httpcontrolOff" value="0"<?php if($twcmanagerlp2httpcontrolold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($twcmanagerlp2httpcontrolold == 1) echo " active" ?>">
											<input type="radio" name="twcmanagerlp2httpcontrol" id="twcmanagerlp2httpcontrolOn" value="1"<?php if($twcmanagerlp2httpcontrolold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="twcmanagerlp2ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="twcmanagerlp2ip" id="twcmanagerlp2ip" value="<?php echo $twcmanagerlp2ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1 input-port">
									<label for="twcmanagerlp2port" class="col-md-4 col-form-label">Port</label>
									<div class="col">
										<input class="form-control" type="number" min="80" max="10000" step="1" name="twcmanagerlp2port" id="twcmanagerlp2port" value="<?php echo $twcmanagerlp2portold ?>">
										<span class="form-text small">Port des HTTP Control Interface. Standard: 8080</span>
									</div>
								</div>
								<div class="form-row mb-1 input-phases">
									<label for="twcmanagerlp2phasen" class="col-md-4 col-form-label">Anzahl Phasen</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="3" step="1" name="twcmanagerlp2phasen" id="twcmanagerlp2phasen" value="<?php echo $twcmanagerlp2phasenold ?>">
										<span class="form-text small">Definiert die genutzte Anzahl der Phasen zur korrekten Errechnung der Ladeleistung (BETA).</span>
									</div>
								</div>
							</div>
						</div>
						<script>
							$(function() {
								function visibility_twcmanagerlp2_connection() {
									if($('#twcmanagerlp2httpcontrolOff').prop("checked")) {
										hideSection('#evsecontwcmanagers1 .input-port');
										showSection('#evsecontwcmanagers1 .input-phases');
									} else {
										showSection('#evsecontwcmanagers1 .input-port');
										hideSection('#evsecontwcmanagers1 .input-phases');
									}
								}

								$('input[type=radio][name=twcmanagerlp2httpcontrol]').change(function(){
									visibility_twcmanagerlp2_connection();
								});

								visibility_twcmanagerlp2_connection();
							});
						</script>
						<div id="evsecoslaveeth" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="mpm3pmethll">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="evseconswifis1" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="simpleevsewifis1">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsewifiiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evsewifiiplp2" id="evsewifiiplp2" value="<?php echo $evsewifiiplp2old ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evsewifitimeoutlp2" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="evsewifitimeoutlp2" id="evsewifitimeoutlp2" value="<?php echo $evsewifitimeoutlp2old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecongoes1" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="goelp2">
							<div class="form-group">
								<div class="alert alert-info">
									Seit Firmware Version 0.40 wird PV-Laden besser unterstützt. 
									<span class="text-danger">
										Bitte halten Sie die go-e Firmware auf einem aktuellen Stand.
									</span>
								</div>
								<div class="form-row mb-1">
									<label for="goeiplp2" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="goeiplp2" id="goeiplp2" value="<?php echo $goeiplp2old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="goetimeoutlp2" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="goetimeoutlp2" id="goetimeoutlp2" value="<?php echo $goetimeoutlp2old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="llmodullp2" class="hide">
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="ladeleistungs1modul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungs1modul" id="ladeleistungs1modul" class="form-control">
										<optgroup label="openWB">
											<option <?php if($ladeleistungs1modulold == "mpm3pmlllp2") echo "selected" ?> value="mpm3pmlllp2">openWB Satelit</option>
											<option <?php if($ladeleistungs1modulold == "mpm3pmtripplelp2") echo "selected" ?> value="mpm3pmtripplelp2">openWB Tripple</option>
										</optgroup>
										<optgroup label="andere Messgeräte">
											<option <?php if($ladeleistungs1modulold == "goelp2") echo "selected" ?> value="goelp2">Go-e</option>
											<option <?php if($ladeleistungs1modulold == "mpm3pmlls1") echo "selected" ?> value="mpm3pmlls1">MPM3PM Modbus</option>
											<option <?php if($ladeleistungs1modulold == "sdm120modbuslls1") echo "selected" ?> value="sdm120modbuslls1">SDM 120 Modbus</option>
											<option <?php if($ladeleistungs1modulold == "sdm630modbuslls1") echo "selected" ?> value="sdm630modbuslls1">SDM 630 Modbus</option>
											<option <?php if($ladeleistungs1modulold == "simpleevsewifis1") echo "selected" ?> value="simpleevsewifis1">Simple EVSE Wifi</option>
										</optgroup>
										<optgroup label="generische Module">
											<option <?php if($ladeleistungs1modulold == "mqttlllp2") echo "selected" ?> value="mqttlllp2">MQTT</option>
										</optgroup>
									</select>
								</div>
							</div>
							<div id="mqttlllp2div" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/2/W</span> Ladeleistung in Watt, int, positiv<br>
									<span class="text-info">openWB/set/lp/2/kWhCounter</span> Zählerstand in kWh, float, Punkt als Trenner, nur positiv<br>
									Optional zusätzlich:<br>
									<span class="text-info">openWB/set/lp/2/VPhase1</span> Spannung Phase 1, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/2/VPhase2</span> Spannung Phase 2, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/2/VPhase3</span> Spannung Phase 3, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/2/APhase1</span> Strom Phase 1, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/2/APhase2</span> Strom Phase 2, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/2/APhase3</span> Strom Phase 3, float, Punkt als Trenner, nur positiv
								</div>
							</div>
							<div id="mpm3pmlllp2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpmlp2ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp2ip" id="mpmlp2ip" value="<?php echo $mpmlp2ipold ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse des Modbus Ethernet Konverters im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp2id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp2id" id="mpmlp2id" value="<?php echo $mpmlp2idold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="mpm3pmlls1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpm3pmlls1source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="mpm3pmlls1source" id="mpm3pmlls1source" value="<?php echo $mpm3pmlls1sourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das MPM3PM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpm3pmlls1id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmlls1id" id="mpm3pmlls1id" value="<?php echo $mpm3pmlls1idold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="swifis1div" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="sdm630s1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630lp2source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm630lp2source" id="sdm630lp2source" value="<?php echo $sdm630lp2sourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdmids1" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdmids1" id="sdmids1" value="<?php echo $sdmids1old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="sdm120s1div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm120lp2source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm120lp2source" id="sdm120lp2source" value="<?php echo $sdm120lp2sourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid1s1" class="col-md-4 col-form-label">ID Phase 1</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid1s1" id="sdm120modbusllid1s1" value="<?php echo $sdm120modbusllid1s1old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der ersten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid2s1" class="col-md-4 col-form-label">ID Phase 2</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid2s1" id="sdm120modbusllid2s1" value="<?php echo $sdm120modbusllid2s1old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase. Wenn nicht vorhanden 254 eintragen.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3s1" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3s1" id="sdm120modbusllid3s1" value="<?php echo $sdm120modbusllid3s1old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase. Wenn nicht vorhanden 254 eintragen.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="rs485lanlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="lllaniplp2" class="col-md-4 col-form-label">IP Adresse RS485/Lan-Konverter</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lllaniplp2" id="lllaniplp2" value="<?php echo $lllaniplp2old ?>">
											<span class="form-text small">
												Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
												Gültige Werte IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>

						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="socmodul1" class="col-md-4 col-form-label">SOC Modul</label>
							<div class="col">
								<select name="socmodul1" id="socmodul1" class="form-control">
									<option <?php if($socmodul1old == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<optgroup label="universelle Module">
										<option <?php if($socmodul1old == "soc_evcclp2") echo "selected" ?> value="soc_evcclp2">EVCC</option>
										<option <?php if($socmodul1old == "soc_evnotifys1") echo "selected" ?> value="soc_evnotifys1">EVNotify</option>
										<option <?php if($socmodul1old == "soc_http1") echo "selected" ?> value="soc_http1">HTTP</option>
										<option <?php if($socmodul1old == "soc_manuallp2") echo "selected" ?> value="soc_manuallp2">Manuell + Berechnung</option>
										<option <?php if($socmodul1old == "soc_mqtt") echo "selected" ?> value="soc_mqtt">MQTT</option>
										<option <?php if($socmodul1old == "soc_tronitylp2") echo "selected" ?> value="soc_tronitylp2">Tronity</option>
									</optgroup>
									<optgroup label="Fahrzeughersteller">
										<option <?php if($socmodul1old == "soc_aiwayslp2") echo "selected" ?> value="soc_aiwayslp2">Aiways</option>
										<option <?php if($socmodul1old == "soc_audilp2") echo "selected" ?> value="soc_audilp2">Audi</option>
										<option <?php if($socmodul1old == "soc_i3s1") echo "selected" ?> value="soc_i3s1">BMW &amp; Mini</option>
										<option <?php if($socmodul1old == "soc_kialp2") echo "selected" ?> value="soc_kialp2">Kia / Hyundai</option>
										<option <?php if($socmodul1old == "soc_eqlp2") echo "selected" ?> value="soc_eqlp2">Mercedes EQ</option>
										<option <?php if($socmodul1old == "soc_myopellp2") echo "selected" ?> value="soc_myopellp2">MyOpel</option>
										<option <?php if($socmodul1old == "soc_mypeugeotlp2") echo "selected" ?> value="soc_mypeugeotlp2">MyPeugeot</option>
										<option <?php if($socmodul1old == "soc_myrenaultlp2") echo "selected" ?> value="soc_myrenaultlp2">MyRenault</option>
										<option <?php if($socmodul1old == "soc_leafs1") echo "selected" ?> value="soc_leafs1">Nissan Leaf</option>
										<option <?php if($socmodul1old == "soc_psalp2") echo "selected" ?> value="soc_psalp2">PSA (Peugeot/Citroen/DS/Opel/Vauxhall)</option>
										<option <?php if($socmodul1old == "soc_zoelp2") echo "selected" ?> value="soc_zoelp2">Renault Zoe alt</option>
										<option <?php if($socmodul1old == "soc_teslalp2") echo "selected" ?> value="soc_teslalp2">Tesla</option>
										<option <?php if($socmodul1old == "soc_vaglp2") echo "selected" ?> value="soc_vaglp2">VAG</option>
										<option <?php if($socmodul1old == "soc_volvolp2") echo "selected" ?> value="soc_volvolp2">Volvo</option>
										<option <?php if($socmodul1old == "soc_carnetlp2") echo "selected" ?> value="soc_carnetlp2">VW Carnet</option>
										<option <?php if($socmodul1old == "soc_idlp2") echo "selected" ?> value="soc_idlp2">VW ID-alt</option>
										<option <?php if($socmodul1old == "soc_vwidlp2") echo "selected" ?> value="soc_vwidlp2">VW ID</option>
										<option <?php if($socmodul1old == "soc_zeronglp2") echo "selected" ?> value="soc_zeronglp2">Zero NG</option>
									</optgroup>
								</select>
								<div id="socoldevccwarninglp2" class="mt-1 alert alert-danger hide">
									Dieses Modul nutzt eine nicht mehr unterstützte Version von EVCC-SOC und wird nicht weiter gepflegt.
								</div>
								<div id="socsupportinfolp2" class="mt-1 alert alert-success hide">
									Support für dieses Modul gibt es im <a id="socsuportlinklp2" href="#" target="_blank" rel="noopener noreferrer">openWB Forum</a>.
								</div>
								<div id="socnosupportinfolp2" class="mt-1 alert alert-warning hide">
									Dieses Modul wird nicht aktiv gepflegt.
								</div>
							</div>
						</div>
						<div id="socmodullp2" class="hide">
							<!-- soc is always requested, ignoring plug stat -->
							<div id="socmnone1" class="hide">
								<!-- nothing here -->
							</div>
							<div id="socmtype2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Fahrzeugtyp</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($soc2typeold == 'vw') echo " active" ?>">
													<input type="radio" name="soc2type" id="soc2type_vw" value="vw"<?php if($soc2typeold == 'vw') echo " checked=\"checked\"" ?>>VW
												</label>
												<label class="btn btn-outline-info<?php if($soc2typeold == 'id') echo " active" ?>">
													<input type="radio" name="soc2type" id="soc2type_id" value="id"<?php if($soc2typeold == 'id') echo " checked=\"checked\"" ?>>ID
												</label>
												<label class="btn btn-outline-info<?php if($soc2typeold == 'porsche') echo " active" ?>">
													<input type="radio" name="soc2type" id="soc2type_porsche" value="porsche"<?php if($soc2typeold == 'porsche') echo " checked=\"checked\"" ?>>Porsche
												</label>
											</div>
											<span class="form-text small">Auswahl Fahrzeugtyp</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmvwidinfolp2" class="mt-1 alert alert-info hide">
								Für VW Fahrzeuge. Es wird benötigt:<br>
								- We Connect (ID) Account aktiv<br>
								- We Connect ID App eingerichtet - auch für nicht-ID!<br>
							</div>
							<div id="socmuser2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2user" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="soc2user" id="soc2user" value="<?php echo $soc2userold ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="socmpass2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2pass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc2pass" id="soc2pass" value="<?php echo $soc2passold ?>">
										</div>
									</div>
								</div>
							</div>
							<div id="socmanuallp2" class="hide">
								<div class="alert alert-info">
									Beim Anstecken des Fahrzeugs muss der aktuelle SoC (am Display oder über einen Browser) angegeben werden.
									Anhand des Zählers im Ladepunkt wird dann der aktuelle SoC errechnet. Ausschlaggebend für die Qualität dieses Moduls sind die beiden Einstellungen "Akkugröße" und "Wirkungsgrad".<br>
								</div>
								<div class="form-row mb-1">
									<label for="akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="akkuglp2" value="<?php echo $akkuglp2old ?>">
										<span class="form-text small">
											Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
											Die Netto-Kapazität unterscheidet sich meist von den Angaben der Fahrzeughersteller. So besitzt ein Tesla Model S 90 z. B. nur ca. 83kWh und nicht die durch die Typenbezeichnung suggerierten 90kWh.
											Andere Hersteller begrenzen die nutzbare Kapazität absichtlich, um eine höhere Lebensdauer der Akkus zu erreichen. Gängig sind eine Drosselung auf 90% der angegebenen Brutto-Kapazität.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="wirkungsgradlp2" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp2" id="wirkungsgradlp2" value="<?php echo $wirkungsgradlp2old ?>">
										<span class="form-text small">
											Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
											Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
											Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
											Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
											SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
											SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
										</span>
									</div>
								</div>
							</div>
							<div id="socmqtt1" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/2/%Soc</span> Ladezustand in %, int, 0-100
								</div>
							</div>
							<div id="socmzeronglp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_zeronglp2_username" id="soc_zeronglp2_username" value="<?php echo $soc_zeronglp2_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Zero Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_zeronglp2_password" id="soc_zeronglp2_password" value="<?php echo $soc_zeronglp2_passwordold ?>">
											<span class="form-text small">
												Password des Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zeronglp2_intervall" id="soc_zeronglp2_intervall" value="<?php echo $soc_zeronglp2_intervallold ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_zeronglp2_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_zeronglp2_intervallladen" id="soc_zeronglp2_intervallladen" value="<?php echo $soc_zeronglp2_intervallladenold ?>">
											<span class="form-text small">
												Wie oft die Zero abgefragt wird während geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmteslalp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_teslalp2_username" class="col-md-4 col-form-label">E-Mail</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_teslalp2_username" id="soc_teslalp2_username" value="<?php echo $soc_teslalp2_usernameold ?>">
											<span class="form-text small">
												Email Adresse des Tesla Logins.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tesla_login_btn" class="col-md-4 col-form-label">Anmeldedaten prüfen</label>
										<div class="col">
											<button type="button" class="btn btn-success soc-tesla-login-btn" data-email="#soc_teslalp2_username" value="2">Bei Tesla anmelden</button>
											<button type="button" class="btn btn-danger soc-tesla-clear-btn" value="2">Anmeldedaten entfernen</button>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_teslalp2_carnumber" class="col-md-4 col-form-label">Auto im Account</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_teslalp2_carnumber" id="soc_teslalp2_carnumber" value="<?php echo $soc_teslalp2_carnumberold ?>">
											<span class="form-text small">
												Im Normalfall hier 0 eintragen. Sind mehrere Teslas im Account für den zweiten Tesla eine 1 eintragen.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_teslalp2_intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_teslalp2_intervall" id="soc_teslalp2_intervall" value="<?php echo $soc_teslalp2_intervallold ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos abgefragt werden soll, wenn nicht geladen wird.<br>
												Damit das Auto in den Standby gehen kann und die Energieverluste gering bleiben, sollte das Intervall mindestens eine Stunde ("60") betragen, besser 12 Stunden ("720") oder mehr.<br>
												Zu Beginn einer Ladung wird das Auto immer geweckt, um den aktuellen SoC zu erhalten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_teslalp2_intervallladen" class="col-md-4 col-form-label">Abfrageintervall Laden</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="soc_teslalp2_intervallladen" id="soc_teslalp2_intervallladen" value="<?php echo $soc_teslalp2_intervallladenold ?>">
											<span class="form-text small">
												Gibt an, in welchem Intervall (in Minuten bei normaler Regelgeschwindigkeit) der Ladestand des Autos während des Ladens abgefragt werden soll.<br>
												Je nach Ladeleistung werden 5 - 10 Minuten empfohlen, damit eventuell eingestellte SoC-Grenzen rechtzeitig erkannt werden können.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socaiwayslp2" class="hide">
                                <div class="form-group">
                                    <div class="form-row mb-1">
                                        <label for="soc_aiwayslp2_user" class="col-md-4 col-form-label">Account</label>
                                        <div class="col">
                                            <input class="form-control" type="text" name="soc_aiwayslp2_user" id="soc_aiwayslp2_user" value="<?php echo $soc_aiwayslp2_userold ?>">
                                            <span class="form-text small">
                                                Aiways Account Name (nicht die E-Mail-Adresse)
                                            </span>
                                        </div>
                                    </div>
									<div class="form-row mb-1">
										<label for="soc_aiwayslp2_pass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_aiwayslp2_pass" id="soc_aiwayslp2_pass" value="<?php echo $soc_aiwayslp2_passold ?>">
											<span class="form-text small">
												Aiways Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_aiwayslp2_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_aiwayslp2_vin" id="soc_aiwayslp2_vin" value="<?php echo $soc_aiwayslp2_vinold ?>">
											<span class="form-text small">
												VIN des Fahrzeugs
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_aiwayslp2_intervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_aiwayslp2_intervall" id="soc_aiwayslp2_intervall" value="<?php echo $soc_aiwayslp2_intervallold ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
                            </div>
							<div id="soccarnetlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="carnetlp2user" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="carnetlp2user" id="carnetlp2user" value="<?php echo $carnetlp2userold ?>">
											<span class="form-text small">
												VW Carnet Benutzername. Wenn der SoC nicht korrekt angezeigt wird, z.B. weil AGB von VW geändert wurden, ist es nötig sich auf https://www.portal.volkswagen-we.com anzumelden.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="carnetlp2pass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="carnetlp2pass" id="carnetlp2pass" value="<?php echo $carnetlp2passold ?>">
											<span class="form-text small">
												VW Carnet Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soccarnetlp2intervall" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soccarnetlp2intervall" id="soccarnetlp2intervall" value="<?php echo $soccarnetlp2intervallold ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soczoelp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="zoelp2username" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="zoelp2username" id="zoelp2username" value="<?php echo $zoelp2usernameold ?>">
											<span class="form-text small">
												Renault Zoe Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="zoelp2passwort" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="zoelp2passwort" id="zoelp2passwort" value="<?php echo $zoelp2passwortold ?>">
											<span class="form-text small">
											Renault Zoe Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupzoelp2old == 0) echo " active" ?>">
													<input type="radio" name="wakeupzoelp2" id="wakeupzoelp2Off" value="0"<?php if($wakeupzoelp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupzoelp2old == 1) echo " active" ?>">
													<input type="radio" name="wakeupzoelp2" id="wakeupzoelp2On" value="1"<?php if($wakeupzoelp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmyrenaultlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="myrenault_userlp2" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_userlp2" id="myrenault_userlp2" value="<?php echo $myrenault_userlp2old ?>">
											<span class="form-text small">
												MyRenault Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_passlp2" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="myrenault_passlp2" id="myrenault_passlp2" value="<?php echo $myrenault_passlp2old ?>">
											<span class="form-text small">
												MyRenault Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_locationlp2" class="col-md-4 col-form-label">Standort</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_locationlp2" id="myrenault_locationlp2" value="<?php echo $myrenault_locationlp2old ?>">
											<span class="form-text small">
												MyRenault Standort, z.B. de_DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myrenault_countrylp2" class="col-md-4 col-form-label">Land</label>
										<div class="col">
											<input class="form-control" type="text" name="myrenault_countrylp2" id="myrenault_countrylp2" value="<?php echo $myrenault_countrylp2old ?>">
											<span class="form-text small">
												MyRenault Land, z.B. CH, AT, DE
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soclp2_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soclp2_vin" id="soclp2_vin" value="<?php echo $soclp2_vinold ?>">
											<span class="form-text small">
												VIN des Autos. Ist nur nötig wenn es sich um ein Importfahrzeug handelt. Kann auf none belassen werden wenn die Auslesung funktioniert.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label">Zoe Remote wecken wenn sie eingeschlafen ist</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp2old == 0) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp2" id="wakeupmyrenaultlp2Off" value="0"<?php if($wakeupmyrenaultlp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($wakeupmyrenaultlp2old == 1) echo " active" ?>">
													<input type="radio" name="wakeupmyrenaultlp2" id="wakeupmyrenaultlp2On" value="1"<?php if($wakeupmyrenaultlp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Erfordert einen openWB Ladepunkt, Go-e oder Keba. Nicht kompatibel mit EVSE Wifi und SimpleEVSE WB (mit DAC).
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socevnotifylp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="evnotifyakeylp2" class="col-md-4 col-form-label">Akey</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifyakeylp2" id="evnotifyakeylp2" value="<?php echo $evnotifyakeylp2old ?>">
											<span class="form-text small">
												Akey des EVNotify Kontos
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="evnotifytokenlp2" class="col-md-4 col-form-label">Token</label>
										<div class="col">
											<input class="form-control" type="text" name="evnotifytokenlp2" id="evnotifytokenlp2" value="<?php echo $evnotifytokenlp2old ?>">
											<span class="form-text small">
												Token des Kontos
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmhttp1" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="hsocip1" class="col-md-4 col-form-label">Abfrage URL</label>
										<div class="col">
											<input class="form-control" type="text" name="hsocip1" id="hsocip1" value="<?php echo htmlspecialchars($hsocip1old) ?>">
											<span class="form-text small">
												Gültige Werte none, "url". URL für die Abfrage des Soc, Antwort muss der reine Zahlenwert sein.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socleaf1" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="leafusernames1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="leafusernames1" id="leafusernames1" value="<?php echo $leafusernames1old ?>">
											<span class="form-text small">
												Nissan Connect Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="leafpassworts1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="leafpassworts1" id="leafpassworts1" value="<?php echo $leafpassworts1old ?>">
											<span class="form-text small">
												Nissan Connect Passwort
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="soci31" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="i3usernames1" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="i3usernames1" id="i3usernames1" value="<?php echo $i3usernames1old ?>">
											<span class="form-text small">
												BMW Services Benutzername
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3passworts1" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="i3passworts1" id="i3passworts1" value="<?php echo $i3passworts1old ?>">
											<span class="form-text small">
												BMW Services Passwort
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="i3vins1" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="i3vins1" id="i3vins1" value="<?php echo $i3vins1old ?>">
											<span class="form-text small">
												BMW VIN. Sie ist in voller Länge anzugeben.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soci3intervall1" class="col-md-4 col-form-label">Verkürztes Intervall beim Laden</label>
										<div class="col">
											<input class="form-control" type="text" name="soci3intervall1" id="soci3intervall1" value="<?php echo $soci3intervall1old ?>">
											<span class="form-text small">
												Verkürzt das Abfrageintervall beim Laden auf xx Minuten
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmpin2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2pin" class="col-md-4 col-form-label">Pin</label>
										<div class="col">
											<input class="form-control" type="password" name="soc2pin" id="soc2pin" value="<?php echo $soc2pinold ?>">
											<span class="form-text small">
												PIN des Accounts.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmvin2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc2vin" id="soc2vin" value="<?php echo $soc2vinold ?>">
											<span class="form-text small">
												Vollständige VIN des Fahrzeugs
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmypeugeotlp2" class="hide">
								<div class="form-group">
									<div class="card-text alert alert-info">
										Die notwendige <a href="https://developer.groupe-psa.io/webapi/b2c/quickstart/connect/#connect-your-app" target="_blank" rel="noopener noreferrer">API</a> ist derzeit von PSA noch nicht freigegeben, daher funktionieren über den dokumentierten Weg erstellte Client-IDs und Client-Secrets leider noch nicht.<br>
										Auf eigenes Risiko kann diese Anleitung genutzt werden, dies hat bisher zu guten Ergebnissen geführt und wird durch die openWB Community (nicht openWB selbst) gepflegt. <a href="https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden" target="_blank" rel="noopener noreferrer">https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden</a><br> 
										Weitere Diskussion zu diesem Thema findet sich <a href="https://openwb.de/forum/viewtopic.php?f=5&t=1206" target="_blank" rel="noopener noreferrer">im Forum.</a>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_userlp2" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="mypeugeot_userlp2" id="mypeugeot_userlp2" value="<?php echo $mypeugeot_userlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_passlp2" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="mypeugeot_passlp2" id="mypeugeot_passlp2" value="<?php echo $mypeugeot_passlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_clientidlp2" class="col-md-4 col-form-label">Client-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="mypeugeot_clientidlp2" id="mypeugeot_clientidlp2" value="<?php echo $mypeugeot_clientidlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mypeugeot_clientsecretlp2" class="col-md-4 col-form-label">Client-Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="mypeugeot_clientsecretlp2" id="mypeugeot_clientsecretlp2" value="<?php echo $mypeugeot_clientsecretlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere Peugeot SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($mypeugeot_soccalclp2old == 0) echo " active" ?>">
													<input type="radio" name="mypeugeot_soccalclp2" id="mypeugeot_soccalclp2Off" value="0"<?php if($mypeugeot_soccalclp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($mypeugeot_soccalclp2old == 1) echo " active" ?>">
													<input type="radio" name="mypeugeot_soccalclp2" id="mypeugeot_soccalclp2On" value="1"<?php if($mypeugeot_soccalclp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Aktuell liefert die Peugeot API keine SoC Aktualisierung während des Ladevorgangs.<br>
												Wenn Ja gewählt wird, wird der SoC vor dem Laden über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet. Dies erlaubt eine SoC-gesteuerte Ladung.<br>
												Bei Nein wird immer der SoC über die API abgefragt. SoC gesteuerte Ladung ist erst möglich nachdem PSA den SoC auch während des Ladens übermittelt.
											</span>
										</div>
										<div id="peugeotmanualcalclp2div" class="hide">
											<div class="form-row mb-1">
												<label for="peugeot_akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="peugeot_akkuglp2" value="<?php echo $akkuglp2old ?>">
													<span class="form-text small">
														Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
														Für Peugeot e208 und e2008: 46kWh
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="peugeot_wirkungsgradlp2" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp2" id="peugeot_wirkungsgradlp2" value="<?php echo $wirkungsgradlp2old ?>">
													<span class="form-text small">
														Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
														Für Peugeot e208 und e2008: 94-96 Prozent
														Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
														Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
														Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
														SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
														SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<script>
								$(function() {
									function visibility_mypeugeot_soccalclp2() {
										if($('#mypeugeot_soccalclp2Off').prop("checked")) {
											hideSection('#peugeotmanualcalclp2div');
										} else {
											showSection('#peugeotmanualcalclp2div');
										}
									}

									$('input[type=radio][name=mypeugeot_soccalclp2]').change(function(){
										visibility_mypeugeot_soccalclp2();
									});

									visibility_mypeugeot_soccalclp2();
								});
								</script>
							</div>
							<div id="socmyopellp2" class="hide">
								<div class="form-group">
									<div class="card-text alert alert-info">
										Die notwendige <a href="https://developer.groupe-psa.io/webapi/b2c/quickstart/connect/#connect-your-app" target="_blank" rel="noopener noreferrer">API</a> ist derzeit von PSA noch nicht freigegeben, daher funktionieren über den dokumentierten Weg erstellte Client-IDs und Client-Secrets leider noch nicht.<br>
										Auf eigenes Risiko kann diese Anleitung genutzt werden, dies hat bisher zu guten Ergebnissen geführt und wird durch die openWB Community (nicht openWB selbst) gepflegt. <a href="https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden" target="_blank" rel="noopener noreferrer">https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden</a><br> 
										Weitere Diskussion zu diesem Thema findet sich <a href="https://openwb.de/forum/viewtopic.php?f=5&t=1206" target="_blank" rel="noopener noreferrer">im Forum.</a>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_userlp2" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="myopel_userlp2" id="myopel_userlp2" value="<?php echo $myopel_userlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_passlp2" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="myopel_passlp2" id="myopel_passlp2" value="<?php echo $myopel_passlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_clientidlp2" class="col-md-4 col-form-label">Client-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="myopel_clientidlp2" id="myopel_clientidlp2" value="<?php echo $myopel_clientidlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="myopel_clientsecretlp2" class="col-md-4 col-form-label">Client-Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="myopel_clientsecretlp2" id="myopel_clientsecretlp2" value="<?php echo $myopel_clientsecretlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere MyOpel SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($myopel_soccalclp2old == 0) echo " active" ?>">
													<input type="radio" name="myopel_soccalclp2" id="myopel_soccalclp2Off" value="0"<?php if($myopel_soccalclp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($myopel_soccalclp2old == 1) echo " active" ?>">
													<input type="radio" name="myopel_soccalclp2" id="myopel_soccalclp2On" value="1"<?php if($myopel_soccalclp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Aktuell liefert die Opel API keine SoC Aktualisierung während des Ladevorgangs.<br>
												Wenn Ja gewählt wird, wird der SoC vor dem Laden über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet. Dies erlaubt eine SoC-gesteuerte Ladung.<br>
												Bei Nein wird immer der SoC über die API abgefragt. SoC gesteuerte Ladung ist erst möglich nachdem Opel/PSA den SoC auch während des Ladens übermittelt.
											</span>
										</div>
										<div id="opelmanualcalclp2div" class="hide">
											<div class="form-row mb-1">
												<label for="opel_akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="opel_akkuglp2" value="<?php echo $akkuglp2old ?>">
													<span class="form-text small">
														Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
														Für Corsa-e: 46kWh
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="opel_wirkungsgradlp2" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp2" id="opel_wirkungsgradlp2" value="<?php echo $wirkungsgradlp2old ?>">
													<span class="form-text small">
														Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
														Für Corsa-e: 94-96 Prozent<br>
														Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
														Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
														Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
														SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
														SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<script>
								$(function() {
									function visibility_myopel_soccalclp2() {
										if($('#myopel_soccalclp2Off').prop("checked")) {
											hideSection('#opelmanualcalclp2div');
										} else {
											showSection('#opelmanualcalclp2div');
										}
									}

									$('input[type=radio][name=myopel_soccalclp2]').change(function(){
										visibility_myopel_soccalclp2();
									});

									visibility_myopel_soccalclp2();
								});
								</script>
							</div>
							<div id="socpsalp2" class="hide">
								<div class="form-group">
									<div class="card-text alert alert-info">
										Die notwendige <a href="https://developer.groupe-psa.io/webapi/b2c/quickstart/connect/#connect-your-app" target="_blank" rel="noopener noreferrer">API</a> ist derzeit von PSA noch nicht freigegeben, daher funktionieren über den dokumentierten Weg erstellte Client-IDs und Client-Secrets leider noch nicht.<br>
										Auf eigenes Risiko kann diese Anleitung genutzt werden, dies hat bisher zu guten Ergebnissen geführt und wird durch die openWB Community (nicht openWB selbst) gepflegt. <a href="https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden" target="_blank" rel="noopener noreferrer">https://github.com/snaptec/openWB/wiki/Fahrzeugspezifische-Konfigurationen#welches-soc-modul-kann-verwendet-werden</a><br> 
										Weitere Diskussion zu diesem Thema findet sich <a href="https://openwb.de/forum/viewtopic.php?f=5&t=1206" target="_blank" rel="noopener noreferrer">im Forum.</a>
									</div>
									<div class="form-row mb-1">
										<label for="psa_manufacturerlp2" class="col-md-4 col-form-label">Hersteller</label>
										<div class="col">
											<select name="psa_manufacturerlp2" id="psa_manufacturerlp2" class="form-control">
												<option <?php if($psa_manufacturerlp2old == "Peugeot") echo "selected" ?> value="Peugeot">Peugeot</option>
												<option <?php if($psa_manufacturerlp2old == "Citroen") echo "selected" ?> value="Citroen">Citroen</option>
												<option <?php if($psa_manufacturerlp2old == "DS") echo "selected" ?> value="DS">DS</option>
												<option <?php if($psa_manufacturerlp2old == "Opel") echo "selected" ?> value="Opel">Opel</option>
												<option <?php if($psa_manufacturerlp2old == "Vauxhall") echo "selected" ?> value="Vauxhall">Vauxhall</option>
											</select>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_userlp2" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="text" name="psa_userlp2" id="psa_userlp2" value="<?php echo $psa_userlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_passlp2" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="psa_passlp2" id="psa_passlp2" value="<?php echo $psa_passlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_clientidlp2" class="col-md-4 col-form-label">Client-ID</label>
										<div class="col">
											<input class="form-control" type="text" name="psa_clientidlp2" id="psa_clientidlp2" value="<?php echo $psa_clientidlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_clientsecretlp2" class="col-md-4 col-form-label">Client-Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="psa_clientsecretlp2" id="psa_clientsecretlp2" value="<?php echo $psa_clientsecretlp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="psa_intervallp2" class="col-md-4 col-form-label">Abfrageintervall</label>
										<div class="col">
											<input class="form-control" type="number" min="1" step="1" name="psa_intervallp2" id="psa_intervallp2" value="<?php echo $psa_intervallp2old ?>">
											<span class="form-text small">
												Wie oft abgefragt wird. Angabe in Minuten.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere PSA SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($psa_soccalclp2old == 0) echo " active" ?>">
													<input type="radio" name="psa_soccalclp2" id="psa_soccalclp2Off" value="0"<?php if($psa_soccalclp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($psa_soccalclp2old == 1) echo " active" ?>">
													<input type="radio" name="psa_soccalclp2" id="psa_soccalclp2On" value="1"<?php if($psa_soccalclp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Aktuell liefert die PSA API keine SoC Aktualisierung während des Ladevorgangs.<br>
												Wenn Ja gewählt wird, wird der SoC vor dem Laden über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet. Dies erlaubt eine SoC-gesteuerte Ladung.<br>
												Bei Nein wird immer der SoC über die API abgefragt. SoC gesteuerte Ladung ist erst möglich nachdem PSA den SoC auch während des Ladens übermittelt.
											</span>
										</div>
										<div id="psamanualcalclp2div" class="hide">
											<div class="form-row mb-1">
												<label for="psa_akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="psa_akkuglp2" value="<?php echo $akkuglp2old ?>">
													<span class="form-text small">
														Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
														Für Opel Corsa-e und Peugeot e208/e2008: 45-46kWh
													</span>
												</div>
											</div>
											<div class="form-row mb-1">
												<label for="psa_wirkungsgradlp2" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
												<div class="col">
													<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp2" id="psa_wirkungsgradlp2" value="<?php echo $wirkungsgradlp2old ?>">
													<span class="form-text small">
														Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
														Für Opel Corsa-e und Peugeot e208/e2008: 96-98 Prozent<br>
														Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
														Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%. Eine Ausnahme stellt der Zoe dar, dessen Chameleonlader je nach Modellversion und freigegebener Leistung der Wallbox teilweise nur auf ca. 50% kommt.<br>
														Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
														SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
														SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
													</span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<script>
								$(function() {
									function visibility_psa_soccalclp2() {
										if($('#psa_soccalclp2Off').prop("checked")) {
											hideSection('#psamanualcalclp2div');
										} else {
											showSection('#psamanualcalclp2div');
										}
									}

									$('input[type=radio][name=psa_soccalclp2]').change(function(){
										visibility_psa_soccalclp2();
									});

									visibility_psa_soccalclp2();
								});
								</script>
							</div>
							<div id="socmeqlp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label"></label>
										<div class="col">
											<span class="form-text small font-weight-bold">
												Das Mercedes EQ SoC Modul basiert auf der Electric Vehicle Status API des Mercedes Developer Programms. Um die API zu nutzen, muss ein eigener Developer Zugang bei Mercedes beantragt werden. <br/>
												<a href="https://github.com/snaptec/openWB/wiki/EV-SoC-Modul-Mercedes-EQ" target="_blank" rel="noopener noreferrer">Eine Step-by-Step Anleitung findet ihr hier</a>
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_client_id_lp2" class="col-md-4 col-form-label">Client ID</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_client_id_lp2" id="soc_eq_client_id_lp2" value="<?php echo $soc_eq_client_id_lp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_client_secret_lp2" class="col-md-4 col-form-label">Client Secret</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_client_secret_lp2" id="soc_eq_client_secret_lp2" value="<?php echo $soc_eq_client_secret_lp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_vin_lp2" class="col-md-4 col-form-label">Fahrzeug ident</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_vin_lp2" id="soc_eq_vin_lp2" value="<?php echo $soc_eq_vin_lp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_eq_cb_lp2" class="col-md-4 col-form-label">Callback</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_eq_cb_lp2" id="soc_eq_cb_lp2" value="<?php echo $soc_eq_cb_lp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label class="col-md-4 col-form-label"></label>
										<div class="col">
											<span class="form-text small"><b>Wichtig: Nach dem Eintragen der Werte müssen diese gespeichert werden und danach einmalig der folgende Link aufgerufen werden<br/>
											<a href="<?php echo "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&state=lp2&client_id=" . $soc_eq_client_id_lp2old . "&redirect_uri=" . $soc_eq_cb_lp2old . "&scope=mb:vehicle:mbdata:evstatus%20offline_access"?>" target="_blank" rel="noopener noreferrer">HIER bei Mercedes Me anmelden</a></b>
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmkialp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kombiniere SoC Modul und manuelle Berechnung</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($kia_soccalclp2old == 0) echo " active" ?>">
													<input type="radio" name="kia_soccalclp2" id="kia_soccalclp2Off" value="0"<?php if($kia_soccalclp2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($kia_soccalclp1old == 1) echo " active" ?>">
													<input type="radio" name="kia_soccalclp2" id="kia_soccalclp2On" value="1"<?php if($kia_soccalclp2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Wenn Ja gewählt wird, wird der SoC regelmäßig über die API abgerufen. Während des Ladens wird der SoC dann anhand des Zählerstands im Ladepunkt berechnet.<br>
												Bei Nein wird immer der SoC über die API abgefragt.
											</span>
										</div>
									</div>
									<div id="kiamanualcalclp2div" class="hide">
										<div class="form-row mb-1">
											<label for="kia_akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh bei manueller Berechnung</label>
											<div class="col">
												<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="kia_akkuglp2" value="<?php echo $akkuglp2old ?>">
												<span class="form-text small">
													Angabe der Netto-Kapazität der Fahrzeugbatterie in kWh. Dient zur Berechnung des manuellen SoC.<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_wirkungsgradlp2" class="col-md-4 col-form-label">Wirkungsgrad Ladeelektronik bei manueller Berechnung</label>
											<div class="col">
												<input class="form-control" type="number" min="1" step="1" max="100" name="wirkungsgradlp2" id="kia_wirkungsgradlp2" value="<?php echo $wirkungsgradlp2old ?>">
												<span class="form-text small">
													Wert in Prozent, der den gemittelten Wirkungsgrad der Ladeelektronik angibt.<br>
													Für Kia e-niro (11 kWh Lader): 85-90 Prozent<br>
													Durch Verluste in der Ladeelektronik (z. B. Umwandlung Wechselspannung in Gleichspannung) gelangt nicht die komplette Energie, welche durch den Zähler in der Wallbox gemesen wird, im Akku des Fahrzeugs.
													Der anzugebende Wert liegt bei gängigen Fahrzeugen im Bereich 90-95%.<br>
													Liegen die Angaben der Wallbox und des Fahrzeugs nach der Ladung mehrere Prozent auseinander, dann kann mit dieser Einstellung eine Feinabstimmung erfolgen:<br>
													SoC an der Wallbox zu hoch: Wirkungsgrad um ein paar Prozent reduzieren<br>
													SoC an der Wallbox zu gering: Wirkungsgrad um ein paar Prozent erhöhen
												</span>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Push-Funktion für ABRP</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($kia_abrp_enable_2old == 0) echo " active" ?>">
													<input type="radio" name="kia_abrp_enable_2" id="kia_abrp_enable_2Off" value="0"<?php if($kia_abrp_enable_2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($kia_abrp_enable_2old == 1) echo " active" ?>">
													<input type="radio" name="kia_abrp_enable_2" id="kia_abrp_enable_2On" value="1"<?php if($kia_abrp_enable_2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												Wenn Ja gew&auml;hlt wird, wird der SoC regelm&auml;&szlig;ig an ABRP &uuml;bermittelt.<br>
											</span>
										</div>
									</div>
									<div id="kia_abrp_enable_2div" class="hide">
										<div class="form-row mb-1">
											<label for="kia_abrp_token_2" class="col-md-4 col-form-label">ABRP Token</label>
											<div class="col">
												<input class="form-control" type="text" name="kia_abrp_token_2" id="kia_abrp_token_2_text" value="<?php echo $kia_abrp_token_2old ?>">
												<span class="form-text small">
													Token vom Typ "Generic" aus den Fahrzeug-Einstellungen (mehrere Tokens per Semikolon trennen)<br>
												</span>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Erweiterte Einstellungen</label>
										<div class="col">
											<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($kia_advanced2old == 0) echo " active" ?>">
													<input type="radio" name="kia_advanced2" id="kia_advanced2Off" value="0"<?php if($kia_advanced2old == 0) echo " checked=\"checked\"" ?>>Nein
												</label>
												<label class="btn btn-outline-info<?php if($kia_advanced2old == 1) echo " active" ?>">
													<input type="radio" name="kia_advanced2" id="kia_advanced2On" value="1"<?php if($kia_advanced2old == 1) echo " checked=\"checked\"" ?>>Ja
												</label>
											</div>
											<span class="form-text small">
												<br>
											</span>
										</div>
									</div>
									<div id="kia_advanced2div" class="hide">
										<div class="form-row mb-1">
											<label for="kia_adv_cachevalid2" class="col-md-4 col-form-label">Cache G&uuml;ltigkeit</label>
											<div class="col">
												<input class="form-control" type="number" min="-15" step="1" name="kia_adv_cachevalid2" id="kia_adv_cachevalid2" value="<?php echo $kia_adv_cachevalid2old ?>">
												<span class="form-text small">
													Gültigkeitsdauer des letzten Status in Minuten, z.B. nach Abstellen des Autos oder Abruf in der App (0=Abruf immer vom Auto; Default: 10)<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_adv_12v2" class="col-md-4 col-form-label">12V SoC Limit</label>
											<div class="col">
												<input class="form-control" type="number" min="0" max="100" step="1" name="kia_adv_12v2" id="kia_adv_12v2" value="<?php echo $kia_adv_12v2old ?>">
												<span class="form-text small">
													Minimaler SoC der 12V-Batterie für Abrufe in Prozent (Default: 20)<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_adv_interval_unplug2" class="col-md-4 col-form-label">Abrufintervall abgesteckt</label>
											<div class="col">
												<input class="form-control" type="number" min="0" step="1" name="kia_adv_interval_unplug2" id="kia_adv_interval_unplug2" value="<?php echo $kia_adv_interval_unplug2old ?>">
												<span class="form-text small">
													Abrufintervall bei abgestecktem Auto in Minuten (sofern freigegeben)<br>
												</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="kia_adv_ratelimit2" class="col-md-4 col-form-label">Abrufsperre</label>
											<div class="col">
												<input class="form-control" type="number" min="0" step="1" name="kia_adv_ratelimit2" id="kia_adv_ratelimit2" value="<?php echo $kia_adv_ratelimit2old ?>">
												<span class="form-text small">
													Minimaler Abstand zwischen Abrufen in Minuten (default: 15)<br>
												</span>
											</div>
										</div>
									</div>
								</div>
								<script>
								$(function() {
									function visibility_kia_soccalclp2() {
										if($('#kia_soccalclp2Off').prop("checked")) {
											hideSection('#kiamanualcalclp2div');
										} else {
											showSection('#kiamanualcalclp2div');
										}
									}
									function visibility_kia_abrp_enable_2() {
										if($('#kia_abrp_enable_2Off').prop("checked")) {
											hideSection('#kia_abrp_enable_2div');
										} else {
											showSection('#kia_abrp_enable_2div');
										}
									}
									function visibility_kia_advanced2() {
										if($('#kia_advanced2Off').prop("checked")) {
											hideSection('#kia_advanced2div');
										} else {
											showSection('#kia_advanced2div');
										}
									}

									$('input[type=radio][name=kia_soccalclp2]').change(function(){
										visibility_kia_soccalclp2();
									});
									$('input[type=radio][name=kia_abrp_enable_2]').change(function(){
										visibility_kia_abrp_enable_2();
									});
									$('input[type=radio][name=kia_advanced2]').change(function(){
										visibility_kia_advanced2();
									});

									visibility_kia_soccalclp2();
									visibility_kia_abrp_enable_2();
									visibility_kia_advanced2();
								});
								</script>
							</div>
							<div id="soctronitylp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<div class="alert alert-info">
											Für dieses Modul wird ein Konto bei <a href="https://www.tronity.io/" target="_blank" rel="noopener noreferrer">TRONITY</a> benötigt. Über <a href="https://app.tronity.io/signup/7e_-r_uXh" target="_blank" rel="noopener noreferrer">diesen Empfehlungs-Link</a> wird der kostenlose Testzeitraum auf 4 Wochen verlängert. Wie man an die benötigten Zugangsdaten für die openWB kommt, ist <a href="https://help.tronity.io/hc/de-de/articles/360020836760" target="_blank" rel="noopener noreferrer">hier erklärt</a>.
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_client_id_lp2" class="col-md-4 col-form-label">Client ID</label>
										<div class="col">
											<input class="form-control" type="text" required placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" pattern="[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}" name="soc_tronity_client_id_lp2" id="soc_tronity_client_id_lp2" value="<?php echo $soc_tronity_client_id_lp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_client_secret_lp2" class="col-md-4 col-form-label">Client Secret</label>
										<div class="col">
											<input class="form-control" type="text" required placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" pattern="[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}" name="soc_tronity_client_secret_lp2" id="soc_tronity_client_secret_lp2" value="<?php echo $soc_tronity_client_secret_lp2old ?>">
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_select_vehicle_lp2" class="col-md-4 col-form-label">Fahrzeug</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend clickable">
													<div id="soc_tronity_load_vehicles_lp2" class="input-group-text">
														<i class="fas fa-sync"></i>
													</div>
												</div>
												<select id="soc_tronity_select_vehicle_lp2" class="form-control" readonly>
													<option value="">Bitte aktualisieren</option>
												</select>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_tronity_vehicle_id_lp2" class="col-md-4 col-form-label">Fahrzeug ID</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														<i class="fas fa-car"></i>
													</div>
												</div>
												<input required readonly class="form-control" type="text" name="soc_tronity_vehicle_id_lp2" id="soc_tronity_vehicle_id_lp2" value="<?php echo $soc_tronity_vehicle_id_lp2old ?>">
											</div>
										</div>
									</div>
								</div>
								<script>
									$('#soc_tronity_select_vehicle_lp2').change(function(){
										$('#soc_tronity_vehicle_id_lp2').val($(this).val());
									});

									$('#soc_tronity_load_vehicles_lp2').click(function(){
										if( ! $('#soc_tronity_client_id_lp2').val().match(TronityClientPattern) || ! $('#soc_tronity_client_secret_lp2').val().match(TronityClientPattern) ){
											alert("Bitte geben Sie eine gültige Client ID und ein Client Secret an.");
										} else {
											$('#soc_tronity_load_vehicles_lp2').removeClass("bg-warning");
											$('#soc_tronity_load_vehicles_lp2').removeClass("bg-success");
											$(this).find('.fa-sync').addClass('fa-spin');
											$("#soc_tronity_select_vehicle_lp2").empty();
											$.ajax({
												type: "POST",
												url: "https://api-eu.TRONITY.io/oauth/authentication",
												data: JSON.stringify( { "client_id": $('#soc_tronity_client_id_lp2').val(), "client_secret": $('#soc_tronity_client_secret_lp2').val(), "grant_type": "app" } ),
												contentType: "application/json",
												dataType: "json",
												success: function(authdata){
													$('#soc_tronity_load_vehicles_lp2').addClass("bg-warning");
													$.ajax({
														type: "GET",
														url: "https://api-eu.TRONITY.io/v1/vehicles",
														headers: {
															Authorization: 'Bearer '+authdata.access_token
														},
														success: function(vehicledata){
															$('#soc_tronity_load_vehicles_lp2').removeClass("bg-warning");
															$('#soc_tronity_load_vehicles_lp2').addClass("bg-success");
															var vehicleid = $('#soc_tronity_vehicle_id_lp2').val();
															$("<option/>").val('').text("-- Bitte auswählen --").appendTo('#soc_tronity_select_vehicle_lp2');
															vehicledata.data.forEach(function(vehicle){
																newVehicle = $("<option/>").val(vehicle.id).text(vehicle.displayName);
																if( vehicleid == vehicle.id ){
																	newVehicle.attr('selected','selected');
																}
																newVehicle.appendTo('#soc_tronity_select_vehicle_lp2');
															});
															$('#soc_tronity_select_vehicle_lp2').attr('readonly', false);
														},
														error: function(errMsg) {
															alert("Fahrzeuge konnten nicht abgerufen werden!");
														}
													});
												},
												error: function(errMsg) {
													alert("Anmeldung gescheitert!");
												},
												complete: function(){
													$('#soc_tronity_load_vehicles_lp2').find('.fa-sync').removeClass('fa-spin');
												}
											});
										};
									});
								</script>
							</div>
							<div id="socevcclp2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_evcc_select_vehicle_lp2" class="col-md-4 col-form-label">Unterstützte Fahrzeuge</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend clickable">
													<div id="soc_evcc_load_vehicles_lp2" class="input-group-text">
														<i class="fas fa-sync"></i>
													</div>
												</div>
												<select id="soc_evcc_select_vehicle_lp2" class="form-control" readonly>
													<option value="">-- Bitte aktualisieren --</option>
												</select>
											</div>
											<span class="form-text small">
												Die Auswahlliste dient nur der einfachen Eingabe des Fahrzeugtyps.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_vehicle_id_lp2" class="col-md-4 col-form-label">Fahrzeug Typ</label>
										<div class="col">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														<i class="fas fa-car"></i>
													</div>
												</div>
												<input required readonly class="form-control" type="text" name="soc_evcc_type_lp2" id="soc_evcc_type_lp2" value="<?php echo $soc_evcc_type_lp2old ?>">
											</div>
											<span class="form-text small">
												Dies ist der intern verwendete Typ, nicht der lesbare Name aus der Auswahlliste.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_username_lp2" class="col-md-4 col-form-label">Benutzername</label>
										<div class="col">
											<input class="form-control" type="email" name="soc_evcc_username_lp2" id="soc_evcc_username_lp2" value="<?php echo $soc_evcc_username_lp2old ?>">
											<span class="form-text small">
												Email Adresse des Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_password_lp2" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_evcc_password_lp2" id="soc_evcc_password_lp2" value="<?php echo $soc_evcc_password_lp2old ?>">
											<span class="form-text small">
												Passwort des Logins
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_vin_lp2" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_evcc_vin_lp2" id="soc_evcc_vin_lp2" value="<?php echo $soc_evcc_vin_lp2old ?>">
											<span class="form-text small">
												Vollständige VIN des Fahrzeugs
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="soc_evcc_token_lp2" class="col-md-4 col-form-label">Token</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_evcc_token_lp2" id="soc_evcc_token_lp2" value="<?php echo $soc_evcc_token_lp2old ?>">
											<span class="form-text small">
												EVCC Abo Token, zu beziehen unter https://cloud.evcc.io
											</span>
										</div>
									</div>
								</div>
								<script>
									$('#soc_evcc_select_vehicle_lp2').change(function(){
										$('#soc_evcc_type_lp2').val($(this).val());
									});

									$('#soc_evcc_load_vehicles_lp2').click(function(){
										$('#soc_evcc_load_vehicles_lp2').removeClass("bg-danger");
										$('#soc_evcc_load_vehicles_lp2').removeClass("bg-success");
										$('#soc_evcc_load_vehicles_lp2').addClass("bg-warning");
										$(this).find('.fa-sync').addClass('fa-spin');
										$("#soc_evcc_select_vehicle_lp2").empty();
										$.ajax({
											type: "GET",
											url: "https://cloud.evcc.io/api/vehicles",
											success: function(vehicledata){
												$('#soc_evcc_load_vehicles_lp2').removeClass("bg-warning");
												$('#soc_evcc_load_vehicles_lp2').addClass("bg-success");
												var vehicleid = $('#soc_evcc_type_lp2').val();
												$("<option/>").val('').text("-- Bitte auswählen --").appendTo('#soc_evcc_select_vehicle_lp2');
												vehicledata.forEach(function(vehicle){
													newVehicle = $("<option/>").val(vehicle.id).text(vehicle.name);
													if( vehicleid == vehicle.id ){
														newVehicle.attr('selected','selected');
													}
													newVehicle.appendTo('#soc_evcc_select_vehicle_lp2');
												});
												$('#soc_evcc_select_vehicle_lp2').attr('readonly', false);
											},
											error: function(errMsg) {
												$('#soc_evcc_load_vehicles_lp2').removeClass("bg-warning");
												$('#soc_evcc_load_vehicles_lp2').addClass("bg-danger");
												alert("Fahrzeuge konnten nicht abgerufen werden!");
											},
											complete: function(){
												$('#soc_evcc_load_vehicles_lp2').find('.fa-sync').removeClass('fa-spin');
											}
										});
									});
								</script>
							</div>
							<div id="socmintervall2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2intervall" class="col-md-4 col-form-label">Abfrageintervall Standby</label>
										<div class="col">
											<input class="form-control" type="text" name="soc2intervall" id="soc2intervall" value="<?php echo $soc2intervallold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn nicht geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="socmintervallladen2" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc2intervallladen" class="col-md-4 col-form-label">Abfrageintervall Ladevorgang</label>
										<div class="col">
											<input class="form-control" type="text" name="soc2intervallladen" id="soc2intervallladen" value="<?php echo $soc2intervallladenold ?>">
											<span class="form-text small">
												Wie oft das Fahrzeug abgefragt wird, wenn geladen wird. Angabe in Minuten.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function display_lp2() {
							hideSection('#evsecondacs1');
							hideSection('#evseconmbs1');
							hideSection('#evseconswifis1');
							hideSection('#llmodullp2');
							hideSection('#evsecongoes1');
							hideSection('#evsecoslaveeth');
							hideSection('#evseconkebas1');
							hideSection('#evseconnrgkicks1');
							hideSection('#openwb12s1v1');
							hideSection('#openwb12s1v2');
							hideSection('#evseconextopenwblp2');
							hideSection('#evseconowbprolp2');
							hideSection('#evsecondaemonlp2');
							hideSection('#evseconipevselp2');
							hideSection('#evseconmqtts1');
							hideSection('#evsecontwcmanagers1');

							if($('#evsecons1').val() == 'modbusevse') {
								switch( $("#evsecons1 option:selected").attr('data-id') ){
									case "openwb series1/2 duo v1":
										showSection('#openwb12s1v1');
									break;
									case "openwb series1/2 duo v2":
										showSection('#openwb12s1v2');
									break;
						       			default:
										showSection('#evseconmbs1');
										showSection('#llmodullp2');
										display_llmp2();
								}
							}
							if($('#evsecons1').val() == 'ipevse') {
								showSection('#evseconipevselp2');
								showSection('#llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'dac') {
								showSection('#evsecondacs1');
								showSection('#llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'mqttevse') {
								showSection('#evseconmqtts1');
								showSection('#llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'simpleevsewifi') {
								showSection('#evseconswifis1');
							}
							if($('#evsecons1').val() == 'extopenwb') {
								showSection('#evseconextopenwblp2');
							}
							if($('#evsecons1').val() == 'owbpro') {
								showSection('#evseconowbprolp2');
							}

							if($('#evsecons1').val() == 'daemon') {
								showSection('#evsecondaemonlp2');
							}
							if($('#evsecons1').val() == 'goe') {
								showSection('#evsecongoes1');
							}
							if($('#evsecons1').val() == 'slaveeth') {
								showSection('#evsecoslaveeth');
							}
							if($('#evsecons1').val() == 'keba') {
								showSection('#evseconkebas1');
							}
							if($('#evsecons1').val() == 'nrgkick') {
								showSection('#evseconnrgkicks1');
							}
							if($('#evsecons1').val() == 'twcmanager') {
								showSection('#evsecontwcmanagers1');
							}
						}

						function display_llmp2() {
							hideSection('#sdm630s1div');
							hideSection('#sdm120s1div');
							hideSection('#swifis1div');
							hideSection('#mpm3pmlls1div');
							hideSection('#rs485lanlp2');
							hideSection('#mpm3pmlllp2div');
							hideSection('#mqttlllp2div');

							if($('#ladeleistungs1modul').val() == 'sdm630modbuslls1') {
								showSection('#sdm630s1div');
								showSection('#rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'sdm120modbuslls1') {
								showSection('#sdm120s1div');
								showSection('#rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'simpleevsewifis1') {
								showSection('#swifis1div');
							}
							if($('#ladeleistungs1modul').val() == 'goelp2') {
								showSection('#swifis1div');
							}
							if($('#ladeleistungs1modul').val() == 'mpm3pmlllp2') {
								showSection('#mpm3pmlllp2div');
								hideSection('#rs485lanlp2'); // BUG show/hide typo?
							}
							if($('#ladeleistungs1modul').val() == 'mpm3pmlls1') {
								showSection('#mpm3pmlls1div');
								showSection('#rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'mqttlllp2') {
								showSection('#mqttlllp2div');
							}
						}

						function display_socmodul1() {

							hideSection('#socmodullp2');
							hideSection('#socmqtt1');
							hideSection('#socmtype2');
							hideSection('#socmuser2');
							hideSection('#socmpass2');
							hideSection('#socmpin2');
							hideSection('#socmnone1');
							hideSection('#socmhttp1');
							hideSection('#socleaf1');
							hideSection('#soci31');
							hideSection('#socevnotifylp2');
							hideSection('#soczoelp2');
							hideSection('#socmteslalp2');
							hideSection('#socmeqlp2');
							hideSection('#socmyrenaultlp2');
							hideSection('#soccarnetlp2');
							hideSection('#socmzeronglp2');
							hideSection('#socmypeugeotlp2');
							hideSection('#socmyopellp2');
							hideSection('#socpsalp2');
							hideSection('#socmvin2');
							hideSection('#socmintervall2');
							hideSection('#socmintervallladen2');
							hideSection('#socmanuallp2');
							hideSection('#soctronitylp2');
							hideSection('#socevcclp2');
							hideSection('#socmkialp2');
							hideSection('#socoldevccwarninglp2');
							hideSection('#socmvwidinfolp2');
							hideSection('#socsupportinfolp2');
							hideSection('#socnosupportinfolp2');

							if($('#socmodul1').val() == 'none') {
								showSection('#socmnone1');
							} else {
								showSection('#socmodullp2', false); // do not enable all input child-elements!
							}
							if($('#socmodul1').val() == 'soc_mqtt') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3145')
								showSection('#socsupportinfolp2');
								showSection('#socmqtt1');
							}
							if($('#socmodul1').val() == 'soc_http1') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3143')
								showSection('#socsupportinfolp2');
								showSection('#socmhttp1');
								showSection('#socmintervall2');
								showSection('#socmintervallladen2');
							}
							if($('#socmodul1').val() == 'soc_aiwayslp2') {
                                showSection('#socaiwayslp2');
                            }
							if($('#socmodul1').val() == 'soc_audilp2') {
								showSection('#socoldevccwarninglp2');
								showSection('#socmuser2');
								showSection('#socmpass2');
								showSection('#socmvin2');
							}
							if($('#socmodul1').val() == 'soc_kialp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3137')
								showSection('#socsupportinfolp2');
								showSection('#socmuser2');
								showSection('#socmpass2');
								showSection('#socmpin2');
								showSection('#socmvin2');
								showSection('#socmintervall2');
								showSection('#socmkialp2');
							}
							if($('#socmodul1').val() == 'soc_idlp2') {
								showSection('#socoldevccwarninglp2');
								showSection('#socmuser2');
								showSection('#socmpass2');
								showSection('#socmvin2');
							}
							if($('#socmodul1').val() == 'soc_vwidlp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&p=58178')
								showSection('#socsupportinfolp2');
								showSection('#socmvwidinfolp2');
								showSection('#socmuser2');
								showSection('#socmpass2');
								showSection('#socmvin2');
								showSection('#socmintervall2');
								showSection('#socmintervallladen2');
							}
							if($('#socmodul1').val() == 'soc_vaglp2') {
								showSection('#socoldevccwarninglp2');
								showSection('#socmtype2');
								showSection('#socmuser2');
								showSection('#socmpass2');
								showSection('#socmvin2');
								showSection('#socmintervall2');
								showSection('#socmintervallladen2');
							}
							if($('#socmodul1').val() == 'soc_evcclp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3134')
								showSection('#socsupportinfolp2');
								showSection('#socevcclp2');
								showSection('#socmintervall2');
								showSection('#socmintervallladen2');
							}
							if($('#socmodul1').val() == 'soc_leafs1') {
								showSection('#socleaf1');
							}
							if($('#socmodul1').val() == 'soc_myrenaultlp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3139')
								showSection('#socsupportinfolp2');
								showSection('#socmyrenaultlp2');
							}
							if($('#socmodul1').val() == 'soc_i3s1') {
								showSection('#soci31');
							}
							if($('#socmodul1').val() == 'soc_evnotifys1') {
								showSection('#socevnotifylp2');
							}
							if($('#socmodul1').val() == 'soc_zoelp2') {
								showSection('#soczoelp2');
							}
							if($('#socmodul1').val() == 'soc_eqlp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3135')
								showSection('#socsupportinfolp2');
								showSection('#socmeqlp2');
							}
							if($('#socmodul1').val() == 'soc_carnetlp2') {
								showSection('#soccarnetlp2');
							}
							if($('#socmodul1').val() == 'soc_teslalp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3141')
								showSection('#socsupportinfolp2');
								showSection('#socmteslalp2');
							}
							if($('#socmodul1').val() == 'soc_zeronglp2') {
								showSection('#socmzeronglp2');
							}
							if($('#socmodul1').val() == 'soc_mypeugeotlp2') {
								showSection('#socmypeugeotlp2');
							}
							if($('#socmodul1').val() == 'soc_myopellp2') {
								showSection('#socmyopellp2');
							}
							if($('#socmodul1').val() == 'soc_psalp2') {
								showSection('#socpsalp2');
							}
							if($('#socmodul1').val() == 'soc_manuallp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3144')
								showSection('#socsupportinfolp2');
								showSection('#socmanuallp2');
							}
							if($('#socmodul1').val() == 'soc_volvolp2') {
								showSection('#socmuser2');
								showSection('#socmpass2');
							}
							if($('#socmodul1').val() == 'soc_tronitylp2') {
								$('#socsuportlinklp2').attr('href', 'https://openwb.de/forum/viewtopic.php?f=12&t=3142')
								showSection('#socsupportinfolp2');
								showSection('#soctronitylp2');
								showSection('#socmintervall2');
								showSection('#socmintervallladen2');
							}
						}

						function display_lastmanagement() {
							if($('#lastmanagementOff').prop("checked")) {
								hideSection('#lastmman');
							}
							else {
								showSection('#lastmman');
								display_socmodul1();
								display_llmp2 ();
								display_lp2();
							}
						}

						$(function() {
							display_lastmanagement();
							display_socmodul1();
							display_llmp2 ();
							display_lp2();

							$('input[type=radio][name=lastmanagement]').change(function() {
								display_lastmanagement();
							} );

							$('#socmodul1').change( function(){
								display_socmodul1();
							});

							$('#ladeleistungs1modul').change( function(){
								display_llmp2();
							});

							$('#evsecons1').change( function(){
								display_lp2();
							});
						});
					</script>
				</div>

				<!-- Ladepunkt 3 -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Ladepunkt 3</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagements2old == 0) echo " active" ?>">
											<input type="radio" name="lastmanagements2" id="lastmanagements2Off" value="0"<?php if($lastmanagements2old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($lastmanagements2old == 1) echo " active" ?>">
											<input type="radio" name="lastmanagements2" id="lastmanagements2On" value="1"<?php if($lastmanagements2old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body hide" id="lasts2mman">
						<div class="form-group">
							<div class="form-row mb-1">
								<label for="lp3name" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="lp3name" id="lp3name" value="<?php echo $lp3nameold ?>">
								</div>
							</div>
						</div>
						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="evsecons2" class="col-md-4 col-form-label">Anbindung</label>
							<div class="col">
								<select name="evsecons2" id="evsecons2" class="form-control">
									<optgroup label="openWB">
										<option <?php if($evsecons2old == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
										<option <?php if($evsecons2old == "owbpro") echo "selected" ?> value="owbpro">openWB Pro</option>
										<option <?php if($evsecons2old == "thirdeth") echo "selected" ?> value="thirdeth">dritter Ladepunkt</option>
										<option <?php if($evsecons2old == "ipevse") echo "selected" ?> value="ipevse">Satellit</option>
									</optgroup>
									<optgroup label="andere Ladepunkte">
										<option <?php if($evsecons2old == "goe") echo "selected" ?> value="goe">Go-e</option>
										<option <?php if($evsecons2old == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($evsecons2old == "dac") echo "selected" ?> value="dac">DAC</option>
										<option <?php if($evsecons2old == "modbusevse") echo "selected" ?> value="modbusevse">Modbus</option>
										<option <?php if($evsecons2old == "mqttevse") echo "selected" ?> value="mqttevse">MQTT</option>
									</optgroup>
								</select>
							</div>
						</div>
						<div id="evseconthirdeth" class="hide">
							<input type="hidden" name="ladeleistungs2modul" value="mpm3pmethlls2">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="evseconextopenwblp3" class="hide">
							<input type="hidden" name="ladeleistungs2modul" value="extopenwblp3">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="chargep3ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep3ip" id="chargep3ip" value="<?php echo $chargep3ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="chargep3cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="2" step="1" name="chargep3cp" id="chargep3cp" value="<?php echo $chargep3cpold ?>">
										<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconowbprolp3" class="hide">
							<input type="hidden" name="ladeleistungs2modul" value="owbprolp3">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="owbpro3ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="owbpro3ip" id="owbpro3ip" value="<?php echo $owbpro3ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="evseconipevselp3" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evseiplp3" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp3" id="evseiplp3" value="<?php echo $evseiplp3old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Aufgedruckt auf dem Label der openWB.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseidlp3" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp3" id="evseidlp3" value="<?php echo $evseidlp3old ?>">
										<span class="form-text small">Gültige Werte 1-254. Aufgedruckt auf dem Label der openWB.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmbs2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsesources2" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="evsesources2" id="evsesources2" value="<?php echo $evsesources2old ?>">
										<span class="form-text small">Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus der EVSE angeschlossen ist.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evseids2" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evseids2" id="evseids2" value="<?php echo $evseids2old ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evselanips2" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evselanips2" id="evselanips2" value="<?php echo $evselanips2old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Vermutlich gleich der IP des SDM Zählers in der WB.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecondacs2" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="dacregisters2" class="col-md-4 col-form-label">Dacregister</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="99" step="1" name="dacregisters2" id="dacregisters2" value="<?php echo $dacregisters2old ?>">
										<span class="form-text small">
											Gültige Werte 0-99. Bei EVSE Anbindung per DAC (MCP 4725) Standardwert meist 62, oft auch 60 oder 48. Abhängig vom verbauten MCP.
											Der benötigte Wert sollte <a href="/openWB/ramdisk/i2csearch">HIER</a> zu finden sein.
											Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evseconmqtts2" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu lesen:<br>
								<span class="text-info">openWB/lp/3/AConfigured</span> Stromvorgabe in A<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/lp/3/plugStat</span> Status, ob ein Fahrzeug angesteckt ist, nur 0 (nein) oder 1 (ja)<br>
								<span class="text-info">openWB/set/lp/3/chargeStat</span> Status, ob gerade geladen wird, nur 0 (nein) oder 1 (ja)
							</div>
						</div>
						<div id="evseconswifis2" class="hide">
							<input type="hidden" name="ladeleistungs2modul" value="simpleevsewifis2">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="evsewifiiplp3" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evsewifiiplp3" id="evsewifiiplp3" value="<?php echo $evsewifiiplp3old ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="evsewifitimeoutlp3" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="evsewifitimeoutlp3" id="evsewifitimeoutlp3" value="<?php echo $evsewifitimeoutlp3old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort der Simple EVSE gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn die SimpleEVSE z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecongoes2" class="hide">
							<input type="hidden" name="ladeleistungs2modul" value="goelp3">
							<div class="form-group">
								<div class="alert alert-info">
									Seit Firmware Version 0.40 wird PV-Laden besser unterstützt. 
									<span class="text-danger">
										Bitte halten Sie die go-e Firmware auf einem aktuellen Stand.
									</span>
								</div>
								<div class="form-row mb-1">
									<label for="goeiplp3" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="goeiplp3" id="goeiplp3" value="<?php echo $goeiplp3old ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="goetimeoutlp3" class="col-md-4 col-form-label">Timeout</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="10" step="1" name="goetimeoutlp3" id="goetimeoutlp3" value="<?php echo $goetimeoutlp3old ?>">
										<span class="form-text small">
											Gibt die Zeit in Sekunden an wie lange auf Antwort des Go-echargers gewartet wird. Bei gutem Wlan reichen 2 Sekunden aus.
											Zu lange Wartezeit zieht einen Verzug der Regellogik von openWB mit sich wenn der Go-echarger z.B. gerade unterwegs genutzt wird.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="llmodullp3" class="hide">
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="ladeleistungs2modul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungs2modul" id="ladeleistungs2modul" class="form-control">
										<optgroup label="openWB">
											<option <?php if($ladeleistungs2modulold == "mpm3pmlllp3") echo "selected" ?> value="mpm3pmlllp3">openWB Satellit</option>
											<option <?php if($ladeleistungs2modulold == "mpm3pmtripplelp3") echo "selected" ?> value="mpm3pmtripplelp3">openWB Tripple</option>
										</optgroup>
										<optgroup label="andere Messgeräte">
											<option <?php if($ladeleistungs2modulold == "mpm3pmlls2") echo "selected" ?> value="mpm3pmlls2">MPM3PM Modbus</option>
											<option <?php if($ladeleistungs2modulold == "sdm120modbuslls2") echo "selected" ?> value="sdm120modbuslls2">SDM 120 Modbus</option>
											<option <?php if($ladeleistungs2modulold == "sdm630modbuslls2") echo "selected" ?> value="sdm630modbuslls2">SDM 630 Modbus</option>
											<option <?php if($ladeleistungs2modulold == "simpleevsewifis2") echo "selected" ?> value="simpleevsewifis2">Simple EVSE Wifi</option>
										</optgroup>
										<optgroup label="generische Module">
											<option <?php if($ladeleistungs2modulold == "mqttlllp3") echo "selected" ?> value="mqttlllp3">MQTT</option>
										</optgroup>
									</select>
								</div>
							</div>
							<div id="mqttlllp3div" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/3/W</span> Ladeleistung in Watt, int, positiv<br>
									<span class="text-info">openWB/set/lp/3/kWhCounter</span> Zählerstand in kWh, float, Punkt als Trenner, nur positiv<br>
									Optional zusätzlich:<br>
									<span class="text-info">openWB/set/lp/3/VPhase1</span> Spannung Phase 1, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/3/VPhase2</span> Spannung Phase 2, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/3/VPhase3</span> Spannung Phase 3, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/3/APhase1</span> Strom Phase 1, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/3/APhase2</span> Strom Phase 2, float, Punkt als Trenner, nur positiv<br>
									<span class="text-info">openWB/set/lp/3/APhase3</span> Strom Phase 3, float, Punkt als Trenner, nur positiv
								</div>
							</div>
							<div id="mpm3pmlllp3div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpmlp3ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp3ip" id="mpmlp3ip" value="<?php echo $mpmlp3ipold ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse des Modbus Ethernet Konverters im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp3id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp3id" id="mpmlp3id" value="<?php echo $mpmlp3idold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="mpm3pmlls2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="mpm3pmlls2source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="mpm3pmlls2source" id="mpm3pmlls2source" value="<?php echo $mpm3pmlls2sourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das MPM3PM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpm3pmlls2id" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmlls2id" id="mpm3pmlls2id" value="<?php echo $mpm3pmlls2idold ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="swifis2div" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.
								</div>
							</div>
							<div id="sdm630s2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm630lp3source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm630lp3source" id="sdm630lp3source" value="<?php echo $sdm630lp3sourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdmids2" class="col-md-4 col-form-label">ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdmids2" id="sdmids2" value="<?php echo $sdmids2old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM. Für SDM230 & SDM630v2.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="sdm120s2div" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="sdm120lp3source" class="col-md-4 col-form-label">Source</label>
										<div class="col">
											<input class="form-control" type="text" name="sdm120lp3source" id="sdm120lp3source" value="<?php echo $sdm120lp3sourceold ?>">
											<span class="form-text small">
												Gültige Werte z. B. /dev/ttyUSB0, /dev/virtualcom0. Serieller Port an dem der Modbus das SDM angeschlossen ist.
												Nach Ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid1s2" class="col-md-4 col-form-label">ID Phase 1</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid1s2" id="sdm120modbusllid1s2" value="<?php echo $sdm120modbusllid1s2old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der ersten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid2s2" class="col-md-4 col-form-label">ID Phase 2</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid2s2" id="sdm120modbusllid2s2" value="<?php echo $sdm120modbusllid2s2old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3s2" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3s2" id="sdm120modbusllid3s2" value="<?php echo $sdm120modbusllid3s2old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="rs485lanlp3" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="lllaniplp3" class="col-md-4 col-form-label">IP Adresse RS485/Lan-Konverter</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lllaniplp3" id="lllaniplp3" value="<?php echo $lllaniplp3old ?>">
											<span class="form-text small">
												Ist nur von Belang, wenn die Source auf /dev/virtualcomX steht. Ansonsten irrelevant.<br>
												Gültige Werte IPs. Wenn ein LAN Konverter genutzt wird, muss die Source auf /dev/virtualcomx (z.B. /dev/virtualcom0) gesetzt werden.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function display_lastmanagement2() {
							if($('#lastmanagements2Off').prop("checked")) {
								hideSection('#lasts2mman');
							}
							else {
								showSection('#lasts2mman');
								display_llmp3();
								display_lp3();
							}
						}

						function display_lp3 () {
							hideSection('#evsecondacs2');
							hideSection('#evseconmbs2');
							hideSection('#evseconswifis2');
							hideSection('#llmodullp3');
							hideSection('#evsecongoes2');
							hideSection('#evseconipevselp3');
							hideSection('#evseconextopenwblp3');
							hideSection('#evseconowbprolp3');
							hideSection('#evseconthirdeth');
							hideSection('#evseconmqtts2');

							if($('#evsecons2').val() == 'thirdeth') {
								showSection('#evseconthirdeth');
							}
							if($('#evsecons2').val() == 'dac') {
								showSection('#evsecondacs2');
								showSection('#llmodullp3');
								display_llmp3();
							}
							if($('#evsecons2').val() == 'mqttevse') {
								showSection('#evseconmqtts2');
								showSection('#llmodullp3');
								display_llmp2();
							}
							if($('#evsecons2').val() == 'modbusevse') {
								showSection('#evseconmbs2');
								showSection('#llmodullp3');
								display_llmp3();
							}
							if($('#evsecons2').val() == 'simpleevsewifi') {
								showSection('#evseconswifis2');
							}
							if($('#evsecons2').val() == 'extopenwb') {
								showSection('#evseconextopenwblp3');
							}
							if($('#evsecons2').val() == 'owbpro') {
								showSection('#evseconowbprolp3');
							}
							if($('#evsecons2').val() == 'goe') {
								showSection('#evsecongoes2');
							}
							if($('#evsecons2').val() == 'ipevse') {
								showSection('#evseconipevselp3');
								showSection('#llmodullp3');
								display_llmp3();
							}
						}

						function display_llmp3 () {
							hideSection('#sdm630s2div');
							hideSection('#sdm120s2div');
							hideSection('#swifis2div');
							hideSection('#rs485lanlp3');
							hideSection('#mpm3pmlls2div');
							hideSection('#mpm3pmlllp3div');
							hideSection('#mqttlllp3div');

							if($('#ladeleistungs2modul').val() == 'mpm3pmlllp3') {
								showSection('#mpm3pmlllp3div');
								showSection('#rs485lanlp3');
							}
							if($('#ladeleistungs2modul').val() == 'sdm630modbuslls2') {
								showSection('#sdm630s2div');
								showSection('#rs485lanlp3');
							}
							if($('#ladeleistungs2modul').val() == 'sdm120modbuslls2') {
								showSection('#sdm120s2div');
								showSection('#rs485lanlp3');
							}
							if($('#ladeleistungs2modul').val() == 'simpleevsewifis2') {
								showSection('#swifis2div');
							}
							if($('#ladeleistungs2modul').val() == 'goelp3') {
								showSection('#swifis2div');
							}
							if($('#ladeleistungs2modul').val() == 'mpm3pmlls2') {
								showSection('#mpm3pmlls2div');
								showSection('#rs485lanlp3');
							}
							if($('#ladeleistungs2modul').val() == 'mqttlllp3') {
								showSection('#mqttlllp3div');
							}
						}

						$(function() {
							display_lastmanagement2();

							$('#evsecons2').change( function(){
								display_lp3();
							});

							$('input[type=radio][name=lastmanagements2]').change(function() {
								display_lastmanagement2();
							});

							$('#ladeleistungs2modul').change( function(){
								display_llmp3();
							});
						});
					</script>
				</div>

				<?php for( $chargepointNum = 4; $chargepointNum <= 8; $chargepointNum++ ){ ?>
					<!-- Ladepunkt <?php echo $chargepointNum; ?> -->
					<div class="card border-primary">
						<div class="card-header bg-primary">
							<div class="form-group mb-0">
								<div class="form-row vaRow mb-0">
									<div class="col-4">Ladepunkt <?php echo $chargepointNum; ?></div>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-sm btn-outline-info<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 0) echo " active" ?>">
												<input type="radio" name="lastmanagementlp<?php echo $chargepointNum; ?>" id="lastmanagementlp<?php echo $chargepointNum; ?>Off" value="0"<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-sm btn-outline-info<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 1) echo " active" ?>">
												<input type="radio" name="lastmanagementlp<?php echo $chargepointNum; ?>" id="lastmanagementlp<?php echo $chargepointNum; ?>On" value="1"<?php if(${'lastmanagementlp'.$chargepointNum.'old'} == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card-body hide" id="lastlp<?php echo $chargepointNum; ?>mman">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="lp<?php echo $chargepointNum; ?>name" class="col-md-4 col-form-label">Name</label>
									<div class="col">
										<input class="form-control" type="text" name="lp<?php echo $chargepointNum; ?>name" id="lp<?php echo $chargepointNum; ?>name" value="<?php echo ${'lp'.$chargepointNum.'nameold'} ?>">
									</div>
								</div>
							</div>
							<hr class="border-primary">
							<div class="form-row mb-1">
								<label for="evseconlp<?php echo $chargepointNum; ?>" class="col-md-4 col-form-label">Anbindung</label>
								<div class="col">
									<select name="evseconlp<?php echo $chargepointNum; ?>" id="evseconlp<?php echo $chargepointNum; ?>" class="form-control">
										<optgroup label="openWB">
											<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
											<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "owbpro") echo "selected" ?> value="owbpro">openWB Pro</option>
											<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "ipevse") echo "selected" ?> value="ipevse">Satellit</option>
										</optgroup>
									</select>
								</div>
							</div>
							<div id="evseconextopenwblp<?php echo $chargepointNum; ?>" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="chargep<?php echo $chargepointNum; ?>ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="chargep<?php echo $chargepointNum; ?>ip" id="chargep<?php echo $chargepointNum; ?>ip" value="<?php echo ${'chargep'.$chargepointNum.'ipold'} ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12<br>
												Die externe openWB muss die Option "openWB ist nur ein Ladepunkt" aktiv haben!
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="chargep<?php echo $chargepointNum; ?>cp" class="col-md-4 col-form-label">Ladepunkt an der externen openWB</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="2" step="1" name="chargep<?php echo $chargepointNum; ?>cp" id="chargep<?php echo $chargepointNum; ?>cp" value="<?php echo ${'chargep'.$chargepointNum.'cpold'} ?>">
											<span class="form-text small">Ist die externe openWB eine Duo gibt diese Option an ob Ladepunkt 1 oder 2 angesprochen werden soll.</span>
										</div>
									</div>
								</div>
							</div>
							<div id="evseconowbprolp<?php echo $chargepointNum; ?>" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="owbpro<?php echo $chargepointNum; ?>ip" class="col-md-4 col-form-label">IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="owbpro<?php echo $chargepointNum; ?>ip" id="owbpro<?php echo $chargepointNum; ?>ip" value="<?php echo ${'owbpro'.$chargepointNum.'ipold'} ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											</span>
										</div>
									</div>
								</div>
							</div>

							<div id="evseconipevselp<?php echo $chargepointNum; ?>" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="evseiplp<?php echo $chargepointNum; ?>" class="col-md-4 col-form-label">EVSE IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evseiplp<?php echo $chargepointNum; ?>" id="evseiplp<?php echo $chargepointNum; ?>" value="<?php echo ${'evseiplp'.$chargepointNum.'old'} ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="evseidlp<?php echo $chargepointNum; ?>" class="col-md-4 col-form-label">EVSE ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="evseidlp<?php echo $chargepointNum; ?>" id="evseidlp<?php echo $chargepointNum; ?>" value="<?php echo ${'evseidlp'.$chargepointNum.'old'} ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID der EVSE.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp<?php echo $chargepointNum; ?>ip" class="col-md-4 col-form-label">Ladeleistung IP Adresse</label>
										<div class="col">
											<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpmlp<?php echo $chargepointNum; ?>ip" id="mpmlp<?php echo $chargepointNum; ?>ip" value="<?php echo ${'mpmlp'.$chargepointNum.'ipold'} ?>">
											<span class="form-text small">
												Gültige Werte IP Adresse im Format: 192.168.0.12. IP Adresse des Modbus Ethernet Konverters.
											</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="mpmlp<?php echo $chargepointNum; ?>id" class="col-md-4 col-form-label">Ladeleistung ID</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="mpmlp<?php echo $chargepointNum; ?>id" id="mpmlp<?php echo $chargepointNum; ?>id" value="<?php echo ${'mpmlp'.$chargepointNum.'idold'} ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
										</div>
									</div>
								</div>
							</div>
						</div>
						<script>
							function display_lp<?php echo $chargepointNum; ?> () {
								hideSection('#evseconipevselp<?php echo $chargepointNum; ?>');
								hideSection('#evseconextopenwblp<?php echo $chargepointNum; ?>');
								hideSection('#evseconowbprolp<?php echo $chargepointNum; ?>');
								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'owbpro') {
									showSection('#evseconowbprolp<?php echo $chargepointNum; ?>');
								}
								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'extopenwb') {
									showSection('#evseconextopenwblp<?php echo $chargepointNum; ?>');
								}
								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'ipevse') {
									showSection('#evseconipevselp<?php echo $chargepointNum; ?>');
								}
							}

							function display_lastmanagementlp<?php echo $chargepointNum; ?>() {
								if($('#lastmanagementlp<?php echo $chargepointNum; ?>Off').prop("checked")) {
									hideSection('#lastlp<?php echo $chargepointNum; ?>mman');
								}
								else {
									showSection('#lastlp<?php echo $chargepointNum; ?>mman');
									display_lp<?php echo $chargepointNum; ?>();
								}
							}

							$(function() {
								display_lastmanagementlp<?php echo $chargepointNum; ?>();

								$('#evseconlp<?php echo $chargepointNum; ?>').change( function(){
									display_lp<?php echo $chargepointNum; ?>();
								});
								$('input[type=radio][name=lastmanagementlp<?php echo $chargepointNum; ?>]').change(function() {
									display_lastmanagementlp<?php echo $chargepointNum; ?>();
								});
							});
						</script>
					</div>
				<?php } ?>

				<div class="form-row text-center">
					<div class="col">
						<button type="submit" class="btn btn-success">Speichern</button>
					</div>
				</div>
			</form>

			<div class="row justify-content-center">
				<div class="col text-center">
					Open Source made with love!<br>
					Jede Spende hilft die Weiterentwicklung von openWB voranzutreiben<br>
					<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
						<input type="hidden" name="cmd" value="_s-xclick">
						<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
						<input type="image" src="./img/btn_donate_SM.gif" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
						<img alt="" src="./img/pixel.gif" width="1" height="1">
					</form>
				</div>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
			  <small>Sie befinden sich hier: Einstellungen/Modulkonfiguration</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navModulkonfigurationLp').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
