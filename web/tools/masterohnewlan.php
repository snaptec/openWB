<?php
exec("sudo /var/www/html/openWB/runs/masterohnewlan.sh");
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
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
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
?>
