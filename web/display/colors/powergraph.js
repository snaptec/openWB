class PowerGraph {


  constructor() {
    this.graphData = [];
    this.initCounter = 0;
    this.staging = [];
    this.rawData = [];
    this.graphdata = []
    this.initialGraphData = [];
    this.initialized = false;
    this.colors = [];
    this.gridColors = {};
    this.bgcolor = "";
    this.axiscolor = "";
    this.chargeColor = "";
    this.lp1color = "";
    this.lp2color = "";
    this.batteryColor = "";
    this.batSocColor = "";
    this.graphRefreshCounter = 0;
    this.width = 500;
    this.height = 500;
    this.margin = { top: 10, right: 20, bottom: 10, left: 25 };
    this.liveGraphMinutes = 0;
    wbdata.usageStackOrder = 2;
    this.svg=null;
    this.xScale=null;
  }

  init() {
    var style = getComputedStyle(document.body);
    this.colors.housePower = 'var(--color-house)';
    this.colors.batIn = 'var(--color-battery)';
    this.colors.inverter = 'var(--color-pv)';
    this.gridColors[0] = 'var(--color-battery)';
    this.colors.batOut = 'var(--color-battery)';
    this.gridColors[1] = 'var(--color-pv)';
    this.colors.selfUsage = 'var(--color-pv)';
    this.gridColors[2] = 'var(--color-export)';
    this.colors.gridPush = 'var(--color-export)';
    this.gridColors[3] = 'var(--color-evu)';
    this.colors.gridPull = 'var(--color-evu)';
    this.bgcolor = 'var(--color-bg)';
    this.chargeColor = 'var(--color-charging)';
    this.axiscolor = 'var(--color-axis)';
    this.gridcolor = 'var(--color-grid)';
    this.lp1color = 'var(--color-lp1)';
    this.lp2color = 'var(--color-lp2)';
    this.batteryColor = 'var(--color-battery)';
    this.batSocColor = 'var(--color-title)';
    var i;
    for (i = 0; i < 8; i++) {
      this.colors["lp" + i] = wbdata.chargePoint[i].color;
    }
    for (i = 0; i < 8; i++) {
      this.colors["sh" + i] = wbdata.shDevice[i].color;
    }
    this.colors.co0 = 'var(--color-co1)';
    this.colors.co1 = 'var(--color-co2)';

    var figure = d3.select("figure#powergraph");
    this.svg = figure.append("svg")
      .attr("viewBox", `0 0 500 500`);

  }

  activateLive() {
    try {
      this.resetLiveGraph();
      subscribeMqttGraphSegments();
      subscribeGraphUpdates();
    } catch (err) {
      // on initial invocation this method is not existing
    }
    this.updateHeading();
  }

  deactivateLive() {
    try {
      unsubscribeMqttGraphSegments();
      unsubscribeGraphUpdates();
    } catch (err) {
      // on intial run this method is not existing
    }
  }

  updateHeading() {
    var heading = "";
    heading = heading + this.liveGraphMinutes + " min";
    d3.select("h3#widgetheading").text(heading);
  }

  updateLive(topic, payload) {
    if (wbdata.graphMode == 'live') { // only update if live graph is active
      if (this.initialized) { // steady state
        if (topic === "openWB/graph/lastlivevalues") {
          const values = this.extractLiveValues(payload.toString());
          this.graphRefreshCounter++;
          this.graphData.push(values);
          this.updateGraph();
          if (this.graphRefreshCounter > 60) {
            this.resetLiveGraph();
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
                const values = this.extractLiveValues(line);
                this.graphData.push(values);
              });
            });
            const startTime = this.graphData[0].date;
            const endTime = this.graphData[this.graphData.length - 1].date;
            this.liveGraphMinutes = Math.round((endTime - startTime) / 60000);
            this.updateHeading();
            this.updateGraph();
            unsubscribeMqttGraphSegments();
          }
        }
      }
    }
  }

  extractLiveValues(payload) {
    const elements = payload.split(",");
    const now = new Date (Date.now());
    const mSecondsPerDay = 86400000 // milliseconds in a day
    var values = {};
    values.date = new Date(d3.timeParse("%H:%M:%S")(elements[0]));
    values.date.setDate (now.getDate())
    values.date.setMonth (now.getMonth())
    values.date.setFullYear (now.getFullYear())
    if (values.date.getHours() > now.getHours()) { // this is an entry from yesterday
      values.date = new Date (values.date.getTime() - mSecondsPerDay) // change date to yesterday
    }
  
    // evu
    if (+elements[1] > 0) {
      values.gridPull = +elements[1];
      values.gridPush = 0;
    } else {
      values.gridPull = 0;
      values.gridPush = -elements[1];
    }
    // pv
    if (+elements[3] >= 0) {
      values.solarPower = +elements[3];
      values.inverter = 0;
    } else {
      values.solarPower = 0;
      values.inverter = -elements[3]
    }
    // calculated values
    values.housePower = +elements[11];
    values.selfUsage = values.solarPower - values.gridPush;
    if (values.selfUsage < 0) {
      values.selfUsage = 0;
    }
    // charge points
    var i;
    values.lp0 = +elements[4];
    values.lp1 = +elements[5];
    for (i = 2; i < 9; i++) {
      values["lp" + i] = +elements[11 + i];
    }
    values.soc1 = +elements[9];
    values.soc2 = +elements[10];

    // smart home
    for (i = 0; i < 8; i++) {
      if (!(wbdata.shDevice[i].countAsHouse)) {
        values["sh" + i] = +elements[20 + i];
      } else {
        values["sh" + i] = +0;
      }
    }
    //consumers
    values.co0 = +elements[12];
    values.co1 = +elements[13];
    //battery
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
    values.batterySoc = +elements[8];

    return values;
  }

  reset() {
    this.resetLiveGraph();
  }

  resetLiveGraph() {
    // fresh reload of the graph
    this.initialized = false;
    this.initCounter = 0;
    this.initialGraphData = [];
    this.graphData = [];
    this.graphRefreshCounter = 0;
  }

  calcValue(i, array, oldArray) {
    var val = (array[i] - oldArray[i]) * 12;
    if (val < 0 || val > 150000) {
      val = 0;
    }
    return val;
  }

  calcMonthlyValue(i, array, oldArray) {
    var val = (array[i] - oldArray[i]);

    if (val < 0 || val > 150000) {
      val = 0;
    }
    return val;
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
    if (wbdata.graphMode != 'month') {
      this.drawSoc(svg, width, height / 2);
    }
    this.drawXAxis(svg, width, height);
  }

  drawSourceGraph(svg, width, height) {
    var keys = (wbdata.graphMode == 'month') ? ["gridPull", "batOut", "selfUsage", "gridPush"] : ["selfUsage", "gridPush", "batOut", "gridPull"];

    this.xScale = d3.scaleTime().domain(d3.extent(this.graphData, d => d.date));

    this.xScale.range([0, width - this.margin.right]);
    const yScale = d3.scaleLinear().range([height - 10, 0]);
    const extent = d3.extent(this.graphData, (d) =>
      Math.max(d.solarPower + d.gridPull + d.batOut, d.selfUsage + d.gridPush));

    yScale.domain([0, Math.ceil(extent[1] / 1000) * 1000]);

    const stackGen = d3.stack().keys(keys);
    const stackedSeries = stackGen(this.graphData);


    svg.selectAll(".sourceareas")
      .data(stackedSeries)
      .join("path")
      .attr("d", d3.area()
        .x((d, i) => this.xScale(this.graphData[i].date))
        .y0((d) => yScale(d[0]))
        .y1((d) => yScale(d[1]))
      )
      .attr("fill", (d, i) => this.colors[keys[i]]);


    const yAxis = svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(yScale)
        .tickSizeInner(-(width - this.margin.right))
        .ticks(4)
        .tickFormat((d, i) => (d == 0) ? "" : (Math.round(d / 100) / 10)))
      ;
    yAxis.selectAll(".tick")
      .attr("font-size", 12)
      .attr("color", this.axiscolor);

    if (wbdata.showGrid) {
      yAxis.selectAll(".tick line")
        .attr("stroke", this.gridcolor)
        .attr("stroke-width", "0.5");
    } else {
      yAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    }
    yAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }

  drawUsageGraph(svg, width, height) {
    const yScale = d3.scaleLinear().range([height + 10, 2 * height]);

    const extent = d3.extent(this.graphData, (d) =>
    (d.housePower + d.lp0 + d.lp1 + d.lp2 + d.lp3 + d.lp4
      + d.lp5 + d.lp6 + d.lp7 + d.sh0 + d.sh1 + d.sh2 + d.sh3 + d.sh4
      + d.sh5 + d.sh6 + d.sh7 + d.co0 + d.co1 + d.batIn + d.inverter)
    );
    yScale.domain([0, Math.ceil(extent[1] / 1000) * 1000]);
    const keys = [["lp0", "lp1", "lp2", "lp3", "lp4",
      "lp5", "lp6", "lp7",
      "sh0", "sh1", "sh2", "sh3", "sh4",
      "sh5", "sh6", "sh7", "co0", "co1", "housePower", "batIn", "inverter"],
    ["housePower", "lp0", "lp1", "lp2", "lp3", "lp4",
      "lp5", "lp6", "lp7",
      "sh0", "sh1", "sh2", "sh3", "sh4",
      "sh5", "sh6", "sh7", "co0", "co1", "batIn", "inverter"],
    ["sh0", "sh1", "sh2", "sh3", "sh4",
      "sh5", "sh6", "sh7", "co0", "co1", "housePower", "lp0", "lp1", "lp2", "lp3", "lp4",
      "lp5", "lp6", "lp7",
      "batIn", "inverter"]
    ];

    const stackGen = d3.stack().keys(keys[wbdata.usageStackOrder]);
    const stackedSeries = stackGen(this.graphData);
    if (wbdata.graphMode == 'month') {
      svg.selectAll(".sourcebar")
        .data(stackedSeries).enter()
        .append("g")
        .attr("fill", (d, i) => this.colors[keys[wbdata.usageStackOrder][i]])
        .selectAll("rect")
        .data(d => d).enter()
        .append("rect")
        .attr("x", (d) => this.xScale(d.data.date.getDate()))
        .attr("y", d => yScale(d[0]))
        .attr("height", d => yScale(d[1]) - yScale(d[0]))
        .attr("width", this.xScale.bandwidth())
    } else {
      svg.selectAll(".targetareas")
        .data(stackedSeries)
        .join("path")
        .attr("d", d3.area()
          .x((d, i) => this.xScale(this.graphData[i].date))
          .y0((d) => yScale(d[0]))
          .y1((d) => yScale(d[1]))
        )
        .attr("fill", (d, i) => this.colors[keys[wbdata.usageStackOrder][i]]);
    }
    const yAxis = svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(yScale)
        .tickSizeInner(-(width - this.margin.right))
        .ticks(4)
        .tickFormat((d, i) => (d == 0) ? "" : (Math.round(d / 100) / 10))
      );
    yAxis.selectAll(".tick")
      .attr("font-size", 12)
      .attr("color", this.axiscolor);
    if (wbdata.showGrid) {
      yAxis.selectAll(".tick line")
        .attr("stroke", this.gridcolor)
        .attr("stroke-width", "0.5");
    } else {
      yAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    }
    yAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }

  drawXAxis(svg, width, height) {
    const fontsize = 12;
    const xScale = d3.scaleTime().range([0, width - this.margin.right]);
    xScale.domain(d3.extent(this.graphData, (d) => d.date));

    var ticksize = (wbdata.showGrid) ? -(height / 2 - 7) : -10
    if (wbdata.graphMode == 'month') {
      ticksize = 0;
    }
    const xAxisGenerator = d3
      .axisBottom(this.xScale)
      .ticks(4)
      .tickSizeInner(ticksize)

    if (wbdata.graphMode != 'month') {
      xAxisGenerator.tickFormat(d3.timeFormat("%H:%M"))
        .ticks(4);
    }

    const xAxis = svg.append("g").attr("class", "axis")
      .call(xAxisGenerator);
    xAxis.attr("transform", "translate(0," + (height / 2 - 6) + ")");
    xAxis.selectAll(".tick")
      .attr("color", this.axiscolor)
      .attr("font-size", fontsize);
    if (wbdata.showGrid) {
      xAxis.selectAll(".tick line")
        .attr("stroke", this.gridcolor)
        .attr("stroke-width", "0.5");
    } else {
      xAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    }
    xAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
    svg.append("text")
      .attr("x", - this.margin.left)
      .attr("y", height / 2 + 5)
      .attr("fill", this.axiscolor)
      .attr("font-size", fontsize)
      .text("kW")

    if (wbdata.showGrid) {
      // second x axis for the grid
      const ticksize2 = -(height / 2 - 10);
      const xAxisGenerator2 = d3
        .axisTop(xScale)
        .ticks(4)
        .tickSizeInner(ticksize2)
        .tickFormat("");
      const xAxis2 = svg.append("g").attr("class", "axis")
        .call(xAxisGenerator2);
      xAxis2.attr("transform", "translate(0," + (height / 2 + 10) + ")");
      xAxis2.selectAll(".tick")
        .attr("color", this.axiscolor)
        .attr("font-size", fontsize);
      xAxis2.selectAll(".tick line").attr("stroke", this.gridcolor).attr("stroke-width", "0.5");


      xAxis2.select(".domain")
        .attr("stroke", this.bgcolor)
        ;
      // add a rectangle around the graph
      svg.append("g")
        .append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", width - this.margin.right)
        .attr("height", height)
        .attr("fill", "none")
        .attr("stroke", this.gridcolor)
        .attr("stroke-width", "0.5");
    }
  }

  drawSoc(svg, width, height) {
    const xScale = d3.scaleTime().range([0, width - this.margin.right]);
    const yScale = d3.scaleLinear().range([height - 10, 0]);
    xScale.domain(d3.extent(this.graphData, (d) => d.date));
    yScale.domain([0, 100]);
    // Chargepoint 1
    if (wbdata.chargePoint[0].isSocConfigured) {
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.bgcolor)
        .attr("stroke-width", 1)
        .attr("fill", "none")
        //.style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.soc1))
        );
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.lp1color)
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.soc1))
        );
      svg.append("text")
        .attr("x", width - this.margin.right - 3)
        .attr("y", yScale(this.graphData[this.graphData.length - 1].soc1 + 2))
        .text(wbdata.chargePoint[0].name)
        .attr("fill", this.lp1color)
        .style("font-size", 10)
        .attr("text-anchor", "end");
    }
    // Chargepoint 2
    if (wbdata.chargePoint[1].isSocConfigured) {
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.bgcolor)
        .attr("stroke-width", 1)
        .attr("fill", "none")
        // .style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.soc2))
        );
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.lp2color)
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.soc2))
        );
      svg.append("text")
        .attr("x", 3)
        .attr("y", yScale(this.graphData[this.graphData.length - 1].soc2 + 2))
        .text(wbdata.chargePoint[1].name)
        .attr("fill", this.lp2color)
        .style("font-size", 10)
        .attr("text-anchor", "start");
    }
    // Battery
    if (wbdata.isBatteryConfigured) {
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.bgcolor)
        .attr("stroke-width", 2)
        .attr("fill", "none")
        //.style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.batterySoc))
        );
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.batSocColor)
        .attr("stroke-width", 2)
        .attr("fill", "none")
        .style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.batterySoc))
        );
      svg.append("text")
        .attr("x", (width - this.margin.right) / 2)
        .attr("y", yScale(this.graphData[this.graphData.length - 1].batterySoc + 2))
        .text("Speicher")
        .attr("fill", this.batteryColor)
        .style("background-color", "black")
        .style("font-size", 10)
        .attr("text-anchor", "middle");
    }
    const socAxis = svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + (width - 20) + ",0)")
      .call(d3.axisRight(yScale)
        .ticks(5)
        .tickFormat((d) => (d + "%")))
      ;
    socAxis.selectAll(".tick")
      .attr("font-size", 12)
      .attr("color", this.axiscolor);
    socAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    socAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }




  getEnergyValues() {

  }
}

// Change the order of values in the stack
function changeStack() {
  wbdata.usageStackOrder = wbdata.usageStackOrder + 1;
  if (wbdata.usageStackOrder > 2) {
    wbdata.usageStackOrder = 0;
  }
  wbdata.persistGraphPreferences();
  powerGraph.updateGraph();
}

var powerGraph = new PowerGraph();

