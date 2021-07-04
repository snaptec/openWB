<?php
   //Callback procedure for mercedes SoC API LP2 
   if( $_GET["code"] ) {
	   system( "/var/www/html/openWB/modules/soc_eq/auth.py 2 " . $_GET['code']) ;
   }
?>
