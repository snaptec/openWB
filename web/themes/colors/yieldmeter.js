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
		this.margin = 40;
	}

	// to be called when the document is loaded
	init() {
		const figure = d3.select("figure#energymeter");
		this.svg = figure.append("svg")
			.attr("viewBox", `0 0 500 500`);

		const style = getComputedStyle(document.body);
    this.houseColor = style.getPropertyValue('--color-house');
    this.pvColor = style.getPropertyValue('--color-pv');
    this.exportColor = style.getPropertyValue('--color-export');
    this.gridColor = style.getPropertyValue('--color-evu');
    this.bgColor = style.getPropertyValue('--color-bg');
		this.chargeColor = style.getPropertyValue('--color-charging');
		this.axisColor = style.getPropertyValue('--color-axis');
	}

	// to be called when values have changed
	update() {
		this.plotdata = wbdata.sourceSummary
			.filter((row) => (row.energy > 0))
			.concat(wbdata.usageDetails
				.filter((row) => (row.energy > 0)));
		const svg = this.createOrUpdateSvg();
		this.drawChart(svg);
	};

	createOrUpdateSvg() {
		this.svg.selectAll("*").remove();
		/* this.svg
			.append("rect")
			.attr("width", "100%")
			.attr("height", "100%")
			.attr("fill", "midnightblue"); */

		const g = this.svg.append("g")
			.attr("transform", "translate(" + this.margin + "," + this.margin + ")");
		this.xScale = d3.scaleBand()
			.range([0, this.width - this.margin - 10])
			.padding(0.4);
		this.yScale = d3.scaleLinear()
			.range([this.height - 2 * this.margin, 0]);

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
			.attr("height", (d) => +this.height - this.margin - this.margin - this.yScale(d.energy))
			.attr("fill", (d) => d.color);

		const xAxisGenerator = d3.axisBottom(this.xScale);
		const xAxis = svg
			.append("g")
			.attr("transform", "translate(0," + (+this.height - 80) + ")")
			.call(xAxisGenerator);
		xAxis.selectAll(".tick").attr("stroke", this.axisColor);
		xAxis.selectAll(".tick line").attr("stroke", this.axisColor);


		const yAxisGenerator = d3.axisLeft(this.yScale)
			.tickFormat(function (d) {
				return d + " kWh";
			})
			.ticks(6)
			.tickSizeInner(-this.width);

		const yAxis = svg.append("g")
			.call(yAxisGenerator);

		yAxis.append("text")
			.attr("y", 6)
			.attr("dy", "0.71em")
			.attr("text-anchor", "end")
			.text("energy");

		yAxis.selectAll(".tick").attr("stroke", this.axisColor);
		yAxis.selectAll(".tick line").attr("stroke", this.bgColor);

		const labels = svg.selectAll(".label")
			.data(this.plotdata)
			.enter()
			.append("g");
		labels
			.append("text")
			.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 2)
			.attr("y", (d) => this.yScale(d.energy) - 10)

			.attr("text-anchor", "middle")
			.attr("fill", (d) => d.color)
			.text((d) => (formatWattH(d.energy * 1000)));
	}
}
var yieldMeter = new YieldMeter();

