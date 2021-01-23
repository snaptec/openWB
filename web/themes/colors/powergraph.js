class PowerGraph {

  graphData;
  initialGraphData;
  svg;
  axiscolor;


  margin = { top: 10, right: 20, bottom: 20, left: 25 };

  constructor() {
    this.graphData = [];
    this.initCounter = 0;
    this.initialGraphData = [];
    this.initialized = false;
    this.colors = [];
    this.gridColors = [];
    this.graphRefreshCounter = 0;
    this.width = 500;
    this.height = 500;
  }

  init() {
    var style = getComputedStyle(document.body);
    this.colors[18] = style.getPropertyValue('--color-house');
    this.colors[19] = style.getPropertyValue('--color-battery');
    this.gridColors[0] = style.getPropertyValue('--color-battery');
    this.gridColors[1] = style.getPropertyValue('--color-pv');
    this.gridColors[2] = style.getPropertyValue('--color-export');
    this.gridColors[3] = style.getPropertyValue('--color-evu');
    this.bgcolor = style.getPropertyValue('--color-bg');
    this.chargeColor = style.getPropertyValue('--color-charging');
    this.axiscolor = style.getPropertyValue('--color-axis');

    var i;
    for (i = 0; i < 8; i++) {
      this.colors[i] = wbdata.chargePoint[i].color;
    }
    for (i = 0; i < 8; i++) {
      this.colors[8 + i] = wbdata.shDevice[i].color;
    }
    this.colors[16] = style.getPropertyValue('--color-co1');
    this.colors[17] = style.getPropertyValue('--color-co2');
    var figure = d3.select("figure#powergraph");
    this.svg = figure.append("svg")
      .attr("viewBox", `0 0 500 500`);

  }


  update(topic, payload) {

    if (this.initialized) { // steady state

      if (topic === "openWB/graph/lastlivevalues") {
        const values = this.extractValues(payload.toString());
        this.graphRefreshCounter++;
        this.graphData.push(values);
        this.updateGraph();

        if (this.graphData > 60) {
          this.initialized = false;
          this.initialGraphData = true;
          subscribeMqttGraphSegments();
        }
      }
    } else { // init phase
      const t = topic;
      if (t.substring(t.length - 13, t.length) === "alllivevalues") {
        // init message
        const serialNo = t.substring(13, t.length - 13);
        var bulkdata = payload.toString().split("\n");
        if (bulkdata.length <= 1) {
          bulkdata = [];
        }
        if (serialNo != "") {
          if (typeof (this.initialGraphData[+serialNo - 1]) === 'undefined') {
            this.initialGraphData[+serialNo - 1] = bulkdata;
            this.initCounter++;
          }
        }
        if (this.initCounter == 16) {// Initialization complete
          this.initialized = true;
          this.initialGraphData.map(bulkdata => {
            bulkdata.map((line) => {
              const values = this.extractValues(line);
              this.graphData.push(values);
            });
          });

          this.graphData = this.graphData.sort((a, b) =>
            a.date > b.date ? 1 : -1
          );
          this.updateGraph();
          unsubscribeMqttGraphSegments();
        }
      }
    }
  }


  extractValues(payload) {
    const elements = payload.split(",");
    var values = {};
    values.date = new Date(d3.timeParse("%H:%M:%S")(elements[0]));
    if (+elements[1] > 0) {
      values.gridPull = +elements[1];
      values.gridPush = 0;
    } else {
      values.gridPull = 0;
      values.gridPush = -elements[1];
    }
    // values.chargePower = +elements[2];
    values.solarPower = +elements[3];
    values.housePower = +elements[11];
    // values.boilerPower = +elements[21];
    values.soc1 = +elements[9];
    values.soc2 = +elements[10];
    values.selfUsage = values.solarPower - values.gridPush;
    if (values.selfUsage < 0) {
      values.selfUsage = 0;
    }
    var i;
    
    values.lp0 = +elements[4];
    values.lp1 = +elements[5];
    for (i = 2; i < 9; i++) {
      values["lp" + i] = +elements[11 + i];
    }
    for (i = 0; i < 8; i++) {
      values["sh" + i] = +elements[20 + i];
    }
    values.co1 = +elements[12];
    values.co2 = +elements[13];
    if (+elements[7] > 0) {
      values.batIn = +elements[7];
      values.batOut = 0;
    } else if (+elements[7] < 0) {
      values.batIn = 0;
      values.batOut = -elements[7]
    } else {
      values.batIn = 0;
      values.batOut = 0;
    };
    values.batSoc = +elements[8];
    return values;
  }




  updateGraph() {
    const svg = this.createOrUpdateSvg();
    this.drawChart(svg);
  };

  createOrUpdateSvg() {
    this.svg.selectAll("*").remove();


    this.g = this.svg
      .append("g")
      .attr(
        "transform",
        "translate(" + this.margin.left + "," + this.margin.top + ")"
      );
    return this.g;
  }

  drawChart(svg) {
    const height = this.height - this.margin.top - this.margin.bottom;
    const width = this.width - this.margin.left - this.margin.right;

    this.drawSourceGraph(svg, width, height / 2);
    this.drawUsageGraph(svg, width, height / 2);
    this.drawXAxis(svg, width, height);
    this.drawSoc(svg, width, height / 2);
  }

  drawSourceGraph(svg, width, height) {
    const keys = ["batOut","selfUsage", "gridPush", "gridPull"];
    const xScale = d3.scaleTime().range([0, width - this.margin.right]);
    const yScale = d3.scaleLinear().range([height - 10, 0]);
    const extent = d3.extent(this.graphData, (d) =>
      Math.max(d.solarPower + d.gridPull, d.selfUsage + d.gridPush));

    xScale.domain(d3.extent(this.graphData, (d) => d.date));
    yScale.domain([0, extent[1]]);

    const stackGen = d3.stack().keys(keys);
    const stackedSeries = stackGen(this.graphData);

    svg.selectAll(".sourceareas")
      .data(stackedSeries)
      .join("path")
      .attr("d", d3.area()
        .x((d, i) => xScale(this.graphData[i].date))
        .y0((d) => yScale(d[0]))
        .y1((d) => yScale(d[1]))
      )
      .attr("fill", (d, i) => this.gridColors[i]);

    const yAxis = svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(yScale)
      .tickSizeInner(-width)
      .ticks(6)
      .tickFormat((d, i) => (d == 0) ? "" : (Math.round(d / 100) / 10)))
      ;
    yAxis.selectAll(".tick")
      .attr("font-size", 12);
    yAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    yAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }

  drawUsageGraph(svg, width, height) {
    const xScale = d3.scaleTime().range([0, width - this.margin.right]);
    const yScale = d3.scaleLinear().range([height + 10, 2 * height + 15]);

    xScale.domain(d3.extent(this.graphData, (d) => d.date));
    const extent = d3.extent(this.graphData, (d) =>
      Math.max(d.housePower + d.lp0 + d.lp1 + d.lp2 + d.lp3 + d.lp4
        + d.lp5 + d.lp6 + d.lp7 + d.sh0 + d.sh1 + d.sh2 + d.sh3 + d.sh4
        + d.sh5 + d.sh6 + d.sh7, 0)
    );
    yScale.domain([0, (extent[1])]);
    const keys = ["lp0", "lp1", "lp2", "lp3", "lp4",
      "lp5", "lp6", "lp7",
      "sh0", "sh1", "sh2", "sh3", "sh4",
      "sh5", "sh6", "sh7", "co1", "co2", "housePower", "batIn"];

    const stackGen = d3.stack().keys(keys);
    const stackedSeries = stackGen(this.graphData);

    svg.selectAll(".targetareas")
      .data(stackedSeries)
      .join("path")
      .attr("d", d3.area()
        .x((d, i) => xScale(this.graphData[i].date))
        .y0((d) => yScale(d[0]))
        .y1((d) => yScale(d[1]))
      )
      .attr("fill", (d, i) => this.colors[i]);

    const yAxis = svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(yScale)
      .tickSizeInner(-width)
      .ticks(6)
      .tickFormat((d, i) => (d == 0) ? "" : (Math.round(d / 100) / 10))
    );
    yAxis.selectAll(".tick")
      .attr("font-size", 12);
    yAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    yAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }

  drawXAxis(svg, width, height) {
    const xScale = d3.scaleTime().range([0, width - this.margin.right]);
    xScale.domain(d3.extent(this.graphData, (d) => d.date));

    const xAxisGenerator = d3
      .axisBottom(xScale)
      .ticks(4)
      .tickSizeInner(-10)
      .tickFormat(d3.timeFormat("%H:%M"));

    const xAxis = svg.append("g").attr("class", "axis")
      .call(xAxisGenerator);
    xAxis.attr("transform", "translate(0," + (height / 2 - 6) + ")");
    xAxis.selectAll(".tick")
      .attr("color", this.axiscolor)
      .attr("font-size", 12)
    xAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    xAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;

  }
  drawSoc(svg, width, height) {
    const xScale = d3.scaleTime().range([0, width - this.margin.right]);
    const yScale = d3.scaleLinear().range([height - 10, 0]);
    xScale.domain(d3.extent(this.graphData, (d) => d.date));
    yScale.domain([0, 100]);

    svg.append("path")
      .datum(this.graphData)
      .attr("stroke", this.chargeColor)
      .attr("stroke-width", 1)
      .attr("fill", this.bgcolor)
      .style("stroke-dasharray", ("3, 3"))
      .style("background-color", this.bgcolor)
      .attr("d", d3.line()
        .x((d, i) => xScale(this.graphData[i].date))
        .y(d => yScale(d.soc1))
      );

    const socAxis = svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + (width - 20) + ",0)")
      .call(d3.axisRight(yScale)
        .ticks(5)
        .tickFormat((d) => (d + "%")))

      ;
    socAxis.selectAll(".tick").attr("font-size", 12);
    socAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    socAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }
}


var powerGraph = new PowerGraph();

