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
		$authfile = $_SERVER['DOCUMENT_ROOT'].'/openWB/web/settings/.htaccess';
		$passwordfile = $_SERVER['DOCUMENT_ROOT'].'/openWB/web/settings/.passwd';
		$tempfile = $_SERVER['DOCUMENT_ROOT'].'/openWB/web/settings/temppassword';
		?>

		<div id="nav"></div> <!-- placeholder for navbar -->

		<div role="main" class="container" style="margin-top:20px">
			<div class="col-sm-12">
				<div class="row">
					<h3>Passwortschutz</h3>
				</div>
				<?php
					if(array_key_exists( 'action', $_POST )){ // We need to do something...
						?>
						<div class="row">
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
									<p class="text-success">Passwortschutz wurde eingerichtet.</p>
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
									<p class="text-danger">Passwortschutz wurde entfernt.</p>
								</div>
								<?php
							break;
						}
					}
					if( !file_exists( $authfile )){ // show form to setup password protection
						?>
						<form action="./settings/setPassword.php" method="POST">
							<div class="row">
								<b><label for="username">Benutzername:</label></b> <input type="text" name="username" id="username" value="" required pattern="[A-Za-z0-9]*">
							</div>
							<div class="row">
								Der Benutzername darf nur Buchstaben und Zahlen enthalten. Keine Umlaute, Sonderzeichen oder Leerzeilen.
							</div>
							<div class="row">
								<b><label for="password">Passwort:</label></b> <input type="password" name="password" id="password" value="" required>
							</div>
							<div class="row">
								Passwort des Accounts.
							</div>

							<button type="submit" name="action" value="create" class="btn btn-green">Passwort einrichten</button>
						</form>
						<?php
					} else { // show button to delete password protection
						?>
						<div class="row">
							<h4>Es wurde bereits ein Passwort eingerichtet.</h4>
						</div>
						<div class="row">
							<form action="./settings/setPassword.php" method="POST">
								<button type="submit" name="action" value="delete" class="btn btn-red">Passwort löschen</button>
							</form>
						</div>
						<?php
					}
				?>
				<hr>
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
			</div>
		</div>  <!-- container -->

		<script type="text/javascript">
 			$(document).ready(function(){
 				// disable navbar entry for current page
				$('#navPasswortschutz').addClass('disabled');
				});
		</script>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/Passwortschutz</small>
			</div>
		</footer>

		<script type="text/javascript">

			$.get("settings/navbar.html", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navPasswort').addClass('disabled');
			});

		</script>

	</body>
</html>
