/**
 * Show the current power production and consumption in a donut
 *
 * @author Claus Hagen
 */

class PowerMeter {
  constructor() {
    this.width = 500;
    this.height = this.width;
    this.margin = 45;
    this.radius = this.width / 2 - this.margin;
    this.cornerRadius = 1;
    this.shapefactor = (Math.PI / 40);
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
    this.addLabel(svg, -this.width / 2 + this.margin / 4, -this.height / 2 + this.margin - 10, "left", wbdata.sourceSummary[1]);
    this.addLabel(svg, 0, -this.height / 2 + this.margin - 20, "middle", wbdata.sourceSummary[0]);
    this.addLabel(svg, this.width / 2 - this.margin / 4, -this.height / 2 + this.margin - 10, "end", wbdata.sourceSummary[2]);
    this.addLabel(svg, -this.width / 2 + this.margin / 4, this.height / 2 - this.margin, "left", wbdata.usageSummary[0]);
    this.addLabel(svg, 0, this.height / 2 - this.margin + 20, "middle", wbdata.usageSummary[1]);
    this.addLabel(svg, this.width / 2 - this.margin / 4, this.height / 2 - this.margin, "end", wbdata.usageSummary[2]);

    const solarfraction = Math.round(wbdata.pvwatt / (wbdata.housePower + wbdata.usageSummary[1].power + wbdata.usageSummary[2].power) * 100);
    svg.append("text")
      .attr("x", 0)
      .attr("y", -(this.height / 8))
      //.attr ("dy", "1em")
      .text("Eigenproduktion: \n " + solarfraction + " % ")
      .attr("fill", this.pvColor)
      .style("text-anchor", "middle")
      .style("font-size", "24")
      ;

    if (wbdata.chargePoint[0].isSocConfigured) {
      svg.append("text")
        .attr("x", 0)
        .attr("y", 0)

        .text("SOC (" + wbdata.chargePoint[0].name + "): " + (wbdata.chargePoint[0].soc) + " %")
        .attr("fill", this.chargeColor)
        .attr("backgroundcolor", this.bgColor)
        .style("text-anchor", "middle")
        .style("font-size", "24");
    }
    svg.append("text")
      .attr("x", 0)
      .attr("y", this.height / 8)
      .text("Verbrauch: " + formatWatt(wbdata.housePower + wbdata.usageSummary[1].power + wbdata.usageSummary[2].power))
      .attr("fill", this.houseColor)
      .attr("backgroundcolor", this.bgColor)
      .style("text-anchor", "middle")
      .style("font-size", "24")
      ;
  }

  drawSourceArc(svg) {
    // Define the generator for the segments
    const pieGenerator = d3.pie()
      .value((record) => Number(record.power))
      .startAngle(-Math.PI / 2 + this.shapefactor)
      .endAngle(Math.PI / 2 - this.shapefactor);

    // Generator for the pie chart
    const arc = d3.arc()
      .innerRadius(this.radius / 4 * 3)
      .outerRadius(this.radius)
      .cornerRadius(this.cornerRadius);

    // Add the chart to the svg
    svg.selectAll("sources")
      .data(pieGenerator(wbdata.sourceSummary)).enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => d.data.color);
  }

  drawUsageArc(svg) {

    // Define the generator for the segments
    const pieGenerator = d3.pie()
      .value((record) => Number(record.power))
      .startAngle(Math.PI * 1.5 - this.shapefactor)
      .endAngle(Math.PI / 2 + this.shapefactor);

    // Generator for the pie chart
    const arc = d3.arc()
      .innerRadius(this.radius / 4 * 3)
      .outerRadius(this.radius)
      .cornerRadius(this.cornerRadius);

    // Add the chart to the svg
    svg.selectAll("consumers")
      .data(pieGenerator(wbdata.usageDetails)).enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => d.data.color);
  }

  addLabel(svg, x, y, anchor, data) {
    const labelFontSize = 22;
    svg
      .append("text")
      .attr("x", x)
      .attr("y", y)
      .attr("dy", ".35em")
      .text(data.name + " : " + formatWatt(data.power))
      .attr("fill", data.color)
      .attr("text-anchor", anchor)
      .style("font-size", labelFontSize)
      ;
  }

  calcColor(row) {
    return ("color:" + row.color + "; text-align:center");
  }
}

var powerMeter = new PowerMeter();
