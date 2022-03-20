/***********
 * EVU gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.24, // The line thickness
	radiusScale: 0.67, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0.1, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: true,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	//colorStart: 'green',   // Colors
	//colorStop: 'red',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	percentColors: [[0.0, "#00FF00" ], [1.0, "#FF0000"]],
	generateGradient: true,
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [displayevumax * -1, 0, displayevumax],  // Print labels at these values
		color: "#FFFFFF",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
	staticZones: [
		{strokeStyle: "#F03E3E", min: displayevumax * 0.1, max: displayevumax}, // Red from 100 to 130
		{strokeStyle: "#FFDD00", min: 0, max: displayevumax * 0.1}, // Yellow
		{strokeStyle: "#30B32D", min: displayevumax * -1, max: 0}, // Green
	],
};

var target = document.getElementById('evu'); // your canvas element
var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!

gauge.maxValue = displayevumax; // set max gauge value
gauge.setMinValue(displayevumax * -1);  // Prefer setter over gauge.minValue = 0
gauge.animationSpeed = 50; // set animation speed (32 is default value)
gauge.set(0); // set actual value

/***********
 * PV gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.24, // The line thickness
	radiusScale: 0.67, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: 'green',   // Colors
	colorStop: 'green',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	percentColors: [[0.0, "#20610f" ], [1.0, "#00FF00"]],
	generateGradient: true,
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, displaypvmax],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	}, 
};

var targetpv = document.getElementById('pv'); // your canvas element
var gaugepv = new Gauge(targetpv).setOptions(opts); // create sexy gauge!

gaugepv.maxValue = displaypvmax; // set max gauge value
gaugepv.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugepv.animationSpeed = 5; // set animation speed (32 is default value)
gaugepv.set(0); // set actual value

/***********
 * Speicher gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.24, // The line thickness
	radiusScale: 0.67, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0.1, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: true,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	percentColors: [[0.0, "#FF0000" ], [0.5, "#FFFF00"],[1.0, "#00FF00"]],
	generateGradient: true,
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [displayspeichermax * -1, 0, displayspeichermax],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	}, 
	staticZones: [
		{strokeStyle: "#F03E3E", min: displayspeichermax * -1, max: displayspeichermax * -0.1}, // Red from 100 to 130
		{strokeStyle: "#FFDD00", min: displayspeichermax * -0.1, max: 0}, // Yellow
		{strokeStyle: "#30B32D", min: 0, max: displayspeichermax}, // Green
	],
};

var targetspeicher = document.getElementById('speicher'); // your canvas element
var gaugespeicher = new Gauge(targetspeicher).setOptions(opts); // create sexy gauge!

gaugespeicher.maxValue = displayspeichermax; // set max gauge value
gaugespeicher.setMinValue(displayspeichermax * -1);  // Prefer setter over gauge.minValue = 0
gaugespeicher.animationSpeed = 5; // set animation speed (32 is default value)
gaugespeicher.set(0); // set actual value

/***********
 * Speicher-SoC gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.08, // The line thickness
	radiusScale: 0.5, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: false,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	percentColors: [[0.0, "#73c0FF" ], [1.0, "#0000FF"]],
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, 100],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
};

var targetspeichers = document.getElementById('speichers'); // your canvas element
var gaugespeichers = new Gauge(targetspeichers).setOptions(opts); // create sexy gauge!

gaugespeichers.maxValue = 100; // set max gauge value
gaugespeichers.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugespeichers.animationSpeed = 5; // set animation speed (32 is default value)
gaugespeichers.set(70); // set actual value

/***********
 * Hausverbrauch gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.24, // The line thickness
	radiusScale: 0.67, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: '#6EFFF8',   // Colors
	colorStop: '#6EFFF8',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, (displayhausmax / 2), displayhausmax],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
};

var targethaus = document.getElementById('haus'); // your canvas element
var gaugehaus = new Gauge(targethaus).setOptions(opts); // create sexy gauge!

gaugehaus.maxValue = displayhausmax; // set max gauge value
gaugehaus.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugehaus.animationSpeed = 5; // set animation speed (32 is default value)
gaugehaus.set(0); // set actual value

/***********
 * LP1 gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.24, // The line thickness
	radiusScale: 0.67, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	percentColors: [[0.0, "#73c0FF" ], [1.0, "#0000FF"]],
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, displaylp1max],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
};

var targetlp1 = document.getElementById('lp1'); // your canvas element
var gaugelp1 = new Gauge(targetlp1).setOptions(opts); // create sexy gauge!

gaugelp1.maxValue = displaylp1max; // set max gauge value
gaugelp1.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugelp1.animationSpeed = 5; // set animation speed (32 is default value)
gaugelp1.set(0); // set actual value

/***********
 * LP1-SoC gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.08, // The line thickness
	radiusScale: 0.5, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: false,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	percentColors: [[0.0, "#73c0FF" ], [1.0, "#0000FF"]],
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, 100],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
};

var targetlp1s = document.getElementById('lp1s'); // your canvas element
var gaugelp1s = new Gauge(targetlp1s).setOptions(opts); // create sexy gauge!

gaugelp1s.maxValue = 100; // set max gauge value
gaugelp1s.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugelp1s.animationSpeed = 5; // set animation speed (32 is default value)
gaugelp1s.set(70); // set actual value

/***********
 * LP2 gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.24, // The line thickness
	radiusScale: 0.67, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: false,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	percentColors: [[0.0, "#73c0FF" ], [1.0, "#0000FF"]],
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, displaylp2max],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
};

var targetlp2 = document.getElementById('lp2'); // your canvas element
var gaugelp2 = new Gauge(targetlp2).setOptions(opts); // create sexy gauge!

gaugelp2.maxValue = displaylp2max; // set max gauge value
gaugelp2.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugelp2.animationSpeed = 5; // set animation speed (32 is default value)
gaugelp2.set(0); // set actual value

/***********
 * LP2-SoC gauge
 */
var opts = {
	angle: 0, // The span of the gauge arc
	lineWidth: 0.08, // The line thickness
	radiusScale: 0.5, // Relative radius
	pointer: {
		length: 0.6, // // Relative to gauge radius
		strokeWidth: 0, // The thickness
		color: '#000000' // Fill color
	},
	limitMax: false,     // If false, max value increases automatically if value > maxValue
	limitMin: true,     // If true, the min value of the gauge will be fixed
	colorStart: '#6FADCF',   // Colors
	colorStop: '#8FC0DA',    // just experiment with them
	strokeColor: 'grey',  // to see which ones work best for you
	generateGradient: true,
	percentColors: [[0.0, "#73c0FF" ], [1.0, "#0000FF"]],
	staticLabels: {
		font: "13px sans-serif",  // Specifies font
		labels: [0, 100],  // Print labels at these values
		color: "white",  // Optional: Label text color
		fractionDigits: 0  // Optional: Numerical precision. 0=round off.
	},
};

var targetlp2s = document.getElementById('lp2s'); // your canvas element
var gaugelp2s = new Gauge(targetlp2s).setOptions(opts); // create sexy gauge!

gaugelp2s.maxValue = 100; // set max gauge value
gaugelp2s.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gaugelp2s.animationSpeed = 5; // set animation speed (32 is default value)
gaugelp2s.set(70); // set actual value
