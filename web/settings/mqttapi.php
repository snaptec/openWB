<?php
# HTTP-API as bridge to MQTT

if(isset($_GET["topic"])) {
	$topic = $_GET["topic"];
	# writing topic
	if(isset($_GET["message"])) {
		$message = $_GET["message"];
		# check if topic is allowed to write
		if(strpos($topic, "/set/") !== false){
			$command = "mosquitto_pub -h localhost -t " . escapeshellarg($topic) . " -m " . escapeshellarg($message) . " 2>&1";
			$output = exec($command);
			# Skip an annoying warning because it doesn't cause any problems
			$output = str_replace("Warning: Unable to locate configuration directory, default config not loaded.", "", $output);
			# no output if mosquitto_pub was successful
			if($output != ""){
				http_response_code(500);
				echo "Error: $output";
			}
			else{
				http_response_code(200);
				echo "Message '$message' successfully published to topic '$topic'.";
			}
		}
		else{
			http_response_code(400);
			echo "Error: Only '.../set/...' topics are allowed to write.";
		}
	}
	# reading topic
	else{
		$command = "mosquitto_sub -h localhost -t " . escapeshellarg($topic) . " -C 1 -W 1 2>&1";
		$output = exec($command);
		# Skip an annoying warning because it doesn't cause any problems
		$output = str_replace("Warning: Unable to locate configuration directory, default config not loaded.", "", $output);
		# no output if mosquitto_sub failed
		if($output != ""){
			http_response_code(200);
			echo $output;
		}
		else{
			http_response_code(404);
			echo "Error: The topic '$topic' doesn't contain a retained value.";
		}
	}
}
else{
	http_response_code(400);
	echo "Error: No 'topic' field provided. \nExample reading a MQTT-Topic: 'http://IP/openWB/web/settings/mqttapi.php?topic=openWB/pv/W' \nExample writing a MQTT-Topic: 'http://IP/openWB/web/settings/mqttapi.php?topic=openWB/set/pv/1/W&message=-1000' ";
}
?>
