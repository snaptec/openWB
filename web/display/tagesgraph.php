<!DOCTYPE html>
<html lang="en">

<head>
	<script src="../js/core.js"></script>
	<script src="../js/charts.js"></script>
	<!-- Normalize -->

	<link rel="stylesheet" type="text/css" href="../css/bootstrap.css">
	<!-- Elegant Icons -->
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="../css/pwa.css">
        <link rel="stylesheet" type="text/css" href="../fonts/eleganticons/et-icons.css">
        <!-- Main style -->
        <link rel="stylesheet" type="text/css" href="../css/cardio.css">
	<script src="../js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1 maximum-scale=1,user-scalable=0">
         <meta name="apple-mobile-web-app-capable" content="yes">
         <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
         <meta name="apple-mobile-web-app-title" content="OpenWB">
	<meta name="apple-mobile-web-app-status-bar-style" content="default">
	<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png"  />
	<link rel="apple-touch-startup-image" media="(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)" href="img/favicons/splash1125x2436w.png">
	<meta name="apple-mobile-web-app-title" content="OpenWB">
	<title>OpenWB</title>
	<meta name="description" content="OpenWB" />
	<meta name="keywords" content="OpenWB" />
	<meta name="author" content="Kevin Wieland" />
	<link rel="apple-touch-icon" sizes="72x72" href="img/favicons/apple-icon-72x72.png">
	<link rel="apple-touch-icon" sizes="76x76" href="img/favicons/apple-icon-76x76.png">
	<link rel="apple-touch-icon" sizes="114x114" href="img/favicons/apple-icon-114x114.png">
	<link rel="apple-touch-icon" sizes="120x120" href="img/favicons/apple-icon-120x120.png">
	<link rel="apple-touch-icon" sizes="144x144" href="img/favicons/apple-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="152x152" href="img/favicons/apple-icon-152x152.png">
	<link rel="apple-touch-icon" sizes="180x180" href="img/favicons/apple-icon-180x180.png">
	<link rel="icon" type="image/png" sizes="192x192"  href="img/favicons/android-icon-192x192.png">
	<link rel="icon" type="image/png" sizes="32x32" href="img/favicons/favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="96x96" href="img/favicons/favicon-96x96.png">
	<link rel="icon" type="image/png" sizes="16x16" href="img/favicons/favicon-16x16.png">
	<meta name="msapplication-TileColor" content="#ffffff">
	<meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="manifest" href="manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<link rel="apple-touch-startup-image" href="img/loader.gif">
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<meta name="google" content="notranslate">
	<!-- Main style -->


</head>
<style>
body {
background-color: black;
}
</style>
<?php
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		if(strpos($line, "grapham=") !== false) {
			list(, $graphamold) = explode("=", $line);
		}
		if(strpos($line, "graphinteractiveam=") !== false) {
			list(, $graphinteractiveamold) = explode("=", $line);
		}

		if(strpos($line, "lastmanagement=") !== false) {
			list(, $lastmanagementold) = explode("=", $line);
		}
		if(strpos($line, "lastmanagements2=") !== false) {
			list(, $lastmanagements2old) = explode("=", $line);
		}
		if(strpos($line, "verbraucher1_name=") !== false) {
			list(, $verbraucher1_nameold) = explode("=", $line);
		}
		if(strpos($line, "verbraucher2_name=") !== false) {
			list(, $verbraucher2_nameold) = explode("=", $line);
		}
		if(strpos($line, "verbraucher3_name=") !== false) {
			list(, $verbraucher3_nameold) = explode("=", $line);
		}



	}
	$speichervorhanden = file_get_contents('/var/www/html/openWB/ramdisk/speichervorhanden');
	$soc1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/soc1vorhanden');
	$verbraucher1vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher1vorhanden');
	$verbraucher2vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher2vorhanden');
	$verbraucher3vorhanden = file_get_contents('/var/www/html/openWB/ramdisk/verbraucher3vorhanden');
	$verbraucher1_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher1_nameold));
	$verbraucher2_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher2_nameold));
	$verbraucher3_nameold = trim(preg_replace('/\s+/', ' ', $verbraucher3_nameold));

					?>



<body>


<?php
	$today = date('Y-m-d');
	$daydate = $today;
?>

	<div style="height:440px;" id="dailydiv"></div>

<div class="row col-xs-12 text-center" style="font-size: 12px; height: 10px; top: 430px; left: 50px; position: absolute; width: 750px; color: white; text-align:center;"> 

	    <div class=" col-xs-10">
</div> 
        <div class=" col-xs-2"> 
		<a href="../display.php" class="btn btn-block btn-blue" style="height: 10px;">Zurück</a>
                </div> 
        </div> 														 
</div>

<!--
<form name="dailydate" id="dailydate" action="daily.php" method="GET">
<div class="row col-xs-12">
	<div class="col-xs-2">
	</div>
	<div class="col-xs-8 block-center text-center .text-align:center">
	<a href="daily.php?date=<?php print $daybefore ?>"><i class="fa fa-angle-left" style="font-size:48px;"></i></a>
	 &emsp;
<input id="date" name="date" type="date" min="2018-01-01" value="<?php print $daydate ?>" required="required" />
&emsp;

		<a href="daily.php?date=<?php print $nextday ?>"><i class="fa fa-angle-right" style="font-size:48px;"></i></a>
	</div>
	<div class="col-xs-2">
	</div>
</div>
<div class="row"><br></div><br>
<div class="row col-xs-12">
	<div class="col-xs-4">
	</div>
	<div class="col-xs-4 block-center text-center .text-align:center">
<button type="submit">Go</button>

	</div>
	<div class="col-xs-4">
	</div>
</div>



</form>
-->


</body>

<script>
	var lastmanagements2 = <?php echo $lastmanagements2old ?>;
	var lastmanagement = <?php echo $lastmanagementold ?>;
	var soc1vorhanden = <?php echo $soc1vorhanden ?>;
	var speichervorhanden = <?php echo $speichervorhanden ?>;
	var graphinteractiveam = <?php echo $graphinteractiveamold ?>;
	var verbraucher1vorhanden = <?php echo $verbraucher1vorhanden ?>;
	var verbraucher1name = "<?php echo $verbraucher1_nameold ?> (I)";
	var verbrauchere1name = "<?php echo $verbraucher1_nameold ?> (E)";
	var verbraucher2vorhanden = <?php echo $verbraucher2vorhanden ?>;
	var verbraucher2name = "<?php echo $verbraucher2_nameold ?> (I)";
	var verbrauchere2name = "<?php echo $verbraucher2_nameold ?> (E)";
	var verbraucher3vorhanden = <?php echo $verbraucher3vorhanden ?>;
	var verbraucher3name = "<?php echo $verbraucher3_nameold ?>";

if ( graphinteractiveam == 2 ){
	am4core.useTheme(am4themes_animated);
}
// Create chart instance
var chart = am4core.create("dailydiv", am4charts.XYChart);
 chart.numberFormatter.numberFormat = "#.## a";
// Set up data source
chart.dataSource.url = "/openWB/web/logging/graph-dailye.php?thedate=<?php echo $daydate ?>";
chart.dataSource.parser = new am4core.CSVParser();
chart.dataSource.parser.options.useColumnNames = false;
chart.dataSource.reloadFrequency = 120000;
//
// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "col0";
categoryAxis.renderer.labels.template.fill = am4core.color("white");
// Create value axis
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "[white]Wh[/]";


valueAxis.renderer.labels.template.fill = am4core.color("white");
valueAxis.adapter.add("getTooltipText", (text) => {
if (text.includes("k")) {
	text = text.substring(0, text.length -1);
	text = text * 12 * 1000;
	text = Math.round(text);
	text = text +"W";
} else {
	text = text * 12 + "W";
}

return text;
});


var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis2.renderer.opposite = true;
valueAxis2.title.text = "[white]% SoC";
valueAxis2.minimum = 0;
valueAxis2.maximum = 100;
valueAxis2.unit = "%";
valueAxis2.unitPosition = "right";
valueAxis2.strictMinMax = true;
valueAxis2.renderer.grid.template.disabled = true;
valueAxis2.renderer.labels.template.fill = am4core.color("white");
// Create series
var series1 = chart.series.push(new am4charts.LineSeries());
series1.dataFields.valueY = "col1";
series1.dataFields.categoryX = "col0";
series1.name = "EVU (I)";
series1.fill = am4core.color("#ff0000");
series1.stroke = am4core.color("#ff0000");
series1.strokeWidth = 3;
series1.tensionX = 0.8;
series1.tensionY = 0.8;
series1.strokeWidth = 1.5;
series1.fillOpacity = 0.3;

var series2 = chart.series.push(new am4charts.LineSeries());
series2.dataFields.valueY = "col3";
series2.dataFields.categoryX = "col0";
series2.name = "LL Gesamt";
series2.stroke = am4core.color("#4074c9");
series2.tensionX = 0.8;
series2.tensionY = 0.8;
series2.strokeWidth = 1.5;
series2.fill = am4core.color("#4074c9");
series2.fillOpacity = 0.3;

var series4 = chart.series.push(new am4charts.LineSeries());
series4.dataFields.valueY = "col4";
series4.dataFields.categoryX = "col0";
series4.name = "PV (E)";
series4.stroke = am4core.color("#00ff00");
series4.tensionX = 0.8;
series4.tensionY = 0.8;
series4.strokeWidth = 1.5;
series4.fill = am4core.color("#00ff00");
series4.fillOpacity = 0.3;

var series9 = chart.series.push(new am4charts.LineSeries());
series9.dataFields.valueY = "col2";
series9.dataFields.categoryX = "col0";
series9.name = "EVU (E)";
series9.stroke = am4core.color("#fff600");
series9.tensionX = 0.8;
series9.tensionY = 0.8;
series9.strokeWidth = 1.5;
series9.fill = am4core.color("#fff600");
series9.fillOpacity = 0.3;

if (speichervorhanden == 1) {
var series11 = chart.series.push(new am4charts.LineSeries());
series11.dataFields.valueY = "col5";
series11.dataFields.categoryX = "col0";
series11.name = "Speicher (I)";
series11.stroke = am4core.color("#fcbe1e");
series11.fill = am4core.color("#fcbe1e");
series11.fillOpacity = 0.3;
series11.tensionX = 0.8;
series11.tensionY = 0.8;
series11.strokeWidth = 1.5;
var series3 = chart.series.push(new am4charts.LineSeries());
series3.dataFields.valueY = "col6";
series3.dataFields.categoryX = "col0";
series3.name = "Speicher (E)";
series3.stroke = am4core.color("#fc6f1e");
series3.fill = am4core.color("#fc6f1e");
series3.fillOpacity = 0.3;
series3.tensionX = 0.8;
series3.tensionY = 0.8;
series3.strokeWidth = 1.5;
var series12 = chart.series.push(new am4charts.LineSeries());
series12.dataFields.valueY = "col12";
series12.dataFields.categoryX = "col0";
series12.name = "Speicher SoC";
series12.stroke = am4core.color("#fc6f1e");
series12.strokeWidth = 1.5;
series12.yAxis = valueAxis2;
series11.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
series3.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";



}
var series5 = chart.series.push(new am4charts.LineSeries());
series5.dataFields.valueY = "col7";
series5.dataFields.categoryX = "col0";
series5.name = "LP 1";
series5.stroke = am4core.color("#845EC2");
series5.tensionX = 0.8;
series5.tensionY = 0.8;
series5.strokeWidth = 1.5;
if ( lastmanagement == 1) {
var series6 = chart.series.push(new am4charts.LineSeries());
series6.dataFields.valueY = "col8";
series6.dataFields.categoryX = "col0";
series6.name = "LP 2";
series6.stroke = am4core.color("#aa5ec2");
series6.tensionX = 0.8;
series6.tensionY = 0.8;
series6.strokeWidth = 1.5;
series6.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";

}
if ( lastmanagements2 == 1) {
var series30 = chart.series.push(new am4charts.LineSeries());
series30.dataFields.valueY = "col11";
series30.dataFields.categoryX = "col0";
series30.name = "LP 3";
series30.stroke = am4core.color("#aa5ec2");
series30.tensionX = 0.8;
series30.tensionY = 0.8;
series30.strokeWidth = 1.5;

}
if ( verbraucher1vorhanden == 1) {
var series31 = chart.series.push(new am4charts.LineSeries());
series31.dataFields.valueY = "col13";
series31.dataFields.categoryX = "col0";
series31.name = verbraucher1name ;
series31.stroke = am4core.color("#bb5ec2");
series31.tensionX = 0.8;
series31.tensionY = 0.8;
series31.strokeWidth = 1.5;
series31.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
var series41 = chart.series.push(new am4charts.LineSeries());
series41.dataFields.valueY = "col14";
series41.dataFields.categoryX = "col0";
series41.name = verbrauchere1name ;
series41.stroke = am4core.color("#e01036");
series41.tensionX = 0.8;
series41.tensionY = 0.8;
series41.strokeWidth = 1.5;
series41.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
}
if ( verbraucher2vorhanden == 1) {
var series32 = chart.series.push(new am4charts.LineSeries());
series32.dataFields.valueY = "col15";
series32.dataFields.categoryX = "col0";
series32.name = verbraucher2name ;
series32.stroke = am4core.color("#fb5ec2");
series32.tensionX = 0.8;
series32.tensionY = 0.8;
series32.strokeWidth = 1.5;
series32.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
var series52 = chart.series.push(new am4charts.LineSeries());
series52.dataFields.valueY = "col16";
series52.dataFields.categoryX = "col0";
series52.name = verbrauchere2name ;
series52.stroke = am4core.color("#fb5ec2");
series52.tensionX = 0.8;
series52.tensionY = 0.8;
series52.strokeWidth = 1.5;
series52.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
}
if ( verbraucher3vorhanden == 1) {
var series33 = chart.series.push(new am4charts.LineSeries());
series33.dataFields.valueY = "col16";
series33.dataFields.categoryX = "col0";
series33.name = verbraucher3name ;
series33.stroke = am4core.color("#ebeec2");
series33.tensionX = 0.8;
series33.tensionY = 0.8;
series33.strokeWidth = 1.5;
series33.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";

}
var series8 = chart.series.push(new am4charts.LineSeries());
series8.dataFields.valueY = "col9";
series8.dataFields.categoryX = "col0";
series8.name = "Lp1 SoC";
series8.stroke = am4core.color("#845EC2");
//series8.tensionX = 0.8;
//series8.tensionY = 0.8;
series8.strokeWidth = 1.5;
series8.yAxis = valueAxis2;


if (soc1vorhanden == 1) {
var series10 = chart.series.push(new am4charts.LineSeries());
series10.dataFields.valueY = "col10";
series10.dataFields.categoryX = "col0";
series10.name = "Lp2 SoC";
series10.stroke = am4core.color("#aa5ec2");
//series9.tensionX = 0.8;
//series9.tensionY = 0.8;
series10.strokeWidth = 1.5;
series10.yAxis = valueAxis2;
}

chart.cursor = new am4charts.XYCursor();
// Add legend

series4.customField = 12;
series1.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
series4.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
series2.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
series9.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";
series5.legendSettings.valueText = "[{color} font-size: 10px]{valueY.sum}Wh[/]";

chart.legend = new am4charts.Legend();
chart.legend.labels.template.text = "[bold {color} font-size: 10px]{name}[/]";

chart.legend.markers.template.disabled = true;
chart.legend.position = "absolute";
</script>




</html>
