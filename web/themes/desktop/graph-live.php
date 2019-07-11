<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$verbraucher1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1vorhanden');
$verbraucher2vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2vorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$evufile = '/var/www/html/openWB/ramdisk/evu-live.graph';
$pvfile = '/var/www/html/openWB/ramdisk/pv-live.graph';
$evfile = '/var/www/html/openWB/ramdisk/ev-live.graph';
$timefile = '/var/www/html/openWB/ramdisk/time-live.graph';
$socfile = '/var/www/html/openWB/ramdisk/soc-live.graph';
$ev1file = '/var/www/html/openWB/ramdisk/ev1-live.graph';
$verbraucher1_name = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1_name');
$verbraucher2_name = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2_name');

if ($speichervorhanden == 1) {
	$speicherfile = '/var/www/html/openWB/ramdisk/speicher-live.graph';
}
if ($soc1vorhanden == 1) {
	$ev2file = '/var/www/html/openWB/ramdisk/ev2-live.graph';
}
if ($verbraucher1vorhanden == 1) {
	$verbraucher1file = '/var/www/html/openWB/ramdisk/verbraucher1-live.graph';
	$VER1 = file($verbraucher1file, FILE_IGNORE_NEW_LINES);
}
if ($verbraucher2vorhanden == 1) {
	$verbraucher2file = '/var/www/html/openWB/ramdisk/verbraucher2-live.graph';
	$VER2 = file($verbraucher2file, FILE_IGNORE_NEW_LINES);
}
$EV = file($evfile, FILE_IGNORE_NEW_LINES);
$EV1 = file($ev1file, FILE_IGNORE_NEW_LINES);
$EVU = file($evufile, FILE_IGNORE_NEW_LINES);
$PV = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
if ($speichervorhanden == 1) {
	$SPEICHER = file($speicherfile, FILE_IGNORE_NEW_LINES);
}
if ($soc1vorhanden == 1) {
	$EV2 = file($ev2file, FILE_IGNORE_NEW_LINES);
}
$myData = new pData();
$myData->addPoints($EV,"EV");
$myData->addPoints($EV1,"EV1");
$myData->addPoints($EVU,"EVU");
$myData->addPoints($PV,"PV");
if ($speichervorhanden == 1) {
	$myData->addPoints($SPEICHER, "Speicher");
}
if ($soc1vorhanden == 1) {
	$myData->addPoints($EV2,"EV2");
}
if ($verbraucher1vorhanden == 1) {
	$myData->addPoints($VER1,$verbraucher1_name);
	$myData->setSerieOnAxis($verbraucher1_name,0);
	$myData->setPalette($verbraucher1_name,array("R"=>255,"G"=>202,"B"=>0));

}
if ($verbraucher2vorhanden == 1) {
	$myData->addPoints($VER2,$verbraucher2_name);
	$myData->setSerieOnAxis($verbraucher2_name,0);
	$myData->setPalette($verbraucher2_name,array("R"=>255,"G"=>0,"B"=>230));

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

$myData->setSerieOnAxis("EV1",0);
$myData->setSerieOnAxis("EV",0);
$myData->setSerieOnAxis("EVU",0);
$myData->setSerieOnAxis("PV",0);
if ($speichervorhanden == 1) {
	$myData->setSerieOnAxis("Speicher",0);
	$myData->setPalette("Speicher",array("R"=>122,"G"=>29,"B"=>29));
}
if ($soc1vorhanden == 1) {
	$myData->setSerieOnAxis("EV2",0);
	$myData->setPalette("EV2",array("R"=>51,"G"=>122,"B"=>83));
}

$myData->setPalette("EV",array("R"=>51,"G"=>122,"B"=>183));
$myData->setPalette("EV1",array("R"=>51,"G"=>122,"B"=>213));
$myData->setPalette("EVU",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));

$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisPosition(1,AXIS_POSITION_RIGHT);
$myData->setAxisName(0,"kW");
$myData->setAxisPosition(2,AXIS_POSITION_RIGHT);
$myData->setAxisDisplay(0,AXIS_FORMAT_CUSTOM,"YAxisFormat");

$AxisBoundaries = array(0=>array("Min"=>$loweste,"Max"=>$highest),1=>array("Min"=>$minsoc,"Max"=>$maxsoc));
$ScaleSettings  = array("DrawYLines"=>array(0),"GridR"=>128,"GridG"=>128,"GridB"=>128,"GridTicks"=>0,"GridAlpha"=>5,"DrawXLines"=>FALSE,"Mode"=>SCALE_MODE_MANUAL,
						"ManualScale"=>$AxisBoundaries,"LabelSkip"=>48);


$width = 950;
$height = 400;

$myImage = new pImage($width, $height, $myData, TRUE);
$myImage->setFontProperties(array(
    "FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
    "FontSize" => 18,"R"=>255,"G"=>255,"B"=>255));
$myImage->setGraphArea(70,25,940,375);
// set background gradient
//$Settings = array("StartR" => 221, "StartG" => 221, "StartB" => 221, "EndR" => 120, "EndG" => 120, "EndB" => 120, "Alpha" => 50);
//$myImage->drawGradientArea(0, 0, $width, $height, DIRECTION_VERTICAL, $Settings);

$myImage->drawScale($ScaleSettings);
$myImage->drawLegend(250,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));
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
}
if ($verbraucher1vorhanden == 1){
	$myData->setSerieDrawable("Verbraucher 1",false);
}
if ($verbraucher2vorhanden == 1){
	$myData->setSerieDrawable("Verbraucher 2",false);
}
$myData->setSerieDrawable("PV",true);
$myData->setSerieDrawable("EVU",true);
$myData->setSerieDrawable("EV",true);
$myData->setSerieDrawable("EV1",false);
$myData->setSerieDrawable("EV2",false);
$myImage->drawAreaChart();



header("Content-Type: image/png");
$myImage->autoOutput('/var/www/html/openWB/ramdisk/chart-m.png');
function YAxisFormat($Value) { return(round($Value/1000,2)); }
