<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$evufile = '/var/www/html/openWB/ramdisk/evu-live.graph';
$pvfile = '/var/www/html/openWB/ramdisk/pv-live.graph';
$evfile = '/var/www/html/openWB/ramdisk/ev-live.graph';
$timefile = '/var/www/html/openWB/ramdisk/time-live.graph';
$socfile = '/var/www/html/openWB/ramdisk/soc-live.graph';

$EV = file($evfile, FILE_IGNORE_NEW_LINES);
$EVU = file($evufile, FILE_IGNORE_NEW_LINES);
$PV = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$SOC = file($socfile, FILE_IGNORE_NEW_LINES);

$myData = new pData();
$myData->addPoints($EV,"EV");
$myData->addPoints($EVU,"EVU");
$myData->addPoints($PV,"PV");
$myData->addPoints($SOC, "SoC");

$highest1 = max($EVU);
$highest = max($EV);
$highest2 = max($PV);
$highest = max($highest,$highest1,$highest2);
$lowestevu = min($EVU);
$lowestpv = min($PV);
$lowest = min($lowestevu,$lowestpv);
$myData->setSerieOnAxis("EV",0);
$myData->setSerieOnAxis("EVU",0);
$myData->setSerieOnAxis("PV",0);
$myData->setSerieOnAxis("SoC",1);
$myData->setPalette("EV",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EVU",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));

$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisPosition(1,AXIS_POSITION_RIGHT);

$myData->setAxisName(0,"Watt");
$AxisBoundaries = array(0=>array("Min"=>$lowest,"Max"=>$highest),1=>array("Min"=>(min($SOC) - "5" ),"Max"=>(max($SOC) + 5 )));
$ScaleSettings  = array("Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"LabelSkip"=>24);



$myImage = new pImage(650, 200, $myData);

$myImage->setFontProperties(array(
    "FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
    "FontSize" => 18));
$myImage->setGraphArea(85,25, 610,175);
$myImage->drawScale($ScaleSettings);

$myImage->drawLineChart();

$myImage->drawLegend(240,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));



header("Content-Type: image/png");
$myImage->autoOutput('/var/www/html/openWB/ramdisk/chart-m.png');
