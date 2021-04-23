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
			<h1>Modulkonfiguration PV</h1>
			<form action="./settings/saveconfig.php" method="POST">

				<!-- PV Module 1 -->
				<div class="card border-success">
					<div class="card-header bg-success">
						PV-Modul 1
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="pvwattmodul" class="col-md-4 col-form-label">PV-Modul</label>
							<div class="col">
								<select name="pvwattmodul" id="pvwattmodul" class="form-control">
									<option <?php if($pvwattmodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<optgroup label="openWB">
										<option <?php if($pvwattmodulold == "wr_pvkit") echo "selected" ?> value="wr_pvkit">openWB PV Kit</option>
										<option <?php if($pvwattmodulold == "wr_ethmpm3pmaevu") echo "selected" ?> value="wr_ethmpm3pmaevu">Zähler an openWB EVU Kit</option>
										<option <?php if($pvwattmodulold == "wr_ethsdm120") echo "selected" ?> value="wr_ethsdm120">SDM120 an openWB Modbus Lan Konverter</option>
									</optgroup>
									<optgroup label="andere Hersteller">
										<option <?php if($pvwattmodulold == "wr_discovergy") echo "selected" ?> value="wr_discovergy">Discovergy</option>
										<option <?php if($pvwattmodulold == "wr_fronius") echo "selected" ?> value="wr_fronius">Fronius WR</option>
										<option <?php if($pvwattmodulold == "wr_huawei") echo "selected" ?> value="wr_huawei">Huawei</option>
										<option <?php if($pvwattmodulold == "wr_kostalpiko") echo "selected" ?> value="wr_kostalpiko">Kostal Piko</option>
										<option <?php if($pvwattmodulold == "wr_kostalpikovar2") echo "selected" ?> value="wr_kostalpikovar2">Kostal Piko alt</option>
										<option <?php if($pvwattmodulold == "wr_plenticore") echo "selected" ?> value="wr_plenticore">Kostal Plenticore</option>
										<option <?php if($pvwattmodulold == "wr_lgessv1") echo "selected" ?> value="wr_lgessv1">LG ESS 1.0VI</option>
										<option <?php if($pvwattmodulold == "wr_fems") echo "selected" ?> value="wr_fems">openEMS / Fenecon FEMS / Kaco Hy-Control</option>
										<option <?php if($pvwattmodulold == "wr_powerdog") echo "selected" ?> value="wr_powerdog">Powerdog</option>
										<option <?php if($pvwattmodulold == "wr_rct") echo "selected" ?> value="wr_rct">RCT</option>
										<option <?php if($pvwattmodulold == "wr_siemens") echo "selected" ?> value="wr_siemens">Siemens Speicher</option>
										<option <?php if($pvwattmodulold == "smaemd_pv") echo "selected" ?> value="smaemd_pv">SMA Energy Meter</option>
										<option <?php if($pvwattmodulold == "wr_tripower9000") echo "selected" ?> value="wr_tripower9000">SMA ModbusTCP WR</option>
										<option <?php if($pvwattmodulold == "wr_smartme") echo "selected" ?> value="wr_smartme">SmartMe</option>
										<option <?php if($pvwattmodulold == "wr_solaredge") echo "selected" ?> value="wr_solaredge">SolarEdge WR</option>
										<option <?php if($pvwattmodulold == "wr_solarlog") echo "selected" ?> value="wr_solarlog">SolarLog</option>
										<option <?php if($pvwattmodulold == "wr_solarview") echo "selected" ?> value="wr_solarview">Solarview</option>
										<option <?php if($pvwattmodulold == "wr_solarwatt") echo "selected" ?> value="wr_solarwatt">Solarwatt / My Reserver Speicher</option>
										<option <?php if($pvwattmodulold == "wr_solarworld") echo "selected" ?> value="wr_solarworld">Solarworld</option>
										<option <?php if($pvwattmodulold == "wr_solax") echo "selected" ?> value="wr_solax">Solax WR</option>
										<option <?php if($pvwattmodulold == "wr_sungrow") echo "selected" ?> value="wr_sungrow">Sungrow</option>
										<option <?php if($pvwattmodulold == "wr_sunways") echo "selected" ?> value="wr_sunways">Sunways</option>
										<option <?php if($pvwattmodulold == "wr_powerwall") echo "selected" ?> value="wr_powerwall">Tesla Powerwall</option>
										<option <?php if($pvwattmodulold == "wr_victron") echo "selected" ?> value="wr_victron">Victron</option>
										<option <?php if($pvwattmodulold == "wr_youless120") echo "selected" ?> value="wr_youless120">Youless 120</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($pvwattmodulold == "wr_http") echo "selected" ?> value="wr_http">Http</option>
										<option <?php if($pvwattmodulold == "wr_json") echo "selected" ?> value="wr_json">Json</option>
										<option <?php if($pvwattmodulold == "mpm3pmpv") echo "selected" ?> value="mpm3pmpv">MPM3PM </option>
										<option <?php if($pvwattmodulold == "wr_mqtt") echo "selected" ?> value="wr_mqtt">MQTT</option>
										<option <?php if($pvwattmodulold == "sdm630modbuswr") echo "selected" ?> value="sdm630modbuswr">SDM 630 Modbus</option>
										<option <?php if($pvwattmodulold == "wr_shelly") echo "selected" ?> value="wr_shelly">Shelly</option>
										<option <?php if($pvwattmodulold == "vzloggerpv") echo "selected" ?> value="vzloggerpv">VZLogger</option>
									</optgroup>
								</select>
							</div>
						</div>
						<div id="pvmqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/pv/1/W</span> PV-Leistung in Watt, int, negativ<br>
								<span class="text-info">openWB/set/pv/1/WhCounter</span> Erzeugte Energie in Wh, float, nur positiv
							</div>
						</div>
						<div id="pvsungrow" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen Speichermodul des Sungrow erforderlich.
							</div>
						</div>
						<div id="pvlgessv1" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen Speichermodul des LG ESS 1.0VI erforderlich. Als EVU-Modul auch LG ESS 1.0VI wählen!
							</div>
						</div>
						<div id="pvsolarwatt" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen Speichermodul des Solarwatt/My Reserve erforderlich.
							</div>
						</div>
						<div id="pvip" class="hide">
							<div class="form-row mb-1">
								<label for="pv1_ipa" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="pv1_ipa" id="pv1_ipa" value="<?php echo $pv1_ipaold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pvsiemens" class="hide">
							<!-- nothing here, just generic IP -->
						</div>
						<div id="pvpowerdog" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul.
							</div>
						</div>
						<div id="pvrct" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul.
							</div>
						</div>
						<div id="pvfems" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul des FEMS erforderlich.
							</div>
						</div>
						<div id="pvsolarworld" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen EVU Modul des Solarworld erforderlich.
							</div>
						</div>
						<div id="pvyouless" class="hide">
							<div class="form-row mb-1">
								<label for="wryoulessip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wryoulessip" id="wryoulessip" value="<?php echo $wryoulessipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pvsunways" class="hide">
							<div class="form-row mb-1">
								<label for="wrsunwaysip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrsunwaysip" id="wrsunwaysip" value="<?php echo $wrsunwaysipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsunwayspw" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="wrsunwayspw" id="wrsunwayspw" value="<?php echo htmlspecialchars($wrsunwayspwold) ?>">
								</div>
							</div>
						</div>
						<div id="pvsolarlog" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_solarlog_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug_solarlog_ip" id="bezug_solarlog_ip" value="<?php echo $bezug_solarlog_ipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										Wenn ein Eigenverbrauchszähler installiert ist bitte EVU SolarLog Modul nutzen. Wenn nicht dann dieses Modul.
									</span>
								</div>
							</div>
						</div>
						<div id="pvdiscovergy" class="hide">
							<div class="form-row mb-1">
								<label for="discovergypvid" class="col-md-4 col-form-label">Meter ID des Zählers</label>
								<div class="col">
									<input class="form-control" type="text" name="discovergypvid" id="discovergypvid" value="<?php echo htmlspecialchars($discovergypvidold) ?>">
									<span class="form-text small">
										Gültige Werte ID. Um die ID herauszufinden mit dem Browser die Adresse "https://api.discovergy.com/public/v1/meters" aufrufen und dort Benutzername und Passwort eingeben. Hier wird nun u.a. die ID des Zählers angezeigt.<br>
										Die Benutzerdaten werden im Discovergy EVU Modul konfiguriert.
									</span>
								</div>
							</div>
						</div>
						<div id="pvsolarview" class="hide">
							<div class="form-row mb-1">
								<label for="solarview_hostname" class="col-md-4 col-form-label">Hostname/IP des SolarView TCP-Servers</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|[a-zA-Z0-9.\-_]+$" name="solarview_hostname" id="solarview_hostname" value="<?php echo $solarview_hostnameold ?>">
									<span class="form-text small">
										Gültige Werte Hostname oder IP-Adresse.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solarview_port" class="col-md-4 col-form-label">Port des Solarview TCP-Servers</label>
								<div class="col">
									<input class="form-control" type="number" name="solarview_port" id="solarview_port" value="<?php echo htmlspecialchars($solarview_portold) ?>">
									<span class="form-text small">
										Gültige Werte Port, z.B. 15000.
									</span>
								</div>
							</div>
						</div>
						<div id="pvpowerwall" class="hide">
							<div class="card-text alert alert-info">
								Keine Einstellung nötig. Die IP wird im Speichermodul konfiguriert.
							</div>
						</div>
						<div id="pvkitdiv" class="hide">
							<div class="form-row mb-1">
								<label for="pvkitversion" class="col-md-4 col-form-label">Version des openWB PV Kits</label>
								<div class="col">
									<select name="pvkitversion" id="pvkitversion" class="form-control">
										<option <?php if($pvkitversionold == 0) echo "selected" ?> value="0">PV Kit mit MPM3PM Zähler</option>
										<option <?php if($pvkitversionold == 1) echo "selected" ?> value="1">PV Kit mit Lovato Zähler</option>
										<option <?php if($pvkitversionold == 2) echo "selected" ?> value="2">PV Kit mit Eastron SDM630 Zähler</option>
									</select>
								</div>
							</div>
						</div>
						<div id="pvplenti" class="hide">
							<div class="form-row mb-1">
								<label for="kostalplenticoreip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="kostalplenticoreip" id="kostalplenticoreip" value="<?php echo $kostalplenticoreipold ?>">
									<span class="form-text small">
										Gültige Werte: IP-Adresse des 1. Kostal Plenticore. An diesem muss (wenn vorhanden) der EM300/das KSEM und ggf. Speicher angeschlossen sein.
										Modbus/Sunspec (TCP) muss im WR aktiviert sein (Port 1502, Unit-ID 71).
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="name_wechselrichter1" class="col-md-4 col-form-label">Name</label>
								<div class="col">
									<input class="form-control" type="text" name="name_wechselrichter1" id="name_wechselrichter1" value="<?php echo $name_wechselrichter1old ?>">
									<span class="form-text small">
										Freie Bezeichnung des Wechselrichters zu Anzeigezwecken, kann leer bleiben.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="kostalplenticoreip2" class="col-md-4 col-form-label">WR 2 IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="kostalplenticoreip2" id="kostalplenticoreip2" value="<?php echo $kostalplenticoreip2old ?>">
									<span class="form-text small">
										Gültige Werte: IP-Adresse des 2. Kostal Plenticore oder "none". An diesem WR darf kein Speicher angeschlossen sein.
										Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden, ansonsten muss Modbus/Sunspec (TCP) im WR aktiviert sein (Port 1502, Unit-ID 71).
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="kostalplenticoreip3" class="col-md-4 col-form-label">WR 3 IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="kostalplenticoreip3" id="kostalplenticoreip3" value="<?php echo $kostalplenticoreip3old ?>">
									<span class="form-text small">
										Gültige Werte: IP-Adresse des 3. Kostal Plenticore oder "none". An diesem WR darf kein Speicher angeschlossen sein.
										Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden, ansonsten muss Modbus/Sunspec (TCP) im WR aktiviert sein (Port 1502, Unit-ID 71).
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="name_wechselrichter2" class="col-md-4 col-form-label">WR 2 Name</label>
								<div class="col">
									<input class="form-control" type="text" name="name_wechselrichter2" id="name_wechselrichter2" value="<?php echo $name_wechselrichter2old ?>">
									<span class="form-text small">
										Freie Bezeichnung des zweiten Wechselrichters zu Anzeigezwecken, kann leer bleiben.
									</span>
								</div>
							</div>
						</div>
						<div id="pvsmartme" class="hide">
							<div class="form-row mb-1">
								<label for="wr_smartme_user" class="col-md-4 col-form-label">Smartme Benutzername</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_smartme_user" id="wr_smartme_user" value="<?php echo $wr_smartme_userold ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_smartme_pass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="wr_smartme_pass" id="wr_smartme_pass" value="<?php echo htmlspecialchars($wr_smartme_passold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_smartme_url" class="col-md-4 col-form-label">Smartme URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_smartme_url" id="wr_smartme_url" value="<?php echo $wr_smartme_urlold ?>">
								</div>
							</div>
						</div>
						<div id="pvpiko2" class="hide">
							<div class="form-row mb-1">
								<label for="wr_piko2_user" class="col-md-4 col-form-label">Benutzername</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_piko2_user" id="wr_piko2_user" value="<?php echo $wr_piko2_userold ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_piko2_pass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="wr_piko2_pass" id="wr_piko2_pass" value="<?php echo htmlspecialchars($wr_piko2_passold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_piko2_url" class="col-md-4 col-form-label">URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_piko2_url" id="wr_piko2_url" value="<?php echo $wr_piko2_urlold ?>">
								</div>
							</div>
						</div>
						<div id="pvwrjson" class="hide">
							<div class="form-row mb-1">
								<label for="wrjsonurl" class="col-md-4 col-form-label">WR URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wrjsonurl" id="wrjsonurl" value="<?php echo $wrjsonurlold ?>">
									<span class="form-text small">
										Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrjsonwatt" class="col-md-4 col-form-label">Json Abfrage für Watt</label>
								<div class="col">
									<input class="form-control" type="text" name="wrjsonwatt" id="wrjsonwatt" value="<?php echo htmlspecialchars($wrjsonwattold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> So muss hier <span class="text-info">.PowerOut</span> eingetragen werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrjsonkwh" class="col-md-4 col-form-label">Json Abfrage für Wh</label>
								<div class="col">
									<input class="form-control" type="text" name="wrjsonkwh" id="wrjsonkwh" value="<?php echo htmlspecialchars($wrjsonkwhold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> So muss hier <span class="text-info">.PowerProduced</span> eingetragen werden.
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrkostalpiko" class="hide">
							<div class="form-row mb-1">
								<label for="wrkostalpikoip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrkostalpikoip" id="wrkostalpikoip" value="<?php echo $wrkostalpikoipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrtri9000" class="hide">
							<div class="form-row mb-1">
								<label for="tri9000ip" class="col-md-4 col-form-label">WR 1 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="tri9000ip" id="tri9000ip" value="<?php echo $tri9000ipold ?>">
									<span class="form-text small">
										Gültige Werte: IPs. IP Adresse des SMA WR, ggf. muss der modbusTCP im WR noch aktiviert werden (normalerweise deaktiviert, entweder direkt am Wechselrichter, per Sunny Portal oder über das Tool "Sunny Explorer").
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Handelt es sich um eine SMA Webbox?</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($wrsmawebboxold == 0) echo " active" ?>">
											<input type="radio" name="wrsmawebbox" id="wrsmawebboxNo" value="0"<?php if($wrsmawebboxold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($wrsmawebboxold == 1) echo " active" ?>">
											<input type="radio" name="wrsmawebbox" id="wrsmawebboxYes" value="1"<?php if($wrsmawebboxold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
									<span class="form-text small">
										Diese Option aktivieren wenn ein Solaredge SmartMeter verbaut ist welches vorhandene Bestands PV Anlagen erfasst.
										Das Meter muss an Position 2 konfiguriert sein.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsma2ip" class="col-md-4 col-form-label">WR 2 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrsma2ip" id="wrsma2ip" value="<?php echo $wrsma2ipold ?>">
									<span class="form-text small">
										Gültige Werte: IP Adresse oder "none". IP des zweiten SMA Wechselrichters. Wenn nur ein WR genutzt wird, muss der Wert "none" gesetzt werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsma3ip" class="col-md-4 col-form-label">WR 3 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrsma3ip" id="wrsma3ip" value="<?php echo $wrsma3ipold ?>">
									<span class="form-text small">
										Gültige Werte: IP Adresse oder "none". IP des dritten SMA Wechselrichters. Wenn weniger WR genutzt werden, muss der Wert "none" gesetzt werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrsma4ip" class="col-md-4 col-form-label">WR 4 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrsma4ip" id="wrsma4ip" value="<?php echo $wrsma4ipold ?>">
									<span class="form-text small">
										Gültige Werte: IP Adresse oder "none". IP des vierten SMA Wechselrichters. Wenn weniger WR genutzt werden, muss der Wert "none" gesetzt werden.
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrsolaredge" class="hide">
							<div class="form-row mb-1">
								<label for="solaredgepvip" class="col-md-4 col-form-label">WR Solaredge IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaredgepvip" id="solaredgepvip" value="<?php echo $solaredgepvipold ?>">
									<span class="form-text small">
										Gültige Werte: IPs. IP Adresse des SolarEdge Wechselrichters. Modbus TCP muss am WR aktiviert werden, der Port ist auf 502 zu stellen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Externes Meter mit auslesen</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($wr1extprodold == 0) echo " active" ?>">
											<input type="radio" name="wr1extprod" id="wr1extprodNo" value="0"<?php if($wr1extprodold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($wr1extprodold == 1) echo " active" ?>">
											<input type="radio" name="wr1extprod" id="wr1extprodYes" value="1"<?php if($wr1extprodold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
									<span class="form-text small">
										Diese Option aktivieren wenn ein Solaredge SmartMeter verbaut ist welches vorhandene Bestands PV Anlagen erfasst.
										Das Meter muss an Position 2 konfiguriert sein.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave1" class="col-md-4 col-form-label">WR 1 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="1" name="solaredgepvslave1" id="solaredgepvslave1" value="<?php echo $solaredgepvslave1old ?>">
									<span class="form-text small">
										Gültige Werte Zahl. ID des SolarEdge Wechselrichters. Normalerweise 1.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave2" class="col-md-4 col-form-label">WR 2 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="text" name="solaredgepvslave2" id="solaredgepvslave2" value="<?php echo $solaredgepvslave2old ?>">
									<span class="form-text small">
										Gültige Werte Zahl oder none. ID des zweiten SolarEdge Wechselrichters. Wenn nur ein WR genutzt wird auf none setzen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave3" class="col-md-4 col-form-label">WR 3 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="text" name="solaredgepvslave3" id="solaredgepvslave3" value="<?php echo $solaredgepvslave3old ?>">
									<span class="form-text small">
										Gültige Werte Zahl oder none. ID des dritten SolarEdge Wechselrichters. Wenn weniger WR genutzt werden auf none setzen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgepvslave4" class="col-md-4 col-form-label">WR 4 Solaredge ID</label>
								<div class="col">
									<input class="form-control" type="text" name="solaredgepvslave4" id="solaredgepvslave4" value="<?php echo $solaredgepvslave4old ?>">
									<span class="form-text small">
										Gültige Werte Zahl oder none. ID des vierten SolarEdge Wechselrichters. Wenn weniger WR genutzt werden auf none setzen.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgewr2ip" class="col-md-4 col-form-label">WR 2 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="solaredgewr2ip" id="solaredgewr2ip" value="<?php echo $solaredgewr2ipold ?>">
									<span class="form-text small">
										Gültige Werte IP oder none. IP des zweiten SolarEdge Wechselrichters. Ist nur nötig, wenn 2 Wechselrichter genutzt werden die nicht per Modbus miteinander verbunden sind.
									</span>
								</div>
							</div>
						</div>
						<div id="pvwrsolax" class="hide">
							<div class="form-row mb-1">
								<label for="solaxip" class="col-md-4 col-form-label">WR Solax IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaxip" id="solaxip" value="<?php echo $solaxipold ?>">
									<span class="form-text small">
										Gültige Werte: IPs. IP Adresse des Solax Wechselrichters. 
									</span>
								</div>
							</div>
						</div> 
						<div id="pvwrfronius" class="hide">
							<div class="form-row mb-1">
								<label for="wrfroniusip" class="col-md-4 col-form-label">WR Fronius IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrfroniusip" id="wrfroniusip" value="<?php echo $wrfroniusipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12. IP Adresse des Fronius Wechselrichters. Werden hier und im Feld unten zwei verschiedene Adressen eingetragen, muss hier die Adresse des Wechselrichters stehen, an dem das SmartMeter angeschlossen ist.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Handelt es sich um einen Gen24?</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($wrfroniusisgen24old == 0) echo " active" ?>">
											<input type="radio" name="froniusisgen24" id="froniusisgen24No" value="0"<?php if($wrfroniusisgen24old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($wrfroniusisgen24old == 1) echo " active" ?>">
											<input type="radio" name="froniusisgen24" id="froniusisgen24Yes" value="1"<?php if($wrfroniusisgen24old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
									<span class="form-text small">
										Diese Option aktivieren wenn es sich um einen Gen24 handelt.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wrfronius2ip" class="col-md-4 col-form-label">WR Fronius 2 IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])|none$" name="wrfronius2ip" id="wrfronius2ip" value="<?php echo $wrfronius2ipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12. IP Adresse des zweiten Fronius Wechselrichters. Sind nur Symos in Nutzung, welche über Fronius Solar Net / DATCOM miteinander verbunden sind, reicht die Angabe der Adresse eines Wechselrichters im ersten Feld. Sind aber z.B. Symo und Symo Hybrid im Einsatz, müssen diese beide angegeben werden (hier dann die Adresse des Wechselrichters, an dem das SmartMeter NICHT angeschlossen ist). Ist kein zweiter Wechselrichter vorhanden, dann bitte hier "none" eintragen.
									</span>
								</div>
							</div>
						</div>
						<div id="pvmpm3pm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="mpm3pmpvsource" class="col-md-4 col-form-label">MPM3PM Wechselrichterleistung Source</label>
									<div class="col">
										<input class="form-control" type="text" name="mpm3pmpvsource" id="mpm3pmpvsource" value="<?php echo $mpm3pmpvsourceold ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM angeschlossen ist. Meist /dev/ttyUSB0<br>
											Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmpvid" class="col-md-4 col-form-label">MPM3PM Wechselrichterleistung ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmpvid" id="mpm3pmpvid" value="<?php echo $mpm3pmpvidold ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des MPM3PM.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmpvlanip" class="col-md-4 col-form-label">IP des Modbus/Lan Konverter</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="mpm3pmpvlanip" id="mpm3pmpvlanip" value="<?php echo $mpm3pmpvlanipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Ist die Source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="pvethsdm120" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="wr_sdm120ip" class="col-md-4 col-form-label">SDM Modbus IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wr_sdm120ip" id="wr_sdm120ip" value="<?php echo $wr_sdm120ipold ?>">
										<span class="form-text small">
											Gültige Werte IP. IP Adresse des ModbusLAN Konverters.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="wr_sdm120id" class="col-md-4 col-form-label">SDM Modbus ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="wr_sdm120id" id="wr_sdm120id" value="<?php echo $wr_sdm120idold ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des SDM.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="pvsdmwr" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sdm630modbuswrsource" class="col-md-4 col-form-label">SDM Modbus Wechselrichterleistung Source</label>
									<div class="col">
										<input class="form-control" type="text" name="sdm630modbuswrsource" id="sdm630modbuswrsource" value="<?php echo $sdm630modbuswrsourceold ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der SDM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
											Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbuswrid" class="col-md-4 col-form-label">SDM Modbus Wechselrichterleistung ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="sdm630modbuswrid" id="sdm630modbuswrid" value="<?php echo $sdm630modbuswridold ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des SDM. Getestet SDM230 & SDM630v2.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbuswrlanip" class="col-md-4 col-form-label">IP des Modbus/Lan Konverter</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sdm630modbuswrlanip" id="sdm630modbuswrlanip" value="<?php echo $sdm630modbuswrlanipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Ist die Source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="pvvzl" class="hide">
							<div class="form-row mb-1">
								<label for="vzloggerpvip" class="col-md-4 col-form-label">IP Adresse und Port</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5]):[1-9][0-9]*$" name="vzloggerpvip" id="vzloggerpvip" value="<?php echo $vzloggerpvipold ?>">
									<span class="form-text small">
										Gültige Werte IP:Port z.B. 192.168.0.12:8080.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="vzloggerpvline" class="col-md-4 col-form-label">Vzloggerpv Zeile</label>
								<div class="col">
									<input class="form-control" type="number" min="1" step="1" name="vzloggerpvline" id="vzloggerpvline" value="<?php echo $vzloggerpvlineold ?>">
									<span class="form-text small">
										Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq .|cat -n"<br>
										Nun zählen in welcher Zeile der gewünschte Wert steht und diesen hier eintragen.
									</span>
								</div>
							</div>
						</div>
						<div id="pvhttp" class="hide">
							<div class="form-row mb-1">
								<label for="wr_http_w_url" class="col-md-4 col-form-label">Vollständige URL für die Wechselrichter Watt</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_http_w_url" id="wr_http_w_url" value="<?php echo htmlspecialchars($wr_http_w_urlold) ?>">
									<span class="form-text small">
										Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr_http_kwh_url" class="col-md-4 col-form-label">Vollständige URL für die Wechselrichter absolut Wh</label>
								<div class="col">
									<input class="form-control" type="text" name="wr_http_kwh_url" id="wr_http_kwh_url" value="<?php echo htmlspecialchars($wr_http_kwh_urlold) ?>">
									<span class="form-text small">
										Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
									</span>
								</div>
							</div>
						</div>
						<div id="pvsma" class="hide">
							<div class="form-row mb-1">
								<label for="smaemdpvid" class="col-md-4 col-form-label">Seriennummer des SMA Energy Meter</label>
								<div class="col">
									<input class="form-control" type="text" name="smaemdpvid" id="smaemdpvid" value="<?php echo $smaemdpvidold ?>">
									<span class="form-text small">
									Gültige Werte Seriennummer. Hier die Seriennummer des SMA Meter für die PV angeben.
									</span>
								</div>
							</div>
						</div>

						<script>
							function display_pvwattmodul() {
								hideSection('#pvvzl');
								hideSection('#pvsdmwr');
								hideSection('#pvwrfronius');
								hideSection('#pvhttp');
								hideSection('#pvsma');
								hideSection('#pvwrjson');
								hideSection('#pvmpm3pm');
								hideSection('#pvwrkostalpiko');
								hideSection('#pvwrsolaredge');
								hideSection('#pvwrsolax');
								hideSection('#pvsmartme');
								hideSection('#pvwrtri9000');
								hideSection('#pvplenti');
								hideSection('#pvsolarlog');
								hideSection('#pvpiko2');
								hideSection('#pvpowerwall');
								hideSection('#pvkitdiv');
								hideSection('#pvethsdm120');
								hideSection('#pvsolarview');
								hideSection('#pvdiscovergy');
								hideSection('#pvyouless');
								hideSection('#pvlgessv1');
								hideSection('#pvmqtt');
								hideSection('#pvsunways');
								hideSection('#pvfems');
								hideSection('#pvsolarworld');
								hideSection('#pvip');
								hideSection('#pvsiemens');
								hideSection('#pvrct');
								hideSection('#pvpowerdog');
								hideSection('#pvsolarwatt');
								hideSection('#pvsungrow');
								if($('#pvwattmodul').val() == 'wr_siemens') {
									showSection('#pvip');
									showSection('#pvsiemens');
								}
								if($('#pvwattmodul').val() == 'wr_victron') {
									showSection('#pvip');
								}
								if($('#pvwattmodul').val() == 'wr_huawei') {
									showSection('#pvip');
								}
								if($('#pvwattmodul').val() == 'wr_shelly') {
									showSection('#pvip');
								}
								if($('#pvwattmodul').val() == 'wr_powerdog') {
									showSection('#pvpowerdog');
								}
								if($('#pvwattmodul').val() == 'wr_rct') {
									showSection('#pvrct');
								}
								if($('#pvwattmodul').val() == 'wr_fems') {
									showSection('#pvfems');
								}
								if($('#pvwattmodul').val() == 'wr_solarworld') {
									showSection('#pvsolarworld');
								}
								if($('#pvwattmodul').val() == 'wr_sunways') {
									showSection('#pvsunways');
								}
								if($('#pvwattmodul').val() == 'wr_mqtt') {
									showSection('#pvmqtt');
								}
								if($('#pvwattmodul').val() == 'wr_youless120') {
									showSection('#pvyouless');
								}
								if($('#pvwattmodul').val() == 'wr_solarview') {
									showSection('#pvsolarview');
								}
								if($('#pvwattmodul').val() == 'wr_discovergy') {
									showSection('#pvdiscovergy');
								}
								if($('#pvwattmodul').val() == 'wr_ethsdm120') {
									showSection('#pvethsdm120');
								}
								if($('#pvwattmodul').val() == 'wr_pvkit') {
									showSection('#pvkitdiv');
								}
								if($('#pvwattmodul').val() == 'wr_ethmpm3pmaevu') {
									showSection('#pvkitdiv');
								}
								if($('#pvwattmodul').val() == 'vzloggerpv') {
									showSection('#pvvzl');
								}
								if($('#pvwattmodul').val() == 'sdm630modbuswr')   {
									showSection('#pvsdmwr');
								}
								if($('#pvwattmodul').val() == 'wr_fronius')   {
									showSection('#pvwrfronius');
								}
								if($('#pvwattmodul').val() == 'wr_http')   {
									showSection('#pvhttp');
								}
								if($('#pvwattmodul').val() == 'smaemd_pv')   {
									showSection('#pvsma');
								}
								if($('#pvwattmodul').val() == 'wr_json')   {
									showSection('#pvwrjson');
								}
								if($('#pvwattmodul').val() == 'mpm3pmpv')   {
									showSection('#pvmpm3pm');
								}
								if($('#pvwattmodul').val() == 'wr_kostalpiko')   {
									showSection('#pvwrkostalpiko');
								}
								if($('#pvwattmodul').val() == 'wr_solaredge')   {
									showSection('#pvwrsolaredge');
								}
								if($('#pvwattmodul').val() == 'wr_solax')   {
									showSection('#pvwrsolax');
								}
								if($('#pvwattmodul').val() == 'wr_smartme')   {
									showSection('#pvsmartme');
								}
								if($('#pvwattmodul').val() == 'wr_tripower9000')   {
									showSection('#pvwrtri9000');
								}
								if($('#pvwattmodul').val() == 'wr_plenticore')   {
									showSection('#pvplenti');
								}
								if($('#pvwattmodul').val() == 'wr_solarlog')   {
									showSection('#pvsolarlog');
								}
								if($('#pvwattmodul').val() == 'wr_kostalpikovar2')   {
									showSection('#pvpiko2');
								}
								if($('#pvwattmodul').val() == 'wr_powerwall')   {
									showSection('#pvpowerwall');
								}
								if($('#pvwattmodul').val() == 'wr_lgessv1')   {
									showSection('#pvlgessv1');
								}
								if($('#pvwattmodul').val() == 'wr_solarwatt')   {
									showSection('#pvsolarwatt');
								}
								if($('#pvsungrow').val() == 'wr_sungrow')   {
									showSection('#pvsungrow');
								}
							}

							$(function() {
								display_pvwattmodul();

								$('#pvwattmodul').change( function(){
									display_pvwattmodul();
								} );
							});
						</script>
					</div>
				</div>

				<!-- PV Module 2 -->
				<div class="card border-success">
					<div class="card-header bg-success">
						PV-Modul 2
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="pv2wattmodul" class="col-md-4 col-form-label">PV-Modul</label>
							<div class="col">
								<select name="pv2wattmodul" id="pv2wattmodul" class="form-control">
									<option <?php if($pv2wattmodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<optgroup label="openWB">
										<option <?php if($pv2wattmodulold == "wr2_ethlovatoaevu") echo "selected" ?> value="wr2_ethlovatoaevu">PV Zähler an openWB EVU Kit</option>
										<option <?php if($pv2wattmodulold == "wr2_ethlovato") echo "selected" ?> value="wr2_ethlovato">openWB PV Kit</option>
									</optgroup>
									<optgroup label="andere Hersteller">
										<option <?php if($pv2wattmodulold == "wr2_kostalpiko") echo "selected" ?> value="wr2_kostalpiko">Kostal Piko</option>
										<option <?php if($pv2wattmodulold == "wr2_kostalsteca") echo "selected" ?> value="wr2_kostalsteca">Kostal Piko MP oder Steca Grid Coolcept</option>
										<option <?php if($pv2wattmodulold == "wr2_smamodbus") echo "selected" ?> value="wr2_smamodbus">SMA Wechselrichter</option>
										<option <?php if($pv2wattmodulold == "wr2_solaredge") echo "selected" ?> value="wr2_solaredge">Solaredge</option>
										<option <?php if($pv2wattmodulold == "wr2_solax") echo "selected" ?> value="wr2_solax">Solax</option>
										<option <?php if($pv2wattmodulold == "wr2_victron") echo "selected" ?> value="wr2_victron">Victron MPPT</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($pv2wattmodulold == "wr2_json") echo "selected" ?> value="wr2_json">Json Abfrage</option>
										<option <?php if($pv2wattmodulold == "wr2_ethsdm120") echo "selected" ?> value="wr2_ethsdm120">SDM120 an Netzwerk Modbus Adapter</option>
									</optgroup>
								</select>
							</div>
						</div>
						<div id="pv2noconfig" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="pv2kitdiv" class="hide">
							<div class="form-row mb-1">
								<label for="pv2kitversion" class="col-md-4 col-form-label">Version des openWB PV Kits</label>
								<div class="col">
									<select name="pv2kitversion" id="pv2kitversion" class="form-control">
										<option <?php if($pv2kitversionold == 0) echo "selected" ?> value="0">Lovato Zähler</option>
										<option <?php if($pv2kitversionold == 1) echo "selected" ?> value="1">Eastron SDM630 Zähler</option>
									</select>
								</div>
							</div>
						</div>
						<div id="pv2ipdiv" class="hide">
							<div class="form-row mb-1">
								<label for="pv2ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="pv2ip" id="pv2ip" value="<?php echo $pv2ipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="pv2iddiv" class="hide">
							<div class="form-row mb-1">
								<label for="pv2id" class="col-md-4 col-form-label">Modbus ID</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="1" name="pv2id" id="pv2id" value="<?php echo $pv2idold ?>">
									<span class="form-text small">Gültige Werte ID. ID Adresse</span>
								</div>
							</div>
						</div>
						<div id="pv2wrjsondiv" class="hide">
							<div class="form-row mb-1">
								<label for="wr2jsonurl" class="col-md-4 col-form-label">WR URL</label>
								<div class="col">
									<input class="form-control" type="text" name="wr2jsonurl" id="wr2jsonurl" value="<?php echo $wr2jsonurlold ?>">
									<span class="form-text small">
										Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr2jsonwatt" class="col-md-4 col-form-label">Json Abfrage für Watt</label>
								<div class="col">
									<input class="form-control" type="text" name="wr2jsonwatt" id="wr2jsonwatt" value="<?php echo htmlspecialchars($wr2jsonwattold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> So muss hier <span class="text-info">.PowerOut</span> eingetragen werden.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="wr2jsonkwh" class="col-md-4 col-form-label">Json Abfrage für Wh</label>
								<div class="col">
									<input class="form-control" type="text" name="wr2jsonkwh" id="wr2jsonkwh" value="<?php echo htmlspecialchars($wr2jsonkwhold) ?>">
									<span class="form-text small">
										Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
										Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> So muss hier <span class="text-info">.PowerProduced</span> eingetragen werden.
									</span>
								</div>
							</div>
						</div>
						<script>
							function display_pv2wattmodul() {
								hideSection('#pv2noconfig');
								hideSection('#pv2ipdiv');
								hideSection('#pv2iddiv');
								hideSection('#pv2kitdiv');
								hideSection('#pv2wrjsondiv');
								
								if($('#pv2wattmodul').val() == 'wr2_json') {
									showSection('#pv2wrjsondiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_ethlovatoaevu') {
									showSection('#pv2kitdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_ethlovato') {
									showSection('#pv2kitdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_smamodbus') {
									showSection('#pv2ipdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_solax') {
									showSection('#pv2ipdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_kostalpiko') {
									showSection('#pv2ipdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_kostalsteca') {
									showSection('#pv2ipdiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_victron') {
									showSection('#pv2ipdiv');
									showSection('#pv2iddiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_solaredge') {
									showSection('#pv2ipdiv');
									showSection('#pv2iddiv');
								}
								if($('#pv2wattmodul').val() == 'wr2_ethsdm120') {
									showSection('#pv2ipdiv');
									showSection('#pv2iddiv');
								}
							}
							$(function() {
								display_pv2wattmodul();

								$('#pv2wattmodul').change( function(){
									display_pv2wattmodul();
								} );
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
			<form id="wizzarddoneForm" action="settings/saveconfig.php" method="POST">
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
					$('#navModulkonfigurationPv').addClass('disabled');

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
