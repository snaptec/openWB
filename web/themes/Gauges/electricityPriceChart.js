function createPriceAnnotations(){
	// creates green annotation boxes for all times where price is <= maxPrice
	class Annotation {
		type = 'box';
		drawTime = "beforeDatasetsDraw"; // (default)
		xScaleID = 'x-axis-0';
		// left and right edge of the box, units are x-axis index
		// initially set to index found
		xMin = 0;
		xMax = 0;
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

function buildXLabel(value) {
	// builds a string like "morgen 13 Uhr" from timestamp
	var xLabelDate = new Date(value);  // date-object from timestamp
	var theDate = new Date();  // now
	var xLabel = xLabelDate.getHours() + ' Uhr';
	var datumIstHeute = xLabelDate.getYear() == theDate.getYear() && xLabelDate.getMonth() == theDate.getMonth() && xLabelDate.getDate() == theDate.getDate();
	if ( !datumIstHeute ) {
		theDate.setDate(theDate.getDate() + 1);  // set date to tomorrow
		if ( xLabelDate.getYear() == theDate.getYear() && xLabelDate.getMonth() == theDate.getMonth() && xLabelDate.getDate() == theDate.getDate() ) {
			xLabel = 'morgen ' + xLabel;
		} else {
			xLabel = xLabelDate.getDate() + '.' + xLabelDate.getMonth() + '.' + xLabelDate.getFullYear() + ', ' + xLabel;
		}
	}
	return xLabel;
}

function getXLabels(timestampLabels){
	// converts array of timestamps and returns converted array
	var labels = [];
	for (i=0; i<timestampLabels.length; i++) {
		labels.push(buildXLabel(timestampLabels[i]));
	}
	return labels;
}

function loadElectricityPriceChart() {
	var xLabels = getXLabels(electricityPriceTimeline);

	var electricityPriceChartData = {
		labels: xLabels,
		datasets: [{
			//yAxisID: 'y-axis-left',
			data: electricityPriceChartline,
			borderColor: evuCol,  // from liveChart
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 3,
			fill: false,
			steppedLine: true
		}]
	}

	var ctxElectricityPricechart = $('#electricityPriceChartCanvas')[0].getContext('2d');

	window.electricityPricechart = new Chart.Line(ctxElectricityPricechart, {
		data: electricityPriceChartData,
		options: {
			tooltips: {
				enabled: true,
				callbacks: {
					label: function(tooltipItem, data) {
						let i = tooltipItem.index;
						return data.datasets[0].data[i] + ' ct/kWh';
					},
					title: function(tooltipItem, data) {
						let i = tooltipItem[0].index;
						let title = 'jetzt';
						if ( i > 0 ) {
							title =  'ab ' + xLabels[i];
						}
						return title;
					}
				}
			},
			responsive: true,
			maintainAspectRatio: false,
			animation: false,
			legend: {
				display: false
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [{
					gridLines: {
						color: xgridCol  // from liveChart
					},
					ticks: {
						fontColor: tickCol  // from liveChart
					}
				}],
				yAxes: [{
					// values = price
					position: 'left',
					id: 'y-axis-left',
					type: 'linear',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Preis [ct/kWh]',
						fontColor: fontCol  // from liveChart
					},
					gridLines: {
						color: gridCol,  // from liveChart
						zeroLineColor: gridCol
					},
					ticks: {
						fontColor: tickCol,  // from liveChart
						maxTicksLimit: 7.1
					}
				}]
			},
			annotation: {
				annotations: createPriceAnnotations()
			}
		}
	});
}
