<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Kevin Wieland" />
	<!-- Favicons (created with http://realfavicongenerator.net/)-->
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="img/favicons/manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<!-- Owl -->
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<!-- Animate.css -->
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome -->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.1.0/css/font-awesome.min.css">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>
<?php
require 'config.php';
?>
<script type='text/javascript'>
setInterval(loadText, 2000);
function loadText(){
 $.ajax({
  url:"./tools/debugmode.php",  
  type: "post", //request type,
  dataType: 'json',
  data: {call: "loadfile"},
  success:function(result){
   if(result.text == 0){
    $('#errorfeed').hide();
   }
   if(result.text == 1){
	 $('#errorfeed').show();
    }
   if(result.text == 2){
 	 $('#errorfeed').show(); 
	}

  }
 });
}
</script> 

<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
    url: "/openWB/ramdisk/llkombiniert",
    complete: function(request){
      $("#lldiv").html(request.responseText);
    }
  });
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
    url: "/openWB/ramdisk/pvwatt",
    complete: function(request){
      $("#pvdiv").html(request.responseText);
    }
  });
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
    url: "/openWB/ramdisk/llsoll",
    complete: function(request){
      $("#llsolldiv").html(request.responseText);
    }
  });
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
    url: "/openWB/ramdisk/wattbezug",
    complete: function(request){
      $("#bezugdiv").html(request.responseText);
    }
  });
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
function getfile() {
  $.ajaxSetup({ cache: false});
  $.ajax({
   url: "/openWB/ramdisk/ladestatus",
    complete: function(request){
      $("#controlleranaus").html(request.responseText);
	}
	});
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajaxSetup({ cache: false});
  $.ajax({
   url: "/openWB/ramdisk/soc",
    complete: function(request){
      $("#soclevel").html(request.responseText);
        }
        });
}
doInterval = setInterval(getfile, 2000);
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
   url: "/openWB/ramdisk/lademodus",
    complete: function(request){
      var lademodus=data;
	console.log(data);
	}
	});
}
doInterval = setInterval(getfile, 2000);
</script> <!--
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
   url: "/openWB/ramdisk/openWB.log",
	   complete: function(request){
//	$("#errorfeed").html(request.replace(/\\n/g,"<br>").responseText);
	$("#errorfeed").html(request.responseText);
	}
	});
}
doInterval = setInterval(getfile, 2000);
</script> -->
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
   url: "/openWB/ramdisk/openWB.log",
   dataType: "text",
   success : function (data) {
	  //  $("#errorfeed").html(data.replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g,"<br>"));
	   	 $("#errorfeedcontent").html(data.replace(/\n/g, "<br />"));
	}
	});
}
doInterval = setInterval(getfile, 2000);
</script>


<body>


	<div class="preloader">
		<img src="img/loader.gif" alt="Preloader image">
	</div>
	
	<section id="services">
		<div class="container">
			<div class="row">
				<div class="col-xs-12 text-center">
					<h3> OpenWB Charge Controller </h3>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-6 text-center">                     
                            		<button type="button" class="btn btn-primary btn-lg btn-block btn-green">PV in Watt
                        			<div id="pvdiv"></div> 
			                </button>
               			</div>
				<div class="col-xs-6 text-center">
                                        <button type="button" class="btn btn-primary btn-lg btn-block btn-orange">EVU Bezug in Watt
                                                <div id="bezugdiv"></div> 
                                        </button>
                                </div>  
			</div>	
			<div class="row">
				<div class="col-xs-6 text-center">		
		                	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladeleistung in Watt
                        			<div id="lldiv"></div>
					</button>
				</div>
				<div class="col-xs-6 text-center">
                                	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">SOC in %
					<div id="soclevel"></div>
					</button>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-6 text-center">
					<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladestatus
					<div id="controlleranaus"></div>
					</button>
				</div>
				<div class="col-xs-6 text-center">
                	             	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladeleistung Soll  in A
					<div id="llsolldiv"></div>
					</button>
				</div>
			
			</div>
			<div class="row">
					<?php
						$result = '';
						$lines = file('/var/www/html/openWB/openwb.conf');
						foreach($lines as $line) {
						    if(substr($line, 0, 11) == 'nachtladen=') {
						    $nachtladenold = substr($line, 11, 2);
	    
						    }
						}
					?>
					<?php
						$result = '';
						$lines = file('/var/www/html/openWB/openwb.conf');
						foreach($lines as $line) {
						    if(substr($line, 0, 15) == 'lastmanagement=') {
						    $lastmanagementold = substr($line, 15, 2);
	    
						    }
						}
					?>

					<div class="col-xs-6 text-center">
                	             		<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Nachtladen <?php echo $nachtladenold ?>
					</button>
					</div>
				
					<div class="col-xs-6 text-center">
                	             	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Lastmanagement <?php echo $lastmanagementold ?>

					</button>
					</div>

			</div>

			<hr>
			<div class="col-xs-12 text-center">
				<h4>Lademodus</h4>
			</div>	
                        <div class="row">
                                <div class="col-xs-6 text-center">
					<div class="actstat">
						<a href="./tools/changelademodus.php?jetzt=1" class="btn btn-lg btn-block">Sofort Laden</a>
					</div>
                           	</div>
                                <div class="col-xs-6 text-center">
                                        <div class="actstat1">
                                                <a href="./tools/changelademodus.php?minundpv=1" class="btn btn-lg btn-block">Min + PV</a>
                                        </div>
				</div>
			</div>
			<div class="row">
				<div class="col-xs-6 text-center">
					<div class="actstat3">
						<a href="./tools/changelademodus.php?stop=1" class="btn btn-lg btn-block">Stop</a>
					</div>
				</div>
				<div class="col-xs-6 text-center">
                                        <div class="actstat2">
					        <a href="./tools/changelademodus.php?pvuberschuss=1" class="btn btn-lg btn-block">Nur PV</a>
                                        </div>
				</div>
			</div>
			<div class="row">
			<hr>
			</div>
			<div class="row">
				<div class="col-xs-12 text-center">
					<?php
						$result = '';
						$lines = file('/var/www/html/openWB/openwb.conf');
						foreach($lines as $line) {
							if(strpos($line, "minimalstromstaerke=") !== false) {
										list(, $minimalstromstaerkeold) = explode("=", $line);
											}
							if(strpos($line, "maximalstromstaerke=") !== false) {
										list(, $maximalstromstaerkeold) = explode("=", $line);
							}
							if(strpos($line, "sofortll=") !== false) {
								list(, $sofortllold) = explode("=", $line);
							}
						}

					?>
					<form name="sofortll" action="./tools/sofortll.php" method="POST">
						<div class="col-xs-4 text-center">
						<input type="range" min=<?php echo $minimalstromstaerkeold ?> max=<?php echo $maximalstromstaerkeold ?> step="1" name="sofortll" id="sofortll" value=<?php echo $sofortllold ?>>
						</div>
						<div class="col-xs-4 text-center">
						<label for="sofortll">Sofortladen: <span id="sofortlll"></span>A</label>
						</div>
						<script>
						var slider = document.getElementById("sofortll");
						var output = document.getElementById("sofortlll");
						output.innerHTML = slider.value;

						slider.oninput = function() {
						  output.innerHTML = this.value;
						}
						</script>
						<div class="col-xs-4 text-center">
						<button type="submit" class="btn btn-primary btn-lg btn-block btn-grey">Save</button>	 
						</div>
					 </form>

				</div>
			</div>
			<hr>
			
		<!--	<div class="row">
				<iframe frameBorder="0" height="312" class="col-xs-12" src="/metern/index2.php"></iframe>
			</div> -->
			<div class="row">
				<div class="col-xs-4">
					Ver0.36
				</div>
				<div class="col-xs-4 text-center">
					<a href="http://openwb.de">www.openwb.de</a>
				</div>
				<div class="col-xs-4 text-right">
					<a href="settings.php">Einstellungen</a> 
				</div>
			</div>
			<div class="row">
				<div class="col-xs-4 text-center">
				</div>

				<div class="col-xs-4 text-center">
					<a href="/metern/index.php">Logging</a>
				</div>
				<div class="col-xs-4 text-right">
					<a href="status.php">Status</a> 
				</div>

			</div>
			<div id="errorfeed">
			<div id="errorfeedcontent"></div>

			</div>
		</div>
	</section>
	<!-- Holder for mobile navigation -->
	<div class="mobile-nav">
		<ul>
		</ul>
		<a href="#" class="close-link"><i class="arrow_up"></i></a>
	</div>
	<!-- Scripts -->
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
	<script src="js/main.js"></script>
	<script type='text/javascript'>
setInterval(loadText, 2000);
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
    }
   if(result.text == 2){
    $('.actstat2 .btn').addClass("btn-green");
    $('.actstat .btn').addClass("btn-red");    
    $('.actstat1 .btn').addClass("btn-red");
    $('.actstat3 .btn').addClass("btn-red");
    $('.actstat .btn').removeClass("btn-green");
    $('.actstat3 .btn').removeClass("btn-green");
    $('.actstat1 .btn').removeClass("btn-green");    
	}
     if(result.text == 3){
    $('.actstat2 .btn').addClass("btn-red");
    $('.actstat3 .btn').addClass("btn-green");
    $('.actstat .btn').addClass("btn-red");    
    $('.actstat1 .btn').addClass("btn-red");
    $('.actstat .btn').removeClass("btn-green");
    $('.actstat1 .btn').removeClass("btn-green");    
	}

  }
 });
}
</script>
</body>

</html>



