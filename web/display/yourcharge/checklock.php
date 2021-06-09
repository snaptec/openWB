<?php
$lines = file($_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf');
foreach ($lines as $line) {
	list($key, $value) = explode("=", $line, 2);
	${$key . "old"} = trim($value, " '\t\n\r\0\x0B"); // remove all garbage and single quotes
}

if (array_key_exists("pin", $_REQUEST)) {
	if ($_REQUEST["pin"] == $displaypincodeold) {
		echo "1";
	} else {
		echo "0";
	}
} elseif (array_key_exists("lock", $_REQUEST)) {
	echo $displaypinaktivold;
}
