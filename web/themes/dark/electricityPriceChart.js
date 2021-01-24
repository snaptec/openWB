function createPriceAnnotations(){
	// creates annotation boxes for all times when price is <= maxPrice
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

function loadElectricityPriceChart() {
	var electricityPriceChartData = {
		labels: electricityPriceTimeline,
		datasets: [{
			yAxisID: 'y-axis-left',
			data: electricityPriceChartline,
			borderColor: "rgba(255, 155, 155, 0.9)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 2,
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
				xAxes: [
					{
					gridLines: {
							// light grey, opacy = 100% (visible)
							color: "rgba(204, 204, 204, 1)",
						},

					ticks: {
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
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
						labelString: 'Strompreis [Cent/kWh]',
						fontColor: "rgba(153, 153, 153, 1)"
					},
					gridLines: {
						color: "rgba(204, 204, 204, 1)",
					},
					ticks: {
						fontColor: "rgba(153, 153, 153, 1)"
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
