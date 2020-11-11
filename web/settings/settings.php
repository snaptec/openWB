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
		<script src = "settings/helperFunctions.js?ver=20200505-a" ></script>
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

			$speichervorhanden = trim( file_get_contents( $_SERVER['DOCUMENT_ROOT'] . '/openWB/ramdisk/speichervorhanden' ) );
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Allgemeine Einstellungen</h1>
			<form action="./tools/saveconfig.php" method="POST">

				<!-- Übergreifendes -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Übergreifendes
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">openWB ist nur ein Ladepunkt</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($isssold == 0) echo " active" ?>">
											<input type="radio" name="isss" id="isssOff" value="0"<?php if($isssold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($isssold == 1) echo " active" ?>">
											<input type="radio" name="isss" id="isssOn" value="1"<?php if($isssold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">
										Wird hier Ja gewählt ist diese openWB nur ein Ladepunkt und übernimmt keine eigene Regelung.
										Hier ist Ja zu wählen wenn bereits eine openWB vorhanden ist und diese nur ein weiterer Ladepunkt der vorhandenen openWB sein soll.
										<span class="text-danger">Alle in dieser openWB getätigten Einstellungen werden NICHT beachtet.</span>
										An der Haupt openWB wird als Ladepunkt "externe openWB" gewählt und die IP Adresse eingetragen.
									</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Awattar -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Awattar</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($awattaraktivold == 0) echo " active" ?>">
											<input type="radio" name="awattaraktiv" id="awattaraktivOff" value="0"<?php if($awattaraktivold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($awattaraktivold == 1) echo " active" ?>">
											<input type="radio" name="awattaraktiv" id="awattaraktivOn" value="1"<?php if($awattaraktivold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Ermöglicht Laden nach Strompreis. Hierfür benötigt wird der Awattar Hourly Tarif sowie ein Discovergy Zähler. Die Awattar Funktion ist nur im SofortLaden Modus aktiv!
						</div>
						<div id="awattardiv" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="awattarlocation" class="col-md-4 col-form-label">Land</label>
									<div class="col">
										<select name="awattarlocation" id="awattarlocation" class="form-control">
											<option <?php if($awattarlocationold == 0) echo "selected" ?> value="de">Deutschland</option>
											<option <?php if($awattarlocationold == 1) echo "selected" ?> value="at">Österreich</option>
										</select>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_awattaraktiv() {
								if($('#awattaraktivOff').prop("checked")) {
									hideSection('awattardiv');
								} else {
									showSection('awattardiv');
								}
							}

							$('input[type=radio][name=awattaraktiv]').change(function(){
								visibility_awattaraktiv();
							});

							visibility_awattaraktiv();
						});
					</script>
				</div>

				<!-- Sperren nach Abstecken -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Ladepunkte sperren nach Abstecken
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Nachdem der Stecker gezogen wird, wird der entsprechende Ladepunkt gesperrt. Ein manuelles aktivieren des Ladepunktes ist erforderlich. Nach aktivieren bleibt der Ladepunkt solange aktiv bis ein Stecker eingesteckt und wieder abgezogen wird. Ist unabhängig davon ob geladen wird.
						</div>
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<div class="col-md-4">
									Ladepunkt 1
								</div>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($stopchargeafterdisclp1old == 0) echo " active" ?>">
										<input type="radio" name="stopchargeafterdisclp1" id="stopchargeafterdisclp1Off" value="0"<?php if($stopchargeafterdisclp1old == 0) echo " checked=\"checked\"" ?>>Nein
									</label>
									<label class="btn btn-outline-info<?php if($stopchargeafterdisclp1old == 1) echo " active" ?>">
										<input type="radio" name="stopchargeafterdisclp1" id="stopchargeafterdisclp1On" value="1"<?php if($stopchargeafterdisclp1old == 1) echo " checked=\"checked\"" ?>>Ja
									</label>
								</div>
							</div>
							<div id="lp2aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 2
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp2old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp2" id="stopchargeafterdisclp2Off" value="0"<?php if($stopchargeafterdisclp2old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp2old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp2" id="stopchargeafterdisclp2On" value="1"<?php if($stopchargeafterdisclp2old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp3aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 3
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp3old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp3" id="stopchargeafterdisclp3Off" value="0"<?php if($stopchargeafterdisclp3old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp3old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp3" id="stopchargeafterdisclp3On" value="1"<?php if($stopchargeafterdisclp3old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp4aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 4
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp4old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp4" id="stopchargeafterdisclp4Off" value="0"<?php if($stopchargeafterdisclp4old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp4old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp4" id="stopchargeafterdisclp4On" value="1"<?php if($stopchargeafterdisclp4old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp5aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 5
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp5old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp5" id="stopchargeafterdisclp5Off" value="0"<?php if($stopchargeafterdisclp5old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp5old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp5" id="stopchargeafterdisclp5On" value="1"<?php if($stopchargeafterdisclp5old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp6aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 6
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp6old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp6" id="stopchargeafterdisclp6Off" value="0"<?php if($stopchargeafterdisclp6old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp6old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp6" id="stopchargeafterdisclp6On" value="1"<?php if($stopchargeafterdisclp6old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp7aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 7
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp7old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp7" id="stopchargeafterdisclp7Off" value="0"<?php if($stopchargeafterdisclp7old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp7old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp7" id="stopchargeafterdisclp7On" value="1"<?php if($stopchargeafterdisclp7old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
							<div id="lp8aktdiv" class="hide">
								<div class="form-row vaRow mb-1">
									<div class="col-md-4">
										Ladepunkt 8
									</div>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp8old == 0) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp8" id="stopchargeafterdisclp8Off" value="0"<?php if($stopchargeafterdisclp8old == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($stopchargeafterdisclp8old == 1) echo " active" ?>">
											<input type="radio" name="stopchargeafterdisclp8" id="stopchargeafterdisclp8On" value="1"<?php if($stopchargeafterdisclp8old == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							var lp2akt = <?php echo $lastmanagementold ?>;
							var lp3akt = <?php echo $lastmanagements2old ?>;
							var lp4akt = <?php echo $lastmanagementlp4old ?>;
							var lp5akt = <?php echo $lastmanagementlp5old ?>;
							var lp6akt = <?php echo $lastmanagementlp6old ?>;
							var lp7akt = <?php echo $lastmanagementlp7old ?>;
							var lp8akt = <?php echo $lastmanagementlp8old ?>;

							if(lp2akt == '0') {
								hideSection('lp2aktdiv');
								hideSection('loadsharingdiv');
								showSection('loadsharingoffdiv');
								hideSection('nachtladenlp2div');
								hideSection('durchslp2div');
							} else {
								showSection('lp2aktdiv');
								showSection('loadsharingdiv');
								hideSection('loadsharingoffdiv');
								showSection('nachtladenlp2div');
								showSection('durchslp2div');
							}
							if(lp3akt == '0') {
								hideSection('lp3aktdiv');
								hideSection('durchslp3div');
							} else {
								showSection('lp3aktdiv');
								showSection('durchslp3div');
							}
							if(lp4akt == '0') {
								hideSection('lp4aktdiv');
							} else {
								showSection('lp4aktdiv');
							}
							if(lp5akt == '0') {
								hideSection('lp5aktdiv');
							} else {
								showSection('lp5aktdiv');
							}
							if(lp6akt == '0') {
								hideSection('lp6aktdiv');
							} else {
								showSection('lp6aktdiv');
							}
							if(lp7akt == '0') {
								hideSection('lp7aktdiv');
							} else {
								showSection('lp7aktdiv');
							}
							if(lp8akt == '0') {
								hideSection('lp8aktdiv');
							} else {
								showSection('lp8aktdiv');
							}
						});
					</script>
				</div>

				<!-- Zielladen -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Zielladen (Beta)
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Ladepunkt 1</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 0) echo " active" ?>">
										<input type="radio" name="zielladenaktivlp1" id="zielladenaktivlp1Off" value="0"<?php if($zielladenaktivlp1old == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 1) echo " active" ?>">
										<input type="radio" name="zielladenaktivlp1" id="zielladenaktivlp1On" value="1"<?php if($zielladenaktivlp1old == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div id="zielladenaktivlp1div" class="hide">
								<div class="card-text alert alert-info">
									Gewünschten SoC, Ziel Uhrzeit sowie Ladegeschwindigkeit einstellen. Sicherstellen das die Akkugröße wie auch die richtige Anzahl der Phasen konfiguriert sind.
								</div>
								<div class="form-row mb-1">
									<label for="zielladensoclp1" class="col-md-4 col-form-label">Ziel-SoC</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="zielladensoclp1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $zielladensoclp1old; ?> %</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="zielladensoclp1" id="zielladensoclp1" min="0" max="100" step="5" value="<?php echo $zielladensoclp1old; ?>">
											</div>
										</div>
										<span class="form-text small">Der SoC Wert auf den geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="zielladenuhrzeitlp1" class="col-md-4 col-form-label">Ziel-Zeitpunkt</label>
									<div class="col">
										<input class="form-control" type="text" pattern="20[0-9]{2}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:30))|(?:(?:0[13578]|1[02])-31)) (0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])" name="zielladenuhrzeitlp1" id="zielladenuhrzeitlp1" value="<?php echo $zielladenuhrzeitlp1old; ?>">
										<span class="form-text small">Gültige Werte YYYY-MM-DD HH:MM, z.B. 2018-12-16 06:15. Ende der gewünschten Ladezeit. Das Datum muss exakt in diesem Format mit Leerzeichen zwischen Monat und Stunde eingegeben werden.</span>
										<!--
											test datetime input (not supported by all Browsers)
											value format: YYY-MM-DDTHH:MM needs to be handled before passing to config file!
										<input class="form-control" type="datetime-local" name="zielladenuhrzeitlp1_test" id="zielladenuhrzeitlp1_test" value="<?php echo str_replace( ' ', 'T', $zielladenuhrzeitlp1old ); ?>">
										-->
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="zielladenalp1" class="col-md-4 col-form-label">Stromstärke</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="zielladenalp1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $zielladenalp1old; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="zielladenalp1" id="zielladenalp1" min="6" max="32" step="1" value="<?php echo $zielladenalp1old; ?>">
											</div>
										</div>
										<span class="form-text small">Ampere mit denen geladen werden soll um den Ziel SoC zu erreichen.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_zielladenaktivlp1() {
								if($('#zielladenaktivlp1Off').prop("checked")) {
									hideSection('zielladenaktivlp1div');
								} else {
									showSection('zielladenaktivlp1div');
								}
							}

							$('input[type=radio][name=zielladenaktivlp1]').change(function(){
								visibility_zielladenaktivlp1();
							});

							visibility_zielladenaktivlp1();
						});
					</script>
				</div>

				<!-- EV Daten -->
				<div class="card border-primary">
					<div class="card-header bg-primary">
						EV Daten
					</div>
					<div class="card-body">
						<div id="durchslp1div">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col">
										Ladepunkt 1
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="durchslp1" class="col-md-4 col-form-label">Durchschnittsverbrauch in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="0.1" name="durchslp1" id="durchslp1" value="<?php echo $durchslp1old ?>">
										<span class="form-text small">Gültige Werte xx.xx, z.B. 14.5. Dient zur Berechnung der geladenen Strecke.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="akkuglp1" class="col-md-4 col-form-label">Akkugröße in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="akkuglp1" id="akkuglp1" value="<?php echo $akkuglp1old ?>">
										<span class="form-text small">Gültige Werte xx, z.B. 41. Dient zur Berechnung der benötigten Ladezeit.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Anzahl genutzter Phasen</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 1) echo " active" ?>">
												<input type="radio" name="zielladenphasenlp1" id="zielladenphasenlp11" value="1"<?php if($zielladenphasenlp1old == 1) echo " checked=\"checked\"" ?>>1
											</label>
											<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 2) echo " active" ?>">
												<input type="radio" name="zielladenphasenlp1" id="zielladenphasenlp12" value="2"<?php if($zielladenphasenlp1old == 2) echo " checked=\"checked\"" ?>>2
											</label>
											<label class="btn btn-outline-info<?php if($zielladenaktivlp1old == 3) echo " active" ?>">
												<input type="radio" name="zielladenphasenlp1" id="zielladenphasenlp13" value="3"<?php if($zielladenphasenlp1old == 3) echo " checked=\"checked\"" ?>>3
											</label>
										</div>
										<span class="form-text small">Nur für Zielladen relevant.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="zielladenmaxalp1" class="col-md-4 col-form-label">maximale Stromstärke</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="zielladenmaxalp1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $zielladenmaxalp1old; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="zielladenmaxalp1" id="zielladenmaxalp1" min="6" max="32" step="1" value="<?php echo $zielladenmaxalp1old; ?>">
											</div>
										</div>
										<span class="form-text small">Ampere mit denen geladen werden kann, um den Ziel SoC zu erreichen. Orientiert an der Leistung der Hausinstallation, oder der des zu ladenden Autos.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="durchslp2div" class="hide">
							<hr class="border-primary">
							<div class="form-group mb-1">
								<div class="form-row mb-1">
									<div class="col">
										Ladepunkt 2
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="durchslp2" class="col-md-4 col-form-label">Durchschnittsverbrauch in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step=".1" name="durchslp2" id="durchslp2" value="<?php echo $durchslp2old ?>">
										<span class="form-text small">Gültige Werte xx.xx, z.B. 14.5. Dient zur Berechnung der geladenen Strecke.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="akkuglp2" class="col-md-4 col-form-label">Akkugröße in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step="1" name="akkuglp2" id="akkuglp2" value="<?php echo $akkuglp2old ?>">
										<span class="form-text small">Gültige Werte xx, z.B. 41. Dient zur Berechnung der benötigten Ladezeit.</span>
									</div>
								</div>
							</div>
						</div>
						<div id="durchslp3div" class="hide">
							<hr class="border-primary">
							<div class="form-group">
								<div class="form-row mb-1">
									<div class="col">
										Ladepunkt 3
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="durchslp3" class="col-md-4 col-form-label">Durchschnittsverbrauch in kWh</label>
									<div class="col">
										<input class="form-control" type="number" min="1" step=".1" name="durchslp3" id="durchslp3" value="<?php echo $durchslp3old ?>">
										<span class="form-text small">Gültige Werte xx.xx, z.B. 14.5. Dient zur Berechnung der geladenen Strecke.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Automatische Phasenumschaltung -->
				<div class="card border-success">
					<div class="card-header bg-success">
						<div class="form-group mb-0">
							<div class="form-row vaRow mb-0">
								<div class="col-4">Automatische Phasenumschaltung</div>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-sm btn-outline-info<?php if($u1p3paktivold == 0) echo " active" ?>">
											<input type="radio" name="u1p3paktiv" id="u1p3paktivOff" value="0"<?php if($u1p3paktivold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-sm btn-outline-info<?php if($u1p3paktivold == 1) echo " active" ?>">
											<input type="radio" name="u1p3paktiv" id="u1p3paktivOn" value="1"<?php if($u1p3paktivold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Automatisierte Umschaltung von 1- und 3-phasiger Ladung. Nur aktivieren, wenn diese Option in der OpenWB verbaut ist. Je nach gekaufter Hardwareoption gültig für alle Ladepunkte!
						</div>
						<div id="u1p3pan" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Sofort Laden</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3psofortold == 1) echo " active" ?>">
											<input type="radio" name="u1p3psofort" id="u1p3psofort1" value="1"<?php if($u1p3psofortold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3psofortold == 3) echo " active" ?>">
											<input type="radio" name="u1p3psofort" id="u1p3psofort3" value="3"<?php if($u1p3psofortold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Standby</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3pstandbyold == 1) echo " active" ?>">
											<input type="radio" name="u1p3pstandby" id="u1p3pstandby1" value="1"<?php if($u1p3pstandbyold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pstandbyold == 3) echo " active" ?>">
											<input type="radio" name="u1p3pstandby" id="u1p3pstandby3" value="3"<?php if($u1p3pstandbyold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Min + PV Laden</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3pminundpvold == 1) echo " active" ?>">
											<input type="radio" name="u1p3pminundpv" id="u1p3pminundpv1" value="1"<?php if($u1p3pminundpvold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pminundpvold == 3) echo " active" ?>">
											<input type="radio" name="u1p3pminundpv" id="u1p3pminundpv3" value="3"<?php if($u1p3pminundpvold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pminundpvold == 4) echo " active" ?>">
											<input type="radio" name="u1p3pminundpv" id="u1p3pminundpv4" value="4"<?php if($u1p3pminundpvold == 4) echo " checked=\"checked\"" ?>>Automatikmodus
										</label>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Nur PV Laden</label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($u1p3pnurpvold == 1) echo " active" ?>">
												<input type="radio" name="u1p3pnurpv" id="u1p3pnurpv1" value="1"<?php if($u1p3pnurpvold == 1) echo " checked=\"checked\"" ?>>einphasig
											</label>
											<label class="btn btn-outline-info<?php if($u1p3pnurpvold == 3) echo " active" ?>">
												<input type="radio" name="u1p3pnurpv" id="u1p3pnurpv3" value="3"<?php if($u1p3pnurpvold == 3) echo " checked=\"checked\"" ?>>dreiphasig
											</label>
											<label class="btn btn-outline-info<?php if($u1p3pnurpvold == 4) echo " active" ?>">
												<input type="radio" name="u1p3pnurpv" id="u1p3pnurpv4" value="4"<?php if($u1p3pnurpvold == 4) echo " checked=\"checked\"" ?>>Automatikmodus
											</label>
										</div>
										<span class="form-text small">Im Automatikmodus wird die PV Ladung einphasig begonnen. Ist für durchgehend 10 Minuten die Maximalstromstärke erreicht, wird die Ladung auf dreiphasige Ladung umgestellt. Ist die Ladung nur für ein Intervall unterhalb der Maximalstromstärke, beginnt der Counter für die Umschaltung erneut. Ist die Ladung im dreiphasigen Modus für 8 Minuten bei der Minimalstromstärke, wird wieder auf einphasige Ladung gewechselt.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Nachtladen</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($u1p3pnlold == 1) echo " active" ?>">
											<input type="radio" name="u1p3pnl" id="u1p3pnl1" value="1"<?php if($u1p3pnlold == 1) echo " checked=\"checked\"" ?>>einphasig
										</label>
										<label class="btn btn-outline-info<?php if($u1p3pnlold == 3) echo " active" ?>">
											<input type="radio" name="u1p3pnl" id="u1p3pnl3" value="3"<?php if($u1p3pnlold == 3) echo " checked=\"checked\"" ?>>dreiphasig
										</label>
									</div>
								</div>
							</div>
							<hr class="border-success">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Schieflastbeachtung</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($schieflastaktivold == 0) echo " active" ?>">
											<input type="radio" name="schieflastaktiv" id="schieflastaktivOff" value="0"<?php if($schieflastaktivold == 0) echo " checked=\"checked\"" ?>>Nein
										</label>
										<label class="btn btn-outline-info<?php if($schieflastaktivold == 1) echo " active" ?>">
											<input type="radio" name="schieflastaktiv" id="schieflastaktivOn" value="1"<?php if($schieflastaktivold == 1) echo " checked=\"checked\"" ?>>Ja
										</label>
									</div>
								</div>
								<div class="form-row mb-1 hide" id="schieflastan">
									<label for="schieflastmaxa" class="col-md-4 col-form-label">Schieflastbegrenzung</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="schieflastmaxa" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $schieflastmaxaold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="schieflastmaxa" id="schieflastmaxa" min="10" max="32" step="1" value="<?php echo $schieflastmaxaold; ?>">
											</div>
										</div>
										<span class="form-text small">Gibt an mit wieviel Ampere maximal geladen wird wenn die automatische Umschaltung aktiv ist und mit einer Phase lädt.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_u1p3paktiv() {
								if($('#u1p3paktivOff').prop("checked")) {
									hideSection('u1p3pan');
								} else {
									showSection('u1p3pan');
									visibility_schieflastaktiv();
								}
							}

							function visibility_schieflastaktiv() {
								if($('#schieflastaktivOff').prop("checked")) {
									hideSection('schieflastan');
								} else {
									showSection('schieflastan');
								}
							}

							$('input[type=radio][name=u1p3paktiv]').change(function(){
								visibility_u1p3paktiv();
							});

							$('input[type=radio][name=schieflastaktiv]').change(function(){
								visibility_schieflastaktiv();
							});

							visibility_u1p3paktiv();
						});
					</script>
				</div>

				<!-- Nachtlademodus -->
				<div class="card border-info">
					<div class="card-header bg-info">
						Nachtlademodus
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<div class="col">
									Aktivierung je Lademodus
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Sofort</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_sofortold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_sofort" id="nlakt_sofortOff" value="0"<?php if($nlakt_sofortold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_sofortold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_sofort" id="nlakt_sofortOn" value="1"<?php if($nlakt_sofortold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Min+PV</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_minpvold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_minpv" id="nlakt_minpvOff" value="0"<?php if($nlakt_minpvold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_minpvold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_minpv" id="nlakt_minpvOn" value="1"<?php if($nlakt_minpvold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Nur PV</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_nurpvold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_nurpv" id="nlakt_nurpvOff" value="0"<?php if($nlakt_nurpvold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_nurpvold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_nurpv" id="nlakt_nurpvOn" value="1"<?php if($nlakt_nurpvold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Standby</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nlakt_standbyold == 0) echo " active" ?>">
										<input type="radio" name="nlakt_standby" id="nlakt_standbyOff" value="0"<?php if($nlakt_standbyold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nlakt_standbyold == 1) echo " active" ?>">
										<input type="radio" name="nlakt_standby" id="nlakt_standbyOn" value="1"<?php if($nlakt_standbyold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
						</div>
						<hr class="border-info">
						<div class="form-group">
							<div class="form-row vaRow mb-1">
								<label class="col-md-4 col-form-label">Ladepunkt 1</label>
								<div class="btn-group btn-group-toggle col" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($nachtladenold == 0) echo " active" ?>">
										<input type="radio" name="nachtladen" id="nachtladenOff" value="0"<?php if($nachtladenold == 0) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($nachtladenold == 1) echo " active" ?>">
										<input type="radio" name="nachtladen" id="nachtladenOn" value="1"<?php if($nachtladenold == 1) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
							</div>
							<div id="nachtladenan" class="hide">
								<div class="form-row mb-1">
									<div class="col">
										Nachtladen
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nachtll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="nachtll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $nachtllold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="nachtll" id="nachtll" min="6" max="32" step="1" value="<?php echo $nachtllold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="nachtladenabuhr" id="nachtladenabuhr" class="form-control">
														<option <?php if($nachtladenabuhrold == 17) echo "selected" ?> value="17">17:00</option>
														<option <?php if($nachtladenabuhrold == 18) echo "selected" ?> value="18">18:00</option>
														<option <?php if($nachtladenabuhrold == 19) echo "selected" ?> value="19">19:00</option>
														<option <?php if($nachtladenabuhrold == 20) echo "selected" ?> value="20">20:00</option>
														<option <?php if($nachtladenabuhrold == 21) echo "selected" ?> value="21">21:00</option>
														<option <?php if($nachtladenabuhrold == 22) echo "selected" ?> value="22">22:00</option>
														<option <?php if($nachtladenabuhrold == 23) echo "selected" ?> value="23">23:00</option>
														<option <?php if($nachtladenabuhrold == 24) echo "selected" ?> value="24">24:00</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="nachtladenbisuhr" id="nachtladenbisuhr" class="form-control">
														<option <?php if($nachtladenbisuhrold == 0) echo "selected" ?> value="0">0:00</option>
														<option <?php if($nachtladenbisuhrold == 1) echo "selected" ?> value="1">1:00</option>
														<option <?php if($nachtladenbisuhrold == 2) echo "selected" ?> value="2">2:00</option>
														<option <?php if($nachtladenbisuhrold == 3) echo "selected" ?> value="3">3:00</option>
														<option <?php if($nachtladenbisuhrold == 4) echo "selected" ?> value="4">4:00</option>
														<option <?php if($nachtladenbisuhrold == 5) echo "selected" ?> value="5">5:00</option>
														<option <?php if($nachtladenbisuhrold == 6) echo "selected" ?> value="6">6:00</option>
														<option <?php if($nachtladenbisuhrold == 7) echo "selected" ?> value="7">7:00</option>
														<option <?php if($nachtladenbisuhrold == 8) echo "selected" ?> value="8">8:00</option>
														<option <?php if($nachtladenbisuhrold == 9) echo "selected" ?> value="9">9:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der nachts geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nachtsoc" class="col-md-4 col-form-label">SoC Sonntag bis Donnerstag</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="nachtsoc" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsocold; ?> %</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="nachtsoc" id="nachtsoc" min="5" max="100" step="5" value="<?php echo $nachtsocold; ?>">
											</div>
										</div>
										<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster. Das SoC Fenster is von von Sonntag Abend bis Freitag Morgen aktiv.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="nachtsoc1" class="col-md-4 col-form-label">SoC Freitag bis Sonntag</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="nachtsoc1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsoc1old; ?> %</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="nachtsoc1" id="nachtsoc1" min="5" max="100" step="5" value="<?php echo $nachtsoc1old; ?>">
											</div>
										</div>
										<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster. Das SoC Fenster is von von Freitag Morgen bis Sonntag Abend aktiv.</span>
									</div>
								</div>
								<hr class="border-info">
								<div class="form-row mb-1">
									<div class="col">
										Morgensladen
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Montag
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1moll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1moll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1mollold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1moll" id="mollp1moll" min="6" max="32" step="1" value="<?php echo $mollp1mollold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1moab" id="mollp1moab" class="form-control">
														<option <?php if($mollp1moabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1moabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1moabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1moabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1moabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1moabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1moabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1moabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1moabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1moabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1moabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1moabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1moabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1moabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1moabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1moabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1moabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1moabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1moabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1moabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1moabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1moabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1moabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1moabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1moabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1moabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1moabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1moabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1moabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1moabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1moabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1moabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1mobis" id="mollp1mobis" class="form-control">
														<option <?php if($mollp1mobisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1mobisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1mobisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1mobisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1mobisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1mobisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1mobisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1mobisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1mobisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1mobisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1mobisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1mobisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1mobisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1mobisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1mobisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1mobisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1mobisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1mobisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1mobisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1mobisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1mobisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1mobisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1mobisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1mobisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1mobisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1mobisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1mobisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1mobisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1mobisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1mobisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1mobisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1mobisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1mobisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Montag morgens geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Dienstag
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1dill" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1dill" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1dillold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1dill" id="mollp1dill" min="6" max="32" step="1" value="<?php echo $mollp1dillold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1diab" id="mollp1diab" class="form-control">
														<option <?php if($mollp1diabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1diabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1diabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1diabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1diabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1diabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1diabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1diabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1diabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1diabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1diabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1diabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1diabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1diabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1diabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1diabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1diabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1diabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1diabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1diabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1diabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1diabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1diabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1diabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1diabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1diabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1diabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1diabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1diabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1diabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1diabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1diabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1dibis" id="mollp1dibis" class="form-control">
														<option <?php if($mollp1dibisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1dibisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1dibisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1dibisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1dibisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1dibisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1dibisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1dibisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1dibisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1dibisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1dibisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1dibisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1dibisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1dibisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1dibisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1dibisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1dibisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1dibisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1dibisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1dibisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1dibisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1dibisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1dibisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1dibisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1dibisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1dibisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1dibisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1dibisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1dibisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1dibisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1dibisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1dibisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1dibisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Dienstag morgens geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Mittwoch
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1mill" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1mill" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1millold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1mill" id="mollp1mill" min="6" max="32" step="1" value="<?php echo $mollp1millold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1miab" id="mollp1miab" class="form-control">
														<option <?php if($mollp1miabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1miabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1miabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1miabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1miabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1miabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1miabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1miabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1miabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1miabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1miabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1miabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1miabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1miabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1miabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1miabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1miabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1miabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1miabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1miabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1miabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1miabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1miabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1miabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1miabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1miabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1miabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1miabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1miabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1miabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1miabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1miabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1mibis" id="mollp1mibis" class="form-control">
														<option <?php if($mollp1mibisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1mibisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1mibisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1mibisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1mibisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1mibisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1mibisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1mibisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1mibisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1mibisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1mibisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1mibisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1mibisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1mibisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1mibisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1mibisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1mibisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1mibisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1mibisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1mibisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1mibisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1mibisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1mibisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1mibisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1mibisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1mibisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1mibisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1mibisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1mibisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1mibisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1mibisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1mibisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1mibisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Mittwoch morgens geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Donnerstag
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1doll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1doll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1dollold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1doll" id="mollp1doll" min="6" max="32" step="1" value="<?php echo $mollp1dollold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1doab" id="mollp1doab" class="form-control">
														<option <?php if($mollp1doabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1doabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1doabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1doabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1doabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1doabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1doabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1doabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1doabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1doabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1doabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1doabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1doabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1doabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1doabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1doabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1doabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1doabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1doabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1doabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1doabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1doabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1doabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1doabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1doabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1doabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1doabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1doabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1doabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1doabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1doabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1doabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1dobis" id="mollp1dobis" class="form-control">
														<option <?php if($mollp1dobisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1dobisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1dobisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1dobisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1dobisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1dobisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1dobisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1dobisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1dobisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1dobisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1dobisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1dobisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1dobisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1dobisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1dobisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1dobisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1dobisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1dobisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1dobisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1dobisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1dobisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1dobisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1dobisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1dobisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1dobisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1dobisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1dobisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1dobisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1dobisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1dobisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1dobisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1dobisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1dobisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Donnerstag morgens geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Freitag
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1frll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1frll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1frllold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1frll" id="mollp1frll" min="6" max="32" step="1" value="<?php echo $mollp1frllold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1frab" id="mollp1frab" class="form-control">
														<option <?php if($mollp1frabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1frabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1frabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1frabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1frabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1frabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1frabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1frabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1frabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1frabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1frabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1frabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1frabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1frabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1frabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1frabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1frabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1frabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1frabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1frabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1frabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1frabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1frabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1frabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1frabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1frabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1frabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1frabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1frabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1frabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1frabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1frabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1frbis" id="mollp1frbis" class="form-control">
														<option <?php if($mollp1frbisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1frbisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1frbisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1frbisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1frbisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1frbisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1frbisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1frbisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1frbisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1frbisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1frbisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1frbisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1frbisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1frbisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1frbisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1frbisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1frbisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1frbisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1frbisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1frbisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1frbisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1frbisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1frbisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1frbisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1frbisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1frbisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1frbisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1frbisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1frbisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1frbisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1frbisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1frbisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1frbisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Freitag morgens geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Samstag
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1sall" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1sall" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1sallold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1sall" id="mollp1sall" min="6" max="32" step="1" value="<?php echo $mollp1sallold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1saab" id="mollp1saab" class="form-control">
														<option <?php if($mollp1saabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1saabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1saabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1saabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1saabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1saabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1saabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1saabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1saabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1saabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1saabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1saabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1saabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1saabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1saabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1saabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1saabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1saabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1saabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1saabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1saabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1saabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1saabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1saabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1saabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1saabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1saabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1saabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1saabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1saabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1saabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1saabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1sabis" id="mollp1sabis" class="form-control">
														<option <?php if($mollp1sabisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1sabisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1sabisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1sabisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1sabisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1sabisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1sabisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1sabisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1sabisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1sabisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1sabisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1sabisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1sabisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1sabisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1sabisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1sabisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1sabisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1sabisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1sabisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1sabisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1sabisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1sabisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1sabisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1sabisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1sabisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1sabisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1sabisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1sabisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1sabisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1sabisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1sabisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1sabisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1sabisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Samstag morgens geladen werden soll.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col">
										Sonntag
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="mollp1soll" class="col-md-4 col-form-label">Stromstärke in A</label>
									<div class="col-md-8">
										<div class="form-row vaRow mb-1">
											<label for="mollp1soll" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $mollp1sollold; ?> A</label>
											<div class="col-10">
												<input type="range" class="form-control-range rangeInput" name="mollp1soll" id="mollp1soll" min="6" max="32" step="1" value="<?php echo $mollp1sollold; ?>">
											</div>
										</div>
									</div>
								</div>
								<div class="form-row mb-1">
									<div class="col-md-4">
										Zeitspanne
									</div>
									<div class="col">
										<div class="form-row">
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Anfang
														</div>
													</div> 
													<select name="mollp1soab" id="mollp1soab" class="form-control">
														<option <?php if($mollp1soabold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1soabold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1soabold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1soabold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1soabold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1soabold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1soabold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1soabold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1soabold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1soabold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1soabold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1soabold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1soabold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1soabold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1soabold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1soabold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1soabold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1soabold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1soabold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1soabold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1soabold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1soabold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1soabold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1soabold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1soabold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1soabold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1soabold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1soabold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1soabold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1soabold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1soabold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1soabold == "10:45") echo "selected" ?> value="10:45">10:45</option>
													</select>
												</div>
											</div>
											<div class="col-sm-6">
												<div class="input-group">
													<div class="input-group-prepend">
														<div class="input-group-text">
															Ende
														</div>
													</div> 
													<select name="mollp1sobis" id="mollp1sobis" class="form-control">
														<option <?php if($mollp1sobisold == "03:00") echo "selected" ?> value="03:00">03:00</option>
														<option <?php if($mollp1sobisold == "03:15") echo "selected" ?> value="03:15">03:15</option>
														<option <?php if($mollp1sobisold == "03:30") echo "selected" ?> value="03:30">03:30</option>
														<option <?php if($mollp1sobisold == "03:45") echo "selected" ?> value="03:45">03:45</option>
														<option <?php if($mollp1sobisold == "04:00") echo "selected" ?> value="04:00">04:00</option>
														<option <?php if($mollp1sobisold == "04:15") echo "selected" ?> value="04:15">04:15</option>
														<option <?php if($mollp1sobisold == "04:30") echo "selected" ?> value="04:30">04:30</option>
														<option <?php if($mollp1sobisold == "04:45") echo "selected" ?> value="04:45">04:45</option>
														<option <?php if($mollp1sobisold == "05:00") echo "selected" ?> value="05:00">05:00</option>
														<option <?php if($mollp1sobisold == "05:15") echo "selected" ?> value="05:15">05:15</option>
														<option <?php if($mollp1sobisold == "05:30") echo "selected" ?> value="05:30">05:30</option>
														<option <?php if($mollp1sobisold == "05:45") echo "selected" ?> value="05:45">05:45</option>
														<option <?php if($mollp1sobisold == "06:00") echo "selected" ?> value="06:00">06:00</option>
														<option <?php if($mollp1sobisold == "06:15") echo "selected" ?> value="06:15">06:15</option>
														<option <?php if($mollp1sobisold == "06:30") echo "selected" ?> value="06:30">06:30</option>
														<option <?php if($mollp1sobisold == "06:45") echo "selected" ?> value="06:45">06:45</option>
														<option <?php if($mollp1sobisold == "07:00") echo "selected" ?> value="07:00">07:00</option>
														<option <?php if($mollp1sobisold == "07:15") echo "selected" ?> value="07:15">07:15</option>
														<option <?php if($mollp1sobisold == "07:30") echo "selected" ?> value="07:30">07:30</option>
														<option <?php if($mollp1sobisold == "07:45") echo "selected" ?> value="07:45">07:45</option>
														<option <?php if($mollp1sobisold == "08:00") echo "selected" ?> value="08:00">08:00</option>
														<option <?php if($mollp1sobisold == "08:15") echo "selected" ?> value="08:15">08:15</option>
														<option <?php if($mollp1sobisold == "08:30") echo "selected" ?> value="08:30">08:30</option>
														<option <?php if($mollp1sobisold == "08:45") echo "selected" ?> value="08:45">08:45</option>
														<option <?php if($mollp1sobisold == "09:00") echo "selected" ?> value="09:00">09:00</option>
														<option <?php if($mollp1sobisold == "09:15") echo "selected" ?> value="09:15">09:15</option>
														<option <?php if($mollp1sobisold == "09:30") echo "selected" ?> value="09:30">09:30</option>
														<option <?php if($mollp1sobisold == "09:45") echo "selected" ?> value="09:45">09:45</option>
														<option <?php if($mollp1sobisold == "10:00") echo "selected" ?> value="10:00">10:00</option>
														<option <?php if($mollp1sobisold == "10:15") echo "selected" ?> value="10:15">10:15</option>
														<option <?php if($mollp1sobisold == "10:30") echo "selected" ?> value="10:30">10:30</option>
														<option <?php if($mollp1sobisold == "10:45") echo "selected" ?> value="10:45">10:45</option>
														<option <?php if($mollp1sobisold == "11:00") echo "selected" ?> value="11:00">11:00</option>
													</select>
												</div>
											</div>
										</div>
										<span class="form-text small">Zeitspanne, in der am Sonntag morgens geladen werden soll.</span>
									</div>
								</div>
							</div>
						</div>

						<div id="nachtladenlp2div" class="hide">
							<hr class="border-info">
							<div class="form-group">
								<div class="form-row vaRow mb-1">
									<label class="col-md-4 col-form-label">Ladepunkt 2</label>
									<div class="btn-group btn-group-toggle col" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($nachtladens1old == 0) echo " active" ?>">
											<input type="radio" name="nachtladens1" id="nachtladens1Off" value="0"<?php if($nachtladens1old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($nachtladens1old == 1) echo " active" ?>">
											<input type="radio" name="nachtladens1" id="nachtladens1On" value="1"<?php if($nachtladens1old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
								<div id="nachtladenans1" class="hide">
									<div class="form-row mb-1">
										<div class="col">
											Nachtladen
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nachtlls1" class="col-md-4 col-form-label">Stromstärke in A</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nachtlls1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $nachtlls1old; ?> A</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nachtlls1" id="nachtlls1" min="6" max="32" step="1" value="<?php echo $nachtlls1old; ?>">
												</div>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<div class="col-md-4">
											Zeitspanne
										</div>
										<div class="col">
											<div class="form-row">
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Anfang
															</div>
														</div>
														<select name="nachtladenabuhrs1" id="nachtladenabuhrs1" class="form-control">
															<option <?php if($nachtladenabuhrs1old == 17) echo "selected" ?> value="17">17:00</option>
															<option <?php if($nachtladenabuhrs1old == 18) echo "selected" ?> value="18">18:00</option>
															<option <?php if($nachtladenabuhrs1old == 19) echo "selected" ?> value="19">19:00</option>
															<option <?php if($nachtladenabuhrs1old == 20) echo "selected" ?> value="20">20:00</option>
															<option <?php if($nachtladenabuhrs1old == 21) echo "selected" ?> value="21">21:00</option>
															<option <?php if($nachtladenabuhrs1old == 22) echo "selected" ?> value="22">22:00</option>
															<option <?php if($nachtladenabuhrs1old == 23) echo "selected" ?> value="23">23:00</option>
															<option <?php if($nachtladenabuhrs1old == 24) echo "selected" ?> value="24">24:00</option>
														</select>
													</div>
												</div>
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Ende
															</div>
														</div>
														<select name="nachtladenbisuhrs1" id="nachtladenbisuhrs1" class="form-control">
															<option <?php if($nachtladenbisuhrs1old == 0) echo "selected" ?> value="0">0:00</option>
															<option <?php if($nachtladenbisuhrs1old == 1) echo "selected" ?> value="1">1:00</option>
															<option <?php if($nachtladenbisuhrs1old == 2) echo "selected" ?> value="2">2:00</option>
															<option <?php if($nachtladenbisuhrs1old == 3) echo "selected" ?> value="3">3:00</option>
															<option <?php if($nachtladenbisuhrs1old == 4) echo "selected" ?> value="4">4:00</option>
															<option <?php if($nachtladenbisuhrs1old == 5) echo "selected" ?> value="5">5:00</option>
															<option <?php if($nachtladenbisuhrs1old == 6) echo "selected" ?> value="6">6:00</option>
															<option <?php if($nachtladenbisuhrs1old == 7) echo "selected" ?> value="7">7:00</option>
															<option <?php if($nachtladenbisuhrs1old == 8) echo "selected" ?> value="8">8:00</option>
															<option <?php if($nachtladenbisuhrs1old == 9) echo "selected" ?> value="9">9:00</option>
														</select>
													</div>
												</div>
											</div>
											<span class="form-text small">Zeitspanne, in der nachts geladen werden soll.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nachtsocs1" class="col-md-4 col-form-label">SoC Sonntag bis Donnerstag</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nachtsocs1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsocs1old; ?> %</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nachtsocs1" id="nachtsocs1" min="5" max="100" step="5" value="<?php echo $nachtsocs1old; ?>">
												</div>
											</div>
											<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster. Das SoC Fenster is von von Sonntag Abend bis Freitag Morgen aktiv.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nachtsoc1s1" class="col-md-4 col-form-label">SoC Freitag bis Sonntag</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nachtsoc1s1" class="col-2 col-form-label valueLabel" suffix="%"><?php echo $nachtsoc1s1old; ?> %</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nachtsoc1s1" id="nachtsoc1s1" min="5" max="100" step="5" value="<?php echo $nachtsoc1s1old; ?>">
												</div>
											</div>
											<span class="form-text small">Wenn SoC Modul vorhanden wird Nachts bis xx% SoC geladen in dem angegebenen Zeitfenster. Das SoC Fenster is von von Freitag Morgen bis Sonntag Abend aktiv.</span>
										</div>
									</div>
									<hr class="border-info">
									<div class="form-row mb-1">
										<div class="col">
											Morgensladen
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="nacht2lls1" class="col-md-4 col-form-label">Stromstärke in A</label>
										<div class="col-md-8">
											<div class="form-row vaRow mb-1">
												<label for="nacht2lls1" class="col-2 col-form-label valueLabel" suffix="A"><?php echo $nacht2lls1old; ?> A</label>
												<div class="col-10">
													<input type="range" class="form-control-range rangeInput" name="nacht2lls1" id="nacht2lls1" min="6" max="32" step="1" value="<?php echo $nacht2lls1old; ?>">
												</div>
											</div>
										</div>
									</div>
									<div class="form-row mb-1">
										<div class="col-md-4">
											Zeitspanne
										</div>
										<div class="col">
											<div class="form-row">
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Anfang
															</div>
														</div>
														<select name="nachtladen2abuhrs1" id="nachtladen2abuhrs1" class="form-control">
															<option <?php if($nachtladen2abuhrs1old == 3) echo "selected" ?> value="3">03:00</option>
															<option <?php if($nachtladen2abuhrs1old == 4) echo "selected" ?> value="4">04:00</option>
															<option <?php if($nachtladen2abuhrs1old == 5) echo "selected" ?> value="5">05:00</option>
															<option <?php if($nachtladen2abuhrs1old == 6) echo "selected" ?> value="6">06:00</option>
															<option <?php if($nachtladen2abuhrs1old == 7) echo "selected" ?> value="7">07:00</option>
															<option <?php if($nachtladen2abuhrs1old == 8) echo "selected" ?> value="8">08:00</option>
															<option <?php if($nachtladen2abuhrs1old == 9) echo "selected" ?> value="9">09:00</option>
														</select>
													</div>
												</div>
												<div class="col-sm-6">
													<div class="input-group">
														<div class="input-group-prepend">
															<div class="input-group-text">
																Ende
															</div>
														</div>
														<select name="nachtladen2bisuhrs1" id="nachtladen2bisuhrs1" class="form-control">
															<option <?php if($nachtladen2bisuhrs1old == 4) echo "selected" ?> value="4">04:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 5) echo "selected" ?> value="5">05:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 6) echo "selected" ?> value="6">06:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 7) echo "selected" ?> value="7">07:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 8) echo "selected" ?> value="8">08:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 9) echo "selected" ?> value="9">09:00</option>
															<option <?php if($nachtladen2bisuhrs1old == 10) echo "selected" ?> value="10">10:00</option>
														</select>
													</div>
												</div>
											</div>
											<span class="form-text small">Zeitspanne, in der morgens geladen werden soll.</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_nachtladen() {
								if($('#nachtladenOff').prop("checked")) {
									hideSection('nachtladenan');
								} else {
									showSection('nachtladenan');
								}
							}

							function visibility_nachtladens1() {
								if($('#nachtladens1Off').prop("checked")) {
									hideSection('nachtladenans1');
								} else {
									showSection('nachtladenans1');
								}
							}

							$('input[type=radio][name=nachtladen]').change(function(){
								visibility_nachtladen();
							});

							$('input[type=radio][name=nachtladens1]').change(function(){
								visibility_nachtladens1();
							});

							visibility_nachtladen();
							visibility_nachtladens1()
						});
					</script>
				</div>

				<!-- EVU basiertes Lastmanagement -->
				<div class="card border-warning">
					<div class="card-header bg-warning">
						EVU basiertes Lastmanagement
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									maximale Stromstärken in A
								</div>
								<div class="col">
									<div class="form-row">
										<div class="col-sm-4">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														Phase 1
													</div>
												</div> 
												<input type="number" min="7" max="125" step="1" name="lastmaxap1" id="lastmaxap1" class="form-control" value="<?php echo $lastmaxap1old ?>">
											</div>
										</div>
										<div class="col-sm-4">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														Phase 2
													</div>
												</div> 
												<input type="number" min="7" max="125" step="1" name="lastmaxap2" id="lastmaxap2" class="form-control" value="<?php echo $lastmaxap2old ?>">
											</div>
										</div>
										<div class="col-sm-4">
											<div class="input-group">
												<div class="input-group-prepend">
													<div class="input-group-text">
														Phase 3
													</div>
												</div> 
												<input type="number" min="7" max="125" step="1" name="lastmaxap3" id="lastmaxap3" class="form-control" value="<?php echo $lastmaxap3old ?>">
											</div>
										</div>
									</div>
									<span class="form-text small">Gültige Werte 7-125. Definiert die maximal erlaubte Stromstärke der einzelnen Phasen des Hausanschlusses im Sofort Laden Modus, sofern das EVU Modul die Werte je Phase zur Verfügung stellt.</span>
								</div>
							</div>
							<div class="form-row mb-1">
								<label for="lastmmaxw" class="col-md-4 col-form-label">maximaler Bezug in W</label>
								<div class="col">
									<input class="form-control" type="number" min="2000" max="200000" step="1000" name="lastmmaxw" id="lastmmaxw" value="<?php echo $lastmmaxwold ?>">
									<span class="form-text small">Gültige Werte 2000-200000. Definiert die maximal erlaubten bezogenen Watt des Hausanschlusses im Sofort Laden Modus, sofern die Bezugsleistung bekannt ist.</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Loadsharing -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Loadsharing
					</div>
					<div class="card-body">
						<div id="loadsharingoffdiv" class="card-text alert alert-info hide">
							Diese Einstellungen sind nur verfügbar, wenn mindestens zwei Ladepunkte konfiguriert sind.
						</div>
						<div id="loadsharingdiv" class="hide">
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Loadsharing für Ladepunkte 1 und 2</label>
									<div class="col">
										<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if($loadsharinglp12old == 0) echo " active" ?>">
												<input type="radio" name="loadsharinglp12" id="loadsharinglp12Off" value="0"<?php if($loadsharinglp12old == 0) echo " checked=\"checked\"" ?>>Deaktiviert
											</label>
											<label class="btn btn-outline-info<?php if($loadsharinglp12old == 1) echo " active" ?>">
												<input type="radio" name="loadsharinglp12" id="loadsharinglp12On" value="1"<?php if($loadsharinglp12old == 1) echo " checked=\"checked\"" ?>>Aktiviert
											</label>
										</div>
										<span class="form-text small">
											Wenn Ladepunkt 1 und 2 sich eine Zuleitung teilen, diese Option aktivieren. Sie stellt in jedem Lademodus sicher, dass nicht mehr als 16 bzw. 32A je Phase in der Summe von Ladepunkt 1 und 2 genutzt werden.
											<span class="text-danger">Bei der OpenWB Duo muss diese Option aktiviert werden!</span>
										</span>
									</div>
								</div>
								<div id="loadsharinglp12div" class="hide">
									<div class="form-row mb-2">
										<label class="col-md-4 col-form-label">Maximaler Strom</label>
										<div class="col">
											<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
												<label class="btn btn-outline-info<?php if($loadsharingalp12old == 16) echo " active" ?>">
													<input type="radio" name="loadsharingalp12" id="loadsharingalp1216" value="16"<?php if($loadsharingalp12old == 16) echo " checked=\"checked\"" ?>>16 Ampere
												</label>
												<label class="btn btn-outline-info<?php if($loadsharingalp12old == 32) echo " active" ?>">
													<input type="radio" name="loadsharingalp12" id="loadsharingalp1232" value="32"<?php if($loadsharingalp12old == 32) echo " checked=\"checked\"" ?>>32 Ampere
												</label>
											</div>
										</div>
									</div>
									<div class="alert alert-warning">
										<p class="text-danger">Der richtige Anschluss ist zu gewährleisten.</p>
										<div class="row">
											<div class="col-md-4">Ladepunkt 1:</div>
											<div class="col">
												<ul>
													<li>Zuleitung Phase 1 = Phase 1</li>
													<li>Zuleitung Phase 2 = Phase 2</li>
													<li>Zuleitung Phase 3 = Phase 3</li>
												</ul>
											</div>
										</div>
										<div class="row">
											<div class="col-md-4">Ladepunkt 2:</div>
											<div class="col">
												<ul>
													<li>Zuleitung Phase 1 = <span class="text-danger">Phase 2</span></li>
													<li>Zuleitung Phase 2 = <span class="text-danger">Phase 3</span></li>
													<li>Zuleitung Phase 3 = <span class="text-danger">Phase 1</span></li>
												</ul>
											</div>
										</div>
										<p>Durch das Drehen der Phasen ist sichergestellt, dass 2 einphasige Autos mit voller Geschwindigkeit laden können.</p>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							function visibility_loadsharinglp12() {
								if($('#loadsharinglp12Off').prop("checked")) {
									hideSection('loadsharinglp12div');
								} else {
									showSection('loadsharinglp12div');
								}
							}

							$('input[type=radio][name=loadsharinglp12]').change(function(){
								visibility_loadsharinglp12();
							});

							visibility_loadsharinglp12();
						});
					</script>
				</div>

				<div class="form-row text-center">
					<div class="col">
						<button type="submit" class="btn btn-success">Speichern</button>
					</div>
				</div>
			</form>
		</div>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/Allgemein</small>
			</div>
		</footer>


		<script>
			$('.rangeInput').on('input', function() {
				// show slider value in label of class valueLabel
				updateLabel($(this).attr('id'));
			});

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navAllgemein').addClass('disabled');
				}
			);
		</script>

	</body>
</html>
