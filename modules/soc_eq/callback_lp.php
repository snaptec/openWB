<?php
	//Callback procedure for mercedes SoC API LP1 
	if( $_GET["code"] ) {
		$state= escapeshellarg($_GET['state']);
		$code= escapeshellarg($_GET['code']);
		$command = escapeshellcmd($_SERVER['DOCUMENT_ROOT'] . "/openWB/modules/soc_eq/auth.py");
		$system_command = join(" ", [$command, $state, $code]);
		system($system_command);
	}
	else {
		echo "<html>";
		echo "<p>" . $_GET["error"] . "</p>";
		echo "<p>" . $_GET["error_description"] . "</p>";
		echo "</html>";
	}
?>
