
<?php
$result = '';
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	$writeit = '0';
	foreach($_POST as $k => $v) {
		if(strpos($line, $k.'=') !== false) {
			if ( $k != "hook1ein_url" && $k != "hook1aus_url" && $k != "hook2ein_url" && $k != "hook2aus_url" && $k != "angesteckthooklp1_url" && $k != "hook3ein_url" && $k != "hook3aus_url" && $k != "verbraucher1_urlw" && $k != "verbraucher1_urlh" && $k != "verbraucher2_urlw" && $k != "verbraucher2_urlh") {   
				$result .= $k.'='.$v."\n";
				$writeit = '1';
			}
		}
	}
	if(strpos($line, "hook1ein_url=") !== false) {
		$result .= 'hook1ein_url=\''.$_POST['hook1ein_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "angesteckthooklp1_url=") !== false) {
		$result .= 'angesteckthooklp1_url=\''.$_POST['angesteckthooklp1_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "hook1aus_url=") !== false) {
		$result .= 'hook1aus_url=\''.$_POST['hook1aus_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "hook2ein_url=") !== false) {
		$result .= 'hook2ein_url=\''.$_POST['hook2ein_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "hook2aus_url=") !== false) {
		$result .= 'hook2aus_url=\''.$_POST['hook2aus_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "hook3ein_url=") !== false) {
		$result .= 'hook3ein_url=\''.$_POST['hook3ein_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "hook3aus_url=") !== false) {
		$result .= 'hook3aus_url=\''.$_POST['hook3aus_url']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "verbraucher1_urlw=") !== false) {
		$result .= 'verbraucher1_urlw=\''.$_POST['verbraucher1_urlw']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "verbraucher1_urlh=") !== false) {
		$result .= 'verbraucher1_urlh=\''.$_POST['verbraucher1_urlh']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "verbraucher2_urlw=") !== false) {
		$result .= 'verbraucher2_urlw=\''.$_POST['verbraucher2_urlw']."'\n";
		$writeit = '1';
	}
	if(strpos($line, "verbraucher2_urlh=") !== false) {
		$result .= 'verbraucher2_urlh=\''.$_POST['verbraucher2_urlh']."'\n";
		$writeit = '1';
	}

	if ( $writeit == '0' ) {
		$result .= $line;
	}
}
file_put_contents('/var/www/html/openWB/openwb.conf', $result);

header("Location: ../index.php");
?>
