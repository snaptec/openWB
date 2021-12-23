<?php
   //Callback procedure for mercedes SoC API LP1 
   if( $_GET["code"] ) {
      system( "/var/www/html/openWB/modules/soc_eq/auth.py 1 " . $_GET['code']) ;
   }
?>
