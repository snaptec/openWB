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
    this.tbody=null;
    this.footer=null;
  };

    // initialize after document is created
  init() {
    const div = d3.select("div#chargePointTable")
    this.cplist = div.append("div")
      .attr("class", "container-fluid");

    this.footer = div.append("div");
    this.fgColor = "var(--color-fg)";  }

  // update if data has changed
  update() {
    this.updateValues();
    this.cplist.selectAll("*").remove();
    this.footer.selectAll("*").remove();
   
    const chargePoint = this.cplist
      .selectAll("rows")
      .data(this.chargepoints).enter()

      ;
    const rows = chargePoint.append("div")
      .attr("class", "row p-0 mb-4")
      .style ( "background-color","var(--color-bg")
      .append("div").attr("class", "container-fluid");
      
    rows.append((row, i) => this.cpNameButtonCell(row, i));

    const chargeInfo = rows.selectAll("cells")
      .data(row => [
        ["Parameter: " , formatWatt(row.power) + " " + this.phaseSymbols[row.phasesInUse] + " " + row.targetCurrent + " A"],
        ["Geladen: " , formatWattH(row.energy * 1000) + " / " + Math.round(row.energy / row.energyPer100km * 1000) / 10 + " km"]
     ]).enter()
      .append("div")
      .attr("class", "row px-3 py-1 chargePointData")
      .attr("style", "vertical-align:middle;");
      chargeInfo
      .append("div").attr("class", "col px-0")
      .text(data => data[0])
      chargeInfo
      .append("div").attr("class", "col px-0")
      .text(data => data[1]).style("text-align","right");
rows.append ((row,i) => this.cpButtonRow (row,i));
     

  }

  updateValues() {
    this.chargepoints = wbdata.chargePoint.filter((cp,i) => cp.configured && i <3); // limit number of charge points displayed to 3
  }

  cpNameButtonCell(row, index) {
    const nameRow = d3.create("div").classed("row", true)
    const nameCell = nameRow
      .append("div")
        .attr("class", "col-8  px-2 py-0 chargePointName")
        .style("color", row.color)
        .style("vertical-align", "middle")
        .style ("text-align", "left")
        .attr("onClick", "lpButtonClicked(" + index + ")");

    if (row.isEnabled) {
      nameCell.append("span")
        .attr("class", "fa fa-toggle-on text-green px-0")
    } else {
      nameCell.append("span")
        .attr("class", "fa fa-toggle-off text-red px-0")
    }

    nameCell
      .append("span").text(row.name)
      .attr("class", "px-2");

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
    const socCell = nameRow
    .append("div")
      .attr("class", "col-4  px-1 py-0 chargePointName")
      .style("color", row.color)
      .style("vertical-align", "middle")
      .style ("text-align", "right")
      .attr("onClick", "lpButtonClicked(" + index + ")");


    if (row.isSocConfigured) {
      socCell.append("span").text(row.soc + " %")
        .attr("class", "px-2");
    }
    return nameRow.node();
  }

  cpButtonRow (row, index) {
    const chargeModes = ["Sofort", "Min & PV", "PV", "Stop", "Standby"]
  
    const buttonRow = d3.create("div").attr ("class", "row pt-3 pb-1")
        
    const modeButton = buttonRow.append ("div").attr ("class", "col-6 m-0 px-1")
      .append ("button")
      .attr("class", "btn btn-block btn-success display-button chargeModeSelectBtn px-1")
      .attr("type", "button")
      .on("click", () => {
          $("#chargeModeModal").modal("show");      
      })
     modeButton
     .append ("span").attr("class","chargeModeSelectBtnText" )
     .text(chargeModes[wbdata.chargeMode])
    modeButton.append ("span").attr("class", "priorityEvBattery hide")
          .append ("span").attr("class", "fas fa-car priorityEvBatteryIcon")
     .text(" ")

     const configButton = buttonRow.append("div").attr ("class", "col-6 m-0 px-1")
     .append ("button")
     .attr ("class", "btn btn-block btn-outline-secondary display-button ladepunktConfigBtn px-1 ")
     .attr ("type", "button")
     .on("click", () => {
        if (displaylocked == false) {
            // currentLp = parseInt($(this).closest('[data-lp]').data('lp'));  // get attribute lp-# of parent element
            $('#ladepunktConfigModal').find('.configLp').text(index+1);
            $('#ladepunktConfigModal').find('[data-config-lp]').addClass('hide');
            $('#ladepunktConfigModal').find('[data-config-lp="' + (index+1) + '"]').removeClass('hide');
            $('#ladepunktConfigModal').modal("show");
        } else {
            $("#lockInfoModal").modal("show");
        }
    });
     

     const buttonText = configButton.append("span")
     
     configButton.append ("i").attr("class", "fas fa-wrench")
     configButton.append("text").html('&nbsp;&nbsp;')
     configButton.append("text").text(" Konfig")
     
     return buttonRow.node()
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

var chargePointList = new ChargePointList();
