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
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20201231" ></script>
		<script>
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
			<h1>Modulkonfiguration Batteriespeicher</h1>
			<form action="./tools/saveconfig.php" method="POST">

				<!-- Speicher -->
				<div class="card border-warning">
					<div class="card-header bg-warning">
						Speicher-Modul
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="speichermodul" class="col-md-4 col-form-label">Speicher-Modul</label>
							<div class="col">
								<select name="speichermodul" id="speichermodul" class="form-control">
									<option <?php if($speichermodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<optgroup label="openWB">
										<option <?php if($speichermodulold == "speicher_mpm3pm") echo "selected" ?> value="speicher_mpm3pm">openWB Speicher Kit</option>
									</optgroup>
									<optgroup label="andere Hersteller">
										<option <?php if($speichermodulold == "speicher_alphaess") echo "selected" ?> value="speicher_alphaess">Alpha ESS</option>
										<option <?php if($speichermodulold == "speicher_bydhv") echo "selected" ?> value="speicher_bydhv">BYD</option>
										<option <?php if($speichermodulold == "speicher_e3dc") echo "selected" ?> value="speicher_e3dc">E3DC Speicher</option>
										<option <?php if($speichermodulold == "speicher_fronius") echo "selected" ?> value="speicher_fronius">Fronius Speicher (Solar Battery oder BYD HV/HVS/HVM)</option>
										<option <?php if($speichermodulold == "speicher_kostalplenticore") echo "selected" ?> value="speicher_kostalplenticore">Kostal Plenticore mit Speicher</option>
										<option <?php if($speichermodulold == "speicher_lgessv1") echo "selected" ?> value="speicher_lgessv1">LG ESS 1.0VI</option>
										<option <?php if($speichermodulold == "speicher_fems") echo "selected" ?> value="speicher_fems">openEMS / Fenecon FEMS / Kaco Hy-Control</option>
										<option <?php if($speichermodulold == "speicher_rct") echo "selected" ?> value="speicher_rct">RCT</option>
										<option <?php if($speichermodulold == "speicher_siemens") echo "selected" ?> value="speicher_siemens">Siemens</option>
										<option <?php if($speichermodulold == "speicher_sbs25") echo "selected" ?> value="speicher_sbs25">SMA Sunny Boy Storage</option>
										<option <?php if($speichermodulold == "speicher_sunnyisland") echo "selected" ?> value="speicher_sunnyisland">SMA Sunny Island</option>
										<option <?php if($speichermodulold == "speicher_solaredge") echo "selected" ?> value="speicher_solaredge">Solaredge Speicher</option>
										<option <?php if($speichermodulold == "speicher_solarwatt") echo "selected" ?> value="speicher_solarwatt">Solarwatt My Reserve</option>
										<option <?php if($speichermodulold == "speicher_solax") echo "selected" ?> value="speicher_solax">Solax Speicher</option>
										<option <?php if($speichermodulold == "speicher_sonneneco") echo "selected" ?> value="speicher_sonneneco">Sonnen eco</option>
										<option <?php if($speichermodulold == "speicher_studer") echo "selected" ?> value="speicher_studer">Studer-Innotec System</option>
										<option <?php if($speichermodulold == "speicher_sungrow") echo "selected" ?> value="speicher_sungrow">Sungrow Hybrid</option>
										<option <?php if($speichermodulold == "speicher_powerwall") echo "selected" ?> value="speicher_powerwall">Tesla Powerwall</option>
										<option <?php if($speichermodulold == "speicher_tesvoltsma") echo "selected" ?> value="speicher_tesvoltsma">Tesvolt mit SMA</option>
										<option <?php if($speichermodulold == "speicher_varta") echo "selected" ?> value="speicher_varta">Varta Element u.a.</option>
										<option <?php if($speichermodulold == "speicher_victron") echo "selected" ?> value="speicher_victron">Victron Speicher (GX o.ä.)</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($speichermodulold == "speicher_http") echo "selected" ?> value="speicher_http">HTTP Abfrage</option>
										<option <?php if($speichermodulold == "speicher_json") echo "selected" ?> value="speicher_json">JSON Abfrage BETA!!!!</option>
										<option <?php if($speichermodulold == "mpm3pmspeicher") echo "selected" ?> value="mpm3pmspeicher">MPM3PM</option>
										<option <?php if($speichermodulold == "speicher_mqtt") echo "selected" ?> value="speicher_mqtt">MQTT</option>
									</optgroup>
								</select>
							</div>
						</div>

						<div id="divspeicherlgessv1" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="lgessv1ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="lgessv1ip" id="lgessv1ip" value="<?php echo $lgessv1ipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="lgessv1pass" class="col-md-4 col-form-label">Password</label>
									<div class="col">
										<input class="form-control" type="password" name="lgessv1pass" id="lgessv1pass" value="<?php echo $lgessv1passold ?>">
										<span class="form-text small">
											Standardmäßig ist hier die Registrierungsnummer des LG ESS 1.0VI anzugeben.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="ess_api_ver" class="col-md-4 col-form-label">API-Version</label>
									<div class="col">
										<select name="ess_api_ver" id="ess_api_ver" class="form-control">
											<option <?php if($ess_api_verold == "10.2019") echo "selected" ?> value="10.2019">API-Version Oktober 2019</option>
											<option <?php if($ess_api_verold == "01.2020") echo "selected" ?> value="01.2020">API-Version Januar 2020</option>
										</select>
										<span class="form-text small">
											Falls Sie nicht wissen, welche API-Version benötigen, benutzten Sie bitte die neueste API-Version.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherkit" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicherkitversion" class="col-md-4 col-form-label">Version des openWB Speicher Kits</label>
									<div class="col">
										<select name="speicherkitversion" id="speicherkitversion" class="form-control">
											<option <?php if($speicherkitversionold == 0) echo "selected" ?> value="0">Dreiphasig (MPM3PM)</option>
											<option <?php if($speicherkitversionold == 1) echo "selected" ?> value="1">Einphasig (SDM120)</option>
										</select>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichermqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/houseBattery/W</span> Speicherleistung in Watt, int, positiv Ladung, negativ Entladung<br>
								<span class="text-info">openWB/set/houseBattery/WhImported</span> Geladene Energie in Wh, float, nur positiv<br>
								<span class="text-info">openWB/set/houseBattery/WhExported</span> Entladene Energie in Wh, float, nur positiv<br>
								<span class="text-info">openWB/set/houseBattery/%Soc</span> Ladestand des Speichers, int, 0-100
							</div>
						</div>

						<div id="divspeichervictron" class="hide">
							<div class="alert alert-info">
								Konfiguration im Bezug Victron Modul.
							</div>
						</div>

						<div id="divspeicherstuder" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="studer_ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="studer_ip" id="studer_ip" value="<?php echo $studer_ipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
							<div class="alert alert-info">
								Hier bitte die IP Adresse des ModbusGateway's eintragen.
							</div>
						</div>
						
						<div id="divspeicherfems" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="multifems" class="col-md-4 col-form-label">Anzahl der verbauten Speicher</label>
									<div class="col">
										<select name="multifems" id="multifems" class="form-control">
											<option <?php if($multifemsold == 0) echo "selected" ?> value="0">Ein Speicher vorhanden</option>
											<option <?php if($multifemsold == 1) echo "selected" ?> value="1">Zwei Speicher vorhanden</option>
										</select>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherip" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicher1_ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="speicher1_ip" id="speicher1_ip" value="<?php echo $speicher1_ipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersiemens" class="hide">
							<div class="alert alert-info">
								Im Siemens Speicher muss als Schnittstelle <span class="text-info">openWB</span> gewählt werden.
							</div>
						</div>

						<div id="divspeichersungrow" class="hide">
							<div class="alert alert-info">
								Es muss Sungrow als PV und EVU Modul gewählt werden.
							</div>
						</div>

						<div id="divspeicherrct" class="hide">
							<div class="alert alert-info">
								Konfiguration im zugehörigen EVU Modul.
							</div>
						</div>

						<div id="divspeichervarta" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="vartaspeicherip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="vartaspeicherip" id="vartaspeicherip" value="<?php echo $vartaspeicheripold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="usevartamodbus" class="col-md-4 col-form-label">Ausleseart Modbus</label>
									<div class="col">
										<select name="usevartamodbus" id="usevartamodbus" class="form-control">
											<option <?php if($usevartamodbusold == "0") echo "selected" ?> value="0">Nein</option>
											<option <?php if($usevartamodbusold == "1") echo "selected" ?> value="1">Ja</option>
										</select>
										<span class="form-text small">Für z.B. Pulse, Element, Neo.</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicheralphaess" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>

						<div id="divspeicherpw" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicherpwip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="speicherpwip" id="speicherpwip" value="<?php echo $speicherpwipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherpwloginneeded" class="col-md-4 col-form-label">Anmeldung erforderlich</label>
									<div class="col">
										<select name="speicherpwloginneeded" id="speicherpwloginneeded" class="form-control">
											<option <?php if($speicherpwloginneededold == "0") echo "selected" ?> value="0">Nein</option>
											<option <?php if($speicherpwloginneededold == "1") echo "selected" ?> value="1">Ja</option>
										</select>
										<span class="form-text small">Ab Version 20.49 stehen die Daten erst nach einer Anmeldung an der Powerwall zur Verfügung. Bei "Ja" müssen auch Benutzername und Passwort angegeben werden.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherpwuser" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherpwuser" id="speicherpwuser" value="<?php echo $speicherpwuserold ?>">
										<span class="form-text small">Benutzername für den lokalen Login auf der Powerwall.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherpwpass" class="col-md-4 col-form-label">Passwort</label>
									<div class="col">
										<input class="form-control" type="password" name="speicherpwpass" id="speicherpwpass" value="<?php echo $speicherpwpassold ?>">
										<span class="form-text small">Passwort für den lokalen Login auf der Powerwall.</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherseco" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sonnenecoip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sonnenecoip" id="sonnenecoip" value="<?php echo $sonnenecoipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sonnenecoalternativ" class="col-md-4 col-form-label">Datenverbindung</label>
									<div class="col">
										<select name="sonnenecoalternativ" id="sonnenecoalternativ" class="form-control">
											<option <?php if($sonnenecoalternativold == "0") echo "selected" ?> value="0">Rest-API 1 (z. B. ECO 4)</option>
											<option <?php if($sonnenecoalternativold == "2") echo "selected" ?> value="2">Rest-API 2 (z. B. ECO 6)</option>
											<option <?php if($sonnenecoalternativold == "1") echo "selected" ?> value="1">JSON-API (z. B. ECO 8)</option>
										</select>
										<span class="form-text small">
											Je nach Sonnen Batterie muss die richtige Datenverbindung ausgewählt werden.
											Folgende URLs werden zum Abruf der Daten genutzt und können auch manuell über einen Browser abgefragt werden, um die richtige Einstellung zu finden:<br>
											Rest-API 1: [ip]:7979/rest/devices/battery<br>
											Rest-API 2: [ip]:7979/rest/devices/battery/M05<br>
											JSON-API: [ip]/api/v1/status
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichere3dc" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="e3dcip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^(none)|((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="e3dcip" id="e3dcip" value="<?php echo $e3dcipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="e3dcextprod" class="col-md-4 col-form-label">Externe Produktion des E3DC mit einbeziehen</label>
									<div class="col">
										<select name="e3dcextprod" id="e3dcextprod" class="form-control">
											<option <?php if($e3dcextprodold == "0") echo "selected" ?> value="0">Nein</option>
											<option <?php if($e3dcextprodold == "1") echo "selected" ?> value="1">Ja</option>
										</select>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="e3dc2ip" class="col-md-4 col-form-label">2. IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^(none)|((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="e3dc2ip" id="e3dc2ip" value="<?php echo $e3dc2ipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											Wenn nicht vorhanden none eintragen.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersbs25" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sbs25ip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sbs25ip" id="sbs25ip" value="<?php echo $sbs25ipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersunnyisland" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sunnyislandip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sunnyislandip" id="sunnyislandip" value="<?php echo $sunnyislandipold ?>">
										<span class="form-text small">Gültige Werte IP Adresse im Format: 192.168.0.12</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersolaredge" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="solaredgespeicherip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaredgespeicherip" id="solaredgespeicherip" value="<?php echo $solaredgespeicheripold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Solaredge Wechselrichters an dem der Speicher angeschlossen ist.
										</span>
									</div>
								</div>
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="solaredgezweiterspeicher" class="col-md-4 col-form-label">Ist ein zweiter Speicher am Wechselrichter angeschlossen?</label>
										<div class="col">
											<select name="solaredgezweiterspeicher" id="solaredgezweiterspeicher" class="form-control">
												<option <?php if($solaredgezweiterspeicherold == 0) echo "selected" ?> value="0">Nein</option>
												<option <?php if($solaredgezweiterspeicherold == 1) echo "selected" ?> value="1">Ja</option>
											</select>
										</div>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichersolax" class="hide">
							<div class="alert alert-info">
								Die IP des Wechselrichters wird im dazugehörigen Solax PV-Modul eingestellt.
							</div>
						</div>

						<div id="divspeicherplenti" class="hide">
							<div class="alert alert-info">
								Ein am 1. Kostal Plenticore angeschlossener Speicher setzt einen EM300/KSEM voraus.
								Nach entsprechender Auswahl im Strombezugsmessmodul und Konfiguration der IP des WR im PV-Modul erfolgt das Auslesen des Speichers über den WR ohne weitere Einstellungen.
							</div>
						</div>

						<div id="divspeicherfronius" class="hide">
							<div class="alert alert-info">
								Die IP des Wechselrichters wird im dazugehörigen Fronius PV-Modul eingestellt.
							</div>
						</div>

						<div id="divspeicherhttp" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="speicherleistung_http" class="col-md-4 col-form-label">Leistung URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherleistung_http" id="speicherleistung_http" value="<?php echo htmlspecialchars($speicherleistung_httpold) ?>">
										<span class="form-text small">
											Gültige Werte URL. Vollständige URL die den aktuellen Leistungswert in Watt wiedergibt.
											Erwartet wird eine Ganzzahl. Positiv heißt Speicher wird geladen und eine negative Zahl bedeutet das der Speicher entladen wird.
											Das Modul dient dazu bei NurPV Ladung eine Entladung des Speichers zu verhindern.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speichersoc_http" class="col-md-4 col-form-label">SoC URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speichersoc_http" id="speichersoc_http" value="<?php echo htmlspecialchars($speichersoc_httpold) ?>">
										<span class="form-text small">
											Gültige Werte URL. Vollständige URL die den aktuellen SoC wiedergibt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherikwh_http" class="col-md-4 col-form-label">Import Wh URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherikwh_http" id="speicherikwh_http" value="<?php echo htmlspecialchars($speicherikwh_httpold) ?>">
										<span class="form-text small">
											Gültige Werte URL. Wenn nicht vorhanden, none eintragen.
											Vollständige URL die den Zählerstand der Batterieladung in WattStunden wiedergibt. Erwartet wird eine Ganzzahl.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="speicherekwh_http" class="col-md-4 col-form-label">Export Wh URL</label>
									<div class="col">
										<input class="form-control" type="text" name="speicherekwh_http" id="speicherekwh_http" value="<?php echo htmlspecialchars($speicherekwh_httpold) ?>">
										<span class="form-text small">
											Gültige Werte URL. Wenn nicht vorhanden, none eintragen.
											Vollständige URL die den Zählerstand der Batterieentladung in WattStunden wiedergibt. Erwartet wird eine Ganzzahl.
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeicherjson" class="hide">
							<div class="form-row mb-1">
								<label for="battjsonurl" class="col-md-4 col-form-label">Speicher URL</label>
								<div class="col">
									<input class="form-control" type="text" name="battjsonurl" id="battjsonurl" value="<?php echo $battjsonurlold ?>">
									<span class="form-text small">
										Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="battjsonwatt" class="col-md-4 col-form-label">Json Abfrage für Watt</label>
								<div class="col">
									<input class="form-control" type="text" name="battjsonwatt" id="battjsonwatt" value="<?php echo htmlspecialchars($battjsonwattold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span>
										So muss hier <span class="text-info">.PowerOut</span> eingetragen werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="battjsonsoc" class="col-md-4 col-form-label">Json Abfrage für SoC</label>
								<div class="col">
									<input class="form-control" type="text" name="battjsonsoc" id="battjsonsoc" value="<?php echo htmlspecialchars($battjsonsocold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span>
										So muss hier <span class="text-info">.PowerProduced</span> eingetragen werden.
									</span>
								</div>
							</div>
						</div>

						<div id="divspeicherbydhv" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="bydhvuser" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<input class="form-control" type="text" name="bydhvuser" id="bydhvuser" value="<?php echo $bydhvuserold ?>">
									</div>
								</div>
								<div class="form-group">
									<div class="form-row mb-1">
										<label for="bydhvpass" class="col-md-4 col-form-label">Passwort</label>
										<div class="col">
											<input class="form-control" type="password" name="bydhvpass" id="bydhvpass" value="<?php echo $bydhvpassold ?>">
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bydhvip" class="col-md-4 col-form-label">IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bydhvip" id="bydhvip" value="<?php echo $bydhvipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
							</div>
						</div>

						<div id="divspeichermpm3pm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="mpm3pmspeichersource" class="col-md-4 col-form-label">Source</label>
									<div class="col">
										<input class="form-control" type="text" name="mpm3pmspeichersource" id="mpm3pmspeichersource" value="<?php echo $mpm3pmspeichersourceold ?>">
										<span class="form-text small">Gültige Werte /dev/ttyUSBx , /dev/virtualcomX bei Verwendung mit Ethernet Modbus.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmspeicherid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmspeicherid" id="mpm3pmspeicherid" value="<?php echo $mpm3pmspeicheridold ?>">
										<span class="form-text small">Gültige Werte 1-254.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmspeicherpv" class="col-md-4 col-form-label">PV mit einberechnen?</label>
									<div class="col">
										<select name="mpm3pmspeicherpv" id="mpm3pmspeicherpv" class="form-control">
											<option <?php if($mpm3pmspeicherpvold == "0") echo "selected" ?> value="0">Keine extra Berechnung</option>
											<option <?php if($mpm3pmspeicherpvold == "1") echo "selected" ?> value="1">Subtrahieren der PV Leistung</option>
										</select>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmspeicherlanip" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpm3pmspeicherlanip" id="mpm3pmspeicherlanip" value="<?php echo $mpm3pmspeicherlanipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12
										</span>
									</div>
								</div>
							</div>
						</div>

						<script>
							function display_speichermodul() {
								hideSection('#divspeichermqtt');
								hideSection('#divspeicherhttp');
								hideSection('#divspeichermpm3pm');
								hideSection('#divspeicherbydhv');
								hideSection('#divspeicherfronius');
								hideSection('#divspeichere3dc');
								hideSection('#divspeichersbs25');
								hideSection('#divspeichersolaredge');
								hideSection('#divspeichersolax');
								hideSection('#divspeicherpw');
								hideSection('#divspeicherplenti');
								hideSection('#divspeichersunnyisland');
								hideSection('#divspeicherseco');
								hideSection('#divspeicherkit');
								hideSection('#divspeichervarta');
								hideSection('#divspeicheralphaess');
								hideSection('#divspeichervictron');
								hideSection('#divspeicherstuder');
								hideSection('#divspeicherlgessv1');
								hideSection('#divspeicherfems');
								hideSection('#divspeicherip');
								hideSection('#divspeichersiemens');
								hideSection('#divspeicherrct');
								hideSection('#divspeichersungrow');
								hideSection('#divspeicherjson');

								if($('#speichermodul').val() == 'speicher_fems') {
									showSection('#divspeicherfems');
								}
								if($('#speichermodul').val() == 'speicher_rct') {
									showSection('#divspeicherrct');
								}
								if($('#speichermodul').val() == 'speicher_siemens') {
									showSection('#divspeicherip');
									showSection('#divspeichersiemens');
								}
								if($('#speichermodul').val() == 'speicher_solarwatt') {
									showSection('#divspeicherip');
								}
								if($('#speichermodul').val() == 'speicher_tesvoltsma') {
									showSection('#divspeicherip');
								}
								if($('#speichermodul').val() == 'speicher_sungrow') {
									showSection('#divspeicherip');
									showSection('#divspeichersungrow');
								}
								if($('#speichermodul').val() == 'speicher_alphaess') {
									showSection('#divspeicheralphaess');
								}
								if($('#speichermodul').val() == 'speicher_mqtt') {
									showSection('#divspeichermqtt');
								}
								if($('#speichermodul').val() == 'speicher_victron') {
									showSection('#divspeichervictron');
								}
                                if($('#speichermodul').val() == 'speicher_studer') {
									showSection('#divspeicherstuder');
								}
								if($('#speichermodul').val() == 'speicher_mpm3pm') {
									showSection('#divspeicherkit');
								}
								if($('#speichermodul').val() == 'speicher_sonneneco') {
									showSection('#divspeicherseco');
								}
								if($('#speichermodul').val() == 'speicher_http')   {
									showSection('#divspeicherhttp');
								}
								if($('#speichermodul').val() == 'speicher_json')   {
									showSection('#divspeicherjson');
								}
								if($('#speichermodul').val() == 'mpm3pmspeicher')   {
									showSection('#divspeichermpm3pm');
								}
								if($('#speichermodul').val() == 'speicher_bydhv')   {
									showSection('#divspeicherbydhv');
								}
								if($('#speichermodul').val() == 'speicher_fronius')   {
									showSection('#divspeicherfronius');
								}
								if($('#speichermodul').val() == 'speicher_e3dc')   {
									showSection('#divspeichere3dc');
								}
								if($('#speichermodul').val() == 'speicher_sbs25')   {
									showSection('#divspeichersbs25');
								}
								if($('#speichermodul').val() == 'speicher_solaredge')   {
									showSection('#divspeichersolaredge');
								}
								if($('#speichermodul').val() == 'speicher_solax')   {
									showSection('#divspeichersolax');
								}
								if($('#speichermodul').val() == 'speicher_varta')   {
									showSection('#divspeichervarta');
								}
								if($('#speichermodul').val() == 'speicher_powerwall')   {
									showSection('#divspeicherpw');
								}
								if($('#speichermodul').val() == 'speicher_kostalplenticore')   {
									showSection('#divspeicherplenti');
								}
								if($('#speichermodul').val() == 'speicher_sunnyisland')   {
									showSection('#divspeichersunnyisland');
								}
								if($('#speichermodul').val() == 'speicher_lgessv1')   {
									showSection('#divspeicherlgessv1');
								}
							}

							$(function() {
								$('#speichermodul').change( function(){
									display_speichermodul();
								});

								display_speichermodul();
							});
						</script>
					</div>
				</div>

				<div class="row justify-content-center">
					<div class="col-3 text-center">
						<button class="btn btn-success" type="submit" id="saveBtn">Speichern</button>
					</div>
					<div class="col-1 wizzard hide">
						<input type="hidden" name="wizzarddone" id="wizzarddoneInput" value="<?php echo $wizzarddoneold+1; ?>" disabled>
					</div>
					<div class="col-3 text-center wizzard hide">
						<button class="btn btn-danger" id="abortWizzardBtn" type="button">Assistent beenden</button>
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


			<!-- modal abort confirmation window -->
			<div class="modal fade" id="abortWizzardConfirmationModal" role="dialog">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<!-- modal header -->
						<div class="modal-header bg-danger">
							<h4 class="modal-title text-light">Achtung</h4>
						</div>
						<!-- modal body -->
						<div class="modal-body text-center">
							<p>
								Wollen Sie den Assistenten wirklich beenden?<br>
								Die Einrichtung eines <span class="text-danger">EVU</span>-Moduls ist für den Betrieb von openWB zwingend erforderlich.
								<span class="text-success">PV</span>- und <span class="text-warning">BAT</span>-Module sind optional, ermöglichen aber weitere Einstellungen der Regelung.
							</p>
						</div>
						<!-- modal footer -->
						<div class="modal-footer d-flex justify-content-center">
							<button type="button" class="btn btn-success" data-dismiss="modal">Zurück zum Assistenten</button>
							<button type="button" class="btn btn-danger" data-dismiss="modal" id="abortWizzardConfirmationBtn">Assistent beenden</button>
						</div>
					</div>
				</div>
			</div>

			<!-- hidden form to save wizzard done to config on abort -->
			<form id="wizzarddoneForm" action="tools/saveconfig.php" method="POST">
				<input type="hidden" name="wizzarddone" value="100">
			</form>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
			  <small>Sie befinden sich hier: Einstellungen/Modulkonfiguration</small>
			</div>
		</footer>

		<script>
			// wizzard specific code
			$(document).ready(function(){

				$('#abortWizzardBtn').on("click",function() {
					$('#abortWizzardConfirmationModal').modal();
				});

				// shown in confirmation modal
				$('#abortWizzardConfirmationBtn').on("click",function() {
					$('#wizzarddoneForm').submit();
				});

			});

			var wizzarddone = <?php if(isset($wizzarddoneold)){ echo $wizzarddoneold; } else { echo 100; } ?>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navModulkonfigurationBat').addClass('disabled');

					// check if wizzard is running
					if( wizzarddone < 100 ){
						// remove navbar entries
						$('#collapsibleNavbar').remove();
						// remove link from logo
						$('.navbar-brand').removeAttr('href');
						// enable hidden wizzarddone input
						$('#wizzarddoneInput').removeAttr('disabled');
						// change text of submit button
						$('#saveBtn').html("Speichern und weiter...");
						// display wizzard specific elements
						$('.wizzard').removeClass('hide');
					} else {
						// disable hidden wizzarddone input
						// on some browsers hidden input fields cannot be initially disabled
						$('#wizzarddoneInput').attr('disabled', true);
					}
				}
			);

		</script>

	</body>
</html>
