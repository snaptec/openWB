<?php

$result = '';
$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf');
foreach($lines as $line) {
 	if(strpos($line, "displayaktiv=") !== false) {
		list(, $displayaktivold) = explode("=", $line);
	}
	if(strpos($line, "displaylp1max=") !== false) {
		list(, $displaylp1maxold) = explode("=", $line);
	}
	// if(strpos($line, "displaylp2max=") !== false) {
	// 	list(, $displaylp2maxold) = explode("=", $line);
	// }
	if(strpos($line, "rfidakt=") !== false) {
		list(, $rfidaktold) = explode("=", $line);
	}
	if(strpos($line, "isss=") !== false) {
		list(, $isssold) = explode("=", $line);
	}
}
?>
