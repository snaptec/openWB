<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	if(strpos($line, "https=") !== false) {
		$result .= 'https='.$_POST['https']."\n";
		$writeit = '1';
	}
	if(strpos($line, "httpsCert=") !== false) {
		$result .= 'httpsCert='.$_POST['httpsCert']."\n";
		$writeit = '1';
	}

	if ( $writeit == '0') {
		$result .= $line;
	}
}

if ($_POST['https'] == '0') {
	if ($_POST['https'] !== $_POST['httpsold']) {
		shell_exec('../../runs/disableHttps.sh');
	}
}
else {
	if ($_POST['https'] !== $_POST['httpsold']) {
		if ($_POST['httpsCert'] == '0') {
			shell_exec('../../runs/createSelfSignedCertificate.sh ' . $_SERVER['HTTP_HOST']);
		}

		shell_exec('../../runs/enableHttps.sh');
	}
}

file_put_contents('/var/www/html/openWB/openwb.conf', $result);
file_put_contents('/var/www/html/openWB/ramdisk/reloaddisplay', "1");
file_put_contents('/var/www/html/openWB/ramdisk/execdisplay', "1");
$location = 'http://' . $_SERVER['HTTP_HOST'] . '/openWB/web/index.php';
header('Location: ' . $location);
?>
