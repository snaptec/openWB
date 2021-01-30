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
  }

  // public method to initialize
  init() {
    const figure = d3.select("figure#powermeter");
    this.svg = figure.append("svg")
      .attr("viewBox", `0 0 500 500`);
    const style = getComputedStyle(document.body);
    this.houseColor = style.getPropertyValue('--color-house');
    this.pvColor = style.getPropertyValue('--color-pv');
    this.exportColor = style.getPropertyValue('--color-export');
    this.gridColor = style.getPropertyValue('--color-evu');
    this.bgColor = style.getPropertyValue('--color-bg');
    this.chargeColor = style.getPropertyValue('--color-charging');
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
    this.drawSourceArc(svg);
    this.drawUsageArc(svg);

    this.addLabel(svg, 0, -this.height / 2 * 3 / 5, "middle", wbdata.sourceSummary.pv); // PV
    this.addLabel(svg, 0, -this.height / 2 * 2 / 5, "middle", wbdata.sourceSummary.evuIn); // Netz
    this.addLabel(svg, this.width / 2 - this.margin / 4, this.height / 2 - this.margin + 15, "end", wbdata.sourceSummary.batIn); // Speicher Out
    this.addLabel(svg, 0, -this.height / 2 * 2 / 5, "middle", wbdata.usageSummary[0]);  // Export
    this.addLabel(svg, 0, this.height / 2 * 1 / 5, "middle", wbdata.usageSummary[1]); // Laden
    this.addLabel(svg, 0, this.height / 2 * 3 / 5, "middle", wbdata.usageSummary[2]); // Geräte
    this.addLabel(svg, this.width / 2 - this.margin / 4, this.height / 2 - this.margin + 15, "end", wbdata.usageSummary[3]); // Speicher in
   // this.addLabel(svg, -this.width / 2 + this.margin / 4, this.height / 2 - this.margin, "start", wbdata.batterySoc); // Speicher in
    this.addLabel(svg, 0, this.height / 2 * 2 / 5, "middle", wbdata.usageSummary[4]);  // Haus

    if (wbdata.chargePoint[0].isSocConfigured) {
      this.addLabelWithColor (svg, 
        (-this.width/2 - this.margin/4 +5), 
        (-this.height/2 + this.margin + 5), 
        "start", 
        (wbdata.chargePoint[0].name + ": " + (wbdata.chargePoint[0].soc) + "%"), 
        wbdata.chargePoint[0].color);
    }
  
    if (wbdata.chargePoint[1].isSocConfigured) {
      this.addLabelWithColor (svg, 
        (this.width/2 + this.margin/4 -5), 
        (-this.height/2 + this.margin + 5), 
        "end", 
        (wbdata.chargePoint[1].name + ": " + (wbdata.chargePoint[1].soc) + "%"), 
        wbdata.chargePoint[1].color);
    }
    if (wbdata.batterySoc > 0)  {
    this.addLabelWithColor (svg, 
      (-this.width/2 - this.margin/4 +5), 
      (this.height/2 - this.margin +15), 
      "start", 
      ("Speicher: " + wbdata.batterySoc + "%"), 
      wbdata.usageSummary[3].color);
    }

    svg.append("text")
      .attr("x", 0)
      .attr("y", 0)
      .text("Aktueller Verbrauch: " + formatWatt(wbdata.housePower + wbdata.usageSummary[1].power + wbdata.usageSummary[2].power + wbdata.usageSummary[3].power))
      .attr("fill", "white")
      .attr("backgroundcolor", this.bgColor)
      .style("text-anchor", "middle")
      .style("font-size", "22")
      ;
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
    svg.selectAll("sources")
      .data(pieGenerator(Object.values (wbdata.sourceSummary))).enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => d.data.color);
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

    // Add the chart to the svg
    svg.selectAll("consumers")
      .data(pieGenerator(wbdata.usageSummary)).enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => d.data.color);
  }

  addLabel(svg, x, y, anchor, data) {
    const labelFontSize = 22;

    if (data.power > 0) {
      svg
        .append("text")
        .attr("x", x)
        .attr("y", y)
        .text(data.name + " : " + formatWatt(data.power))
        .attr("fill", data.color)
        .attr("text-anchor", anchor)
        .style("font-size", labelFontSize)
        ;
    }
  }

  addLabelWithColor (svg, x, y, anchor, labeltext, color) {
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
}

var powerMeter = new PowerMeter();
