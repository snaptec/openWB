function loadElectricityPriceChart() {
	var electricityPriceChartData = {
		labels: electricityPriceTimeline,
		datasets: [{
			label: 'Strompreis Cent/kWh',
			borderColor: "rgba(255, 155, 155, 0.9)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 2,
			fill: false,
			data: electricityPriceChartline,
			yAxisID: 'y-axis-1',
			steppedLine: true
		} ]
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
				yAxes: [
					{
						// horizontal line for values displayed on the left side (power)
						position: 'left',
						id: 'y-axis-1',
						type: 'linear',
						display: true,
						scaleLabel: {
						display: true,
						labelString: 'Preis Cent/kWh',
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
					},
						gridLines: {
							// light grey, opacy = 100% (visible)
							color: "rgba(204, 204, 204, 1)",
						},
						ticks: {
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						}

					}]
			}
		}
	});
}  // end loadgraph
