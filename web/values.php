<?php
// load openwb.conf
$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
foreach($lines as $line) {
	list($key, $value) = explode("=", $line, 2);
	${$key."old"} = trim( $value, " '\t\n\r\0\x0B" ); // remove all garbage and single quotes
}

$themeold = preg_replace('~[\r\n]+~', '', $themeold);

// load some ramdisk files
$lastregelungaktiv = file_get_contents('/var/www/html/openWB/ramdisk/lastregelungaktiv');
$lademodusold = file_get_contents('/var/www/html/openWB/ramdisk/lademodus');
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$verbraucher1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1vorhanden');
$verbraucher2vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2vorhanden');

$owbversion = file_get_contents('/var/www/html/openWB/web/version');

if (isset($_GET['theme'])) {
	$theme = $_GET['theme'];
	$_SESSION['theme'] = $theme;
} else {
	$theme = $themeold;
	$_SESSION['theme'] = $theme;
}

// convert lines to key/value array for faster manipulation
foreach($lines as $line) {
	// split line at char '='
	$splitLine = explode('=', $line);
	// trim parts
	$splitLine[0] = trim($splitLine[0]);
	$splitLine[1] = trim($splitLine[1]);
	// push key/value pair to new array
	$settingsArray[$splitLine[0]] = $splitLine[1];
}
// now values can be accessed by $settingsArray[$key] = $value;

$isConfiguredLp = array_fill(1, 8, false); // holds boolean for configured lp
// due to inconsitent variable naming need individual lines
$isConfiguredLp[1] = 1;  // lp1 always configured
$isConfiguredLp[2] = ($settingsArray['lastmanagement'] == 1) ? 1 : 0;
$isConfiguredLp[3] = ($settingsArray['lastmanagements2'] == 1) ? 1 : 0;
for ( $lp = 4  ; $lp <= 8; $lp++) {
	$isConfiguredLp[$lp] = ($settingsArray['lastmanagementlp'.$lp] == 1) ? 1 : 0;
}
$countLpConfigured = array_sum($isConfiguredLp);

// remove special characters from lp-names except space and underscore... maybe dangerous
for ( $lp = 1  ; $lp <= 8; $lp++) {
	$settingsArray['lp'.$lp.'name'] = preg_replace('/[^A-Za-z0-9_ ]/', '', $settingsArray['lp'.$lp.'name']);
}
?>
