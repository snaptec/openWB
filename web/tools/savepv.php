
<?php
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	foreach($_POST as $k => $v) {
	    if(strpos($line, $k.'=') !== false) {
		if ( $k != "hook1ein_url" && $k != "hook1aus_url") {   
		$result .= $k.'='.$v."\n";
		$writeit = '1';
		}
	    } 
	}
	  	    if(strpos($line, "hook1ein_url=") !== false) {
	    $result .= 'hook1ein_url=\''.$_POST[hook1ein_url]."'\n";
	    $writeit = '1';
} 
	    if(strpos($line, "hook1aus_url=") !== false) {
	    $result .= 'hook1aus_url=\''.$_POST[hook1aus_url]."'\n";
	    $writeit = '1';
} 

		if ( $writeit == '0' ) {
		$result .= $line;
	}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);





header("Location: ../index.php");
?>



