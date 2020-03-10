<?php
$ajax = new Ajaxloader();

//Class for loading Content
class Ajaxloader{

	//Init
	function __construct(){
		$call = $_POST['call'];
		//$text = file_get_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/ramdisk/lademodus');

		$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf');
		foreach($lines as $line) {
			if(strpos($line, "debug=") !== false) {
				list(, $debugold) = explode("=", $line);
			}
		}

		if($call == "loadfile"){
			$result = $debugold;
			header("Content-type: text/json");
			echo json_encode(array("text"=> $result));
		}
	}

}
?>
