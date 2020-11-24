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

			// read selected debug mode from config file
			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "debug=") !== false) {
					list(, $debugmode) = explode("=", $line);
				}
				if(strpos($line, "datenschutzack=") !== false) {
					list(, $datenschutzackold) = explode("=", $line, 2);
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
			<h1>Debugging und Support</h1>

			<div class="card border-secondary">
				<form class="form" id="debugmodeForm" action="./tools/savedebug.php" method="POST">
					<div class="card-header bg-secondary">
						Debug-Modus
					</div>
					<div class="card-body">
						<div class="form-group mb-0">
							<div class="custom-control custom-radio">
								<input class="custom-control-input" type="radio" name="debugmodeRadioBtn" id="mode0RadioBtn" value="0"<?php if($debugmode == "0") echo " checked"?>>
								<label class="custom-control-label" for="mode0RadioBtn">
									Mode 0 (aus)
								</label>
							</div>
							<div class="custom-control custom-radio">
								<input class="custom-control-input" type="radio" name="debugmodeRadioBtn" id="mode1RadioBtn" value="1"<?php if($debugmode == "1") echo " checked"?>>
								<label class="custom-control-label" for="mode1RadioBtn">
									Mode 1 (Regelwerte)
								</label>
							</div>
							<div class="custom-control custom-radio">
								<input class="custom-control-input" type="radio" name="debugmodeRadioBtn" id="mode2RadioBtn" value="2"<?php if($debugmode == "2") echo " checked"?>>
								<label class="custom-control-label" for="mode2RadioBtn">
									Mode 2 (Berechnungsgrundlage)
								</label>
							</div>
						</div>
					</div>
					<div class="card-footer text-center">
						<button type="submit" class="btn btn-success">Speichern</button>
					</div>
				</form>
			</div>

			<div class="card border-secondary">
				<form class="form" id="sendTokenForm" action="./tools/starttunnel.php" method="POST">
					<div class="card-header bg-secondary">
						Remote Support
					</div>
					<div class="card-body">
						<?php if ( $datenschutzackold != 1 ) { ?>
						<div class="alert alert-danger">
							Sie müssen der <a href="tools/datenschutz.html">Datenschutzerklärung</a> zustimmen, um den Online-Support nutzen zu können.
						</div>
						<?php } else { ?>
						<div class="alert alert-success">
							Sie haben der <a href="tools/datenschutz.html">Datenschutzerklärung</a> zugestimmt und können den Online-Support nutzen.
						</div>
						<?php } ?>
						<div class="form-group mb-0">
							<span id="textHelpBlock" class="form-text">Durch Angabe des Tokens und mit Klick auf "Tunnel herstellen" wird eine Verbindung von der lokalen openWB zum openWB Support hergestellt. openWB erhält damit Vollzugriff auf diese Installation. Diese Schnittstelle nur nach Aufforderung mit dem entsprechenden Token aktivieren.</span>
							<div class="input-group">
								<div class="input-group-prepend">
									<div class="input-group-text">
										<i class="fa fa-key"></i>
									</div>
								</div>
								<input type="text" class="form-control" id="token" name="token" placeholder="Token" aria-describedby="textHelpBlock" required="required">
							</div>
						</div>
					</div>
					<div class="card-footer text-center">
						<button type="submit" class="btn btn-success"<?php if( $datenschutzackold != 1 ) echo ' disabled="disabled"'; ?>>Tunnel herstellen</button>
					</div>
				</form>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Debugging</small>
			</div>
		</footer>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navDebugging').addClass('disabled');
				}
			);

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
