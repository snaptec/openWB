var doInterval;

function updateGauge(gauge, value, isSymmetric, bottomText, autoRescale) {
    // gauge: zu erneuernde Gauge
    // value: neuer Wert
    // isSymmetric: symmetrische Gauge oder nicht (min-max or 0-max)
    // bottomText: Text unter der Leistungsanzeige
    // autoRescale: Skala passt sich nach defaultScaleCounter-Aufrufen selbst nach unten an
    // setzt neuen Wert und passt Skala an
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
        // Text unter Leistungsanzeige wie übergeben setzen
        gauge.set('titleBottom', bottomText);
        // Farben der Schrift anpassen
        if (value < 0) {
            gauge.set('titleBottomColor', 'red');
        } else {
            gauge.set('titleBottomColor', 'green');
        }
        // neuen Wert für Gauge setzen
        gauge.value = value;
        // und Anzeige erneuern
        gauge.grow();
    }
}

function getfile() {
  $.ajax({
    // Gauge für Hausverbrauch anpassen
    url: "/openWB/ramdisk/hausverbrauch",
    complete: function(request){
        var value = parseInt(request.responseText,10);
        if (value < 0) {
            // beim Hausverbrauch bleibt Gauge im positiven Bereich
            // negative Werte werden = 0 gesetzt
            value = 0;
        }
        // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max
        updateGauge(gaugeHome, value, false, '', true);
    }
  });

  $.ajax({
    // Gauge für PV-Leistung anpassen
    url: "/openWB/ramdisk/pvwatt",
    complete: function(request){
        // Erzeugung bei Übergabe in positiven Wert umwandeln, liegt zur Regelung negativ vor
        // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max
        updateGauge(gaugePV, (parseInt(request.responseText,10) * -1), false, '', false);
    }
  });

  $.ajax({
    // Gauge für Speicher-Leistung anpassen
    url: "/openWB/ramdisk/speicherleistung",
    complete: function(request){
        // Entladung = negativ, Ladung = positiv
        // Vorzeichen zur Darstellung umdrehen
        // Gauge mit Rückgabewert erneuern, symmetrische Gauge Min-Max
        var value = parseInt(request.responseText,10);
        var text = '';
        if (value > 0) {
            text = 'Ladung';
        } else if (value < 0) {
            text = 'Entadung';
        }
        updateGauge(gaugeBatt, value, true, text, false);
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
        // Gauge mit Rückgabewert erneuern, symmetrische Gauge Min-Max
        var value = parseInt(request.responseText,10) * -1;
        var text = '';
        if (value > 0) {
            text = 'Einspeisung';
        } else if (value < 0) {
            text = 'Bezug';
        }
        updateGauge(gaugeEVU, value, true, text, false);
    }
  });
}

doInterval = setInterval(getfile, 2000);
