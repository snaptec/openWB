var doval;

function getgraph() {
	var themeCookie = document.cookie.split("openWBTheme")[1].split("; ")[0].substr(1);
	var source = "themes/"+themeCookie+"/livechart_php.php",
	timestamp = (new Date()).getTime(),
	newUrl = source + '?_=' + timestamp;
	if (document.getElementById("livegraph")) {
		document.getElementById("livegraph").src = newUrl;
	}
}

doval = setInterval(getgraph, 20000);

getgraph();
