<?php
   //Callback procedure for mercedes SoC API LP1 
   if( $_GET["code"] ) {
      system( "/var/www/html/openWB/modules/soc_eq/auth.py " . $_GET['state'] . " " . $_GET['code']) ;
   }
   else {
      echo "<html>";
      echo "<p>" . $_GET["error"] . "</p>";
      echo "<p>" . $_GET["error_description"] . "</p>";
      echo "</html>";
   }
?>
