<?php
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	foreach($_POST as $k => $v) {
		if(strpos($line, $k.'=') !== false) {
			if ( $k != "zielladenuhrzeitlp1") {
				$result .= $k.'='.$v."\n";
				$writeit = '1';
			}
		}
	}
	if (strpos($line, "zielladenuhrzeitlp1=") !== false) {
		$result .= 'zielladenuhrzeitlp1=\''.$_POST['zielladenuhrzeitlp1']."'\n";
		$writeit = '1';
	} 

	if ( $writeit == '0' ) {
		$result .= $line;
	}
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

header("Location: ../index.php");
?>
