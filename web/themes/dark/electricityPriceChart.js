function createPriceAnnotations(){
	// creates green annotation boxes for all times where price is <= maxPrice
	class Annotation {
		type = 'box';
		xScaleID = 'x-axis-0';
		yScaleID = 'y-axis-left';
		// left and right edge of the box, units are x-axis index
		// initially set to index found
		xMin = 0;
		xMax = 0;
		yMin = Math.floor(Math.min(...electricityPriceChartline));
		yMax = Math.ceil(Math.max(...electricityPriceChartline));
		borderColor = 'rgba(73, 238, 73, 0.3)';
		borderWidth = 2;
		backgroundColor = 'rgba(73, 238, 73, 0.3)';
		cornerRadius = 0;
	}
	var annotations = [];
	var maxPrice = parseFloat($('#MaxPriceForCharging').val());
	if ( !isNaN(maxPrice) ) {
		for ( var i = 0; i < electricityPriceChartline.length; i++ ) {
			if ( electricityPriceChartline[i] <= maxPrice ) {
				var newAnnotation = new Annotation();
				newAnnotation.xMin = i;  // set left edge of box
				while ( i < electricityPriceChartline.length && electricityPriceChartline[i] <= maxPrice ) {
					i++;
				}
				if ( i == electricityPriceChartline.length ) {
					// correct index if out of bounds
					i--;
				}
				newAnnotation.xMax = i;  // first index electricityPriceChartline[i] > maxPrice is right edge of box
				annotations.push(newAnnotation);  // add box to annotations
			}
		}
	}
	return annotations;
}

function formatTimeLabels(chart) {

}

function loadElectricityPriceChart() {
	var electricityPriceChartData = {
		labels: electricityPriceTimeline,
		datasets: [{
			yAxisID: 'y-axis-left',
			data: electricityPriceChartline,
			borderColor: evuCol,  // from liveChart
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 3,
			fill: false,
			steppedLine: true
		}]
	}
	var ctxElectricityPricechart = $('#electricityPriceChartCanvas')[0].getContext('2d');
	var priceAnnotations = createPriceAnnotations();


	window.electricityPricechart = new Chart.Line(ctxElectricityPricechart, {
		data: electricityPriceChartData,
		options: {
			tooltips: {
				enabled: true
			},
			responsive: true,
			maintainAspectRatio: false,
			animation: false,
			hover: {
				mode: 'null'
			},
			stacked: false,
			legend: {
				display: false
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [{
					type: 'time',
      				time: {
				        unit: 'hour',
				        unitStepSize: 1,
				        displayFormats: {
           					hour: "HH"
						}
        			},
					gridLines: {
						color: xgridCol  // from liveChart
					},
					ticks: {
						fontColor: tickCol,  // from liveChart
						callback: function(value, index, values) {
							var tick = value + ' Uhr';
							var tickDate = new Date(values[index].value);
							var theDate = new Date();
							if ( tickDate.getYear() == theDate.getYear() && tickDate.getMonth() == theDate.getMonth() && tickDate.getDate() == theDate.getDate() ) {
								tick = 'heute ' + tick;
							} else {
								theDate.setDate(theDate.getDate() + 1);  // now it is tomorrow
								if ( tickDate.getYear() == theDate.getYear() && tickDate.getMonth() == theDate.getMonth() && tickDate.getDate() == theDate.getDate() ) {
									tick = 'morgen ' + tick;
								} else {
									tick = tickDate.getDate() + '.' + tickDate.getMonth() + '.' + tickDate.getFullYear() + ', ' + tick;
								}
							}
							return tick;
						}
					}
				}],
				yAxes: [{
					// values price
					position: 'left',
					id: 'y-axis-left',
					type: 'linear',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Strompreis [ct/kWh]',
						fontColor: fontCol  // from liveChart
					},
					gridLines: {
						color: gridCol  // from liveChart
					},
					ticks: {
						fontColor: tickCol,  // from liveChart
						maxTicksLimit: 7.1
					}
				}]
			},
			annotation: {
		        annotations: priceAnnotations,
		        drawTime: "beforeDatasetsDraw" // (default)
		    }
		}
	});
}
