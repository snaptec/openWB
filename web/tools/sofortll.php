
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
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortlls1=") !== false) {
	       $result .= 'sofortlls1='.$_POST[sofortlls1]."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
       if(strpos($line, "sofortlls2=") !== false) {
	       $result .= 'sofortlls2='.$_POST[sofortlls2]."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

}
header("Location: ../index.php");
?>



