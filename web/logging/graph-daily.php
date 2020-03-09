<?php
session_start();
require_once "/var/www/html/openWB/web/class/pDraw.class.php";
require_once "/var/www/html/openWB/web/class/pImage.class.php";
require_once "/var/www/html/openWB/web/class/pData.class.php";
$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	if(strpos($line, "logdailywh=") !== false) {
		list(, $logdailywh) = explode("=", $line);
	}
	if(strpos($line, "logeinspeisungneg=") !== false) {
		list(, $logeinspeisungneg) = explode("=", $line);
	}
}
$daydate1 = $_GET['thedate'];
$daydate = date("Ymd", strtotime($daydate1));
$ll1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll1.csv';
$ll2file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll2.csv';
$ll3file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll3.csv';
$llgfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-llg.csv';
$pvfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-pv.csv';
$bezugfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-bezug.csv';
$einspeisungfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-einspeisung.csv';
$timefile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-date.csv';
$socfile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-soc.csv';
if ($speichervorhanden == 1) {
	$speicherifile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-speicheriwh.csv';
	$speicherefile = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-speicherewh.csv';
	$speicheriwh = file($speicherifile, FILE_IGNORE_NEW_LINES);
	$speicherewh = file($speicherefile, FILE_IGNORE_NEW_LINES);
	$firstsiwh = reset($speicheriwh);
	$lastsiwh = end($speicheriwh);
	$dailysiwh = number_format((($lastsiwh - $firstsiwh) / 1000), 2);
	$firstsewh = reset($speicherewh);
	$lastsewh = end($speicherewh);
	$dailysewh = number_format((($lastsewh - $firstsewh) / 1000), 2);
	$rspeicheriwh = array_reverse($speicheriwh);
	$rspeicherewh = array_reverse($speicherewh);

}
if ($soc1vorhanden == 1) {
	$soc1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-soc1.csv';
	$soc1 = file($soc1file, FILE_IGNORE_NEW_LINES);
}

$bezug = file($bezugfile, FILE_IGNORE_NEW_LINES);
$einspeisung = file($einspeisungfile, FILE_IGNORE_NEW_LINES);
$pv = file($pvfile, FILE_IGNORE_NEW_LINES);
$timef = file($timefile, FILE_IGNORE_NEW_LINES);
$ll1 = file($ll1file, FILE_IGNORE_NEW_LINES);
$ll2 = file($ll2file, FILE_IGNORE_NEW_LINES);
$ll3 = file($ll3file, FILE_IGNORE_NEW_LINES);
$llg = file($llgfile, FILE_IGNORE_NEW_LINES);
$soc = file($socfile, FILE_IGNORE_NEW_LINES);

$firstbezug = reset($bezug);
$lastbezug = end($bezug);
$dailybezug = number_format((($lastbezug - $firstbezug) / 1000), 2);

$firstev = reset($llg);
$lastev = end($llg);
$dailyev = number_format((($lastev - $firstev) / 1000), 2);

$firstpv = reset($pv);
$lastpv = end($pv);
$dailypv = number_format((($lastpv - $firstpv) / 1000), 2);


$firsteinspeisung = reset($einspeisung);
$lasteinspeisung = end($einspeisung);
$dailyeinspeisung = number_format((($lasteinspeisung - $firsteinspeisung) / 1000), 2);

$rll1 = array_reverse($ll1);
$rll2 = array_reverse($ll2);
$rll3 = array_reverse($ll3);
$rllg = array_reverse($llg);
$rpv = array_reverse($pv);
$rbezug = array_reverse($bezug);
$reinspeisung = array_reverse($einspeisung);

$anzahl = count($timef);

if ($logdailywh == 1) {
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
	if ($speichervorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$speicheriwhdiff[$x] = $rspeicheriwh[$x-1] - $rspeicheriwh[$x];
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$speicherewhdiff[$x] = $rspeicherewh[$x-1] - $rspeicherewh[$x];
		}
	}
} else {
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$bezugdiff[$x] = $rbezug[$x-1] * 12 - $rbezug[$x] * 12;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$pvdiff[$x] = $rpv[$x-1] * 12 - $rpv[$x] * 12;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		if ($logeinspeisungneg == 1) {
			$einspeisungdiff[$x] = ($reinspeisung[$x-1] * 12 - $reinspeisung[$x] * 12) * -1;    
		} else {
			$einspeisungdiff[$x] = $reinspeisung[$x-1] * 12 - $reinspeisung[$x] * 12;
		}
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$llgdiff[$x] = $rllg[$x-1] * 12 - $rllg[$x] * 12;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll1diff[$x] = $rll1[$x-1] * 12 - $rll1[$x] * 12;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll2diff[$x] = $rll2[$x-1] * 12 - $rll2[$x] * 12;
	}
	for ($x = $anzahl - 1; $x > 0; $x--) {
		$ll3diff[$x] = $rll3[$x-1] * 12 - $rll3[$x] * 12;
	}
	if ($speichervorhanden == 1) {
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$speicheriwhdiff[$x] = $rspeicheriwh[$x-1] * 12 - $rspeicheriwh[$x] * 12;
		}
		for ($x = $anzahl - 1; $x > 0; $x--) {
			$speicherewhdiff[$x] = $rspeicherewh[$x-1] * 12 - $rspeicherewh[$x] * 12;
		}
	}
}

$myData = new pData();

$myData->addPoints($bezugdiff,"Bezug ".$dailybezug);
$myData->addPoints($einspeisungdiff,"Einspeisung ".$dailyeinspeisung);
$myData->addPoints($pvdiff,"PV ".$dailypv);
$myData->addPoints($ll1diff,"EV LP1");
$myData->addPoints($ll2diff,"EV LP2");
$myData->addPoints($ll3diff,"EV LP3");
$myData->addPoints($llgdiff,"EV ".$dailyev);
$myData->addPoints($soc,"SoC");
if ($speichervorhanden == 1) {
	$myData->addPoints($speicheriwhdiff,"Speicher Ladung ".$dailysiwh);
	$myData->addPoints($speicherewhdiff,"Speicher Entladung ".$dailysewh);
	$myData->setSerieOnAxis("Speicher Ladung ".$dailysiwh,0);
	$myData->setSerieOnAxis("Speicher Entladung ".$dailysewh,0);
	$myData->setPalette("Speicher Ladung ".$dailysiwh,array("R"=>252,"G"=>190,"B"=>50));
	$myData->setPalette("Speicher Entladung ".$dailysewh,array("R"=>190,"G"=>252,"B"=>50));
}
if ($soc1vorhanden == 1) {
	$myData->addPoints($soc1,"SoC LP2");
	$myData->setSerieOnAxis("SoC LP2",1);
	$myData->setPalette("SoC",array("R"=>120,"G"=>125,"B"=>254));
	$minsocc = min($soc);
	$minsocc1 = min($soc1);
	$minsoc = min($minsocc,$minsocc1);
	$socc = max($soc);
	$socc1 = max($soc1);
	$maxsoc = max($socc,$socc1);
} else {
	$socl = (min($soc) - 5);
	if ($socl < "0" ){
		$minsoc = 0;
	} else {
		$minsoc = $socl;
	}
	$maxsoc = max($soc);
}	
$lowest = min($einspeisungdiff);
if ($lowest > 0){
	$lowest = 0;
}
$highest1 = max($pvdiff);
$highest = max($bezugdiff);
$highest2 = max($einspeisungdiff);
$highest = max($highest,$highest1,$highest2);

$myData->setSerieonAxis("Bezug ".$dailybezug,0);
$myData->setSerieOnAxis("Einspeisung ".$dailyeinspeisung,0);
$myData->setSerieOnAxis("PV ".$dailypv,0);
$myData->setSerieOnAxis("EV LP1",0);
$myData->setSerieOnAxis("EV LP2",0);
$myData->setSerieOnAxis("EV LP3",0);
$myData->setSerieOnAxis("EV ".$dailyev,0);
$myData->setSerieOnAxis("SoC",1);
 
$myData->setSerieWeight("Bezug ".$dailybezug,1);
$myData->setSerieWeight("Einspeisung ".$dailyeinspeisung,1);
$myData->setPalette("Bezug ".$dailybezug,array("R"=>254,"G"=>0,"B"=>0));
$myData->setPalette("Einspeisung ".$dailyeinspeisung,array("R"=>0,"G"=>125,"B"=>125));
$myData->setPalette("PV ".$dailypv,array("R"=>0,"G"=>254,"B"=>0));
$myData->setPalette("EV LP1",array("R"=>51,"G"=>122,"B"=>183));
$myData->setPalette("EV LP2",array("R"=>51,"G"=>122,"B"=>183));
$myData->setPalette("EV LP3",array("R"=>51,"G"=>122,"B"=>183));
$myData->setPalette("EV ".$dailyev,array("R"=>51,"G"=>122,"B"=>183));
$myData->setPalette("SoC",array("R"=>70,"G"=>70,"B"=>254));
$myData->addPoints($timef,"Labels");
$myData->setSerieOnAxis("Labels",0);
$myData->setSerieDescription("Labels","Uhrzeit");
$myData->setAbscissa("Labels");
$myData->setAxisPosition(1,AXIS_POSITION_RIGHT);

if ($logdailywh == 1) {
	$myData->setAxisName(0,"Wh");
} else {
	$myData->setAxisName(0,"kW");
	$myData->setAxisDisplay(0,AXIS_FORMAT_CUSTOM,"YAxisFormat");
}
$myData->setAxisName(1,"SoC");

$AxisBoundaries = array(0=>array("Min"=>$lowest,"Max"=>$highest),1=>array("Min"=>$minsoc,"Max"=>$maxsoc));
$ScaleSettings  = array("DrawYLines"=>array(0),"GridR"=>128,"GridG"=>128,"GridB"=>128,"GridTicks"=>0,"GridAlpha"=>10,"DrawXLines"=>FALSE,"Mode"=>SCALE_MODE_MANUAL,"ManualScale"=>$AxisBoundaries,"LabelSkip"=>20);

$myImage = new pImage(1000, 300, $myData);
$myImage->setFontProperties(array(
	"FontName" => "/var/www/html/openWB/web/fonts/GeosansLight.ttf",
	"FontSize" => 18));

$myImage->setGraphArea(95,25, 895,275);

$myImage->drawScale($ScaleSettings);

$myData->setSerieDrawable("Einspeisung ".$dailyeinspeisung,false);
$myData->setSerieDrawable("Bezug ".$dailybezug,false);
$myData->setSerieDrawable("PV ".$dailypv,false);
$myImage->drawLineChart();
if ($speichervorhanden == 1) {
	$myData->setSerieDrawable("Speicher Ladung ".$dailysiwh,false);
	$myData->setSerieDrawable("Speicher Entladung ".$dailysewh,false);
}
if ($soc1vorhanden == 1) {
	$myData->setSerieDrawable("SoC LP2",false);
}
$myData->setSerieDrawable("SoC",false);
$myData->setSerieDrawable("PV ".$dailypv,true);
$myData->setSerieDrawable("EV LP1",false);
$myData->setSerieDrawable("EV LP2",false);
$myData->setSerieDrawable("EV LP3",false);
$myData->setSerieDrawable("EV ".$dailyev,false);
$myData->setSerieDrawable("Bezug ".$dailybezug,true);
$myData->setSerieDrawable("Einspeisung ".$dailyeinspeisung,true);
$myImage->drawAreaChart();
$myData->setSerieDrawable("EV ".$dailyev,true);

$myImage->drawLegend(325,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL));

if ($soc1vorhanden == 1) {
	$myData->setSerieDrawable("SoC LP2",true);
}
$myData->setSerieDrawable("SoC",true);
$myData->setSerieDrawable("PV ".$dailypv,false);
$myData->setSerieDrawable("EV LP1",false);
$myData->setSerieDrawable("EV LP2",false);
$myData->setSerieDrawable("EV LP3",false);
$myData->setSerieDrawable("EV ".$dailyev,false);
$myData->setSerieDrawable("Bezug ".$dailybezug,false);
$myData->setSerieDrawable("Einspeisung ".$dailyeinspeisung,false);

$myImage->drawLegend(170,12,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL, "Family"=>LEGEND_FAMILY_LINE));
if ($speichervorhanden == 1) {
	if ($soc1vorhanden == 1) {
		$myData->setSerieDrawable("SoC LP2",false);
	}
	$myData->setSerieDrawable("Speicher Ladung ".$dailysiwh,true);
	$myData->setSerieDrawable("Speicher Entladung ".$dailysewh,true);
	$myData->setSerieDrawable("SoC",false);
	$myData->setSerieDrawable("PV ".$dailypv,false);
	$myData->setSerieDrawable("EV LP1",false);
	$myData->setSerieDrawable("EV LP2",false);
	$myData->setSerieDrawable("EV LP3",false);
	$myData->setSerieDrawable("EV ".$dailyev,false);
	$myData->setSerieDrawable("Bezug ".$dailybezug,false);
	$myData->setSerieDrawable("Einspeisung ".$dailyeinspeisung,false);
	$myImage->drawLegend(220,42,array("Style"=>LEGEND_NOBORDER,"Mode"=>LEGEND_HORIZONTAL, "Family"=>LEGEND_FAMILY_LINE));
}

header("Content-Type: image/png");
$myImage->autoOutput("testa.png");
function YAxisFormat($Value) { return(round($Value/1000,2)); } 
