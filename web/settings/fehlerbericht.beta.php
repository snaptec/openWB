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
			}
			$debugmode = trim($debugmode);
			if ( $debugmode == "" ) {
				// if no debug mode set, set 0 = off
				$debugmode="0";
			}

		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Fehlermeldungen</h1>

			<div class="card border-secondary">
				<form class="form" id="sendDebugMessageForm" action="./tools/senddebug.php" method="POST">
					<div class="card-header bg-secondary">
						Debug-Meldung
					</div>
					<div class="card-body">
						<div class="form-group">
							<span id="textareaHelpBlock" class="form-text">Das Sammeln der Systemparameter für die Debug-Meldung kann einige Zeit in Anspruch nehmen. Es werden keine Benutzernamen oder Passwörter aus der Konfigurationsdatei übertragen! Der Debug Modus muss nicht verstellt werden.</span>
							<textarea class="form-control" id="debugMessage" name="debugMessage" rows="3" placeholder="Fehlerbeschreibung" maxlength="500" required="required"></textarea>
							<small id="textareaTextLength" class="form-text text-muted text-right">500/500</small>
						</div>
						<div class="form-group mb-0">
							<div class="input-group">
								<div class="input-group-prepend">
									<div class="input-group-text">
										<i class="fa fa-envelope"></i>
									</div>
								</div>
								<input type="email" class="form-control" id="emailAddress" name="emailAddress" placeholder="Email-Adresse notwendig für Rückfragen" required="required">
							</div>
						</div>
					</div>
					<div class="card-footer text-center">
						<button type="submit" class="btn btn-success" disabled="disabled">Absenden</button>
					</div>
				</form>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Fehlerbericht</small>
			</div>
		</footer>

		<script>

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navFehlerberichtBeta').addClass('disabled');
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
