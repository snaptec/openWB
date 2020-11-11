<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>openWB Modulkonfiguration</title>
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
		<script>
			function getCookie(cname) {
				var name = cname + '=';
				var decodedCookie = decodeURIComponent(document.cookie);
				var ca = decodedCookie.split(';');
				for(var i = 0; i <ca.length; i++) {
					var c = ca[i];
					while (c.charAt(0) == ' ') {
						c = c.substring(1);
					}
					if (c.indexOf(name) == 0) {
						return c.substring(name.length, c.length);
					}
				}
				return '';
			}
			var themeCookie = getCookie('openWBTheme');
			// include special Theme style
			if( '' != themeCookie ){
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20201019">');
			}
		</script>
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
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Modulkonfiguration</small>
			</div>
		</footer>
<?php
	// receives chosen modulconfig pages via POST-request,
	// writes value to config file and returns to theme
	// author: M. Ortenstein, L. Bender

	$myConfigFile = $_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf';

	// prepare key/value array
	$settingsArray = [];

	try {
		if ( !file_exists($myConfigFile) ) {
			throw new Exception('Konfigurationsdatei nicht gefunden.');
		}
		// first read config-lines in array
		$settingsFile = file($myConfigFile);

		// convert lines to key/value array for faster manipulation
		foreach($settingsFile as $line) {
			// split line at char '='
			$splitLine = explode('=', $line, 2);
			// trim parts
			$splitLine[0] = trim($splitLine[0]);
			$splitLine[1] = trim($splitLine[1]); // do not trim single quotes, we will need them later
			// push key/value pair to new array
			$settingsArray[$splitLine[0]] = $splitLine[1];
		}
		// now values can be accessed by $settingsArray[$key] = $value;

		// update chosen setting in array
		foreach($_POST as $key => $value) {
			// check if loaded config entry has single quotes
			if( (strpos( $settingsArray[$key], "'" ) === 0) && (strrpos( $settingsArray[$key], "'" ) === strlen( $settingsArray[$key])-1) ){
				$settingsArray[$key] = "'".$value."'";
			} else {
				$settingsArray[$key] = $value;
			}
		}

		// write config to file
		$fp = fopen($myConfigFile, "w");
		if ( !$fp ) {
			throw new Exception('Konfigurationsdatei konnte nicht geschrieben werden.');
		}
		foreach($settingsArray as $key => $value) {
			fwrite($fp, $key."=".$value."\n");
		}
		fclose($fp);

		// update display process if in POST data
		if( array_key_exists( 'displayaktiv', $_POST ) ){
			file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/reloaddisplay', "1");
			file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/execdisplay', "1");
		}

		// update smashm.conf if in POST data
		if( array_key_exists( 'smashmbezugid', $_POST ) ){
			$result = '';
			$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/web/files/smashm.conf');
			foreach($lines as $line) {
				if( (strpos($line, "serials=") !== false) and (strpos($line, "serials=") == 0) ) {
						$result .= 'serials='.$_POST['smashmbezugid']."\n";
				} else {
					$result .= $line;
				}
			}
			file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/web/files/smashm.conf', $result);
		}

		// update i3 SoC auth files if in POST data
		if( array_key_exists( 'i3username', $_POST ) ){
			// charge point 1
			$i3authfile = $_SERVER['DOCUMENT_ROOT']."/openWB/modules/soc_i3/auth.json";
			$i3auth_fp = fopen($i3authfile, 'w');
			fwrite($i3auth_fp,"{".PHP_EOL.'"username": "'.$settingsArray['i3username'].'",'.PHP_EOL.'"password": "'.$settingsArray['i3passwort'].'",'.PHP_EOL.'"vehicle": "'.$settingsArray['i3vin'].'"'.PHP_EOL."}".PHP_EOL);
			fclose($i3auth_fp);
		}
		if( array_key_exists( 'i3usernames1', $_POST ) ){
			// charge point 2
			$i3authfile = $_SERVER['DOCUMENT_ROOT']."/openWB/modules/soc_i3s1/auth.json";
			$i3auth_fp = fopen($i3authfile, 'w');
			fwrite($i3auth_fp,"{".PHP_EOL.'"username": "'.$settingsArray['i3usernames1'].'",'.PHP_EOL.'"password": "'.$settingsArray['i3passworts1'].'",'.PHP_EOL.'"vehicle": "'.$settingsArray['i3vins1'].'"'.PHP_EOL."}".PHP_EOL);
			fclose($i3auth_fp);
		}

	} catch ( Exception $e ) {
		$msg = $e->getMessage();
		echo "<script>alert('$msg');</script>";
	}

	// return to theme
	echo "<script>window.location.href='index.php';</script>";
?>
	</body>
</html>
