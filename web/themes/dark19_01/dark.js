var doval;
function getgraph() {
var source = 'themes/dark19_01/graph-live.php',
		        timestamp = (new Date()).getTime(),
		        newUrl = source + '?_=' + timestamp;
	    document.getElementById("livegraph").src = newUrl;


}

doval = setInterval(getgraph, 5000);

getfile();
