class PowerGraph {
  svg;

  constructor() {
    this.graphData = [];
    this.initCounter = 0;
    this.staging = [];
    this.rawData = [];
    this.graphdata = []
    this.initialGraphData = [];
    this.initialized = false;
    this.colors = [];
    this.gridColors = [];
    this.bgcolor = "";
    this.axiscolor = "";
    this.chargeColor = "";
    this.lp1color = "";
    this.lp2color = "";
    this.batteryColor = "";
    this.graphRefreshCounter = 0;
    this.width = 500;
    this.height = 500;
    this.margin = { top: 10, right: 20, bottom: 20, left: 25 };
    this.graphDate = new Date();
  }

  init() {
    var style = getComputedStyle(document.body);
    this.colors[18] = style.getPropertyValue('--color-house');
    this.colors[19] = style.getPropertyValue('--color-battery');
    this.colors[20] = style.getPropertyValue('--color-pv');
    this.gridColors[0] = style.getPropertyValue('--color-battery');
    this.gridColors[1] = style.getPropertyValue('--color-pv');
    this.gridColors[2] = style.getPropertyValue('--color-export');
    this.gridColors[3] = style.getPropertyValue('--color-evu');
    this.bgcolor = style.getPropertyValue('--color-bg');
    this.chargeColor = style.getPropertyValue('--color-charging');
    this.axiscolor = style.getPropertyValue('--color-axis');
    this.lp1color = style.getPropertyValue('--color-lp1');
    this.lp2color = style.getPropertyValue('--color-lp2');
    this.batteryColor = style.getPropertyValue('--color-battery');
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

    d3.select("button#graphLeftButton")
      .on("click", shiftLeft)
    d3.select("button#graphRightButton")
      .on("click", shiftRight)
  }

  activateLive() {
    try {
      this.resetLiveGraph();
      subscribeMqttGraphSegments();
      subscribeGraphUpdates();
    } catch (err) {
      // on initial invocation this method is not existing
    }
    d3.select("h3#graphheading").text("Leistung / Ladestand")
  }

  deactivateLive() {
    try {
      unsubscribeMqttGraphSegments();
      unsubscribeGraphUpdates();
    } catch (err) {
      // on intial run this method is not existing
    }
  }
  activateDay() {
    if (!wbdata.showLiveGraph) {
      this.resetDayGraph();
      try {
        subscribeDayGraph(this.graphDate);
      } catch (err) {
        //on initial run of activate, subscribeDayGraph is not yet initialized. 
        // the error can be ignored
      }
      var heading = "Leistung / Ladestand ";
      const today = new Date();
      if (today.getDate() == this.graphDate.getDate() && today.getMonth() == this.graphDate.getMonth() && today.getFullYear() == this.graphDate.getFullYear()) {
        heading = heading + "heute";
      } else {
        heading = heading + this.graphDate.getDate() + "." + (this.graphDate.getMonth() + 1) + ".";
      }
      d3.select("h3#graphheading").text(heading);
    }
  }

  deactivateDay() {
  }
  updateLive(topic, payload) {
    if (wbdata.showLiveGraph) { // only udpdate if live graph is active
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
            this.updateGraph();
            unsubscribeMqttGraphSegments();
          }
        }
      }
    }
  }

  updateDay(topic, payload) {
    if (payload != 'empty') {
      var segment = payload.toString().split("\n");
      if (segment.length <= 1) {
        segment = [];
      }
      const serialNo = topic.substring(26, topic.length);
      if (serialNo != "") {
        if (typeof (this.staging[+serialNo - 1]) === 'undefined') {
          this.staging[+serialNo - 1] = segment;
          this.initCounter++;
        }
      }
      if (this.initCounter == 12) {// Initialization complete
        unsubscribeDayGraph();
        
        this.initCounter = 0;
        this.staging.map(segment =>
          segment.map(line => this.rawData.push(line))
        )
        this.rawData.map((line, i, a) => {
          if (i > 0) {
            const values = this.extractDayValues(line, a[i - 1]);
            this.graphData.push(values);
          } else {
            // const values = this.extractValues(line, []);                
          }
        });
        this.updateGraph();
        setTimeout(() => this.activateLive(), 300000)
      }
    }
  }

  extractDayValues(payload, oldPayload) {
    const elements = payload.split(",");
    const oldElements = oldPayload.split(",");
    var values = {};
    values.date = new Date(d3.timeParse("%H%M")(elements[0]));
    // evu
    values.gridPull = this.calcValue(1, elements, oldElements);
    values.gridPush = this.calcValue(2, elements, oldElements);
    // pv
    values.solarPower = this.calcValue(3, elements, oldElements);
    values.inverter = 0;
    // charge points
    values.charging = this.calcValue(7, elements, oldElements);
    var i;
    for (i = 0; i < 3; i++) {
      values["lp" + i] = this.calcValue(4 + i, elements, oldElements);
    }
    for (i = 3; i < 8; i++) {
      values["lp" + i] = this.calcValue(12 + i, elements, oldElements);
    }
    values.soc1 = +elements[21];
    values.soc2 = +elements[22];
    // smart home
    for (i = 0; i < 10; i++) {
      values["sh" + i] = this.calcValue(26 + i, elements, oldElements);
    }
    //consumers
    values.co0 = this.calcValue(10, elements, oldElements);
    values.co1 = this.calcValue(12, elements, oldElements);
    //battery
    values.batIn = this.calcValue(8, elements, oldElements);
    values.batOut = this.calcValue(9, elements, oldElements);
    values.batterySoc = +elements[20];
    // calculated values
    values.housePower = values.gridPull + values.solarPower + values.batOut
      - values.gridPush - values.batIn - values.charging - values.co0 - values.co1
      - values.sh0 - values.sh1 - values.sh2 - values.sh3 - values.sh4 - values.sh5 - values.sh6 - values.sh7 - values.sh8 - values.sh9;
    if (values.housePower < 0) { values.housePower = 0; };
    values.selfUsage = values.solarPower - values.gridPush;
    if (values.selfUsage < 0) { values.selfUsage = 0; };
    return values;
  }

  reset() {
    this.resetLiveGraph();
    this.resetDayGraph();
  }
  resetLiveGraph() {
    // fresh reload of the graph
    this.initialized = false;
    this.initCounter = 0;
    this.initialGraphData = [];
    this.graphData = [];
    this.graphRefreshCounter = 0;
  }
  resetDayGraph() {
    this.initialized = false;
    this.initCounter = 0;
    this.staging = [];
    this.rawData = [];
    this.graphData = [];
  }
  extractLiveValues(payload) {
    const elements = payload.split(",");
    var values = {};
    values.date = new Date(d3.timeParse("%H:%M:%S")(elements[0]));
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
      values["sh" + i] = +elements[20 + i];
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

  calcValue(i, array, oldArray) {
    var val = (array[i] - oldArray[i]) * 12;
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
    this.drawXAxis(svg, width, height);
    this.drawSoc(svg, width, height / 2);
  }

  drawSourceGraph(svg, width, height) {
    const keys = ["batOut", "selfUsage", "gridPush", "gridPull"];
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
    (d.housePower + d.lp0 + d.lp1 + d.lp2 + d.lp3 + d.lp4
      + d.lp5 + d.lp6 + d.lp7 + d.sh0 + d.sh1 + d.sh2 + d.sh3 + d.sh4
      + d.sh5 + d.sh6 + d.sh7 + d.co0 + d.co1 + d.batIn + d.inverter)
    );
    yScale.domain([0, (extent[1])]);
    const keys = ["lp0", "lp1", "lp2", "lp3", "lp4",
      "lp5", "lp6", "lp7",
      "sh0", "sh1", "sh2", "sh3", "sh4",
      "sh5", "sh6", "sh7", "co0", "co1", "housePower", "batIn", "inverter"];

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
    const fontsize = 12;
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
      .attr("font-size", fontsize)
    xAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    xAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
    svg.append("text")
      .attr("x", - this.margin.left)
      .attr("y", height / 2 + 5)
      .attr("fill", this.axiscolor)
      .attr("font-size", fontsize)
      .text("kW")
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
        .attr("stroke-width", 1)
        .attr("fill", "none")
        //.style("stroke-dasharray", ("3, 3"))
        .attr("d", d3.line()
          .x((d, i) => xScale(this.graphData[i].date))
          .y(d => yScale(d.batterySoc))
        );
      svg.append("path")
        .datum(this.graphData)
        .attr("stroke", this.batteryColor)
        .attr("stroke-width", 1)
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
    socAxis.selectAll(".tick").attr("font-size", 12);
    socAxis.selectAll(".tick line").attr("stroke", this.bgcolor);
    socAxis.select(".domain")
      .attr("stroke", this.bgcolor)
      ;
  }
}

function shiftLeft() {
  if (wbdata.showLiveGraph) {
    wbdata.showLiveGraph = false;
    powerGraph.deactivateLive();
    powerGraph.activateDay();
    wbdata.prefs.showLG = false;
    wbdata.persistGraphPreferences();
    d3.select("button#graphRightButton").classed("disabled", false)
  } else {
    powerGraph.graphDate.setTime(powerGraph.graphDate.getTime() - 86400000);
    powerGraph.activateDay();
  }
}
function shiftRight() {
  today = new Date();
  d = powerGraph.graphDate;
  if (d.getDate() == today.getDate() && d.getMonth() == today.getMonth() && d.getFullYear() == today.getFullYear()) {
    if (!wbdata.showLiveGraph) {
      wbdata.showLiveGraph = true;
      powerGraph.deactivateDay();
      powerGraph.activateLive();
      wbdata.prefs.showLG = true;
      wbdata.persistGraphPreferences();
      d3.select("button#graphLeftButton").classed("disabled", false)
      d3.select("button#graphRightButton").classed("disabled", true)
    }
  } else {
    powerGraph.graphDate.setTime(powerGraph.graphDate.getTime() + 86400000);
    powerGraph.activateDay();
  }
}

var powerGraph = new PowerGraph();

