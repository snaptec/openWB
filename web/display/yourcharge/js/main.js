// const inactivityTimeout = 90000;
let displaypinaktiv = 1;
let lockTimeoutHandler = null;
let displaylocked = true;

let hideBlur = true;

function lockDisplay(lock = true) {
	if (lock == false) {
		displaylocked = false;
		$("#displaylock").find(".fa-lock").addClass("hide");
		$("#displaylock").find(".fa-unlock").removeClass("hide");

		$("#lockModal").modal("hide");
		if (hideBlur) $("#main").removeClass("blur");
		lockTimeoutHandler = window.setTimeout(lockDisplay, lockTimeout);
	} else {
		displaylocked = true;
		$("#changeLockModal,#changeDisplayTimeoutModal").modal("hide");
		$("#lockModal").modal("show");
		$("#main").addClass("blur");
		$("#displaylock").find(".fa-lock").removeClass("hide");
		$("#displaylock").find(".fa-unlock").addClass("hide");
		if ($(".sidenav").find(".btn.active").hasClass("displayLock")) {
			// console.log('changing panel');
			initPanels();
		}
		window.clearTimeout(lockTimeoutHandler);
		lockTimeoutHandler = null;
	}
}
//!!!! IMPLEMENT LATER
lockDisplay();
//!!!! IMPLEMENT LATER
$("#lockModal,#changeLockModal,#changeDisplayTimeoutModal").on(
	"hidden.bs.modal",
	() => {
		if (hideBlur) $("#main").removeClass("blur");
	}
);

const inactivityTime = () => {
	let time;
	const resetTimer = () => {
		clearTimeout(time);
		time = setTimeout(() => lockDisplay(true), inactivityTimeout);
		// 1000 milliseconds = 1 second
	};
	window.onload = resetTimer;
	// DOM Events
	document.onmousemove = resetTimer;
	document.onkeypress = resetTimer;
};
window.setInterval(function () {
	$.get(
		{
			url: "display/cards/checklock.php?lock=1",
			cache: false,
		},
		function (data) {
			if (data == "1") {
				displaypinaktiv = 1;
				if (lockTimeoutHandler == null) {
					displaylocked = true;
				}
				$("#displaylock").removeClass("hide");
			} else {
				displaypinaktiv = 0;
				displaylocked = false;
				window.clearTimeout(lockTimeoutHandler);
				lockTimeoutHandler = null;
				$("#displaylock").addClass("hide");
			}
		}
	);
}, 15000);

var delayUserInput = (function () {
	// sets a timeout on call and resets timout if called again for same id before timeout fires
	var timeoutHandles = {};
	return function (id, callback, ms) {
		if (timeoutHandles[id]) {
			clearTimeout(timeoutHandles[id]);
		}
		timeoutHandles[id] = setTimeout(function () {
			delete timeoutHandles[id];
			callback(id);
		}, ms);
	};
})();

function chargeLimitationOptionsShowHide(btnGrp, option) {
	// show/hide all option-parameters in form-rows for selected option
	var parent = btnGrp.closest(".chargeLimitation[data-lp]"); // get parent div element for charge limitation options
	var index = $(parent).data("lp"); // get current chargepoint number
	$(parent)
		.find(".form-row[data-option=" + option + "]")
		.removeClass("hide"); // now show option elements for selected option
	$(parent)
		.find(".form-row[data-option]")
		.not("[data-option=" + option + "]")
		.addClass("hide"); // hide all other option elements
	// now show/hide elements in modal info dialog
	var dataLpElements = $("[data-lp=" + index + "]"); // get main divs for our current chargepoint
	dataLpElements.find("[data-option-limit=" + option + "]").removeClass("hide"); // show info element for selected option
	dataLpElements
		.find("[data-option-limit]")
		.not("[data-option-limit=" + option + "]")
		.addClass("hide"); // hide all other options
}

function initPanels() {
	$(".resume").addClass("hide");
	$(".sidenav").find(".btn").removeClass("active");
	var firstButton = $(".sidenav")
		.find(".btn")
		.not(".hide")
		.not(".displayLock")
		.first();
	var firstNavTarget = $(firstButton).attr("href");
	$(firstButton).addClass("active");
	$(firstNavTarget).removeClass("hide");
}

$(document).ready(function () {
	// load scripts synchronously in order specified
	var scriptsToLoad = [
		// load mqtt library
		"js/mqttws31.js",
		// some helper functions
		"display/yourcharge/js/helperFunctions.js?ver=20210113",
		// functions for processing messages
		"display/yourcharge/js/processAllMqttMsg.js?ver=20210301",
		// functions performing mqtt and start mqtt-service
		"display/yourcharge/js/setupMqttServices.js?ver=20210301",
	];

	scriptsToLoad.forEach(function (src) {
		var script = document.createElement("script");
		script.src = src;
		script.async = false;
		document.body.appendChild(script);
	});

	// handling of display panels
	initPanels();
	lockDisplay;
	$(".sidenav")
		.find('a[href^="#"]')
		.on("click", function (event) {
			if ($(this).hasClass("displayLock") && displaylocked == true) {
				$("#lockInfoModal").modal("show");
			} else {
				// hide all panels
				$(".resume").addClass("hide");
				// get target panel
				var target = $(this).attr("href");
				// display target panel
				$(".resume" + target).removeClass("hide");
				// remove active menu element
				$(".sidenav").find(".active").removeClass("active");
				// activate clicked menu element
				$(this).addClass("active");
				// update sparklines
				$.sparkline_display_visible();
			}
		});

	$("#lastmanagementShowBtn").on("click", function (event) {
		$("#lastregelungModal").modal("show");
	});

	// display lock
	$.get(
		{
			url: "display/cards/checklock.php?lock=1",
			cache: false,
		},
		function (data) {
			if (data == "1") {
				displaypinaktiv = 1;
				$("#displaylock").removeClass("hide");
			} else {
				displaypinaktiv = 0;
				displaylocked = false;
				$("#displaylock").addClass("hide");
			}
		}
	);

	$("#displaylock").on("click", function () {
		// if (displaylocked == true) {
		//   $("#lockModal").modal("show");
		// } else {

		lockDisplay(true);
		// }
	});

	$(".btn-group-toggle").change(function (event) {
		// only charge limitation has class btn-group-toggle so far
		// option: 0 = keine, 1 = Energiemenge, 2 = EV-SoC
		var elementId = $(this).attr("id");
		var option = $('input[name="' + elementId + '"]:checked')
			.data("option")
			.toString();
		var topic = getTopicToSendTo(elementId);
		publish(option, topic);
		// show/hide respective option-values and progress
		if (elementId.includes("chargeLimitation")) {
			chargeLimitationOptionsShowHide(this, option);
		}
	});

	$(".rangeInput").on("input", function () {
		// show slider value in label of class valueLabel
		var elementId = $(this).attr("id");
		updateLabel(elementId);
		var element = $("#" + $.escapeSelector(elementId));
		var label = $('label[for="' + elementId + '"].valueLabel');
		label.addClass("text-danger");
		delayUserInput(
			elementId,
			function (id) {
				// gets executed on callback, 2000ms after last input-change
				// changes label color back to normal and sends input-value by mqtt
				var elem = $("#" + $.escapeSelector(id));
				var value = elem.val();
				var topic = getTopicToSendTo(id);
				publish(value, topic);
				var label = $('label[for="' + id + '"].valueLabel');
				label.removeClass("text-danger");
				// if rangeInput is for chargeLimitation, recalc progress
				if (id.includes("/energyToCharge")) {
					var parent = elem.closest(".chargeLimitation"); // get parent div element for charge limitation
					var element = parent.find(".progress-bar"); // now get parents progressbar
					var actualCharged = element.data("actualCharged"); // get stored value
					if (isNaN(parseFloat(actualCharged))) {
						actualCharged = 0; // minimum value
					}
					var progress = ((actualCharged / value) * 100).toFixed(0);
					element.width(progress + "%");
				}
			},
			2000
		);
	});
});

window.onload = function () {
	inactivityTime();
};
$(document).on("click", "#changeCode", () => {
	lockDisplay(true);
	const showChangeCodeModal = () => {
		$("#lockModal").off("hidden.bs.modal", showChangeCodeModal);
		$("#changeLockModal").modal("show");
		setTimeout(() => {
			hideBlur = true;
		}, 300);
	};
	hideBlur = false;
	$("#lockModal").on("hidden.bs.modal", showChangeCodeModal);
});
$(document).on("click", "#changeTimeout", () => {
	lockDisplay(true);
	const showChangeDisplayTimeoutModal = () => {
		$("#lockModal").off("hidden.bs.modal", showChangeDisplayTimeoutModal);
		$("#changeDisplayTimeoutModal").modal("show");
		$("#changeDisplayTimeoutBox").val(inactivityTimeout / 1000);
		setTimeout(() => {
			hideBlur = true;
		}, 300);
	};
	hideBlur = false;
	$("#lockModal").on("hidden.bs.modal", showChangeDisplayTimeoutModal);
});
