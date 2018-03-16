
<?php
if(isset($_POST['sofortll'])) {
$data = $_POST['sofortll'];
$config['sofortll'] = $_POST['sofortll'];

$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	    if(substr($line, 0, 9) == 'sofortll=') {
	    $result .= 'sofortll='.$config['sofortll']."\n";
	    } else {
	    $result .= $line;
	    }
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);
}
header("Location: ../index.php");
?>



