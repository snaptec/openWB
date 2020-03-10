<?php
exec("sudo ".$_SERVER['DOCUMENT_ROOT']."/openWB/runs/masterohnewlan.sh");
$result = '';
$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	if(strpos($line, "displayconfigured=") !== false) {
		$result .= 'displayconfigured=1'."\n";
		$writeit = '1';
	}
	if ( $writeit == '0') {
		$result .= $line;
	}
}
file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf', $result);
?>
