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

			// read selected debug mode from config file
			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "debug=") !== false) {
					list(, $debugmode) = explode("=", $line);
				}
			}
			$debugmode = trim($debugmode);
			if ( $debugmode == "" ) {
				// if no debug mode set, set 0 = off
				$debugmode="0";
			}

		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col">
					<h1>Debug-Modus</h1>
				</div>
			</div>
			<form class="form" id="debugmodeForm" action="./tools/savedebug.php" method="POST">
				<div class="form-row">
					<div class="col-auto">
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="debugmodeRadioBtn" id="mode0RadioBtn" value="0" <?php if($debugmode == "0") echo checked?>>
								<label class="form-check-label" for="mode0RadioBtn">
								    Mode 0 (aus)
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="debugmodeRadioBtn" id="mode1RadioBtn" value="1" <?php if($debugmode == "1") echo checked?>>
								<label class="form-check-label" for="mode1RadioBtn">
									Mode 1 (Regelwerte)
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="debugmodeRadioBtn" id="mode2RadioBtn" value="2" <?php if($debugmode == "2") echo checked?>>
								<label class="form-check-label" for="mode2RadioBtn">
									Mode 2 (Berechnungsgrundlage)
								</label>
							</div>
						</div>
					</div>
					<div class="col-auto vaRow">
						<button type="submit" class="btn btn-green">Speichern</button>
					</div>
				</div>
			</form>

			<div class="row">
				<div class="col">
					<h1>Debug-Meldung</h1>
				</div>
			</div>
			<div class="row">
				<div class="col-lg-7">
					Das Sammeln der Systemparameter für die Debug-Meldung kann einige Zeit in Anspruch nehmen.
					<b>Es werden keine Benutzernamen oder Passwörter aus der Konfigurationsdatei übertragen!</b>
				</div>
			</div>
			<br>
			<form class="form" id="sendDebugMessageForm" action="./tools/senddebug.php" method="POST">
				<div class="form-row">
					<div class="form-group col-lg-7">
						<textarea class="form-control" id="debugMessage" name="debugMessage" rows="3" placeholder="Fehlerbeschreibung" maxlength="500"></textarea>
						<small id="textareaTextLength" class="form-text text-muted text-right">0/500</small>
					</div>
				</div>
				<div class="form-row form-row-inline">
					<div class="col-7 col-lg-5">
						<div class="input-group mb-2">
							<div class="input-group-prepend">
								<div class="input-group-text">@</div>
							</div>
							<input type="email" class="form-control" id="emailAddress" name="emailAddress" placeholder="Email-Adresse notwendig für Rückfragen" required>
						</div>
					</div>
					<div class="col-auto">
						<button type="submit" class="btn btn-green mb-2">Absenden</button>
					</div>
				</div>
			</form>
			<div class="row">
				<div class="col">
					<h1>Remote Support</h1>
				</div>
			</div>
			<div class="row">
				<div class="col-lg-7">
					Durch Angabe des Tokens und mit Klick auf "Tunnel herstellen" wird eine Verbindung von der lokalen openWB zum openWB Support hergestellt.
					openWB erhält damit Vollzugriff auf diese Installation. Diese Schnittstelle nur nach Aufforderung mit dem entsprechenden Token aktivieren.
				</div>
			</div>
			<form class="form" id="sendDebugMessageForm" action="./tools/starttunnel.php" method="POST">
				<div class="col-7 col-lg-5">
					<div class="input-group mb-2">
						<div class="input-group-prepend">
							<div class="input-group-text">Token</div>
							</div>
							<input type="text" class="form-control" id="token" name="token" placeholder="Token" required>
						</div>
					</div>
					<div class="col-auto">
						<button type="submit" class="btn btn-green mb-2">Tunnel herstellen</button>
					</div>
				</div>
			</form>
			


		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Debugging</small>
			</div>
		</footer>

		<script type="text/javascript">

			$.get("settings/navbar.php", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navDebugging').addClass('disabled');
			});

			$(document).ready(function(){

				$('textarea').on('change keyup paste', function() {
					var length = $(this).val().length;
					var length = 500-length;
					$('#textareaTextLength').text(length+"/500");
				});

			});

		</script>

	</body>
</html>
