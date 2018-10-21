<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$evufile = '/var/www/html/openWB/ramdisk/evu.graph';
$pvfile = '/var/www/html/openWB/ramdisk/pv.graph';
$evfile = '/var/www/html/openWB/ramdisk/ev.graph';
$timefile = '/var/www/html/openWB/ramdisk/time.graph';

$EV = file($evfile, FILE_IGNORE_NEW_LINES);
$EVU = file($evufile, FILE_IGNORE_NEW_LINES);
$PV = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);


$myData = new pData();
$myData->addPoints($EV,"EV");
$myData->addPoints($EVU,"EVU");
$myData->addPoints($PV,"PV");


$highestu = max($EVU);
$highest = max($EV);
$highest = max($highest,$highestu);
$lowestu = min($EVU);
$lowest = min($PV);
$lowest = min($lowest,$lowestu);
$myData->setSerieOnAxis("EV",0);
$myData->setSerieOnAxis("EVU",0);
$myData->setSerieOnAxis("PV",0);
$myData->setPalette("EV",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EVU",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));

$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");

$myData->setAxisName(0,"Watt");
$AxisBoundaries = array(0=>array("Min"=>$lowest,"Max"=>$highest));
$ScaleSettings  = array("Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"LabelSkip"=>100);



$myImage = new pImage(900, 400, $myData);

$myImage->setFontProperties(array(
    "FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
    "FontSize" => 8));


$myImage->setGraphArea(65,25, 875,375);
$myImage->drawScale($ScaleSettings);

$myImage->drawLineChart();



header("Content-Type: image/png");
$myImage->Render('/var/www/html/openWB/ramdisk/chart-m.png');
