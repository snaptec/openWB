var doInterval;
function getfile() {

	$.ajax({
		url: "/openWB/ramdisk/llaktuell",
		complete: function(request){
			$("#lldiv").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/llkombiniert",
		complete: function(request){
			$("#gesamtllwdiv").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/aktgeladen",
		complete: function(request){
			$("#aktgeladenprog1div").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/aktgeladen",
		complete: function(request){
			var aktgeladen1 = request.responseText;
			document.getElementById("prog1").value= aktgeladen1;
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/pvwatt",
		complete: function(request){
			$("#pvdiv").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/llsoll",
		complete: function(request){
			$("#llsolldiv").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/wattbezug",
		complete: function(request){
			$("#bezugdiv").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/ladestatus",
		complete: function(request){
			$("#controlleranaus").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/soc",
		complete: function(request){
			$("#soclevel").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/restzeitlp1",
		complete: function(request){
			$("#restzeitlp1div").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/gelrlp1",
		complete: function(request){
			$("#gelrlp1div").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/aktgeladen",
		complete: function(request){
			$("#aktgeladendiv").html(request.responseText);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/lademodus",
		complete: function(request){
			var lademodus=data;
			console.log(data);
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/lademodus",
		complete: function(request){
			var lademodus=data;
			console.log(data);
		}
	});

	var source = 'graph-index.html',
		timestamp = (new Date()).getTime(),
		newUrl = source + '?_=' + timestamp;
	document.getElementById("livegraph").src = newUrl;
}

doInterval = setInterval(getfile, 2000);
getfile();
