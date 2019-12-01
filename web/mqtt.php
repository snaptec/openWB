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
			<li><a data-toggle="tab" href="./index.php">Zur&uuml;ck</a></li>
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
            $connectionName = "eindeutiger-verbindungs-bezeichner";
            $remoteAddressAndPort = "entfernter.mqtt.host:8883";
            $remotePrefix = NULL;
            $remoteUser = "nutzername-auf-dem-entfernten-host";
            $remotePassword = "";
            $remoteClientId = "client-id-fuer-den-entfernten-host";
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
                if(preg_match('/^\s*topic\s+openWB\/housebattery\/#/', $bridgeLine) === 1) {
                    $exportHousebattery = true;
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
                    <input type="checkbox" name="bridgeEnabled" value="bridgeEnabled" <?php echo $bridgeEnabled ? "checked=\"checked\"" : "" ?>><?php echo $bridgeEnabled ? "": "&nbsp;&nbsp;<em>! Deaktiviert !</em>" ?><b><label>&nbsp;&nbsp;Br&uuml;cke&nbsp;&nbsp;<input type="text" size="35" name="ConnectionName" id="ConnectionName" value="<?php echo $connectionName; ?>" /></label></b><br/>
                    <?php if($debugold >= 1) echo "<small>in Datei '$currentFile'</small>"; ?><br/>
                    <span style="color: red; font-weight: bold; font-size:small;"><u>ACHTUNG</u>: Die Konfiguration einer MQTT-Br&uuml;cke erlaubt allen Nutzern mit Zugang zum entfernten MQTT-Server alle weitergeleiteten Daten dieser openWB einzusehen !<br/>
                    Es wird schwer empfohlen dies nur f&uuml;r nicht-&ouml;ffentliche MQTT-Server unter Verwendung starker Transport-Verschl&uuml;sselung (TLS)  mit personfiziertem Login und strenger Zugriffskontrolle (zumindest f&uuml;r die MQTT-Thema unterhalb von &quot;Entfernter Pr&auml;fix&quot;) zu aktivieren !</span>
                </div>
                <div style="margin-top: 15px;">
                    Addresse und Portnummer des entfernten MQTT-Servers:&nbsp;<input type="text" size="50" name="RemoteAddress" id="RemoteAddress" value="<?php echo $remoteAddressAndPort; ?>" /><br/>
                    <small>Entfernter MQTT-Server und Port-Nummer. Standard Port ist 8883 f&uuml;r eine TLS-gesch&uuml;tzte Verbindung.</small>
                </div>
                <div style="margin-top: 15px;">
                    Benutzer:&nbsp;<input type="text" size="35" name="RemoteUser" id="RemoteUser" value="<?php echo $remoteUser; ?>" /><br/>
                    <small>Benutzername f&uuml;r den Login auf dem entfernten MQTT-Server.</small>
                </div>
                <div style="margin-top: 15px;">
                    Passwort:&nbsp;<input type="password" size="35" name="RemotePass" id="RemotePass" value="<?php echo $remotePassword; ?>" /><br/>
                    <small>Passwort f&uuml;r den Login auf dem entfernten MQTT-Server. Leerzeichen am Anfang und Ende des Passworts werden nicht unterst&uuml;tzt.</small>
                </div>
                <div style="margin-top: 15px;">
                    Entfernter Pr&auml;fix:&nbsp;<input type="text" size="55" name="RemotePrefix" id="RemotePrefix" value="<?php echo $remotePrefix; ?>" /><br/>
                    <small>MQTT-Thema Pr&auml;fix welches dem 'openWB/...' vorangestellt wird.<br/>
                    Beispiel: Wenn in diesem Feld 'pfx' eingetragen wird, werden alle Weiterleitungen und Registrierungen auf der entfernten Seite mit 'pfx/openWB/...' benannt.</small>
                </div>
                <div style="margin-top: 15px;">
                    MQTT Protokoll:<br/>
                    <small>Version des MQTT Protokolls welches zur Kommunikation mit dem entfernten Server verwendet wird.</small>
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
                    TLS Protokoll:<br/>
                    <small>Version des TLS Protokolls welches zur Verschl&uuml;sselung der Kommunikation mit dem entfernten Server verwendet wird.</small>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.3" disabled <?php echo $tlsVersion == "tlsv1.3" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.3<br/><span style="color: darkgreen; font-size:small;">Empfohlen<br/>Aber auf Debian Stretch<br/>nicht unterst&uuml;tzt</span></td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.2" <?php echo $tlsVersion == "tlsv1.2" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.2<br/><span style="color: lightgreen; font-size:small;">Empfohlen</span></td>
                            <!-- td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="tlsv1.1" <?php echo $tlsVersion == "tlsv1.1" ? "checked=\"checked\"" : "" ?>>&nbsp;TLSv1.1<br/><span style="color: darkred; font-size:small;">Can be broken.</span><td/ -->
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="radio" name="tlsProtocol" value="none" <?php echo $tlsVersion == "none" ? "checked=\"checked\"" : "" ?>>&nbsp;Keine Verschl&uuml;sselung<br/><span style="color: red; font-size:small;">Hochgradig unsicher !<br/>&Uuml;bertr&auml;gt Passw&ouml;rter im Klartext!<br/>Nur in gesch&uuml;tzten Umgebungen verwenden!</span></td>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div style="margin-top: 15px;">
                    <b>Zum entfernten Server weiterleiten:</b><br/>
                    <small>Diese Daten werden von der openWB zum entfernten Server weitergeleitet.</small>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="globalData" value="globalData" <?php echo $exportGlobal ? "checked=\"checked\"" : "" ?>>&nbsp;Allgemeine Daten<br/><small>z.B. Hausverbrauch</small></td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="evuData" value="evuData" <?php echo $exportEvu ? "checked=\"checked\"" : "" ?>>&nbsp;EVU (Energieversorger) Daten</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="pvData" value="pvData" <?php echo $exportPv ? "checked=\"checked\"" : "" ?>>&nbsp;PV (Photovoltaik) Daten</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="housebattery" value="housebattery" <?php echo $exportHousebattery ? "checked=\"checked\"" : "" ?>>&nbsp;Daten des Energiespeichers</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="allLps" value="allLps" <?php echo $exportAllLps ? "checked=\"checked\"" : "" ?>>&nbsp;Daten aller Ladepunkte</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="graph" value="graph" <?php echo $exportGraph ? "checked=\"checked\"" : "" ?>>&nbsp;Daten f&uuml;r Diagramme</td>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div style="margin-top: 15px;">
                    <b>Auf dem entfernten Server registrierte Konfigurationsm&ouml;glichkeiten:</b><br/>
                    <small>MQTT-Themen &uuml;ber welche die openWB Einstellungen vom entfernten Server empfangen soll.<br/>
                    <span style="color: red; font-weight: bold; font-size:small;"><u>ACHTUNG</u>: Dies erlaubt jedem Nutzer des entfernten MQTT-Server mit Zugriff auf die entsprechenden Themen diese openWB fern zu steuern !<br/>
                    Es wird schwer empfohlen dies nur f&uuml;r nicht-&ouml;ffentliche MQTT-Server unter Verwendung starker Transport-Verschl&uuml;sselung (TLS)  mit personfiziertem Login und strenger Zugriffskontrolle zu aktivieren !<br/>
                    KEINESFALLS AUF <u>&Ouml;FFENTLICHE ZUG&Auml;NGLICHEN</u> MQTT-SERVERN AKTIVEREN !!!</b></span>
                    <fieldset>
                        <table>
                        <tr>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="subChargeMode" name="SubscribeChargeMode" value="subChargeMode" <?php echo $subscribeChargeMode ? "checked=\"checked\"" : "" ?>>&nbsp;openWB Lademodus</td>
                            <td style="text-align: left; vertical-align: center; padding: 10px;"><input type="checkbox" name="lp1Control" name="lp1Control" value="lp1Control" <?php echo $subscribeLp1 ? "checked=\"checked\"" : "" ?>>&nbsp;Steuerung f&uuml;r Ladepunkt 1<td/>
                        </tr>
                        </table>
                    </fieldset>
                </div>
                <div>
                    <button type="submit" name="action" value="saveBridge">Einstellungen f&uuml;r Br&uuml;cke '<?php echo urlencode($connectionName); ?>' speichern</button>
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
