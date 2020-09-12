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
/////////////////////////
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

