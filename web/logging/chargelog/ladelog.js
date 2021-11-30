var initialladelogread = 1;
var ConfiguredChargePoints = 0;
var PriceForKWh = 0.30;
var gotprice = 0;
var retries = 0;

var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);

// general helper functions

function getIndex(topic) {
	// get occurrence of numbers between / / in topic
	// since this is supposed to be the index like in openwb/lp/4/w
	// no lookbehind supported by safari, so workaround with replace needed
	var index = topic.match(/(?:\/)([0-9]+)(?=\/)/g)[0].replace(/[^0-9]+/g, '');
	if ( typeof index === 'undefined' ) {
		index = '';
	}
	return index;
}

function getLadelogIndex(topic) {
	// get occurrence of numbers between / / in topic
	// since this is supposed to be the index like in openwb/lp/4/w
	// no lookbehind supported by safari, so workaround with replace needed
	var index = topic.match(/[1-9][0-9]*$/g)[0];
	if ( typeof index === 'undefined' ) {
		index = '';
	}
	return index;
}

// mqtt client options and functions

var thevalues = [
	["openWB/system/MonthLadelogData1"],
	["openWB/system/MonthLadelogData2"],
	["openWB/system/MonthLadelogData3"],
	["openWB/system/MonthLadelogData4"],
	["openWB/system/MonthLadelogData5"],
	["openWB/system/MonthLadelogData6"],
	["openWB/system/MonthLadelogData7"],
	["openWB/system/MonthLadelogData8"],
	["openWB/system/MonthLadelogData9"],
	["openWB/system/MonthLadelogData10"],
	["openWB/system/MonthLadelogData11"],
	["openWB/system/MonthLadelogData12"],
	["openWB/system/ConfiguredChargePoints"],
	["openWB/system/priceForKWh"],
	["openWB/global/rfidConfigured"],
	["openWB/lp/1/boolChargePointConfigured"],
	["openWB/lp/2/boolChargePointConfigured"],
	["openWB/lp/3/boolChargePointConfigured"],
	["openWB/lp/4/boolChargePointConfigured"],
	["openWB/lp/5/boolChargePointConfigured"],
	["openWB/lp/6/boolChargePointConfigured"],
	["openWB/lp/7/boolChargePointConfigured"],
	["openWB/lp/8/boolChargePointConfigured"]
];

var options = {
	timeout: 5,
	onSuccess: function () {
		retries = 0;
		thevalues.forEach(function(thevar) {
			client.subscribe(thevar[0], {qos: 0});
		});
	},
	onFailure: function () {
		window.alert("Verbindung nicht möglich");
	}
};

function handlevar(mqttmsg, mqttpayload) {
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i ) ) {
		// respective charge point configured
		var index = getIndex(mqttmsg);  // extract number between two / /
		// now show/hide element containing data-lp attribute with value=index
		switch (mqttpayload) {
			case '0':
				hideSection('#chargep' + index, false);
				break;
			case '1':
				showSection('#chargep' + index, false);
				break;
		}
	}
	else if ( mqttmsg == "openWB/system/priceForKWh" ) {
		PriceForKWh = mqttpayload;
		gotprice = 1;
		putladelogtogether();

	}
	else if( mqttmsg.match( /^openwb\/system\/MonthLadelogData[1-9][0-9]*$/i )){
		// respective month index
		index = getLadelogIndex(mqttmsg); // extract number at end of topic
		if (initialladelogread == 0 && (mqttpayload != "empty")) {
			window["ladelog"+index+"p"] = mqttpayload;
			window["ladelog"+index] = 1;
			putladelogtogether();
		}
	}
	else if ( mqttmsg == "openWB/global/rfidConfigured" ) {
		switch (mqttpayload) {
			case '0':
				hideSection('#rfidFilter', false);
				break;
			case '1':
				showSection('#rfidFilter', false);
				break;
		}
	}
};

var publish = function (payload, topic) {
	var message = new Messaging.Message(payload);
	message.destinationName = topic;
	message.qos = 2;
	message.retained = true;
	client.send(message);
}

// lade log functions

function initLadelog(){
	ladelog1=0;
	ladelog2=0;
	ladelog3=0;
	ladelog4=0;
	ladelog5=0;
	ladelog6=0;
	ladelog7=0;
	ladelog8=0;
	ladelog9=0;
	ladelog10=0;
	ladelog11=0;
	ladelog12=0;
	ladelog1p="";
	ladelog2p="";
	ladelog3p="";
	ladelog4p="";
	ladelog5p="";
	ladelog6p="";
	ladelog7p="";
	ladelog8p="";
	ladelog9p="";
	ladelog10p="";
	ladelog11p="";
	ladelog12p="";
	initialladelogread=0;
}

function selectladelogclick(newdate){
	$('.loading').removeClass('hide');
	newdate = newdate.replace('-','');
	initLadelog();
	publish(newdate, "openWB/set/graph/RequestMonthLadelog");
}

function putladelogtogether() {
	if ( (ladelog1 == 1) && (ladelog2 == 1) && (ladelog3 == 1) && (ladelog4 == 1) && (ladelog5 == 1) && (ladelog6 == 1) && (ladelog7 == 1) && (ladelog8 == 1) && (ladelog9 == 1) && (ladelog10 == 1) && (ladelog11 == 1) && (ladelog12 == 1) && (gotprice == 1) ){
		var ladelogdata = ladelog1p + "\n" + ladelog2p + "\n" + ladelog3p + "\n" + ladelog4p + "\n" + ladelog5p + "\n" + ladelog6p + "\n" + ladelog7p + "\n" + ladelog8p + "\n" + ladelog9p + "\n" + ladelog10p + "\n" + ladelog11p + "\n" + ladelog12p;
		ladelogdata = ladelogdata.replace(/^\s*[\n]/gm, '');
		initialladelogread = 1 ;

		function parseResult(result) {
			var resultArray = [];
			result.split("\n").forEach(function(row) {
				var rowArray = [];
				row.split(",").forEach(function(cell) {
					rowArray.push(cell);
				});
				if ( rowArray.length > 2 ) {
					resultArray.push(rowArray);
				}
			});
			return resultArray;
		}

		parsedlog = parseResult(ladelogdata);
		var totalkwh = "0";
		var totalkm = "0";
		var filterrfid = 0;
		var rfidtag = "";

		if ($('#showrfid').prop('checked')){
			filterrfid = 1;
			rfidtag = $('#rfidtag').val();
		}

		var testout = [];
		parsedlog.forEach(function(row) {
			var cellcount=0;
			var temparr = [];
			var writelp = 0;
			var writemodus = 0;
			var writerfid = 0;
			row.forEach(function(cell) {
				cellcount+=1;
				temparr.push(cell);
				if ( cellcount == 7) {
					if ($('#showlp'+cell).prop('checked') && !$('#chargep'+cell).hasClass('hide')) {
						writelp = 1;
					}
				}
				if ( cellcount == 8) {
					if (cell == 0 && $('#showsofort').prop('checked')) {
						writemodus = 1;
					}
					if (cell == 1 && $('#showminpv').prop('checked')) {
						writemodus = 1;
					}
					if (cell == 2 && $('#shownurpv').prop('checked')) {
						writemodus = 1;
					}
					if (cell == 3 && $('#showstandby').prop('checked')) {
						writemodus = 1;
					}
					if (cell == 4 && $('#showstandby').prop('checked')) {
						writemodus = 1;
					}
					if (cell == 7 && $('#shownacht').prop('checked')) {
						writemodus = 1;
					}
				}
				if ( cellcount == 9) {
					if (filterrfid == 1) {
						if ( cell == rfidtag ) {
							writerfid = 1;
						} else {
							writerfid = 0;
						}
					} else {
						writerfid = 1;
					}
				}
				if (row.length == 8) {
					if ( cellcount == 8 && writelp == 1 && writemodus == 1 && showrfid == 0) {
						testout.push(temparr);
					}
				}
				if ( cellcount == 9 && writelp == 1 && writemodus == 1 && writerfid == 1) {
					testout.push(temparr);
				}
			});
		});

		if ( testout.length >= 1 ) {
			var content = '<table class="table"> <thead><tr><th scope="col">Startzeit</th><th scope="col">Endzeit</th><th scope="col" class="text-right">geladene km</th><th scope="col" class="text-right">kWh</th><th scope="col" class="text-right">mit kW</th><th scope="col" class="text-right">Ladedauer</th><th scope="col">Ladepunkt</th><th scope="col">Lademodus</th><th scope="col">RFID Tag</th><th scope="col" class="text-right">Kosten</th></tr></thead> <tbody>';
			var rowcount=0;
			var avgkw="0";
			var totalprice="0";

			testout.forEach(function(row) {
				var price = "0"
				rowcount+=1;
				content += "<tr>";
				var cellcount=0;
				row.forEach(function(cell) {

					cellcount+=1;
					switch (cellcount){
						case 1: // Startzeit
						case 2: // Endzeit
							dateString = cell.replace("-", " ");
							content += "<td>" + dateString + "</td>";
							break;
						case 3: // geladene km
							totalkm = parseFloat(totalkm) + parseFloat(cell);
							content += "<td class=\"text-right\">" + cell + "</td>";
							break;
						case 4: // geladene kWh
							totalkwh = parseFloat(totalkwh) + parseFloat(cell);
							price = parseFloat(cell) * PriceForKWh;
							totalprice = parseFloat(totalprice) + parseFloat(price);
							content += "<td class=\"text-right\">" + parseFloat(cell).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>";
							break;
						case 5: // Ladeleistung kW
							avgkw = parseFloat(avgkw) + parseFloat(cell);
							content += "<td class=\"text-right\">" + parseFloat(cell).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>";
							break;
						case 6: // Ladedauer
							timeArray = cell.split(" ");
							if( timeArray.length == 4 ){
								hourString = timeArray[0];
								minuteString = timeArray[2];
							} else {
								hourString = "0";
								minuteString = timeArray[0];
							}
							if( minuteString.length < 2 ){
								minuteString = "0" + minuteString;
							}
							content += "<td class=\"text-right\">" + hourString + ":" + minuteString + "</td>";
							break;
						case 8: // Lademodus
							if (cell == 2) {
								content += "<td>" + "Nur PV" + "</td>" ;
							} else if (cell == 0) {
								content += "<td>" + "Sofort" + "</td>" ;
							} else if (cell == 1) {
								content += "<td>" + "Min+PV" + "</td>" ;
							} else if (cell == 4) {
								content += "<td>" + "Standby" + "</td>" ;
							} else if (cell == 3) {
								content += "<td>" + "Standby" + "</td>" ;
							} else if (cell == 7) {
								content += "<td>" + "Nachtladen" + "</td>" ;
							} else {
								content += "<td>" + cell + "</td>" ;
							}
							break;
						default:
							content += "<td>" + cell + "</td>";
					}
				});
				content += "<td class=\"text-right\">" + price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "€</td>" ;
				content += "</tr>";
			});

			content += '</tbody><tfoot><tr><th scope="col">Startzeit</th><th scope="col">Endzeit</th><th scope="col" class="text-right">' + totalkm.toFixed(0) + ' geladene km</th><th scope="col" class="text-right">' + totalkwh.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh </th><th scope="col" class="text-right">mit ' + (avgkw / rowcount).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kW</th><th scope="col" class="text-right">Ladedauer</th><th scope="col">Ladepunkt</th><th scope="col">Lademodus</th><th scope="col">RFID Tag</th><th scope="col" class="text-right">' + totalprice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '€ Kosten</th></tr></thead>';
			content += "</tfoot></table>";
			$("#ladelogtablediv").html(content);
		} else {
			$("#ladelogtablediv").html("<p>Keine Ergebnisse</p>");
		}
		$('.loading').addClass('hide');
	}
}

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
		column.push(matrix[i][col]);
	}
	return column;
}

// run
initLadelog();

var client = new Messaging.Client(location.hostname,9001, clientuid);
client.onMessageArrived = function (message) {
	handlevar(message.destinationName, message.payloadString, thevalues[0], thevalues[1]);
};
client.connect(options);
