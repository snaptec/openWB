<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>openWB Einstellungen</title>
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

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Software-Update</h1>

			<div class="col alert alert-info" role="alert">
				installierte Version: <span id="installedVersionSpan" data-version=""></span>
			</div>

			<div class="card border-secondary">
				<form class="form" id="releasetrainForm" action="./settings/saveupdate.php" method="POST">
					<div class="card-header bg-secondary">
						Versionsauswahl
					</div>
					<div class="card-body">
						<div class="form-group mb-0">
							<div class="custom-control custom-radio">
								<input class="custom-control-input" type="radio" name="releasetrainRadioBtn" id="radioBtnStable" value="stable" disabled>
								<label class="custom-control-label vaRow" for="radioBtnStable">
									Stable:
									<span class="mx-1" id="availStableVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availStableVersionSpinner"></span>
								</label>
							</div>
							<div class="custom-control custom-radio">
								<input class="custom-control-input" type="radio" name="releasetrainRadioBtn" id="radioBtnBeta" value="beta" disabled>
								<label class="custom-control-label vaRow" for="radioBtnBeta">
									Beta:
									<span class="mx-1" id="availBetaVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availBetaVersionSpinner"></span>
								</label>
							</div>
							<div class="custom-control custom-radio">
								<input class="custom-control-input" type="radio" name="releasetrainRadioBtn" id="radioBtnNightly" value="master" disabled>
								<label class="custom-control-label vaRow" for="radioBtnNightly">
									Nightly:
									<span class="mx-1" id="availNightlyVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availNightlyVersionSpinner"></span>
								</label>
							</div>
						</div>
					</div>
					<div class="card-footer text-center">
						<button type="button" class="btn btn-success" data-toggle="modal" data-target="#updateConfirmationModal">Update</button>
					</div>
				</form>
			</div>

			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					Hinweise
				</div>
				<div class="card-body">
					<div class="row">
						<div class="col">
							<p>Vor dem Update sind ggf. angeschlossene Fahrzeuge abzustecken!</p>
							<p>Eventuell vorhandene externe openWB die als Ladepunkt konfiguriert sind erhalten automatisch ebenso ein Update.</p>
						</div>
					</div>
				</div>
			</div>
			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					Versionserläuterung
				</div>
				<div class="card-body">
					<div class="row">
						<div class="col">
							<p class="alert alert-warning">
								Für alle Versionen gilt: <span class="text-danger">Ein Downgrade auf eine ältere Version kann zu Fehlern führen!</span> Vor dem Update am Besten ein Backup erstellen und dieses im Zweifelsfall wieder einspielen, anstatt ein Downgrade durchzuführen.
							</p>
							<h2>Stable</h2>
							<p>
								Die Stable-Version ist die empfohlene. Sie wurde einschließlich aller Features ausgiebigen Tests unterzogen, dabei sind keine Fehler aufgefallen.
							</p>
							<h2>Beta</h2>
							<p>
								Die Beta-Version beinhaltet neue Features für zukünftige Stable-Versionen, befindet sich aber noch in der Testphase. Fehlverhalten ist nicht ausgeschlossen.
							</p>
							<h2>Nightly</h2>
							<p>
								Die Nightly-Version beinhaltet Neuentwicklungen, die teils nur eingeschränkt getestet sind. Fehlverhalten ist wahrscheinlich.<br>
								Alle Änderungen können auf <a href="https://github.com/snaptec/openWB/commits/master">GitHub</a> eingesehen werden.
							</p>
						</div>
					</div>
				</div>
			</div>

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
					<div class="modal-header btn-danger">
						<h4 class="modal-title text-light">Achtung</h4>
					</div>

					<!-- modal body -->
					<div class="modal-body text-center">
						Aktuelle Version: <span id="modalInstalledVersionSpan"></span><br>
						Soll wirklich ein Update der openWB auf<br>
						<b>die verfügbare Version <span id="selectedVersionSpan"></span></b><br>
						erfolgen?<br>
						Das Update kann einige Zeit in Anspruch nehmen. Alle Einstellungen bleiben erhalten.<br>
						<b>
							Es wird empfohlen, zur Sicherheit zuvor ein Backup zu erstellen.<br>
							<span class="text-danger">Fahrzeuge sind vor dem Update abzustecken!</span>
						</b>
					</div>

					<!-- modal footer -->
					<div class="modal-footer d-flex justify-content-center">
						<button type="button" id="updateBtn" class="btn btn-success" data-dismiss="modal" disabled="disabled">Update</button>
						<button type="button" class="btn btn-danger" data-dismiss="modal">Abbruch</button>
					</div>

				</div>
			</div>
		</div>

		<script>

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navUpdate').addClass('disabled');
				}
			);

			$(document).ready(function(){

				function getVersion(dataURL) {
					// read dataURL filecontent = releasetrain version and return it
					return $.get({
						url: dataURL,
						cache: false
					});
				}

				function displayVersion(releasetrain, url) {
					var elemSpan = "#avail"+releasetrain+"VersionSpan";
					var elemSpinner = "#avail"+releasetrain+"VersionSpinner";
					var elemRadioBtn = "#radioBtn"+releasetrain;
					getVersion(url, function() {
						$(elemSpan).text("rufe ab...");
					})
						.done(function(result) {
							$(elemSpan).text(result);
							$(elemSpan).data("version", result);
							$(elemSpinner).hide();
							$(elemRadioBtn).removeAttr("disabled");
						})
						.fail(function() {
							$(elemSpan).text("derzeit nicht verfügbar");
							$(elemSpan).addClass("text-danger");
							$(elemSpinner).hide();
						});
				}

				$(function getAllVersions() {
					displayVersion("Stable", 'https://raw.githubusercontent.com/snaptec/openWB/stable17/web/version');
					displayVersion("Beta", 'https://raw.githubusercontent.com/snaptec/openWB/beta/web/version');
					displayVersion("Nightly", 'https://raw.githubusercontent.com/snaptec/openWB/master/web/version');
				});

				$.get({
					url: "/openWB/web/version",
					cache: false
				})
				.done(function(result) {
					$("#installedVersionSpan").prepend(result);
					$("#installedVersionSpan").data("version", result);
					$("#modalInstalledVersionSpan").prepend(result);
				});

				if("<?php echo $releasetrain ?>" == "master") {
					$.get({
						url: "/openWB/web/lastcommit",
						cache: false
					})
					.done(function(result) {
						$("#installedVersionSpan").append(" ("+result+")");
						//$("#installedVersionSpan").data("version", result);
						$("#modalInstalledVersionSpan").append(" ("+result+")");
					});
				}


				$(document).ajaxStop(function(){
					// after all ajax requests are finished, set checkbox and enable update button
					var releasetrains = [];
					$(".custom-control-input:enabled").each(function(){
						// all enabled checkbox values
						releasetrains.push( $(this).val() );
					});
					if ( releasetrains.length > 0 ) {
						// if there are any enabled checkBoxes ( equals available updates )
						if ( releasetrains.includes("<?php echo $releasetrain?>") ) {
							// check the box matching config file releasetrain
							$("input[value='<?php echo $releasetrain?>']").prop('checked', true);
						} else if ( releasetrains.includes("stable17") ) {
							// version from config file not availabe so select stable
							$("input[value='stable17']").prop('checked', true);
						} else if ( releasetrains.includes("beta") ) {
							// stable not availabe so select beta
							$("input[value='beta']").prop('checked', true);
						} else if ( releasetrains.includes("master") ) {
							// version from config file not availabe so check if stable can be selected
							$("input[value='master']").prop('checked', true);
						}
						$("#updateBtn").removeAttr("disabled");
					}
					// get the checkbox matching the config file entry
				});

				$('#updateConfirmationModal').on('show.bs.modal', function() {
					// before the modal shows, fill in selected version
					var choice = $(".custom-control-input:checked").attr("value");
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
				}) ;

				// submit form if button in modal window is clicked
				$(document).on("click", '#updateBtn', function() {
					$('#releasetrainForm').submit();
				});

			});

		</script>

	</body>
</html>
