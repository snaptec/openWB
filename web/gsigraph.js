
am4core.useTheme(am4themes_animated);
// Create chart instance
var chart = am4core.create("gsidiv", am4charts.XYChart);
// Set up data source
chart.dataSource.url = "/openWB/ramdisk/gsiforecast.csv";
//}
chart.validateData();
chart.dataSource.parser = new am4core.CSVParser();
chart.dataSource.parser.options.useColumnNames = false;

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "col0";

// Create value axis
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "GSI";

var series1 = chart.series.push(new am4charts.LineSeries());
series1.dataFields.valueY = "col1";
series1.dataFields.categoryX = "col0";
series1.name = "gsi";
series1.fill = am4core.color("#ff0000");
series1.stroke = am4core.color("#ff0000");
series1.strokeWidth = 3;
series1.strokeWidth = 1.5;
series1.fillOpacity = 0.3;
// Add legend
