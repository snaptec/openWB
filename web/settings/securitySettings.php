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
		<div id="nav"></div> <!-- placeholder for navbar -->
		

		<?php			   
			$lines = file('/var/www/html/openWB/openwb.conf');
			foreach($lines as $line) {      
				if(strpos($line, "https=") !== false) {
					list(, $httpsold) = explode("=", $line); 
				}
				if(strpos($line, "httpsCert=") !== false) {
					list(, $httpsCertold) = explode("=", $line); 
				}
			} 
		?>


		<div role="main" class="container" style="margin-top:20px">
		<div class="col-sm-12"><?php echo $_SERVER['HTTP_HOST']; ?>
				<form action="./tools/saveSecuritySettings.php" method="POST">
					<h3>HTTPS</h3>
					<div class="row">
					       	<b><label for="https">Https aktivieren: </label></b>
					       	<select name="https" id="https">
						       	<option <?php if($httpsold == 0) echo "selected" ?> value="0">Deaktiviert</option>
						       	<option <?php if($httpsold == 1) echo "selected" ?> value="1">Aktiviert</option>
						</select>
						<div class="row">
							Wenn diese Option ativiert ist, ist OpenWB über Https erreichbar. Die Adresse ist danach
							https://ip-der-openwp/openwb oder https://name-der-openwb/openwb
						</div>
						<input type=hidden id="httpsold" value="<?php echo $httpsold ?>" />
				       	</div>
					<div class="row">
						<b><label for="httpsCert">Selfsigned Zertifikat erstellen: </label></b>
						<select name="httpsCert" id="httpsCert">
							<option <?php if($httpsCertold == 0) echo "selected" ?> value="0">Ja</option>
							<option <?php if($httpsCertold == 1) echo "selected" ?> value="1">Nein</option>
						</select>
						<div class="row">
							Wenn Ja ausgewählt wird, wird beim speichern ein neues Selber signiertes Zertifikat für HTTPS erstellt.
							Dies ist die einfachere aber auch weniger sichere Art Https zu aktivieren. Wann immer die Möglichkeit
							und das Wissen besteht ein Zertifikat über eine Root Authority wie LetsEncrypt zu erstellen wird empfohlen
							dies zu deaktivieren und in /etc/ssl/certs/openwb.crt und /etc/ssl/private/openwb.key ein gültiges 
							Zertifikat zu installieren.
						</div>
						<input type=hidden id="httpsCertold" value="<?php echo $httpsCertold ?>" />
					</div>

					<button type="submit" name="action" value="save" class="btn btn-green">Save</button>
				</form>
				<hr>
			</div>
		</div>  <!-- container -->

		<script type="text/javascript">
 			$(document).ready(function(){
 				// disable navbar entry for current page
				$('#navSicherheitsEinstellungen').addClass('disabled');
				});
		</script>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: Einstellungen/Sicherheits Einstellungen</small>
			</div>
		</footer>

		<script type="text/javascript">

			$.get("settings/navbar.php", function(data){
				$("#nav").replaceWith(data);
				// disable navbar entry for current page
				$('#navSicherheitsEinstellungen').addClass('disabled');
			});
			
		</script>

	</body>
</html>
