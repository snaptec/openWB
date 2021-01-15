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

	var ctxa = $('#electricityPriceChartCanvas')[0].getContext('2d');

	window.AwattarLine = new Chart.Line(ctxa, {
		data: electricityPriceChartData,
		options: {
			tooltips: {
				enabled: true
			},
			responsive: true,
			maintainAspectRatio: false,
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
		        annotations: [{
		            type: 'line',
					id: 'maxPrice',
		            mode: 'horizontal',
		            scaleID: 'y-axis-left',
		            value: 32,
		            borderColor: 'rgba(73, 238, 73, 0.7)',
		            borderWidth: 2,
					label: {
				        backgroundColor: 'rgba(73, 238, 73, 0.6)',
				        font: {
				            // Font style of text, default below
				            style: "bold",
				            // Font color of text, default below
				            color: "rgba(20, 122, 20, 1)",
				        },
				        // Whether the label is enabled and should be displayed
				        enabled: true,
				        // Text to display in label - default is null. Provide an array to display values on a new line
				        content: "preiyslabel",
				        // Rotation of label, in degrees, or 'auto' to use the degrees of the line, default is 0
				        rotation: "auto"
				    }
		        }],
		        drawTime: "afterDatasetsDraw" // (default)
		    }
		}
	});
}
