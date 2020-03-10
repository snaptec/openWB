<?php
$result = '';
$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf');
foreach($lines as $line) {
		$writeit = '0';
	if(strpos($line, "releasetrain=") !== false) {
		$result .= 'releasetrain='.$_POST['releasetrainCheckbox']."\n";
		$writeit = '1';
	} 

	if ( $writeit == '0') {
		$result .= $line;
	}
}
file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf', $result);

header("Location: ./updateredirect.html");
?>
