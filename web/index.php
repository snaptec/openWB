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
</script>
<script type='text/javascript'>
var doInterval;
function getfile() {
  $.ajax({
   url: "/openWB/web/error.log",
    complete: function(request){
      $("#errorfeed").html(request.responseText);
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
                            		<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">PV
                        			<div id="pvdiv"></div> 
			                </button>
               			</div>
				<div class="col-xs-6 text-center">
                                        <button type="button" class="btn btn-primary btn-lg btn-block btn-blue">EVU Bezug
                                                <div id="bezugdiv"></div> 
                                        </button>
                                </div>  
			</div>	
			<div class="row">
				<div class="col-xs-6 text-center">		
		                	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">Ladung 
                        			<div id="lldiv"></div>
					</button>
				</div>
				<div class="col-xs-6 text-center">
                                	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">SOC
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
                	             	<button type="button" class="btn btn-primary btn-lg btn-block btn-blue">LLSoll
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
						    if(substr($line, 0, 9) == 'sofortll=') {
						    $sofortllold = substr($line, 9, 2);
	    
						    }
						}
					?>
					<form name="sofortll" action="./tools/sofortll.php" method="POST">
						<label for="sofortll">Sofortladen A:</label>
						<input type="number" min="10" max="32" name="sofortll" id="sofortll" value="<?php echo $sofortllold ?>">
						<br>
						<button type="submit" class="btn btn-primary btn-lg btn-block btn-grey">Save</button>	 
					 </form>

				</div>
			</div>
			<hr>
			<div class="row">
				<div class="col-xs-6">
					Ver0.16
				</div>
				<div class="col-xs-6 text-right">
					<a href="settings.php">Einstellungen</a> 
				</div>
			</div>
			<div id="errorfeed"></div>
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



