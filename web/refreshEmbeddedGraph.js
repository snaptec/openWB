var doval;

function getgraph() {
	var source = "themes/"+themeCookie.read()+"/graph-live.php",
	timestamp = (new Date()).getTime(),
	newUrl = source + '?_=' + timestamp;
	document.getElementById("livegraph").src = newUrl;
}

doval = setInterval(getgraph, 5000);
