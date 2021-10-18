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
    chargePoint.append((row, i) => this.cpNameButtonCell(row, i));
    chargePoint.append((row, i) => this.cpChargeInfoRow(row, i));
    chargePoint.append((row, i) => this.cpChargeModeRow(row, i));
    // chargePoint.append((row, i) => this.cpConfigRow(row, i));
  }

  updateValues() {
    this.chargepoints = wbdata.chargePoint.filter((cp, i) => cp.configured && i < 3); // limit number of charge points displayed to 3
  }

  cpNameButtonCell(row, index) {
    const nameRow = d3.create("div").attr("class", "row  m-0 p-0")
    nameRow.on("click", () => {
      if (displaylocked == false) {
        $("#chargeModeModal").modal("show");
      } else {
        $("#lockInfoModal").modal("show");
      }
    })

    const nameCell = nameRow
      .append("div")
      .attr("class", "col  px-0 py-0 chargePointName")
      .style("color", row.color)
      .style("vertical-align", "middle")
      .style("text-align", "left");

    nameCell
      .append("span").text(row.name)
      .attr("class", "px-0");

    if (row.isPluggedIn) {
      const span =
        nameCell.append("span")
          .attr("class", "fa fa-xs fa-plug")
        ;
      span.classed("text-orange", (!row.isCharging))
      span.classed("text-green", row.isCharging)
    }
    if (row.willFinishAtTime) {
      nameCell.append("span")
        .attr("class", "fa fa-xs fa-flag-checkered pl-1")
        .style("color", this.fgColor);
    }
    if (row.chargeAtNight) {
      nameCell.append("span")
        .attr("class", "fa fa-xs fa-moon pl-1")
        .style("color", this.fgColor)
    }

    return nameRow.node();
  }

  cpChargeInfoRow(row, index) {
    const ciRow = d3.create("div").attr("class", "row m-0 p-0")
    ciRow.on("click", () => {
      if (displaylocked == false) {
        $("#chargeModeModal").modal("show");
      } else {
        $("#lockInfoModal").modal("show");
      }
    })
    const socCell = ciRow
      .append("div")
      .attr("class", "col-4  px-0 py-0 chargePointName")
      .style("color", row.color)
      .style("text-align", "left");

    if (row.isSocConfigured) {
      socCell.append("span").text(row.soc + " %")
        .attr("class", "px-0")
        .style("vertical-align", "middle");
    } else {
      socCell.append("span").html("&nbsp;")
    }

    const infoCell = ciRow.append("div")
      .attr("class", "col-8  pl-0 pr-2 py-0 chargePointData")
      .style("color", row.color)
      .style("vertical-align", "middle")
      .style("text-align", "right");

    infoCell.append("p")
      .attr("class", "px-0 pb-0 mb-0 ")
      .text(formatWatt(row.power) + " " + this.phaseSymbols[row.phasesInUse] + " " + row.targetCurrent + " A")
      .style("color", "white")

    infoCell.append("p")
      .attr("class", "px-0 mb-0 ")
      .text(formatWattH(row.energy * 1000) + " / " + Math.round(row.energy / row.energyPer100km * 1000) / 10 + " km")
      .style("color", "white")

    return ciRow.node()
  }


  cpChargeModeRow(row, index) {
    const chargeModes = ["Sofort", "Min & PV", "PV", "Stop", "Standby"]
    const cmRow = d3.create("div").attr("class", "row m-0 p-0")
    const modeButton = cmRow.append("div").attr("class", "col-7 m-0 px-1 py-0")
      .append("button")
      .attr("class", "btn btn-block btn-success display-button chargeModeSelectBtn px-0 py-3")
      .attr("type", "button")
      .on("click", () => {
        if (displaylocked == false) {
          createDisableButton(row, index);
          $("#chargeModeModal").modal("show");
        } else {
          $("#lockInfoModal").modal("show");
        }
      })
    if (row.isEnabled) {
      modeButton
        .append("span").attr("class", "text-white")
        .text(chargeModes[wbdata.chargeMode])
        if (wbdata.isBatteryConfigured && (wbdata.chargeMode == 1 || wbdata.chargeMode == 2)) {
          if (wbdata.hasEVPriority) {
            modeButton.append("span").attr("class", "priorityEvBattery")
              .append("span").attr("class", "fas fa-car px-2")
              .text(" ")
          } else {
            modeButton.append("span").attr("class", "priorityEvBattery")
              .append("span").attr("class", "fas fa-car-battery px-2")
              .text(" ")
          }
        }
    } else {
      modeButton
        .append("span").attr("class", "text-red")
        .text("Inaktiv")
    }
       const configButton = cmRow.append("div").attr("class", "col-5 m-0 px-1 py-0")
      .append("button")
      .attr("class", "btn btn-block btn-outline-secondary display-button ladepunktConfigBtn px-0 mx-0  py-3 ")
      .attr("type", "button")
      .on("click", () => {
        if (displaylocked == false) {
          $('#ladepunktConfigModal').find('.configLp').text(index + 1);
          $('#ladepunktConfigModal').find('[data-config-lp]').addClass('hide');
          $('#ladepunktConfigModal').find('[data-config-lp="' + (index + 1) + '"]').removeClass('hide');
          $('#ladepunktConfigModal').modal("show");
        } else {
          $("#lockInfoModal").modal("show");
        }
      });


    configButton.append("i").attr("class", "fas fa-wrench")
    return cmRow.node()
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

function createDisableButton(row, index) {
  let div = d3.select("div#disableButton");
  div.selectAll("*").remove();
  let buttonText = (row.isEnabled ? "LP Deaktivieren" : "LP Aktivieren")
  let b = div.append("button")
    .attr("type", "button")
    .text(buttonText)
    .attr("class", "chargeModeBtn chargeModeBtnDisable btn btn-lg btn-block")
    .on("click", () => {
      lpButtonClicked(index)
    })


  b.classed("btn-danger", row.isEnabled)
  b.classed("btn-info", !row.isEnabled)

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

var chargePointList = new ChargePointList();
