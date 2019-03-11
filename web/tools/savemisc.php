
<?php
if(isset($_POST['debug'])) {
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
		$writeit = '0';
	if(strpos($line, "debug=") !== false) {
	    $result .= 'debug='.$_POST[debug]."\n";
	$writeit = '1';
	    } 
	    if(strpos($line, "dspeed=") !== false) {
	    $result .= 'dspeed='.$_POST[dspeed]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "livegraph=") !== false) {
	    $result .= 'livegraph='.$_POST[livegraph]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "releasetrain=") !== false) {
	    $result .= 'releasetrain='.$_POST[releasetrain]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "logdailywh=") !== false) {
	    $result .= 'logdailywh='.$_POST[logdailywh]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "logeinspeisungneg=") !== false) {
	    $result .= 'logeinspeisungneg='.$_POST[logeinspeisungneg]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "ladetaster=") !== false) {
	    $result .= 'ladetaster='.$_POST[ladetaster]."\n";
	    $writeit = '1';
	    } 
	    if ( $writeit == '0') {
		$result .= $line;
	    }

}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);



}


header("Location: ../index.php");

?>



