<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$evufile = '/var/www/html/openWB/ramdisk/evu-live.graph';
$pvfile = '/var/www/html/openWB/ramdisk/pv-live.graph';
$evfile = '/var/www/html/openWB/ramdisk/ev-live.graph';
$timefile = '/var/www/html/openWB/ramdisk/time-live.graph';
$socfile = '/var/www/html/openWB/ramdisk/soc-live.graph';
if ($speichervorhanden == 1) {
	$speicherfile = '/var/www/html/openWB/ramdisk/speicher-live.graph';
}
if ($soc1vorhanden == 1) {
	$soc1file = '/var/www/html/openWB/ramdisk/soc1-live.graph';
}
$EV = file($evfile, FILE_IGNORE_NEW_LINES);
$EVU = file($evufile, FILE_IGNORE_NEW_LINES);
$PV = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$SOC = file($socfile, FILE_IGNORE_NEW_LINES);
if ($speichervorhanden == 1) {
	$SPEICHER = file($speicherfile, FILE_IGNORE_NEW_LINES);
}
if ($soc1vorhanden == 1) {
	$SOC1 = file($soc1file, FILE_IGNORE_NEW_LINES);
}
$myData = new pData();
$myData->addPoints($EV,"EV");
$myData->addPoints($EVU,"EVU");
$myData->addPoints($PV,"PV");
$myData->addPoints($SOC, "SoC");
if ($speichervorhanden == 1) {
	$myData->addPoints($SPEICHER, "Speicher");
}
if ($soc1vorhanden == 1) {
	$myData->addPoints($SOC1, "SoC LP2");
}
$highest1 = max($EVU);
$highest = max($EV);
$highest2 = max($PV);
$highest = max($highest,$highest1,$highest2);
$lowest = min($EVU);
$lowest1 = min($PV);
$lowest2 = min($EV);
if ($speichervorhanden == 1) {
$lowest3 = min($SPEICHER);
$loweste = min($lowest,$lowest1,$lowest2,$lowest3);
} else {
$loweste = min($lowest,$lowest1,$lowest2);
}
$myData->setSerieOnAxis("EV",0);
$myData->setSerieOnAxis("EVU",0);
$myData->setSerieOnAxis("PV",0);
if ($speichervorhanden == 1) {
	$myData->setSerieOnAxis("Speicher",0);
	$myData->setPalette("Speicher",array("R"=>252,"G"=>190,"B"=>50));
}
if ($soc1vorhanden == 1) {
	$myData->setSerieOnAxis("SoC LP2",1);
	$myData->setPalette("SoC LP2",array("R"=>0,"G"=>155,"B"=>237));
	$minsoc = min($SOC,$SOC1);
	$minsoc = min($minsoc);
	$maxsoc = max($SOC,$SOC1);
	$maxsoc = max($maxsoc);
	if ($maxsoc > 100) {
		$maxsoc = "100";
	}
} else {
	$minsoc = min($SOC);
	$minsoc = min($minsoc);
	$maxsoc = max($SOC);
	$maxsoc = max($maxsoc);
	if ($maxsoc > 100) {
		$maxsoc = "100";
	}
}
$myData->setSerieOnAxis("SoC",1);
$myData->setPalette("EV",array("R"=>51,"G"=>122,"B"=>183));
$myData->setPalette("SoC",array("R"=>0,"G"=>255,"B"=>237));
$myData->setPalette("EVU",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));

$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisPosition(1,AXIS_POSITION_RIGHT);

$myData->setAxisName(0,"Watt");
$AxisBoundaries = array(0=>array("Min"=>$loweste,"Max"=>$highest),1=>array("Min"=>($minsoc - "5" ),"Max"=>($maxsoc + "5" )));
$ScaleSettings  = array("DrawYLines"=>array(0),"GridR"=>128,"GridG"=>128,"GridB"=>128,"GridTicks"=>0,"GridAlpha"=>5,"DrawXLines"=>FALSE,"Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"LabelSkip"=>24);



$myImage = new pImage(1150, 200, $myData);

$myImage->setFontProperties(array(
    "FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
    "FontSize" => 18));
$myImage->setGraphArea(85,25, 1110,175);
$myImage->drawScale($ScaleSettings);
$myImage->drawLegend(240,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));
$myData->setSerieDrawable("PV",false);
$myData->setSerieDrawable("EVU",false);
if ($speichervorhanden == 1) {
	$myData->setSerieDrawable("Speicher",true);
}

$myImage->drawLineChart();
if ($speichervorhanden == 1) {
	$myData->setSerieDrawable("Speicher",false);
}
if ($soc1vorhanden == 1) {
	$myData->setSerieDrawable("SoC LP2",false);
}
$myData->setSerieDrawable("PV",true);
$myData->setSerieDrawable("EVU",true);
$myData->setSerieDrawable("SoC",false);
$myData->setSerieDrawable("EV",false);
$myImage->drawAreaChart();



header("Content-Type: image/png");
$myImage->autoOutput('/var/www/html/openWB/ramdisk/chart-m.png');
