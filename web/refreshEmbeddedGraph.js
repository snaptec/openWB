function getgraph() {
	var themeCookie = document.cookie.split("openWBTheme")[1].split("; ")[0].substr(1);
	var source = "themes/"+themeCookie+"/graph-live.php",
	timestamp = (new Date()).getTime(),
	newUrl = source + '?_=' + timestamp;
	if (document.getElementById("livegraph")) {
		document.getElementById("livegraph").src = newUrl;
	}
}

var embeddedGraphIntervall;

$(window).load(function() {
    // sobal die Seite vollständig geladen ist, alle Gauges
    // regelmäßig aktualisieren
    // benötigt eingebundene handleIntervalls.js
    embeddedGraphIntervall = mySetInterval(getgraph, 5000);  // alle 5 Sekunden Graph erneuern
});
