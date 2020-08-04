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
		<!-- <link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css"> -->
		<!-- include settings-style -->
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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
			<div class="card">
				<div class="card-header bg-secondary text-white font-weight-bold">
					Cloud Anmeldedaten
				</div>
				<?php if (( $connectionName == "cloud") && ( $bridgeEnabled == "1")) { ?>
					<div class="card-body">
						<div class="row">
							Cloud ist aktiv<br>
							Benutzername: <?php echo $clouduserold; ?><br>
							Passwort: <?php echo $cloudpwold; ?>
						</div>
						<div class="row">
							Mit den Zugangsdaten auf web.openwb.de anmelden
						</div>
					</div>
					<div class="card-footer">
						<form action="./tools/savemqtt.php?bridge=<?php echo urlencode($connectionName); ?>" method="POST">
							<input type="hidden" name="ConnectionName" value="cloud"/>
							<div class="row justify-content-center py-1">
								<button type="submit" class="btn btn-green" name="action" value="deleteBridge">Brücke <?php echo urlencode($connectionName); ?> löschen</button>
							</div>
						</form>
					</div>
				<?php } else { ?>
					<form action="./tools/cloudregistrate.php" method="POST">
						<div class="card-body">
							<div class="row form-group">
								<label for="connect_username" class="col-4 col-form-label">Benutzername</label>
								<div class="col-8">
									<div class="input-group">
										<div class="input-group-prepend">
											<div class="input-group-text">
												<i class="fa fa-user"></i>
											</div>
										</div>
										<input type="text" name="username" id="connect_username" value="" aria-describedby="usernameHelpBlock" class="form-control" required="required">
									</div>
									<span id="usernameHelpBlock" class="form-text">Der Benutzername darf nur Buchstaben und Zahlen enthalten. Keine Umlaute, Sonderzeichen oder Leerzeilen.</span>
								</div>
							</div>
							<div class="row form-group mb-0">
								<label for="cloudpass" class="col-4 col-form-label">Passwort</label>
								<div class="col-8">
									<div class="input-group">
										<div class="input-group-prepend">
											<div class="input-group-text">
												<i class="fa fa-lock"></i>
											</div>
										</div> 
										<input type="text" name="cloudpass" id="cloudpass" value="" class="form-control" aria-describedby="passwordHelpBlock" required="required">
									</div>
									<span id="passwordHelpBlock" class="form-text">Passwort des Cloud Accounts.</span>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" class="btn btn-green">Mit Account anmelden</button>
						</div>
					</form>
				</div> <!-- card 1 -->
				<div class="card">
					<form action="./tools/cloudregistrate.php" method="POST">
						<div class="card-header bg-secondary text-white font-weight-bold">
							Cloud neu einrichten
						</div>
						<div class="card-body">
							<div class="row form-group">
								<label for="register_username" class="col-4 col-form-label">Benutzername</label>
								<div class="col-8">
									<div class="input-group">
										<div class="input-group-prepend">
											<div class="input-group-text">
												<i class="fa fa-user"></i>
											</div>
										</div>
										<input type="text" name="username" id="register_username" value="" aria-describedby="registerUsernameHelpBlock" class="form-control" required="required">
									</div>
									<span id="registerUsernameHelpBlock" class="form-text">Der Benutzername darf nur Buchstaben enthalten. Keine Umlaute, Sonderzeichen oder Leerzeilen</span>
								</div>
							</div>
							<div class="row form-group mb-0">
								<label for="email" class="col-4 col-form-label">Email Adresse</label>
								<div class="col-8">
									<div class="input-group">
										<div class="input-group-prepend">
											<div class="input-group-text">
												<i class="fa fa-envelope"></i>
											</div>
										</div>
										<input type="text" name="email" id="email" value="" aria-describedby="registerPasswordHelpBlock" class="form-control" required="required">
									</div>
									<span id="registerPasswordHelpBlock" class="form-text">Email Adresse angeben</span>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" class="btn btn-green">Neuen Account erstellen und einrichten</button>
						</div>
					</form>
				<?php } ?>
			</div> <!-- card 1 or 2 -->
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
				<small>Sie befinden sich hier: Einstellungen/openWB Cloud</small>
			</div>
		</footer>

		<script>

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navOpenwbCloud').addClass('disabled');
			});

		</script>


	</body>
</html>
