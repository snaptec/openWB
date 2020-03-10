
<?php
$result = '';
$lines = file($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf');
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
file_put_contents($_SERVER['DOCUMENT_ROOT'].'/openWB/openwb.conf', $result);

header("Location: ../index.php");
?>
