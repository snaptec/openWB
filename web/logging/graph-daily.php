<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";

$daydate = $_GET[thedate];
$ll1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll1.csv';
$ll2file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll2.csv';
$ll3file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll3.csv';
$llgfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-llg.csv';
$pvfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-pv.csv';
$bezugfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-bezug.csv';
$einspeisungfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-einspeisung.csv';
$timefile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-date.csv';
$socfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-soc.csv';


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

$anzahl = count($timef);
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $bezugdiff[$x] = $rbezug[$x-1] - $rbezug[$x];
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $pvdiff[$x] = $rpv[$x-1] - $rpv[$x];
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $einspeisungdiff[$x] = $reinspeisung[$x-1] - $reinspeisung[$x];
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $llgdiff[$x] = $rllg[$x-1] - $rllg[$x];
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $ll1diff[$x] = $rll1[$x-1] - $rll1[$x];
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $ll2diff[$x] = $rll2[$x-1] - $rll2[$x];
}
for ($x = $anzahl - 1; $x > 0; $x--) {
	    $ll3diff[$x] = $rll3[$x-1] - $rll3[$x];
}


$myData = new pData();

$myData->addPoints($bezugdiff,"Bezug");
$myData->addPoints($einspeisungdiff,"Einspeisung");
$myData->addPoints($pvdiff,"PV");
$myData->addPoints($ll1diff,"EV LP1");
$myData->addPoints($ll2diff,"EV LP2");
$myData->addPoints($ll3diff,"EV LP3");
$myData->addPoints($llgdiff,"EV");
$myData->addPoints($soc,"SoC");
 
$highest1 = max($pvdiff);
$highest = max($bezugdiff);
$highest2 = max($einspeisungdiff);
$highest = max($highest,$highest1,$highest2);

$myData->setSerieOnAxis("Bezug",0);
$myData->setSerieOnAxis("Einspeisung",0);
$myData->setSerieOnAxis("PV",0);
$myData->setSerieOnAxis("EV LP1",0);
$myData->setSerieOnAxis("EV LP2",0);
$myData->setSerieOnAxis("EV LP3",0);
$myData->setSerieOnAxis("EV",0);
$myData->setSerieOnAxis("SoC",1);

$myData->setSerieWeight("Bezug",1);
$myData->setSerieWeight("Einspeisung",1);
$myData->setPalette("Bezug",array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("Einspeisung",array("R"=>0,"G"=>125,"B"=>125));
$myData->setPalette("PV",array("R"=>0,"G"=>254,"B"=>0));
$myData->setPalette("EV LP1",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EV LP2",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EV LP3",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("EV",array("R"=>0,"G"=>0,"B"=>254));
$myData->setPalette("SoC",array("R"=>70,"G"=>70,"B"=>254));
 
$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisPosition(1,AXIS_POSITION_RIGHT);


$myData->setAxisName(0,"Wh");
$AxisBoundaries = array(0=>array("Min"=>0,"Max"=>$highest),1=>array("Min"=>0,"Max"=>100));
$ScaleSettings  = array("Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"LabelSkip"=>20);
 


$myImage = new pImage(950, 300, $myData);
$myImage->setFontProperties(array(
    "FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
    "FontSize" => 18));


$myImage->setGraphArea(75,25, 895,275);

$myImage->drawScale($ScaleSettings);

$myData->setSerieDrawable("Einspeisung",false);
$myData->setSerieDrawable("Bezug",false);
$myData->setSerieDrawable("PV",false);
$myImage->drawLineChart();

$myData->setSerieDrawable("SoC",false);
$myData->setSerieDrawable("PV",true);
$myData->setSerieDrawable("EV LP1",false);
$myData->setSerieDrawable("EV LP2",false);
$myData->setSerieDrawable("EV LP3",false);
$myData->setSerieDrawable("EV",false);
$myData->setSerieDrawable("Bezug",true);
$myData->setSerieDrawable("Einspeisung",true);
$myImage->drawAreaChart();
$myData->setSerieDrawable("EV",true);

$myImage->drawLegend(280,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));


$myData->setSerieDrawable("SoC",true);
$myData->setSerieDrawable("PV",false);
$myData->setSerieDrawable("EV LP1",false);
$myData->setSerieDrawable("EV LP2",false);
$myData->setSerieDrawable("EV LP3",false);
$myData->setSerieDrawable("EV",false);
$myData->setSerieDrawable("Bezug",false);
$myData->setSerieDrawable("Einspeisung",false);


$myImage->drawLegend(560,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL, "Family"=>LEGEND_FAMILY_LINE));


header("Content-Type: image/png");
$myImage->autoOutput("testa.png");
