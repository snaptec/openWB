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
			$refreshDuration = 8;
			foreach($lines as $line) {
				if(strpos($line, "debug=") !== false) {
					list(, $debugold) = explode("=", $line);
				}
			}

			$lines = file('/etc/os-release');
			$tlsv13Supported = empty(preg_grep('/VERSION_CODENAME=stretch/', $lines)) && empty(preg_grep('/VERSION_CODENAME=jessie/', $lines)) && empty(preg_grep('/VERSION_CODENAME=wheezy/', $lines));
		?>
		<div id="nav"></div> <!-- placeholder for navbar -->
		<div role="main" class="container" style="margin-top:20px">
			<h1>MQTT-Brücke</h1>
			<?php
				$files = glob('/etc/mosquitto/conf.d/99-bridge-*.conf*');
				if (count($files) == 0) {
					array_push($files, "");
				}

				$firstLoopDone = false;
				foreach($files as $currentFile)
				{
					$currentBridge = preg_replace('/^99-bridge-(.+)\.conf/', '${1}', $currentFile);

					$bridgeLines = $currentFile != "" ? file($currentFile) : array();
					$connectionName = "eindeutiger-verbindungs-bezeichner";
					$remoteAddressAndPort = "entfernter.mqtt.host:8883";
					$remotePrefix = NULL;
					$remoteUser = "nutzername-auf-dem-entfernten-host";
					$remotePassword = "";
					$remoteClientId = "client-id-fuer-den-entfernten-host";
					$mqttProtocol = "mqttv31";
					$exportGlobal = false;
					$exportEvu = false;
					$exportPv = false;
					$exportAllLps = false;
					$subscribeChargeMode = false;
					$exportGraph = false;
					$exportStatus = false;
					$tlsVersion = "tlsv1.2";
					$bridgeEnabled = preg_match('/.*\.conf$/', $currentFile) === 1;
					$subscribeConfigs = false;
					foreach($bridgeLines as $bridgeLine) {
						//echo "line '$bridgeLine'<br/>";
						if(is_null($remotePrefix) && preg_match('/^\s*topic\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+/', $bridgeLine, $matches) === 1) {
							// echo "Matches: " . var_dump($matches);
							$remotePrefix = trim($matches[5]);
						}
						else if(preg_match('/^\s*connection\s+(.+)/', $bridgeLine, $matches) === 1) {
							$connectionName = trim($matches[1]);
						}
						else if(preg_match('/^\s*address\s+(.+)/', $bridgeLine, $matches) === 1) {
							$remoteAddressAndPort = trim($matches[1]);
						}
						else if(preg_match('/^\s*remote_username\s+(.+)/', $bridgeLine, $matches) === 1) {
							$remoteUser = trim($matches[1]);
						}
						else if(preg_match('/^\s*remote_password\s+(.+)/', $bridgeLine, $matches) === 1) {
							$remotePassword = trim($matches[1]); //preg_replace('/./', '*', trim($matches[1]));
						}
						else if(preg_match('/^\s*bridge_protocol_version\s+(.+)/', $bridgeLine, $matches) === 1) {
							$mqttProtocol = trim($matches[1]);
						}
						else if(preg_match('/^\s*bridge_tls_version\s+(.+)/', $bridgeLine, $matches) === 1) {
							$tlsVersion = trim($matches[1]);
						}

						if(preg_match('/^\s*topic\s+openWB\/global\/#/', $bridgeLine) === 1) {
							$exportStatus = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/evu\/#/', $bridgeLine) === 1) {
							$exportStatus = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/pv\/#/', $bridgeLine) === 1) {
							$exportStatus = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/lp\/\d+\/#/', $bridgeLine) === 1) {
							$exportStatus = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/housebattery\/#/', $bridgeLine) === 1) {
							$exportStatus = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/graph\/#/', $bridgeLine) === 1) {
							$exportGraph = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/set\//', $bridgeLine) === 1) {
							$subscribeConfigs = true;
						}
					}

					if ($firstLoopDone) echo "<hr>";
			?>
			<form action="./tools/savemqtt.php?bridge=<?php echo urlencode($connectionName); ?>" method="POST">

				<!-- Konfiguration -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Konfiguration der MQTT-Br&uuml;cke
					</div>
					<div class="card-body">
						<div class="card-text alert alert-danger">
						<u>ACHTUNG</u>: Die Konfiguration einer MQTT-Br&uuml;cke erlaubt allen Nutzern mit Zugang zum entfernten MQTT-Server alle weitergeleiteten Daten dieser openWB einzusehen!<br/>
						Es wird dringend empfohlen, dies nur f&uuml;r nicht-&ouml;ffentliche MQTT-Server unter Verwendung starker Transport-Verschl&uuml;sselung (TLS)  mit personfiziertem Login und 
						strenger Zugriffskontrolle (zumindest f&uuml;r die MQTT-Thema unterhalb von &quot;Entfernter Pr&auml;fix&quot;) zu aktivieren!
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">MQTT-Br&uuml;cke</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($bridgeEnabledold == 0) echo " active" ?>">
											<input type="radio" name="bridgeEnabled" id="bridgeEnabledoldOff" value="0" <?php if($bridgeEnabledold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($bridgeEnabledold == 1) echo " active" ?>">
											<input type="radio" name="bridgeEnabled" id="bridgeEnabledoldOn" value="1" <?php if($bridgeEnabledold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="ConnectionName" class="col-md-4 col-form-label">Name der Br&uuml;cke</label>
							<div class="col">
								<input class="form-control" type="text" size="35" name="ConnectionName" id="ConnectionName" value="<?php echo $connectionName; ?>"><br/>
								<?php if($debugold >= 1) echo "<small>in Datei '$currentFile'</small>"; ?>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemoteAddress" class="col-md-4 col-form-label">Addresse und Portnummer des entfernten MQTT-Servers</label>
							<div class="col">
								<input class="form-control" type="text" size="50" name="RemoteAddress" id="RemoteAddress" value="<?php echo $remoteAddressAndPort; ?>">
								<span class="form-text small">Entfernter MQTT-Server und Port-Nummer. Standard Port ist 8883 f&uuml;r eine TLS-gesch&uuml;tzte Verbindung.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemoteUser" class="col-md-4 col-form-label">Benutzer</label>
							<div class="col">
								<input class="form-control" type="text" size="35" name="RemoteUser" id="RemoteUser" value="<?php echo $remoteUser; ?>">
								<span class="form-text small">Benutzername f&uuml;r den Login auf dem entfernten MQTT-Server.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemotePass" class="col-md-4 col-form-label">Passwort</label>
							<div class="col">
								<input class="form-control" ype="password" size="35" name="RemotePass" id="RemotePass" value="<?php echo $remotePassword; ?>">
								<span class="form-text small">Passwort f&uuml;r den Login auf dem entfernten MQTT-Server. Leerzeichen am Anfang und Ende des Passworts werden nicht unterst&uuml;tzt.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemotePrefix" class="col-md-4 col-form-label">Entfernter Pr&auml;fix</label>
							<div class="col">
								<input class="form-control" ype="text" size="55" name="RemotePrefix" id="RemotePrefix" value="<?php echo $remotePrefix; ?>">
								<span class="form-text small">MQTT-Thema Pr&auml;fix, welches dem 'openWB/...' vorangestellt wird.<br/>
									Beispiel: Wenn in diesem Feld 'pfx/' eingetragen wird, werden alle Weiterleitungen und Registrierungen auf der entfernten Seite mit 'pfx/openWB/...' benannt.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="mqttProtocol" class="col-md-4 col-form-label">MQTT Protokoll</label>
							<div class="col">
								<fieldset>
									<table>
										<tr>
											<td style="text-align: left; vertical-align: center; padding: 10px;">
												<input type="radio" name="mqttProtocol" value="mqttv31" <?php echo $mqttProtocol == "mqttv31" ? "checked=\"checked\"" : "" ?>>&nbsp;v3.1
											</td>
											<td style="text-align: left; vertical-align: center; padding: 10px;">
												<input type="radio" name="mqttProtocol" value="mqttv311" <?php echo $mqttProtocol == "mqttv311" ? "checked=\"checked\"" : "" ?>>&nbsp;v3.1.1
											</td>
										</tr>
									</table>
								</fieldset>
								<span class="form-text small">Version des MQTT Protokolls, welches zur Kommunikation mit dem entfernten Server verwendet wird.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="tlsProtocol" class="col-md-4 col-form-label">TLS Protokoll</label>
							<div class="col">
								<fieldset>
									<table>
										<tr>
											<td style="text-align: left; vertical-align: center; padding: 10px;">
												<input type="radio" name="tlsProtocol" value="tlsv1.3" <?php if (!$tlsv13Supported) echo "disabled"; ?> 
												<?php echo $tlsVersion == "tlsv1.3" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.3
												<span style="color: green; font-size:small;"><?php echo $tlsv13Supported ? "Bevorzugt" : "<br/>Auf Debian Versionen kleiner<br/>'Buster' nicht unterst&uuml;tzt"; ?></span>
											</td>
											<td style="text-align: left; vertical-align: center; padding: 10px;">
												<input type="radio" name="tlsProtocol" value="tlsv1.2" <?php echo $tlsVersion == "tlsv1.2" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.2
												<span style="color: green; font-size:small;"><?php if (!$tlsv13Supported) echo "<br/>Empfohlen"; ?></span><
											</td>
											<!-- td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.1" <?php echo $tlsVersion == "tlsv1.1" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.1<br/><span style="color: darkred; font-size:small;">Can be broken.</span><td/ -->
										</tr>
									</table>
								</fieldset>
								<span class="form-text small">Version des TLS Protokolls, welches zur Verschl&uuml;sselung der Kommunikation mit dem entfernten Server verwendet wird.</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Datenauswahl -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Daten
					</div>
					<div class="card-body">
						<div class="card-text alert alert-info">
							Diese Daten werden von der openWB zum entfernten Server weitergeleitet.
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Alle Status Daten</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($exportStatusold == 0) echo " active" ?>">
											<input type="radio" name="exportStatus" id="exportStatusoldOff" value="0"<?php if($exportStatusold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($exportStatusold == 1) echo " active" ?>">
											<input type="radio" name="exportStatus" id="exportStatusoldOn" value="1"<?php if($exportStatusold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">Hausverbrauch, EVU, PV, Ladepunkte, Speicher</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Datenserien f&uuml;r Diagramme</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($exportGraphold == 0) echo " active" ?>">
											<input type="radio" name="exportGraph" id="exportGrapholdOff" value="0"<?php if($exportGraphold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($exportGraphold == 1) echo " active" ?>">
											<input type="radio" name="exportGraph" id="exportGrapholdOn" value="1"<?php if($exportGraphold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Fernkonfiguration -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						<div >Fernkonfiguration der openWB</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-danger">
							<u>ACHTUNG</u>: Dies erlaubt jedem Nutzer des entfernten MQTT-Servers mit Zugriff auf die entsprechenden Themen, diese openWB fern zu steuern!<br/>
							Es wird schwer empfohlen, dies nur f&uuml;r nicht-&ouml;ffentliche MQTT-Server unter Verwendung starker Transport-Verschl&uuml;sselung (TLS) mit 
							personfiziertem Login und strenger Zugriffskontrolle zu aktivieren!<br/>
							KEINESFALLS AUF <u>&Ouml;FFENTLICH ZUG&Auml;NGLICHEN</u> MQTT-SERVERN AKTIVEREN!!!
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Fernkonfiguration erm&ouml;glichen (gef&auml;hrlich)</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($subscribeConfigsold == 0) echo " active" ?>">
											<input type="radio" name="subscribeConfigs" id="subscribeConfigsoldOff" value="0" <?php if($subscribeConfigsold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($subscribeConfigsold == 1) echo " active" ?>">
											<input type="radio" name="subscribeConfigs" id="subscribeConfigsoldOn" value="1" <?php if($subscribeConfigsold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="row justify-content-center py-1">
					<div class="col text-center">
						Das Anwenden der Änderungen dauert <?php echo $refreshDuration ?> Sekunden. Bitte die openWB in dieser Zeit nicht vom Strom trennen!<br><br>
						<button type="submit" class="btn btn-green" name="action" value="saveBridge">Einstellungen f&uuml;r Br&uuml;cke '<?php echo urlencode($connectionName); ?>' speichern</button>
					</div>
				</div>
				<div class="row justify-content-center py-1">
					<button type="submit" class="btn btn-green" name="action" value="deleteBridge">Br&uuml;cke '<?php echo urlencode($connectionName); ?>' l&ouml;schen</button>
				</div>

			</form>
			<?php
					$firstLoopDone = true;
				}
			?>

			<div class="row justify-content-center">
				<div class="col text-center">
					Open Source made with love!<br>
					Jede Spende hilft, die Weiterentwicklung von openWB voranzutreiben<br>
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
				<small>Sie befinden sich hier: Einstellungen/MQTT-Brücke</small>
		</div>
	</footer>

	<script>

		$.get(
			{ url: "settings/navbar.html", cache: false },
			function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navMqttBruecke').addClass('disabled');
			}
		);

	</script>

	</body>
</html>
