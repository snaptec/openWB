<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>openWB Hilfe</title>
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
		<link rel="stylesheet" type="text/css" href="hilfe/hilfe_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
	</head>
		<?php 
			$ethstate = file_get_contents('/sys/class/net/eth0/carrier');
			if ( $ethstate == 1 ) {
				header('Location:/openWB/web/index.php');
			}
		?>
		<br><br>
		<p>
		<h4> Neue Wlanverbindung einrichten</h3>
		</p>
		<h5> Gefundene Wlan Netze:</h5>
		<?php
			$command = escapeshellcmd("sudo /bin/bash /var/www/html/openWB/web/tools/wlan/wlan0.sh"); 
			$output = shell_exec($command); 
			echo $output;
		?>
		<form action="tools/wlan/wlan1.php" method="post" autocomplete="off">
		<br><br>
		<h5> Neuverbinden mit</h5>
		<p> Wlan SSID: <input id="wssid" type="text" name="wssid" /></p>
		<p> Wlan Password: <input id="wpassword" type="text" name="wpassword" /></p>
		<p><input type="submit" value="Verbinden" /></p>
		<br><br>
	<body>
	<?php
		include '/var/www/html/openWB/web/tools/wlan/navbar.php';
	?>

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small id="WlanFooterText">Sie befinden sich hier:tools/wlan</small>
			</div>
		</footer>

	</body>
</html>
