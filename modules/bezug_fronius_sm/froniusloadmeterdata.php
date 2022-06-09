<?php
	$url = "http://".$_GET["ip"]."/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System";

	ini_set("default_socket_timeout", 5);
	header('Content-Type: application/json');
	echo file_get_contents($url);
?>