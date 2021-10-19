/** 
 * List the configured chargepoints and their key data
 * 
 */

class ChargePointList {

  constructor() {
    this.chargepoints = [];
    this.phaseSymbols = ['/', '\u2460', '\u2461', '\u2462']
    this.headers = ["Ladepunkt", "Ladeparameter", "geladen", "Ladestand"];
    this.manualSoc = 0;
    this.tbody = null;
    this.footer = null;
  };

  // initialize after document is created
  init() {
    this.cplist = d3.select("div#chargePointTable")
    // this.cplist.attr("class", "container-fluid m-0 p-0");

    this.footer = this.cplist.append("div");
    this.fgColor = "var(--color-fg)";
  }

  // update if data has changed
  update() {
    this.updateValues();
    this.cplist.selectAll("*").remove();
    this.footer.selectAll("*").remove();

    const chargePoint = this.cplist
      .selectAll("rows")
      .data(this.chargepoints).enter()
      .append("div").attr("class", "container-fluid mt-3 p-0")
      ;
    chargePoint.html((row, index) => `
      <div class="row m-0 p-0" onclick="modeButtonClicked(${row.isEnabled},${index})">
        ${this.cpNameRow(row)}
      </div>
      <div class = "row m-0 p-0" onclick="modeButtonClicked(${row.isEnabled},${index})">
        ${this.cpChargeInfoRow(row)}
      </div>
      <div class = "row m-0 p-0">
        ${this.cpChargeModeRow(row, index)}
      </div>`
    )
    
  }

  updateValues() {
    this.chargepoints = wbdata.chargePoint.filter((cp, i) => cp.configured && i < 3); // limit number of charge points displayed to 3
  }

  cpNameRow(row) {
    let plugColor = row.isCharging ? "text-green" : "text-orange";
    let plugIcon = !row.isPluggedIn ? "" : `
      <span class="fa fa-xs fa-plug ${plugColor}"/></span>
      `
    let finishIcon = !row.willFinishAtTime ? "" : `
      <span class="fa fa-xs fa-flag-checkered pl-0" style="color:${this.fgColor};"/></span>
    `
    let nightIcon = !row.chargeAtNight ? "" : `
      <span class="fa fa-xs fa-moon pl-0" style="color:${this.fgColor};"></span>
    `
    return `
        <div class = "col px-0 py-0 chargePointName"
          style="color:${row.color};vertical-align:middle;text-align:left;">
          <span class="px-0">${row.name}</span>
          ${plugIcon}
          ${finishIcon}
          ${nightIcon}
        </div>
      `
  }

  cpChargeInfoRow(row) {
    let soctext = row.isSocConfigured ? row.soc + " %" : " ";
    let powerString = formatWatt(row.power) + " " + this.phaseSymbols[row.phasesInUse] + row.targetCurrent + " A";
    let energyString = formatWatt(row.energy * 1000) + " / " + Math.round(row.energy / row.energyPer100km * 1000) / 10 + " km"
    return `
      <div class="col-4 px-0 py-0 chargePointName" style="color:${row.color};text-align:left">
        <span class="px-0 " style="vertical-align:middle;">
          ${soctext}
        </span>
      </div>
      <div class="col-8  pl-0 pr-2 py-0 chargePointData" 
        style="color:white;vertical-align:middle;text-align:right;">
        <p class="px-0 pb-0 mb-0">
          ${powerString} 
        </p>
        <p class="px-0 mb-0">
          ${energyString}
        </p>
      </div>
      `
  }

  cpChargeModeRow(row, index) {
    const chargeModes = ["Sofort", "Min & PV", "PV", "Stop", "Standby"]
    var priorityIcon = "";
    if (wbdata.isBatteryConfigured && (wbdata.chargeMode == 1 || wbdata.chargeMode == 2)) {
      priorityIcon = wbdata.hasEVPriority ? "fa-car" : "fa-car-battery"
    }
    var modeButtonText = ""
    if (row.isEnabled) {
      modeButtonText = `
        <span class="text-white;">${chargeModes[wbdata.chargeMode]}</span>
        <span class="priorityEvBattery">
          <span class="fas ${priorityIcon} px-2"> </span>
        </span>`
    } else {
      modeButtonText = `<span class="text-red">Inaktiv</span>`
    }
    return `
      <div class="col-7 m-0 px-0 py-0">
        <button class="btn btn-block btn-success display-button px-0 py-3" 
        type="button" onclick="modeButtonClicked(${row.isEnabled},${index})">
          ${modeButtonText}
        </button>
      </div>
      <div class="col-5 m-0 px-1 py-0">
        <button class="btn btn-block btn-outline-secondary display-button px-0 mx-0  py-3"
          type="button" onclick = "configButtonClicked(${index})">
          <i class="fas fa-wrench"></i>
        </button>
      </div>`
  }


  editManualSoc(i) {
    this.manualSoc = wbdata.chargePoint[i].soc;
    const div = d3.select("div#socSelector");
    div.selectAll("*").remove();

    const col = div.append("div")
      .style("background-color", "steelblue")
      .attr("class", "px-2 py-1");

    col.append("div")
      .attr("class", "row justify-content-center")
      .append("p")
      .attr("class", "largeTextSize popup-header")
      .style("text-align", "center")
      .text("Manuelle SoC-Eingabe - Ladepunkt " + (i + 1));

    const row2 = col.append("div")
      .attr("class", "row justify-content-center")
    row2.append("div")
      .attr("class", "col-2 px-1 py-1")
      .append("button")
      .attr("class", "btn btn-block btn-sm btn-secondary")
      .text("-")
      .on("click", () => {
        if (this.manualSoc > 0) {
          this.manualSoc--;
        }
        box.node().value = this.manualSoc;
      });
    const col22 = row2.append("div").attr("class", "col-5 py-1")
      .append("div").attr("class", "input-group");
    const box = col22.append("input")
      .attr("type", "text")
      .attr("value", this.manualSoc)
      .attr("class", "form-control text-right")
      .on("input", () => {
        const v = box.node().value;
        if (v >= 0 && v <= 100) {
          this.manualSoc = box.node().value;
        }
      });
    col22.append("div").attr("class", "input-group-append")
      .append("div").attr("class", "input-group-text")
      .text("%");
    row2.append("div").attr("class", "col-2 px-1 py-1")
      .append("button")
      .attr("class", "btn btn-block btn-sm btn-secondary")
      .text("+")
      .on("click", () => {
        if (this.manualSoc < 100) {
          this.manualSoc++;
        }
        box.node().value = this.manualSoc;
      });

    const row3 = col.append("div").attr("class", "row justify-content-center");
    const button1 = row3.append("button")
      .attr("type", "submit")
      .attr("class", "btn btn-sm  btn-secondary")
      .text("Abbrechen")
      .on("click", () => {
        div.selectAll("*").remove();
      })
    const button2 = row3.append("button")
      .attr("id", "socSubmitButton")
      .attr("class", "btn btn-sm btn-primary")
      .text("Übernehmen")
      .on("click", () => {
        publish("" + this.manualSoc, "openWB/set/lp/" + (i + 1) + "/manualSoc");
        div.selectAll("*").remove();
      })
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
  if (wbdata.chargePoint[i].isSocManual) {
    chargePointList.editManualSoc(i);
  } else {
    publish("1", "openWB/set/lp/" + (+i + 1) + "/ForceSoCUpdate");
    d3.select("i#soclabel-" + i)
      .classed("fa-spin", true)
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

function configButtonClicked(index) {
  if (displaylocked == false) {
    $('#ladepunktConfigModal').find('.configLp').text(index + 1);
    $('#ladepunktConfigModal').find('[data-config-lp]').addClass('hide');
    $('#ladepunktConfigModal').find('[data-config-lp="' + (index + 1) + '"]').removeClass('hide');
    $('#ladepunktConfigModal').modal("show");
  } else {
    $("#lockInfoModal").modal("show");
  }
}

function modeButtonClicked(isEnabled, index) {
  if (displaylocked == false) {
    let div = d3.select("div#disableButton");
    div.selectAll("*").remove();
    let buttonText = (isEnabled ? "LP Deaktivieren" : "LP Aktivieren")
    let b = div.append("button")
      .attr("type", "button")
      .text(buttonText)
      .attr("class", "chargeModeBtn chargeModeBtnDisable btn btn-lg btn-block")
      .attr("data-dismiss","modal")
      .on("click", () => {
        lpButtonClicked(index)
      })
    b.classed("btn-danger", isEnabled)
    b.classed("btn-info", !isEnabled)

    $("#chargeModeModal").modal("show");
  } else {
    $("#lockInfoModal").modal("show");
  }
}
var chargePointList = new ChargePointList();
