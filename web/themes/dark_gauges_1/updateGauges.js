var doInterval;

function updateGauge(gauge, value, isSymmetric, bottomText, bottomColor) {
    // gauge: zu erneuernde Gauge
    // value: neuer Wert
    // isSymmetric: symmetrische Gauge oder nicht (min-max or 0-max)
    // bottomText: Text unter der Leistungsanzeige
    // setzt neuen Wert und passt Skala an
    var newGaugeMax = Math.ceil((Math.abs(value) / 1000)) * 1000;
    if (gauge.max < newGaugeMax) {
        // neues Max/Min setzen
        gauge.max = newGaugeMax;
        if (isSymmetric) {
            // wenn symmterische Gauge: auch Min ändern
            gauge.min = newGaugeMax *-1;
        }
        gauge.set('colorsRanges', [[gauge.min, 0, 'red', 3], [0, gauge.max, 'green', 3]]);
        // Labels in kW
        gauge.set('labelsSpecific', [(gauge.min/1000), ((gauge.max-Math.abs(gauge.min))/2000), (gauge.max/1000)]);
    }
    // Text unter Leistungsanzeige setzen
    gauge.set('titleBottom', bottomText);
    gauge.set('titleBottomColor', bottomColor);
    // neuen Wert für Gauge setzen
    gauge.value = value;
    // und Anzeige erneuern
    gauge.grow();
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
        updateGauge(gaugeHome, parseInt(request.responseText,10), false);
    }
  });

  $.ajax({
    // Gauge für PV-Leistung anpassen
    url: "/openWB/ramdisk/pvwatt",
    complete: function(request){
        // Erzeugung bei Übergabe in positiven Wert umwandeln, liegt zur Regelung negativ vor
        // Gauge mit Rückgabewert erneuern, asymmetrische Gauge 0-Max
        updateGauge(gaugePV, (parseInt(request.responseText,10) * -1), false);
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
        var color = '';
        if (value > 0) {
            text = 'Ladung';
            color = 'green';
        } else if (value < 0) {
            text = 'Entadung';
            color = 'red';
        }
        updateGauge(gaugeBatt, value, true, text, color);
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
        var color = '';
        if (value > 0) {
            text = 'Einspeisung';
            color = 'green';
        } else if (value < 0) {
            text = 'Bezug';
            color = 'red';
        }
        updateGauge(gaugeEVU, value, true, text, color);
    }
  });
}

doInterval = setInterval(getfile, 5000);
