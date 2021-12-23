/**
 * Show the current power production and consumption in a donut
 *
 * @author Claus Hagen
 */

class PowerMeter {
  constructor() {
    this.width = 500;
    this.height = this.width;
    this.margin = 20;
    this.radius = this.width / 2 - this.margin;
    this.cornerRadius = 1;
    this.circleGapSize = (Math.PI / 40);
    this.maxPower = 4000;
    this.showRelativeArcs = false;
    this.emptyPower = 0;
  }

  // public method to initialize
  init() {
    const figure = d3.select("figure#powermeter");
    this.svg = figure.append("svg")
      .attr("viewBox", `0 0 500 500`);
    const style = getComputedStyle(document.body);
    this.houseColor = 'var(--color-house)';
    this.pvColor = 'var(--color-pv)';
    this.exportColor = 'var(--color-export)';
    this.gridColor = 'var(--color-evu';
    this.bgColor = 'var(--color-bg)';
    this.chargeColor = 'var(--color-charging)';
    this.axisColor = 'var(--color-axis)';
    this.fgColor = "var(--color-fg)";
    this.scaleColor = "var(--color-scale)";


    d3.select("button#powerMeterButton")
      .on("click", switchDisplay);
    d3.select("button#themeSwitchButton")
      .on("click", switchTheme);
    d3.select("button#meterResetButton")
      .on("click", resetButtonClicked);

  }

  getColor(category) {
    const style = getComputedStyle(document.body);
    switch (category) {
      case "house": return style.getPropertyValue('--color-house');
      case "pv": return style.getPropertyValue('--color-pv');
      case "export": return style.getPropertyValue('--color-export');
      case "grid": return style.getPropertyValue('--color-evu');
      case "bg": return style.getPropertyValue('--color-bg');
      case "charge": return style.getPropertyValue('--color-charge');
      case "axis": return style.getPropertyValue('--color-axis');
      case "fg": return style.getPropertyValue('--color-fg');
      default: return "white";

    }
  }
  // public method to update the graph
  update() {
    var svg = this.createOrUpdateSvg();
    this.drawGraph(svg);
  }

  // create the SVG that will contain our graph, and configure it
  createOrUpdateSvg() {
    this.svg.selectAll("*").remove();
    const g = this.svg
      .append("g")
      .attr(
        "transform",
        "translate(" + this.width / 2 + "," + this.height / 2 + ")"
      );

    return g;
  }

  drawGraph(svg) {
    this.updateDisplayRatio();
    this.drawSourceArc(svg);
    this.drawUsageArc(svg);
    this.addLabel(svg, 0, -this.height / 2 * 3 / 5, "middle", wbdata.sourceSummary.pv); // PV
    this.addLabel(svg, 0, -this.height / 2 * 2 / 5, "middle", wbdata.sourceSummary.evuIn); // Netz
    this.addLabel(svg, this.width / 2 - this.margin / 4, this.height / 2 - this.margin + 15, "end", wbdata.sourceSummary.batOut); // Speicher Out
    this.addLabel(svg, 0, -this.height / 2 * 2 / 5, "middle", wbdata.usageSummary.evuOut);  // Export
    this.addLabel(svg, 0, this.height / 2 * 1 / 5, "middle", wbdata.usageSummary.charging); // Laden
    this.addLabel(svg, 0, this.height / 2 * 3 / 5, "middle", wbdata.usageSummary.devices); // Geräte
    this.addLabel(svg, this.width / 2 - this.margin / 4, this.height / 2 - this.margin + 15, "end", wbdata.usageSummary.batIn); // Speicher in
    this.addLabel(svg, 0, this.height / 2 * 2 / 5, "middle", wbdata.usageSummary.house);  // Haus

    if (wbdata.chargePoint[0].isSocConfigured) {
      this.addLabelWithColor(svg,
        (-this.width / 2 - this.margin / 4 + 10),
        (-this.height / 2 + this.margin + 5),
        "start",
        (wbdata.chargePoint[0].name + ": " + (wbdata.chargePoint[0].soc) + "%"),
        wbdata.chargePoint[0].color);
    }

    if (wbdata.chargePoint[1].isSocConfigured) {
      this.addLabelWithColor(svg,
        (this.width / 2 + this.margin / 4 - 10),
        (-this.height / 2 + this.margin + 5),
        "end",
        (wbdata.chargePoint[1].name + ": " + (wbdata.chargePoint[1].soc) + "%"),
        wbdata.chargePoint[1].color);
    }
    if (wbdata.batterySoc > 0) {
      this.addLabelWithColor(svg,
        (-this.width / 2 - this.margin / 4 + 10),
        (this.height / 2 - this.margin + 15),
        "start",
        ("Speicher: " + wbdata.batterySoc + "%"),
        wbdata.usageSummary.batIn.color);
    }

    if (this.showRelativeArcs) {
      svg.append("text")
        .attr("x", 0)
        .attr("y", 5)
        .text("Verbrauch: " + formatWatt(wbdata.housePower + wbdata.usageSummary.charging.power + wbdata.usageSummary.devices.power + wbdata.usageSummary.batIn.power))
        .attr("fill", this.fgColor)
        .attr("backgroundcolor", this.bgColor)
        .style("text-anchor", "middle")
        .style("font-size", "22")
        ;
      svg.append("text")
        .attr("x", this.width / 2 - 44)
        .attr("y", 2)
        .text("Peak: " + formatWatt(this.maxPower))
        .attr("fill", this.axisColor)
        .attr("backgroundcolor", this.bgColor)
        .style("text-anchor", "middle")
        .style("font-size", "12")
        ;
    } else {
      svg.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .text("Aktueller Verbrauch: " + formatWatt(wbdata.housePower + wbdata.usageSummary.charging.power + wbdata.usageSummary.devices.power + wbdata.usageSummary.batIn.power))
        .attr("fill", this.fgColor)
        .attr("backgroundcolor", this.bgColor)
        .style("text-anchor", "middle")
        .style("font-size", "22")
        ;
    }
    d3.select("a#meterResetButton").classed("hide", !this.showRelativeArcs);
  }

  drawSourceArc(svg) {
    // Define the generator for the segments
    const pieGenerator = d3.pie()
      .value((record) => Number(record.power))
      .startAngle(-Math.PI / 2 + this.circleGapSize)
      .endAngle(Math.PI / 2 - this.circleGapSize)
      .sort(null);

    // Generator for the pie chart
    const arc = d3.arc()
      .innerRadius(this.radius / 6 * 5)
      .outerRadius(this.radius)
      .cornerRadius(this.cornerRadius);

    // Add the chart to the svg
    const arcCount = Object.values(wbdata.sourceSummary).length;

    svg.selectAll("sources")
      .data(pieGenerator(Object.values(wbdata.sourceSummary).concat([{ "power": this.emptyPower, "color": this.bgColor }]))).enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => d.data.color)
      .attr("stroke", (d, i) => (i == arcCount && d.data.power > 0) ? this.scaleColor : "null");
  }

  drawUsageArc(svg) {

    // Define the generator for the segments
    const pieGenerator = d3.pie()
      .value((record) => Number(record.power))
      .startAngle(Math.PI * 1.5 - this.circleGapSize)
      .endAngle(Math.PI / 2 + this.circleGapSize)
      .sort(null);

    // Generator for the pie chart
    const arc = d3.arc()
      .innerRadius(this.radius / 6 * 5)
      .outerRadius(this.radius)
      .cornerRadius(this.cornerRadius);

    // Filter out shared home devices that are included in house consumption
    const plotData = [wbdata.usageSummary.evuOut,  wbdata.usageSummary.charging]
    .concat(wbdata.shDevice.filter(row => (row.configured && !row.countAsHouse)).sort((a,b)=>{return (b.power-a.power)}))
    .concat(wbdata.consumer.filter(row => (row.configured)))
    .concat([wbdata.usageSummary.batIn, wbdata.usageSummary.house])
    .concat([{ "power": this.emptyPower, "color": this.bgColor }]);

    // Add the chart to the svg
    const arcCount = Object.values(plotData).length -1;
    svg.selectAll("consumers")
      .data(pieGenerator(Object.values(plotData))).enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => d.data.color)
      .attr("stroke", (d, i) => (i == arcCount && d.data.power > 0) ? this.scaleColor : "null");
  }

  addLabel(svg, x, y, anchor, data) {
    const labelFontSize = 22;

    if (data.power > 0) {
      svg
        .append("text")
        .attr("x", x)
        .attr("y", y)
        .text(data.name + ": " + formatWatt(data.power))
        .attr("fill", data.color)
        .attr("text-anchor", anchor)
        .style("font-size", labelFontSize)
        ;
    }
  }

  addLabelWithColor(svg, x, y, anchor, labeltext, color) {
    const labelFontSize = 22;
    svg.append("text")
      .attr("x", x)
      .attr("y", y)
      .text(labeltext)
      .attr("fill", color)
      .attr("text-anchor", anchor)
      .style("font-size", labelFontSize)
      ;
  }


  calcColor(row) {
    return ("color:" + row.color + "; text-align:center");
  }

  updateDisplayRatio() {
    if (this.showRelativeArcs) {
      this.displayRatio = (+wbdata.sourceSummary.pv.power + wbdata.sourceSummary.evuIn.power + wbdata.sourceSummary.batOut.power) / this.maxPower;
      this.emptyPower = this.maxPower - (+wbdata.sourceSummary.pv.power + wbdata.sourceSummary.evuIn.power + wbdata.sourceSummary.batOut.power);
      if (this.emptyPower < 0) {
        this.maxPower = +wbdata.sourceSummary.pv.power + wbdata.sourceSummary.evuIn.power + wbdata.sourceSummary.batOut.power;
        this.emptyPower = 0;
        wbdata.prefs.maxPow = this.maxPower;
        wbdata.persistGraphPreferences();
      }
    } else {
      this.emptyPower = 0;
    }
  }

  resetDisplayRatio() {
    this.maxPower = +wbdata.sourceSummary.pv.power + wbdata.sourceSummary.evuIn.power + wbdata.sourceSummary.batOut.power;
    this.emptyPower = 0;
    wbdata.prefs.maxPow = this.maxPower;
    wbdata.persistGraphPreferences();
  }
}

function switchDisplay() {
  powerMeter.showRelativeArcs = powerMeter.showRelativeArcs ? false : true;
  wbdata.prefs.relPM = powerMeter.showRelativeArcs;
  wbdata.persistGraphPreferences();
  powerMeter.update();
}



function switchTheme() {
  const doc = d3.select("html");
  switch (wbdata.displayMode) {
    case "gray": wbdata.displayMode = "light";
      break;
    case "light": wbdata.displayMode = "dark";
      break;
    case "dark": wbdata.displayMode = "gray"
      break;
    default: break;
  }
  doc.classed("theme-dark", (wbdata.displayMode == "dark"));
  doc.classed("theme-light", (wbdata.displayMode == "light"));
  doc.classed("theme-gray", (wbdata.displayMode == "gray"));


  wbdata.persistGraphPreferences();
}
function resetButtonClicked() {
  powerMeter.resetDisplayRatio();
  powerMeter.update();
}
var powerMeter = new PowerMeter();
