<?php

	// writes settings from autolock-page via POST-request to config file
	// author: M. Ortenstein

	// first read config-lines in array
	$settingsFile = file('/var/www/html/openWB/web/tools/debugfilewithlotofstuff.txt');
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

	try {
		$myFile = "/var/www/html/openWB/web/tools/debugfilewithlotofstuff.txt";

  		if ( !file_exists($myFile) ) {
  			throw new Exception('Konfigurationsdatei nicht gefunden.');
  		}
  		$fp = fopen($myFile, "w");
		if ( !$fp ) {
			throw new Exception('Konfigurationsdatei konnte nicht geöffnet werden.');
  		}
		$settingsFile = [];  // empty the file array
		foreach($settingsArray as $key => $value) {
			fwrite($fp, $key.' = '.$value."\n");
		}
  		fclose($fp);
  		// send success write to config
	} catch ( Exception $e ) {
  		echo "<script type='text/javascript'>alert('$e');</script>";
    }
	echo "<script>window.location.href='../index.php';</script>";
	
?>
