function loadElectricityPricechart(labels, dataPrice) {
	/**
	 * creates chart for price information
	 *
	 * @function loadElectricityPricechart
	 * @author Michael Ortenstein
	 * @param {array} labels is time
	 * @param {array} dataPrice is hourly price
	 */

	var ctxElectricityPricechart = $('#electricityPricechartCanvas')[0].getContext('2d');

	var config = {
		type: 'line',
		data: {
		  	labels: labels,
			datasets: [{
				yAxisID: 'y-axis-left',
				data: dataPrice,
				borderColor: 'rgba(201, 38, 38, 1)',
				backgroundColor: 'rgba(30, 33, 194, 0.7)',
				borderWidth: 2,
				fill: false,
				steppedLine: true
			}]
		},
		options: {
			tooltips: {
				enabled: true,
				mode: 'index',
				callbacks: {
					label: function(tooltipItem, data) {
						return tooltipItem.yLabel + ' ct/kWh';
					}
				}
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
							color: 'rgba(204, 204, 204, 0.3)',
						},

					ticks: {
							fontColor: 'rgba(153, 153, 153, 1)'
					}
				}],
				yAxes: [
					{
						// values displayed on the left side (price)
						position: 'left',
						id: 'y-axis-left',
						type: 'linear',
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'stündl. Preis [ct/kWh]',
							fontColor: 'rgba(153, 153, 153, 1)'
						},
						gridLines: {
							color: 'rgba(204, 204, 204, 1)',
						},
						ticks: {
							fontColor: 'rgba(153, 153, 153, 1)',
							fontSize: 15
						}

					}]
			}
		}
	};

	var electricityPricechart = new Chart(ctxElectricityPricechart, config);

}
