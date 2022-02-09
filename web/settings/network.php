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
		<link rel="stylesheet" type="text/css" href="fonts/font-awesome-5.8.2/css/all.css">
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
			// load openwb.conf
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Netzwerk-Einstellungen</h1>
			<?php
			$currentHostname = gethostname();
			if(array_key_exists( 'action', $_POST )){ // We need to do something...
				switch( $_POST['action'] ){
					case 'rename':
						// change hostname
						$cmd = "sudo /var/www/html/openWB/runs/sethostname.sh " . escapeshellarg( $_POST['hostname'] );
						exec( $cmd, $output, $returnval );
						?>
						<div class="col alert alert-success" role="alert">
							Der Hostname wurde geändert auf '<?php echo $_POST['hostname']; ?>'.<br>
							Die openWB wird jetzt neu gestartet.
						</div>
						<script>
							window.setTimeout(() => {
								$("#rebootConfirmationModal").modal("show");
							}, 3000);
						</script>
						<?php
						break;
					case 'wlanreset':
						// reset wlan credentials
						$result1 = file_put_contents($_SERVER['DOCUMENT_ROOT'] . '/tmp/wssid', '');
						$result2 = file_put_contents($_SERVER['DOCUMENT_ROOT'] . '/tmp/wpassword', '');
						$cmd = 'nohup sudo /bin/bash /var/www/html/wlanconnect.sh > /dev/null 2>&1 &';
						exec($cmd, $output, $returnval);
						if( $result1 === false || $result2 === false || $returnval !== 0 ){
							?>
							<div class="col alert alert-danger" role="alert">
								Die Zugangsdaten konnten nicht entfernt werden!<br>
								Diese Funktion setzt eine fertig gekaufte openWB voraus. Bei Eigeninstallationen ändern Sie bitte die Zugangsdaten mit den normalen Funktionen des Raspberry Pi OS.
							</div>
							<?php
							break;
						}
						?>
						<div class="col alert alert-success" role="alert">
							Die Zugangsdaten wurden entfernt.<br>
							Die openWB wird jetzt neu gestartet.
						</div>
						<script>
							$.get({ url: "settings/restart.php", cache: false });
						</script>
						<?php
						break;
					case 'virtip':
						// change virtual IPs
						$cmd = "sudo /var/www/html/openWB/runs/setvirtips.sh " . escapeshellarg( $_POST['virtual_ip_eth0'] ) . " " . escapeshellarg( $_POST['virtual_ip_wlan0'] );
						exec( $cmd, $output, $returnval );
						?>
						<div class="col alert alert-success" role="alert">
							Das virtuelles Netzwerk wurde angepasst.<br>
							eth0: <?php echo $_POST['virtual_ip_eth0']; ?><br>
							wlan0: <?php echo $_POST['virtual_ip_wlan0']; ?><br>
							Die openWB wird jetzt neu gestartet.
						</div>
						<script>
							window.setTimeout(() => {
								$("#rebootConfirmationModal").modal("show");
							}, 3000);
						</script>
						<?php
						break;
				}
			} else { // nothing to do yet, show input field ?>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Hostname ändern
					</div>
					<form action="./settings/network.php" method="POST">
						<div class="card-body">
							<div class="row form-group">
								<label for="hostname" class="col-md-4 col-form-label">Neuer Hostname</label>
								<div class="col">
									<input type="text" name="hostname" id="hostname" value="<?php echo $currentHostname; ?>" placeholder="Name" aria-describedby="hostnameHelpBlock" class="form-control" required="required" pattern="[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9]">
									<span id="hostnameHelpBlock" class="form-text small">
										Der Hostname darf nur Buchstaben, Zahlen und einen Bindestrich enthalten. Keine Umlaute, Sonderzeichen oder Leerzeichen. Das erste und letzte Zeichen darf kein Bindestrich sein.<br>
										<span class="text-danger">Die openWB wird direkt nach der Änderung neu gestartet! Alle Fahrzeuge sind vorher abzustecken!</span>
									</span>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" name="action" value="rename" class="btn btn-success">Hostnamen ändern</button>
						</div>
					</form>
				</div> <!-- card end -->

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						WLAN
					</div>
					<form action="./settings/network.php" method="POST">
						<div class="card-body">
							<div class="row form-group">
								<label for="wlanreset" class="col-md-4 col-form-label">Anmeldedaten löschen</label>
								<div class="col">
									<button type="submit" name="action" value="wlanreset" class="btn btn-block btn-danger">Anmeldedaten löschen</button>
									<span id="wlanresetHelpBlock" class="form-text small">
										Hiermit können die aktuellen WLAN Zugangsdaten (SSID und Kennwort) entfernt werden. Nach dem Neustart öffnet die openWB einen Hotspot, falls kein Netzwerkkabel eingesteckt ist.<br>
										<span class="text-danger">
											Die openWB wird direkt nach der Änderung neu gestartet! Alle Fahrzeuge sind vorher abzustecken!<br>
											Diese Funktion setzt eine fertig gekaufte openWB voraus. Bei Eigeninstallationen ändern Sie bitte die Zugangsdaten mit den normalen Funktionen des Raspberry Pi OS.
										</span>
									</span>
								</div>
							</div>
						</div>
					</form>
				</div> <!-- card end -->

				<div class="card border-danger">
					<div class="card-header bg-danger">
						openWB Plug'n'Play Netzwerk
					</div>
					<form action="./settings/network.php" method="POST">
						<div class="card-body">
							<div class="row form-group">
								<label for="" class="col-md-4 col-form-label">eth0</label>
								<div class="col">
									<input type="text" name="virtual_ip_eth0" id="virtual_ip_eth0" value="<?php echo $virtual_ip_eth0old; ?>" aria-describedby="virtualIpEth0HelpBlock" class="form-control" required="required" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
									<span id="virtualIpEth0HelpBlock" class="form-text small">
										Hier kann die IP des virtuellen Netzwerkadapters angepasst werden.<br>
										<span class="text-danger">
											Achtung!<br>
											Wenn hier ungültige Daten eingetragen werden, funktioniert die Verbindung zu einem openWB EVU-/PV-/Speicher-/AlphaESS-Kit nicht mehr! Ein externes Display kann ebenfalls keine Verbindung mehr aufbauen!<br>
											Die Standardeinstellung ist <span class="text-primary">192.168.193.5</span> und sollte nur in Ausnahmefällen geändert werden!<br>
											Die openWB wird direkt nach der Änderung neu gestartet! Alle Fahrzeuge sind vorher abzustecken!
										</span>
									</span>
								</div>
							</div>
							<div class="row form-group">
								<label for="" class="col-md-4 col-form-label">wlan0</label>
								<div class="col">
									<input type="text" name="virtual_ip_wlan0" id="virtual_ip_wlan0" value="<?php echo $virtual_ip_wlan0old; ?>" aria-describedby="virtualIpWlan0HelpBlock" class="form-control" required="required" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
									<span id="virtualIpWlan0HelpBlock" class="form-text small">
										Hier kann die IP des virtuellen Netzwerkadapters angepasst werden.<br>
										<span class="text-danger">
											Achtung!<br>
											Wenn hier ungültige Daten eingetragen werden, funktioniert die Verbindung zu einem openWB EVU-/PV-/Speicher-/AlphaESS-Kit nicht mehr! Ein externes Display kann ebenfalls keine Verbindung mehr aufbauen!<br>
											Die Standardeinstellung ist <span class="text-primary">192.168.193.6</span> und sollte nur in Ausnahmefällen geändert werden!<br>
											Die openWB wird direkt nach der Änderung neu gestartet! Alle Fahrzeuge sind vorher abzustecken!
										</span>
									</span>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" name="action" value="virtip" class="btn btn-danger">Plug'n'Play Netzwerk ändern</button>
						</div>
					</form>
				</div> <!-- card end -->

			<?php } ?>
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
				<small>Sie befinden sich hier: Einstellungen/Netzwerk-Einstellungen</small>
			</div>
		</footer>

		<script>
			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navNetworkSettings').addClass('disabled');
				}
			);
		</script>

	</body>
</html>
