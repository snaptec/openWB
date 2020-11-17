<?php
	// check if update.sh is still running
	$updateinprogress = file_get_contents($_SERVER['DOCUMENT_ROOT'] . '/openWB/ramdisk/updateinprogress');
	// check if atreboot.sh is still running
	$bootinprogress = file_get_contents($_SERVER['DOCUMENT_ROOT'] . '/openWB/ramdisk/bootinprogress');
	// if yes, show placeholder. If not, show theme
	if ( $bootinprogress == 1 or $updateinprogress == 1) {
		//atreboot.sh or update.sh still in progress, wait 5 seconds and retry
		include 'notready.html';
	} else {
		// load openwb.conf
		$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
		foreach($lines as $line) {
			list($key, $value) = explode("=", $line, 2);
			${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
		}

		// check for acknoledgement of dataprotection
		if ( $datenschutzackold == 0 && $clouduserold !== "leer") {
			// load dataprotection page
			include 'tools/datenschutz.html';
		} elseif ( !isset($wizzarddoneold) || ($wizzarddoneold < 100) ) {
			// load wizzard page
			include 'tools/wizzard.php';
		} elseif ( $isssold == 1 ) {
			// load chargepoint only page
			include 'isss.html';
		} else {
			// load normal UI
			// check if forced theme is activated in config file
			if ( isset($simplemodeold) && $simplemodeold == 1 ) {
				// force hidden theme
				?><!-- including themes/hidden/simplemode.php --><?php
				include 'themes/hidden/simplemode.php';
			} else {
				// check if theme cookie exists and theme is installed
				// else set standard theme
				if ( !(isset($_COOKIE['openWBTheme'] ) === true) || !(is_dir('themes/'.$_COOKIE['openWBTheme']) === true) ) {
					$_COOKIE['openWBTheme'] = 'standard';
				}
				// set theme by cookie and expand period of validity now + 2 years
				setcookie('openWBTheme', $_COOKIE['openWBTheme'], time()+(60*60*24*365*2));
				?><!-- including <?php echo 'themes/'.$_COOKIE['openWBTheme'].'/theme.html'; ?> --><?php
				include 'themes/'.$_COOKIE['openWBTheme'].'/theme.html';
			}
		}
	}
?>
