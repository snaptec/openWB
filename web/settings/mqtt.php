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
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
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
			<?php
				$files = glob('/etc/mosquitto/conf.d/99-bridge-*.conf');
				$files = array_merge($files, glob('/etc/mosquitto/conf.d/99-bridge-*.conf.no'));
				$filesCount = count($files);
				// give the user the option to configure more than one bridge
				array_push($files, "");

				$loopCount = 0;
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
					$tryPrivate = false;
					$subscribeChargeMode = false;
					$exportGraph = false;
					$exportStatus = false;
					$tlsVersion = "tlsv1.2";
					$bridgeEnabled = preg_match('/.*\.conf$/', $currentFile) === 1;
					$subscribeConfigs = false;
					foreach($bridgeLines as $bridgeLine) {
						// echo "line '$bridgeLine'<br/>";
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

						if(preg_match('/^\s*try_private\s+true/', $bridgeLine) === 1) {
							$tryPrivate = true;
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
						if(preg_match('/^\s*topic\s+openWB\/config\/get\/#/', $bridgeLine) === 1) {
							$exportGraph = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/SmartHome\/#/', $bridgeLine) === 1) {
							$exportGraph = true;
						}
						if(preg_match('/^\s*topic\s+openWB\/set\//', $bridgeLine) === 1) {
							$subscribeConfigs = true;
						}
					}

					if ($loopCount != 0) echo "<hr>";
			?>
			<h1> <?php if($loopCount != $filesCount) echo "MQTT-Brücke \"$connectionName\""; else echo "Neue MQTT-Brücke"; ?></h1>
			<form action="./settings/savemqtt.php" method="POST">
				<!-- previous bridge name, needed for renaming a bridge -->
				<input type="hidden" name="bridge" value="<?php echo($connectionName); ?>">

				<!-- Konfiguration -->
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Konfiguration der MQTT-Brücke
					</div>
					<div class="card-body">
						<div class="card-text alert alert-danger">
						<u>ACHTUNG</u>: Die Konfiguration einer MQTT-Brücke erlaubt allen Nutzern mit Zugang zum entfernten MQTT-Server alle weitergeleiteten Daten dieser openWB einzusehen!<br/>
						Es wird dringend empfohlen, dies nur für nicht-öffentliche MQTT-Server unter Verwendung starker Transport-Verschlüsselung (TLS)  mit persönlichenm Login und
						strenger Zugriffskontrolle (zumindest für die MQTT-Thema unterhalb von "Entfernter Präfix") zu aktivieren!
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">MQTT-Brücke</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($bridgeEnabled == 0) echo " active" ?>">
											<input type="radio" name="bridgeEnabled" id="bridgeEnabledoldOff" value="0" <?php if($bridgeEnabled == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($bridgeEnabled == 1) echo " active" ?>">
											<input type="radio" name="bridgeEnabled" id="bridgeEnabledoldOn" value="1" <?php if($bridgeEnabled == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="ConnectionName" class="col-md-4 col-form-label">Name der Brücke</label>
							<div class="col">
								<input class="form-control" type="text" size="35" name="ConnectionName" id="ConnectionName" pattern="^[a-zA-Z0-9]+$" value="<?php echo $connectionName; ?>">
								<span class="form-text small">Der Name darf nur aus Buchstaben und Zahlen bestehen, keine Sonderzeichen oder Umlaute.</span>
								<?php if($debugold >= 1) echo "<small>Config-File befindet sich in Datei '$currentFile'</small>"; ?>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemoteAddress" class="col-md-4 col-form-label">Addresse und Portnummer des entfernten MQTT-Servers</label>
							<div class="col">
								<input class="form-control" type="text" size="50" name="RemoteAddress" id="RemoteAddress" pattern="^([a-zA-Z0-9][a-zA-Z0-9.-]+):([1-9][0-9]*)$" value="<?php echo $remoteAddressAndPort; ?>">
								<span class="form-text small">Entfernter MQTT-Server und Port-Nummer. Standard Port ist 8883 für eine TLS-geschützte Verbindung.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemoteUser" class="col-md-4 col-form-label">Benutzer</label>
							<div class="col">
								<input class="form-control" type="text" size="35" name="RemoteUser" id="RemoteUser" pattern="^([a-zA-Z0-9_\-+.]+)$" value="<?php echo $remoteUser; ?>">
								<span class="form-text small">Benutzername für den Login auf dem entfernten MQTT-Server.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemotePass" class="col-md-4 col-form-label">Passwort</label>
							<div class="col">
								<input class="form-control" type="password" size="35" name="RemotePass" id="RemotePass" pattern="^\S.\S+$" value="<?php echo $remotePassword; ?>">
								<span class="form-text small">Passwort für den Login auf dem entfernten MQTT-Server. Leerzeichen am Anfang und Ende des Passworts werden nicht unterstützt.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label for="RemotePrefix" class="col-md-4 col-form-label">Entfernter Präfix</label>
							<div class="col">
								<input class="form-control" type="text" size="55" name="RemotePrefix" id="RemotePrefix" pattern="^[a-zA-Z0-9_\-\/]+[/]$" value="<?php echo $remotePrefix; ?>">
								<span class="form-text small">MQTT-Thema Präfix, welches dem 'openWB/...' vorangestellt wird.<br/>
									Beispiel: Wenn in diesem Feld 'pfx/' eingetragen wird, werden alle Weiterleitungen und Registrierungen auf der entfernten Seite mit 'pfx/openWB/...' benannt.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label class="col-md-4 col-form-label">MQTT Protokoll</label>
							<div class="col">
								<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($mqttProtocol == "mqttv31") echo " active" ?>">
										<input type="radio" name="mqttProtocol" id="mqttProtocol31" value="mqttv31" <?php if($mqttProtocol == "mqttv31") echo " checked=\"checked\"" ?>>v3.1
									</label>
									<label class="btn btn-outline-info<?php if($mqttProtocol == "mqttv311") echo " active" ?>">
										<input type="radio" name="mqttProtocol" id="mqttProtocol311" value="mqttv311" <?php if($mqttProtocol == "mqttv311") echo " checked=\"checked\"" ?>>v3.1.1
									</label>
								</div>
								<span class="form-text small">Version des MQTT Protokolls, welches zur Kommunikation mit dem entfernten Server verwendet wird.</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label class="col-md-4 col-form-label">TLS Protokoll</label>
							<div class="col">
								<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($tlsVersion == "tlsv1.3") echo " active"; if(!$tlsv13Supported) echo " disabled"; ?>">
										<input type="radio" name="tlsProtocol" id="tlsProtocol13" value="tlsv1.3" <?php if($tlsVersion == "tlsv1.3") echo " checked=\"checked\""; if(!$tlsv13Supported) echo " disabled";  ?>>TLS v1.3
									</label>
									<label class="btn btn-outline-info<?php if($tlsVersion == "tlsv1.2") echo " active" ?>">
										<input type="radio" name="tlsProtocol" id="tlsProtocol12" value="tlsv1.2" <?php if($tlsVersion == "tlsv1.2") echo " checked=\"checked\"" ?>>TLS v1.2
									</label>
								</div>
								<span class="form-text small">
									Version des TLS Protokolls, welches zur Verschlüsselung der Kommunikation mit dem entfernten Server verwendet wird.
									TLSv 1.3 ist empfohlen, wird jedoch erst ab Debian Version "Buster" unterstützt.
								</span>
							</div>
						</div>
						<div class="form-row mb-1">
							<label class="col-md-4 col-form-label">Br&uuml;cke signalisieren</label>
							<div class="col">
								<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
									<label class="btn btn-outline-info<?php if($exportStatus == 0) echo " active" ?>">
										<input type="radio" name="tryPrivate" id="tryPrivateOff" value="0"<?php if(! $tryPrivate) echo " checked=\"checked\"" ?>>Aus
									</label>
									<label class="btn btn-outline-info<?php if($exportStatus == 1) echo " active" ?>">
										<input type="radio" name="tryPrivate" id="tryPrivateOn" value="1"<?php if($tryPrivate) echo " checked=\"checked\"" ?>>An
									</label>
								</div>
								<span class="form-text small">Aktiviert eine propriet&auml;re MQTT Protokoll-Erweiterung des Mosquitto Brokers, welche dem entfernten Broker signalisiert dass es sich um
								eine MQTT Br&uumlcke handelt. Ergibt bessere Leistung mit Mosquitto-Brokern, ist jedoch inkompatibel mit vielen anderen MQTT-Brokern. Daher bitte nur aktivieren, wenn der Ziel-Broker
								sicher ein Mosquitto-Broker ist.</span>
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
										<label class="btn btn-outline-info<?php if($exportStatus == 0) echo " active" ?>">
											<input type="radio" name="exportStatus" id="exportStatusoldOff" value="0"<?php if($exportStatus == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($exportStatus == 1) echo " active" ?>">
											<input type="radio" name="exportStatus" id="exportStatusoldOn" value="1"<?php if($exportStatus == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">Hausverbrauch, EVU, PV, Ladepunkte, Speicher</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Datenserien für Diagramme</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($exportGraph == 0) echo " active" ?>">
											<input type="radio" name="exportGraph" id="exportGrapholdOff" value="0"<?php if($exportGraph == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($exportGraph == 1) echo " active" ?>">
											<input type="radio" name="exportGraph" id="exportGrapholdOn" value="1"<?php if($exportGraph == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Fernkonfiguration -->
				<div class="card border-danger">
					<div class="card-header bg-danger">
						<div >Fernkonfiguration der openWB</div>
					</div>
					<div class="card-body">
						<div class="card-text alert alert-danger">
							<u>ACHTUNG</u>: Dies erlaubt jedem Nutzer des entfernten MQTT-Servers mit Zugriff auf die entsprechenden Themen, diese openWB fern zu steuern!<br/>
							Es wird dringend empfohlen, dies nur für nicht-öffentliche MQTT-Server unter Verwendung starker Transport-Verschlüsselung (TLS) mit
							persönlichem Login und strenger Zugriffskontrolle zu aktivieren!<br/>
							KEINESFALLS AUF <u>ÖFFENTLICH ZUGÄNGLICHEN</u> MQTT-SERVERN AKTIVEREN!!!
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Fernkonfiguration ermöglichen (gefährlich)</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($subscribeConfigs == 0) echo " active" ?>">
											<input type="radio" name="subscribeConfigs" id="subscribeConfigsoldOff" value="0" <?php if($subscribeConfigs == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($subscribeConfigs == 1) echo " active" ?>">
											<input type="radio" name="subscribeConfigs" id="subscribeConfigsoldOn" value="1" <?php if($subscribeConfigs == 1) echo " checked=\"checked\"" ?>>An
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
						<button type="submit" class="btn btn-success" name="action" value="saveBridge">Einstellungen für Brücke '<?php echo urlencode($connectionName); ?>' speichern</button>
					</div>
				</div>
				<div class="row justify-content-center py-1">
					<button type="submit" class="btn btn-danger" name="action" value="deleteBridge">Brücke '<?php echo urlencode($connectionName); ?>' löschen</button>
				</div>

			</form>
			<?php
					$loopCount++;
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
