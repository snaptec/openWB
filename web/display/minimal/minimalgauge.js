/***********
 * LP1 gauge
 */
function lpUpdateMaxValue(displaylpmax, lpopts, gaugelp) {
	// switch range depending on magnitute of max value
	if (displaylpmax > 999) {
		var gaugeLpMaxValue = displaylpmax / 1000;
		lpopts['staticLabels'] = {
			font: "13px sans-serif",  // Specifies font
			labels: [0, gaugeLpMaxValue],  // Print labels at these values
			unit: "kW", // Optional: Label unit
			color: "white",  // Optional: Label text color
			fractionDigits: 1  // Optional: Numerical precision. 0=round off.
		}
	} else {
		var gaugeLpMaxValue = displaylpmax;
		lpopts['staticLabels'] = {
			font: "13px sans-serif",  // Specifies font
			labels: [0, gaugeLpMaxValue],  // Print labels at these values
			unit: "W", // Optional: Label unit
			color: "white",  // Optional: Label text color
			fractionDigits: 0  // Optional: Numerical precision. 0=round off.
		}
	}
	gaugelp.maxValue = gaugeLpMaxValue; // set max gauge value
	gaugelp.setOptions(lpopts);
}

function lp1UpdateMaxValue(displaylpmax) {
	lpUpdateMaxValue(displaylpmax, lp1opts, gaugelp1);
}

function lp2UpdateMaxValue(displaylpmax) {
	lpUpdateMaxValue(displaylpmax, lp2opts, gaugelp2);
}

var lp1opts = {
	lineWidth: 0.30, // The line thickness
	angle: 0, // The angle where gauge starts
	radiusScale: 1, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: true,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	percentColors: [[0.0, "#73c0FF"], [1.0, "#0000FF"]],
};

// Duo will only use a quarter circle
if (configuredChargePoints == 1) {
	lp1opts['range'] = 1; // The span of the gauge arc
} else {
	lp1opts['range'] = 0.5; // The span of the gauge arc
}



var targetlp1 = document.getElementById('lp1'); // your canvas element
var gaugelp1 = new Gauge(targetlp1).setOptions(lp1opts); // create sexy gauge!

lp1UpdateMaxValue(displaylp1max);
gaugelp1.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugelp1.animationSpeed = 5; // set animation speed (32 is default value)
gaugelp1.set(0); // set actual value

/***********
 * LP1-SoC gauge
 */
var lp1socopts = {
	lineWidth: 0.10, // The line thickness
	radiusScale: 0.66, // Relative radius
	angle: 0, // The angle where gauge starts
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: true,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, 100],  // Print labels at these values
		unit: "%", // Optional: Label unit
		insideLabel: true, // Optional: Labels are printed insde of the gauge
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	}
};

// Duo will only use a quarter circle
if (configuredChargePoints == 1) {
	lp1socopts['range'] = 1; // The span of the gauge arc
	lp1socopts['percentColors'] = [[0.0, "#73c0FF"], [1.0, "#0000FF"]];
} else {
	lp1socopts['range'] = 0.5; // The span of the gauge arc
	lp1socopts['percentColors'] = [[0.0, "#B22222"], [0.5, "#DAA520"], [1.0, "#33A02C"]];
}
var targetlp1s = document.getElementById('lp1s'); // your canvas element
var gaugelp1s = new Gauge(targetlp1s).setOptions(lp1socopts); // create sexy gauge!

gaugelp1s.maxValue = 100; // set max gauge value
gaugelp1s.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugelp1s.animationSpeed = 5; // set animation speed (32 is default value)
gaugelp1s.set(70); // set actual value


if (configuredChargePoints > 1) {
	/***********
	 * LP2 gauge
	 */
	var lp2opts = {
		angle: 0, // The angle where gauge starts
		range: 0.5, // The span of the gauge arc
		mirror: true, // start gauge from the right
		lineWidth: 0.30, // The line thickness
		radiusScale: 1, // Relative radius
		pointer: {
			length: 0.6, // // Relative to gauge radius
			strokeWidth: 0, // The thickness
			color: '#000000' // Fill color
		},
		limitMax: true,     // If false, max value increases automatically if value > maxValue
		limitMin: true,     // If true, the min value of the gauge will be fixed
		colorStart: '#6FADCF',   // Colors
		colorStop: '#8FC0DA',    // just experiment with them
		strokeColor: 'grey',  // to see which ones work best for you
		generateGradient: true,
		percentColors: [[0.0, "#73c0FF"], [1.0, "#0000FF"]],
	};

	var targetlp2 = document.getElementById('lp2'); // your canvas element
	var gaugelp2 = new Gauge(targetlp2).setOptions(lp2opts); // create sexy gauge!

	lp2UpdateMaxValue(displaylp2max);
	gaugelp2.setMinValue(0);  // Prefer setter over gauge.minValue = 0
	gaugelp2.animationSpeed = 5; // set animation speed (32 is default value)
	gaugelp2.set(0); // set actual value

	/***********
	 * LP2-SoC gauge
	 */
	var lp2socopts = {
		angle: 0, // The angle where gauge starts
		range: 0.5, // The span of the gauge arc
		mirror: true, // start gauge from the right
		lineWidth: 0.1, // The line thickness
		radiusScale: 0.66, // Relative radius
		pointer: {
			length: 0.6, // // Relative to gauge radius
			strokeWidth: 0, // The thickness
			color: '#000000' // Fill color
		},
		limitMax: true,     // If false, max value increases automatically if value > maxValue
		limitMin: true,     // If true, the min value of the gauge will be fixed
		colorStart: '#6FADCF',   // Colors
		colorStop: '#8FC0DA',    // just experiment with them
		strokeColor: 'grey',  // to see which ones work best for you
		generateGradient: true,
		percentColors: [[0.0, "#B22222"], [0.5, "#DAA520"], [1.0, "#33A02C"]],
		staticLabels: {
			font: "13px sans-serif",  // Specifies font
			labels: [0, 100],  // Print labels at these values
			unit: "%", // Optional: Label unit
			insideLabel: true, // Optional: Labels are printed insde of the gauge
			color: "white",  // Optional: Label text color
			fractionDigits: 0  // Optional: Numerical precision. 0=round off.
		}
	};
	var targetlp2s = document.getElementById('lp2s'); // your canvas element
	var gaugelp2s = new Gauge(targetlp2s).setOptions(lp2socopts); // create sexy gauge!
	gaugelp2s.maxValue = 100; // set max gauge value
	gaugelp2s.setMinValue(0);  // Prefer setter over gauge.minValue = 0
	gaugelp2s.animationSpeed = 5; // set animation speed (32 is default value)
	gaugelp2s.set(70); // set actual value
}
