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

			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {

				if(strpos($line, "clouduser=") !== false) {
					list(, $clouduserold) = explode("=", $line, 2);
				}
				if(strpos($line, "cloudpw=") !== false) {
					list(, $cloudpwold) = explode("=", $line, 2);
				}
				if(strpos($line, "datenschutzack=") !== false) {
					list(, $datenschutzackold) = explode("=", $line, 2);
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
					if(isset($remotePrefix) && preg_match('/^\s*topic\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+/', $bridgeLine, $matches) === 1) {
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
			<h1>Einstellungen zur openWB Cloud</h1>
			<?php if ( $datenschutzackold != 1 ) { ?>
				<div class="alert alert-danger">
					Sie müssen der <a href="settings/datenschutz.html">Datenschutzerklärung</a> zustimmen, um die Cloudanbindung nutzen zu können.
				</div>
			<?php } else { ?>
				<div class="alert alert-success">
					Sie haben der <a href="settings/datenschutz.html">Datenschutzerklärung</a> zugestimmt und können die Cloudanbindung nutzen.
				</div>
			<?php }
			if (( $connectionName == "cloud") && ( $bridgeEnabled == "1")) { ?>
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Cloud Anmeldedaten
					</div>
					<div class="card-body">
						<div class="form-row mb-1">
							<div class="col">
								Cloud ist aktiv<br>
								Benutzername: <?php echo $clouduserold; ?><br>
								Passwort: <?php echo $cloudpwold; ?>
							</div>
						</div>
						<div class="form-row mb-1">
							<div class="col">
								Mit den Zugangsdaten auf web.openwb.de anmelden
							</div>
						</div>
					</div>
					<div class="card-footer">
						<form action="./settings/savemqtt.php?bridge=<?php echo urlencode($connectionName); ?>" method="POST">
							<input type="hidden" name="ConnectionName" value="cloud"/>
							<div class="row justify-content-center py-1">
								<button type="submit" class="btn btn-success" name="action" value="deleteBridge">Brücke <?php echo urlencode($connectionName); ?> löschen</button>
							</div>
						</form>
					</div>
				</div> <!-- card -->
			<?php } else { ?>
				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Cloud Anmeldedaten
					</div>
					<form action="./settings/cloudregistrate.php" method="POST">
						<div class="card-body">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="connect_username" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-user"></i>
												</div>
											</div>
											<input type="text" name="username" id="connect_username" value="" aria-describedby="usernameHelpBlock" class="form-control" required="required" pattern="[A-Za-z]+">
										</div>
										<span id="usernameHelpBlock" class="form-text small">Der Benutzername darf nur Buchstaben enthalten. Keine Umlaute, Zahlen, Sonderzeichen oder Leerzeichen.</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="cloudpass" class="col-md-4 col-form-label">Passwort</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-lock"></i>
												</div>
											</div> 
											<input type="password" name="cloudpass" id="cloudpass" value="" class="form-control" required="required">
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" class="btn btn-success"<?php if( $datenschutzackold != 1 ) echo ' disabled="disabled"'; ?>>Mit Account anmelden</button>
						</div>
					</form>
				</div> <!-- card 1 -->
				<div class="card border-secondary">
					<form action="./settings/cloudregistrate.php" method="POST">
						<div class="card-header bg-secondary">
							Cloud neu einrichten
						</div>
						<div class="card-body">
							<div class="form-group">
								<div class="form-row mb-1">
									<label for="register_username" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-user"></i>
												</div>
											</div>
											<input type="text" name="username" id="register_username" value="" aria-describedby="registerUsernameHelpBlock" class="form-control" required="required" pattern="[A-Za-z]+">
										</div>
										<span id="registerUsernameHelpBlock" class="form-text small">Der Benutzername darf nur Buchstaben enthalten. Keine Umlaute, Zahlen, Sonderzeichen oder Leerzeichen</span>
									</div>
								</div>
								<div class="form-row mb-1">
									<label for="email" class="col-md-4 col-form-label">Email Adresse</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-envelope"></i>
												</div>
											</div>
											<input type="email" name="email" id="email" value="" class="form-control" required="required">
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" class="btn btn-success"<?php if( $datenschutzackold != 1 ) echo ' disabled="disabled"'; ?>>Neuen Account erstellen und einrichten</button>
						</div>
					</form>
				</div> <!-- card 2 -->
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
				<small>Sie befinden sich hier: Einstellungen/openWB Cloud</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navOpenwbCloud').addClass('disabled');
				}
			);

		</script>


	</body>
</html>
