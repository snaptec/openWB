<?php
$ajax = new Ajaxloader();

class Ajaxloader{

	function __construct(){
		$call = $_POST['dailychargelp3call'];
		$daydate1 = date('Y-m-d');
		$daydate = date("Ymd", strtotime($daydate1));
		$csv = array_map('str_getcsv', file('/var/www/html/openWB/web/logging/data/daily/'.$daydate.'.csv'));
		$firstev = $csv[0][6];
		$lastev = end($csv)[6];
		$dailyevlp3 = number_format((($lastev - $firstev) / 1000), 2);

		if($call == "loadfile"){
			$result = $dailyevlp3;
			header("Content-type: application/json");
			echo json_encode(array("text"=> $result));
		}
	}

}
?>
