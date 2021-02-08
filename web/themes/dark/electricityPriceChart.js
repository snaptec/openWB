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

function loadElectricityPriceChart() {
	var electricityPriceChartData = {
		labels: electricityPriceTimeline,
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
							// verursacht ab und an fehlermeldung data property of undefinded
							let ticks = this._data.datasets[0]._meta[0].data[0]._chart.scales["x-axis-0"].ticks;
							title =  'ab ' + ticks[i];
						}
                        return title;
                    }
                }
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
					gridLines: {
						color: xgridCol  // from liveChart
					},
					ticks: {
						fontColor: tickCol,  // from liveChart
						callback: function(value, index) {
							var tickDate = new Date(value);
							console.log(value);
							var theDate = new Date();  // now
							var tick = tickDate.getHours() + ' Uhr';
							var datumIstHeute = tickDate.getYear() == theDate.getYear() && tickDate.getMonth() == theDate.getMonth() && tickDate.getDate() == theDate.getDate();
							if ( !datumIstHeute ) {
								theDate.setDate(theDate.getDate() + 1);  // set date to tomorrow
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
					// values = price
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
		        annotations: createPriceAnnotations(),
		        drawTime: "beforeDatasetsDraw" // (default)
		    }
		}
	});
}
