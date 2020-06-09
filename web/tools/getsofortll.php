<?php
$ajax = new Ajaxloader();

//Class for loading Content
class Ajaxloader{

	//Init
	function __construct(){
		$lines = file('/var/www/html/openWB/openwb.conf');
		foreach($lines as $line) {
			if(strpos($line, "sofortll=") !== false) {
				list(, $sofortllold) = explode("=", $line);
			}
		}
		$call = $_POST['call'];
		if($call == "loadfile"){
			$result = $sofortllold;
			header("Content-type: application/json");
			echo json_encode(array("text"=> $result));
		}
	}

}
?>
