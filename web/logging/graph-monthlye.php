<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$monthdate = $_GET['thedate'];
$monthdate = date("Ym", strtotime($monthdate));
$ll1file = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-ll1.csv';
$ll2file = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-ll2.csv';
$ll3file = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-ll3.csv';
$llgfile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-llg.csv';
$pvfile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-pv.csv';
$bezugfile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-bezug.csv';
$einspeisungfile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-einspeisung.csv';
$timefile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-date.csv';

$bezug = file($bezugfile, FILE_IGNORE_NEW_LINES);
$einspeisung = file($einspeisungfile, FILE_IGNORE_NEW_LINES);
$pv = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$ll1 = file($ll1file, FILE_IGNORE_NEW_LINES);
$ll2 = file($ll2file, FILE_IGNORE_NEW_LINES);
$ll3 = file($ll3file, FILE_IGNORE_NEW_LINES);
$llg = file($llgfile, FILE_IGNORE_NEW_LINES);
$soc = file($socfile, FILE_IGNORE_NEW_LINES);

$rll1 = array_reverse($ll1);
$rll2 = array_reverse($ll2);
$rll3 = array_reverse($ll3);
$rllg = array_reverse($llg);
$rpv = array_reverse($pv);
$rbezug = array_reverse($bezug);
$reinspeisung = array_reverse($einspeisung);
$rtimef = array_reverse($timef);

$anzahl = count($timef);
for ($x = $anzahl - 1; $x > 0; $x--) {
	$bezugdiff[$x] = floor(($rbezug[$x-1] - $rbezug[$x]) );
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$timefk[$x] = substr($rtimef[$x], 6);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$pvdiff[$x] = floor(($rpv[$x-1] - $rpv[$x]));
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$einspeisungdiff[$x] = floor(($reinspeisung[$x-1] - $reinspeisung[$x]));
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$llgdiff[$x] = floor(($rllg[$x-1] - $rllg[$x]));
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll1diff[$x] = floor(($rll1[$x-1] - $rll1[$x]));
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll2diff[$x] = floor(($rll2[$x-1] - $rll2[$x]));
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll3diff[$x] = floor(($rll3[$x-1] - $rll3[$x]) );
}

for ($x = $anzahl; $x > 0; $x--){
	$line = $rtimef[$x] . "," . $bezugdiff[$x] . "," . $einspeisungdiff[$x] . "," . $llgdiff[$x] . "," . $pvdiff[$x] . "," . $speicheriwhdiff[$x] . "," . $speicherewhdiff[$x] . "," . $ll1diff[$x] . "," . $ll2diff[$x]  . PHP_EOL;
	print($line);
}
