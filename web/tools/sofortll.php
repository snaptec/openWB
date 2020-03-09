<?php
if(isset($_POST['lademlp1'])) {
	$result = '';
	$lines = file('/var/www/html/openWB/openwb.conf');
	foreach($lines as $line) {
		$writeit = '0';

		if(strpos($line, "lademkwh=") !== false) {
			$result .= 'lademkwh='.$_POST['lademlp1']."\n";
			$writeit = '1';
			}
		if(strpos($line, "lademstat=") !== false) {
			if($_POST['msmoduslp1'] == 1 ) {
				$result .= 'lademstat='."1"."\n";
			}
			if($_POST['msmoduslp1'] == 2 ) {
				$result .= 'lademstat='."0"."\n";
			}
			if($_POST['msmoduslp1'] == 0 ) {
				$result .= 'lademstat='."0"."\n";
			}
			$writeit = '1';
		}
		if(strpos($line, "lademkwhs1=") !== false) {
			$result .= 'lademkwhs1='.$_POST['lademlp2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lademstats1=") !== false) {
			if($_POST['msmoduslp2'] == 1 ) {
				$result .= 'lademstats1='."1"."\n";
			}
			if($_POST['msmoduslp2'] == 2 ) {
				$result .= 'lademstats1='."0"."\n";
			}
			if($_POST['msmoduslp2'] == 0 ) {
				$result .= 'lademstats1='."0"."\n";
			}
			$writeit = '1';
		}
		if(strpos($line, "lademkwhs2=") !== false) {
			$result .= 'lademkwhs2='.$_POST['lademlp3']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sofortsoclp1=") !== false) {
			$result .= 'sofortsoclp1='.$_POST['sofortsoclp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sofortsoclp2=") !== false) {
			$result .= 'sofortsoclp2='.$_POST['sofortsoclp2']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sofortsoclp3=") !== false) {
			$result .= 'sofortsoclp3='.$_POST['sofortsoclp3']."\n";
			$writeit = '1';
		}
		if(strpos($line, "sofortsocstatlp1=") !== false) {
			if($_POST['msmoduslp1'] == 1 ) {
				$result .= 'sofortsocstatlp1='."0"."\n";
			}
			if($_POST['msmoduslp1'] == 2 ) {
				$result .= 'sofortsocstatlp1='."1"."\n";
			}
			if($_POST['msmoduslp1'] == 0 ) {
				$result .= 'sofortsocstatlp1='."0"."\n";
			}
			$writeit = '1';
		}
		if(strpos($line, "sofortsocstatlp2=") !== false) {
			if($_POST['msmoduslp2'] == 1 ) {
				$result .= 'sofortsocstatlp2='."0"."\n";
			}
			if($_POST['msmoduslp2'] == 2 ) {
				$result .= 'sofortsocstatlp2='."1"."\n";
			}
			if($_POST['msmoduslp2'] == 0 ) {
				$result .= 'sofortsocstatlp2='."0"."\n";
			}
			$writeit = '1';
		}
		if(strpos($line, "sofortsocstatlp3=") !== false) {
			$result .= 'sofortsocstatlp3='.$_POST['sofortsocstatlp3']."\n";
			$writeit = '1';
		}
		if(strpos($line, "lademstats2=") !== false) {
			$result .= 'lademstats2='.$_POST['lademlp3check']."\n";
			$writeit = '1';
		} 
		if(strpos($line, "msmoduslp1=") !== false) {
			$result .= 'msmoduslp1='.$_POST['msmoduslp1']."\n";
			$writeit = '1';
		}
		if(strpos($line, "msmoduslp2=") !== false) {
			$result .= 'msmoduslp2='.$_POST['msmoduslp2']."\n";
			$writeit = '1';
		}

		if ($writeit == '0') {
			$result .= $line;
		}
	}
	file_put_contents('/var/www/html/openWB/openwb.conf', $result);
}
header("Location: ../index.php");
?>
