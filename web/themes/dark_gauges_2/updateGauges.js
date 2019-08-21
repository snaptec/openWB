function updateGaugeValue(gauge, value, text, setText, isSymmetric, autoRescale) {
    // gauge: zu erneuernde Gauge
    // value: neuer Wert
    // text: ggf. neuer Text
    // setText: Text und Farbe des Labels anpassen
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
    // neuen Wert für Gauge setzen, ggf. Text im Label ändern
    gauge.value = value;
    if (setText) {
        gauge.set('titleBottom', text);
        // Farben der Schrift ggf. anpassen
        if (value < 0) {
            gauge.set('titleBottomColor', 'red');
        } else {
            gauge.set('titleBottomColor', 'green');
        }
    }
    // und Anzeige erneuern
    gauge.grow();
}

function getValueDailyYieldLabel() {
    // regelmäßig Werte für Tagesertrag-Label vom Server holen
    $.ajax({
        // Tagesertrag PV für Gauge für PV-Leistung lesen
        url:
            "/openWB/ramdisk/daily_pvkwhk",
        complete:
            function(request){
                var anzeigeText = request.responseText + ' kWh';
                // Text setzen
                gaugePV.set('titleBottom', anzeigeText);
                // Neuzeichnen erfolgt bei regelmäßiger Werte-Aktualisierung
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
                // Anpassung des Labesl mit Tagesertrag erfolgt per separatem Ajax
                // Gauge mit Rückgabewert erneuern, kein Text, asymmetrische Gauge 0-Max, kein AutoRescale
                updateGaugeValue(gaugePV, anzeigeWert, '', false, false, false);
            }
    });

    $.ajax({
      // ProgressBar für Wechselrichter 1 anpassen
      url: "/openWB/ramdisk/pvwatt1",
      complete: function(request){
          // ProgressBar mit Rückgabewert (in kW mit 2 Nachkommastellen) erneuern
          var anzeigeWert = (parseInt(request.responseText,10) / -1000).toFixed(2);
          var anzeigeText = anzeigeWert + 'kW'
          progressBarWR1.value = anzeigeWert;
          progressBarWR1.set('title', 'Garage: ' + anzeigeText);
          progressBarWR1.grow();
      }
    });

    $.ajax({
      // ProgressBar für Wechselrichter 2 anpassen
      url: "/openWB/ramdisk/pvwatt2",
      complete: function(request){
          // ProgressBar mit Rückgabewert (in kW mit 2 Nachkommastellen) erneuern
          var anzeigeWert = (parseInt(request.responseText,10) / -1000).toFixed(2);
          var anzeigeText = anzeigeWert + 'kW'
          progressBarWR2.value = anzeigeWert;
          progressBarWR2.set('title', 'Wohnhaus: ' + anzeigeText);
          progressBarWR2.grow();
      }
    });

    $.ajax({
      // Gauge für Speicher-Leistung anpassen
      url: "/openWB/ramdisk/speicherleistung",
      complete: function(request){
          // Entladung = negativ, Ladung = positiv
          var anzeigeWert = parseInt(request.responseText,10);
          var anzeigeText = 'Ladung';
          if (anzeigeWert < 0) anzeigeText = 'Entadung';
          // Text und Farbe des Labels anpassen je nach Ladung/Entadung
          // Neuzeichnung erfolgt bei Update der Werte
          // updateGaugeBottomText(gaugeBatt, anzeigeText, true, true);
          // Gauge mit Rückgabewert und Text erneuern, symmetrische Gauge Min-Max, kein AutoRescale
          updateGaugeValue(gaugeBatt, anzeigeWert, anzeigeText, true, true, false);
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
          var anzeigeText = 'Einspeisung';
          if (anzeigeWert < 0) anzeigeText = 'Bezug';
          // Text und Farbe des Labels anpassen je nach Einspeisung/Bezug
          // Neuzeichnung erfolgt bei Update der Werte
          // updateGaugeBottomText(gaugeEVU, anzeigeText, true, true);
          // Gauge mit Rückgabewert und Text erneuern, symmetrische Gauge Min-Max, kein AutoRescale
          updateGaugeValue(gaugeEVU, anzeigeWert, anzeigeText, true, true, false);
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
              // Gauge mit Rückgabewert erneuern, kein Text, asymmetrische Gauge 0-Max, AutoRescale
              updateGaugeValue(gaugeHome, anzeigeWert, '', false, false, true);
          }
      });
}

var gaugeDataIntervall, dailyYieldLabelIntervall;

$(window).load(function() {
    // sobal die Seite vollständig geladen ist, alle Gauges
    // regelmäßig aktualisieren
    // benötigt eingebundene handleIntervalls.js
    gaugeDataIntervall = mySetInterval(getGaugeDataNeedle, 5000);  // alle 5 Sekunden Needle erneuern
    dailyYieldLabelIntervall = mySetInterval(getValueDailyYieldLabel, 20000);  // alle 20 Sekunden Label mit Tagesertrag erneuern
});
