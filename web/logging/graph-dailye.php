<?php
session_start();
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$verbraucher1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1vorhanden');
$verbraucher2vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2vorhanden');
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	if(strpos($line, "logdailywh=") !== false) {
		list(, $logdailywh) = explode("=", $line);
	}
	if(strpos($line, "logeinspeisungneg=") !== false) {
		list(, $logeinspeisungneg) = explode("=", $line);
	}
}
$today = date('Y-m-d');
if (isset($_GET['thedate'])) {
	$daydate1 = $_GET['thedate'];
} else {
	$daydate1 = $today;
}
$daydate = date("Ymd", strtotime($daydate1));
$ll1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll1.csv';
$ll2file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll2.csv';
$ll3file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll3.csv';
$llgfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-llg.csv';
$pvfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-pv.csv';
$bezugfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-bezug.csv';
$einspeisungfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-einspeisung.csv';
$timefile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-date.csv';
$socfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-soc.csv';
if ($speichervorhanden == 1) {
	$speicherifile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-speicheriwh.csv';
	$speicherefile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-speicherewh.csv';
	$speicheriwh = file($speicherifile, FILE_IGNORE_NEW_LINES);
	$speicherewh = file($speicherefile, FILE_IGNORE_NEW_LINES);
	$speichersocfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-speichersoc.csv';
	$speichersoc = file($speichersocfile, FILE_IGNORE_NEW_LINES);

	$firstsiwh = reset($speicheriwh);
	$lastsiwh = end($speicheriwh);
	$dailysiwh = number_format((($lastsiwh - $firstsiwh) / 1000), 2);
	$firstsewh = reset($speicherewh);
	$lastsewh = end($speicherewh);
	$dailysewh = number_format((($lastsewh - $firstsewh) / 1000), 2);
	$rspeicheriwh = $speicheriwh;
	$rspeicherewh = $speicherewh;
}
if ($soc1vorhanden == 1) {
	$soc1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-soc1.csv';
	$soc1 = file($soc1file, FILE_IGNORE_NEW_LINES);
}
if ($verbraucher1vorhanden == 1) {
	$verbraucher1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-verbraucher1.csv';
	$verbraucher1 = file($verbraucher1file, FILE_IGNORE_NEW_LINES);
	$firstviwh = reset($verbraucher1);
	$lastviwh = end($verbraucher1);
	$dailyviwh = number_format((($lastviwh - $firstviwh) / 1000), 2);
	$rverbraucher1 = $verbraucher1;
	$verbrauchere1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-verbrauchere1.csv';
	$verbrauchere1 = file($verbrauchere1file, FILE_IGNORE_NEW_LINES);
	$firstvewh = reset($verbrauchere1);
	$lastvewh = end($verbrauchere1);
	$dailyvewh = number_format((($lastvewh - $firstvewh) / 1000), 2);
	$rverbrauchere1 = $verbrauchere1;
}
if ($verbraucher2vorhanden == 1) {
	$verbraucher2file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-verbraucher2.csv';
	$verbraucher2 = file($verbraucher2file, FILE_IGNORE_NEW_LINES);
	$firstv2iwh = reset($verbraucher2);
	$lastv2iwh = end($verbraucher2);
	$dailyv2iwh = number_format((($lastv2iwh - $firstv2iwh) / 1000), 2);
	$rverbraucher2 = $verbraucher2;
	$verbrauchere2file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-verbrauchere2.csv';
	$verbrauchere2 = file($verbrauchere2file, FILE_IGNORE_NEW_LINES);
	$firstv2ewh = reset($verbrauchere2);
	$lastv2ewh = end($verbrauchere2);
	$dailyv2ewh = number_format((($lastv2ewh - $firstv2ewh) / 1000), 2);
	$rverbrauchere2 = $verbrauchere2;
}

$bezug = file($bezugfile, FILE_IGNORE_NEW_LINES);
$einspeisung = file($einspeisungfile, FILE_IGNORE_NEW_LINES);
$pv = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$ll1 = file($ll1file, FILE_IGNORE_NEW_LINES);
$ll2 = file($ll2file, FILE_IGNORE_NEW_LINES);
$ll3 = file($ll3file, FILE_IGNORE_NEW_LINES);
$llg = file($llgfile, FILE_IGNORE_NEW_LINES);
$soc = file($socfile, FILE_IGNORE_NEW_LINES);

$firstbezug = reset($bezug);
$lastbezug = end($bezug);
$dailybezug = number_format((($lastbezug - $firstbezug) / 1000), 2);

$firstev = reset($llg);
$lastev = end($llg);
$dailyev = number_format((($lastev - $firstev) / 1000), 2);

$firstpv = reset($pv);
$lastpv = end($pv);
$dailypv = number_format((($lastpv - $firstpv) / 1000), 2);

$firsteinspeisung = reset($einspeisung);
$lasteinspeisung = end($einspeisung);
$dailyeinspeisung = number_format((($lasteinspeisung - $firsteinspeisung) / 1000), 2);

$rll1 = $ll1;
$rll2 = $ll2;
$rll3 = $ll3;
$rllg = $llg;
$rpv = $pv;
$rbezug = $bezug;
$reinspeisung = $einspeisung;

$anzahl = count($timef);

if ($logdailywh == 1) {
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$bezugdiff[$x] = ($rbezug[$x-1] - $rbezug[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$pvdiff[$x] = ($rpv[$x-1] - $rpv[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$einspeisungdiff[$x] = ($reinspeisung[$x-1] - $reinspeisung[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$llgdiff[$x] = ($rllg[$x-1] - $rllg[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll1diff[$x] = ($rll1[$x-1] - $rll1[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll2diff[$x] = ($rll2[$x-1] - $rll2[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll3diff[$x] = ($rll3[$x-1] - $rll3[$x]) * -1;
	}
	if ($speichervorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$speicheriwhdiff[$x] = ($rspeicheriwh[$x-1] - $rspeicheriwh[$x]) * -1;
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$speicherewhdiff[$x] = ($rspeicherewh[$x-1] - $rspeicherewh[$x]) * -1;
		}
	}
	if ($verbraucher1vorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbraucher1diff[$x] = ($rverbraucher1[$x-1] - $rverbraucher1[$x]) * -1;
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbrauchere1diff[$x] = ($rverbrauchere1[$x-1] - $rverbrauchere1[$x]) * -1;
		}
	}
	if ($verbraucher2vorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbraucher2diff[$x] = ($rverbraucher2[$x-1] - $rverbraucher2[$x]) * -1;
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbrauchere2diff[$x] = ($rverbrauchere2[$x-1] - $rverbrauchere2[$x]) * -1;
		}
	}
} else {
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$bezugdiff[$x] = ($rbezug[$x-1] - $rbezug[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$pvdiff[$x] = ($rpv[$x-1] - $rpv[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		if ($logeinspeisungneg == 1) {
			$einspeisungdiff[$x] = $reinspeisung[$x-1] - $reinspeisung[$x];    
		} else {
			$einspeisungdiff[$x] = ($reinspeisung[$x-1] - $reinspeisung[$x]) * -1;
		}
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$llgdiff[$x] = ($rllg[$x-1] - $rllg[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll1diff[$x] = ($rll1[$x-1] - $rll1[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll2diff[$x] = ($rll2[$x-1] - $rll2[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll3diff[$x] = $rll3[$x-1] - $rll3[$x] * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$speicheriwhdiff[$x] = ($rspeicheriwh[$x-1] - $rspeicheriwh[$x]) * -1;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$speicherewhdiff[$x] = ($rspeicherewh[$x-1] - $rspeicherewh[$x]) * -1;
	}
	if ($verbraucher1vorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbraucher1diff[$x] = ($rverbraucher1[$x-1] - $rverbraucher1[$x]) * -1;
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbrauchere1diff[$x] = ($rverbrauchere1[$x-1] - $rverbrauchere1[$x]) * -1;
		}
	}
	if ($verbraucher2vorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbraucher2diff[$x] = ($rverbraucher2[$x-1] - $rverbraucher2[$x]) * -1;
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$verbrauchere2diff[$x] = ($rverbrauchere2[$x-1] - $rverbrauchere2[$x]) * -1;
		}
	}
}

for ($x = 0; $x < $anzahl; $x++){
	$line = $timef[$x] . "," . $bezugdiff[$x] . "," . $einspeisungdiff[$x] . "," . $llgdiff[$x] . "," . $pvdiff[$x] . "," . $speicheriwhdiff[$x] . "," . $speicherewhdiff[$x] . "," . $ll1diff[$x] . "," . $ll2diff[$x]  . "," . $soc[$x] . "," . $soc1[$x] . "," . $ll3diff[$x]  . "," . $speichersoc[$x] . "," . $verbraucher1diff[$x] . "," . $verbrauchere1diff[$x] . "," . $verbraucher2diff[$x] . "," . $verbrauchere2diff[$x] . PHP_EOL;
	print($line);
}
