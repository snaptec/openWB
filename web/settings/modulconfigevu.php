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
			<h1>Modulkonfiguration EVU</h1>
			<form action="settings/saveconfig.php" method="POST">

				<!-- EVU -->
				<div class="card border-danger">
					<div class="card-header bg-danger">
						Strombezugsmessmodul (EVU-Übergabepunkt)
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<label for="wattbezugmodul" class="col-md-4 col-form-label">Strombezugsmodul</label>
							<div class="col">
								<select name="wattbezugmodul" id="wattbezugmodul" class="form-control">
									<option <?php if($wattbezugmodulold == "none") echo "selected" ?> value="none">Nicht vorhanden</option>
									<optgroup label="openWB">
										<option <?php if($wattbezugmodulold == "bezug_ethmpm3pm") echo "selected" ?> value="bezug_ethmpm3pm">openWB EVU Kit</option>
									</optgroup>
									<optgroup label="andere Hersteller">
										<option <?php if($wattbezugmodulold == "bezug_alphaess") echo "selected" ?> value="bezug_alphaess">Alpha ESS</option>
										<option <?php if($wattbezugmodulold == "bezug_batterx") echo "selected" ?> value="bezug_batterx">BatterX</option>
										<option <?php if($wattbezugmodulold == "bezug_carlogavazzilan") echo "selected" ?> value="bezug_carlogavazzilan">Carlo Gavazzi EM24 LAN</option>
										<option <?php if($wattbezugmodulold == "bezug_discovergy") echo "selected" ?> value="bezug_discovergy">Discovergy</option>
										<option <?php if($wattbezugmodulold == "bezug_e3dc") echo "selected" ?> value="bezug_e3dc">E3DC Speicher</option>
										<option <?php if($wattbezugmodulold == "bezug_enphase") echo "selected" ?> value="bezug_enphase">Enphase Envoy / IQ Gateway</option>
										<option <?php if($wattbezugmodulold == "bezug_fronius_sm") echo "selected" ?> value="bezug_fronius_sm">Fronius Energy Meter</option>
										<option <?php if($wattbezugmodulold == "bezug_fronius_s0") echo "selected" ?> value="bezug_fronius_s0">Fronius WR mit S0 Meter</option>
										<option <?php if($wattbezugmodulold == "bezug_good_we") echo "selected" ?> value="bezug_good_we">GoodWe</option>
										<option <?php if($wattbezugmodulold == "bezug_huawei") echo "selected" ?> value="bezug_huawei">Huawei mit SmartMeter</option>
										<option <?php if($wattbezugmodulold == "bezug_kostalpiko") echo "selected" ?> value="bezug_kostalpiko">Kostal Piko mit Energy Meter</option>
										<option <?php if($wattbezugmodulold == "bezug_kostalplenticoreem300haus") echo "selected" ?> value="bezug_kostalplenticoreem300haus">Kostal Plenticore mit EM300/KSEM</option>
										<option <?php if($wattbezugmodulold == "bezug_ksem") echo selected ?> value="bezug_ksem">Kostal Smart Energy Meter oder TQ EM410</option>
										<option <?php if($wattbezugmodulold == "bezug_lgessv1") echo "selected" ?> value="bezug_lgessv1">LG ESS 1.0VI</option>
										<option <?php if($wattbezugmodulold == "bezug_janitza") echo "selected" ?> value="bezug_janitza">Janitza</option>
										<option <?php if($wattbezugmodulold == "bezug_fems") echo "selected" ?> value="bezug_fems">openEMS / Fenecon FEMS / Kaco Hy-Control</option>
										<option <?php if($wattbezugmodulold == "bezug_powerdog") echo "selected" ?> value="bezug_powerdog">Powerdog</option>
										<option <?php if($wattbezugmodulold == "bezug_powerfox") echo "selected" ?> value="bezug_powerfox">Powerfox</option>
										<option <?php if($wattbezugmodulold == "bezug_rct") echo "selected" ?> value="bezug_rct">RCT</option>
										<option <?php if($wattbezugmodulold == "bezug_rct2") echo "selected" ?> value="bezug_rct2">RCT V.2</option>
										<option <?php if($wattbezugmodulold == "bezug_siemens") echo "selected" ?> value="bezug_siemens">Siemens Speicher</option>
										<option <?php if($wattbezugmodulold == "bezug_siemens_sentron") echo "selected" ?> value="bezug_siemens_sentron">Siemens SENTRON</option>
										<option <?php if($wattbezugmodulold == "bezug_smashm") echo "selected" ?> value="bezug_smashm">SMA HomeManager</option>
										<option <?php if($wattbezugmodulold == "bezug_sbs25") echo "selected" ?> value="bezug_sbs25">SMA Sunny Boy Storage </option>
										<option <?php if($wattbezugmodulold == "bezug_smartfox") echo "selected" ?> value="bezug_smartfox">Smartfox</option>
										<option <?php if($wattbezugmodulold == "bezug_smartme") echo "selected" ?> value="bezug_smartme">Smartme</option>
										<option <?php if($wattbezugmodulold == "bezug_solaredge") echo "selected" ?> value="bezug_solaredge">Solaredge</option>
										<option <?php if($wattbezugmodulold == "bezug_solarlog") echo "selected" ?> value="bezug_solarlog">SolarLog</option>
										<option <?php if($wattbezugmodulold == "bezug_solarview") echo "selected" ?> value="bezug_solarview">Solarview</option>
										<option <?php if($wattbezugmodulold == "bezug_solarwatt") echo "selected" ?> value="bezug_solarwatt">Solarwatt / My Reserve Speicher</option>
										<option <?php if($wattbezugmodulold == "bezug_solarworld") echo "selected" ?> value="bezug_solarworld">Solarworld</option>
										<option <?php if($wattbezugmodulold == "bezug_solax") echo "selected" ?> value="bezug_solax">Solax</option>
										<option <?php if($wattbezugmodulold == "bezug_sonneneco") echo "selected" ?> value="bezug_sonneneco">Sonnen eco</option>
										<option <?php if($wattbezugmodulold == "bezug_sungrow") echo "selected" ?> value="bezug_sungrow">Sungrow</option>
										<option <?php if($wattbezugmodulold == "bezug_powerwall") echo "selected" ?> value="bezug_powerwall">Tesla Powerwall</option>
										<option <?php if($wattbezugmodulold == "bezug_varta") echo "selected" ?> value="bezug_varta">Varta Speicher</option>
										<option <?php if($wattbezugmodulold == "bezug_victrongx") echo "selected" ?> value="bezug_victrongx">Victron (z.B. GX)</option>
									</optgroup>
									<optgroup label="generische Module">
										<option <?php if($wattbezugmodulold == "bezug_http") echo "selected" ?> value="bezug_http">HTTP</option>
										<option <?php if($wattbezugmodulold == "bezug_json") echo "selected" ?> value="bezug_json">Json</option>
										<option <?php if($wattbezugmodulold == "bezug_mpm3pm") echo "selected" ?> value="bezug_mpm3pm">MPM3PM</option>
										<option <?php if($wattbezugmodulold == "bezug_mqtt") echo "selected" ?> value="bezug_mqtt">MQTT</option>
										<option <?php if($wattbezugmodulold == "sdm630modbusbezug") echo "selected" ?> value="sdm630modbusbezug">SDM 630</option>
										<option <?php if($wattbezugmodulold == "bezug_ethmpm3pmflex") echo "selected" ?> value="bezug_ethmpm3pmflex">openWB EVU Kit flexible IP</option>
										<option <?php if($wattbezugmodulold == "vzlogger") echo "selected" ?> value="vzlogger">VZLogger</option>
									</optgroup>
								</select>
							</div>
						</div>
						<div id="wattbezugalphaess" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich.
							</div>
						</div>
						<div id="wattbezuggoodwe" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im Wechselrichter
							</div>
						</div>
						<div id="wattbezugbatterx" class="hide">
							<div class="form-row mb-1">
								<label for="batterx_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="batterx_ip" id="batterx_ip" value="<?php echo $batterx_ipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsungrow" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen PV-Modul 1 mit Auswahl "Sungrow" erforderlich!
							</div>
						</div>
						<div id="wattbezugsonneneco" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Alle Einstellungen werden in dem Speicher-Modul vorgenommen.
							</div>
							<div class="card-text alert alert-warning">
								Die EVU-Leistung steht nur in den Varianten "Rest-API 2" und "JSON-API" zur Verfügung!<br />
								Mit diesem Modul ist kein Lastmanagement möglich, da keine Ströme der einzelnen Phasen gemessen werden!
							</div>
						</div>
						<div id="wattbezugvarta" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Es muss beim Speicher Varta ausgewählt werden.
							</div>
						</div>
						<div id="wattbezugjanitza" class="hide">
							<div class="card-text alert alert-info">
								Ausgelesen wird Register 19026 auf Port 502. ModbusTCP muss im Janitza aktiv sein und die ID 1 vergeben sein.
							</div>
						</div>
						<div id="wattbezugcarlogavazzilan" class="hide">
							<div class="card-text alert alert-info">
								Ausgelesen wird ID 1 auf Port 502. ModbusTCP muss aktiviert sein.
							</div>
						</div>

						<div id="wattbezugsolarwatt" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Es muss beim Speicher Solarwatt / My Reserve ausgewählt werden.
							</div>
						</div>
						<div id="wattbezugmqtt" class="hide">
							<div class="alert alert-info">
								Keine Konfiguration erforderlich.<br>
								Per MQTT zu schreiben:<br>
								<span class="text-info">openWB/set/evu/W</span> Bezugsleistung in Watt, int, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/APhase1</span> Strom in Ampere für Phase 1, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/APhase2</span> Strom in Ampere für Phase 2, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/APhase3</span> Strom in Ampere für Phase 3, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/WhImported</span> Bezogene Energie in Wh, float, Punkt als Trenner, nur positiv<br>
								<span class="text-info">openWB/set/evu/WhExported</span> Eingespeiste Energie in Wh, float, Punkt als Trenner, nur positiv<br>
								<span class="text-info">openWB/set/evu/VPhase1</span> Spannung in Volt für Phase 1, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/VPhase2</span> Spannung in Volt für Phase 2, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/VPhase3</span> Spannung in Volt für Phase 3, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/HzFrequenz</span> oder <span class="text-info">openWB/set/evu/Hz</span> Netzfrequenz in Hz, float, Punkt als Trenner<br>
								<span class="text-info">openWB/set/evu/WPhase1</span> Leistung in Watt für Phase 1, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/WPhase2</span> Leistung in Watt für Phase 2, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/WPhase3</span> Leistung in Watt für Phase 3, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/PfPhase1</span> Powerfaktor für Phase 1, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/PfPhase2</span> Powerfaktor für Phase 2, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung<br>
								<span class="text-info">openWB/set/evu/PfPhase3</span> Powerfaktor für Phase 3, float, Punkt als Trenner, positiv Bezug, negativ Einspeisung
							</div>
						</div>
						<div id="wattbezuglgessv1" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen Speichermodul des LG ESS 1.0VI erforderlich. Als PV-Modul auch LG ESS 1.0VI wählen!
							</div>
						</div>
						<div id="wattbezugip" class="hide">
							<div class="form-row mb-1">
								<label for="bezug1_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug1_ip" id="bezug1_ip" value="<?php echo $bezug1_ipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsiemens" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse des Siemens Speichers eingeben. Im Siemens Speicher muss die Schnittstelle openWB gewählt werden.
							</div>
						</div>
						<div id="wattbezugsiemenssentron" class="hide">
							<div class="card-text alert alert-info">
								Derzeit werden nur Messgeräte vom Typ "7KM PAC2200" mit Ethernet-Schnittstelle unterstützt.
							</div>
						</div>
						<div id="wattbezugrct" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse des RCT Speichers eingeben.
							</div>
						</div>
						<div id="wattbezughuawei" class="hide">
							<div class="card-text alert alert-danger">
								Es muss zwingend auch das Huawei PV Modul konfiguriert werden, da alle Daten dort abgerufen werden!
							</div>
						</div>

						<div id="wattbezugpowerdog" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse des Powerdog eingeben. Im Powerdog muss die Schnittstelle ModbusTCP aktiviert werden.
							</div>
						</div>
						
						<div id="wattbezugpowerfox" class="hide">
							<div class="form-row mb-1">
								<label for="powerfoxuser" class="col-md-4 col-form-label">powerfox Username (Email)</label>
								<div class="col">
									<input class="form-control" type="email" name="powerfoxuser" id="powerfoxuser" value="<?php echo htmlspecialchars($powerfoxuserold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="powerfoxpass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="powerfoxpass" id="powerfoxpass" value="<?php echo htmlspecialchars($powerfoxpassold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="powerfoxid" class="col-md-4 col-form-label">Device ID</label>
								<div class="col">
									<input class="form-control" type="text" name="powerfoxid" id="powerfoxid" value="<?php echo $powerfoxidold ?>">
									<span class="form-text small">
										Gültige Werte Device ID. Um die Device ID herauszufinden mit dem Browser die Adresse "https://backend.powerfox.energy/api/2.0/my/all/devices" aufrufen und dort Benutzername und Passwort eingeben.
										Die Device ID ist exakt so einzutragen, wie in der Antwort des Servers. Das bedeutet insbesondere auch die Groß-/KLeinschreibung ist zu beachten!
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugethmpm3pm" class="hide">
							<div class="form-row mb-1">
								<label for="evukitversion" class="col-md-4 col-form-label">Version des openWB evu Kits</label>
								<div class="col">
									<select name="evukitversion" id="evukitversion" class="form-control">
										<option <?php if($evukitversionold == 0) echo "selected" ?> value="0">EVU Kit MPM3PM</option>
										<option <?php if($evukitversionold == 1) echo "selected" ?> value="1">EVU Kit var 2 Lovato</option>
										<option <?php if($evukitversionold == 2) echo "selected" ?> value="2">EVU Kit SDM</option>
									</select>
								</div>
							</div>
						</div>
						<div id="wattbezugethmpm3pmflex" class="hide">
							<div class="form-row mb-1">
								<label for="evuflexversion" class="col-md-4 col-form-label">Version des openWB evu Kits</label>
								<div class="col">
									<select name="evuflexversion" id="evuflexversion" class="form-control">
										<option <?php if($evuflexversionold == 0) echo "selected" ?> value="0">EVU Kit MPM3PM</option>
										<option <?php if($evuflexversionold == 1) echo "selected" ?> value="1">EVU Kit var 2 Lovato</option>
										<option <?php if($evuflexversionold == 2) echo "selected" ?> value="2">EVU Kit SDM</option>
									</select>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="evuflexip" class="col-md-4 col-form-label">EVU Adapter IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="evuflexip" id="evuflexip" value="<?php echo $evuflexipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Protoss/Elfin Adapters.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="evuflexport" class="col-md-4 col-form-label">Port</label>
								<div class="col">
									<input class="form-control" type="number" min="1" step="1" name="evuflexport" id="evuflexport" value="<?php echo (empty($evuflexportold)?'502':$evuflexportold) ?>">
									<span class="form-text small">
										TCP Port der im Protoss/Elfin konfiguriert ist.<br>
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
									<label for="evuflexid" class="col-md-4 col-form-label">Unit ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="evuflexid" id="evuflexid" value="<?php echo $evuflexidold ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID des Gerätes.</span>
									</div>
								</div>
						</div>
						<div id="wattbezugsolarview" class="hide">
							<div class="card-text alert alert-info">
								Konfiguration im zugehörigen PV Modul erforderlich.
							</div>
						</div>
						<div id="wattbezugpowerwall" class="hide">
							<div class="card-text alert alert-info">
								Keine Konfiguration erforderlich. Mit diesem Modul ist kein Lastmanagement / Hausanschlussüberwachung möglich.
							</div>
						</div>
						<div id="wattbezugvictrongx" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_victronip" class="col-md-4 col-form-label">Victron IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug_victronip" id="bezug_victronip" value="<?php echo $bezug_victronipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Victron, z.B. GX.
									</span>
								</div>
							</div>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Messgerät</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($victron_energy_meterold == 1) echo " active" ?>">
												<input type="radio" name="victron_energy_meter" id="victron_energy_meterOn" value="1"<?php if($victron_energy_meterold == 1) echo " checked=\"checked\"" ?>>Energy Meter
											</label>
											<label class="btn btn-outline-info<?php if($victron_energy_meterold == 0) echo " active" ?>">
												<input type="radio" name="victron_energy_meter" id="victron_energy_meterOff" value="0"<?php if($victron_energy_meterold == 0) echo " checked=\"checked\"" ?>>AC-In Victron GX
											</label>
										</div>
									</div>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="bezug_id" class="col-md-4 col-form-label">ID</label>
								<div class="col">
									<input class="form-control" type="text" name="bezug_id" id="bezug_id" value="<?php echo $bezug_idold ?>">
									<span class="form-text small">Gültige Werte ID. Modbus-ID</span>
								</div>
							</div>
						</div>
						<div id="wattbezugfems" class="hide">
							<div class="form-row mb-1">
								<label for="femsip" class="col-md-4 col-form-label">Fenecon IP</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="femsip" id="femsip" value="<?php echo $femsipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Fenecon FEMS.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="femskacopw" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="femskacopw" id="femskacopw" value="<?php echo htmlspecialchars($femskacopwold) ?>">
									<span class="form-text small">
										Bei Nutzung von Fenecon FEMS ist das Passwort im Normalfall user, bei Kaco mit Hy-Control ist das Passwort meist admin.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsolarworld" class="hide">
							<div class="form-row mb-1">
								<label for="solarworld_emanagerip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solarworld_emanagerip" id="solarworld_emanagerip" value="<?php echo $solarworld_emanageripold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12<br>
										IP Adresse des Solarworld eManager.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugdiscovergy" class="hide">
							<div class="form-row mb-1">
								<label for="discovergyuser" class="col-md-4 col-form-label">Discovergy Username (Email)</label>
								<div class="col">
									<input class="form-control" type="email" name="discovergyuser" id="discovergyuser" value="<?php echo htmlspecialchars($discovergyuserold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="discovergypass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="discovergypass" id="discovergypass" value="<?php echo htmlspecialchars($discovergypassold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="discovergyevuid" class="col-md-4 col-form-label">Meter ID</label>
								<div class="col">
									<input class="form-control" type="text" name="discovergyevuid" id="discovergyevuid" value="<?php echo $discovergyevuidold ?>">
									<span class="form-text small">
										Gültige Werte ID. Um die ID herauszufinden mit dem Browser die Adresse "https://api.discovergy.com/public/v1/meters" aufrufen und dort Benutzername und Passwort eingeben.
										Hier wird nun u.a. die ID des Zählers angezeigt.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugkostalsmartenergymeter" class="hide">
							<div class="form-row mb-1">
								<label for="ksemip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="ksemip" id="ksemip" value="<?php echo $ksemipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugkostalpiko" class="hide">
							<div class="card-text alert alert-info">
								IP Adresse wird im PV Modul konfiguriert. Angeschlossenes Meter erforderlich. Der WR liefert Werte nur solange er auch PV Leistung liefert. Nachts geht er in den Standby.
								Die Hausanschlussüberwachung ist nur aktiv wenn der Wechselrichter auch aktiv ist. Ein extra PV-Modul muss nicht mehr ausgewählt werden.
							</div>
						</div>
						<div id="wattbezugplentihaus" class="hide">
							<div class="card-text alert alert-info">
								Dieses Modul erfordert als 1. PV-Modul das Modul "Kostal Plenticore". Dieses wird automatisch fest eingestellt. Der EM300 bzw. das KSEM muss am 1. Plenticore angeschlossen sein.
								Ein am 1. Plenticore angeschlossener Speicher wird ebenfalls ohne weitere Einstellung ausgelesen, das Speicher-Modul wird dazu entsprechend voreingestellt.
								Am 2. Plenticore darf kein Speicher angeschlossen sein, da dies die weiteren Berechnungen verfälscht.
								Die Einbauposition des EM300/KSEM (Hausverbrauchs-Zweig = Pos. 1 oder Netzanschluss-Zweig = Pos. 2) ist anzugeben.
							</div>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Einbauposition</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($kostalplenticorehausold == 0) echo " active" ?>">
												<input type="radio" name="kostalplenticorehaus" id="kostalplenticorehausOff" value="0"<?php if($kostalplenticorehausold == 0) echo " checked=\"checked\"" ?>>Pos. 1
											</label>
											<label class="btn btn-outline-info<?php if($kostalplenticorehausold == 1) echo " active" ?>">
												<input type="radio" name="kostalplenticorehaus" id="kostalplenticorehausOn" value="1"<?php if($kostalplenticorehausold == 1) echo " checked=\"checked\"" ?>>Pos. 2
											</label>
										</div>
										<span class="form-text small">
											Hausverbrauchs-Zweig = Pos. 1 oder Netzanschluss-Zweig = Pos. 2
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugmpm3pm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="mpm3pmevusource" class="col-md-4 col-form-label">MPM3PM Zähler EVU Source</label>
									<div class="col">
										<input class="form-control" type="text" name="mpm3pmevusource" id="mpm3pmevusource" value="<?php echo $mpm3pmevusourceold ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSB0, /dev/virtualcomX. Serieller Port an dem der MPM3PM in der Wallbox angeschlossen ist. Meist /dev/ttyUSB0<br>
											Nach ändern der Einstellung von ttyUSB auf virtualcom0 ist ein Neustart erforderlich.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mpm3pmevuid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="mpm3pmevuid" id="mpm3pmevuid" value="<?php echo $mpm3pmevuidold ?>">
										<span class="form-text small">Gültige Werte 1-254. Modbus ID des MPM3PM.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Einbauposition</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($mpm3pmevuhausold == 0) echo " active" ?>">
												<input type="radio" name="mpm3pmevuhaus" id="mpm3pmevuhausOff" value="0"<?php if($mpm3pmevuhausold == 0) echo " checked=\"checked\"" ?>>Pos. 1
											</label>
											<label class="btn btn-outline-info<?php if($mpm3pmevuhausold == 1) echo " active" ?>">
												<input type="radio" name="mpm3pmevuhaus" id="mpm3pmevuhausOn" value="1"<?php if($mpm3pmevuhausold == 1) echo " checked=\"checked\"" ?>>Pos. 2
											</label>
										</div>
										<span class="form-text small">
											Wenn der MPM3PM EVU Zähler im Hausverbrauchszweig NACH den Ladepunkten angeschlossen ist, Pos. 2 auswählen.
											Z.B. auch zu nutzen wenn der Ladepunkt an einem seperaten Rundsteuerempfänger(=extra Zähler) angeschlossen ist.
											Bei gesetzter Pos. 2 werden die Ladeströme der Ladepunkte zu den Strömen gemessen am EVU Zähler hinzuaddiert.
											Somit ist ein Lastmanagement / Hausanschlussüberwachung möglich. Auf korrekte Verkabelung ist zu achten!<br>
											EVU L1, LP1 L1, LP2 L2<br>
											EVU L2, LP1 L2, LP2 L3<br>
											EVU L3, LP1 L3, LP2 L1
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugnone" class="hide">
							<div class="form-row mb-1">
								<label for="hausbezugnone" class="col-md-4 col-form-label">Angenommener Hausverbrauch</label>
								<div class="col">
									<input class="form-control" type="number" min="0" step="100" name="hausbezugnone" id="hausbezugnone" value="<?php echo htmlspecialchars($hausbezugnoneold) ?>">
									<span class="form-text small">
										Gültige Werte Zahl. Wenn keine EVU Messung vorhanden ist kann hier ein Hausgrundverbrauch festgelegt werden.
										Daraus resultierend agiert die PV Regelung bei vorhandenem PV-Modul
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsdm" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="sdm630modbusbezugsource" class="col-md-4 col-form-label">SDM Zähler EVU Source</label>
									<div class="col">
										<input class="form-control" type="text" name="sdm630modbusbezugsource" id="sdm630modbusbezugsource" value="<?php echo $sdm630modbusbezugsourceold ?>">
										<span class="form-text small">
											Gültige Werte /dev/ttyUSBx, /dev/virtualcomx. Das "x" steht für den Adapter. Dies kann 0,1,2, usw sein. Serieller Port an dem der SDM angeschlossen ist.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbusbezugid" class="col-md-4 col-form-label">ID</label>
									<div class="col">
										<input class="form-control" type="number" min="1" max="254" step="1" name="sdm630modbusbezugid" id="sdm630modbusbezugid" value="<?php echo $sdm630modbusbezugidold ?>">
										<span class="form-text small">
											Gültige Werte 1-254. Modbus ID des SDM. Getestet sind SDM230 & SDM630v2.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="sdm630modbusbezuglanip" class="col-md-4 col-form-label">RS485/Lan-Konverter IP Adresse</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="sdm630modbusbezuglanip" id="sdm630modbusbezuglanip" value="<?php echo $sdm630modbusbezuglanipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Modbus/Lan Konverter. Ist die Source "virtualcomX" wird automatisch ein Lan Konverter genutzt.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugvz" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="vzloggerip" class="col-md-4 col-form-label">Vzlogger IP Adresse inkl Port</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5]):[0-9]+$" name="vzloggerip" id="vzloggerip" value="<?php echo $vzloggeripold ?>">
										<span class="form-text small">
											Gültige Werte IP:Port z.B. 192.168.0.12:8080
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="vzloggerline" class="col-md-4 col-form-label">Vzlogger Watt Zeile</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="vzloggerline" id="vzloggerline" value="<?php echo $vzloggerlineold ?>">
										<span class="form-text small">
											Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq .|cat -n"<br>
											Nun zählen in welcher Zeile die aktullen Watt stehen und diesen hier eintragen.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="vzloggerkwhline" class="col-md-4 col-form-label">Vzlogger Bezug Wh Zeile</label>
									<div class="col">
										<input class="form-control" type="text" name="vzloggerkwhline" id="vzloggerkwhline" value="<?php echo $vzloggerkwhlineold ?>">
										<span class="form-text small">
											Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq .|cat -n"<br>
											Nun zählen in welcher Zeile die Gesamt Wh stehen und diesen hier eintragen. Der Wert dient rein dem Logging.
											Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="vzloggerekwhline" class="col-md-4 col-form-label">Vzlogger Einspeisung Wh Zeile</label>
									<div class="col">
										<input class="form-control" type="text" name="vzloggerekwhline" id="vzloggerekwhline" value="<?php echo $vzloggerekwhlineold ?>">
										<span class="form-text small">
											Gültige Werte z.B. Zahl. Bitte auf der Shell ausführen: "curl -s IPdesVZLogger:Port/ | jq .|cat -n"<br>
											Nun zählen in welcher Zeile die Gesamt eingespeisten Wh stehen und diesen hier eintragen.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezughttp" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="bezug_http_w_url" class="col-md-4 col-form-label">Vollständige URL für den Watt Bezug</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_w_url" id="bezug_http_w_url" value="<?php echo htmlspecialchars($bezug_http_w_urlold) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Watt sein.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_ikwh_url" class="col-md-4 col-form-label">Vollständige URL für den Wh Bezug</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_ikwh_url" id="bezug_http_ikwh_url" value="<?php echo htmlspecialchars($bezug_http_ikwh_urlold) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_ekwh_url" class="col-md-4 col-form-label">Vollständige URL für die Wh Einspeisung</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_ekwh_url" id="bezug_http_ekwh_url" value="<?php echo htmlspecialchars($bezug_http_ekwh_urlold) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Der Wert muss in WattStunden sein. Der Wert dient rein dem Logging. Wird dieses nicht genutzt oder ist der Wert nicht verfügbar bitte auf "none" setzen, dann wird die Abfrage nicht ausgeführt.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_l1_url" class="col-md-4 col-form-label">Vollständige URL für die Ampere Phase 1</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_l1_url" id="bezug_http_l1_url" value="<?php echo htmlspecialchars($bezug_http_l1_urlold) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_l2_url" class="col-md-4 col-form-label">Vollständige URL für die Ampere Phase 2</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_l2_url" id="bezug_http_l2_url" value="<?php echo htmlspecialchars($bezug_http_l2_urlold) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezug_http_l3_url" class="col-md-4 col-form-label">Vollständige URL für die Ampere Phase 3</label>
									<div class="col">
										<input class="form-control" type="text" name="bezug_http_l3_url" id="bezug_http_l3_url" value="<?php echo htmlspecialchars($bezug_http_l3_urlold) ?>">
										<span class="form-text small">
											Gültige Werte vollständige URL. Die abgerufene Url muss eine reine Zahl zurückgeben. Enthält der Rückgabewert etwas anderes als "-" (für Einspeisung) oder "0-9" wird der Wert auf null gesetzt. Der Wert muss in Ampere sein. Bei nicht Nutzung auf none setzen.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugsmartme" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_smartme_user" class="col-md-4 col-form-label">Smartme Benutzername</label>
								<div class="col">
									<input class="form-control" type="text" name="bezug_smartme_user" id="bezug_smartme_user" value="<?php echo htmlspecialchars($bezug_smartme_userold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="bezug_smartme_pass" class="col-md-4 col-form-label">Passwort</label>
								<div class="col">
									<input class="form-control" type="password" name="bezug_smartme_pass" id="bezug_smartme_pass" value="<?php echo htmlspecialchars($bezug_smartme_passold) ?>">
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="bezug_smartme_url" class="col-md-4 col-form-label">Smartme Url</label>
								<div class="col">
									<input class="form-control" type="text" name="bezug_smartme_url" id="bezug_smartme_url" value="<?php echo $bezug_smartme_urlold ?>">
								</div>
							</div>
						</div>
						<div id="wattbezugshm" class="hide">
							<div class="form-row mb-1">
								<label for="smashmbezugid" class="col-md-4 col-form-label">Seriennummer</label>
								<div class="col">
									<input class="form-control" type="text" name="smashmbezugid" id="smashmbezugid" value="<?php echo $smashmbezugidold ?>">
									<span class="form-text small">
										Gültige Werte: Seriennummer. Hier die Seriennummer des SMA Meter für Bezug/Einspeisung anzugeben.
										Ist nur erforderlich wenn mehrere SMA HomeManager in Betrieb sind, ansonsten none eintragen. Funktioniert auch mit Energy Meter statt Home Manager.
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsmartfox" class="hide">
							<div class="form-row mb-1">
								<label for="bezug_smartfox_ip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="bezug_smartfox_ip" id="bezug_smartfox_ip" value="<?php echo $bezug_smartfox_ipold ?>">
									<span class="form-text small">
										Gültige Werte IP Adresse im Format: 192.168.0.12
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsma" class="hide">
							<div class="form-row mb-1">
								<label for="smaemdbezugid" class="col-md-4 col-form-label">Seriennummer des SMA Energy Meter</label>
								<div class="col">
									<input class="form-control" type="text" name="smaemdbezugid" id="smaemdbezugid" value="<?php echo $smaemdbezugidold ?>">
									<span class="form-text small">
										Gültige Werte Seriennummer. Hier die Seriennummer des SMA Meter für Bezug/Einspeisung angeben<br>
										Infos zum SMA Energy Meter <a href="https://github.com/snaptec/openWB#extras">HIER</a>
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugfronius" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="wrfroniusip" class="col-md-4 col-form-label">Fronius IP</label>
									<div class="col">
										<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="wrfroniusip" id="wrfroniusip" value="<?php echo $wrfroniusipold ?>">
										<span class="form-text small">
											Gültige Werte IP Adresse im Format: 192.168.0.12<br>
											IP Adresse des Fronius WR.
										</span>
										<button id="wattbezugfroniusload" class="btn btn-primary" type="button">Daten auslesen</button>
										<button id="wattbezugfroniusmanual" class="btn btn-primary hide" type="button">Daten manuell eingeben</button>
										<span id="wattbezugfroniusloadmessage" class="form-text small"></span>
									</div>
								</div>
								<div id="wattbezugfroniusmeterid" class="form-row mb-1">
									<label class="col-md-4 col-form-label">Energymeter ID</label>
									<div class="col">
										<input class="form-control" type="number" min="0" max="65535" step="1" name="froniuserzeugung" id="froniuserzeugung"value="<?php echo $froniuserzeugungold ?>">
									</div>
								</div>
								<div id="wattbezugfroniusmeterlist" class="form-row mb-1 hide">
									<label class="col-md-4 col-form-label">Energymeter</label>
									<div class="col">
										<select name="froniuserzeugung" id="froniuserzeugungselect" class="form-control"<?php if (isset($froniuserzeugungold)) echo " data-old=\"$froniuserzeugungold\"" ?>>
											<option>Nicht ermittelbar</option>
										</select>
									</div>
								</div>
								<hr>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kompatibilitätsmodus für Gen24 / neuere Symo</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($froniusvar2old == 0) echo " active" ?>">
												<input type="radio" name="froniusvar2" id="froniusvar2Off" value="0"<?php if($froniusvar2old == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if($froniusvar2old == 1) echo " active" ?>">
												<input type="radio" name="froniusvar2" id="froniusvar2v1" value="1"<?php if($froniusvar2old == 1) echo " checked=\"checked\"" ?>>Variante 1
											</label>
											<label class="btn btn-outline-info<?php if($froniusvar2old == 2) echo " active" ?>">
												<input type="radio" name="froniusvar2" id="froniusvar2v2" value="2"<?php if($froniusvar2old == 2) echo " checked=\"checked\"" ?>>Variante 2
											</label>

										</div>
										<span class="form-text small">
											Gegebenenfalls auch für alte Modelle nach einem Softwareupdate erforderlich. Fronius hat derzeit keine Konsistente Schnittstelle. Speziell beim Gen24 kann Variante 1 oder 2 erforderlich sein. Nach speichern sollten nach etwa 10-20 Sekunden Daten angezeigt werden. Ist dies nicht der Fall die andere Variante ausprobieren.
										</span>
									</div>
								</div>
							</div>
							<script>
								// load meter data from Fronius inverter
								$(document).ready(function(){
									$('#wattbezugfroniusload').on("click",function() {
										$('#wattbezugfroniusload').attr("disabled", true);
										$('#wattbezugfroniusloadmessage').text("Lade Daten...");
										$.getJSON('/openWB/modules/bezug_fronius_sm/froniusloadmeterdata.php?ip=' + $('#wrfroniusip').val(), function(data) {
											var options = '';
											// fill listbox, format <manufacturer> <meter model> (<serial>)
											for(var i in data.Body.Data) {
												var meter = data.Body.Data[i];
												options += '<option value="'+i+'"'
												if($('#froniuserzeugungselect').attr("data-old") == i) {
													options += ' selected=true';
												}
												options += '>';
												options += meter.Details.Manufacturer+' '+meter.Details.Model;
												options += ' ('+meter.Details.Serial+')';
												options += '</option>';
											}
											$('#froniuserzeugungselect').html(options);
											$('#wattbezugfroniusloadmessage').text("");

											// set meter id corresponding to displayed entry in listbox
											setInputValue('froniuserzeugung', $('#froniuserzeugungselect option:selected').attr('value'));

											hideSection('#wattbezugfroniusload')
											hideSection('#wattbezugfroniusmeterid');
											showSection('#wattbezugfroniusmanual')
											showSection('#wattbezugfroniusmeterlist');
										})
										.fail(function(jqXHR, textStatus, errorThrown) {
											var errorMsg = 'Die Daten konnten nicht abgerufen werden. Eingabe pr&uuml;fen oder Daten manuell eingeben.';
											if(jqXHR.responseText !== "") {
												errorMsg += '<br>';
												errorMsg += jqXHR.responseText;
											}
											$('#wattbezugfroniusloadmessage').html(errorMsg);
										})
										.always(function() {
											$('#wattbezugfroniusload').attr("disabled", false);
										});

									});

									$('#wattbezugfroniusmanual').on("click",function() {
										// switch back to default configuration form
										hideSection('#wattbezugfroniusmanual')
										hideSection('#wattbezugfroniusmeterlist');
										showSection('#wattbezugfroniusload')
										showSection('#wattbezugfroniusmeterid');
									});

									$('#froniuserzeugungselect').change(function() {
										// on change entry of listbox, set corresponding meter id
										setInputValue('froniuserzeugung', $('#froniuserzeugungselect option:selected').attr('value'));
										// on change entry of listbox, set corresponding meter location
										setToggleBtnGroup('froniusmeterlocation', $('#froniuserzeugungselect option:selected').attr('data-meterlocation'));
									});
								});
							</script>
						</div>
						<div id="wattbezugjson" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="bezugjsonurl" class="col-md-4 col-form-label">Bezug URL</label>
									<div class="col">
										<input class="form-control" type="text" name="bezugjsonurl" id="bezugjsonurl" value="<?php echo htmlspecialchars($bezugjsonurlold) ?>">
										<span class="form-text small">
											Gültige Werte URL. Vollständige URL die die Json Antwort enthält.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezugjsonwatt" class="col-md-4 col-form-label">Json Abfrage für Watt</label>
									<div class="col">
										<input class="form-control" type="text" name="bezugjsonwatt" id="bezugjsonwatt" value="<?php echo htmlspecialchars($bezugjsonwattold) ?>">
										<span class="form-text small">
											Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
											Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> so muss hier <span class="text-info">.PowerOut</span> eingetragen werden.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="bezugjsonkwh" class="col-md-4 col-form-label">Json Abfrage für Bezug Wh</label>
									<div class="col">
										<input class="form-control" type="text" name="bezugjsonkwh" id="bezugjsonkwh" value="<?php echo htmlspecialchars($bezugjsonkwhold) ?>">
										<span class="form-text small">
											Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
											Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> so muss hier <span class="text-info">.PowerProduced</span> eingetragen werden.
										</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="einspeisungjsonkwh" class="col-md-4 col-form-label">Json Abfrage für Einspeisung Wh</label>
									<div class="col">
										<input class="form-control" type="text" name="einspeisungjsonkwh" id="einspeisungjsonkwh" value="<?php echo htmlspecialchars($einspeisungjsonkwhold) ?>">
										<span class="form-text small">
											Der hier eingetragene Befehl reduziert die Json Abfrage auf das wesentliche. Im Hintergrund wird der Befehl jq benutzt.<br>
											Ist die Json Antwort z.B. <span class="text-info">{"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428}</span> so muss hier <span class="text-info">.PowerSelfSupplied</span> eingetragen werden.
										</span>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugsolarlog" class="hide">
							<div class="card-text alert alert-info">
								Die zugehörige IP Adresse ist im PV Modul einzustellen.
							</div>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Kompatibilitätsmodus bei vorhandenem Speicher</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($bezug_solarlog_speichervold == 0) echo " active" ?>">
												<input type="radio" name="bezug_solarlog_speicherv" id="bezug_solarlog_speichervOff" value="0"<?php if($bezug_solarlog_speichervold == 0) echo " checked=\"checked\"" ?>>Nein
											</label>
											<label class="btn btn-outline-info<?php if($bezug_solarlog_speichervold == 1) echo " active" ?>">
												<input type="radio" name="bezug_solarlog_speicherv" id="bezug_solarlog_speichervOn" value="1"<?php if($bezug_solarlog_speichervold == 1) echo " checked=\"checked\"" ?>>Ja
											</label>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div id="wattbezugsolaredge" class="hide">
							<div class="form-row mb-1">
								<label for="solaredgeip" class="col-md-4 col-form-label">IP Adresse</label>
								<div class="col">
									<input class="form-control" type="text" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$" name="solaredgeip" id="solaredgeip" value="<?php echo $solaredgeipold ?>">
									<span class="form-text small">
										IP Adresse des Solaredge Wechselrichters im lokalen Netzwerk.<br>
										Hierfür muss ein EVU Zähler am SolarEdge Wechselrichter per Modbus angebunden sein.<br>
										Ebenso muss ModbusTCP am Wechselrichter aktiviert werden.<br>
										Der Zähler muss an erster Position im Wechselrichter konfiguriert sein, sonst ist eine Auslesung nicht möglich.<br>
										Es ist die IP-Adresse des SolarEdge Wechselrichters anzugeben.
									</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="solaredgemodbusport" class="col-md-4 col-form-label">Port</label>
								<div class="col">
									<input class="form-control" type="number" min="1" step="1" name="solaredgemodbusport" id="solaredgemodbusport" value="<?php echo (empty($solaredgemodbusportold)?'502':$solaredgemodbusportold) ?>">
									<span class="form-text small">
										Modbus/TCP Port der im Wechselrichter konfiguriert ist. Standardmäßig ist das 502 oder 1502.<br>
									</span>
								</div>
							</div>
						</div>
						<div id="wattbezugsolax" class="hide">
							<div class="alert alert-info">
								Die IP des Wechselrichters wird im dazugehörigen Solax PV-Modul eingestellt.
							</div>
						</div>
						<div id="wattbezuge3dc" class="hide">
							<div class="card-text alert alert-info">
								Die IP des Speichers wird im dazugehörigen E3DC Speicher-Modul eingestellt.<br>
								Es kann nötig sein in den Einstellungen des E3DC ModbusTCP zu aktivieren.<br>
								Das Protokoll in den E3DC Einstellungen ist auf E3DC zu stellen.
							</div>
						</div>
						<div id="wattbezugsbs25" class="hide">
							<div class="card-text alert alert-info">
								Die IP des Speichers wird im dazugehörigen SMA SBS Speicher-Modul eingestellt.
							</div>
						</div>
						<div id="wattbezugenphase" class="hide">
							<div class="card-text alert alert-info">
								Die IP des Envoy / IQ Gateway wird im dazugehörigen Envoy PV-Modul eingestellt.
							</div>
							<div class="form-row mb-1">
								<label for="bezugenphaseeid" class="col-md-4 col-form-label">Zähler EID</label>
								<div class="col">
									<input class="form-control" type="number" min="1" step="1" name="bezugenphaseeid" id="bezugenphaseeid" value="<?php echo (empty($bezugenphaseeidold)?'':$bezugenphaseeidold) ?>">
									<span class="form-text small">
										EID des EVU-Zählers (<i>net-consumption</i>).<br>
									</span>
								</div>
							</div>
						</div>
						<div id="evuglaettungdiv" class="hide">
							<hr class="border-danger">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">EVU Glättung</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($evuglaettungaktold == 0) echo " active" ?>">
												<input type="radio" name="evuglaettungakt" id="evuglaettungaktOff" value="0"<?php if($evuglaettungaktold == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if($evuglaettungaktold == 1) echo " active" ?>">
												<input type="radio" name="evuglaettungakt" id="evuglaettungaktOn" value="1"<?php if($evuglaettungaktold == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
										<span class="form-text small">
											Kombiniert die EVU Werte der letzten x Sekunden und bildet einen Mittelwert.
											Sinnvoll, wenn öfter kurze Lastspitzen auftreten.
										</span>
									</div>
								</div>
								<div id="evuglaettungandiv">
									<div class="form-row mb-1">
										<label for="evuglaettung" class="col-md-4 col-form-label">Zeitspanne</label>
										<div class="col">
											<input class="form-control" type="number" min="10" step="10" name="evuglaettung" id="evuglaettung" value="<?php echo $evuglaettungold ?>">
											<span class="form-text small">
												Gültige Werte: Zeit in Sekunden, z.B. 30,50,200
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>

						<script>
							function display_evuglaettung() {
								if($('#evuglaettungaktOff').prop("checked")) {
									hideSection('#evuglaettungandiv');
								} else {
									showSection('#evuglaettungandiv');
								}
							}

							function display_wattbezugmodul() {
								hideSection('#evuglaettungdiv');
								hideSection('#wattbezugvz');
								hideSection('#wattbezugsdm');
								hideSection('#wattbezugnone');
								hideSection('#wattbezughttp');
								hideSection('#wattbezugsma');
								hideSection('#wattbezugsolarworld');
								hideSection('#wattbezugfronius');
								hideSection('#wattbezugjson');
								hideSection('#wattbezugmpm3pm');
								hideSection('#wattbezugsolarlog');
								hideSection('#wattbezugsolaredge');
								hideSection('#wattbezugsolax');
								hideSection('#wattbezugshm');
								hideSection('#wattbezugsmartme');
								hideSection('#wattbezugsbs25');
								hideSection('#wattbezuge3dc');
								hideSection('#wattbezugethmpm3pm');
								hideSection('#wattbezugethmpm3pmflex');
								hideSection('#wattbezugplentihaus');
								hideSection('#wattbezugkostalpiko');
								hideSection('#wattbezugkostalsmartenergymeter');
								hideSection('#wattbezugsmartfox');
								hideSection('#wattbezugpowerwall');
								hideSection('#wattbezugvictrongx');
								hideSection('#wattbezugsolarview');
								hideSection('#wattbezugdiscovergy');
								hideSection('#wattbezuglgessv1');
								hideSection('#wattbezugmqtt');
								hideSection('#wattbezugsonneneco');
								hideSection('#wattbezugvarta');
								hideSection('#wattbezugfems');
								hideSection('#wattbezugsiemens');
								hideSection('#wattbezugsiemenssentron');
								hideSection('#wattbezugpowerdog');
								hideSection('#wattbezugpowerfox');
								hideSection('#wattbezugrct');
								hideSection('#wattbezugrct2');
								hideSection('#wattbezughuawei');
								hideSection('#wattbezugip');
								hideSection('#wattbezugalphaess');
								hideSection('#wattbezuggoodwe');
								hideSection('#wattbezugbatterx');
								hideSection('#wattbezugsungrow');
								hideSection('#wattbezugsolarwatt');
								hideSection('#wattbezugjanitza');
								hideSection('#wattbezugcarlogavazzilan');
								hideSection('#wattbezugenphase');
								// Auswahl PV-Modul generell erlauben
								//enable_pv_selector();
								if($('#wattbezugmodul').val() != 'none') {
									showSection('#evuglaettungdiv');
									display_evuglaettung();
								} else {
									showSection('#wattbezugnone');
								}
								if($('#wattbezugmodul').val() == 'bezug_alphaess') {
									showSection('#wattbezugalphaess');
								}
								if($('#wattbezugmodul').val() == 'bezug_batterx') {
									showSection('#wattbezugbatterx');
								}
								if($('#wattbezugmodul').val() == 'bezug_sungrow') {
									showSection('#wattbezugsungrow');
								}
								if($('#wattbezugmodul').val() == 'bezug_sonneneco') {
									showSection('#wattbezugsonneneco');
								}
								if($('#wattbezugmodul').val() == 'bezug_varta') {
									showSection('#wattbezugvarta');
								}
								if($('#wattbezugmodul').val() == 'bezug_siemens') {
									showSection('#wattbezugsiemens');
									showSection('#wattbezugip');
								}
								if($('#wattbezugmodul').val() == 'bezug_siemens_sentron') {
									showSection('#wattbezugip');
									showSection('#wattbezugsiemenssentron');
								}
								if($('#wattbezugmodul').val() == 'bezug_janitza') {
									showSection('#wattbezugjanitza');
									showSection('#wattbezugip');
								}
								if($('#wattbezugmodul').val() == 'bezug_carlogavazzilan') {
									showSection('#wattbezugcarlogavazzilan');
									showSection('#wattbezugip');
								}
								if($('#wattbezugmodul').val() == 'bezug_solax') {
									showSection('#wattbezugsolax');
								}
								if($('#wattbezugmodul').val() == 'bezug_good_we') {
									showSection('#wattbezuggoodwe');
								}
								if($('#wattbezugmodul').val() == 'bezug_huawei') {
									showSection('#wattbezughuawei');
								}

								if($('#wattbezugmodul').val() == 'bezug_rct') {
									showSection('#wattbezugrct');
									showSection('#wattbezugip');
								}
								if($('#wattbezugmodul').val() == 'bezug_rct2') {
									showSection('#wattbezugrct2');
									showSection('#wattbezugrct');
									showSection('#wattbezugip');
								}
								if($('#wattbezugmodul').val() == 'bezug_powerdog') {
									showSection('#wattbezugpowerdog');
									showSection('#wattbezugip');
								}
								if($('#wattbezugmodul').val() == 'bezug_powerfox') {
									showSection('#wattbezugpowerfox');
								}
								if($('#wattbezugmodul').val() == 'bezug_fems') {
									showSection('#wattbezugfems');
								}
								if($('#wattbezugmodul').val() == 'bezug_solarworld') {
									showSection('#wattbezugsolarworld');
								}
								if($('#wattbezugmodul').val() == 'bezug_solarview') {
									showSection('#wattbezugsolarview');
								}
								if($('#wattbezugmodul').val() == 'bezug_discovergy') {
									showSection('#wattbezugdiscovergy');
								}
								if($('#wattbezugmodul').val() == 'bezug_mqtt') {
									showSection('#wattbezugmqtt');
								}
								if($('#wattbezugmodul').val() == 'bezug_victrongx') {
									showSection('#wattbezugvictrongx');
								}
								if($('#wattbezugmodul').val() == 'vzlogger') {
									showSection('#wattbezugvz');
								}
								if($('#wattbezugmodul').val() == 'sdm630modbusbezug')   {
									showSection('#wattbezugsdm');
								}
								if($('#wattbezugmodul').val() == 'bezug_http')   {
									showSection('#wattbezughttp');
								}
								if($('#wattbezugmodul').val() == 'bezug_fronius_sm')   {
									showSection('#wattbezugfronius');
								}
								if($('#wattbezugmodul').val() == 'bezug_fronius_s0')   {
									showSection('#wattbezugfronius');
								}
								if($('#wattbezugmodul').val() == 'bezug_json')   {
									showSection('#wattbezugjson');
								}
								if($('#wattbezugmodul').val() == 'bezug_mpm3pm')   {
									showSection('#wattbezugmpm3pm');
								}
								if($('#wattbezugmodul').val() == 'bezug_solarlog')   {
									showSection('#wattbezugsolarlog');
								}
								if($('#wattbezugmodul').val() == 'bezug_solaredge')   {
									showSection('#wattbezugsolaredge');
								}
								if($('#wattbezugmodul').val() == 'bezug_smashm')   {
									showSection('#wattbezugshm');
								}
								if($('#wattbezugmodul').val() == 'bezug_smartme')   {
									showSection('#wattbezugsmartme');
								}
								if($('#wattbezugmodul').val() == 'bezug_e3dc')   {
									showSection('#wattbezuge3dc');
								}
								if($('#wattbezugmodul').val() == 'bezug_ethmpm3pm')   {
									showSection('#wattbezugethmpm3pm');
								}
								if($('#wattbezugmodul').val() == 'bezug_ethmpm3pmflex')   {
									showSection('#wattbezugethmpm3pmflex');
								}
								if($('#wattbezugmodul').val() == 'bezug_sbs25')   {
									showSection('#wattbezugsbs25');
								}
								if($('#wattbezugmodul').val() == 'bezug_kostalplenticoreem300haus')   {
									showSection('#wattbezugplentihaus');
									// keine Auswahl PV-Modul in dieser Konfiguration
									// Plenticore immer fix auswählen
									//document.getElementById('pvwattmodul').value = 'wr_plenticore';
									// und Einstellung sperren
									//disable_pv_selector();
									//display_pvwattmodul();
									// passendes Speichermodul 'optisch' voreinstellen, da automatisch alle Werte
									// mit aus dem WR gelesen werden
									//document.getElementById('speichermodul').value = 'speicher_kostalplenticore';
									//display_speichermodul();
								}
								if($('#wattbezugmodul').val() == 'bezug_kostalpiko')   {
									showSection('#wattbezugkostalpiko');
								}
								if($('#wattbezugmodul').val() == 'bezug_ksem')   {
									showSection('#wattbezugkostalsmartenergymeter');
								}
								if($('#wattbezugmodul').val() == 'bezug_smartfox')   {
									showSection('#wattbezugsmartfox');
								}
								if($('#wattbezugmodul').val() == 'bezug_powerwall')   {
									showSection('#wattbezugpowerwall');
								}
								if($('#wattbezugmodul').val() == 'bezug_lgessv1')   {
									showSection('#wattbezuglgessv1');
								}
								if($('#wattbezugmodul').val() == 'bezug_solarwatt')   {
									showSection('#wattbezugsolarwatt');
								}
								if($('#wattbezugmodul').val() == 'bezug_enphase')   {
									showSection('#wattbezugenphase');
								}
							}

							$(function() {
								display_wattbezugmodul();

								$('#wattbezugmodul').change( function(){
									display_wattbezugmodul();
								});

								$('input[type=radio][name=evuglaettungakt]').change(function() {
									display_evuglaettung();
								});
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
		</div>  <!-- container -->

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
					$('#navModulkonfigurationEvu').addClass('disabled');

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
