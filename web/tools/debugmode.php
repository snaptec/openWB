<?php
$ajax = new Ajaxloader();

//Class for loading Content
class Ajaxloader{

	//Init
	function __construct(){
		$call = $_POST['call'];
		//$text = file_get_contents('/var/www/html/openWB/ramdisk/lademodus');

		$lines = file('/var/www/html/openWB/openwb.conf');
		foreach($lines as $line) {
			if(strpos($line, "debug=") !== false) {
				list(, $debugold) = explode("=", $line);
			}
		}

		if($call == "loadfile"){
			$result = $debugold;
			header("Content-type: application/json");
			echo json_encode(array("text"=> $result));
		}
	}

}
?>
