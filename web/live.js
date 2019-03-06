
var doInterval;
function getfile() {
$.ajaxSetup({ cache: false});
 $.ajax({
   url: "/openWB/ramdisk/aktgeladens1",
    complete: function(request){
      $("#aktgeladens1div").html(request.responseText);
        }
        });
  $.ajax({
    url: "/openWB/ramdisk/llaktuell",
    complete: function(request){
      $("#lldiv").html(request.responseText);
    }
});
$.ajax({
    url: "/openWB/ramdisk/llkombiniert",
    complete: function(request){
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
      $("#pvdiv").html(request.responseText);
    }
  });
 $.ajax({
    url: "/openWB/ramdisk/llaktuells1",
    complete: function(request){
      $("#lllp2div").html(request.responseText);
    }
  });
  $.ajax({
    url: "/openWB/ramdisk/llaktuells2",
    complete: function(request){
      $("#lllp3div").html(request.responseText);
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
      $("#bezugdiv").html(request.responseText);
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
  $.ajax({
   url: "/openWB/ramdisk/lademodus",
    complete: function(request){
      var lademodus=data;
	console.log(data);
	}
	});
 $.ajax({
   url: "/openWB/ramdisk/speichersoc",
    complete: function(request){
      $("#speichersocdiv").html(request.responseText);
        }
        });
$.ajax({
   url: "/openWB/ramdisk/speicherleistung",
    complete: function(request){
      $("#speicherleistungdiv").html(request.responseText);
        }
        });
$.ajax({
   url: "/openWB/ramdisk/lastregelungaktiv",
    complete: function(request){
      $("#lastregelungaktivdiv").html(request.responseText);
        }
        });


var source = 'graph-live.php',
		        timestamp = (new Date()).getTime(),
		        newUrl = source + '?_=' + timestamp;
	    document.getElementById("livegraph").src = newUrl;


}
doInterval = setInterval(getfile, 5000);
getfile();

