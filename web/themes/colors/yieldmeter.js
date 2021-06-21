/**
 * Show the daily yield and consumption in a bar graph
 *
 * @author Claus Hagen
 */

class YieldMeter {
	bardata;
	xScale;
	yScale;
	svg;

	constructor() {
		this.width = 500;
		this.height = 500;
		this.margin = {
			top: 25, bottom: 30, left: 25, right: 0
		};
		this.labelfontsize = 16;
		this.axisFontSize = 12;
	}

	// to be called when the document is loaded
	init() {
		const figure = d3.select("figure#energymeter");
		this.svg = figure.append("svg")
			.attr("viewBox", `0 0 500 500`);
		const style = getComputedStyle(document.body);
		this.houseColor = 'var(--color-house)';
		this.pvColor = 'var(--color-pv)';
		this.exportColor = 'var(--color-export)';
		this.evuColor = 'var(--color-evu)';
		this.bgColor = 'var(--color-bg)';
		this.chargeColor = 'var(--color-charging)';
		this.axisColor = 'var(--color-axis)';
		this.gridColor = 'var(--color-grid)';
   	d3.select("button#energyLeftButton")
			.on("click", shiftLeft)
		d3.select("button#energyRightButton")
			.on("click", shiftRight)
			d3.select("button#calendarButton")
			.on("click", toggleMonthView)	
	}

	// to be called when values have changed
	update() {
		switch (wbdata.graphMode) {
			case 'live':
				this.plotdata = Object.values(wbdata.sourceSummary)
				.filter((row) => (row.energy > 0))
				.concat(wbdata.usageDetails
					.filter((row) => (row.energy > 0)));
				break;
			case 'day':
				if (wbdata.showTodayGraph) {
					this.plotdata = Object.values(wbdata.sourceSummary)
						.filter((row) => (row.energy > 0))
						.concat(wbdata.usageDetails
							.filter((row) => (row.energy > 0)));			
				} else {
					this.plotdata = Object.values(wbdata.historicSummary)
						.filter((row) => (row.energy > 0));		
				}
				break;
			case 'month':
				this.plotdata = Object.values(wbdata.historicSummary)
					.filter((row) => (row.energy > 0));
				break;
			default: break;
		}		
		const svg = this.createOrUpdateSvg();
		this.drawChart(svg);
		this.updateHeading();
	};

	createOrUpdateSvg() {
		this.svg.selectAll("*").remove();
		const g = this.svg.append("g")
			.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
		this.xScale = d3.scaleBand()
			.range([0, this.width - this.margin.left - this.margin.right])
			.padding(0.4);
		this.yScale = d3.scaleLinear()
			.range([this.height - this.margin.bottom - this.margin.top, 0]);
		return g;
	}

	drawChart(svg) {
		const ymax = d3.max(this.plotdata, (d) => d.energy);
		this.xScale.domain(this.plotdata.map((d) => d.name));
		this.yScale.domain([0, ymax]);
		const bargroups = svg
			.selectAll(".bar")
			.data(this.plotdata)
			.enter()
			.append("g");
		bargroups
			.append("rect")
			.attr("class", "bar")
			.attr("x", (d) => this.xScale(d.name))
			.attr("y", (d) => this.yScale(d.energy))
			.attr("width", this.xScale.bandwidth())
			.attr("height", (d) => this.height - this.yScale(d.energy) - this.margin.top - this.margin.bottom)
			.attr("fill", (d) => d.color);

		const yAxisGenerator = d3.axisLeft(this.yScale)
			.tickFormat(function (d) {
				return ((d > 0) ? d : "");
			})
			.ticks(8)
			.tickSizeInner(-this.width);

		const yAxis = svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + 0 + ")")
			.call(yAxisGenerator);

		yAxis.append("text")
			.attr("y", 6)
			.attr("dy", "0.71em")
			.attr("text-anchor", "end")
			.text("energy");

		yAxis.selectAll(".tick").attr("font-size", this.axisFontSize);
		if (wbdata.showGrid) {
			yAxis.selectAll(".tick line")
			.attr("stroke", this.gridColor)
			.attr ("stroke-width", "0.5");			
		} else {
			yAxis.selectAll(".tick line").attr("stroke", this.bgColor);
		}
		yAxis.select(".domain")
			.attr("stroke", this.bgcolor);

		svg.append("text")
			.attr("x", -this.margin.left)
			.attr("y", -15)
			.style("fill", this.axisColor)
			.attr("font-size", this.axisFontSize)
			.text("kWh")
			;
		const labels = svg.selectAll(".label")
			.data(this.plotdata)
			.enter()
			.append("g");
		labels
			.append("text")
			.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 2)
			.attr("y", (d) => this.yScale(d.energy) - 10)
			.attr("font-size", this.labelfontsize)
			.attr("text-anchor", "middle")
			.attr("fill", (d) => d.color)
			.text((d) => (formatWattH(d.energy * 1000)));


		const categories = svg.selectAll(".category")
			.data(this.plotdata)
			.enter()
			.append("g");
		labels
			.append("text")
			.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 2)
			.attr("y", this.height - this.margin.bottom - 5)
			.attr("font-size", this.labelfontsize)
			.attr("text-anchor", "middle")
			.attr("fill", (d) => d.color)
			.text((d) => (d.name));
	}

	updateHeading() {
		var heading = "Energie ";

		switch (wbdata.graphMode) {
			case 'live':
				heading = heading + " heute";
				break;
			case 'day':
				if (wbdata.showTodayGraph) {
					heading = heading + " heute";
				} else {
					heading = heading + wbdata.graphDate.getDate() + "." + (wbdata.graphDate.getMonth() + 1) + ".";
				}
				break;
			case 'month':
				heading = "Monatswerte " + formatMonth (wbdata.graphMonth.month, wbdata.graphMonth.year);
				break;
			default: break;
		}
		d3.select("h3#energyheading").text(heading);
	}
}
var yieldMeter = new YieldMeter();

