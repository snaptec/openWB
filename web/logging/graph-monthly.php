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
	$bezugdiff[$x] = floor(($rbezug[$x-1] - $rbezug[$x]) / 1000);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$timefk[$x] = substr($rtimef[$x], 6);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$pvdiff[$x] = floor(($rpv[$x-1] - $rpv[$x]) / 1000);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$einspeisungdiff[$x] = floor(($reinspeisung[$x-1] - $reinspeisung[$x]) / 1000);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$llgdiff[$x] = floor(($rllg[$x-1] - $rllg[$x]) / 1000);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll1diff[$x] = floor(($rll1[$x-1] - $rll1[$x]) / 1000);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll2diff[$x] = floor(($rll2[$x-1] - $rll2[$x]) / 1000);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$ll3diff[$x] = floor(($rll3[$x-1] - $rll3[$x]) / 1000);
}

$myData = new pData();

$myData->addPoints($bezugdiff,"Bezug");
$myData->addPoints($einspeisungdiff,"Einspeisung");
$myData->addPoints($pvdiff,"PV");
//$myData->addPoints($ll1diff,"EV LP1");
//$myData->addPoints($ll2diff,"EV LP2");
//$myData->addPoints($ll3diff,"EV LP3");
$myData->addPoints($llgdiff,"EV");
 
$highest1 = max($pvdiff);
$highest = max($bezugdiff);
$highest2 = max($einspeisungdiff);
$highest = max($highest,$highest1,$highest2);

$myData->setSerieOnAxis("Bezug",0);
$myData->setSerieOnAxis("Einspeisung",0);
$myData->setSerieOnAxis("PV",0);
//$myData->setSerieOnAxis("EV LP1",0);
//$myData->setSerieOnAxis("EV LP2",0);
//$myData->setSerieOnAxis("EV LP3",0);
$myData->setSerieOnAxis("EV",0);

$myData->setSerieWeight("Bezug",1);
$myData->setSerieWeight("Einspeisung",1);
$myData->setPalette("Bezug",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("Einspeisung",array("R"=>0,"G"=>125,"B"=>125));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));
//$myData->setPalette("EV LP1",array("R"=>0,"G"=>0,"B"=>254));
//$myData->setPalette("EV LP2",array("R"=>0,"G"=>0,"B"=>254));
//$myData->setPalette("EV LP3",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EV",array("R"=>51,"G"=>122,"B"=>183));;
 
$myData->addPoints($timefk,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");

$myData->setAxisName(0,"kWh");
$AxisBoundaries = array(0=>array("Min"=>0,"Max"=>$highest),1=>array("Min"=>0,"Max"=>100));
$ScaleSettings  = array("DrawYLines"=>array(0),"GridR"=>128,"GridG"=>128,"GridB"=>128,"GridTicks"=>0,"GridAlpha"=>5,"DrawXLines"=>FALSE,"Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"Factors"=>array(10,20));

$myImage = new pImage(1150, 400, $myData);
$myImage->setFontProperties(array(
	"FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
	"FontSize" => 12));

$myImage->setGraphArea(105,25, 1095,375);

$myImage->drawScale($ScaleSettings);
$settings = array("DisplayPos"=>LABEL_POS_INSIDE, "DisplayValues"=>FALSE, "DisplayOrientation"=>ORIENTATION_VERTICAL, "Gradient"=>TRUE);
$myImage->drawBarChart($settings);
$myImage->drawLegend(360,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));

header("Content-Type: image/png");
$myImage->autoOutput("testa.png");
