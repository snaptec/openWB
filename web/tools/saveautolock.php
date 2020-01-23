<?php

	// writes settings from autolock-page via POST-request to config file
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
			// split line at char '='
			$splitLine = explode('=', $line);
			// trim parts
			$splitLine[0] = trim($splitLine[0]);
			$splitLine[1] = trim($splitLine[1]);
			// push key/value pair to new array
			$settingsArray[$splitLine[0]] = $splitLine[1];
		}
		// now values can be accessed by $settingsArray[$key] = $value;

		// due to naming convention in calling file
		// values will be parsed as arrays
		// rebuild key names and put respective key/value pair in $settingsArray
		foreach($_POST as $key => $chargePoint) {
			// will process keys lockBoxLp, unlockBoxLp, lockTimeLp and unlockTimeLp
			foreach($chargePoint as $numberOfLp => $dayOfWeek) {
				// process all lp
				foreach($dayOfWeek as $numberOfDay => $value) {
					// process days of week
					$elem = $key.$numberOfLp.'_'.$numberOfDay;  // format is like lockBoxLp1_1
					// put value in settingsArray or update existing value
					$settingsArray[$elem] = $value;
				}  // end foreach
			}  // end foreach
		}  // end foreach

		// write config to file
  		$fp = fopen($myConfigFile, "w");
		if ( !$fp ) {
			throw new Exception('Konfigurationsdatei konnte nicht geschrieben werden.');
  		}
		foreach($settingsArray as $key => $value) {
			fwrite($fp, $key.'='.$value."\n");
		}
  		// send success write to config
	} catch ( Exception $e ) {
		$msg = $e->getMessage();
  		echo "<script type='text/javascript'>alert('$msg');</script>";
    } finally {
		fclose($fp);
		echo "<script>window.location.href='../index.php';</script>";
	}

?>
