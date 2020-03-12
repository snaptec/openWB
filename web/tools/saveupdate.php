<!DOCTYPE html>
<html lang="de">
	<head>
		<title>Update wird gestartet</title>
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
		echo "<script>window.location.href='../index.php';</script>";
	}
	// if successfully saved to config, start update
	echo "<script>window.location.href='./update.php';</script>";
?>
	</body>
</html>
