/**
 * Functions to process configured hooks
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

var doHookInterval;

function getHookStatus(dataURL) {
	// read dataURL filecontent and return it
	return $.get(dataURL);
}

function displayHookStatus(hookNumber) {
	var element = "#hook"+hookNumber+"div";
	getHookStatus("/openWB/ramdisk/hook"+hookNumber+"akt").done(function(result) {
		if ( result == 1 ) {
			$(element).removeClass("bg-danger");
			$(element).addClass("bg-success");
		} else {
			$(element).removeClass("bg-success");
			$(element).addClass("bg-danger");
		}
	});
}

function processAllHooks() {
	for (numberOfHook=1; numberOfHook<=3; numberOfHook++) {
		displayHookStatus(numberOfHook);
	}
}

$(document).ready(function(){
	doHookInterval = setInterval(processAllHooks, 5000);
	processAllHooks();
});
