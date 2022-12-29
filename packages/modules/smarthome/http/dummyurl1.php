<?php
$dec = $_REQUEST['d'];
$file = "/var/www/html/openWB/ramdisk/device" . $dec . "_req_relais";
if (is_file($file)) {
	$a = file_get_contents($file);
	if ($a == "1") {
		echo 100;
	} else { echo 0; }
} else { echo 0; }
?>
