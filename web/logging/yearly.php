<html>


<head>
	<script src="../js/core.js"></script>
	<script src="../js/charts.js"></script>
	<script src="../js/animated.js"></script>
	<script src="../js/jquery-1.11.1.min.js"></script>
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
	<link rel="stylesheet" type="text/css" href="../css/normalize.css">
	<link rel="stylesheet" type="text/css" href="../css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="../css/owl.css">
	<link rel="stylesheet" type="text/css" href="../css/animate.css">
	<link rel="stylesheet" type="text/css" href="../fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<link rel="stylesheet" type="text/css" href="../fonts/eleganticons/et-icons.css">
	<link rel="stylesheet" type="text/css" href="../css/cardio.css">
</head>


<body>


		 <ul class="nav nav-tabs">
			 <li><a href="../index.php?theme=<?php echo $_GET["theme"]?>">Zurück</a></li>
			 <li><a href="index.php?theme=<?php echo $_GET["theme"]?>">Live</a></li>
			 <li><a href="daily.php?theme=<?php echo $_GET["theme"]?>">Daily</a></li>
			 <li><a href="monthly.php?theme=<?php echo $_GET["theme"]?>">Monthly</a></li>
			 <li class="active"><a href="yearly.php?theme=<?php echo $_GET["theme"]?>">Yearly</a></li>
		 </ul>


<!--	<div class="preloader">
		<img src="../img/loader.gif" alt="Preloader image">
	</div> -->

<?php
$today = date('Y');
if (isset($_GET[date])) {
	$yeardate = $_GET[date];
	$_SESSION = $yeardate;
}
else
{
	$yeardate = $today;
	$_SESSION = $yeardate;
}

?>


	<div class="text-center">
		<br><h4> Yearly Graph</h4><br>
<br>...in development
	</div>
 <div style="height:600px;" id="chartdiv">
</div><br><br><br><br><br><br>
<form name="yearlydate" id="yearlydate" action="yearly.php" method="GET">
<div class="row col-xs-12">
	<div class="col-xs-2">
	</div>
	<div class="col-xs-8 block-center text-center .text-align:center">
<input id="date" name="date" type="year" min="2017" value="<?php print $yeardate ?>" required="required" />

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

</body>

<script>
am4core.useTheme(am4themes_animated);
// Create chart instance
var chart = am4core.create("chartdiv", am4charts.XYChart);
 chart.numberFormatter.numberFormat = "#.## a";
// Set up data source
chart.dataSource.url = "/openWB/web/logging/graph-yearlye.php?thedate=<?php echo $yeardate ?>";
chart.dataSource.parser = new am4core.CSVParser();
chart.dataSource.parser.options.useColumnNames = false;
//
// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "col0";

// Create value axis
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "kWh";
/*
valueAxis.adapter.add("getTooltipText", (text) => {
return text * 12 + "Watt";
});
 */
// Creaite series
var series1 = chart.series.push(new am4charts.ColumnSeries());
series1.dataFields.valueY = "col1";
series1.dataFields.categoryX = "col0";
series1.name = "Bezug";
series1.fill = am4core.color("#ff0000");
series1.stroke = am4core.color("#ff0000");
series1.strokeWidth = 3;
series1.tensionX = 0.8;
series1.tensionY = 0.8;
series1.strokeWidth = 1.5;
series1.fillOpacity = 0.3;
//series1.columns.template.tooltipText = "test";

var series2 = chart.series.push(new am4charts.ColumnSeries());
series2.dataFields.valueY = "col3";
series2.dataFields.categoryX = "col0";
series2.name = "LL Gesamt";
series2.stroke = am4core.color("#4074c9");
series2.tensionX = 0.8;
series2.tensionY = 0.8;
series2.strokeWidth = 1.5;
series2.fill = am4core.color("#4074c9");
series2.fillOpacity = 0.3;

var series4 = chart.series.push(new am4charts.ColumnSeries());
series4.dataFields.valueY = "col4";
series4.dataFields.categoryX = "col0";
series4.name = "PV";
series4.stroke = am4core.color("#00ff00");
series4.tensionX = 0.8;
series4.tensionY = 0.8;
series4.strokeWidth = 1.5;
series4.fill = am4core.color("#00ff00");
series4.fillOpacity = 0.3;

var series9 = chart.series.push(new am4charts.ColumnSeries());
series9.dataFields.valueY = "col2";
series9.dataFields.categoryX = "col0";
series9.name = "Einspeisung";
series9.stroke = am4core.color("#5d90e2");
series9.tensionX = 0.8;
series9.tensionY = 0.8;
series9.strokeWidth = 1.5;
series9.fill = am4core.color("#5d90e2");
series9.fillOpacity = 0.3;

var series5 = chart.series.push(new am4charts.ColumnSeries());
series5.dataFields.valueY = "col7";
series5.dataFields.categoryX = "col0";
series5.name = "LP 1";
series5.stroke = am4core.color("#845EC2");
series5.tensionX = 0.8;
series5.tensionY = 0.8;
series5.strokeWidth = 1.5;

var series6 = chart.series.push(new am4charts.ColumnSeries());
series6.dataFields.valueY = "col8";
series6.dataFields.categoryX = "col0";
series6.name = "LP 2";
series6.stroke = am4core.color("#aa5ec2");
series6.tensionX = 0.8;
series6.tensionY = 0.8;
series6.strokeWidth = 1.5;


chart.cursor = new am4charts.XYCursor();
chart.cursor.xAxis = categoryAxis;
chart.cursor.fullWidthLineX = true;
chart.cursor.lineX.strokeWidth = 0;
chart.cursor.lineX.fill = am4core.color("#003985");
chart.cursor.lineX.fillOpacity = 0.1;
// Add legend

//series4.customField = 12;
series1.legendSettings.valueText = "{valueY.sum}kWh";

series4.legendSettings.valueText = "{valueY.sum}kWh";
//series3.legendSettings.valueText = "{valueY.sum}kWh";
series2.legendSettings.valueText = "{valueY.sum}kWh";
series9.legendSettings.valueText = "{valueY.sum}kWh";
series5.legendSettings.valueText = "{valueY.sum}kWh";
series6.legendSettings.valueText = "{valueY.sum}kWh";
//series11.legendSettings.valueText = "{valueY.sum}kWh";


chart.legend = new am4charts.Legend();
</script>



</html>
