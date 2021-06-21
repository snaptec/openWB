<!DOCTYPE html>
<html lang="de">

	<head>
		<base href="/openWB/web/">

		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>openWB Update wird gestartet</title>
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
				$('head').append('<link rel="stylesheet" href="themes/' + themeCookie + '/settings.css?v=20200801">');
			}
		</script>
	</head>

	<body>
<?php

	// receives chosen releasetrain from update-page via POST-request,
	// writes value to config file and start update
	// author: M. Ortenstein

	$myConfigFile = '/var/www/html/openWB/openwb.conf';

	try {
		if ( !file_exists($myConfigFile) ) {
			throw new Exception('Konfigurationsdatei nicht gefunden.');
		}
		// first read config-lines in array
		$settingsFile = file($myConfigFile);
		// prepare key/value array
		$settingsArray = [];

		// convert lines to key/value array for faster manipulation
		foreach($settingsFile as $line) {
			// check for comment-lines in older config files and don't process them
			if ( strlen(trim($line)) > 3 && $line[0] != "#" ) {
				// split line at char '='
				$splitLine = explode('=', $line, 2);
				// trim parts
				$splitLine[0] = trim($splitLine[0]);
				$splitLine[1] = trim($splitLine[1]);
				// push key/value pair to new array
				$settingsArray[$splitLine[0]] = $splitLine[1];
			}
		}
		// now values can be accessed by $settingsArray[$key] = $value;

		// update chosen setting in array
		$settingsArray["releasetrain"] = $_POST["releasetrainRadioBtn"];

		// write config to file
  		$fp = fopen($myConfigFile, "w");
		if ( !$fp ) {
			throw new Exception('Konfigurationsdatei konnte nicht geschrieben werden.');
  		}
		foreach($settingsArray as $key => $value) {
			fwrite($fp, $key.'='.$value."\n");
		}
		fclose($fp);
	} catch ( Exception $e ) {
		$msg = $e->getMessage();
		echo "<script>alert('$msg');</script>";
		// return to theme on error
		echo "<script>window.location.href='index.php';</script>";
	}
	// if successfully saved to config, start update
	echo "<script>window.location.href='tools/update.php';</script>";
?>
	</body>
</html>
