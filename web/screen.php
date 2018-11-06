<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="OpenWB" />
	<meta name="keywords" content="OpenWB" />
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
<script src="screen.js"></script>

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
		if(strpos($line, "sofortlls1=") !== false) {
			list(, $sofortlls1old) = explode("=", $line);
		}
		if(strpos($line, "sofortlls2=") !== false) {
			list(, $sofortlls2old) = explode("=", $line);
		}
		if(strpos($line, "lastmanagement=") !== false) {
			list(, $lastmanagementold) = explode("=", $line);
		}
		if(strpos($line, "lastmanagements2=") !== false) {
			list(, $lastmanagements2old) = explode("=", $line);
		}
		if(strpos($line, "lademstat=") !== false) {
			list(, $lademstatold) = explode("=", $line);
		}
		if(strpos($line, "lademstats1=") !== false) {
			list(, $lademstats1old) = explode("=", $line);
		}
		if(strpos($line, "lademkwh=") !== false) {
			list(, $lademkwhold) = explode("=", $line);
		}
		if(strpos($line, "lademkwhs1=") !== false) {
			list(, $lademkwhs1old) = explode("=", $line);
		}
		if(strpos($line, "lademstats2=") !== false) {
			list(, $lademstats2old) = explode("=", $line);
		}
		if(strpos($line, "lademkwhs2=") !== false) {
			list(, $lademkwhs2old) = explode("=", $line);
		}
		if(strpos($line, "sofortsoclp1=") !== false) {
			list(, $sofortsoclp1old) = explode("=", $line);
		}
		if(strpos($line, "sofortsoclp2=") !== false) {
			list(, $sofortsoclp2old) = explode("=", $line);
		}
		if(strpos($line, "sofortsoclp3=") !== false) {
			list(, $sofortsoclp3old) = explode("=", $line);
		}
		if(strpos($line, "sofortsocstatlp1=") !== false) {
			list(, $sofortsocstatlp1old) = explode("=", $line);
		}
		if(strpos($line, "sofortsocstatlp2=") !== false) {
			list(, $sofortsocstatlp2old) = explode("=", $line);
		}
		if(strpos($line, "sofortsocstatlp3=") !== false) {
			list(, $sofortsocstatlp3old) = explode("=", $line);
		}
		if(strpos($line, "msmoduslp1=") !== false) {
			list(, $msmoduslp1old) = explode("=", $line);
		}
		if(strpos($line, "msmoduslp2=") !== false) {
			list(, $msmoduslp2old) = explode("=", $line);
		}

	}
	$lademodusold = file_get_contents('/var/www/html/openWB/ramdisk/lademodus');
?>	

<body>


<div class="preloader">
	<img src="img/loader.gif" alt="Preloader image">
</div>
<section id="services">
<div class="container">
	<div class="row">
		<div class="col-xs-12 text-center">
			OpenWB
		</div>
	</div>
	<div class="row"><div class="col-xs-12 text-center">
		<div class="col-xs-6 text-center bg-success" style="font-size: 6vw">
			PV: <span id="pvdiv"></span>Watt 
		</div>
		<div class="col-xs-6 text-center bg-warning" style="font-size: 6vw">
			EVU: <span id="bezugdiv"></span>Watt 
		</div>
	</div>
</div>
<div class="row">
	<div class="col-xs-12 text-center">
		<div class="imgwrapper">	
			<img id="livegraph" src="graph-screen.php"
			alt="Graph" class="img-responsive" />
		</div>
	</div>
</div>
<div class="row">	
	<div class="col-xs-8 text-center bg-primary" style="font-size: 5vw">
		LP1: <span id="lldiv"></span>Watt, <span id="llsolldiv"></span>A 
	</div>
	<div class="col-xs-4 text-center bg-primary" style="font-size: 5vw">
		SoC: <span id="soclevel"></span>% 
</div>
<div class="row">	
</div>
			
<div class="row" style="font-size: 2vw">
	<div class="col-xs-6 text-center" style="font-size: 5vw">
		LP1 <span id="gelrlp1div"></span>km,<span id="aktgeladendiv"></span>kWh	<br><span id="sofortlmdiv"><div id="lademstatdiv">
					<progress id="prog1" value= "0" max=<?php echo $lademkwhold ?>></progress>
					</div></span>
	</div>

	<div class="col-xs-6">
		<div id="actstat" class="bg-success">
			<div class="text-center" style="font-size: 5vw">Sofort Laden</div>
		</div>
                <div id="actstat1" class="bg-success">
	                <div class="text-center" style="font-size: 5vw">Min + PV</div>
                </div>
		<div id="actstat2" class="bg-success">
		        <div class="text-center" style="font-size: 5vw">Nur PV</div>
                </div>
		<div id="actstat3" class="bg-danger">
			<div class="text-center" style="font-size: 5vw">Stop</div>
		</div>
        </div>

</div>	
</div>
<script>
	$(function() {
	   if($('#lastmanagement').val() == '0') {
		$('#ladepunkts1ndiv').show(); 
		$('#ladepunkts1div').hide();
		$('#ladepunkts11div').hide();
		$('#ladepunkts111div').hide();
		$('#ladepunkts1111div').hide();
		$('#ladepunkts11111div').hide();
		$('#ladepunkts111111div, #ladepunkts1111111div, #lp2lldiv, #gesamtlldiv').hide();
	      } else {
		$('#ladepunkts1ndiv').hide();
		$('#ladepunkts1div').show();
		$('#ladepunkts11div').show();
		$('#ladepunkts111div').show();	
		$('#ladepunkts1111div').show();
		$('#ladepunkts11111div').show();
		$('#ladepunkts111111div, #ladepunkts1111111div, #lp2lldiv, #gesamtlldiv').show();
	      } 
	});
</script>
<input hidden name="lademlp1stat" id="lademlp1stat" value="<?php echo $lademstatold ; ?>">
<script>
	$(function() {
	   if($('#lademlp1stat').val() == '1') {
		$('#lademstatdiv').show();
		$('#lademstat1div').show(); 
	      } else {
		$('#lademstatdiv').hide();
		$('#lademstat1div').hide();
	      } 
	});
</script>
<input hidden name="lademlp2stat" id="lademlp2stat" value="<?php echo $lademstats1old ; ?>">
<script>
	$(function() {
	   if($('#lademlp2stat').val() == '1') {
		$('#lademstats1div, #lademstats1div1').show(); 
	      } else {
		$('#lademstats1div, #lademstats1div1').hide();
	      } 
	});
</script>
</section>
	<!-- Holder for mobile navigation -->
	<!-- Scripts -->
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/wow.min.js"></script>
	<script src="js/typewriter.js"></script>
	<script src="js/jquery.onepagenav.js"></script>
	<script src="js/main.js"></script>
	<input hidden name="sofortlm" id="sofortlm" value="<?php echo $lademodusold ; ?>">
	<script>
	$(function() {
   	   if($('#sofortlm').val() == '0') {
		$('#sofortlmdiv, #sofortlmdiv1, #sofortlmdiv2').show(); 
	      } else {
		$('#sofortlmdiv, #sofortlmdiv1, #sofortlmdiv2').hide();
		      } 
		});
	</script>

	<script type='text/javascript'>
	loadText();
function loadText(){
 $.ajax({
  url:"./tools/lademodus.php",  
  type: "post", //request type,
  dataType: 'json',
  data: {call: "loadfile"},
  success:function(result){
   if(result.text == 0){
    $('#actstat').show(); 
    $('#actstat1').hide(); 
    $('#actstat2').hide(); 
    $('#actstat3').hide(); 
   }
   if(result.text == 1){
    $('#actstat').hide(); 
    $('#actstat1').show(); 
    $('#actstat2').hide(); 
    $('#actstat3').hide(); 
    }
   if(result.text == 2){
    $('#actstat').hide(); 
    $('#actstat1').hide(); 
    $('#actstat2').show(); 
    $('#actstat3').hide(); 
 
}
     if(result.text == 3){
    $('#actstat').hide(); 
    $('#actstat1').hide(); 
    $('#actstat2').hide(); 
    $('#actstat3').show(); 
  
     }

  }
 });
}

</script>
<script>
$(function() {
      if($('#msmoduslp1').val() == '0') {
		$('#msmodusnlp1').show(); 
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').hide();
      } 
     if($('#msmoduslp1').val() == '1') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').show();
      } 
     if($('#msmoduslp1').val() == '2') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').show();
		$('#msmodusmlp1').hide();
      } 

	$('#msmoduslp1').change(function(){
      if($('#msmoduslp1').val() == '0') {
		$('#msmodusnlp1').show(); 
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').hide();
      } 
     if($('#msmoduslp1').val() == '1') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').hide();
		$('#msmodusmlp1').show();
      } 
     if($('#msmoduslp1').val() == '2') 
      {
		$('#msmodusnlp1').hide();
		$('#msmodusslp1').show();
		$('#msmodusmlp1').hide();
      } 
	    });
});
</script>
<script>
$(function() {
      if($('#msmoduslp2').val() == '0') {
		$('#msmodusnlp2').show(); 
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').hide();
      } 
     if($('#msmoduslp2').val() == '1') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').show();
      } 
     if($('#msmoduslp2').val() == '2') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').show();
		$('#msmodusmlp2').hide();
      } 

	$('#msmoduslp2').change(function(){
      if($('#msmoduslp2').val() == '0') {
		$('#msmodusnlp2').show(); 
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').hide();
      } 
     if($('#msmoduslp2').val() == '1') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').hide();
		$('#msmodusmlp2').show();
      } 
     if($('#msmoduslp2').val() == '2') 
      {
		$('#msmodusnlp2').hide();
		$('#msmodusslp2').show();
		$('#msmodusmlp2').hide();
      } 
	    });
});
</script>
<script>
$(function() {
      if($('#lademlp3check').val() == '0') {
		$('#msmodusnlp3').show(); 
		$('#msmodusmlp3').hide();
      } 
     if($('#lademlp3check').val() == '1') 
      {
		$('#msmodusnlp3').hide();
		$('#msmodusmlp3').show();
      } 
	$('#lademlp3check').change(function(){
      if($('#lademlp3check').val() == '0') {
		$('#msmodusnlp3').show(); 
		$('#msmodusmlp3').hide();
      } 
     if($('#lademlp3check').val() == '1') 
      {
		$('#msmodusnlp3').hide();
		$('#msmodusmlp3').show();
      } 
       
	    });
});
</script>



</body>

</html>



