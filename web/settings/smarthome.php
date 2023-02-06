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
			<h1>SmartHome</h1>
			<form action="./settings/saveconfig.php" method="POST">
				<div class="alert alert-danger">
					Dieser Bereich wird bald entfernt. Bitte SmartHome 2.0 nutzen.<br />
					Werden Teile dieser Seite noch benötigt? Dann bitte <a href="https://www.openwb.de/forum/viewtopic.php?f=14&t=5777" target="_blank" rel="noopener noreferrer">hier im Forum</a> melden.
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						WebHooks
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Nach Anstecken an Ladepunkt 1</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($angesteckthooklp1old == 0) echo " active" ?>">
											<input type="radio" name="angesteckthooklp1" id="angesteckthooklp1Off" value="0"<?php if($angesteckthooklp1old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($angesteckthooklp1old == 1) echo " active" ?>">
											<input type="radio" name="angesteckthooklp1" id="angesteckthooklp1On" value="1"<?php if($angesteckthooklp1old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
							<div id="angesteckthooklp1andiv">
								<div class="form-row mb-1">
									<label for="angesteckthooklp1_url" class="col-md-4 col-form-label">URL</label>
									<div class="col">
										<input class="form-control" type="text" name="angesteckthooklp1_url" id="angesteckthooklp1_url" value="<?php echo htmlspecialchars($angesteckthooklp1_urlold) ?>">
										<span class="form-text small">URL die (einmalig) aufgerufen wird wenn ein Fahrzeug an LP1 angesteckt wird. Erneutes Ausführen erfolgt erst nachdem abgesteckt wurde.</span>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Nach Abstecken an Ladepunkt 1</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($abgesteckthooklp1old == 0) echo " active" ?>">
											<input type="radio" name="abgesteckthooklp1" id="abgesteckthooklp1Off" value="0"<?php if($abgesteckthooklp1old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($angesteckthooklp1old == 1) echo " active" ?>">
											<input type="radio" name="abgesteckthooklp1" id="abgesteckthooklp1On" value="1"<?php if($abgesteckthooklp1old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
							<div id="abgesteckthooklp1andiv">
								<div class="form-row mb-1">
									<label for="abgesteckthooklp1_url" class="col-md-4 col-form-label">URL</label>
									<div class="col">
										<input class="form-control" type="text" name="abgesteckthooklp1_url" id="abgesteckthooklp1_url" value="<?php echo htmlspecialchars($abgesteckthooklp1_urlold) ?>">
										<span class="form-text small">URL die (einmalig) aufgerufen wird wenn ein Fahrzeug an LP1 abgesteckt wird. Erneutes Ausführen erfolgt erst nachdem angesteckt wurde.</span>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Nach Ladestart an Ladepunkt 1</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($ladestarthooklp1old == 0) echo " active" ?>">
											<input type="radio" name="ladestarthooklp1" id="ladestarthooklp1Off" value="0"<?php if($ladestarthooklp1old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($ladestarthooklp1old == 1) echo " active" ?>">
											<input type="radio" name="ladestarthooklp1" id="ladestarthooklp1On" value="1"<?php if($ladestarthooklp1old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
							<div id="ladestarthooklp1andiv">
								<div class="form-row mb-1">
									<label for="ladestarthooklp1_url" class="col-md-4 col-form-label">URL</label>
									<div class="col">
										<input class="form-control" type="text" name="ladestarthooklp1_url" id="ladestarthooklp1_url" value="<?php echo htmlspecialchars($ladestarthooklp1_urlold) ?>">
										<span class="form-text small">URL die (einmalig) aufgerufen wird wenn ein Ladevorgang an LP1 startet. Erneutes Ausführen erfolgt erst nachdem der Ladevorgang gestoppt wurde.</span>
									</div>
								</div>
							</div>
							<hr class="border-secondary">
							<div class="form-row mb-1">
								<label class="col-md-4 col-form-label">Nach Ladestopp an Ladepunkt 1</label>
								<div class="col">
									<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($ladestophooklp1old == 0) echo " active" ?>">
											<input type="radio" name="ladestophooklp1" id="ladestophooklp1Off" value="0"<?php if($ladestophooklp1old == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($ladestophooklp1old == 1) echo " active" ?>">
											<input type="radio" name="ladestophooklp1" id="ladestophooklp1On" value="1"<?php if($ladestophooklp1old == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
							<div id="ladestophooklp1andiv">
								<div class="form-row mb-1">
									<label for="ladestophooklp1_url" class="col-md-4 col-form-label">URL</label>
									<div class="col">
										<input class="form-control" type="text" name="ladestophooklp1_url" id="ladestophooklp1_url" value="<?php echo htmlspecialchars($ladestophooklp1_urlold) ?>">
										<span class="form-text small">URL die (einmalig) aufgerufen wird wenn ein Ladevorgang an LP1 stoppt. Erneutes Ausführen erfolgt erst nachdem der Ladevorgang gestartet wurde.</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<script>
						$(function() {
							if($('#angesteckthooklp1Off').prop("checked")) {
								hideSection('#angesteckthooklp1andiv');
							} else {
								showSection('#angesteckthooklp1andiv');
							}

							$('input[type=radio][name=angesteckthooklp1]').change(function(){
								if(this.value == '0') {
									hideSection('#angesteckthooklp1andiv');
								} else {
									showSection('#angesteckthooklp1andiv');
								}
							});
							if($('#abgesteckthooklp1Off').prop("checked")) {
								hideSection('#abgesteckthooklp1andiv');
							} else {
								showSection('#abgesteckthooklp1andiv');
							}

							$('input[type=radio][name=abgesteckthooklp1]').change(function(){
								if(this.value == '0') {
									hideSection('#abgesteckthooklp1andiv');
								} else {
									showSection('#abgesteckthooklp1andiv');
								}
							});
							if($('#ladestarthooklp1Off').prop("checked")) {
								hideSection('#ladestarthooklp1andiv');
							} else {
								showSection('#ladestarthooklp1andiv');
							}

							$('input[type=radio][name=ladestarthooklp1]').change(function(){
								if(this.value == '0') {
									hideSection('#ladestarthooklp1andiv');
								} else {
									showSection('#ladestarthooklp1andiv');
								}
							});
							if($('#ladestophooklp1Off').prop("checked")) {
								hideSection('#ladestophooklp1andiv');
							} else {
								showSection('#ladestophooklp1andiv');
							}

							$('input[type=radio][name=ladestophooklp1]').change(function(){
								if(this.value == '0') {
									hideSection('#ladestophooklp1andiv');
								} else {
									showSection('#ladestophooklp1andiv');
								}
							});
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Externe Geräte
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Externe Geräte lassen sich per definierter URL (Webhook) in Abhängigkeit vom Überschuss an- und ausschalten.
						</div>
						<?php for( $deviceNum = 1; $deviceNum < 4; $deviceNum++ ){ ?>
							<?php if( $deviceNum > 1){ ?>
							<hr class="border-secondary">
							<?php } ?>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Gerät <?php echo $deviceNum; ?></label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if(${"hook" . $deviceNum . "_aktivold"} == 0) echo " active" ?>">
												<input type="radio" name="hook<?php echo $deviceNum; ?>_aktiv" id="hook<?php echo $deviceNum; ?>_aktivOff" value="0"<?php if(${"hook" . $deviceNum . "_aktivold"} == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if(${"hook" . $deviceNum . "_aktivold"} == 1) echo " active" ?>">
												<input type="radio" name="hook<?php echo $deviceNum; ?>_aktiv" id="hook<?php echo $deviceNum; ?>_aktivOn" value="1"<?php if(${"hook" . $deviceNum . "_aktivold"} == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
									</div>
								</div>
								<div id="hook<?php echo $deviceNum; ?>andiv">
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>ein_watt" class="col-md-4 col-form-label">Einschaltschwelle</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="10" name="hook<?php echo $deviceNum; ?>ein_watt" id="hook<?php echo $deviceNum; ?>ein_watt" value="<?php echo ${"hook" . $deviceNum . "ein_wattold"} ?>">
											<span class="form-text small">Einschaltschwelle in Watt, bei deren Erreichen das Gerät eingeschaltet werden soll.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>einschaltverz" class="col-md-4 col-form-label">Einschaltverzögerung</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="hook<?php echo $deviceNum; ?>einschaltverz" id="hook<?php echo $deviceNum; ?>einschaltverz" value="<?php echo ${"hook" . $deviceNum . "einschaltverzold"} ?>">
											<span class="form-text small">Bestimmt die Dauer in Sekunden, für die die Einschaltschwelle überschritten werden muss bevor eingeschaltet wird.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>ein_url" class="col-md-4 col-form-label">Einschalt-URL</label>
										<div class="col">
											<input class="form-control" type="text" name="hook<?php echo $deviceNum; ?>ein_url" id="hook<?php echo $deviceNum; ?>ein_url" value="<?php echo htmlspecialchars(${"hook" . $deviceNum . "ein_urlold"}) ?>">
											<span class="form-text small">Einschalt-Url die aufgerufen wird bei entsprechendem Überschuss.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>_dauer" class="col-md-4 col-form-label">Einschaltdauer</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="hook<?php echo $deviceNum; ?>_dauer" id="hook<?php echo $deviceNum; ?>_dauer" value="<?php echo ${"hook" . $deviceNum . "_dauerold"} ?>">
											<span class="form-text small">Einschaltdauer in Minuten. Gibt an, wie lange das Gerät nach Start mindestens aktiv bleiben muss, ehe die Ausschalt-Url aufgerufen wird.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>aus_watt" class="col-md-4 col-form-label">Ausschaltschwelle</label>
										<div class="col">
											<input class="form-control" type="number" step="10" name="hook<?php echo $deviceNum; ?>aus_watt" id="hook<?php echo $deviceNum; ?>aus_watt" value="<?php echo ${"hook" . $deviceNum . "aus_wattold"} ?>">
											<span class="form-text small">Ausschaltschwelle in Watt bei die unten stehende URL aufgerufen wird. Soll die Abschaltung bei Bezug stattfinden eine negative Zahl eingeben.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>aus_url" class="col-md-4 col-form-label">Ausschalt-URL</label>
										<div class="col">
											<input class="form-control" type="text" name="hook<?php echo $deviceNum; ?>aus_url" id="hook<?php echo $deviceNum; ?>aus_url" value="<?php echo htmlspecialchars(${"hook" . $deviceNum . "aus_urlold"}) ?>">
											<span class="form-text small">Ausschalt-Url, die aufgerufen wird bei entsprechendem Überschuss.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="hook<?php echo $deviceNum; ?>_ausverz" class="col-md-4 col-form-label">Ausschaltverzögerung</label>
										<div class="col">
											<input class="form-control" type="number" min="0" step="1" name="hook<?php echo $deviceNum; ?>_ausverz" id="hook<?php echo $deviceNum; ?>_ausverz" value="<?php echo ${"hook" . $deviceNum . "_ausverzold"} ?>">
											<span class="form-text small">Bestimmt die Dauer in Sekunden, für die die Ausschaltschwelle unterschritten werden muss, bevor ausgeschaltet wird.</span>
										</div>
									</div>
								</div>
							</div>
						<?php } ?>
					</div>
					<script>
						$(function() {
							<?php for ( $deviceNum = 1; $deviceNum < 4; $deviceNum++ ){ ?>
								if($('#hook<?php echo $deviceNum; ?>_aktivOff').prop("checked")) {
									hideSection('#hook<?php echo $deviceNum; ?>andiv');
								} else {
									showSection('#hook<?php echo $deviceNum; ?>andiv');
								}

								$('input[type=radio][name=hook<?php echo $deviceNum; ?>_aktiv]').change(function(){
									if(this.value == '0') {
										hideSection('#hook<?php echo $deviceNum; ?>andiv');
									} else {
										showSection('#hook<?php echo $deviceNum; ?>andiv');
									}
								});
							<?php } ?>
						});
					</script>
				</div>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Verbraucher
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Externe Verbraucher lassen sich in das Logging von OpenWB einbinden.
						</div>
						<?php for( $deviceNum = 1; $deviceNum < 3; $deviceNum++ ){ ?>
							<?php if( $deviceNum > 1){ ?>
							<hr class="border-secondary">
							<?php } ?>
							<div class="form-group">
								<div class="form-row mb-1">
									<label class="col-md-4 col-form-label">Verbraucher <?php echo $deviceNum; ?></label>
									<div class="col">
										<div class="btn-group btn-group-toggle btn-block" data-toggle="buttons">
											<label class="btn btn-outline-info<?php if(${"verbraucher" . $deviceNum . "_aktivold"} == 0) echo " active" ?>">
												<input type="radio" name="verbraucher<?php echo $deviceNum; ?>_aktiv" id="verbraucher<?php echo $deviceNum; ?>_aktivOff" value="0"<?php if(${"verbraucher" . $deviceNum . "_aktivold"} == 0) echo " checked=\"checked\"" ?>>Aus
											</label>
											<label class="btn btn-outline-info<?php if(${"verbraucher" . $deviceNum . "_aktivold"} == 1) echo " active" ?>">
												<input type="radio" name="verbraucher<?php echo $deviceNum; ?>_aktiv" id="verbraucher<?php echo $deviceNum; ?>_aktivOn" value="1"<?php if(${"verbraucher" . $deviceNum . "_aktivold"} == 1) echo " checked=\"checked\"" ?>>An
											</label>
										</div>
									</div>
								</div>
								<div id="verbraucher<?php echo $deviceNum; ?>andiv">
									<div class="form-row mb-1">
										<label for="verbraucher<?php echo $deviceNum; ?>_name" class="col-md-4 col-form-label">Name</label>
										<div class="col">
											<input class="form-control" type="text" name="verbraucher<?php echo $deviceNum; ?>_name" id="verbraucher<?php echo $deviceNum; ?>_name" value="<?php echo ${"verbraucher" . $deviceNum . "_nameold"} ?>">
											<span class="form-text small">Name des Verbrauchers.</span>
										</div>
									</div>
									<div class="form-row mb-1">
										<label for="verbraucher<?php echo $deviceNum; ?>_typ" class="col-md-4 col-form-label">Anbindung</label>
										<div class="col">
											<select name="verbraucher<?php echo $deviceNum; ?>_typ" id="verbraucher<?php echo $deviceNum; ?>_typ" class="form-control">
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "http") echo "selected" ?> value="http">Http Abfrage</option>
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "mpm3pm") echo "selected" ?> value="mpm3pm">MPM3PM</option>
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "sdm120") echo "selected" ?> value="sdm120">SDM120</option>
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "sdm630") echo "selected" ?> value="sdm630">SDM630</option>
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "abb-b23") echo "selected" ?> value="abb-b23">ABB-B23</option>
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "tasmota") echo "selected" ?> value="tasmota">Sonoff mit Tasmota FW</option>
												<option <?php if(${"verbraucher" . $deviceNum . "_typold"} == "shelly") echo "selected" ?> value="shelly">Shelly 1PM</option>
											</select>
										</div>
									</div>
									<div id="v<?php echo $deviceNum; ?>http">
										<div class="form-row mb-1">
											<label for="verbraucher<?php echo $deviceNum; ?>_urlw" class="col-md-4 col-form-label">URL Leistung</label>
											<div class="col">
												<input class="form-control" type="text" name="verbraucher<?php echo $deviceNum; ?>_urlw" id="verbraucher<?php echo $deviceNum; ?>_urlw" value="<?php echo htmlspecialchars(${"verbraucher" . $deviceNum . "_urlwold"}) ?>">
												<span class="form-text small">URL des Verbrauchers, welche die aktuelle Leistung in Watt zurück gibt.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="verbraucher<?php echo $deviceNum; ?>_urlh" class="col-md-4 col-form-label">URL Zählerstand</label>
											<div class="col">
												<input class="form-control" type="text" name="verbraucher<?php echo $deviceNum; ?>_urlh" id="verbraucher<?php echo $deviceNum; ?>_urlh" value="<?php echo htmlspecialchars(${"verbraucher" . $deviceNum . "_urlhold"}) ?>">
												<span class="form-text small">URL des Verbrauchers, welche den Zählerststand in Watt Stunden zurück gibt.</span>
											</div>
										</div>
									</div>
									<div id="v<?php echo $deviceNum; ?>modbus">
										<div class="form-row mb-1">
											<label for="verbraucher<?php echo $deviceNum; ?>_source" class="col-md-4 col-form-label">Source</label>
											<div class="col">
												<input class="form-control" type="text" name="verbraucher<?php echo $deviceNum; ?>_source" id="verbraucher<?php echo $deviceNum; ?>_source" value="<?php echo htmlspecialchars(${"verbraucher" . $deviceNum . "_sourceold"}) ?>">
												<span class="form-text small">Bei lokal angeschlossenem Zähler ist dies z. B. /dev/ttyUSB3. Wird ein Modbus Ethernet Konverter genutzt, z.B. der aus dem Shop, hier die IP Adresse eintragen.</span>
											</div>
										</div>
										<div class="form-row mb-1">
											<label for="verbraucher<?php echo $deviceNum; ?>_id" class="col-md-4 col-form-label">Source</label>
											<div class="col">
												<input class="form-control" type="number" min="1" step="1" name="verbraucher<?php echo $deviceNum; ?>_id" id="verbraucher<?php echo $deviceNum; ?>_id" value="<?php echo ${"verbraucher" . $deviceNum . "_idold"} ?>">
												<span class="form-text small">Modbus ID.</span>
											</div>
										</div>
									</div>
									<div id="v<?php echo $deviceNum; ?>tasmota">
										<div class="card-text alert alert-danger">
											Die Einstellungen für Tasmota und Shelly Geräte werden an dieser Stelle demnächst entfernt. Bitte benutzen Sie die Einstellungen unter "SmartHome 2.0", um solch ein Gerät einzubinden.
										</div>

										<div class="form-row mb-1">
											<label for="verbraucher<?php echo $deviceNum; ?>_ip" class="col-md-4 col-form-label">Source</label>
											<div class="col">
												<input class="form-control" type="text" name="verbraucher<?php echo $deviceNum; ?>_ip" id="verbraucher<?php echo $deviceNum; ?>_ip" value="<?php echo ${"verbraucher" . $deviceNum . "_ipold"} ?>">
												<span class="form-text small">IP Adresse des Geräts.</span>
											</div>
										</div>
									</div>
								</div>
							</div>
						<?php } ?>
					</div>
					<script>
						$(function() {
							<?php for ( $deviceNum = 1; $deviceNum < 4; $deviceNum++ ){ ?>
								if($('#verbraucher<?php echo $deviceNum; ?>_aktivOff').prop("checked")) {
									hideSection('#verbraucher<?php echo $deviceNum; ?>andiv');
								} else {
									showSection('#verbraucher<?php echo $deviceNum; ?>andiv');
								}

								$('input[type=radio][name=verbraucher<?php echo $deviceNum; ?>_aktiv]').change(function(){
									if(this.value == '0') {
										hideSection('#verbraucher<?php echo $deviceNum; ?>andiv');
									} else {
										showSection('#verbraucher<?php echo $deviceNum; ?>andiv');
									}
								});

								function display_verbraucher<?php echo $deviceNum; ?> () {
									hideSection('#v<?php echo $deviceNum; ?>http');
									hideSection('#v<?php echo $deviceNum; ?>modbus');
									hideSection('#v<?php echo $deviceNum; ?>tasmota');
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'http') {
										showSection('#v<?php echo $deviceNum; ?>http');
									}
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'mpm3pm') {
										showSection('#v<?php echo $deviceNum; ?>modbus');
									}
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'sdm630') {
										showSection('#v<?php echo $deviceNum; ?>modbus');
									}
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'sdm120') {
										showSection('#v<?php echo $deviceNum; ?>modbus');
									}
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'abb-b23') {
										showSection('#v<?php echo $deviceNum; ?>modbus');
									}
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'tasmota') {
										showSection('#v<?php echo $deviceNum; ?>tasmota');
									}
									if($('#verbraucher<?php echo $deviceNum; ?>_typ').val() == 'shelly') {
										showSection('#v<?php echo $deviceNum; ?>tasmota');
									}

								}

								display_verbraucher<?php echo $deviceNum; ?>();
								$('#verbraucher<?php echo $deviceNum; ?>_typ').change(function(){
									display_verbraucher<?php echo $deviceNum; ?>();
								});
							<?php } ?>
						});
					</script>
				</div>

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
				<small>Sie befinden sich hier: Einstellungen/Smart Home</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navSmartHome').addClass('disabled');
				}
			);

		</script>

	</body>
</html>
