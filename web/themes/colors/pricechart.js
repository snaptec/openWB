class PriceChart {

  constructor() {
    this.width = 400;
    this.height = 120;
    this.margin = { top: 5, bottom: 15, left: 15, right: 5 };

  }

  // initialize when application is loaded
  init() {
    const figure = d3.select("figure#priceChart");
    this.svg = figure.append("svg")
      .attr("viewBox", `0 0 400 120`);
    this.bgColor = 'var(--color-bg)';
    this.gridColor = 'var(--color-grid)';
    this.axisColor = 'var(--color-axis)';
    this.chargeColor = 'var(--color-charging)';
    this.noChargeColor = 'var(--color-axis)';
    wbdata.etPriceList = '';
    
  }

  // update the view
  update() {
    var svg = this.createOrUpdateSvg();
    d3.select(".priceConfiguration").classed("hide", !((wbdata.chargeMode == "0") && wbdata.isEtEnabled));
    d3.select(".labelMaxPrice").text(wbdata.etMaxPrice + " ct/kWh");
    d3.select(".maxPriceInput").property("value", wbdata.etMaxPrice);
      
    if (wbdata.etPriceList != "") {
      this.plotdata = wbdata.etPriceList.split(/\r?\n|\r/); // split into lines
      this.plotdata.shift();                                // remove first line
      this.plotdata = this.plotdata.map((line, i) => {      // split lines into tuples [time,price]
        return line.split(',')
      }) .map(line => [line[0] * 1000, +line[1]]);           // multiply timestamps by 1000
      this.drawGraph(svg);
    }
    d3.select(".maxPriceInput")
			.on("input", function () { updateMaxPriceInput(this.value) });
    d3.select(".priceMore")
			.on("click", function () { incrementMaxPrice() });
    d3.select(".priceLess")
			.on("click", function () { decrementMaxPrice() });
    
  }

  // clear the display area
  createOrUpdateSvg() {
    this.svg.selectAll("*").remove();
    const g = this.svg.append("g")
      .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
    return g
  }

  // draw the graph
  drawGraph(svg) {
    const height = this.height - this.margin.top - this.margin.bottom;
    const width = this.width - this.margin.left - this.margin.right;
    const barwidth = width / this.plotdata.length - 1
    const xdomain = d3.extent(this.plotdata, (d) => d[0])
    xdomain[1] = xdomain[1] + 3600000
    this.xScale = d3.scaleTime()
      .range([0, width])
      .domain(xdomain);
    const ydomain = d3.extent(this.plotdata, (d) => d[1]);
    if (ydomain[0] > 0) {
      ydomain[0] = 0;
    }
    ydomain[1] = Math.floor(ydomain[1] + 1)
    this.yScale = d3.scaleLinear()
      .range([this.height - this.margin.bottom - this.margin.top, 0])
      .domain(ydomain);

    const bargroups = svg.selectAll("bar")
      .data(this.plotdata).enter()
      .append("g");
    bargroups.append("rect")
      .attr("class", "bar")
      .attr("x", (d) => this.xScale(d[0]))
      .attr("y", (d) => (d[1] >= 0) ? this.yScale(d[1]) : this.yScale(0))
      .attr("width", barwidth)
      .attr("height", (d) => (d[1] >=0) 
        ? this.yScale(0) - this.yScale(d[1]) 
        : this.yScale(d[1]) - this.yScale(0))
      .attr("fill", (d) => (d[1] <= wbdata.etMaxPrice) ? this.chargeColor : this.noChargeColor)

    // Line for max price
    const generator = d3.line();
    const points = [[0, this.yScale(wbdata.etMaxPrice)], [width, this.yScale(wbdata.etMaxPrice)]]
    const path = generator(points)
    svg.append("path")
      .attr('d', path)
      .attr("stroke", "yellow")

    // X Axis
    const xAxisGenerator = d3.axisBottom(this.xScale)
      .ticks(4)
      .tickFormat(d3.timeFormat("%H:%M"))
    const xAxis = this.svg.append("g")
      .attr("class", "axis")
      .call(xAxisGenerator);
    xAxis.attr("transform", "translate(" + this.margin.left + "," + (height + this.margin.top) + ")");
    xAxis.selectAll(".tick")
    .attr("font-size", 8)
    .attr("color", this.bgColor);
    xAxis.selectAll(".tick line")
    .attr("stroke", this.bgColor)
    .attr("stroke-width", "0.5");
    xAxis.select(".domain")
    .attr("stroke", this.bgColor)
    ;
    // Y Axis
    const yAxisGenerator = d3.axisLeft(this.yScale)
      .ticks(6)
      .tickSizeInner(-(this.width - this.margin.right - this.margin.left))
      .tickFormat((d) => d)

    const yAxis = this.svg.append("g")
      .attr("class", "axis")
      .call(yAxisGenerator)

    yAxis.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
    yAxis.selectAll(".tick")
      .attr("font-size", 8)
      .attr("color", this.bgColor);

    yAxis.selectAll(".tick line")
      .attr("stroke", this.bgColor)
      .attr("stroke-width", "0.5");

    yAxis.select(".domain")
      .attr("stroke", this.bgColor)
      ;
  }
}

function updateMaxPriceInput(value) {
  const label = d3.select(".labelMaxPrice").text(value + " ct/kWh");
	label.classed("text-danger", true)

	wbdata.updateET ("etMaxPrice", parseFloat(value));
	if (wbdata.maxPriceDelayTimer) {
		clearTimeout(wbdata.maxPriceDelayTimer)
	}
	wbdata.maxPriceDelayTimer = setTimeout(() => {
		label.classed("text-danger", false)
		publish(String(value), "openWB/set/awattar/MaxPriceForCharging" )
		wbdata.maxPriceDelayTimer = null;
	}, 2000)
}
const maxPriceIncrement = 0.1;

function incrementMaxPrice() {
  updateMaxPriceInput (String (Math.round ((wbdata.etMaxPrice + maxPriceIncrement)*10)/10));
  d3.select(".maxPriceInput").property("value", wbdata.etMaxPrice);
}

function decrementMaxPrice() {
  updateMaxPriceInput (String (Math.round ((wbdata.etMaxPrice - maxPriceIncrement)*10)/10));
  d3.select(".maxPriceInput").property("value", wbdata.etMaxPrice);
}

var priceChart = new PriceChart();
