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
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
	</head>

	<body>
		<?php
			$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
			foreach($lines as $line) {
				list($key, $value) = explode("=", $line, 2);
				${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
			}

			if ( $debugold == "" ) {
				// if no debug mode set, set 0 = off
				$debugold = "0";
			}

		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Debugging und Support</h1>

			<div class="card border-secondary">
				<form class="form" id="debugmodeForm" action="./settings/saveconfig.php" method="POST">
					<div class="card-header bg-secondary">
						Protokollierung
					</div>
					<div class="card-body">
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Debug-Modus</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($debugold == 0) echo " active" ?>">
											<input type="radio" name="debug" id="debugmode0" value="0"<?php if($debugold == 0) echo " checked=\"checked\"" ?>>Mode 0 (aus)
										</label>
										<label class="btn btn-outline-info<?php if($debugold == 2) echo " active" ?>">
											<input type="radio" name="debug" id="debugmode1" value="1"<?php if($debugold == 1) echo " checked=\"checked\"" ?>>Mode 1 (Regelwerte)
										</label>
										<label class="btn btn-outline-info<?php if($debugold == 2) echo " active" ?>">
											<input type="radio" name="debug" id="debugmode2" value="2"<?php if($debugold == 2) echo " checked=\"checked\"" ?>>Mode 2 (Berechnungsgrundlage)
										</label>
									</div>
									<span class="form-text small">
										Mit dieser Einstellung können zusätzliche Log-Meldungen aktiviert werden, um eine Fehlersuche zu vereinfachen.
									</span>
								</div>
							</div>
						</div>
						<div class="form-group">
							<div class="form-row mb-1">
								<div class="col-md-4">
									<label class="col-form-label">Gateway prüfen</label>
								</div>
								<div class="col">
									<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">
										<label class="btn btn-outline-info<?php if($pingcheckactiveold == 0) echo " active" ?>">
											<input type="radio" name="pingcheckactive" id="pingcheckactive0" value="0"<?php if($pingcheckactiveold == 0) echo " checked=\"checked\"" ?>>Aus
										</label>
										<label class="btn btn-outline-info<?php if($pingcheckactiveold == 2) echo " active" ?>">
											<input type="radio" name="pingcheckactive" id="pingcheckactive1" value="1"<?php if($pingcheckactiveold == 1) echo " checked=\"checked\"" ?>>An
										</label>
									</div>
									<span class="form-text small">
										Wird diese Option aktiviert, dann wird die Verbindung zum Netzwerk Gateway alle 5 Minuten mit einem Ping geprüft.
									</span>
								</div>
							</div>
						</div>
					</div>
					<div class="card-footer text-center">
						<button type="submit" class="btn btn-success">Speichern</button>
					</div>
				</form>
			</div>

			<div class="card border-secondary">
				<form class="form" id="sendTokenForm" action="./settings/starttunnel.php" method="POST">
					<div class="card-header bg-secondary">
						Remote Support
					</div>
					<div class="card-body">
						<?php if ( $datenschutzackold != 1 ) { ?>
						<div class="alert alert-danger">
							Sie müssen der <a href="settings/datenschutz.html">Datenschutzerklärung</a> zustimmen, um den Online-Support nutzen zu können.
						</div>
						<?php } else { ?>
						<div class="alert alert-success">
							Sie haben der <a href="settings/datenschutz.html">Datenschutzerklärung</a> zugestimmt und können den Online-Support nutzen.
						</div>
						<?php } ?>
						<div class="form-group mb-0">
							<span id="textHelpBlock" class="form-text">Durch Angabe des Tokens und mit Klick auf "Tunnel herstellen" wird eine Verbindung von der lokalen openWB zum openWB Support hergestellt. openWB erhält damit Vollzugriff auf diese Installation. Diese Schnittstelle nur nach Aufforderung mit dem entsprechenden Token aktivieren.</span>
							<?php
								$remoteSupportRunning = false;
								$pidFile = $_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/remotesupportpid';
								if( file_exists($pidFile) ){
									echo "<!-- file exists -->\n";
									$remoteSupportPid = trim(file_get_contents($pidFile));
									if( file_exists('/proc/'.$remoteSupportPid) ){
										echo "<!-- process is running -->\n";
										if( substr(file_get_contents('/proc/'.$remoteSupportPid.'/cmdline'), 0, 7) == 'sshpass' ){
											echo "<!-- process is sshpass -->\n";
											$remoteSupportRunning = true;
											?>
												<div class="alert alert-warning">
													Es ist bereits ein Support-Tunnel aufgebaut.
												</div>
											<?php
										} else {
											echo "<!-- process is not sshpass -->\n";
											// process is not a sshpass, remove outdated pid file
											unlink($pidFile);
										}
									} else {
										echo "<!-- process is not running -->\n";
										// process not running, remove pid file
										unlink($pidFile);
									}
								}
								if( !$remoteSupportRunning ){
									?>
									<div class="input-group">
										<div class="input-group-prepend">
											<div class="input-group-text">
												<i class="fa fa-key"></i>
											</div>
										</div>
										<input type="text" class="form-control" id="token" name="token" placeholder="Token" aria-describedby="textHelpBlock" required="required">
									</div>
									<?php
								}
							?>
						</div>
					</div>
					<div class="card-footer text-center">
						<button type="submit" class="btn btn-success"<?php if( $datenschutzackold != 1 || $remoteSupportRunning ) echo ' disabled="disabled"'; ?>>Tunnel herstellen</button>
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
