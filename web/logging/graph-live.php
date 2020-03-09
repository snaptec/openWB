<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$evufile = '/var/www/html/openWB/ramdisk/evu.graph';
$pvfile = '/var/www/html/openWB/ramdisk/pv.graph';
$evfile = '/var/www/html/openWB/ramdisk/ev.graph';
$timefile = '/var/www/html/openWB/ramdisk/time.graph';
$socfile = '/var/www/html/openWB/ramdisk/soc.graph';
if ($soc1vorhanden == 1) {
	$soc1file = '/var/www/html/openWB/ramdisk/soc1.graph';
}
$EV = file($evfile, FILE_IGNORE_NEW_LINES);
$EVU = file($evufile, FILE_IGNORE_NEW_LINES);
$PV = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$SOC = file($socfile, FILE_IGNORE_NEW_LINES);
if ($speichervorhanden == 1) {
	$speicherfile = '/var/www/html/openWB/ramdisk/speicher.graph';
	$speichersocfile = '/var/www/html/openWB/ramdisk/speichersoc.graph';
}

$myData = new pData();
$myData->addPoints($EV,"EV");
$myData->addPoints($EVU,"EVU");
$myData->addPoints($PV,"PV");
$myData->addPoints($SOC, "SoC");
if ($speichervorhanden == 1) {
	$SPEICHER = file($speicherfile, FILE_IGNORE_NEW_LINES);
	$myData->addPoints($SPEICHER, "Speicher");
	$SPEICHERSOC = file($speichersocfile, FILE_IGNORE_NEW_LINES);
	$myData->addPoints($SPEICHERSOC, "Speicher SoC");
}
if ($soc1vorhanden == 1) {
	$SOC1 = file($soc1file, FILE_IGNORE_NEW_LINES);
	$myData->addPoints($SOC1, "SoC LP2");
}
$highest1 = max($EVU);
$highest = max($EV);
$highest2 = max($PV);
$highest = max($highest,$highest1,$highest2);
$lowestu = min($EVU);
$lowest = min($PV);
$soc1 = "0";
if ($speichervorhanden == 1) {
	$lowest = min($SPEICHER);
	$minsoc = min($SOC,$SPEICHERSOC);
	$soc1 = min($minsoc);
	$highestsoc = max($SOC,$SPEICHERSOC);
	$hsocmax = max($SOC);
	$hsocmaxx = max($SPEICHERSOC);
	$hsocmaxxx = max($hsocmax,$hsocmaxx);
} else {
	$socl = min($SOC);
	$hsocmaxxx = max($SOC);
}
$lowestg = min($lowest,$lowestu);

if ($soc1 < "0" ){
	$soc1 = "0";
}
if ($soc1vorhanden == 1) {
	$soc1max = max($SOC1);
	$hsocmaxxx = max($soc1max,$hsocmaxxx);
	$soc1min = min($SOC1);
	$soc1 = min($soc1min,$soc1);
	$myData->setSerieOnAxis("SoC LP2",1);
	$myData->setPalette("SoC LP2",array("R"=>0,"G"=>155,"B"=>237));
}
$myData->setSerieOnAxis("EV",0);
$myData->setSerieOnAxis("EVU",0);
$myData->setSerieOnAxis("PV",0);
$myData->setSerieOnAxis("SoC",1);
$myData->setPalette("EV",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EVU",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));
if ($speichervorhanden == 1) {
	$myData->setSerieOnAxis("Speicher",0);
	$myData->setPalette("Speicher",array("R"=>252,"G"=>190,"B"=>50));
	$myData->setSerieOnAxis("Speicher SoC",1);
	$myData->setPalette("Speicher SoC",array("R"=>152,"G"=>190,"B"=>50));
}
$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisPosition(1,AXIS_POSITION_RIGHT);
$myData->setAxisName(0,"kW");
$myData->setAxisDisplay(0,AXIS_FORMAT_CUSTOM,"YAxisFormat");

$AxisBoundaries = array(0=>array("Min"=>$lowestg,"Max"=>$highest),1=>array("Min"=>$soc1,"Max"=>$hsocmaxxx));
$ScaleSettings  = array("DrawYLines"=>array(0),"GridR"=>128,"GridG"=>128,"GridB"=>128,"GridTicks"=>0,"GridAlpha"=>10,"DrawXLines"=>FALSE,"Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"LabelSkip"=>100);
$myImage = new pImage(950, 400, $myData);
$myImage->setFontProperties(array(
	"FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
	"FontSize" => 16));
$myImage->setGraphArea(75,25, 895,375);
$myImage->drawScale($ScaleSettings);

$myData->setSerieDrawable("PV",false);
$myData->setSerieDrawable("EVU",false);
if ($speichervorhanden == 1) {
	$myData->setSerieDrawable("Speicher",true);
}
$myImage->drawLegend(260,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL, "Family"=>LEGEND_FAMILY_LINE));

$myImage->drawLineChart();
if ($speichervorhanden == 1) {
	$myData->setSerieDrawable("Speicher",false);
	$myData->setSerieDrawable("Speicher SoC",false);
}
if ($soc1vorhanden == 1) {
	$myData->setSerieDrawable("SoC LP2",false);
}
$myData->setSerieDrawable("SoC",false);
$myData->setSerieDrawable("PV",true);
$myData->setSerieDrawable("EV",false);
$myData->setSerieDrawable("EVU",true);
$myImage->drawAreaChart();

$myImage->drawLegend(160,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));

header("Content-Type: image/png");
$myImage->autoOutput('/var/www/html/openWB/ramdisk/chart-m.png');
function YAxisFormat($Value) { return(round($Value/1000,2)); } 
