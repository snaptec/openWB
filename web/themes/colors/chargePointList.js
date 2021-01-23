/** 
 * List the configured chargepoints and their key data
 * 
 */

class ChargePointList {
  tbody;
  formSection;

  constructor() {
    this.chargepoints = [];
    this.phaseSymbols = ['/', '\u2460', '\u2461', '\u2462']
    this.headers = ["Ladepunkt", "Ladeparameter", "geladen", "Soc"];
  };

  // initialize after document is created
  init() {
    const div = d3.select ("div#chargePointTable")
    const table = div.append("table")
      .attr("class", "table table-borderless p-0 m-0");
    
    table.append("thead")
      .append("tr")
      .selectAll("headers")
      .data(this.headers).enter()
      .append("th")
      .attr("class", "tablecell")
      .style("color", "white")
      .style("text-align", "center")
      //.classed ("tablecell", true)
      //.classed ("px-1", true)
      .text((data) => data)
      ;

    this.tbody = table.append ("tbody");
    this.formSection = div.append("div");
  }

  // update if data has changed
  update() {
    this.updateValues();
    this.tbody.selectAll("*").remove();
    this.formSection.selectAll("*").remove();

    const rows = this.tbody
      .selectAll("rows")
      .data(this.chargepoints).enter()
      .append("tr")
      .style("color", row => row.color)
      .style("text-align", "center")
      .style("vertical-align", "middle");

    rows.append((row, i) => this.cpNameButtonCell(row, i));

    rows.selectAll("cells")
      .data(row => [
        formatWatt(row.power) + " " + this.phaseSymbols[row.phasesInUse] + " " + row.targetCurrent + " A",
        row.energy + " kWh / " + Math.round(row.energy / row.energyPer100km * 1000) / 10 + " km"
        //  row.soc + " %"
      ]).enter()
      .append("td")
      .attr("class", "tablecell px-1 py-1")
      .attr("style", "vertical-align:middle;")
      .text(data => data);
    rows.append((row, i) => this.cpSocButtonCell(row, i));

  }


 

  updateValues() {
    this.chargepoints = wbdata.chargePoint.filter(cp => cp.configured);
  }

  cpNameButtonCell(row, index) {
    const cell = d3.create("td")
      .attr("class", "tablecell px-1 py-1");
    const button = cell
      .append("button")
      .attr("class", "btn btn-sm")
      .attr("id", "lpbutton-" + index)
      .style("text-align", "center")
      .style("vertical-align", "middle")
      .style("color", row.color)
      .classed("disabled", false)
      .attr("onClick", (row, i) => ("lpButtonClicked(" + i + ")"));
    button
      .text(row.name);

    if (row.isEnabled) {
      button.classed("btn-outline-success", true);
    } else {
      button.classed("btn-outline-danger", true);
    }
    button.append("span").text(" ");
    if (row.isPluggedIn) {
      button.append("span")
        .attr("class", "fa fa-xs fa-plug text-orange ")
        ;
    }
    if (row.willFinishAtTime) {
      button.append("span")
        .attr("class", "fa fa-xs fa-flag-checkered");
    }
    if (row.chargeAtNight) {
      button.append("span")
        .attr("fa fa-xs fa-moon");
    }
    return cell.node();
  }

  cpSocButtonCell(row, index) {

    const cell = d3.create("td")
      .attr("class", "tablecell px-1 py-1")
      .style("text-align", "center")
      .style("vertical-align", "middle");
    if (row.isSocConfigured) {
      cell.text(row.soc + " %");
      cell.append("span").text("   ");
      const button = cell
        .append("button")
        .attr("class", "btn btn-outline-basic px-2 pt-0 mt-0 pb-1")
        .style("text-align", "center")
        .style("vertical-align", "middle")
        .style("color", "white")
        .attr("onClick", (row, i) => ("socButtonClicked(" + i + ")"))
      button.append("i")
        .attr("class", "small reloadLpSoc fas fa-redo-alt")
        .attr("id", "soclabel-" + index)
        ;
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

var chargePointList = new ChargePointList();
