/** 
 * List the configured chargepoints and their key data
 * 
 */

class SmartHomeList {

  div;

  constructor() {
    var consumers = [];
  };

  // initialize after document is created
  init() {
    this.div = d3.select("div#smartHomeTable");
  }

  // update if data has changed
  update() {
    this.updateValues();
    this.div.selectAll("*").remove();

    if (this.consumers.length > 0) {
      d3.select("div#smartHomeWidget").classed("hide", false);
      var table = this.div.append("table")
        .attr("class", "table table-borderless table-condensed p-0 m-0");
      
      const headers = ["Gerät", "Verbrauch", "Laufzeit", "Modus"];
      const thead = table.append("thead");
      thead
        .selectAll("headers")
        .data(headers).enter()
        .append("th")
        .attr("style", (data, i) => (i == 0) ? "text-align:left;"
          : "text-align:center;")
        .attr("class", "tablecell ")
        .text((data) => data)
        ;
      thead.append("th")
        .attr("style", "text-align:right")
        .attr("class", "tablecell")
        .append("span")
        .attr("class", "fa fa-chart-area px-0");

      const rows = table.append("tbody").selectAll("rows")
        .data(this.consumers).enter()
        .append("tr")
        .attr("style", row => this.calcColor(row));

      const cell = rows.append("td")
        .attr("class", "tablecell py-1 px-1")
        .attr("onClick", (row) => "shDeviceClicked(" + row.id + ")")
        .attr("id", (row, i) => "shbutton-" + i)
        .attr("style", "text-align:left; vertical-align:middle;");
      // status indicator
      cell.append("span")
        .attr("id", (row) => "shbutton-" + row.id)
        .attr("class", (row) => row.isOn ? "fa fa-toggle-on text-green pr-2" : "fa fa-toggle-off text-red pr-2");
      // name
      cell.append("span")
        .text(row => row.name);
      // Power/energy
      rows.append("td")
        .attr("class", "tablecell py-1 px-1")
        .attr("style", "vertical-align: middle;color:var(--color-fg)")
        .text(row => formatWatt(row.power) + " (" + formatWattH(row.energy * 1000) + ")");
      // Running time
      rows.append("td")
        .attr("class", "tablecell py-1 px-1")
        .attr("style", "vertical-align: middle;color:var(--color-fg)")
        .text(row => formatTime(row.runningTime))
      // Automatic mode button
      rows.append("td")
        .attr("class", "tablecell py-1 px-1")
        .append("button")
        .attr("id", (row) => "shmodebutton-" + row.id)
        .attr("class", row => this.modeClass(row))
        .attr("style", "color:var(--color-fg); text-align:center;")
        .attr("onClick", (row) => "shModeClicked(" + row.id + ")")
        .classed("disabled", false)
        .text(row => row.isAutomatic ? "Automatik" : "Manuell");
      // select graph display
      rows.append("td")
        .attr("class", "tablecell py-1 px-1")
        .append("div")
        .attr("class", "form-check")
        .style("text-align", "right")
        .append("input")
        .attr("type", "checkbox")
        .attr("name", "graphswitch")
        .attr("class", "form-check-input")
        .property("checked", row => row.showInGraph)
        .attr("id", (row) => row.id)
        ;

      d3.selectAll("[name=graphswitch]")
        .on("change", function () {
          wbdata.updateSH(+this.id + 1, "showInGraph", this.checked);
        })

    }
    else {
      d3.select("div#smartHomeWidget").classed("hide", true);
    }
  }

  calcColor(row) {
    return ("color:" + row.color + "; text-align:center");
  }

  buttonClass = "btn btn-sm";

  deviceClass(row) {
    return (this.buttonClass + (row.isOn ? " btn-outline-success" : " btn-outline-danger"));
  }

  modeClass(row) {
    return (this.buttonClass + (row.isAutomatic ? " btn-outline-info" : " btn-outline-warning"));
  }

  updateValues() {
    this.consumers = wbdata.shDevice.filter((dv) => dv.configured);
  }
}

function shModeClicked(i) {
  // send mqtt set to enable/disable Device after click
  if (wbdata.shDevice[i].isAutomatic) {
    publish("1", "openWB/config/set/SmartHome/Devices/" + (+i + 1) + "/mode");
  } else {
    publish("0", "openWB/config/set/SmartHome/Devices/" + (+i + 1) + "/mode");
  }
  d3.select("button#shmodebutton-" + i)
    .classed("disabled", true);
};

function shDeviceClicked(i) {

  if (!wbdata.shDevice[i].isAutomatic) {
    if (wbdata.shDevice[i].isOn) {
      publish("0", "openWB/config/set/SmartHome/Device" + (+i + 1) + "/device_manual_control");
    } else {
      publish("1", "openWB/config/set/SmartHome/Device" + (+i + 1) + "/device_manual_control");
    }
    d3.select("span#shbutton-" + i)
      .attr("class", "fa fa-clock text-white pr-2")
      ;
  }
}

function toggleGraphDisplay(i) {
  console.log("toggle graph display");
  const checkbox = d3.select("input#graphcheckbox-" + i)

}

var smartHomeList = new SmartHomeList();



