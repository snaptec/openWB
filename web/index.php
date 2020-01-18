<?php
	// check if forced theme is activated in config file
	$simplemodeold = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach( $lines as $line ) {
		if( strpos($line, "simplemode=") !== false ) {
			list(, $simplemodeold) = explode("=", $line);
		}
	}
	if ( $simplemodeold == 1 ) {
		// force hidden theme
		include 'themes/hidden/simplemode.php';
	} else {
		// theme set by cookie
		// check if theme cookie exists
		// then expand period of validity
		// else set standard theme
		if ( !(isset($_COOKIE['openWBTheme'] ) === true)) {
			setcookie('openWBTheme', 'standard', time()+(60*60*24*365*2));
			$_COOKIE['openWBTheme'] = 'standard';
		} else {
			$themeCookie = $_COOKIE['openWBTheme'];
			setcookie('openWBTheme', $themeCookie, time()+(60*60*24*365*2));
		}
		// check if theme exists
		// if not, set standard theme
		if ( is_dir('themes/'.$_COOKIE['openWBTheme']) == 0 ) {
			setcookie('openWBTheme', 'standard', time()+(60*60*24*365*2));
			$_COOKIE['openWBTheme'] = 'standard';
		}
		include 'themes/'.$_COOKIE['openWBTheme'].'/theme.html';
	}
?>
