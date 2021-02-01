/** 
 * List the configured chargepoints and their key data
 * 
 */

class ChargePointList {
  tbody;
  footer;

  constructor() {
    this.chargepoints = [];
    this.phaseSymbols = ['/', '\u2460', '\u2461', '\u2462']
    this.headers = ["Ladepunkt", "Ladeparameter", "geladen", "Ladestand"];
  };

  // initialize after document is created
  init() {
    const div = d3.select("div#chargePointTable")
    const table = div.append("table")
      .attr("class", "table table-borderless p-0 m-0");

    table.append("thead")
      .append("tr")
      .selectAll("headers")
      .data(this.headers).enter()
      .append("th")
      .attr("class", "tablecell")
      // .style("color", "white")
      .style("text-align", (data,i) => (i==0) ? "left" : "center" )
      //.classed ("tablecell", true)
      //.classed ("px-1", true)
      .text((data) => data)
      ;

    this.tbody = table.append("tbody");
    this.footer = div.append("div");
  }

  // update if data has changed
  update() {
    this.updateValues();
    this.tbody.selectAll("*").remove();
    this.footer.selectAll("*").remove();

    const chargePoint = this.tbody
      .selectAll("rows")
      .data(this.chargepoints).enter()
      ;
    const rows = chargePoint.append("tr")
      .style("color", "white")
      .style("text-align", "center")
      .style("vertical-align", "middle");

    rows.append((row, i) => this.cpNameButtonCell(row, i));

    rows.selectAll("cells")
      .data(row => [
        formatWatt(row.power) + " " + this.phaseSymbols[row.phasesInUse] + " " + row.targetCurrent + " A",
        formatWattH(row.energy*1000) + " / " + Math.round(row.energy / row.energyPer100km * 1000) / 10 + " km"
        
      ]).enter()
      .append("td")
      .attr("class", "tablecell px-1 py-1")
      .attr("style", "vertical-align:middle;")
      .text(data => data);
    rows.append((row, i) => this.cpSocButtonCell(row, i));
    
    if (wbdata.isPriceChartEnabled) {
      this.footer.append ('p')
      .attr ("class", "pt-3 pb-0 m-0")
      .style("text-align" ,"center")
        .text ("Aktueller Strompreis: " + wbdata.currentPowerPrice + " Cent/kWh");
    }
  }

  updateValues() {
    this.chargepoints = wbdata.chargePoint.filter(cp => cp.configured);
  }

  cpNameButtonCell(row, index) {
    const cell = d3.create("td")
      .attr("class", "tablecell px-1 py-1")
      .style ("color", row.color)
      .style ("vertical-align", "middle")
      .style ("text-align", "left")
      .attr("onClick", "lpButtonClicked(" + index + ")");
    
      if (row.isEnabled) { 
        cell.append("span")
        .attr("class", "fa fa-toggle-on text-green px-0")
       } else {
        cell.append("span")
         .attr("class", "fa fa-toggle-off text-red px-0")
      }

      cell
      .append("span").text(row.name)
      .attr("class", "px-2");
    
    if (row.isPluggedIn) {
      const span = 
      cell.append("span")
        .attr("class", "fa fa-xs fa-plug")
        ;
        span.classed("text-orange", (!row.isCharging))
        span.classed("text-green", row.isCharging)
    }
    if (row.willFinishAtTime) {
      cell.append("span")
        .attr("class", "fa fa-xs fa-flag-checkered");
    }
    if (row.chargeAtNight) {
      cell.append("span")
        .attr("fa fa-xs fa-moon");
    }

    
    return cell.node();
  }

  cpSocButtonCell(row, index) {
    const cell = d3.create("td")
      .attr("class", "tablecell px-1 py-1")
      .attr("onClick", (row) => ("socButtonClicked(" + index + ")"))
      .style("text-align", "center")
      .style("vertical-align", "middle");
    if (row.isSocConfigured) {
      cell.append("span").text(row.soc + " %")
      .attr ("class", "px-2");
      cell.append("i")
      .attr("class", "small fas fa-redo-alt")
      .attr("id", "soclabel-" + index)
      .style("color", "white");
    
    }
    return cell.node();
  }


}
function lpButtonClicked(i) {
  if (wbdata.chargePoint[i].isEnabled) {
    publish("0", "openWB/set/lp/" + (+i + 1) + "/ChargePointEnabled");
  } else {
    publish("1", "openWB/set/lp/" + (+i + 1) + "/ChargePointEnabled");
  }
  d3.select("button#lpbutton-" + i)
    .classed("disabled", true);
}

function socButtonClicked(i) {
  publish("1", "openWB/set/lp/" + (+i + 1) + "/ForceSoCUpdate");
  d3.select("i#soclabel-" + i)
    .classed("fa-spin", true)
}

function socButtonClicked(i) {
  publish("1", "openWB/set/lp/" + (+i + 1) + "/ForceSoCUpdate");
  d3.select("i#soclabel-" + i)
    .classed("fa-spin", true)
}

var chargePointList = new ChargePointList();
