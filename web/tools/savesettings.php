
<?php
echo hello;
echo $_POST[sofortll];
echo $_POST[debug];
echo danach;
if(isset($_POST['debug'])) {
$result = '';

$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(strpos($line, "sofortll=") !== false) {
	    $result .= 'sofortll='.$_POST[sofortll]."\n";
	    } 
	    else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

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





}
//header("Location: ../settings.php");

?>



