var do3Interval;
var pvwattarrow;
var llaktuellarrow = 0;
var llaktuelllp2arrow;
var llaktuelllp3arrow;
var llaktuelllp4arrow;
var llaktuelllp5arrow;
var llaktuelllp6arrow;
var llaktuelllp7arrow;
var llaktuelllp8arrow;
var llaktuellgarrow;
var intbezugarrow;
var intspeicherarrow;
var speichersoc;
var lp1soc;
var lp2soc;
function refresharrows() {
		var lp1arrow = document.getElementById("arrowlp1");
		var lp1speed = document.getElementById("speedlp1");
		lp1arrow.classList.remove("arrowrightblue");
		lp1speed.classList.remove("arrowSlidingRightMid");
		if (llaktuellarrow > 99) {
			lp1speed.classList.add("arrowSlidingRightMid");
			lp1arrow.classList.add("arrowrightblue");
		}
		var lp2arrow = document.getElementById("arrowlp2");
		var lp2speed = document.getElementById("speedlp2");
		lp2arrow.classList.remove("arrowrightblue");
		lp2speed.classList.remove("arrowSlidingRightMid");
		if (llaktuelllp2arrow > 99) {
			lp2speed.classList.add("arrowSlidingRightMid");
			lp2arrow.classList.add("arrowrightblue");
		}
		var lp3arrow = document.getElementById("arrowlp3");
		var lp3speed = document.getElementById("speedlp3");
		lp3arrow.classList.remove("arrowrightblue");
		lp3speed.classList.remove("arrowSlidingRightMid");
		if (llaktuelllp3arrow > 99) {
			lp3speed.classList.add("arrowSlidingRightMid");
			lp3arrow.classList.add("arrowrightblue");
		}
		var lp4arrow = document.getElementById("arrowlp4");
		var lp4speed = document.getElementById("speedlp4");
		lp4arrow.classList.remove("arrowrightblue");
		lp4speed.classList.remove("arrowSlidingRightMid");
		if (llaktuelllp4arrow > 99) {
			lp4speed.classList.add("arrowSlidingRightMid");
			lp4arrow.classList.add("arrowrightblue");
		}
		var lp5arrow = document.getElementById("arrowlp5");
		var lp5speed = document.getElementById("speedlp5");
		lp5arrow.classList.remove("arrowrightblue");
		lp5speed.classList.remove("arrowSlidingRightMid");
		if (llaktuelllp5arrow > 99) {
			lp5speed.classList.add("arrowSlidingRightMid");
			lp5arrow.classList.add("arrowrightblue");
		}
		var lpgarrow = document.getElementById("arrowlpg");
		var lpgspeed = document.getElementById("speedlpg");
		lpgarrow.classList.remove("arrowdownblue");
		lpgspeed.classList.remove("arrowSlidingDowngMid");
		if (llaktuellgarrow > 99) {
			lpgspeed.classList.add("arrowSlidingDowngMid");
			lpgarrow.classList.add("arrowdownblue");
		}
		var evuarrow = document.getElementById("arrowevu");
		var evuspeed = document.getElementById("speedevu");
		evuarrow.classList.remove("arrowleft");
		evuarrow.classList.remove("arrowrightred");
		evuspeed.classList.remove("arrowSlidingLeftMid");
		evuspeed.classList.remove("arrowSlidingRightMid");
	    	if (intbezugarrow < -30) {
			evuspeed.classList.add("arrowSlidingLeftMid");
			evuarrow.classList.add("arrowleft");
		}

	    	if (intbezugarrow > 30) {
			evuspeed.classList.add("arrowSlidingRightMid");
			evuarrow.classList.add("arrowrightred");
		}
		var pvarrow = document.getElementById("arrowpv");
		var pvspeed = document.getElementById("speedpv");
			pvarrow.classList.remove("arrowdown");
			pvspeed.classList.remove("arrowSlidingDownMid");
		if (pvwattarrow > 50) {
			pvspeed.classList.add("arrowSlidingDownMid");
			pvarrow.classList.add("arrowdown");

		}
		var speicherarrow = document.getElementById("arrowspeicher");
		var speicherspeed = document.getElementById("speedspeicher");
		speicherarrow.classList.remove("arrowleftyellow");
		speicherarrow.classList.remove("arrowright");
		speicherspeed.classList.remove("arrowSlidingLeftMid");
		speicherspeed.classList.remove("arrowSlidingRightMid");
	    	if (intspeicherarrow < -19) {
			speicherspeed.classList.add("arrowSlidingLeftMid");
			speicherarrow.classList.add("arrowleftyellow");
		}

	    	if (intspeicherarrow > 19) {
			speicherspeed.classList.add("arrowSlidingRightMid");
			speicherarrow.classList.add("arrowright");
		}

		
	    var element = document.getElementById("speichersocstatdiv");
		if (speichersoc > 0 && speichersoc < 25) {
			element.classList.add("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (speichersoc > 24 && speichersoc < 50) {
			element.classList.remove("fa-battery-empty");
			element.classList.add("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (speichersoc > 49 && speichersoc < 75) {
			element.classList.remove("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.add("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (speichersoc > 74 && speichersoc < 95) {
			element.classList.remove("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.add("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (speichersoc > 94 && speichersoc < 101) {
			element.classList.remove("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.add("fa-battery-full");
		}
		var element = document.getElementById("socstatlp1div");
		if (lp1soc >= 0 && lp1soc < 25) {
			element.classList.add("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if ( lp1soc > 24 && lp1soc < 50) {
			element.classList.remove("fa-battery-empty");
			element.classList.add("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (lp1soc > 49 && lp1soc < 75) {
			element.classList.remove("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.add("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (lp1soc > 74 && lp1soc < 95) {
			element.classList.remove("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.add("fa-battery-three-quarters");
			element.classList.remove("fa-battery-full");
		}
		if (lp1soc > 94 && lp1soc < 101) {
			element.classList.remove("fa-battery-empty");
			element.classList.remove("fa-battery-quarter");
			element.classList.remove("fa-battery-half");
			element.classList.remove("fa-battery-three-quarters");
			element.classList.add("fa-battery-full");
		}
		var e2lement = document.getElementById("socstatlp2div");
		if (lp2soc >= 0 && lp2soc < 25) {
			e2lement.classList.add("fa-battery-empty");
			e2lement.classList.remove("fa-battery-quarter");
			e2lement.classList.remove("fa-battery-half");
			e2lement.classList.remove("fa-battery-three-quarters");
			e2lement.classList.remove("fa-battery-full");
		}
		if (lp2soc > 24 && lp2soc < 50) {
			e2lement.classList.remove("fa-battery-empty");
			e2lement.classList.add("fa-battery-quarter");
			e2lement.classList.remove("fa-battery-half");
			e2lement.classList.remove("fa-battery-three-quarters");
			e2lement.classList.remove("fa-battery-full");
		}
		if (lp2soc > 49 && lp2soc < 75) {
			e2lement.classList.remove("fa-battery-empty");
			e2lement.classList.remove("fa-battery-quarter");
			e2lement.classList.add("fa-battery-half");
			e2lement.classList.remove("fa-battery-three-quarters");
			e2lement.classList.remove("fa-battery-full");
		}
		if (lp2soc > 74 && lp2soc < 95) {
			e2lement.classList.remove("fa-battery-empty");
			e2lement.classList.remove("fa-battery-quarter");
			e2lement.classList.remove("fa-battery-half");
			e2lement.classList.add("fa-battery-three-quarters");
			e2lement.classList.remove("fa-battery-full");
		}
		if (lp2soc > 94 && lp2soc < 101) {
			e2lement.classList.remove("fa-battery-empty");
			e2lement.classList.remove("fa-battery-quarter");
			e2lement.classList.remove("fa-battery-half");
			e2lement.classList.remove("fa-battery-three-quarters");
			e2lement.classList.add("fa-battery-full");
		}






}
do3Interval = setInterval(refresharrows, 500);
refresharrows();
