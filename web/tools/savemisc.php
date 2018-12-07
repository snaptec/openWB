
<?php
if(isset($_POST['debug'])) {
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "debug=") !== false) {
	    $result .= 'debug='.$_POST[debug]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "dspeed=") !== false) {
	    $result .= 'dspeed='.$_POST[dspeed]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "livegraph=") !== false) {
	    $result .= 'livegraph='.$_POST[livegraph]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "releasetrain=") !== false) {
	    $result .= 'releasetrain='.$_POST[releasetrain]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "logdailywh=") !== false) {
	    $result .= 'logdailywh='.$_POST[logdailywh]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);


}


header("Location: ../index.php");

?>



