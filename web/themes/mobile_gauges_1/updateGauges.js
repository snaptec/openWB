function updateGaugeBottomText(gauge, bottomText, setColor) {
    // gauge: zu erneuernde Gauge
    // bottomText: Text unter der Leistungsanzeige
    // setColor: soll die Textfarbe je nach Wert der Anzeige geändert werden
    // Text unter Leistungsanzeige wie übergeben setzen
    gauge.set('titleBottom', bottomText);
    // Farben der Schrift ggf. anpassen
    if (setColor) {
        if (gauge.value < 0) {
            gauge.set('titleBottomColor', 'red');
        } else {
            gauge.set('titleBottomColor', 'green');
        }
    }
}

function updateGaugeValue(gauge, value, isSymmetric, autoRescale) {
    // gauge: zu erneuernde Gauge
    // value: neuer Wert
    // isSymmetric: symmetrische Gauge oder nicht (min-max or 0-max)
    // autoRescale: Skala passt sich nach defaultScaleCounter-Aufrufen selbst nach unten an
    if(isNaN(value)){
        // es wurde keine Zahl als Wert übergeben
	     return;  // gleich wieder zurück
    }
    var needsScaling = false;
    var newGaugeMax = Math.ceil((Math.abs(value) / 1000)) * 1000;
    if (gauge.max < newGaugeMax) {
        // benötigtes Maximum ist größer als Skala
        gauge.max = newGaugeMax;  // Skala positiv anpassen
        gauge.scaleCounter = defaultScaleCounter;  // Counter reset
        needsScaling = true;
        if (!autoRescale) {
            // neues Maximum der Gauge als Cookie speichern
            gauge_identifier = 'dark_gauges_1_' + gauge.id;
            $.ajax({
                type: "GET",
                url: "./setGaugeScaleCookie.php",
                data: {
                    name: gauge_identifier,
                    value: newGaugeMax
                }
            });
        }
    } else if (gauge.max > newGaugeMax) {
        // Skala ist aktuell eigentlich zu groß
        if (autoRescale) {
            // und Anpassung soll automatisch erfolgen
            gauge.scaleCounter -= 1; // dann Counter reduzieren
            if (gauge.scaleCounter == 0) {
                // wenn Zeit rum
                gauge.scaleCounter = defaultScaleCounter;  // Counter reset
                gauge.max = gauge.max-(Math.ceil((gauge.max-newGaugeMax) / 2000) * 1000);  // Skala anpassen
                needsScaling = true;
            }
        }
    } else {
        // Skala soll bleiben, keine automatische Anpassung
        if (gauge.scaleCounter < defaultScaleCounter) {
            // aber Zähler zum Wechsel ist schon angelaufen
            gauge.scaleCounter = defaultScaleCounter;  // Counter reset
        }
    }
    if (needsScaling) {
        // wenn Skala angepasst werden muss
        if (isSymmetric) {
            // bei symmetrischer Gauge die negative Skala angleichen
            gauge.min = gauge.max *-1;
        }
        // farbigen Rand anpassen
        gauge.set('colorsRanges', [[gauge.min, 0, 'red', 3], [0, gauge.max, 'green', 3]]);
        // Labels in kW
        gauge.set('labelsSpecific', [(gauge.min/1000), ((gauge.max-Math.abs(gauge.min))/2000), (gauge.max/1000)]);
    }
    // neu zeichnen nur, wenn sich Wert oder die Skala ändert
    if (gauge.value != value || needsScaling) {
        // neuen Wert für Gauge setzen
        gauge.value = value;
        // und Anzeige erneuern
        gauge.grow();
    }
}

function getGaugeDataLabel() {
    // regelmäßig Werte für Gauge-Label vom Server holen
    $.ajax({
        // Tagesertrag PV für Gauge für PV-Leistung lesen
        url:
            "/openWB/ramdisk/daily_pvkwhk",
        complete:
            function(request){
                var anzeigeText = request.responseText + ' kWh';
                // Text setzen ohne Farbanpassung
                updateGaugeBottomText(gaugePV, anzeigeText, false);
            }
    });
}

function getGaugeDataNeedle() {
    // regelmäßig alle Werte für die Gauge-Needle vom Server holen
    $.ajax({
        // Gauge für PV-Leistung anpassen
        url:
            "/openWB/ramdisk/pvwatt",
        complete:
            function(request){
                // Vorzeichen zur Darstellung umdrehen, wegen Regelung ist Erzeugung negativ
                var anzeigeWert = parseInt(request.responseText,10) * -1;
                // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max, kein AutoRescale
                updateGaugeValue(gaugePV, anzeigeWert, false, false);
            }
    });

    $.ajax({
      // Gauge für Speicher-Leistung anpassen
      url: "/openWB/ramdisk/speicherleistung",
      complete: function(request){
          // Entladung = negativ, Ladung = positiv
          // Vorzeichen zur Darstellung umdrehen
          var anzeigeWert = parseInt(request.responseText,10);
          // Gauge mit Rückgabewert erneuern, symmetrische Gauge Min-Max, kein AutoRescale
          updateGaugeValue(gaugeBatt, anzeigeWert, true, false);
          var anzeigeText = 'Ladung';
          if (anzeigeWert < 0) anzeigeText = 'Entadung';
          // Text setzen mit Farbanpassung
          updateGaugeBottomText(gaugeBatt, anzeigeText, true);
      }
    });

    $.ajax({
      // ProgressBar für Speicher SoC anpassen
      url: "/openWB/ramdisk/speichersoc",
      complete: function(request){
          // ProgressBar mit Rückgabewert erneuern
          progressBarSoC.value = parseInt(request.responseText,10);
          progressBarSoC.set('title', 'SoC: '+request.responseText+'%');
          progressBarSoC.grow();
      }
    });

    $.ajax({
      // Gauge für EVU-Leistung anpassen
      url: "/openWB/ramdisk/wattbezug",
      complete: function(request){
          // zur Regelung: Einspeisung = negativ, Bezug = positiv
          // Vorzeichen zur Darstellung umdrehen
          var anzeigeWert = parseInt(request.responseText,10) * -1;
          // Gauge mit Rückgabewert erneuern, symmetrische Gauge Min-Max, kein AutoRescale
          updateGaugeValue(gaugeEVU, anzeigeWert, true, false);
          var anzeigeText = 'Einspeisung';
          if (anzeigeWert < 0) anzeigeText = 'Bezug';
          // Text setzen mit Farbanpassung
          updateGaugeBottomText(gaugeEVU, anzeigeText, true);
      }
    });

    $.ajax({
      // Gauge für Hausverbrauch anpassen
      url:
          "/openWB/ramdisk/hausverbrauch",
      complete:
          function(request){
              var anzeigeWert = parseInt(request.responseText,10);
              if (anzeigeWert < 0) {
                  // beim Hausverbrauch bleibt Gauge im positiven Bereich
                  // negative Werte werden = 0 gesetzt
                  anzeigeWert = 0;
              }
              // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max, AutoRescale
              updateGaugeValue(gaugeHome, anzeigeWert, false, true);
          }
      });

      $.ajax({
        // Gauge für lp1-Leistung anpassen
        url: "/openWB/ramdisk/llaktuell",
        complete: function(request){
            // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max
            updateGaugeValue(gaugelp1, (parseInt(request.responseText,10)), false, true);
        }
      });

      $.ajax({
        // ProgressBar für LP1 SoC anpassen
        url: "/openWB/ramdisk/soc",
        complete: function(request){
            // ProgressBar mit Rückgabewert erneuern
            lp1SoC.value = parseInt(request.responseText,10);
            lp1SoC.set('title','SoC: ');
            lp1SoC.grow();
        }
      });

      $.ajax({
        // ProgressBar für LP1 Soll anpassen
        url: "/openWB/ramdisk/llsoll",
        complete: function(request){
            // ProgressBar mit Rückgabewert erneuern
            lp1soll.value = parseInt(request.responseText,10);
            lp1soll.set('title', 'Soll: ');
            lp1soll.grow();
        }
      });

      $.ajax({
        // Gauge für lp2-Leistung anpassen
        url: "/openWB/ramdisk/llaktuells1",
        complete: function(request){
            // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max
            updateGaugeValue(gaugelp2, (parseInt(request.responseText,10)), false, true);
        }
      });

      $.ajax({
        // ProgressBar für LP2 SoC anpassen
        url: "/openWB/ramdisk/soc1",
        complete: function(request){
            // ProgressBar mit Rückgabewert erneuern
            lp2SoC.value = parseInt(request.responseText,10);
            lp2SoC.set('title', 'SoC: ');
            lp2SoC.grow();
        }
      });

      $.ajax({
        // ProgressBar für LP2 Soll anpassen
        url: "/openWB/ramdisk/llsolls1",
        complete: function(request){
            // ProgressBar mit Rückgabewert erneuern
            lp2soll.value = parseInt(request.responseText,10);
            lp2soll.set('title', 'Soll: ');
            lp2soll.grow();
        }
      });
}

var gaugeDataIntervall, gaugeLabelIntervall;

$(window).load(function() {
    // sobal die Seite vollständig geladen ist, alle Gauges
    // regelmäßig aktualisieren
    gaugeDataIntervall = mySetInterval(getGaugeDataNeedle, 5000);  // alle 5 Sekunden Needle erneuern
    gaugeLabelIntervall = mySetInterval(getGaugeDataLabel, 20000);  // alle 20 Sekunden Label mit Werten erneuern
});
