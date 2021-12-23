<?php
	if (isset($_POST['email'])) {
		# Our new data
		$data = array(
			'username' => $_POST['username'],
			'email' => $_POST['email']
		);
		# Create a connection
		$url = 'https://web.openwb.de/php/localregistrate.php';
		$ch = curl_init($url);
		# Form data string
		$postString = http_build_query($data)."\n";
		# Setting our options
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		# Get the response
		$response = curl_exec($ch);
		curl_close($ch);
	} else {
		$response = $_POST['username'].','.$_POST['cloudpass'];
	}

	if ( $response == "nomail" ) {
		echo "Keine gültige Email angegeben, Weiterleitung erfolgt in 10 Sekunden...";
		header( "refresh:10;url='../settings/cloudconfig.php" );
	} elseif ( $response == "maildoesnotexist" ) {
		echo "Keine Email angegeben, dies ist eine Pflichtangabe! Weiterleitung erfolgt in 10 Sekunden...";
		header( "refresh:10;url='../settings/cloudconfig.php" );
	} elseif ( $response == "usernamenotvalid" ) {
		echo "Kein gültiger Benutzername, dieser darf nur Buchstaben enthalten, keine -,. Zahlen oder Leerzeichen. Weiterleitung erfolgt in 10 Sekunden...";
		header( "refresh:10;url='../settings/cloudconfig.php" );
	} elseif ( $response == "usernameempty" ) {
		echo "Kein Benutzername angegeben. Weiterleitung erfolgt in 10 Sekunden...";
		header( "refresh:10;url='../settings/cloudconfig.php" );
	} elseif ( $response == "exists" ) {
		echo "Der Benutzername exisitiert bereits. Weiterleitung erfolgt in 10 Sekunden...";
		header( "refresh:10;url='../settings/cloudconfig.php" );
	} else {
		$upass = explode(',', $response);
		$clouduser = $upass[0];
		$cloudpw = $upass[1];
		$result = '';
		$lines = file('/var/www/html/openWB/openwb.conf');
		foreach($lines as $line) {
			$writeit = '0';
			if(strpos($line, "clouduser=") !== false) {
				$result .= 'clouduser='.$clouduser."\n";
				$writeit = '1';
			}
			if(strpos($line, "cloudpw=") !== false) {
				$result .= 'cloudpw='.$cloudpw."\n";
				$writeit = '1';
			}
			if ( $writeit == '0') {
				$result .= $line;
			}
		}
		file_put_contents('/var/www/html/openWB/openwb.conf', $result);

		$url = $_SERVER['HTTP_HOST'].'/openWB/web/settings/savemqtt.php?bridge=cloud';
		$data = array(
			'ConnectionName' => 'cloud',
			'bridgeEnabled' => '1',
			'RemoteAddress' => 'web.openwb.de:1883',
			'RemoteUser' => $clouduser,
			'RemotePass' => $cloudpw,
			'RemotePrefix' => $clouduser.'/',
			'mqttProtocol' => 'mqttv311',
			'tlsProtocol' => 'tlsv1.2',
			'tryPrivate' => '1',
			'exportStatus' => '1',
			'exportGraph' => '1',
			'subscribeConfigs' => '1',
			'username' => $_POST['username']
		);
		$ch = curl_init($url);
		# Form data string
		$postString = http_build_query($data)."\n";
		# Setting our options
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		# Add auth info if required
		if( isset($_SERVER['AUTH_TYPE']) && $_SERVER['AUTH_TYPE'] == 'Basic'){
			curl_setopt($ch, CURLOPT_USERPWD, $_SERVER['PHP_AUTH_USER'] . ":" . $_SERVER['PHP_AUTH_PW']);
		}
		# Get the response
		$response = curl_exec($ch);
		curl_close($ch);
		echo 'Account angelegt, Weiterleitung erfolgt automatisch';
		header( "refresh:5;url='../settings/cloudconfig.php" );
	}
?>
