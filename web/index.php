<?php
	// check if update.sh is still running
	$updateinprogress = file_get_contents('/var/www/html/openWB/ramdisk/updateinprogress');
	// check if atreboot.sh is still running
	$bootinprogress = file_get_contents('/var/www/html/openWB/ramdisk/bootinprogress');
	// if yes, show placeholder. If not, show theme
	if ( $bootinprogress == 1 or $updateinprogress == 1) {
		//atreboot.sh or update.sh still in progress, wait 5 seconds and retry
		header( "refresh:5;url=index.php" );
		?>
<!DOCTYPE html>
<html lang="de">
	<head>
	</head>
	<body>
		<h4 style="text-align:center;">openWB ist noch nicht bereit</h4>
		<p style="text-align:center;">
			Der Vorgang kann länger dauern, bitte warten...<br>
 			Die Seite aktualisiert sich automatisch neu.
		</p>
	</body>
</html>
		<?php
	} else {
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
			?><!-- including themes/hidden/simplemode.php --><?php
			include 'themes/hidden/simplemode.php';
		} else {
			// theme set by cookie
			// check if theme cookie exists
			// then expand period of validity
			// else set standard theme
			if ( !(isset($_COOKIE['openWBTheme'] ) === true)) {
				setcookie('openWBTheme', 'standard', time()+(60*60*24*365*2));
				$_COOKIE['openWBTheme'] = 'standard';
				$themeCookie = 'standard';
			} else {
				$themeCookie = $_COOKIE['openWBTheme'];
				setcookie('openWBTheme', $themeCookie, time()+(60*60*24*365*2));
			}
			// check if theme exists
			// if not, set standard theme
			if ( is_dir('themes/'.$_COOKIE['openWBTheme']) == 0 ) {
				setcookie('openWBTheme', 'standard', time()+(60*60*24*365*2));
				$_COOKIE['openWBTheme'] = 'standard';
				$themeCookie = 'standard';
			}
			?><!-- including <?php echo 'themes/'.$_COOKIE['openWBTheme'].'/theme.html'; ?> --><?php
			include 'themes/'.$_COOKIE['openWBTheme'].'/theme.html';
		}
	}

?>
