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

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Netzwerk-Einstellungen</h1>
			<?php
			$currentHostname = gethostname();
			if(array_key_exists( 'action', $_POST )){ // We need to do something...
				switch( $_POST['action'] ){
					case 'rename':
						// change hostname
						$cmd = "sudo /var/www/html/openWB/runs/sethostname.sh " . escapeshellarg( $_POST['hostname'] );
						exec( $cmd, $output, $returnval );
						?>
						<div class="col alert alert-success" role="alert">
							Der Hostname wurde geändert auf '<?php echo $_POST['hostname']; ?>'.<br>
							Die openWB wird jetzt neu gestartet.
						</div>
						<script>
							window.setTimeout(() => {
								$("#rebootConfirmationModal").modal("show");
							}, 3000);
						</script>
						<?php
					break;
				}
			} else { // nothing to do yet, show input field ?>

				<div class="card border-secondary">
					<div class="card-header bg-secondary">
						Hostname ändern
					</div>
					<form action="./settings/network.php" method="POST">
						<div class="card-body">
							<div class="row form-group">
								<label for="hostname" class="col-md-4 col-form-label">Neuer Hostname</label>
								<div class="col">
									<input type="text" name="hostname" id="hostname" value="<?php echo $currentHostname; ?>" placeholder="Name" aria-describedby="hostnameHelpBlock" class="form-control" required="required" pattern="[A-Za-z0-9_-]*">
									<span id="hostnameHelpBlock" class="form-text small">
										Der Hostname darf nur Buchstaben, Zahlen und die Zeichen "-_" enthalten. Keine Umlaute, Sonderzeichen oder Leerzeichen.<br>
										<span class="text-danger">Die openWB wird direkt nach der Änderung neu gestartet! Alle Fahrzeuge sind vorher abzustecken!</span>
									</span>
								</div>
							</div>
						</div>
						<div class="card-footer text-center">
							<button type="submit" name="action" value="rename" class="btn btn-success">Hostnamen ändern</button>
						</div>
					</form>
				</div> <!-- card end -->
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
				<small>Sie befinden sich hier: Einstellungen/Netzwerk-Einstellungen</small>
			</div>
		</footer>

		<script>
			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navNetworkSettings').addClass('disabled');
				}
			);
		</script>

	</body>
</html>
