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

				if(strpos($line, "clouduser=") !== false) {
					list(, $clouduserold) = explode("=", $line, 2);
				}
				if(strpos($line, "cloudpw=") !== false) {
					list(, $cloudpwold) = explode("=", $line, 2);
				}
			}
			$files = glob('/etc/mosquitto/conf.d/99-bridge-*.conf*');
			if (count($files) == 0) {
				array_push($files, "");
			}

			$firstLoopDone = false;
			foreach($files as $currentFile) {
				$currentBridge = preg_replace('/^99-bridge-(.+)\.conf/', '${1}', $currentFile);
				$bridgeEnabled = preg_match('/.*\.conf$/', $currentFile) === 1;
				$bridgeLines = $currentFile != "" ? file($currentFile) : array();
				$connectionName = "eindeutiger-verbindungs-bezeichner";
				foreach($bridgeLines as $bridgeLine) {
					if(is_null($remotePrefix) && preg_match('/^\s*topic\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+/', $bridgeLine, $matches) === 1) {
						// echo "Matches: " . var_dump($matches);
						$remotePrefix = trim($matches[5]);
					} else if(preg_match('/^\s*connection\s+(.+)/', $bridgeLine, $matches) === 1) {
						$connectionName = trim($matches[1]);
					}
				}
			}

		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="col-sm-12">
				<div class="row">
					<h3>Cloud Einstellungen</h3>
				</div>
				<?php if (( $connectionName == "cloud") && ( $bridgeEnabled == "1")) {
				echo '
					<div class="row">
						Cloud ist aktiv<br>
						Benutzername: '.$clouduserold.'<br>
						Passwort: '.$cloudpwold.'<br>
					</div>
					<div class="row">
						Mit den Zugangsdaten auf web.openwb.de anmelden
					</div>
					<form action="./tools/savemqtt.php?bridge='.urlencode($connectionName).'" method="POST">
						<input type="hidden" name="ConnectionName" value="cloud"/>
                                        	<div class="row justify-content-center py-1">
                                        	        <button type="submit" class="btn btn-green" name="action" value="deleteBridge">Br&uuml;cke '.urlencode($connectionName).' l&ouml;schen</button>
						</div>
					</form>
				'; } else { echo '
					<form action="./tools/cloudregistrate.php" method="POST">
						<div class="row">
							<b><label for="connect_username">Benutzername:</label></b>
							<input type="text" name="username" id="connect_username" value="">
						</div>
						<div class="row">
							Der Benutzername darf nur Buchstaben und Zahlen enthalten. Keine Umlaute, Sonderzeichen oder Leerzeilen
						</div>
						<div class="row">
							<b><label for="cloudpass">Passwort:</label></b>
							<input type="text" name="cloudpass" id="cloudpass" value="">
						</div>
						<div class="row">
							Passwort des Cloud Accounts
						</div>

						<button type="submit" class="btn btn-green">Mit Account anmelden</button>
					</form>
					<hr>
					<form action="./tools/cloudregistrate.php" method="POST">
						<div class="row">
							<b><label for="register_username">Benutzername:</label></b>
							<input type="text" name="username" id="register_username" value="">
						</div>
						<div class="row">
							Der Benutzername darf nur Buchstaben und Zahlen enthalten. Keine Umlaute, Sonderzeichen oder Leerzeilen
						</div>
						<div class="row">
							<b><label for="email">Email Adresse:</label></b>
							<input type="text" name="email" id="email" value="">
						</div>
						<div class="row">
							Email Adresse angeben
						</div>

						<button type="submit" class="btn btn-green">Neuen Account erstellen und einrichten</button>
					</form>
				'; } ?>
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
				<small>Sie befinden sich hier: Einstellungen/openWB Cloud</small>
			</div>
		</footer>

		<script type="text/javascript">

			$.get("settings/navbar.php", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navOpenwbCloud').addClass('disabled');
			});

		</script>


	</body>
</html>
