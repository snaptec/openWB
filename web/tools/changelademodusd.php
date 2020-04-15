<?php
$returnPage = "Location: ../display.php";

if (isset($_GET['jetzt'])) {
	if ($_GET['jetzt'] == "1") {
		$config['lademodus'] = '0';
		file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 0);
		header($returnPage);
	}
}
if (isset($_GET['minundpv'])) {
	if ($_GET['minundpv'] == "1") {
		$config['lademodus'] = '1';
		file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 1);
		header($returnPage);
	}
}
if (isset($_GET['pvuberschuss'])) {
	if ($_GET['pvuberschuss'] == "1") {
		$config['lademodus'] = '2';
		file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 2);
		header($returnPage);
	}
}
if (isset($_GET['stop'])) {
	if ($_GET['stop'] == "1") {
		$config['lademodus'] = '3';
		file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 3);
		header($returnPage);
	}
}
if (isset($_GET['semistop'])) {
	if ($_GET['semistop'] == "1") {
		$config['lademodus'] = '4';
		file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 4);
		header($returnPage);
	}
}
if (isset($_GET['pveinbeziehen'])) {
	if ($_GET['pveinbeziehen'] == "0") {
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		$writeit = '0';
		if(strpos($line, "speicherpveinbeziehen=") !== false) {
			$result .= 'speicherpveinbeziehen=0'."\n";
			$writeit = '1';
		}
		if ($writeit == '0') {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);
	header($returnPage);
	}
	if ($_GET['pveinbeziehen'] == "1") {
		$result = '';
		$lines = file('/var/www/html/openWB/openwb.conf');
		foreach($lines as $line) {
			$writeit = '0';
			if(strpos($line, "speicherpveinbeziehen=") !== false) {
				$result .= 'speicherpveinbeziehen=1'."\n";
				$writeit = '1';
			}
			if ($writeit == '0') {
				$result .= $line;
			}
		}
		file_put_contents('/var/www/html/openWB/openwb.conf', $result);
		header($returnPage);
  }
}
/*
if (isset($_GET['sofortlllp1'])) {
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		$writeit = '0';
		if(strpos($line, "sofortll=") !== false) {
			$result .= 'sofortll='.$_GET['sofortlllp1']."\n";
			$writeit = '1';
		}
		if ($writeit == '0') {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);
}
 */
header($returnPage);
?>
