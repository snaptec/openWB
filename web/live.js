var doInterval;
var do2Interval;
function loadText(){
    $.ajax({
        url:"./tools/lademodus.php",
        type: "post", //request type,
        dataType: 'json',
        data: {call: "loadfile"},
        success:function(result){
            if(result.text == 0){
                $('.actstat .btn').addClass("btn-green");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat2 .btn').removeClass("btn-green");
            }
            if(result.text == 1){
                $('.actstat1 .btn').addClass("btn-green");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat2 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");

            }
            if(result.text == 2){
                $('.actstat2 .btn').addClass("btn-green");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");

            }
            if(result.text == 3){
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-green");
	        $('.actstat2 .btn').removeClass("btn-green");

                $('.actstat .btn').addClass("btn-red");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");

            }
            if(result.text == 4){
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat2 .btn').removeClass("btn-green");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-green");
                $('.actstat4 .btn').removeClass("btn-red");

            }
        }
    });
}
loadText();

function getfile() {
$.ajaxSetup({ cache: false});
    $.ajax({
        url:"./tools/dailychargelp1.php",
        type: "post", //request type,
        dataType: 'json',
        data: {dailychargelp1call: "loadfile"},
        success:function(result){
            $("#dailychargelp1div").html(result.text);
	}
	    });
$.ajaxSetup({ cache: false});
    $.ajax({
        url:"./tools/dailychargelp2.php",
        type: "post", //request type,
        dataType: 'json',
        data: {dailychargelp2call: "loadfile"},
        success:function(result){
            $("#dailychargelp2div").html(result.text);
	}
	    });
	$.ajaxSetup({ cache: false});
    $.ajax({
        url:"./tools/dailychargelp3.php",
        type: "post", //request type,
        dataType: 'json',
        data: {dailychargelp3call: "loadfile"},
        success:function(result){
            $("#dailychargelp3div").html(result.text);
	}
	    });
$.ajax({
   url: "/openWB/ramdisk/aktgeladens1",
    complete: function(request){
      $("#aktgeladens1div").html(request.responseText);
        }
        });
  $.ajax({
    url: "/openWB/ramdisk/llaktuell",
    complete: function(request){
		if (request.responseText > 999) {
			    request.responseText = (request.responseText / 1000).toFixed(2);
		    	    request.responseText = request.responseText + " kW";
		    } else {
			request.responseText = request.responseText + " W";
			}
      $("#lldiv").html(request.responseText);
    }
});
  $.ajax({
    url: "/openWB/ramdisk/hausverbrauch",
    complete: function(request){
		if (request.responseText > 999) {
			    request.responseText = (request.responseText / 1000).toFixed(2);
		    	    request.responseText = request.responseText + " kW";
		    } else {
			request.responseText = request.responseText + " W";
			}
      $("#hausverbrauchdiv").html(request.responseText);
    }
});

$.ajax({
    url: "/openWB/ramdisk/llkombiniert",
    complete: function(request){
		if (request.responseText > 999) {
			    request.responseText = (request.responseText / 1000).toFixed(2);
		    	    request.responseText = request.responseText + " kW";
		    } else {
			request.responseText = request.responseText + " W";
			}
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
    url: "/openWB/ramdisk/aktgeladens1",
	    complete: function(request){
		    var aktgeladens1 = request.responseText;
		    document.getElementById("progs1").value= aktgeladens1;
    }
  });
 $.ajax({
    url: "/openWB/ramdisk/aktgeladens2",
	    complete: function(request){
		    var aktgeladens2 = request.responseText;
		    document.getElementById("progs2").value= aktgeladens2;
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/pvwatt",
    complete: function(request){
	    var pvwatt = parseInt(request.responseText, 10);
	if ( pvwatt <= 0){
		pvwatt = pvwatt * -1;
		if (pvwatt > 999) {
			    pvwatt = (pvwatt / 1000).toFixed(2);
		    	    pvwatt = pvwatt + " kW Erzeugung";
		    } else {
			pvwatt = pvwatt + " W Erzeugung";
			}
	}

      $("#pvdiv").html(pvwatt);
    }
  });
 $.ajax({
    url: "/openWB/ramdisk/llaktuells1",
    complete: function(request){
		if (request.responseText > 999) {
			    request.responseText = (request.responseText / 1000).toFixed(2);
		    	    request.responseText = request.responseText + " kW";
		    } else {
			request.responseText = request.responseText + " W";
			}
      $("#lllp2div").html(request.responseText);
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/llaktuells2",
    complete: function(request){
		if (request.responseText > 999) {
			    request.responseText = (request.responseText / 1000).toFixed(2);
		    	    request.responseText = request.responseText + " kW";
		    } else {
			request.responseText = request.responseText + " W";
			}
      $("#lllp3div").html(request.responseText);
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/plugstats1",
    complete: function(request){
		if (request.responseText == 1) {
			var element = document.getElementById("plugstatlp2div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
	
		    } else {
			var element = document.getElementById("plugstatlp2div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
			}
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/plugstat",
    complete: function(request){
		if (request.responseText == 1) {
			var element = document.getElementById("plugstatlp1div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
			    } else {
			var element = document.getElementById("plugstatlp1div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		
			}
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/chargestat",
    complete: function(request){
		if (request.responseText == 1) {
			var element = document.getElementById("plugstatlp1div");

			element.setAttribute("style", "color: #00FF00;");
		    } else {
			var element = document.getElementById("plugstatlp1div");
			element.setAttribute("style", "color: white;");
			}
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/chargestats1",
    complete: function(request){
		if (request.responseText == 1) {
			var element = document.getElementById("plugstatlp2div");

			element.setAttribute("style", "color: #00FF00;");
		    } else {
			var element = document.getElementById("plugstatlp2div");
			element.setAttribute("style", "color: white;");
			}
    }
  });
$.ajax({
    url: "/openWB/ramdisk/llsoll",
    complete: function(request){
      $("#llsolldiv").html(request.responseText);
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/llsolls1",
    complete: function(request){
      $("#llsolllp2div").html(request.responseText);
    }
  });
$.ajax({
    url: "/openWB/ramdisk/llsolls2",
    complete: function(request){
      $("#llsolllp3div").html(request.responseText);
    }
  });
 $.ajax({
    url: "/openWB/ramdisk/wattbezug",
    complete: function(request){
	    var wattbezug = request.responseText;
	    var intbezug = parseInt(wattbezug, 10);
	    if (intbezug > 0) {
		    if (intbezug > 999) {
			    intbezug = (intbezug / 1000).toFixed(2);
		    	    wattbezug = intbezug + " kW Bezug";
		    } else {
			wattbezug = intbezug + " W Bezug";
			}
	    } else {
	    	    intbezug = intbezug * -1;
			if (intbezug > 999) {
			    intbezug = (intbezug / 1000).toFixed(2);
		    	    wattbezug = intbezug + " kW Einspeisung";
		    } else {
			wattbezug = intbezug + " W Einspeisung";
			}
	    }

      $("#bezugdiv").html(wattbezug);
    }
  });
 $.ajax({
    url: "/openWB/ramdisk/glattwattbezug",
    complete: function(request){
      $("#bezugglattdiv").html(request.responseText);
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
   url: "/openWB/ramdisk/soc1",
    complete: function(request){
      $("#soc1level").html(request.responseText);
        }
        });
$.ajax({
   url: "/openWB/ramdisk/restzeitlp1",
    complete: function(request){
      $("#restzeitlp1div").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/restzeitlp2",
    complete: function(request){
      $("#restzeitlp2div").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/restzeitlp3",
    complete: function(request){
      $("#restzeitlp3div").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/gelrlp1",
    complete: function(request){
      $("#gelrlp1div").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/gelrlp2",
    complete: function(request){
      $("#gelrlp2div").html(request.responseText);
        }
	});
  $.ajax({
   url: "/openWB/ramdisk/gelrlp3",
    complete: function(request){
      $("#gelrlp3div").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/aktgeladen",
    complete: function(request){
      $("#aktgeladendiv").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/aktgeladens2",
    complete: function(request){
      $("#aktgeladens2div").html(request.responseText);
        }
        });
//  $.ajax({
//   url: "/openWB/ramdisk/lademodus",
//    complete: function(request){
//      var lademodus=data;
//	console.log(data);
//	}
//	});
 $.ajax({
   url: "/openWB/ramdisk/speichersoc",
    complete: function(request){
      $("#speichersocdiv").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/pluggedladungbishergeladen",
    complete: function(request){
      $("#pluggedladungbishergeladendiv").html(request.responseText);
        }
        });
 $.ajax({
   url: "/openWB/ramdisk/pluggedladungbishergeladenlp2",
    complete: function(request){
      $("#pluggedladungbishergeladenlp2div").html(request.responseText);
        }
        });
$.ajax({
   url: "/openWB/ramdisk/speicherleistung",
    complete: function(request){
	    var speicherwatt = request.responseText;
	    var intspeicherw = parseInt(speicherwatt, 10);
	    if (intspeicherw > 0) {
		   if (intspeicherw > 999) {
			intspeicherw = (intspeicherw / 1000).toFixed(2);
		    	    speicherwatt = intspeicherw + " kW Ladung";
		   } else {
		    speicherwatt = intspeicherw + " W Ladung";
		   }
	    } else {
	    	    intspeicherw = intspeicherw * -1;
	   if (intspeicherw > 999) {
		intspeicherw = (intspeicherw / 1000).toFixed(2);
		speicherwatt = intspeicherw + " kW Entladung";
	} else {
		speicherwatt = intspeicherw + " W Entladung";
	   }
	    }
      $("#speicherleistungdiv").html(speicherwatt);
        }
        });
$.ajax({
   url: "/openWB/ramdisk/lastregelungaktiv",
    complete: function(request){
      $("#lastregelungaktivdiv").html(request.responseText);
        }
        });


}

doInterval = setInterval(getfile, 5000);
do2Interval = setInterval(loadText, 5000);

getfile();
