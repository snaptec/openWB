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
		<link rel="stylesheet" type="text/css" href="css/settings_style.css">

		<!-- important scripts to be loaded -->
		<script src="js/jquery-3.6.0.min.js"></script>
		<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
		<!-- load helper functions -->
		<script src = "settings/helperFunctions.js?ver=20210329" ></script>
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
			<h1>Einstellungen werden gespeichert</h1>
			<div id="feedbackdiv" class="alert alert-info">
				Bitte warten ... <i class="fas fa-cog fa-spin"></i>
			</div>
		</div>  <!-- container -->

		<footer class="footer bg-dark text-light font-small">
			<div class="container text-center">
				<small>Sie befinden sich hier: System/Einstellungen</small>
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
			// only update settings already present in array
			if( array_key_exists( $key, $settingsArray ) ){
				// check if loaded config entry has single quotes
				if( (strpos( $settingsArray[$key], "'" ) === 0) && (strrpos( $settingsArray[$key], "'" ) === strlen( $settingsArray[$key])-1) ){
					$settingsArray[$key] = "'".$value."'";
				} else {
					$settingsArray[$key] = $value;
				}
			}
		}

		// write config to file
		$fp = fopen($myConfigFile, "w");
		if ( !$fp ) {
			throw new Exception('Konfigurationsdatei konnte nicht geschrieben werden.');
		}
		foreach($settingsArray as $key => $value) {
			// only save to config if $key has some meaningful length
			if( strlen($key) > 0 ){
				fwrite($fp, $key."=".$value."\n");
			}
		}
		fclose($fp);

		// handling of different actions required by some modules

		// check for manual ev soc module on lp1
		if( array_key_exists( 'socmodul', $_POST ) ){
			if( $_POST['socmodul'] == 'soc_manual' ){
				exec( 'mosquitto_pub -t openWB/lp/1/boolSocManual -r -m "1"' );
			} else {
				exec( 'mosquitto_pub -t openWB/lp/1/boolSocManual -r -m "0"' );
			}
		}
		// check for manual ev soc module on lp2
		if( array_key_exists( 'socmodul1', $_POST ) ){
			if( $_POST['socmodul1'] == 'soc_manuallp2' ){
				exec( 'mosquitto_pub -t openWB/lp/2/boolSocManual -r -m "1"' );
			} else {
				exec( 'mosquitto_pub -t openWB/lp/2/boolSocManual -r -m "0"' );
			}
		}

		// update display process if in POST data
		if( array_key_exists( 'displayaktiv', $_POST ) || array_key_exists( 'isss', $_POST) ){ ?>
			<script>$('#feedbackdiv').append("<br>Displays werden neu geladen.");</script>
			<?php
			exec( 'mosquitto_pub -t openWB/system/reloadDisplay -m "1"' );
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

		// start etprovider update if in POST data
		if( array_key_exists( 'etprovideraktiv', $_POST ) && ($_POST['etprovideraktiv'] == 1) ){ ?>
			<script>$('#feedbackdiv').append("<br>Update des Stromtarifanbieters gestartet.");</script>
			<?php
			exec( $_SERVER['DOCUMENT_ROOT'] . "/openWB/modules/" . $_POST['etprovider'] . "/main.sh > /var/log/openWB.log 2>&1 &" );
			exec( 'mosquitto_pub -t openWB/global/ETProvider/modulePath -r -m "' . $_POST['etprovider'] . '"' );
		}

		// start ev-soc updates if in POST data
		if( array_key_exists( 'socmodul', $_POST ) && ($_POST['socmodul'] != 'none') ){ ?>
			<script>$('#feedbackdiv').append("<br>Update SoC-Modul an Ladepunkt 1 gestartet.");</script>
			<?php
			file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/soctimer', "20005");
			exec( $_SERVER['DOCUMENT_ROOT'] . "/openWB/modules/" . $_POST['socmodul'] . "/main.sh > /dev/null &" );
		}
		if( array_key_exists( 'socmodul1', $_POST ) && ($_POST['socmodul1'] != 'none') ){ ?>
			<script>$('#feedbackdiv').append("<br>Update SoC-Modul an Ladepunkt 2 gestartet.");</script>
			<?php
			file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/soctimer1', "20005");
			exec( $_SERVER['DOCUMENT_ROOT'] . "/openWB/modules/" . $_POST['socmodul1'] . "/main.sh > /dev/null &" );
		}

	} catch ( Exception $e ) {
		$msg = $e->getMessage();
		echo "<script>alert('$msg');</script>";
	}

	// return to theme
	?>
		<script>
			window.setTimeout( function(){
				window.location.href='index.php';
			}, 3000);
		</script>
	<?php
?>
	</body>
</html>
