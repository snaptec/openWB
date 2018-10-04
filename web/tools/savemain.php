
<?php

foreach($_POST as $k => $v) {
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
	    if(strpos($line, $k.'=') !== false) {
	    	$result .= $k.'='.$v."\n";
	    } 
	    else {
	    	$result .= $line;
	    }
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);

}






header("Location: ../index.php");
?>



