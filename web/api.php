<?php

if($_GET["lademodus"] == "jetzt") {
	file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 0);
}

if($_GET["lademodus"] == "minundpv") {
	file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 1);
}
if($_GET["lademodus"] == "pvuberschuss") {
	file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 2);
}
if($_GET["lademodus"] == "stop") {
	file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 3);
}


if($_GET["jetztll"] > "10" && $_GET["jetztll"] < "32") {

	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		if(substr($line, 0, 9) == 'sofortll=') {
			$result .= 'sofortll='.$_GET['jetztll']."\n";
		} else {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);
}
if($_GET["speicher"]) {
	file_put_contents('/var/www/html/openWB/ramdisk/speicher', $_GET['speicher']);
}
?>
