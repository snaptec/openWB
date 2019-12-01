<!DOCTYPE html>
<html lang="en">

<head>
	<script src="js/jquery-1.11.1.min.js"></script>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>OpenWB</title>
	<meta name="description" content="Control your charge" />
	<meta name="keywords" content="html template, css, free, one page, gym, fitness, web design" />
	<meta name="author" content="Kevin Wieland" />
	<!-- Favicons (created with http://realfavicongenerator.net/)-->
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="icon" type="image/png" href="img/favicons/favicon-32x32.png" sizes="32x32">
	<link rel="icon" type="image/png" href="img/favicons/favicon-16x16.png" sizes="16x16">
	<link rel="manifest" href="manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<meta name="msapplication-TileColor" content="#00a8ff">
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize.css">
	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<!-- Owl -->
	<link rel="stylesheet" type="text/css" href="css/owl.css">
	<!-- Animate.css -->
	<link rel="stylesheet" type="text/css" href="css/animate.css">
	<!-- Font Awesome, all styles -->
	  <link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">
	<!-- Elegant Icons -->
	<link rel="stylesheet" type="text/css" href="fonts/eleganticons/et-icons.css">
	<!-- Main style -->
	<link rel="stylesheet" type="text/css" href="css/cardio.css">
</head>
<body>

<?php
$lines = file('/var/www/html/openWB/openwb.conf');
foreach($lines as $line) {
	if(strpos($line, "debug=") !== false) {
		list(, $debugold) = explode("=", $line);
	}

    if(strpos($line, "settingspw=") !== false) {
		list(, $settingspwold) = explode("=", $line, 2);
	}
	if(strpos($line, "settingspwakt=") !== false) {
		list(, $settingspwaktold) = explode("=", $line);
	}
}

$settingspwsold = str_replace( "'", "", $settingspwold);
?>

<div class="container">
	<div class="row"><br>
		<ul class="nav nav-tabs">
			<li><a data-toggle="tab" href="./index.php">Zurück</a></li>
			<li><a href="./settings.php">Einstellungen</a></li>
  			<li><a href="./pvconfig.php">PV Ladeeinstellungen</a></li>
			<li><a href="./smarthome.php">Smart Home</a></li>
			<li><a href="./modulconfig.php">Modulkonfiguration</a></li>
			<li><a href="./setTheme.php">Theme</a></li>
            <li class="active"><a href="./mqtt.php">MQTT</a></li>
			<li><a href="./misc.php">Misc</a></li>
		</ul><br><br>
	</div>

    <?php
        $files = glob('/etc/mosquitto/conf.d/*-bridge-*.conf*');
        array_push($files, "");
        $firstLoopDone = false;
        foreach($files as $currentFile)
        {
            $currentBridge = preg_replace('/^99-bridge-(.+)\.conf/', '${1}', $currentFile);

            $bridgeLines = file($currentFile);
            $connectionName = "unique-connection-name";
            $remoteAddressAndPort = "your.remote.mqtt.host:8883";
            $remotePrefix = NULL;
            $remoteUser = "remote-mqtt-host-user-name";
            $remotePassword = "";
            $remoteClientId = "unique-mqtt-client-id-used-with-remote";
            $mqttProtocol = "mqttv31";
            $exportGlobal = false;
            $exportEvu = false;
            $exportPv = false;
            $exportAllLps = false;
            $subscribeChargeMode = false;
            $exportGraph = false;
            $tlsVersion = "tlsv1.2";
            $bridgeEnabled = preg_match('/.*\.conf$/', $currentFile) === 1;
            foreach($bridgeLines as $bridgeLine) {
                //echo "line '$bridgeLine'<br/>";
                if(is_null($remotePrefix) && preg_match('/^\s*topic\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+([^\s]+?)\s+/', $bridgeLine, $matches) === 1) {
                    // echo "Matches: " . var_dump($matches);
                    $remotePrefix = trim($matches[5]);
                }
                else if(preg_match('/^\s*connection\s+(.+)/', $bridgeLine, $matches) === 1) {
                    $connectionName = trim($matches[1]);
                }
                else if(preg_match('/^\s*address\s+(.+)/', $bridgeLine, $matches) === 1) {
                    $remoteAddressAndPort = trim($matches[1]);
                }
                else if(preg_match('/^\s*remote_username\s+(.+)/', $bridgeLine, $matches) === 1) {
                    $remoteUser = trim($matches[1]);
                }
                else if(preg_match('/^\s*remote_password\s+(.+)/', $bridgeLine, $matches) === 1) {
                    $remotePassword = preg_replace('/./', '*', trim($matches[1]));
                }
                else if(preg_match('/^\s*bridge_protocol_version\s+(.+)/', $bridgeLine, $matches) === 1) {
                    $mqttProtocol = trim($matches[1]);
                }
                else if(preg_match('/^\s*bridge_tls_version\s+(.+)/', $bridgeLine, $matches) === 1) {
                    $tlsVersion = trim($matches[1]);
                }
                
                if(preg_match('/^\s*topic\s+openWB\/global\/#/', $bridgeLine) === 1) {
                    $exportGlobal = true;
                }
                if(preg_match('/^\s*topic\s+openWB\/evu\/#/', $bridgeLine) === 1) {
                    $exportEvu = true;
                }
                if(preg_match('/^\s*topic\s+openWB\/pv\/#/', $bridgeLine) === 1) {
                    $exportPv = true;
                }
                if(preg_match('/^\s*topic\s+openWB\/graph\/#/', $bridgeLine) === 1) {
                    $exportGraph = true;
                }
                if(preg_match('/^\s*topic\s+openWB\/lp\/#/', $bridgeLine) === 1) {
                    $exportAllLps = true;
                }
                if(preg_match('/^\s*topic\s+openWB\/set\/Lademodus/', $bridgeLine) === 1) {
                    $subscribeChargeMode = true;
                }
                if(preg_match('/^\s*topic\s+openWB\/set\/lp1/', $bridgeLine) === 1) {
                    $subscribeLp1 = true;
                }
            }

            if ($firstLoopDone) echo "<hr>";
    ?>
            <form action="./tools/savemqtt.php?bridge=<?php echo urlencode($connectionName); ?>" method="POST">
                <div class="row">
                    <input type="checkbox" name="bridgeEnabled" value="bridgeEnabled" <?php echo $bridgeEnabled ? "checked=\"checked\"" : "" ?>><?php echo $bridgeEnabled ? "": "&nbsp;&nbsp;<em>! Disabled !</em>" ?><b><label>&nbsp;&nbsp;Bridge&nbsp;&nbsp;<input type="text" size="35" name="ConnectionName" id="ConnectionName" value="<?php echo $connectionName; ?>" /></label></b><br/>
                    <?php if($debugold >= 1) echo "<small>in file '$currentFile'</small>"; ?><br/>
                    <span style="color: red; font-weight: bold; font-size:small;"><u>ATTENTION</u>: Configuring an MQTT might allow all users with access to the remote MQTT server to see your openWB data !<br/>
                    It's highly recommended to enable only for private MQTT servers with strong transport encryption, personal login and strict access control, at least for topics starting with the "Remote Prefix" configured below !</span>
                </div>
                <div style="margin-top: 15px;">
                    Remote Address and Port:&nbsp;<input type="text" size="50" name="RemoteAddress" id="RemoteAddress" value="<?php echo $remoteAddressAndPort; ?>" /><br/>
                    <small>Remote MQTT server address and port number. Default port is 8883 for TLS protected connections.</small>
                </div>
                <div style="margin-top: 15px;">
                    Remote User:&nbsp;<input type="text" size="35" name="RemoteUser" id="RemoteUser" value="<?php echo $remoteUser; ?>" /><br/>
                    <small>User name to log in on the remote MQTT server.</small>
                </div>
                <div style="margin-top: 15px;">
                    Remote Password:&nbsp;<input type="password" size="35" name="RemotePass" id="RemotePass" value="<?php echo $remotePassword; ?>" /><br/>
                    <small>Password to log in on the remote MQTT server. White spaces at beginning or end of the password are NOT supported.</small>
                </div>
                <div style="margin-top: 15px;">
                    Remote Prefix:&nbsp;<input type="text" size="55" name="RemotePrefix" id="RemotePrefix" value="<?php echo $remotePrefix; ?>" /><br/>
                    <small>The topic prefix to prepend to the 'openWB/...' topics.<br/>
                    Example: If this field is 'pfx' then the topic publish and subscribed to remote will be 'pfx/openWB/...' </small>
                </div>
                <div style="margin-top: 15px;">
                    MQTT Protocol:<br/>
                    <small>The MQTT protocol version to use when talking to the remote MQTT server.</small>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="mqttProtocol" value="mqttv31" <?php echo $mqttProtocol == "mqttv31" ? "checked=\"checked\"" : "" ?>>&nbsp;v3.1</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="mqttProtocol" value="mqttv311" <?php echo $mqttProtocol == "mqttv311" ? "checked=\"checked\"" : "" ?>>&nbsp;v3.1.1<td/>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div style="margin-top: 15px;">
                    TLS Protocol:<br/>
                    <small>The TLS protocol version to use for encrypting the traffic to the remote MQTT server.</small>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.3" disabled <?php echo $tlsVersion == "tlsv1.3" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.3<br/><span style="color: darkgreen; font-size:small;">Recommended<br/>But not supported on<br/>Debian Stretch</span></td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.2" <?php echo $tlsVersion == "tlsv1.2" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.2<br/><span style="color: lightgreen; font-size:small;">Recommended</span></td>
                            <!-- td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.1" <?php echo $tlsVersion == "tlsv1.1" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.1<br/><span style="color: darkred; font-size:small;">Can be broken.</span><td/ -->
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="none" <?php echo $tlsVersion == "none" ? "checked=\"checked\"" : "" ?>>&nbsp;No encryption<br/><span style="color: red; font-size:small;">Highly unsafe !<br/>Transmits plain-text passwords.<br/>Use only in protected environments!</span></td>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div style="margin-top: 15px;">
                    <b>Publish to remote:</b><br/>
                    <small>The data that shall be sent to the remote MQTT server.</small>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="globalData" value="globalData" <?php echo $exportGlobal ? "checked=\"checked\"" : "" ?>>&nbsp;Global Data</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="evuData" value="evuData" <?php echo $exportEvu ? "checked=\"checked\"" : "" ?>>&nbsp;EP Data<td/>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="pvData" value="pvData" <?php echo $exportPv ? "checked=\"checked\"" : "" ?>>&nbsp;PV Data</td>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="allLps" value="allLps" <?php echo $exportAllLps ? "checked=\"checked\"" : "" ?>>&nbsp;All Charging Points</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="graph" value="graph" <?php echo $exportGraph ? "checked=\"checked\"" : "" ?>>&nbsp;Graphing Data</td>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div style="margin-top: 15px;">
                    <b>Subscribe on remote:</b><br/>
                    <small>The data that we subscribe to on the remote MQTT server.<br/>
                    <span style="color: red; font-weight: bold; font-size:small;"><u>ATTENTION</u>: This will allow all users with write access to the remote MQTT server's topics to remote-control this openWB !<br/>
                    It's highly recommended to enable only for private MQTT servers with strong transport encryption, personal login and strict access control !<br/>
                    DO NOT ENABLE ANY OF THESE FOR <u>PUBLIC</u> MQTT SERVERS !!!</b></span>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="subChargeMode" name="SubscribeChargeMode" value="subChargeMode" <?php echo $subscribeChargeMode ? "checked=\"checked\"" : "" ?>>&nbsp;Charge Mode</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="lp1Control" name="lp1Control" value="lp1Control" <?php echo $subscribeLp1 ? "checked=\"checked\"" : "" ?>>&nbsp;Charge Point 1 Control<td/>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div>
                    <button type="submit" name="action" value="saveBridge">Save bridge '<?php echo urlencode($connectionName); ?>'</button>
                </div>
            </form>
    <?php

            $firstLoopDone = true;
        }
    ?>
</div>

<div class="row">
<div class="text-center">
Open Source made with love!<br>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="2K8C4Y2JTGH7U">
<input type="image" src="./img/btn_donate_SM.gif" border="0" name="submit" alt="Jetzt einfach, schnell und sicher online bezahlen – mit PayPal.">
<img alt="" border="0" src="./img/pixel.gif" width="1" height="1">
</form>
</div></div>
</div>
<script>
	var settingspwaktold = <?php echo $settingspwaktold ?>;

	var settingspwold = <?php echo $settingspwold ?>;
if ( settingspwaktold == 1 ) {
passWord();
}
function passWord() {
var testV = 1;
var pass1 = prompt('Einstellungen geschützt, bitte Password eingeben:','');

while (testV < 3) {
	if (!pass1) 
		history.go(-1);
	if (pass1 == settingspwold) {
		break;
	} 
	testV+=1;
	var pass1 = prompt('Passwort falsch','Password');
}
if (pass1!="password" & testV == 3) 
	history.go(-1);
return " ";
} 
</script>
</body></html>
