<html>


<head>
	<script src="../js/core.js"></script>
	<script src="../js/charts.js"></script>
	<script src="../js/animated.js"></script>
	<script src="../js/jquery-1.11.1.min.js"></script>
	<script src="../js/owl.carousel.min.js"></script>
	<script src="../js/bootstrap.min.js"></script>
	<script src="../js/wow.min.js"></script>
	<script src="../js/typewriter.js"></script>
	<script src="../js/jquery.onepagenav.js"></script>
	<script src="../js/main.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB Logging</title>
	<meta name="description" content="Control your charge" />
	<meta name="author" content="Kevin Wieland" />
	<link rel="apple-touch-icon" sizes="57x57" href="../img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="../img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="../img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="../img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="../img/favicons/manifest.json">
	<link rel="shortcut icon" href="../img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="../img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<meta http-equiv="refresh" content="600; URL=index.php">
	<link rel="stylesheet" type="text/css" href="../css/normalize.css">
	<link rel="stylesheet" type="text/css" href="../css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="../css/owl.css">
	<link rel="stylesheet" type="text/css" href="../css/animate.css">
	<link rel="stylesheet" type="text/css" href="../fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<link rel="stylesheet" type="text/css" href="../fonts/eleganticons/et-icons.css">
	<link rel="stylesheet" type="text/css" href="../css/cardio.css">
</head>
<?php
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		if(strpos($line, "graphinteractiveam=") !== false) {
			list(, $graphinteractiveamold) = explode("=", $line);
		}


		if(strpos($line, "grapham=") !== false) {
			list(, $graphamold) = explode("=", $line);
		}
					}
					?>

<body>


		 <ul class="nav nav-tabs">
			 <li><a href="../index.php">Zurück</a></li>
			 <li class="active"><a href="index.html">Live</a></li>
			 <li><a href="daily.php">Daily</a></li>
			 <li><a href="monthly.php">Monthly</a></li>
			 <li><a href="yearly.php">Yearly</a></li>
		 </ul>

	<div class="preloader">
		<img src="../img/loader.gif" alt="OpenWB loading...">
	</div>


<div class="row">
	<div class="text-center">
		<br><h3> OpenWB Logging</h3><br>
	</div>
</div>

	<?php if ($graphamold == 1) {
	echo '
<div style="border-left:solid transparent 30px; border-right:solid transparent 30px;">
	<div style="height:800px;" id="chartdiv"></div>
</div>';	
				   } else {
					   echo '

	<div class="row"> 
<div class="col-xs-12">
		<div class="imgwrapper">	
			<img src="./graph-live.php"
			alt="" class="center-block img-responsive" />
		</div>
	</div>
</div>
	'; } ?> 





	<script>


var graphinteractiveam = <?php echo $graphinteractiveamold ?>;


if ( graphinteractiveam == 1 ){
	am4core.useTheme(am4themes_animated);
}
// Create chart instance
var chart = am4core.create("chartdiv", am4charts.XYChart);

// Set up data source
chart.dataSource.url = "/openWB/ramdisk/all.graph";
chart.dataSource.parser = new am4core.CSVParser();
chart.dataSource.parser.options.useColumnNames = false;

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "col0";

// Create value axis
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "Watt";

var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis2.renderer.opposite = true;
valueAxis2.title.text = "% SoC";
valueAxis2.renderer.grid.template.disabled = true;
// Creaite series
var series1 = chart.series.push(new am4charts.LineSeries());
series1.dataFields.valueY = "col1";
series1.dataFields.categoryX = "col0";
series1.name = "Bezug";
series1.fill = am4core.color("#ff0000");
series1.stroke = am4core.color("#ff0000");
series1.strokeWidth = 3;
//series1.tensionX = 0.8;
//series1.tensionY = 0.8;
series1.strokeWidth = 1.5;
series1.fillOpacity = 0.3;


var series2 = chart.series.push(new am4charts.LineSeries());
series2.dataFields.valueY = "col2";
series2.dataFields.categoryX = "col0";
series2.name = "LL Gesamt";
series2.stroke = am4core.color("#4074c9");
//series2.tensionX = 10;
//series2.tensionY = 10;
series2.strokeWidth = 1.5;
series2.fill = am4core.color("#4074c9");
series2.fillOpacity = 0.3;

var series4 = chart.series.push(new am4charts.LineSeries());
series4.dataFields.valueY = "col3";
series4.dataFields.categoryX = "col0";
series4.name = "PV";
series4.stroke = am4core.color("#00ff00");
//series4.tensionX = 10;
//series4.tensionY = 10;
series4.strokeWidth = 1.5;
series4.fill = am4core.color("#00ff00");
series4.fillOpacity = 0.3;

var series5 = chart.series.push(new am4charts.LineSeries());
series5.dataFields.valueY = "col4";
series5.dataFields.categoryX = "col0";
series5.name = "LP 1";
series5.stroke = am4core.color("#845EC2");
//series5.tensionX = 10;
//series5.tensionY = 10;
series5.strokeWidth = 1.5;

var series6 = chart.series.push(new am4charts.LineSeries());
series6.dataFields.valueY = "col5";
series6.dataFields.categoryX = "col0";
series6.name = "LP 2";
series6.stroke = am4core.color("#aa5ec2");
//series6.tensionX = 10;
//series6.tensionY = 10;
series6.strokeWidth = 1.5;

var series3 = chart.series.push(new am4charts.LineSeries());
series3.dataFields.valueY = "col7";
series3.dataFields.categoryX = "col0";
series3.name = "Speicherleistung";
series3.stroke = am4core.color("#fcbe1e");
series3.fill = am4core.color("#fcbe1e");
series3.fillOpacity = 0.3;
//series3.tensionX = 10;
//series3.tensionY = 10;
series3.strokeWidth = 1.5;

var series7 = chart.series.push(new am4charts.LineSeries());
series7.dataFields.valueY = "col8";
series7.dataFields.categoryX = "col0";
series7.name = "Speicher SoC";
series7.stroke = am4core.color("#fcbe1e");
//series7.tensionX = 10;
//series7.tensionY = 10;
series7.strokeWidth = 1.5;
series7.yAxis = valueAxis2;

var series8 = chart.series.push(new am4charts.LineSeries());
series8.dataFields.valueY = "col9";
series8.dataFields.categoryX = "col0";
series8.name = "Lp1 SoC";
series8.stroke = am4core.color("#845EC2");
series8.strokeWidth = 1.5;
series8.yAxis = valueAxis2;

var series9 = chart.series.push(new am4charts.LineSeries());
series9.dataFields.valueY = "col10";
series9.dataFields.categoryX = "col0";
series9.name = "Lp2 SoC";
series9.stroke = am4core.color("#aa5ec2");
series9.strokeWidth = 1.5;
series9.yAxis = valueAxis2;


var series10 = chart.series.push(new am4charts.LineSeries());
series10.dataFields.valueY = "col11";
series10.dataFields.categoryX = "col0";
series10.name = "Hausverbrauch";
series10.stroke = am4core.color("#fefedf");
series10.strokeWidth = 2;



chart.cursor = new am4charts.XYCursor();



// Add scrollbar
// chart.scrollbarX = new am4charts.XYChartScrollbar();
// chart.scrollbarX.series.push(lineSeries);
// chart.scrollbarX.scrollbarChart.series.getIndex(0).xAxis.startLocation = 0.5;
// chart.scrollbarX.scrollbarChart.series.getIndex(0).xAxis.endLocation = 0.5;

// Add legend
chart.legend = new am4charts.Legend();

</script>






</body>
</html>






