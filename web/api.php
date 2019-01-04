<?php
if(isset($_GET["lademodus"])) {
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
}
if(isset($_GET["jetztll"])) {

	if($_GET["jetztll"] > "5" && $_GET["jetztll"] < "33") {

		$result = '';
		$lines = file('/var/www/html/openWB/openwb.conf');
		foreach($lines as $line) {
			if(strpos($line, "sofortll=") !== false) {
			    $result .= 'sofortll='.$_GET[jetztll]."\n";
			}
			else {
			    $result .= $line;
			}
		}
		file_put_contents('/var/www/html/openWB/openwb.conf', $result);

	}
}
if(isset($_GET["speicher"])) {
	if($_GET["speicher"]) {
		file_put_contents('/var/www/html/openWB/ramdisk/speicher', $_GET['speicher']);
	}
}
if(isset($_GET["get"])) {

	if($_GET["get"] == "all") {
		$json = array(
			"date"	=>	date('Y:m:d-H:i:s'),
			"lademodus"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/lademodus'))[0],
			"llsoll"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/llsoll'))[0],
			"restzeitlp1"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/restzeitlp1'))[0],
			"restzeitlp2"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/restzeitlp2'))[0],
			"restzeitlp3"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/restzeitlp3'))[0],
			"gelkwhlp1"	=>      explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/aktgeladen'))[0],
			"gelkwhlp2"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/aktgeladens1'))[0],
			"gelkwhlp3"	=>      explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/aktgeladens2'))[0],
			"gelrlp1"	=>      explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/gelrlp1'))[0],
			"gelrlp2"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/gelrlp2'))[0],
			"gelrlp3"	=>      explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/gelrlp3'))[0],
			"llgesamt"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/llkombiniert'))[0],
			"evua1"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/bezuga1'))[0],
			"evua2"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/bezuga2'))[0],
			"evua3"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/bezuga3'))[0],
			"lllp1"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/llaktuell'))[0],
			"lllp2"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/llaktuells1'))[0],
			"lllp3"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/llaktuells2'))[0],
			"evuw"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/wattbezug'))[0],
			"pvw"	=>	explode(PHP_EOL, file_get_contents('/var/www/html/openWB/ramdisk/pvwatt'))[0]

		);
		echo json_encode($json);
	}
}



?>
