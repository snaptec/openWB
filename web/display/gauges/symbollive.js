function refresharrows() {
	var lp1arrow = $("#arrowlp1");
	var lp1speed = $("#speedlp1");

	lp1arrow.removeClass("arrowrightblue");
	lp1speed.removeClass("arrowSlidingRightMid");

	if (llaktuellarrow > 99) {
		lp1speed.addClass("arrowSlidingRightMid");
		lp1arrow.addClass("arrowrightblue");
	}

	if (lastmanagementold == 1 ) {
		var lp2arrow = $("#arrowlp2");
		var lp2speed = $("#speedlp2");
		lp2arrow.removeClass("arrowrightblue");
		lp2speed.removeClass("arrowSlidingRightMid");
		if (llaktuelllp2arrow > 99) {
			lp2speed.addClass("arrowSlidingRightMid");
			lp2arrow.addClass("arrowrightblue");
		}
		var e2lement = $("#socstatlp2div");
		if (lp2soc >= 0 && lp2soc < 25) {
			e2lement.addClass("fa-battery-empty");
			e2lement.removeClass("fa-battery-quarter");
			e2lement.removeClass("fa-battery-half");
			e2lement.removeClass("fa-battery-three-quarters");
			e2lement.removeClass("fa-battery-full");
		}
		if (lp2soc > 24 && lp2soc < 50) {
			e2lement.removeClass("fa-battery-empty");
			e2lement.addClass("fa-battery-quarter");
			e2lement.removeClass("fa-battery-half");
			e2lement.removeClass("fa-battery-three-quarters");
			e2lement.removeClass("fa-battery-full");
		}
		if (lp2soc > 49 && lp2soc < 75) {
			e2lement.removeClass("fa-battery-empty");
			e2lement.removeClass("fa-battery-quarter");
			e2lement.addClass("fa-battery-half");
			e2lement.removeClass("fa-battery-three-quarters");
			e2lement.removeClass("fa-battery-full");
		}
		if (lp2soc > 74 && lp2soc < 95) {
			e2lement.removeClass("fa-battery-empty");
			e2lement.removeClass("fa-battery-quarter");
			e2lement.removeClass("fa-battery-half");
			e2lement.addClass("fa-battery-three-quarters");
			e2lement.removeClass("fa-battery-full");
		}
		if (lp2soc > 94 && lp2soc < 101) {
			e2lement.removeClass("fa-battery-empty");
			e2lement.removeClass("fa-battery-quarter");
			e2lement.removeClass("fa-battery-half");
			e2lement.removeClass("fa-battery-three-quarters");
			e2lement.addClass("fa-battery-full");
		}
		$.ajax({
			url: "/openWB/ramdisk/ladestatuss1",
			complete: function(request){
				if (request.responseText == 1) {
					$("#stationlp2").css("color", "#00FF00");
				} else {
					$("#stationlp2").css("color", "white");
				}
			}
		});
	}

	var lpgarrow = $("#arrowlpg");
	var lpgspeed = $("#speedlpg");

	lpgarrow.removeClass("arrowdownblue");
	lpgspeed.removeClass("arrowSlidingDowngMid");

	if (llaktuellgarrow > 99) {
		lpgspeed.addClass("arrowSlidingDowngMid");
		lpgarrow.addClass("arrowdownblue");
	}
	var evuarrow = $("#arrowevu");
	var evuspeed = $("#speedevu");
	evuarrow.removeClass("arrowleft");
	evuarrow.removeClass("arrowrightred");
	evuspeed.removeClass("arrowSlidingLeftMid");
	evuspeed.removeClass("arrowSlidingRightMid");
	if (intbezugarrow < -30) {
		evuspeed.addClass("arrowSlidingLeftMid");
		evuarrow.addClass("arrowleft");
	}
	if (intbezugarrow > 30) {
		evuspeed.addClass("arrowSlidingRightMid");
		evuarrow.addClass("arrowrightred");
	}
	var pvarrow = $("#arrowpv");
	var pvspeed = $("#speedpv");
	pvarrow.removeClass("arrowdown");
	pvspeed.removeClass("arrowSlidingDownMid");
	if (pvwattarrow > 50) {
		pvspeed.addClass("arrowSlidingDownMid");
		pvarrow.addClass("arrowdown");
	}
	var speicherarrow = $("#arrowspeicher");
	var speicherspeed = $("#speedspeicher");
	speicherarrow.removeClass("arrowleftyellow");
	speicherarrow.removeClass("arrowright");
	speicherspeed.removeClass("arrowSlidingLeftMid");
	speicherspeed.removeClass("arrowSlidingRightMid");
	if (intspeicherarrow < -19) {
		speicherspeed.addClass("arrowSlidingLeftMid");
		speicherarrow.addClass("arrowleftyellow");
	}
	if (intspeicherarrow > 19) {
		speicherspeed.addClass("arrowSlidingRightMid");
		speicherarrow.addClass("arrowright");
	}
	var element = $("#speichersocstatdiv");
	if (speichersoc >= 0 && speichersoc < 25) {
		element.addClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (speichersoc > 24 && speichersoc < 50) {
		element.removeClass("fa-battery-empty");
		element.addClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (speichersoc > 49 && speichersoc < 75) {
		element.removeClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.addClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (speichersoc > 74 && speichersoc < 95) {
		element.removeClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.addClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (speichersoc > 94 && speichersoc < 101) {
		element.removeClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.addClass("fa-battery-full");
	}
	var element = $("#socstatlp1div");
	if (lp1soc >= 0 && lp1soc < 25) {
		element.addClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if ( lp1soc > 24 && lp1soc < 50) {
		element.removeClass("fa-battery-empty");
		element.addClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (lp1soc > 49 && lp1soc < 75) {
		element.removeClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.addClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (lp1soc > 74 && lp1soc < 95) {
		element.removeClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.addClass("fa-battery-three-quarters");
		element.removeClass("fa-battery-full");
	}
	if (lp1soc > 94 && lp1soc < 101) {
		element.removeClass("fa-battery-empty");
		element.removeClass("fa-battery-quarter");
		element.removeClass("fa-battery-half");
		element.removeClass("fa-battery-three-quarters");
		element.addClass("fa-battery-full");
	}
	$.ajax({
		url: "/openWB/ramdisk/plugstats1",
		complete: function(request){
			if (request.responseText == 1) {
				$("#carlp2").css("color", "blue");
			} else {
				$("#carlp2").css("color", "white");
			}
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/plugstat",
		complete: function(request){
			if (request.responseText == 1) {
				$("#carlp1").css("color", "blue");
			} else {
				$("#carlp1").css("color", "white");
			}
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/ladestatus",
		complete: function(request){
			if (request.responseText == 1) {
				$("#stationlp1").css("color", "#00FF00");
			} else {
				$("#stationlp1").css("color", "white");
			}
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/chargestat",
		complete: function(request){
			if (request.responseText == 1) {
				$("#socstatlp1div").css("color", "#00FF00");
			} else {
				$("#socstatlp1div").css("color", "white");
			}
		}
	});
	$.ajax({
		url: "/openWB/ramdisk/chargestats1",
		complete: function(request){
			if (request.responseText == 1) {
				$("#socstatlp2div").css("color", "#00FF00");
			} else {
				$("#socstatlp2div").css("color", "white");
			}
		}
	});
	$('#plugstatlp1div').hide();
	$('#plugstatlp2div').hide();
}

var do3Interval;

if ( displaytheme == 1) {
	do3Interval = setInterval(refresharrows, 4000);
	refresharrows();
}
