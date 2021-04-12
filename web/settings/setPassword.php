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
		$authfile = $_SERVER['DOCUMENT_ROOT'].'/openWB/web/settings/.htaccess';
		$passwordfile = $_SERVER['DOCUMENT_ROOT'].'/openWB/web/settings/.passwd';
		$tempfile = $_SERVER['DOCUMENT_ROOT'].'/openWB/web/settings/temppassword';
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<h1>Passwortschutz der Einstellungen</h1>
			<?php if(array_key_exists( 'action', $_POST )){ // We need to do something... ?>
				<?php
					switch( $_POST['action'] ){
						case 'create':
							// setup password protection
							// generate necessary files and set proper permissions
							exec( 'sudo touch ' . $passwordfile . ' ' . $authfile . ' ' . $tempfile );
							exec( 'sudo chown pi:pi ' . $passwordfile . ' ' . $authfile . ' ' . $tempfile );
							exec( 'sudo chmod 666 ' . $passwordfile . ' ' . $authfile . ' ' . $tempfile );
							// save password in file
							// no need to worry about special characters
							file_put_contents( $tempfile, $_POST['password'] );
							// generate password hash
							exec( 'sudo htpasswd -i -c ' . $passwordfile . ' ' . $_POST['username'] . ' < ' . $tempfile );
							// remove temp password file
							exec( 'sudo rm ' . $tempfile );
							// write .htaccess file
							$htaccessFile = fopen( $authfile, 'w');
							fwrite( $htaccessFile, <<<AUTHEND
AuthType Basic
AuthUserFile $passwordfile
AuthName "openWB Einstellungen"
require valid-user

<Files ".passwd">
  Require all denied
</Files>
AUTHEND
							);
							fclose( $htaccessFile );
							// protect .htaccess file
							exec( 'sudo chmod 644 ' . $passwordfile . ' ' . $authfile );
							?>
							<div class="col alert alert-success" role="alert">
								Passwortschutz wurde eingerichtet.
							</div>
							<?php
						break;
						case 'delete':
							// remove password protection
							// simply delete both files
							if( file_exists( $authfile )){
								exec( 'sudo rm ' . $authfile );
							}
							if( file_exists( $passwordfile )){
								exec( 'sudo rm ' . $passwordfile );
							}
							?>
							<div class="col alert alert-danger" role="alert">
								Passwortschutz wurde entfernt.
							</div>
							<?php
						break;
					}
			} ?>

			<div class="card border-secondary">
				<div class="card-header bg-secondary">
					Anmeldedaten
				</div>
				<?php
					if( !file_exists( $authfile )){ // show form to setup password protection
						?>
						<form action="./settings/setPassword.php" method="POST">
							<div class="card-body">
								<div class="row form-group">
									<label for="username" class="col-md-4 col-form-label">Benutzername</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-user"></i>
												</div>
											</div> 
											<input type="text" name="username" id="username" value="" placeholder="Benutzername" aria-describedby="usernameHelpBlock" class="form-control" required="required" pattern="[A-Za-z0-9]*">
										</div>
										<span id="usernameHelpBlock" class="form-text small">Der Benutzername darf nur Buchstaben und Zahlen enthalten. Keine Umlaute, Sonderzeichen oder Leerzeilen.</span>
									</div>
								</div>
								<div class="row form-group mb-0">
									<label for="password" class="col-md-4 col-form-label">Passwort</label>
									<div class="col">
										<div class="input-group">
											<div class="input-group-prepend">
												<div class="input-group-text">
													<i class="fa fa-lock"></i>
												</div>
											</div> 
											<input type="password" name="password" id="password" value="" placeholder="Passwort" class="form-control" required="required">
										</div>
									</div>
								</div>
							</div>
							<div class="card-footer text-center">
								<button type="submit" name="action" value="create" class="btn btn-success">Passwort einrichten</button>
							</div>
						</form>
						<?php
					} else { // show button to delete password protection
						?>
						<div class="card-body">
							Es wurde bereits ein Passwort eingerichtet.
						</div>
						<div class="card-footer text-center">
							<form action="./settings/setPassword.php" method="POST">
								<button type="submit" name="action" value="delete" class="btn btn-danger">Passwort löschen</button>
							</form>
						</div>
						<?php
					}
				?>
			</div> <!-- card end -->
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
				<small>Sie befinden sich hier: Einstellungen/Passwortschutz</small>
			</div>
		</footer>

		<script>
 			$(document).ready(function(){
 				// disable navbar entry for current page
				$('#navPasswortschutz').addClass('disabled');
			});

			$.get(
				{ url: "settings/navbar.html", cache: false },
				function(data){
					$("#nav").replaceWith(data);
					// disable navbar entry for current page
					$('#navPasswortschutz').addClass('disabled');
				}
			);
		</script>

	</body>
</html>
