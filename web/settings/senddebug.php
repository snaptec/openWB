<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>openWB Fehlermeldung</title>
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

		<header>
			<!-- Fixed navbar -->
			<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
				<div class="navbar-brand">
					openWB
				</div>
			</nav>
		</header>

		<div role="main" class="container" style="margin-top:20px">

			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					Fehlermeldung senden
				</div>
				<?php
					$result = '';
					if (filter_var($_POST['emailAddress'], FILTER_VALIDATE_EMAIL) && strlen($_POST['debugMessage'])>20) {
						$result = $_POST['debugMessage'] . "\n" . $_POST['emailAddress'] . "\n";
						file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/debuguser', $result);
						file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/debugemail', $_POST['emailAddress'] . "\n");

						// header("Location: ./debug.php");
						?>
						<div class="card-body">
							<div class="alert alert-info">
								Debugdaten werden im Hintergrund gesammelt und verschickt. Dieser Vorgang dauert etwa eine Minute.<br>
								Sie werden danach auf die Hauptseite weitergeleitet.
							</div>
							<div class="row">
								<div class="cssload-loader text-center">
									<div class="cssload-inner cssload-one"></div>
									<div class="cssload-inner cssload-two"></div>
									<div class="cssload-inner cssload-three"></div>
								</div>
							</div>
						</div>
						<?php exec("/var/www/html/openWB/runs/senddebuginit.sh > /dev/null &"); // exec in background ?>
						<script>
							window.setTimeout( function() {
								window.location = "index.php";
							}, 60000);
						</script>
						<?php
					} else {
				?>
				<div class="card-body">
					<div class="alert alert-warning">
						Keine gültige Email angegeben oder Fehlerbeschreibung zu kurz.<br>
						Weiterleitung in 5 Sekunden...
					</div>
					<div class="row">
						<div class="cssload-loader text-center">
							<div class="cssload-inner cssload-one"></div>
							<div class="cssload-inner cssload-two"></div>
							<div class="cssload-inner cssload-three"></div>
						</div>
					</div>
				</div>
				<script>
					window.setTimeout( function() {
						window.history.back();
					}, 5000);
				</script>
				<?php
					}
				?>
			</div>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Fehlerbericht</small>
			</div>
		</footer>

	</body>
</html>
