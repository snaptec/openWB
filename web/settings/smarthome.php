<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
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
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>

	<body>
		<?php

			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "hook1einschaltverz=") !== false) {
					list(, $hook1einschaltverzold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2einschaltverz=") !== false) {
					list(, $hook2einschaltverzold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2_ausverz=") !== false) {
					list(, $hook2_ausverzold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3_ausverz=") !== false) {
					list(, $hook3_ausverzold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook1_ausverz=") !== false) {
					list(, $hook1_ausverzold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook1ein_url=") !== false) {
					list(, $hook1ein_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "angesteckthooklp1_url=") !== false) {
					list(, $angesteckthooklp1_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook1aus_url=") !== false) {
					list(, $hook1aus_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook1ein_watt=") !== false) {
					list(, $hook1ein_wattold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook1aus_watt=") !== false) {
					list(, $hook1aus_wattold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook1_aktiv=") !== false) {
					list(, $hook1_aktivold) = explode("=", $line, 2);
				}
				if(strpos($line, "angesteckthooklp1=") !== false) {
					list(, $angesteckthooklp1old) = explode("=", $line, 2);
				}

				if(strpos($line, "hook1_dauer=") !== false) {
					list(, $hook1_dauerold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2ein_url=") !== false) {
					list(, $hook2ein_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2aus_url=") !== false) {
					list(, $hook2aus_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2ein_watt=") !== false) {
					list(, $hook2ein_wattold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2aus_watt=") !== false) {
					list(, $hook2aus_wattold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2_aktiv=") !== false) {
					list(, $hook2_aktivold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook2_dauer=") !== false) {
					list(, $hook2_dauerold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3ein_url=") !== false) {
					list(, $hook3ein_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3aus_url=") !== false) {
					list(, $hook3aus_urlold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3ein_watt=") !== false) {
					list(, $hook3ein_wattold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3aus_watt=") !== false) {
					list(, $hook3aus_wattold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3_aktiv=") !== false) {
					list(, $hook3_aktivold) = explode("=", $line, 2);
				}
				if(strpos($line, "hook3_dauer=") !== false) {
					list(, $hook3_dauerold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_aktiv=") !== false) {
					list(, $verbraucher1_aktivold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_typ=") !== false) {
					list(, $verbraucher1_typold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_urlw=") !== false) {
					list(, $verbraucher1_urlwold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_urlh=") !== false) {
					list(, $verbraucher1_urlhold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_name=") !== false) {
					list(, $verbraucher1_nameold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_id=") !== false) {
					list(, $verbraucher1_idold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_ip=") !== false) {
					list(, $verbraucher1_ipold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher1_source=") !== false) {
					list(, $verbraucher1_sourceold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_aktiv=") !== false) {
					list(, $verbraucher2_aktivold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_typ=") !== false) {
					list(, $verbraucher2_typold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_urlw=") !== false) {
					list(, $verbraucher2_urlwold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_urlh=") !== false) {
					list(, $verbraucher2_urlhold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_name=") !== false) {
					list(, $verbraucher2_nameold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_id=") !== false) {
					list(, $verbraucher2_idold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_ip=") !== false) {
					list(, $verbraucher2_ipold) = explode("=", $line, 2);
				}
				if(strpos($line, "verbraucher2_source=") !== false) {
					list(, $verbraucher2_sourceold) = explode("=", $line, 2);
				}
			}

			$angesteckthooklp1_urlold = str_replace( "'", "", $angesteckthooklp1_urlold);

			$hook1ein_urlold = str_replace( "'", "", $hook1ein_urlold);
			$hook1aus_urlold = str_replace( "'", "", $hook1aus_urlold);
			$hook2ein_urlold = str_replace( "'", "", $hook2ein_urlold);
			$hook2aus_urlold = str_replace( "'", "", $hook2aus_urlold);
			$hook3ein_urlold = str_replace( "'", "", $hook3ein_urlold);
			$hook3aus_urlold = str_replace( "'", "", $hook3aus_urlold);
			$verbraucher1_urlwold = str_replace( "'", "", $verbraucher1_urlwold);
			$verbraucher1_urlhold = str_replace( "'", "", $verbraucher1_urlhold);
			$verbraucher2_urlwold = str_replace( "'", "", $verbraucher2_urlwold);
			$verbraucher2_urlhold = str_replace( "'", "", $verbraucher2_urlhold);
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="col-sm-12">
				<form action="./tools/savesmarthome.php" method="POST">
					<div class="row">
						<b><label for="angesteckthooklp1">Webhook bei Anstecken an LP1:</label></b>
						<select name="angesteckthooklp1" id="angesteckthooklp1">
							<option <?php if($angesteckthooklp1old == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($angesteckthooklp1old == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="angesteckthooklp1ausdiv">
					</div>
					<div id="angesteckthooklp1andiv">
						<div class="row">
							<b><label for="angesteckthooklp1_url">URL:</label></b>
							<input type="text" name="angesteckthooklp1_url" id="angesteckthooklp1_url" value="<?php echo htmlspecialchars($angesteckthooklp1_urlold) ?>">
						</div>
						<div class="row">
							URL die (einmalig) aufgerufen wird wenn ein Fahrzeug an LP1 angesteckt wird. Erneutes Ausführen erfolgt erst nachdem abgesteckt wurde.
						</div>
					</div>
					<hr>
					<script>
						$(function() {
							if($('#angesteckthooklp1').val() == '0') {
								$('#angesteckthooklp1ausdiv').show();
								$('#angesteckthooklp1andiv').hide();
							} else {
								$('#angesteckthooklp1ausdiv').hide();
								$('#angesteckthooklp1andiv').show();
							}

							$('#angesteckthooklp1').change(function(){
								if($('#angesteckthooklp1').val() == '0') {
									$('#angesteckthooklp1ausdiv').show();
									$('#angesteckthooklp1andiv').hide();
								} else {
									$('#angesteckthooklp1ausdiv').hide();
									$('#angesteckthooklp1andiv').show();
								}
							});
						});
					</script>

					<div class="row">
						<b><label for="hook1_aktiv">Externes Gerät 1:</label></b>
						<select name="hook1_aktiv" id="hook1_aktiv">
							<option <?php if($hook1_aktivold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($hook1_aktivold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="hook1ausdiv">
					</div>
					<div id="hook1andiv">
						<div class="row">
							Externe Geräte lassen sich per definierter URL (Webhook) an- und ausschalten in Abhängigkeit des Überschusses
						</div>
						<div class="row">
							<b><label for="hook1ein_watt">Gerät 1 Einschaltschwelle:</label></b>
							<input type="text" name="hook1ein_watt" id="hook1ein_watt" value="<?php echo $hook1ein_wattold ?>">
						</div>
						<div class="row">
							Einschaltschwelle in Watt bei die unten stehende URL aufgerufen wird.
						</div>
						<div class="row">
							<b><label for="hook1einschaltverz">Gerät 1 Einschaltverzögerung:</label></b>
							<input type="text" name="hook1einschaltverz" id="hook1einschaltverz" value="<?php echo $hook1einschaltverzold ?>">
						</div>
						<div class="row">
							Bestimmt die Dauer für die die Einschaltschwelle überschritten werden muss bevor eingeschaltet wird.<br><br>
						</div>
						<div class="row">
							<b><label for="hook1ein_url">Gerät 1 Einschalturl:</label></b>
							<input type="text" name="hook1ein_url" id="hook1ein_url" value="<?php echo htmlspecialchars($hook1ein_urlold) ?>">
						</div>
						<div class="row">
							Einschalturl die aufgerufen wird bei entsprechendem Überschuss.
						</div>
						<div class="row">
							<b><label for="hook1_dauer">Gerät 1 Einschaltdauer:</label></b>
							<input type="text" name="hook1_dauer" id="hook1_dauer" value="<?php echo $hook1_dauerold ?>">
						</div>
						<div class="row">
							Einschaltdauer in Minuten. Gibt an wie lange das Gerät nach Start mindestens aktiv bleiben muss ehe Ausschalturl aufgerufen wird.
						</div>
						<div class="row">
							<b><label for="hook1aus_watt">Gerät 1 Ausschaltschwelle:</label></b>
							<input type="text" name="hook1aus_watt" id="hook1aus_watt" value="<?php echo $hook1aus_wattold ?>">
						</div>
						<div class="row">
							Ausschaltschwelle in Watt bei die unten stehende URL aufgerufen wird. Soll die Abschaltung bei Bezug stattfinden eine negative Zahl eingeben.
						</div>
						<div class="row">
							<b><label for="hook1aus_url">Gerät 1 Ausschalturl:</label></b>
							<input type="text" name="hook1aus_url" id="hook1aus_url" value="<?php echo htmlspecialchars($hook1aus_urlold) ?>">
						</div>
						<div class="row">
							Ausschalturl die aufgerufen wird bei entsprechendem Überschuss.
						</div>
						<div class="row">
							<b><label for="hook1_ausverz">Gerät 1 Ausschaltverzögerung:</label></b>
							<input type="text" name="hook1_ausverz" id="hook1_ausverz" value="<?php echo $hook1_ausverzold ?>">
						</div>
						<div class="row">
							Bestimmt die Dauer für die die Ausschaltschwelle unterschritten werden muss bevor ausgeschaltet wird.
						</div>
					</div>
					<script>
						$(function() {
							if($('#hook1_aktiv').val() == '0') {
								$('#hook1ausdiv').show();
								$('#hook1andiv').hide();
							} else {
								$('#hook1ausdiv').hide();
								$('#hook1andiv').show();
							}

							$('#hook1_aktiv').change(function(){
								if($('#hook1_aktiv').val() == '0') {
									$('#hook1ausdiv').show();
									$('#hook1andiv').hide();
								} else {
									$('#hook1ausdiv').hide();
									$('#hook1andiv').show();
								}
							});
						});
					</script>
					<hr>
					<div class="row">
						<b><label for="hook2_aktiv">Externes Gerät 2:</label></b>
						<select name="hook2_aktiv" id="hook2_aktiv">
							<option <?php if($hook2_aktivold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($hook2_aktivold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="hook2ausdiv">
					</div>
					<div id="hook2andiv">
						<div class="row">
							Externe Geräte lassen sich per definierter URL (Webhook) an- und ausschalten in Abhängigkeit des Überschusses
						</div>
						<div class="row">
							<b><label for="hook2ein_watt">Gerät 2 Einschaltschwelle:</label></b>
							<input type="text" name="hook2ein_watt" id="hook2ein_watt" value="<?php echo $hook2ein_wattold ?>">
						</div>
						<div class="row">
							Einschaltschwelle in Watt bei die unten stehende URL aufgerufen wird.
						</div>
						<div class="row">
							<b><label for="hook2einschaltverz">Gerät 2 Einschaltverzögerung:</label></b>
							<input type="text" name="hook2einschaltverz" id="hook2einschaltverz" value="<?php echo $hook2einschaltverzold ?>">
						</div>
						<div class="row">
							Bestimmt die Dauer für die die Einschaltschwelle überschritten werden muss bevor eingeschaltet wird.<br><br>
						</div>
						<div class="row">
							<b><label for="hook2ein_url">Gerät 2 Einschalturl:</label></b>
							<input type="text" name="hook2ein_url" id="hook2ein_url" value="<?php echo htmlspecialchars($hook2ein_urlold) ?>">
						</div>
						<div class="row">
							Einschalturl die aufgerufen wird bei entsprechendem Überschuss.
						</div>
						<div class="row">
							<b><label for="hook2_dauer">Gerät 2 Einschaltdauer:</label></b>
							<input type="text" name="hook2_dauer" id="hook2_dauer" value="<?php echo $hook2_dauerold ?>">
						</div>
						<div class="row">
							Einschaltdauer in Minuten. Gibt an wie lange das Gerät nach Start mindestens aktiv bleiben muss ehe Ausschalturl aufgerufen wird.
						</div>
						<div class="row">
							<b><label for="hook2aus_watt">Gerät 2 Ausschaltschwelle:</label></b>
							<input type="text" name="hook2aus_watt" id="hook2aus_watt" value="<?php echo $hook2aus_wattold ?>">
						</div>
						<div class="row">
							Ausschaltschwelle in Watt bei die unten stehende URL aufgerufen wird. Soll die Abschaltung bei Bezug stattfinden eine negative Zahl eingeben.
						</div>
						<div class="row">
							<b><label for="hook2aus_url">Gerät 2 Ausschalturl:</label></b>
							<input type="text" name="hook2aus_url" id="hook2aus_url" value="<?php echo htmlspecialchars($hook2aus_urlold) ?>">
						</div>
						<div class="row">
							Ausschalturl die aufgerufen wird bei entsprechendem Überschuss.
						</div>
						<div class="row">
							<b><label for="hook2_ausverz">Gerät 2 Ausschaltverzögerung:</label></b>
							<input type="text" name="hook2_ausverz" id="hook2_ausverz" value="<?php echo $hook2_ausverzold ?>">
						</div>
						<div class="row">
							Bestimmt die Dauer für die die Ausschaltschwelle unterschritten werden muss bevor ausgeschaltet wird.
						</div>
					</div>
					<script>
						$(function() {
							if($('#hook2_aktiv').val() == '0') {
								$('#hook2ausdiv').show();
								$('#hook2andiv').hide();
							} else {
								$('#hook2ausdiv').hide();
								$('#hook2andiv').show();
							}

							$('#hook2_aktiv').change(function(){
								if($('#hook2_aktiv').val() == '0') {
									$('#hook2ausdiv').show();
									$('#hook2andiv').hide();
								} else {
									$('#hook2ausdiv').hide();
									$('#hook2andiv').show();
								}
							});
						});
					</script>
					<hr>
					<div class="row">
						<b><label for="hook3_aktiv">Externes Gerät 3:</label></b>
						<select name="hook3_aktiv" id="hook3_aktiv">
							<option <?php if($hook3_aktivold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($hook3_aktivold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="hook3ausdiv">
					</div>
					<div id="hook3andiv">
						<div class="row">
							Externe Geräte lassen sich per definierter URL (Webhook) an- und ausschalten in Abhängigkeit des Überschusses
						</div>
						<div class="row">
							<b><label for="hook3ein_watt">Gerät 3 Einschaltschwelle:</label></b>
							<input type="text" name="hook3ein_watt" id="hook3ein_watt" value="<?php echo $hook3ein_wattold ?>">
						</div>
						<div class="row">
							Einschaltschwelle in Watt bei die unten stehende URL aufgerufen wird.
						</div>
						<div class="row">
							<b><label for="hook3ein_url">Gerät 3 Einschalturl:</label></b>
							<input type="text" name="hook3ein_url" id="hook3ein_url" value="<?php echo htmlspecialchars($hook3ein_urlold) ?>">
						</div>
						<div class="row">
							Einschalturl die aufgerufen wird bei entsprechendem Überschuss.
						</div>
						<div class="row">
							<b><label for="hook3_dauer">Gerät 3 Einschaltdauer:</label></b>
							<input type="text" name="hook3_dauer" id="hook3_dauer" value="<?php echo $hook3_dauerold ?>">
						</div>
						<div class="row">
							Einschaltdauer in Minuten. Gibt an wie lange das Gerät nach Start mindestens aktiv bleiben muss ehe Ausschalturl aufgerufen wird.
						</div>
						<div class="row">
							<b><label for="hook3aus_watt">Gerät 3 Ausschaltschwelle:</label></b>
							<input type="text" name="hook3aus_watt" id="hook3aus_watt" value="<?php echo $hook3aus_wattold ?>">
						</div>
						<div class="row">
							Ausschaltschwelle in Watt bei die unten stehende URL aufgerufen wird. Soll die Abschaltung bei Bezug stattfinden eine negative Zahl eingeben.
						</div>
						<div class="row">
							<b><label for="hook3aus_url">Gerät 3 Ausschalturl:</label></b>
							<input type="text" name="hook3aus_url" id="hook3aus_url" value="<?php echo htmlspecialchars($hook3aus_urlold) ?>">
						</div>
						<div class="row">
							Ausschalturl die aufgerufen wird bei entsprechendem Überschuss.
						</div>
						<div class="row">
							<b><label for="hook1_ausverz">Gerät 3 Ausschaltverzögerung:</label></b>
							<input type="text" name="hook3_ausverz" id="hook3_ausverz" value="<?php echo $hook3_ausverzold ?>">
						</div>
						<div class="row">
							Bestimmt die Dauer für die die Ausschaltschwelle unterschritten werden muss bevor ausgeschaltet wird.
						</div>
					</div><hr>
					<script>
						$(function() {
							if($('#hook3_aktiv').val() == '0') {
								$('#hook3ausdiv').show();
								$('#hook3andiv').hide();
							} else {
								$('#hook3ausdiv').hide();
								$('#hook3andiv').show();
							}

							$('#hook3_aktiv').change(function(){
								if($('#hook3_aktiv').val() == '0') {
									$('#hook3ausdiv').show();
									$('#hook3andiv').hide();
								} else {
									$('#hook3ausdiv').hide();
									$('#hook3andiv').show();
								}
							});
						});
					</script>

					<div class="row">
						<b><label for="verbraucher1_aktiv">Verbraucher 1:</label></b>
						<select name="verbraucher1_aktiv" id="verbraucher1_aktiv">
							<option <?php if($verbraucher1_aktivold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($verbraucher1_aktivold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="verbraucher1ausdiv">
					</div>
					<div id="verbraucher1andiv">
						<div class="row">
							Externe Verbraucher lassen sich in das Logging von OpenWB mit einbinden.
						</div>
						<div class="row">
							<b><label for="verbraucher1_typ">Anbindung Verbraucher 1:</label></b>
							<select name="verbraucher1_typ" id="verbraucher1_typ">
								<option <?php if($verbraucher1_typold == "http\n") echo "selected" ?> value="http">Http Abfrage</option>
								<option <?php if($verbraucher1_typold == "mpm3pm\n") echo "selected" ?> value="mpm3pm">MPM3PM</option>
								<option <?php if($verbraucher1_typold == "sdm120\n") echo "selected" ?> value="sdm120">SDM120</option>
								<option <?php if($verbraucher1_typold == "sdm630\n") echo "selected" ?> value="sdm630">SDM630</option>
								<option <?php if($verbraucher1_typold == "tasmota\n") echo "selected" ?> value="tasmota">Sonoff mit Tasmota FW</option>
								<option <?php if($verbraucher1_typold == "shelly\n") echo "selected" ?> value="shelly">Shelly 1PM</option>
							</select>
						</div>
						<div class="row">
							<b><label for="verbraucher1_name">Verbraucher 1 Name:</label></b>
							<input type="text" name="verbraucher1_name" id="verbraucher1_name" value="<?php echo $verbraucher1_nameold ?>">
						</div>
						<div class="row">
							Name des Verbrauchers 1.
						</div>
						<div id="v1http">
							<div class="row">
								<b><label for="verbraucher1_urlw">Verbraucher 1 URL:</label></b>
								<input size="50" type="text" name="verbraucher1_urlw" id="verbraucher1_urlw" value="<?php echo htmlspecialchars($verbraucher1_urlwold) ?>">
							</div>
							<div class="row">
								URL des Verbrauchers Momentanleistung in Watt.
							</div>
							<div class="row">
								<b><label for="verbraucher1_urlh">Verbraucher 1 URL:</label></b>
								<input size="50" type="text" name="verbraucher1_urlh" id="verbraucher1_urlh" value="<?php echo htmlspecialchars($verbraucher1_urlhold) ?>">
							</div>
							<div class="row">
								URL des Verbrauchers Zählerststandes in Watt Stunden.
							</div>
						</div>
						<div id="v1modbus">
							<div class="row">
								<b><label for="verbraucher1_source">Verbraucher 1 Source:</label></b>
								<input type="text" name="verbraucher1_source" id="verbraucher1_source" value="<?php echo $verbraucher1_sourceold ?>">
							</div>
							<div class="row">
								Bei lokal angeschlossenem Zähler ist dies /dev/ttyUSB3 (z.B.). Wird ein Modbus Ethernet Konverter genutzt, z.B. der aus dem Shop, hier die IP Adresse eintragen.
							</div>
							<div class="row">
								<b><label for="verbraucher1_id">Verbraucher 1 ID:</label></b>
								<input type="text" name="verbraucher1_id" id="verbraucher1_id" value="<?php echo $verbraucher1_idold ?>">
							</div>
							<div class="row">
								Modbus ID.
							</div>
						</div>
						<div id="v1tasmota">
							<div class="row">
								<b><label for="verbraucher1_ip">Verbraucher 1 IP:</label></b>
								<input type="text" name="verbraucher1_ip" id="verbraucher1_ip" value="<?php echo $verbraucher1_ipold ?>">
							</div>
							<div class="row">
								IP Adresse des Geräts.
							</div>
						</div>
					</div>

					<script>
						function display_verbraucher1 () {
							$('#v1http').hide();
							$('#v1modbus').hide();
							$('#v1tasmota').hide();
							if($('#verbraucher1_typ').val() == 'http') {
								$('#v1http').show();
							}
							if($('#verbraucher1_typ').val() == 'mpm3pm') {
								$('#v1modbus').show();
							}
							if($('#verbraucher1_typ').val() == 'sdm630') {
								$('#v1modbus').show();
							}
							if($('#verbraucher1_typ').val() == 'sdm120') {
								$('#v1modbus').show();
							}
							if($('#verbraucher1_typ').val() == 'tasmota') {
								$('#v1tasmota').show();
							}
							if($('#verbraucher1_typ').val() == 'shelly') {
								$('#v1tasmota').show();
							}

						}

						display_verbraucher1();
						$('#verbraucher1_typ').change(function(){
							display_verbraucher1();
						});

						$(function() {
							if($('#verbraucher1_aktiv').val() == '0') {
								$('#verbraucher1ausdiv').show();
								$('#verbraucher1andiv').hide();
							} else {
								$('#verbraucher1ausdiv').hide();
								$('#verbraucher1andiv').show();
							}

							$('#verbraucher1_aktiv').change(function(){
								if($('#verbraucher1_aktiv').val() == '0') {
									$('#verbraucher1ausdiv').show();
									$('#verbraucher1andiv').hide();
								} else {
									$('#verbraucher1ausdiv').hide();
									$('#verbraucher1andiv').show();
								}
							});
						});
					</script>

					<hr>
					<div class="row">
						<b><label for="verbraucher2_aktiv">Verbraucher 2:</label></b>
						<select name="verbraucher2_aktiv" id="verbraucher2_aktiv">
							<option <?php if($verbraucher2_aktivold == 0) echo "selected" ?> value="0">Deaktiviert</option>
							<option <?php if($verbraucher2_aktivold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
					</div>

					<div id="verbraucher2ausdiv">
					</div>
					<div id="verbraucher2andiv">
						<div class="row">
							Externe Verbraucher lassen sich in das Logging von OpenWB mit einbinden.
						</div>
						<div class="row">
							<b><label for="verbraucher2_typ">Anbindung Verbraucher 2:</label></b>
							<select name="verbraucher2_typ" id="verbraucher2_typ">
								<option <?php if($verbraucher2_typold == "http\n") echo "selected" ?> value="http">Http Abfrage</option>
								<option <?php if($verbraucher2_typold == "mpm3pm\n") echo "selected" ?> value="mpm3pm">MPM3PM</option>
								<option <?php if($verbraucher2_typold == "sdm120\n") echo "selected" ?> value="sdm120">SDM120</option>
								<option <?php if($verbraucher2_typold == "sdm630\n") echo "selected" ?> value="sdm630">SDM630</option>
								<option <?php if($verbraucher2_typold == "tasmota\n") echo "selected" ?> value="tasmota">Sonoff mit Tasmota FW</option>
							</select>
						</div>
						<div class="row">
							<b><label for="verbraucher2_name">Verbraucher 2 Name:</label></b>
							<input type="text" name="verbraucher2_name" id="verbraucher2_name" value="<?php echo $verbraucher2_nameold ?>">
						</div>
						<div class="row">
							Name des Verbrauchers 2.
						</div>
						<div id="v2http">
							<div class="row">
								<b><label for="verbraucher2_urlw">Verbraucher 2 URL:</label></b>
								<input size="50" type="text" name="verbraucher2_urlw" id="verbraucher2_urlw" value="<?php echo htmlspecialchars($verbraucher2_urlwold) ?>">
							</div>
							<div class="row">
								URL des Verbrauchers Momentanleistung in Watt.
							</div>
							<div class="row">
								<b><label for="verbraucher2_urlh">Verbraucher 2 URL:</label></b>
								<input size="50" type="text" name="verbraucher2_urlh" id="verbraucher2_urlh" value="<?php echo htmlspecialchars($verbraucher2_urlhold) ?>">
							</div>
							<div class="row">
								URL des Verbrauchers Zählerststandes in Watt Stunden.
							</div>
						</div>
						<div id="v2modbus">
							<div class="row">
								<b><label for="verbraucher2_source">Verbraucher 2 Source:</label></b>
								<input type="text" name="verbraucher2_source" id="verbraucher2_source" value="<?php echo $verbraucher2_sourceold ?>">
							</div>
							<div class="row">
								Bei lokal angeschlossenem Zähler ist dies /dev/ttyUSB3 (z.B.). Wird ein Modbus Ethernet Konverter genutzt, z.B. der aus dem Shop, hier die IP Adresse eintragen.
							</div>
							<div class="row">
								<b><label for="verbraucher2_id">Verbraucher 2 ID:</label></b>
								<input type="text" name="verbraucher2_id" id="verbraucher2_id" value="<?php echo $verbraucher2_idold ?>">
							</div>
							<div class="row">
								Modbus ID.
							</div>
						</div>
						<div id="v2tasmota">
							<div class="row">
								<b><label for="verbraucher2_ip">Verbraucher 2 IP:</label></b>
								<input type="text" name="verbraucher2_ip" id="verbraucher2_ip" value="<?php echo $verbraucher2_ipold ?>">
							</div>
							<div class="row">
								IP Adresse des Tasmota Sonoff Geräts.
							</div>
						</div>
					</div>

					<script>
						function display_verbraucher2 () {
							$('#v2http').hide();
							$('#v2modbus').hide();
							$('#v2tasmota').hide();
							if($('#verbraucher2_typ').val() == 'http') {
								$('#v2http').show();
							}
							if($('#verbraucher2_typ').val() == 'mpm3pm') {
								$('#v2modbus').show();
							}
							if($('#verbraucher2_typ').val() == 'sdm630') {
								$('#v2modbus').show();
							}
							if($('#verbraucher2_typ').val() == 'sdm120') {
								$('#v2modbus').show();
							}
							if($('#verbraucher2_typ').val() == 'tasmota') {
								$('#v2tasmota').show();
							}
						}

						display_verbraucher2();

						$('#verbraucher2_typ').change(function(){
							display_verbraucher2();
						});

						$(function() {
							if($('#verbraucher2_aktiv').val() == '0') {
								$('#verbraucher2ausdiv').show();
								$('#verbraucher2andiv').hide();
							} else {
								$('#verbraucher2ausdiv').hide();
								$('#verbraucher2andiv').show();
							}

							$('#verbraucher2_aktiv').change(function(){
								if($('#verbraucher2_aktiv').val() == '0') {
									$('#verbraucher2ausdiv').show();
									$('#verbraucher2andiv').hide();
								} else {
									$('#verbraucher2ausdiv').hide();
									$('#verbraucher2andiv').show();
								}
							});
						});
					</script>

					<button type="submit" class="btn btn-green">Save</button>
	 			</form>

				<div class="row justify-content-center">
					<div class="col text-center">
						Open Source made with love!<br>
						Jede Spende hilft die Weiterentwicklung von openWB vorranzutreiben<br>
						<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
							<input type="hidden" name="cmd" value="_s-xclick">
							<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
							<input type="image" src="./img/btn_donate_SM.gif" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
							<img alt="" src="./img/pixel.gif" width="1" height="1">
						</form>
					</div>
				</div>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/Smart Home</small>
			</div>
		</footer>


		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navSmartHome').addClass('disabled');
			});

		</script>

	</body>
</html>
