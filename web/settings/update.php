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
		<link rel="stylesheet" type="text/css" href="settings/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.4.1.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
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
			<div class="row">
				<div class="col">
					<h1>Versionsauswahl</h1>
				</div>
			</div>
			<div class="row">
				<div class="col">
					<div>
						<b>installierte Version: <span id="installedVersionSpan" data-version=""></span></b>
					</div>
				</div>
			</div>
			<br>
			<form class="form" id="releasetrainForm" action="./tools/saveupdate.php" method="POST">
				<div class="form-row align-items-center">
					<div class="col">
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="radioBtnStable" value="stable" disabled>
								<label class="form-check-label vaRow" for="radioBtnStable">
									Stable:
									<span class="mx-1" id="availStableVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availStableVersionSpinner"></span>
									<br>
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="radioBtnStableold" value="stableold" disabled>
								<label class="form-check-label vaRow" for="radioBtnStableold">
									Stable old:
									<span class="mx-1" id="availStableoldVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availStableoldVersionSpinner"></span>
									<br>
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="radioBtnBeta" value="beta" disabled>
								<label class="form-check-label vaRow" for="radioBtnBeta">
									Beta:
									<span class="mx-1" id="availBetaVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availBetaVersionSpinner"></span>
									<br>
								</label>
							</div>
						</div>
						<div class="form-group">
							<div class="form-check">
								<input class="form-check-input" type="radio" name="releasetrainRadioBtn" id="radioBtnNightly" value="master" disabled>
								<label class="form-check-label vaRow" for="radioBtnNightly">
									Nightly:
									<span class="mx-1" id="availNightlyVersionSpan" data-version=""></span><span class="spinner-grow spinner-grow-sm" id="availNightlyVersionSpinner"></span>
									<br>
								</label>
							</div>
						</div>
					</div>
				</div>
				<div class="form-row ">
					<div class="col-auto">
						<button type="button" class="btn btn-green" data-toggle="modal" data-target="#updateConfirmationModal">Update</button>
					</div>
				</div>
				<br>
			</form>

			<div class="row">
				<div class="col">
					<h1>Versionserläuterung</h1>
				</div>
			</div>
			<div class="row">
				<div class="col">
					<h2>Stable</h2>
					<p>Die Stable-Version ist die empfohlene. Sie wurde einschließlich aller Features ausgiebigen Tests unterzogen, dabei sind keine Fehler aufgefallen.</p>
					<h2>Stable old</h2>
					<p>Ist das letzte (ältere) Release. Sie wurde einschließlich aller Features ausgiebigen Tests unterzogen, dabei sind keine Fehler aufgefallen.</p>
					<h2>Beta</h2>
					<p>Die Beta-Version beinhaltet neue Features für zukünftige Stable-Versionen, befindet sich aber noch in der Testphase. Fehlverhalten ist nicht ausgeschlossen.</p>
					<h2>Nightly</h2>
					<p>Die Nightly-Version beinhaltet Neuentwicklungen, die teils nur eingeschränkt getestet sind. Fehlverhalten ist wahrscheinlich.</p>
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
					<div class="modal-header btn-red">
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
						<button type="button" id="updateBtn" class="btn btn-green" data-dismiss="modal">Update</button>
						<button type="button" class="btn btn-red" data-dismiss="modal">Abbruch</button>
					</div>

				</div>
			</div>
		</div>

		<script type="text/javascript">

			$.get("settings/navbar.php", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navUpdate').addClass('disabled');
			});

			$(document).ready(function(){

				function getVersion(dataURL) {
					// read dataURL filecontent = releasetrain version and return it
					return $.get(dataURL);
				}

				function displayVersion(releasetrain, url) {
					var elemSpan = "#avail"+releasetrain+"VersionSpan";
					var elemSpinner = "#avail"+releasetrain+"VersionSpinner";
					var elemRadioBtn = "#radioBtn"+releasetrain;
					var getURL = url + "?" + $.now();  // add timestamp to request to avoid cache
					getVersion(getURL, function() {
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
					displayVersion("Stableold", 'https://raw.githubusercontent.com/snaptec/openWB/stable/web/version');
					displayVersion("Beta", 'https://raw.githubusercontent.com/snaptec/openWB/beta/web/version');
					displayVersion("Nightly", 'https://raw.githubusercontent.com/snaptec/openWB/master/web/version');
				});

				$.get("/openWB/web/version")
					.done(function(result) {
						$("#installedVersionSpan").text(result);
						$("#installedVersionSpan").data("version", result);
						$("#modalInstalledVersionSpan").text(result);
					});

				$(document).ajaxStop(function(){
					// after all ajax requests are finished, set checkbox and enable update button
					var releasetrains = [];
					$(".form-check-input:enabled").each(function(){
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
						} else if ( releasetrains.includes("stable") ) {
							// version from config file not availabe so select stable
							$("input[value='stable']").prop('checked', true);

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
					var choice = $(".form-check-input:checked").attr("value");
					// and set text
					switch (choice) {
						case "stable":
							$("#selectedVersionSpan").text( $("#availStableVersionSpan").data("version") );
							break;
						case "stableold":
							$("#selectedVersionSpan").text( $("#availStableoldVersionSpan").data("version") );
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
