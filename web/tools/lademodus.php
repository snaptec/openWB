<?php

$ajax = new Ajaxloader();

 //Class for loading Content
 class Ajaxloader{

  //Init
  function __construct(){
   	$call = $_POST['call'];
	$text = file_get_contents('/var/www/html/openWB/ramdisk/lademodus');

   if($call == "loadfile"){
	   $result = $text;
	   echo json_encode(array("text"=> $result));
   }
  }


 }

?>
