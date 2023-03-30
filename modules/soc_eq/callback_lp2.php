<?php
	//Callback procedure for mercedes SoC API LP2 
	if( $_GET["code"] ) {
		$code= escapeshellarg($_GET['code']);
		$command = escapeshellcmd($_SERVER['DOCUMENT_ROOT'] . "/openWB/modules/soc_eq/auth.py" );
		$system_command = join(" ", [$command, "2", $code]);
		system( $system_command);
	}
	else {
		echo "<html>";
		echo "<p>" . $_GET["error"] . "</p>";
		echo "<p>" . $_GET["error_description"] . "</p>";
		echo "</html>";
	}
?>
