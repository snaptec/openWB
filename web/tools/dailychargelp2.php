<?php
$ajax = new Ajaxloader();

 class Ajaxloader{

  function __construct(){
   	$call = $_POST['dailychargelp2call'];
	$daydate1 = date('Y-m-d');
	$daydate = date("Ymd", strtotime($daydate1));
	$ll2file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll2.csv';
	$ll2 = file($ll2file, FILE_IGNORE_NEW_LINES);

	$firstev = reset($ll2);
	$lastev = end($ll2);
	$dailyevlp2 = number_format((($lastev - $firstev) / 1000), 2);


   if($call == "loadfile"){
	   $result = $dailyevlp2;
	   echo json_encode(array("text"=> $result));
   }
  }


 }

?>






