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
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<script>
			/**
			 * hideSection
			 * add class 'hide' to element with id 'section'
			 * disables all contained input and select elements if 'disableChildren' is not set to false
			**/
			function hideSection(section, disableChildren=true) {
				$('#'+section).addClass('hide');
				if (disableChildren) {
					$('#'+section).find('input').prop("disabled", true);
					$('#'+section).find('select').prop("disabled", true);
				}
			}

			/**
			 * showSection
			 * remove class 'hide' from element with id 'section'
			 * enables all contained input and select elements if 'enableChildren' is not set to false
			**/
			function showSection(section, enableChildren=true) {
				$('#'+section).removeClass('hide');
				if (enableChildren) {
					$('#'+section).find('input').prop("disabled", false);
					$('#'+section).find('select').prop("disabled", false);
				}
			}

			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for(var i = 0; i <ca.length; i++) {
					var c = ca[i];
					while (c.charAt(0) == ' ') {
						c = c.substring(1);
					}
					if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
					}
				}
				return '';
			}
			var themeCookie = getCookie('openWBTheme');
			// include special Theme style
			if( '' != themeCookie ){
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20200801">');
			}
		</script>
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
			<form action="./tools/saveconfig.php" method="POST">

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
									<!-- WARNING: the text value of the "openWB series1/2 XXX" options is checked later in the script section -->
									<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/ttyUSB0" && $mpm3pmllidold == "5") echo "selected" ?> value="modbusevse">openWB series1/2</option>
									<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/ttyUSB0" && $mpm3pmllidold == "105") echo "selected" ?> value="modbusevse">openWB series1/2 mit geeichtem Zähler</option>
									<option <?php if($evseconold == "modbusevse" && $ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/serial0" && $mpm3pmllidold == "105") echo "selected" ?> value="modbusevse">openWB series1/2 mit geeichtem Zähler v2</option>
									<option <?php if($evseconold == "buchse") echo "selected" ?> value="buchse">openWB mit Buchse</option>
									<option <?php if($evseconold == "masterethframer") echo "selected" ?> value="masterethframer">openWB Ladepunkt in Verbindung mit Standalone</option>
									<option <?php if($evseconold == "ipevse") echo "selected" ?> value="ipevse">openWB Satellit </option>
									<option <?php if($evseconold == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
									<option <?php if($evseconold == "dac") echo "selected" ?> value="dac">DAC</option>
									<option <?php if($evseconold == "httpevse") echo "selected" ?> value="httpevse">HTTP</option>
									<option <?php if($evseconold == "modbusevse" && !($ladeleistungmodulold == "mpm3pmll" && $mpm3pmllsourceold == "/dev/ttyUSB0" && ($mpm3pmllidold == "5" || $mpm3pmllidold == "105"))) echo "selected" ?> value="modbusevse">Modbusevse</option>
									<option <?php if($evseconold == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									<option <?php if($evseconold == "goe") echo "selected" ?> value="goe">Go-e</option>
									<option <?php if($evseconold == "nrgkick") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
									<option <?php if($evseconold == "twcmanager") echo "selected" ?> value="twcmanager">Tesla TWC mit TWCManager</option>
									<option <?php if($evseconold == "keba") echo "selected" ?> value="keba">Keba</option>
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
							<input type="hidden" name="mpm3pmllid" value="5">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2.
							</div>
						</div>
						<div id="openwbbuchse" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="llbuchse">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option für die openWB mit Buchse.
							</div>
						</div>
						<div id="openwb12mid" class="hide">
							<!-- default values for openwb12mid -->
							<input type="hidden" name="modbusevseid" value="1">
							<input type="hidden" name="ladeleistungmodul" value="mpm3pmll">
							<input type="hidden" name="mpm3pmllsource" value="/dev/ttyUSB0">
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
											Alternativ rauszufinden bei angeschlossenem MCP auf der shell mit dem Befehl: "sudo i2cdetect -y 1"
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
						<div id="evsecontwcmanager" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="twcmanagerlp1">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="twcmanagerlp1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="twcmanagerlp1ip" id="twcmanagerlp1ip" value="<?php echo $twcmanagerlp1ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="twcmanagerlp1phasen" class="col-md-4 col-form-label">Anzahl Phasen</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="3" step="1" name="twcmanagerlp1phasen" id="twcmanagerlp1phasen" value="<?php echo $twcmanagerlp1phasenold ?>">
										<span class="form-text small">Definiert die genutzte Anzahl der Phasen zur korrekten Errechnung der Ladeleistung (BETA).</span>
									</div>
								</div>
							</div>
						</div>
						<div id="evsecongoe" class="hide">
							<input type="hidden" name="ladeleistungmodul" value="goelp1">
							<div class="form-group">
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
										<option <?php if($ladeleistungmodulold == "sdm630modbusll") echo "selected" ?> value="sdm630modbusll">SDM 630 Modbus</option>
										<option <?php if($ladeleistungmodulold == "smaemd_ll") echo "selected" ?> value="smaemd_ll">SMA Energy Meter</option>
										<option <?php if($ladeleistungmodulold == "sdm120modbusll") echo "selected" ?> value="sdm120modbusll">SDM 120 Modbus</option>
										<option <?php if($ladeleistungmodulold == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">Simple EVSE Wifi</option>
										<option <?php if($ladeleistungmodulold == "mpm3pmll") echo "selected" ?> value="mpm3pmll">MPM3PM</option>
										<option <?php if($ladeleistungmodulold == "fsm63a3modbusll") echo "selected" ?> value="fsm63a3modbusll">FSM63A3 Modbus</option>
										<option <?php if($ladeleistungmodulold == "httpll") echo "selected" ?> value="httpll">HTTP</option>
										<option <?php if($ladeleistungmodulold == "mpm3pmtripple") echo "selected" ?> value="mpm3pmtripple">openWB Tripple</option>
										<option <?php if($ladeleistungmodulold == "mpm3pmlllp1") echo "selected" ?> value="mpm3pmlllp1">openWB Satellit</option>
										<option <?php if($ladeleistungmodulold == "mqttll") echo "selected" ?> value="mqttll">MQTT</option>
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
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3" id="sdm120modbusllid3" value="<?php echo $sdm120modbusllid3old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase.</span>
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
							<div id="llsma" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="smaemdllid" class="col-md-4 col-form-label">Seriennummer</label>
										<div class="col">
											<input class="form-control" type="text" name="smaemdllid" id="smaemdllid" value="<?php echo $smaemdllidold ?>">
											<span class="form-text small">
												Gültige Werte: Seriennummer. Hier die Seriennummer des SMA Meter für die Ladeleistung angeben.
											</span>
										</div>
									</div>
								</div>
							</div>
							<div id="mqttll" class="hide">
								<div class="alert alert-info">
									Keine Konfiguration erforderlich.<br>
									Per MQTT zu schreiben:<br>
									<span class="text-info">openWB/set/lp/1/W</span> Ladeleistung in Watt, int, positiv<br>
									<span class="text-info">openWB/set/lp/1/kWhCounter</span> Zählerstand in kWh, float, Punkt als Trenner, nur positiv
								</div>
							</div>
						</div>

						<hr class="border-primary">
						<div class="form-row mb-1">
							<label for="socmodul" class="col-md-4 col-form-label">SOC Modul</label>
							<div class="col">
								<select name="socmodul" id="socmodul" class="form-control">
									<option <?php if($socmodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<option <?php if($socmodulold == "soc_http") echo "selected" ?> value="soc_http">SoC HTTP</option>
									<option <?php if($socmodulold == "soc_leaf") echo "selected" ?> value="soc_leaf">SoC Nissan Leaf</option>
									<option <?php if($socmodulold == "soc_i3") echo "selected" ?> value="soc_i3">SoC BMW & Mini</option>
									<option <?php if($socmodulold == "soc_zoe") echo "selected" ?> value="soc_zoe">SoC Renault Zoe alt</option>
									<option <?php if($socmodulold == "soc_myrenault") echo "selected" ?> value="soc_myrenault">SoC Renault Zoe MyRenault</option>
									<option <?php if($socmodulold == "soc_evnotify") echo "selected" ?> value="soc_evnotify">SoC EVNotify</option>
									<option <?php if($socmodulold == "soc_tesla") echo "selected" ?> value="soc_tesla">SoC Tesla</option>
									<option <?php if($socmodulold == "soc_carnet") echo "selected" ?> value="soc_carnet">SoC VW Carnet</option>
									<option <?php if($socmodulold == "soc_zerong") echo "selected" ?> value="soc_zerong">SoC Zero NG</option>
									<option <?php if($socmodulold == "soc_audi") echo "selected" ?> value="soc_audi">SoC Audi</option>
									<option <?php if($socmodulold == "soc_mqtt") echo "selected" ?> value="soc_mqtt">MQTT</option>
									<option <?php if($socmodulold == "soc_bluelink") echo "selected" ?> value="soc_bluelink">Hyundai Bluelink</option>
									<option <?php if($socmodulold == "soc_kia") echo "selected" ?> value="soc_kia">Kia</option>
									<option <?php if($socmodulold == "soc_volvo") echo "selected" ?> value="soc_volvo">Volvo</option>
								</select>
							</div>
						</div>
						<div id="socmodullp1" class="hide">
							<div class="form-group">
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
										<label for="soc_tesla_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_tesla_password" id="soc_tesla_password" value="<?php echo $soc_tesla_passwordold ?>">
											<span class="form-text small">
												Password des Tesla Logins. Das Passwort wird nur bei der ersten Einrichtung verwendet. Sobald die Anmeldung erfolgreich war, wird die Anmeldung über Token geregelt und das Passwort durch "#TokenInUse#" ersetzt.<br>
												Wird bei Tesla direkt das Passwort geändert, kann die WB sich nicht mehr anmelden und es muss hier wieder einmalig das aktuelle Passwort eingetragen werden.<br>
												Wenn das Eingabefeld geleert wird, dann werden auch die Anmeldetoken komplett entfernt.
											</span>
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
							</div>
							<div id="socmbluelink" class="hide">
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
										<label for="soc_bluelink_pin" class="col-md-4 col-form-label">PIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_bluelink_pin" id="soc_bluelink_pin" value="<?php echo $soc_bluelink_pinold ?>">
											<span class="form-text small">
												PIN des Accounts.
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
								</div>
							</div>
							<div id="socmkia" class="hide">
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="soc_vin" class="col-md-4 col-form-label">VIN</label>
										<div class="col">
											<input class="form-control" type="text" name="soc_vin" id="soc_vin" value="<?php echo $soc_vinold ?>">
											<span class="form-text small">
												VIN des Autos.
											</span>
										</div>
									</div>
								</div>
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
								</div>
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
						</div>
					</div>
					<script>
						// visibility of charge point types
						function display_lp1() {
							hideSection('llmodullp1');
							hideSection('evsecondac');
							hideSection('evseconmod');
							hideSection('evseconswifi');
							hideSection('evsecongoe');
							hideSection('evseconnrgkick');
							hideSection('evseconmastereth');
							hideSection('evseconkeba');
							hideSection('openwb12');
							hideSection('openwb12mid');
							hideSection('openwb12v2mid');
							hideSection('evseconhttp');
							hideSection('evsecontwcmanager');
							hideSection('evseconipevse');
							hideSection('openwbbuchse');
							hideSection('evseconextopenwb');

							if($('#evsecon').val() == 'modbusevse') {
								switch( $("#evsecon option:selected" ).text() ){
									case "openWB series1/2":
										showSection('openwb12');
									break;
									case "openWB series1/2 mit geeichtem Zähler":
										showSection('openwb12mid');
									break;
									case "openWB series1/2 mit geeichtem Zähler v2":
										showSection('openwb12v2mid');
									break;
									default:
										showSection('evseconmod');
										showSection('llmodullp1');
										display_llmp1();
								}
							}
							if($('#evsecon').val() == 'ipevse') {
								showSection('evseconipevse');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'extopenwb') {
								showSection('evseconextopenwb');
							}
							if($('#evsecon').val() == 'buchse') {
								showSection('openwbbuchse');
							}
							if($('#evsecon').val() == 'dac') {
								showSection('evsecondac');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'simpleevsewifi') {
								showSection('evseconswifi');
							}
							if($('#evsecon').val() == 'httpevse') {
								showSection('evseconhttp');
								showSection('llmodullp1');
								display_llmp1();
							}
							if($('#evsecon').val() == 'goe') {
								showSection('evsecongoe');
							}
							if($('#evsecon').val() == 'masterethframer') {
								showSection('evseconmastereth');
							}
							if($('#evsecon').val() == 'nrgkick') {
								showSection('evseconnrgkick');
							}
							if($('#evsecon').val() == 'keba') {
								showSection('evseconkeba');
							}
							if($('#evsecon').val() == 'twcmanager') {
								showSection('evsecontwcmanager');
							}
							if($('#evsecon').val() == 'ipevse') {
								showSection('evseconipevse');
							}
						}

						// visibility of meter modules
						function display_llmp1() {
							hideSection('llmnone');
							hideSection('llmsdm');
							hideSection('llmpm3pm');
							hideSection('llswifi');
							hideSection('llsma');
							hideSection('sdm120div');
							hideSection('rs485lanlp1');
							hideSection('llmfsm');
							hideSection('httpll');
							hideSection('mpm3pmlllp1div');
							hideSection('mqttll');

							if($('#ladeleistungmodul').val() == 'mpm3pmlllp1') {
								showSection('mpm3pmlllp1div');
								hideSection('rs485lanlp1'); // BUG hide/show typo?
							}
							if($('#ladeleistungmodul').val() == 'none') {
								showSection('llmnone');
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmtripple') {
								showSection('llmnone');
							}
							if($('#ladeleistungmodul').val() == 'httpll') {
								showSection('httpll');
							}
							if($('#ladeleistungmodul').val() == 'sdm630modbusll') {
								showSection('llmsdm');
								showSection('rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'smaemd_ll') {
								showSection('llsma');
							}
							if($('#ladeleistungmodul').val() == 'sdm120modbusll') {
								showSection('sdm120div');
								showSection('rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'simpleevsewifi') {
								showSection('llswifi');
							}
							if($('#ladeleistungmodul').val() == 'mpm3pmll') {
								showSection('llmpm3pm');
								showSection('rs485lanlp1');
							}
							if($('#ladeleistungmodul').val() == 'fsm63a3modbusll') {
								showSection('rs485lanlp1');
								showSection('llmfsm');
							}
							if($('#ladeleistungmodul').val() == 'mqttll') {
								showSection('mqttll');
							}
						}

						// visibility of soc modules
						function display_socmodul() {
							hideSection('socmodullp1');
							hideSection('socmnone');
							hideSection('socmhttp');
							hideSection('socleaf');
							hideSection('soci3');
							hideSection('soczoe');
							hideSection('socevnotify');
							hideSection('socmtesla');
							hideSection('soccarnet');
							hideSection('socmzerong');
							hideSection('socmaudi');
							hideSection('socmqtt');
							hideSection('socmbluelink');
							hideSection('socmkia');
							hideSection('socmuser');
							hideSection('socmpass');
							hideSection('socmyrenault');

							if($('#socmodul').val() == 'none') {
								showSection('socmnone');
							} else {
								showSection('socmodullp1', false); // do not enable all input child-elements!
							}
							if($('#socmodul').val() == 'soc_volvo') {
								showSection('socmuser');
								showSection('socmpass');
							}
							if($('#socmodul').val() == 'soc_mqtt') {
								showSection('socmqtt');
							}
							if($('#socmodul').val() == 'soc_bluelink') {
								showSection('socmbluelink');
							}
							if($('#socmodul').val() == 'soc_kia') {
								showSection('socmkia');
								showSection('socmbluelink');
							}
							if($('#socmodul').val() == 'soc_audi') {
								showSection('socmaudi');
							}
							if($('#socmodul').val() == 'soc_myrenault') {
								showSection('socmyrenault');
							}
							if($('#socmodul').val() == 'soc_http') {
								showSection('socmhttp');
							}
							if($('#socmodul').val() == 'soc_zerong') {
								showSection('socmzerong');
							}
							if($('#socmodul').val() == 'soc_leaf') {
								showSection('socleaf');
							}
							if($('#socmodul').val() == 'soc_i3') {
								showSection('soci3');
							}
							if($('#socmodul').val() == 'soc_zoe') {
								showSection('soczoe');
							}
							if($('#socmodul').val() == 'soc_evnotify') {
								showSection('socevnotify');
							}
							if($('#socmodul').val() == 'soc_tesla') {
								showSection('socmtesla');
							}
							if($('#socmodul').val() == 'soc_carnet') {
								showSection('soccarnet');
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
									<!-- WARNING: the text value of the "openWB series1/2 XXX" options is checked later in the script section -->
									<option <?php if($evsecons1old == "modbusevse" && $ladeleistungs1modulold == "mpm3pmlls1" && $mpm3pmlls1sourceold == "/dev/ttyUSB1" && $mpm3pmlls1idold == "6") echo "selected" ?> value="modbusevse">openWB series1/2 Duo</option>
									<option <?php if($evsecons1old == "slaveeth") echo "selected" ?> value="slaveeth">openWB Slave</option>
									<option <?php if($evsecons1old == "ipevse") echo "selected" ?> value="ipevse">openWB Satellit</option>
									<option <?php if($evsecons1old == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
									<option <?php if($evsecons1old == "modbusevse" && !($ladeleistungs1modulold == "mpm3pmlls1" && $mpm3pmlls1sourceold == "/dev/ttyUSB1" && $mpm3pmlls1idold == "6")) echo "selected" ?> value="modbusevse">Modbus</option>
									<option <?php if($evsecons1old == "dac") echo "selected" ?> value="dac">DAC</option>
									<option <?php if($evsecons1old == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									<option <?php if($evsecons1old == "goe") echo "selected" ?> value="goe">Go-e</option>
									<option <?php if($evsecons1old == "nrgkick") echo "selected" ?> value="nrgkick">NRGKick + Connect</option>
									<option <?php if($evsecons1old == "keba") echo "selected" ?> value="keba">Keba</option>
								</select>
							</div>
						</div>
						<div id="evseconextopenwblp2" class="hide">
							<input type="hidden" name="ladeleistungs1modul" value="extopenwblp2">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="lp2id" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lp2id" id="lp2id" value="<?php echo $chargep2ipold ?>">
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
						<div id="openwb12s1" class="hide">
							<input type="hidden" name="evseids1" value="1">
							<input type="hidden" name="ladeleistungs1modul" value="mpm3pmlls1">
							<input type="hidden" name="mpm3pmlls1source" value="/dev/ttyUSB1">
							<input type="hidden" name="mpm3pmlls1id" value="6">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Dies ist die richtige Option, sowohl für Bausatz als auch für fertige openWB series1 oder series2.
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
										<option <?php if($ladeleistungs1modulold == "sdm630modbuslls1") echo "selected" ?> value="sdm630modbuslls1">SDM 630 Modbus</option>
										<option <?php if($ladeleistungs1modulold == "sdm120modbuslls1") echo "selected" ?> value="sdm120modbuslls1">SDM 120 Modbus</option>
										<option <?php if($ladeleistungs1modulold == "simpleevsewifis1") echo "selected" ?> value="simpleevsewifis1">Simple EVSE Wifi</option>
										<option <?php if($ladeleistungs1modulold == "mpm3pmlls1") echo "selected" ?> value="mpm3pmlls1">MPM3PM Modbus</option>
										<option <?php if($ladeleistungs1modulold == "goelp2") echo "selected" ?> value="goelp2">Go-e</option> <!-- BUG go-E als LL-Modul? -->
										<option <?php if($ladeleistungs1modulold == "mpm3pmtripplelp2") echo "selected" ?> value="mpm3pmtripplelp2">openWB Tripple</option>
										<option <?php if($ladeleistungs1modulold == "mpm3pmlllp2") echo "selected" ?> value="mpm3pmlllp2">openWB Satelit</option>
									</select>
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
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der zweiten Phase.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="sdm120modbusllid3s1" class="col-md-4 col-form-label">ID Phase 3</label>
										<div class="col">
											<input class="form-control" type="number" min="1" max="254" step="1" name="sdm120modbusllid3s1" id="sdm120modbusllid3s1" value="<?php echo $sdm120modbusllid3s1old ?>">
											<span class="form-text small">Gültige Werte 1-254. Modbus ID des SDM der dritten Phase.</span>
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
									<option <?php if($socmodul1old == "soc_http1") echo "selected" ?> value="soc_http1">SoC HTTP</option>
									<option <?php if($socmodul1old == "soc_leafs1") echo "selected" ?> value="soc_leafs1">SoC Nissan Leaf</option>
									<option <?php if($socmodul1old == "soc_i3s1") echo "selected" ?> value="soc_i3s1">SoC BMW i3</option>
									<option <?php if($socmodul1old == "soc_evnotifys1") echo "selected" ?> value="soc_evnotifys1">SoC EVNotify</option>
									<option <?php if($socmodul1old == "soc_zoelp2") echo "selected" ?> value="soc_zoelp2">SoC Zoe alt</option>
									<option <?php if($socmodul1old == "soc_myrenaultlp2") echo "selected" ?> value="soc_myrenaultlp2">SoC MyRenault</option>
									<option <?php if($socmodul1old == "soc_teslalp2") echo "selected" ?> value="soc_teslalp2">SoC Tesla</option>
									<option <?php if($socmodul1old == "soc_carnetlp2") echo "selected" ?> value="soc_carnetlp2">SoC VW Carnet</option>
									<option <?php if($socmodul1old == "soc_zeronglp2") echo "selected" ?> value="soc_zeronglp2">SoC Zero NG</option>
									<option <?php if($socmodul1old == "soc_mqtt") echo "selected" ?> value="soc_mqtt">MQTT</option>
									<option <?php if($socmodul1old == "soc_audilp2") echo "selected" ?> value="soc_audilp2">Audi</option>
									<option <?php if($socmodul1old == "soc_bluelinklp2") echo "selected" ?> value="soc_bluelinklp2">Hyundai Bluelink</option>
								</select>
							</div>
						</div>
						<div id="socmodullp2" class="hide">
							<!-- soc is always requested, ignoring plug stat -->
							<div id="socmnone1" class="hide">
								<!-- nothing here -->
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
										<label for="soc_teslalp2_password" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="soc_teslalp2_password" id="soc_teslalp2_password" value="<?php echo $soc_teslalp2_passwordold ?>">
											<span class="form-text small">
												Password des Tesla Logins. Das Passwort wird nur bei der ersten Einrichtung verwendet. Sobald die Anmeldung erfolgreich war, wird die Anmeldung über Token geregelt und das Passwort durch "#TokenInUse#" ersetzt.<br>
												Wird bei Tesla direkt das Passwort geändert, kann die WB sich nicht mehr anmelden und es muss hier wieder einmalig das aktuelle Passwort eingetragen werden.<br>
												Wenn das Eingabefeld geleert wird, dann werden auch die Anmeldetoken komplett entfernt.
											</span>
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
											<input class="form-control" type="text" name="soc2pin" id="soc2pin" value="<?php echo $soc2pinold ?>">
											<span class="form-text small">
												PIN des Accounts.
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						function display_lp2() {
							hideSection('evsecondacs1');
							hideSection('evseconmbs1');
							hideSection('evseconswifis1');
							hideSection('llmodullp2');
							hideSection('evsecongoes1');
							hideSection('evsecoslaveeth');
							hideSection('evseconkebas1');
							hideSection('evseconnrgkicks1');
							hideSection('openwb12s1');
							hideSection('evseconextopenwblp2');
							hideSection('evseconipevselp2');

							if($('#evsecons1').val() == 'modbusevse') {
								switch( $("#evsecons1 option:selected" ).text() ){
									case "openWB series1/2 Duo":
										showSection('openwb12s1');
									break;
									default:
										showSection('evseconmbs1');
										showSection('llmodullp2');
										display_llmp2();
								}
							}
							if($('#evsecons1').val() == 'ipevse') {
								showSection('evseconipevselp2');
								showSection('llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'dac') {
								showSection('evsecondacs1');
								showSection('llmodullp2');
								display_llmp2();
							}
							if($('#evsecons1').val() == 'simpleevsewifi') {
								showSection('evseconswifis1');
							}
							if($('#evsecons1').val() == 'extopenwb') {
								showSection('evseconextopenwblp2');
							}
							if($('#evsecons1').val() == 'goe') {
								showSection('evsecongoes1');
							}
							if($('#evsecons1').val() == 'slaveeth') {
								showSection('evsecoslaveeth');
							}
							if($('#evsecons1').val() == 'keba') {
								showSection('evseconkebas1');
							}
							if($('#evsecons1').val() == 'nrgkick') {
								showSection('evseconnrgkicks1');
							}
						}

						function display_llmp2() {
							hideSection('sdm630s1div');
							hideSection('sdm120s1div');
							hideSection('swifis1div');
							hideSection('mpm3pmlls1div');
							hideSection('rs485lanlp2');
							hideSection('mpm3pmlllp2div');

							if($('#ladeleistungs1modul').val() == 'sdm630modbuslls1') {
								showSection('sdm630s1div');
								showSection('rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'sdm120modbuslls1') {
								showSection('sdm120s1div');
								showSection('rs485lanlp2');
							}
							if($('#ladeleistungs1modul').val() == 'simpleevsewifis1') {
								showSection('swifis1div');
							}
							if($('#ladeleistungs1modul').val() == 'goelp2') {
								showSection('swifis1div');
							}
							if($('#ladeleistungs1modul').val() == 'mpm3pmlllp2') {
								showSection('mpm3pmlllp2div');
								hideSection('rs485lanlp2'); // BUG show/hide typo?
							}
							if($('#ladeleistungs1modul').val() == 'mpm3pmlls1') {
								showSection('mpm3pmlls1div');
								showSection('rs485lanlp2');
							}
						}

						function display_socmodul1() {
							hideSection('socmodullp2');
							hideSection('socmqtt1');
							hideSection('socmuser2');
							hideSection('socmpass2');
							hideSection('socmpin2');
							hideSection('socmnone1');
							hideSection('socmhttp1');
							hideSection('socleaf1');
							hideSection('soci31');
							hideSection('socevnotifylp2');
							hideSection('soczoelp2');
							hideSection('socmteslalp2');
							hideSection('socmyrenaultlp2');
							hideSection('soccarnetlp2');
							hideSection('socmzeronglp2');

							if($('#socmodul1').val() == 'none') {
								showSection('socmnone1');
							} else {
								showSection('socmodullp2', false); // do not enable all input child-elements!
							}
							if($('#socmodul1').val() == 'soc_mqtt') {
								showSection('socmqtt1');
							}
							if($('#socmodul1').val() == 'soc_http1') {
								showSection('socmhttp1');
							}
							if($('#socmodul1').val() == 'soc_audilp2') {
								showSection('socmuser2');
								showSection('socmpass2');
							}
							if($('#socmodul1').val() == 'soc_bluelinklp2') {
								showSection('socmuser2');
								showSection('socmpass2');
								showSection('socmpin2');
							}
							if($('#socmodul1').val() == 'soc_leafs1') {
								showSection('socleaf1');
							}
							if($('#socmodul1').val() == 'soc_myrenaultlp2') {
								showSection('socmyrenaultlp2');
							}
							if($('#socmodul1').val() == 'soc_i3s1') {
								showSection('soci31');
							}
							if($('#socmodul1').val() == 'soc_evnotifys1') {
								showSection('socevnotifylp2');
							}
							if($('#socmodul1').val() == 'soc_zoelp2') {
								showSection('soczoelp2');
							}
							if($('#socmodul1').val() == 'soc_carnetlp2') {
								showSection('soccarnetlp2');
							}
							if($('#socmodul1').val() == 'soc_teslalp2') {
								showSection('socmteslalp2');
							}
							if($('#socmodul1').val() == 'soc_zeronglp2') {
								showSection('socmzeronglp2');
							}
						}

						function display_lastmanagement() {
							if($('#lastmanagementOff').prop("checked")) {
								hideSection('lastmman');
								hideSection('durchslp2');
								hideSection('nachtls1div');
							}
							else {
								showSection('lastmman');
								showSection('durchslp2');
								showSection('nachtls1div');
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
									<option <?php if($evsecons2old == "thirdeth") echo "selected" ?> value="thirdeth">openWB dritter Ladepunkt</option>
									<option <?php if($evsecons2old == "ipevse") echo "selected" ?> value="ipevse">openWB Satellit</option>
									<option <?php if($evsecons2old == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
									<option <?php if($evsecons2old == "modbusevse") echo "selected" ?> value="modbusevse">Modbus</option>
									<option <?php if($evsecons2old == "dac") echo "selected" ?> value="dac">DAC</option>
									<option <?php if($evsecons2old == "simpleevsewifi") echo "selected" ?> value="simpleevsewifi">SimpleEVSEWifi</option>
									<option <?php if($evsecons2old == "goe") echo "selected" ?> value="goe">Go-e</option>
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
								<label for="ladeleistungss2modul" class="col-md-4 col-form-label">Ladeleistungmodul</label>
								<div class="col">
									<select name="ladeleistungss2modul" id="ladeleistungss2modul" class="form-control">
										<option <?php if($ladeleistungs2modulold == "sdm630modbuslls2") echo "selected" ?> value="sdm630modbuslls2">SDM 630 Modbus</option>
										<option <?php if($ladeleistungs2modulold == "sdm120modbuslls2") echo "selected" ?> value="sdm120modbuslls2">SDM 120 Modbus</option>
										<option <?php if($ladeleistungs2modulold == "mpm3pmlls2") echo "selected" ?> value="mpm3pmlls2">MPM3PM Modbus</option>
										<option <?php if($ladeleistungs2modulold == "simpleevsewifis2") echo "selected" ?> value="simpleevsewifis2">Simple EVSE Wifi</option>
										<option <?php if($ladeleistungs2modulold == "goelp3") echo "selected" ?> value="goelp3">Go-E</option> <!-- BUG go-E als LL-Modul? -->
										<option <?php if($ladeleistungs2modulold == "mpm3pmtripplelp3") echo "selected" ?> value="mpm3pmtripplelp3">openWB Tripple</option>
										<option <?php if($ladeleistungs2modulold == "mpm3pmlllp3") echo "selected" ?> value="mpm3pmlllp3">openWB Satellit</option>
									</select>
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
								hideSection('lasts2mman');
							}
							else {
								showSection('lasts2mman');
								display_lp3();
							}
						}

						function display_lp3 () {
							hideSection('evsecondacs2');
							hideSection('evseconmbs2');
							hideSection('evseconswifis2');
							hideSection('llmodullp3');
							hideSection('evsecongoes2');
							hideSection('evseconipevselp3');
							hideSection('evseconextopenwblp3');
							hideSection('evseconthirdeth');

							if($('#evsecons2').val() == 'thirdeth') {
								showSection('evseconthirdeth');
							}
							if($('#evsecons2').val() == 'dac') {
								showSection('evsecondacs2');
								showSection('llmodullp3');
								display_llmp3();
							}
							if($('#evsecons2').val() == 'modbusevse') {
								showSection('evseconmbs2');
								showSection('llmodullp3');
								display_llmp3();
							}
							if($('#evsecons2').val() == 'simpleevsewifi') {
								showSection('evseconswifis2');
							}
							if($('#evsecons2').val() == 'extopenwb') {
								showSection('evseconextopenwblp3');
							}
							if($('#evsecons2').val() == 'goe') {
								showSection('evsecongoes2');
							}
							if($('#evsecons2').val() == 'ipevse') {
								showSection('evseconipevselp3');
								showSection('llmodullp3');
								display_llmp3();
							}
						}

						function display_llmp3 () {
							hideSection('sdm630s2div');
							hideSection('sdm120s2div');
							hideSection('swifis2div');
							hideSection('rs485lanlp3');
							hideSection('mpm3pmlls2div');
							hideSection('mpm3pmlllp3div');


							if($('#ladeleistungss2modul').val() == 'mpm3pmlllp3') {
								showSection('mpm3pmlllp3div');
								showSection('rs485lanlp3');
							}
							if($('#ladeleistungss2modul').val() == 'sdm630modbuslls2') {
								showSection('sdm630s2div');
								showSection('rs485lanlp3');
							}
							if($('#ladeleistungss2modul').val() == 'sdm120modbuslls2') {
								showSection('sdm120s2div');
								showSection('rs485lanlp3');
							}
							if($('#ladeleistungss2modul').val() == 'simpleevsewifis2') {
								showSection('swifis2div');
							}
							if($('#ladeleistungss2modul').val() == 'goelp3') {
								showSection('swifis2div');
							}
							if($('#ladeleistungss2modul').val() == 'mpm3pmlls2') {
								showSection('mpm3pmlls2div');
								showSection('rs485lanlp3');
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

							$('#ladeleistungss2modul').change( function(){
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
										<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "ipevse") echo "selected" ?> value="ipevse">openWB Satellit</option>
										<option <?php if(${'evseconlp'.$chargepointNum.'old'} == "extopenwb") echo "selected" ?> value="extopenwb">externe openWB</option>
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
								hideSection('evseconipevselp<?php echo $chargepointNum; ?>');
								hideSection('evseconextopenwblp<?php echo $chargepointNum; ?>');

								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'extopenwb') {
									showSection('evseconextopenwblp<?php echo $chargepointNum; ?>');
								}
								if($('#evseconlp<?php echo $chargepointNum; ?>').val() == 'ipevse') {
									showSection('evseconipevselp<?php echo $chargepointNum; ?>');
								}
							}

							function display_lastmanagementlp<?php echo $chargepointNum; ?>() {
								if($('#lastmanagementlp<?php echo $chargepointNum; ?>Off').prop("checked")) {
									hideSection('lastlp<?php echo $chargepointNum; ?>mman');
								}
								else {
									showSection('lastlp<?php echo $chargepointNum; ?>mman');
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
