<?php
$ajax = new Ajaxloader();

class Ajaxloader{

	function __construct(){
		$call = $_POST['dailychargelp1call'];
		$daydate1 = date('Y-m-d');
		$daydate = date("Ymd", strtotime($daydate1));
		$ll1file = '/var/www/html/openWB/web/logging/data/daily/'.$daydate.'-ll1.csv';
		$ll1 = file($ll1file, FILE_IGNORE_NEW_LINES);
		$firstev = reset($ll1);
		$lastev = end($ll1);
		$dailyevlp1 = number_format((($lastev - $firstev) / 1000), 2);

		if($call == "loadfile"){
			$result = $dailyevlp1;
			header("Content-type: application/json");
			echo json_encode(array("text"=> $result));
		}
	}

}
?>
