<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$monthdate = $_GET['thedate'];
//$monthdate = "2019";
//$monthdate = date("Y", strtotime($monthdate));
$ll1arf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-ll1.csv") as $filename) {
	$ll1ar = file($filename, FILE_IGNORE_NEW_LINES);
	$ll1arf = array_merge($ll1arf, $ll1ar);
}
$ll2arf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-ll2.csv") as $filename) {
	$ll2ar = file($filename, FILE_IGNORE_NEW_LINES);
	$ll2arf = array_merge($ll2arf, $ll2ar);
}
$ll3arf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-ll3.csv") as $filename) {
	$ll3ar = file($filename, FILE_IGNORE_NEW_LINES);
	$ll3arf = array_merge($ll3arf, $ll3ar);
}
$llgarf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-llg.csv") as $filename) {
	$llgar = file($filename, FILE_IGNORE_NEW_LINES);
	$llgarf = array_merge($llgarf, $llgar);
}
$pvarf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-pv.csv") as $filename) {
	$pvar = file($filename, FILE_IGNORE_NEW_LINES);
	$pvarf = array_merge($pvarf, $pvar);
}
$bezugarf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-bezug.csv") as $filename) {
	$bezugar = file($filename, FILE_IGNORE_NEW_LINES);
	$bezugarf = array_merge($bezugarf, $bezugar);
}
$einspeisungarf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-einspeisung.csv") as $filename) {
	$einspeisungar = file($filename, FILE_IGNORE_NEW_LINES);
	$einspeisungarf = array_merge($einspeisungarf, $einspeisungar);
}
$timefarf = array();
foreach (glob("/var/www/html/openWB/web/logging/data/monthly/".$monthdate."*-date.csv") as $filename) {
	$timefar = file($filename, FILE_IGNORE_NEW_LINES);
	$timefarf = array_merge($timefarf, $timefar);
}

$rll1 = $ll1arf;
$rll2 = $ll2arf;
$rll3 = $ll3arf;
$rllg = $llgarf;
$rpv = $pvarf;
$rbezug = $bezugarf;
$reinspeisung = $einspeisungarf;
$rtimef = array_reverse($timefarf);

$anzahl = count($timefarf);
for ($x = $anzahl - 1; $x > 0; $x--) {
	$bezugdiff[$x] = floor(($rbezug[$x-1] - $rbezug[$x]) * -1);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$timefk[$x] = substr($rtimef[$x], 6);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$pvdiff[$x] = floor(($rpv[$x-1] - $rpv[$x]) * -1);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$einspeisungdiff[$x] = floor(($reinspeisung[$x-1] - $reinspeisung[$x]) * -1);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$llgdiff[$x] = floor(($rllg[$x-1] - $rllg[$x]) * -1);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll1diff[$x] = floor(($rll1[$x-1] - $rll1[$x]) * -1);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll2diff[$x] = floor(($rll2[$x-1] - $rll2[$x]) * -1);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll3diff[$x] = floor(($rll3[$x-1] - $rll3[$x]) * -1);
}

for ($x = 0; $x < $anzahl; $x++){
	$line = $timefarf[$x] . "," . $bezugdiff[$x] . "," . $einspeisungdiff[$x] . "," . $llgdiff[$x] . "," . $pvdiff[$x] . "," . "0" . "," . "0" . "," . $ll1diff[$x] . "," . $ll2diff[$x]  . PHP_EOL;
	print($line);
}
