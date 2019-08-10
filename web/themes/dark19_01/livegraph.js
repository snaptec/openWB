function setupAmCharts() {
    // nur wenn amCharts in Setup ausgewählt, hier einrichten
    if (document.getElementById("chartdiv")) {
        am4core.useTheme(am4themes_animated);
        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart);

        // Set up data source
        chart.dataSource.url = "/openWB/ramdisk/all-live.graph";
        chart.dataSource.incremental = true;
        chart.dataSource.keepCount = true;
        chart.dataSource.reloadFrequency = 10000;
        //}
        chart.validateData();
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
        var series1 = chart.series.push(new am4charts.LineSeries());
        series1.dataFields.valueY = "col1";
        series1.dataFields.categoryX = "col0";
        series1.name = "Bezug";
        series1.fill = am4core.color("#ff0000");
        series1.stroke = am4core.color("#ff0000");
        series1.strokeWidth = 3;
        series1.strokeWidth = 1.5;
        series1.fillOpacity = 0.3;


        var series2 = chart.series.push(new am4charts.LineSeries());
        series2.dataFields.valueY = "col2";
        series2.dataFields.categoryX = "col0";
        series2.name = "LL Gesamt";
        series2.stroke = am4core.color("#4074c9");
        series2.strokeWidth = 1.5;
        series2.fill = am4core.color("#4074c9");
        series2.fillOpacity = 0.3;

        var series4 = chart.series.push(new am4charts.LineSeries());
        series4.dataFields.valueY = "col3";
        series4.dataFields.categoryX = "col0";
        series4.name = "PV";
        series4.stroke = am4core.color("#00ff00");
        series4.strokeWidth = 1.5;
        series4.fill = am4core.color("#00ff00");
        series4.fillOpacity = 0.3;

        var series5 = chart.series.push(new am4charts.LineSeries());
        series5.dataFields.valueY = "col4";
        series5.dataFields.categoryX = "col0";
        series5.name = "LP 1";
        series5.stroke = am4core.color("#845EC2");
        series5.strokeWidth = 1.5;
        if ( lastmanagement == 1) {
            var series6 = chart.series.push(new am4charts.LineSeries());
            series6.dataFields.valueY = "col5";
            series6.dataFields.categoryX = "col0";
            series6.name = "LP 2";
            series6.stroke = am4core.color("#aa5ec2");
            series6.strokeWidth = 1.5;
        }
        if ( speichervorhanden == 1) {
            var series3 = chart.series.push(new am4charts.LineSeries());
            series3.dataFields.valueY = "col7";
            series3.dataFields.categoryX = "col0";
            series3.name = "Speicherleistung";
            series3.stroke = am4core.color("#fcbe1e");
            series3.fill = am4core.color("#fcbe1e");
            series3.fillOpacity = 0.3;
            series3.strokeWidth = 1.5;

            var series7 = chart.series.push(new am4charts.LineSeries());
            series7.dataFields.valueY = "col8";
            series7.dataFields.categoryX = "col0";
            series7.name = "Speicher SoC";
            series7.stroke = am4core.color("#fcbe1e");
            series7.strokeWidth = 1.5;
            series7.yAxis = valueAxis2;
        }

        var series8 = chart.series.push(new am4charts.LineSeries());
        series8.dataFields.valueY = "col9";
        series8.dataFields.categoryX = "col0";
        series8.name = "Lp1 SoC";
        series8.stroke = am4core.color("#845EC2");
        series8.strokeWidth = 1.5;
        series8.yAxis = valueAxis2;
        if (soc1vorhanden == 1) {
            var series9 = chart.series.push(new am4charts.LineSeries());
            series9.dataFields.valueY = "col10";
            series9.dataFields.categoryX = "col0";
            series9.name = "Lp2 SoC";
            series9.stroke = am4core.color("#aa5ec2");
            series9.strokeWidth = 1.5;
            series9.yAxis = valueAxis2;
        }

        var series10 = chart.series.push(new am4charts.LineSeries());
        series10.dataFields.valueY = "col11";
        series10.dataFields.categoryX = "col0";
        series10.name = "Hausverbrauch";
        series10.stroke = am4core.color("#fefedf");
        series10.strokeWidth = 2;

        if ( verbraucher1vorhanden == 1) {
            var series40 = chart.series.push(new am4charts.LineSeries());
            series40.dataFields.valueY = "col12";
            series40.dataFields.categoryX = "col0";
            series40.name = "Verbraucher 1";
            series40.stroke = am4core.color("#FFFF00");
            series40.strokeWidth = 1.5;
        }
        if ( verbraucher2vorhanden == 1) {
            var series41 = chart.series.push(new am4charts.LineSeries());
            series41.dataFields.valueY = "col13";
            series41.dataFields.categoryX = "col0";
            series41.name = "Verbraucher 1";
            series41.stroke = am4core.color("#FF00FF");
            series41.strokeWidth = 1.5;
        }
        //chart.cursor = new am4charts.XYCursor();

        // Add scrollbar
        // chart.scrollbarX = new am4charts.XYChartScrollbar();
        // chart.scrollbarX.series.push(lineSeries);
        // chart.scrollbarX.scrollbarChart.series.getIndex(0).xAxis.startLocation = 0.5;
        // chart.scrollbarX.scrollbarChart.series.getIndex(0).xAxis.endLocation = 0.5;

        // Add legend
        if ( chartlegend == 1 ) {
            chart.legend = new am4charts.Legend();
        }
    }
}

$(window).load(function() {
    // sobal die Seite vollständig geladen ist, Amchart
    // einrichten, falls in Setup ausgewählt
    setupAmCharts();
});
