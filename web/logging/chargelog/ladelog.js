var initialChargeLogRead = 0;
var chargeLogReceived = [false, false, false, false, false, false, false, false, false, false, false, false];
var chargeLogPayloads = ["", "", "", "", "", "", "", "", "", "", "", ""];

var clientUid = Math.random().toString(36).replace(/[^a-z]+/g, '').substring(0, 5);

// general helper functions

/**
 * get occurrence of numbers between / / in topic
 * since this is supposed to be the index like in openwb/lp/4/w
 * no lookbehind supported by safari, so workaround with replace needed
 * @param {String} topic topic to parse
 * @returns {Number}
 */
function getIndex(topic) {
	var index = topic.match(/(?:\/)([0-9]+)(?=\/)/g)[0].replace(/[^0-9]+/g, '');
	if ( typeof index === 'undefined' ) {
		index = '';
	}
	return index;
}

/**
 * get last occurrence of numbers in topic
 * since this is supposed to be the index like in openWB/system/MonthLadelogData1
 * @param {String} topic topic to parse
 * @returns {Number}
 */
function getChargeLogIndex(topic) {
	var index = topic.match(/[1-9][0-9]*$/g)[0];
	if ( typeof index === 'undefined' ) {
		index = '';
	}
	return index;
}

// mqtt client options and functions

var topicsToSubscribe = [
	["openWB/global/rfidConfigured"],
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
		topicsToSubscribe.forEach(function(topic) {
			client.subscribe(topic[0], {qos: 0});
		});
	},
	onFailure: function () {
		window.alert("Verbindung nicht möglich");
	}
};

/**
 * gets called for new received mqtt messages
 * @param {String} topic the topic of the received message
 * @param {String} payload the payload of the received message
 */
function handleMessage(topic, payload) {
	if ( topic.match( /^openwb\/lp\/[1-9][0-9]*\/boolChargePointConfigured$/i ) ) {
		// respective charge point configured
		var index = getIndex(topic);  // extract number between two / /
		// now show/hide element containing data-lp attribute with value=index
		switch (payload) {
			case '0':
				hideSection('#chargep' + index, false);
				break;
			case '1':
				showSection('#chargep' + index, false);
				break;
		}
	}
	else if( topic.match( /^openwb\/system\/MonthLadelogData[1-9][0-9]*$/i )){
		// respective month index
		index = getChargeLogIndex(topic); // extract number at end of topic
		if (initialChargeLogRead == 0 && (payload != "empty")) {
			chargeLogPayloads[index-1] = payload;
			chargeLogReceived[index-1] = true;
			buildChargeLog();
		}
	}
	else if ( topic == "openWB/global/rfidConfigured" ) {
		switch (payload) {
			case '0':
				hideSection('#rfidFilter', false);
				break;
			case '1':
				showSection('#rfidFilter', false);
				break;
		}
	}
};

/**
 * send a message to the mqtt broker
 * @param {String} payload message to send
 * @param {String} topic topic for this message
 */
var publish = function (payload, topic) {
	var message = new Messaging.Message(payload);
	message.destinationName = topic;
	message.qos = 2;
	message.retained = true;
	client.send(message);
}

// charge log functions

/**
 * initializes global arrays
 * chargeLogReceived = [false,...]
 * chargeLogPayloads = ["",...]
 */
function initChargeLog(){
	chargeLogReceived = [false, false, false, false, false, false, false, false, false, false, false, false];
	chargeLogPayloads = ["", "", "", "", "", "", "", "", "", "", "", ""];
	initialChargeLogRead=0;
}

/**
 * requests charge log data for the given newDate
 * @param {String} newDate date in format "yyyy-mm"
 */
function selectChargeLogClick(newDate){
	$('.loading').removeClass('hide');
	newDate = newDate.replace('-','');
	initChargeLog();
	publish(newDate, "openWB/set/graph/RequestMonthLadelog");
}

/**
 * filters and parses the complete charge log data;
 * writes html table into element with id "ladelogtablediv"
 */
function buildChargeLog() {
	if ( chargeLogReceived.every((part) => { return part; }) ){
		var chargeLogData = chargeLogPayloads.join('\n');
		chargeLogData = chargeLogData.replace(/^\s*[\n]/gm, '');
		initialChargeLogRead = 1 ;

		/**
		 * converts charge log text data to array
		 * @param {String} result charge log text data in rows
		 * @returns Array
		 */
		function parseChargeLog(result) {
			var resultArray = [];
			result.split("\n").forEach(function(row) {
				var rowArray = row.split(",");
				if ( rowArray.length > 2 ) {
					resultArray.push(rowArray);
				}
			});
			return resultArray;
		}

		var parsedChargeLog = parseChargeLog(chargeLogData);
		var filterRfid = 0;
		var rfidTag = "";

		if ($('#showrfid').prop('checked')){
			filterRfid = 1;
			rfidTag = $('#rfidtag').val();
		}

		var filteredChargeLog = [];
		parsedChargeLog.forEach(function(row) {
			var cellNumber = 0;
			var tempArray = [];
			var writeChargePoint = 0;
			var writeChargeMode = 0;
			var writeRfid = 0;
			row.forEach(function(cell) {
				cellNumber += 1;
				tempArray.push(cell);
				if ( cellNumber == 7) {
					if ($('#showlp'+cell).prop('checked') && !$('#chargep'+cell).hasClass('hide')) {
						writeChargePoint = 1;
					}
				}
				if ( cellNumber == 8) {
					if (cell == 0 && $('#showsofort').prop('checked')) {
						writeChargeMode = 1;
					}
					if (cell == 1 && $('#showminpv').prop('checked')) {
						writeChargeMode = 1;
					}
					if (cell == 2 && $('#shownurpv').prop('checked')) {
						writeChargeMode = 1;
					}
					if (cell == 3 && $('#showstandby').prop('checked')) {
						writeChargeMode = 1;
					}
					if (cell == 4 && $('#showstandby').prop('checked')) {
						writeChargeMode = 1;
					}
					if (cell == 7 && $('#shownacht').prop('checked')) {
						writeChargeMode = 1;
					}
				}
				if ( cellNumber == 9) {
					if (filterRfid == 1) {
						if ( cell == rfidTag ) {
							writeRfid = 1;
						} else {
							writeRfid = 0;
						}
					} else {
						writeRfid = 1;
					}
				}
				if (row.length == 8) {
					if ( cellNumber == 8 && writeChargePoint == 1 && writeChargeMode == 1 && filterRfid == 0) {
						filteredChargeLog.push(tempArray);
					}
				}
				if ( cellNumber == 9 && writeChargePoint == 1 && writeChargeMode == 1 && writeRfid == 1) {
					filteredChargeLog.push(tempArray);
				}
			});
		});

		if ( filteredChargeLog.length >= 1 ) {
			var content = '<table class="table"><thead><tr>' +
				'<th scope="col">Startzeit</th>' +
				'<th scope="col">Endzeit</th>' +
				'<th scope="col" class="text-right">Reichweite in km</th>' +
				'<th scope="col" class="text-right">Energie in kWh</th>' +
				'<th scope="col" class="text-right">Leistung in kW (Durchschnitt)</th>' +
				'<th scope="col" class="text-right">Dauer in H:MM</th>' +
				'<th scope="col">Ladepunkt</th>' +
				'<th scope="col">Lademodus</th>' +
				'<th scope="col">RFID Tag</th>' +
				'<th scope="col" class="text-right">Kosten</th>' +
				'</tr></thead> <tbody>';
			var rowCounter = 0;
			var totalEnergy = 0;
			var totalRange = 0;
			var totalPower = 0;
			var totalPrice = 0;
			var totalDuration = 0;

			filteredChargeLog.forEach(function(row) {
				rowCounter += 1;
				content += "<tr>";
				var cellCounter = 0;
				row.forEach(function(cell) {
					cellCounter += 1;
					switch (cellCounter){
						case 1: // Startzeit
						case 2: // Endzeit
							content += "<td>" + cell.replace("-", " ") + "</td>";
							break;
						case 3: // geladene km
							var range = parseFloat(cell);
							totalRange += range
							content += "<td class=\"text-right\">" + range.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}) + "</td>";
							break;
						case 4: // geladene kWh
							var energy = parseFloat(cell);
							totalEnergy += energy;
							content += "<td class=\"text-right\">" + energy.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>";
							break;
						case 5: // Ladeleistung kW
							var power = parseFloat(cell);
							totalPower += power
							content += "<td class=\"text-right\">" + power.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>";
							break;
						case 6: // Ladedauer
							var timeArray = cell.split(" ");
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
							totalDuration += parseInt(hourString) * 60 + parseInt(minuteString)
							break;
						// 7: Ladepunkt-Nummer
						case 8: // Lademodus
							content += "<td>";
							switch (parseInt(cell)) {
								case 0:
									content += "Sofort";
									break;
								case 1:
									content += "Min+PV";
									break;
								case 2:
									content += "Nur PV";
									break;
								case 3:
								case 4:
									content += "Standby";
									break;
								case 7:
									content += "Nachtladen";
									break;
								default:
									content += cell;
							}
							content += "</td>";
							break;
						// 9: RFID-Tag
						case 10:
							var price = parseFloat(cell);
							totalPrice += price;
							content += "<td class=\"text-right\">" + price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "€</td>" ;
							break;
						default:
							content += "<td>" + cell + "</td>";
					}
				});
				content += "</tr>";
			});

			content +=
				'</tbody><tfoot><tr>' +
				'<th scope="col">Summe</th>' +
				'<th scope="col">' + rowCounter + ' Einträge</th>' +
				'<th scope="col" class="text-right">' + totalRange.toFixed(0) + ' km</th>' +
				'<th scope="col" class="text-right">' + totalEnergy.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh </th>' +
				'<th scope="col" class="text-right">' + (totalPower / rowCounter).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kW</th>' +
				'<th scope="col" class="text-right">' + Math.trunc(totalDuration / 60) + ':' + (totalDuration % 60) + '</th>' +
				'<th scope="col">&nbsp;</th>' +
				'<th scope="col">&nbsp;</th>' +
				'<th scope="col">&nbsp;</th>' +
				'<th scope="col" class="text-right">' + totalPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '€</th>' +
				'</tr></tfoot></table>';
			$("#ladelogtablediv").html(content);
		} else {
			$("#ladelogtablediv").html("<p>Keine Ergebnisse</p>");
		}
		$('.loading').addClass('hide');
	}
}

// run
initChargeLog();

var client = new Messaging.Client(location.hostname,9001, clientUid);
client.onMessageArrived = function (message) {
	handleMessage(message.destinationName, message.payloadString);
};
client.connect(options);
