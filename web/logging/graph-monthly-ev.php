<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$monthdate = $_GET['thedate'];
$monthdate = date("Ym", strtotime($monthdate));
$llgfile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-llg.csv';
$timefile = '/var/www/html/openWB/web/logging/data/monthly/'.$monthdate.'-date.csv';

$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$llg = file($llgfile, FILE_IGNORE_NEW_LINES);

$rllg = array_reverse($llg);
$rtimef = array_reverse($timef);

$anzahl = count($timef);
for ($x = $anzahl - 1; $x > 0; $x--) {
	$timefk[$x] = substr($rtimef[$x], 6);
}

for ($x = $anzahl - 1; $x > 0; $x--) {
	$llgdiff[$x] = floor(($rllg[$x-1] - $rllg[$x]) / 1000);
}

$myData = new pData();
$myData->addPoints($llgdiff,"EV");
$myData->setSerieOnAxis("EV",0);
$myData->setPalette("EV",array("R"=>51,"G"=>122,"B"=>183));
$myData->addPoints($timefk,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");

$myData->setAxisName(0,"kWh");
$AxisBoundaries = array(0=>array("Min"=>0,"Max"=>max($llgdiff)),1=>array("Min"=>0,"Max"=>100));
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
$myImage->autoOutput("monthly-ev.png");
