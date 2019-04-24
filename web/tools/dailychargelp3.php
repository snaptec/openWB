<?php
$ajax = new Ajaxloader();

 class Ajaxloader{

  function __construct(){
   	$call = $_POST['dailychargelp3call'];
	$daydate1 = date('Y-m-d');
	$daydate = date("Ymd", strtotime($daydate1));
	$ll3file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll3.csv';
	$ll3 = file($ll3file, FILE_IGNORE_NEW_LINES);

	$firstev = reset($ll3);
	$lastev = end($ll3);
	$dailyevlp3 = number_format((($lastev - $firstev) / 1000), 2);


   if($call == "loadfile"){
	   $result = $dailyevlp3;
	   echo json_encode(array("text"=> $result));
   }
  }


 }

?>






