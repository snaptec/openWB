
<?php
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	foreach($_POST as $k => $v) {
		if(strpos($line, $k.'=') !== false) {
			$result .= $k.'='.$v."\n";
			$writeit = '1';
		}
	}
	if ( $writeit == '0' ) {
		$result .= $line;
	}
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

header("Location: ../index.php");
?>
