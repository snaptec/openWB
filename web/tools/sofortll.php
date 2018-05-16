
<?php
if(isset($_POST['sofortll'])) {

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortll=") !== false) {
	       $result .= 'sofortll='.$_POST[sofortll]."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
}
header("Location: ../index.php");
?>



