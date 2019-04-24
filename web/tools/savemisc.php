
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
	    if(strpos($line, "pushbenachrichtigung=") !== false) {
	    $result .= 'pushbenachrichtigung='.$_POST[pushbenachrichtigung]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "pushbstartl=") !== false) {
	    $result .= 'pushbstartl='.$_POST[pushbstartl]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "pushbstopl=") !== false) {
	    $result .= 'pushbstopl='.$_POST[pushbstopl]."\n";
	    $writeit = '1';
	    } 
	    if(strpos($line, "pushovertoken=") !== false) {
	    $result .= 'pushovertoken=\''.$_POST[pushovertoken]."'\n";
		$writeit = '1';
   	 	} 
	    if(strpos($line, "pushoveruser=") !== false) {
	    $result .= 'pushoveruser=\''.$_POST[pushoveruser]."'\n";
	   	$writeit = '1';
 		} 
	   if(strpos($line, "grapham=") !== false) {
	    $result .= 'grapham='.$_POST[grapham]."\n";
	    $writeit = '1';
	    } 
	   if(strpos($line, "graphliveam=") !== false) {
	    $result .= 'graphliveam='.$_POST[graphliveam]."\n";
	    $writeit = '1';
	    } 
	   if(strpos($line, "graphinteractiveam=") !== false) {
	    $result .= 'graphinteractiveam='.$_POST[graphinteractiveam]."\n";
	    $writeit = '1';
	    } 
	   if(strpos($line, "chartlegendmain=") !== false) {
	    $result .= 'chartlegendmain='.$_POST[chartlegendmain]."\n";
	    $writeit = '1';
	    } 
	   if(strpos($line, "hausverbrauchstat=") !== false) {
	    $result .= 'hausverbrauchstat='.$_POST[hausverbrauchstat]."\n";
	    $writeit = '1';
	    } 
	   if(strpos($line, "heutegeladen=") !== false) {
	    $result .= 'heutegeladen='.$_POST[heutegeladen]."\n";
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



