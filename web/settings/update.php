<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>OpenWB</title>
		<meta name="description" content="Control your charge" />
		<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
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

			include '/var/www/html/openWB/web/settings/navbar.php';

			// read selected releasetrain from config file
			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {
				if(strpos($line, "releasetrain=") !== false) {
					list(, $releasetrain) = explode("=", $line);
				}
			}
			$releasetrain = trim($releasetrain);

			if ( $releasetrain == "" ) {
				// if no releasetrain set, set stable
				$releasetrain="stable";
			}

		?>

		<div role="main" class="container" style="margin-top:20px">
			<div class="row">
				<div class="col">
					<h1>Versionsübersicht</h1>
				</div>
			</div>
			<div class="row">
				<div class="col">
					<div>
						<b>installierte Version:
							<span id="installedVersionSpan" data-version=""></span>
						</b><br>
					</div>
					<div>
						verfügbare Stable:
						<span id="availStableVersionSpan" data-version="">nicht verfügbar</span>
						<br>
					</div>
					<div>
						verfügbare Beta:
						<span id="availBetaVersionSpan" data-version="">nicht verfügbar</span>
						<br>
					</div>
					<div>
						verfügbare Nightly:
						<span id="availNightlyVersionSpan" data-version="">nicht verfügbar</span>
						<br>
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<h1>Versionserläuterung</h1>
				</div>
			</div>
			<div class="row">
				<div class="col">
						<b>Stable</b><br>
						Die Stable-Version ist die empfohlene. Sie wurde einschließlich aller Features ausgiebigen Tests unterzogen und als fehlerfrei bewertet.
					<br>
						<b>Beta</b><br>
						Die Beta-Version beinhaltet neue Features für zukünftige Stable-Versionen, befindet sich aber noch in der Testphase. Fehlverhalten ist nicht ausgeschlossen.
					<br>
						<b>Nightly</b><br>
						Die Nightly-Version beinhaltet Neuentwicklungen, die teils nur eingeschränkt getestet sind. Fehlverhalten ist wahrscheinlich.
				</div>
			</div>

			<div class="row">
				<div class="col">
					<h1>Versionsauswahl</h1>
				</div>
			</div>
			<form class="form" id="releasetrainForm" action="./tools/saveupdate.php" method="POST">
				<div class="form-row align-items-center">
					<div class="col-auto">
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="stableRadioBtn" value="stable" <?php if($releasetrain == "stable") echo checked?>>
								<label class="form-check-label" for="stableRadioBtn">
								    Stable
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="betaRadioBtn" value="beta" <?php if($releasetrain == "beta") echo checked?>>
								<label class="form-check-label" for="betaRadioBtn">
									Beta
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="nightlyRadioBtn" value="master" <?php if($releasetrain == "master") echo checked?>>
								<label class="form-check-label" for="nightlyRadioBtn">
									Nightly
								</label>
							</div>
						</div>
					</div>
					<div class="col-auto">
						<button type="button" class="btn btn-green" data-toggle="modal" data-target="#updateConfirmationModal">Update</button>
					</div>
				</div>
				<br>
			</form>

		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
		  <div class="container text-center">
			  <small>Sie befinden sich hier: System/Update</small>
		  </div>
		</footer>

		<!-- modal update-confirmation window -->
		<div class="modal fade" id="updateConfirmationModal" role="dialog">
		    <div class="modal-dialog" role="document">
		        <div class="modal-content">

		            <!-- modal header -->
		            <div class="modal-header btn-red">
		                <h4 class="modal-title text-light">Achtung</h4>
		            </div>

		            <!-- modal body -->
		            <div class="modal-body text-center">
                        Aktuelle Version: <span id="modalInstalledVersionSpan"></span>
						<br>
                        <br>
                        Soll wirklich ein Update der openWB auf<br>
                        <b>die verfügbare Version <span id="selectedVersionSpan"></span></b><br>
                        erfolgen?<br>
                        <br>
                        Das Update kann einige Zeit in Anspruch nehmen. Alle Einstellungen bleiben erhalten.
                        <br>
                        <b>
                            Es wird empfohlen, zur Sicherheit zuvor ein Backup zu erstellen.<br>
                            <span class="text-danger">Fahrzeuge sind vor dem Update abzustecken!</span>
                        </b>
		            </div>

		            <!-- modal footer -->
		            <div class="modal-footer d-flex justify-content-center">
		                <button type="button" id="updateBtn" class="btn btn-green" data-dismiss="modal">Update</button>
		                <button type="button" class="btn btn-red" data-dismiss="modal">Abbruch</button>
		            </div>

		        </div>
		    </div>
		</div>

		<script type="text/javascript">

			$(document).ready(function(){

				// get available versions from github and fill divs
				$.get('https://raw.githubusercontent.com/snaptec/openWB/stable/web/version')
					.done(function(result) {
						$("#availStableVersionSpan").text(result);
						$("#availStableVersionSpan").data("version", result);
					});
				$.get('https://raw.githubusercontent.com/snaptec/openWB/beta/web/version')
					.done(function(result) {
						$("#availBetaVersionSpan").text(result);
						$("#availBetaVersionSpan").data("version", result);
					});
				$.get('https://raw.githubusercontent.com/snaptec/openWB/master/web/version')
					.done(function(result) {
						$("#availNightlyVersionSpan").text(result);
						$("#availNightlyVersionSpan").data("version", result);
					});
				$.get('/openWB/web/version')
					.done(function(result) {
						$("#installedVersionSpan").text(result);
						$("#installedVersionSpan").data("version", result);
						$("#modalInstalledVersionSpan").text(result);
					});

				// fill modal text with selected Version string
				$(document).on('click', "[name = 'releasetrainRadioBtn']", function() {
					// get checked choice
					var choice = $("input[type=radio]:checked").attr("value");
					// and set text
					switch (choice) {
						case "stable":
							$("#selectedVersionSpan").text( $("#availStableVersionSpan").data("version") );
							break;
						case "beta":
							$("#selectedVersionSpan").text( $("#availBetaVersionSpan").data("version") );
							break;
						case "master":
							$("#selectedVersionSpan").text( $("#availNightlyVersionSpan").data("version") );
							break;
					}
				});

				// submit form if button in modal window is clicked
				$(document).on('click', '#updateBtn', function() {
					$('#releasetrainForm').submit();
				});

			});

		</script>

	</body>
</html>
