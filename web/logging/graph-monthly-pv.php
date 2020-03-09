<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$monthdate = $_GET['thedate'];
$monthdate = date("Ym", strtotime($monthdate));
$pvfile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-pv.csv';
$timefile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-date.csv';

$pv = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$rpv = array_reverse($pv);
$rtimef = array_reverse($timef);

$anzahl = count($timef);

for ($x = $anzahl - 1; $x > 0; $x--) {
	$timefk[$x] = substr($rtimef[$x], 6);
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	$pvdiff[$x] = floor(($rpv[$x-1] - $rpv[$x]) / 1000);
}

$myData = new pData();
$myData->addPoints($pvdiff,"PV");
$myData->setSerieOnAxis("PV",0);
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));
$myData->addPoints($timefk,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisName(0,"kWh");
$AxisBoundaries = array(0=>array("Min"=>0,"Max"=>max($pvdiff)),1=>array("Min"=>0,"Max"=>100));
$ScaleSettings  = array("DrawYLines"=>array(0),"GridR"=>128,"GridG"=>128,"GridB"=>128,"GridTicks"=>0,"GridAlpha"=>5,"DrawXLines"=>FALSE,"Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"Factors"=>array(10,20));

$myImage = new pImage(1150, 400, $myData);
$myImage->setFontProperties(array(
	"FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
	"FontSize" => 12));

$myImage->setGraphArea(105,25, 1095,375);

$myImage->drawScale($ScaleSettings);
$settings = array("DisplayPos"=>LABEL_POS_INSIDE, "DisplayValues"=>TRUE, "DisplayOrientation"=>ORIENTATION_VERTICAL, "Gradient"=>TRUE);
$myImage->drawBarChart($settings);
$myImage->drawLegend(360,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));

header("Content-Type: image/png");
$myImage->autoOutput("testa.png");
