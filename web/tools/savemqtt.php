<?php
if ($_POST['action'] === 'backNoChange')
{
	header("Location: ../index.php");
	return;
}
?>
<!DOCTYPE html>
<html lang="de">
	<head>
		<title>MQTT Konfiguration</title>
	</head>
	<body>
<?php
$bridgePrefix = "99-bridge-";
$bridgeOperationDuration = 15;
$randomnr = rand(1, 1000000);

//
// validate bridge name and check if it had already been configured and
// if it has already been configured, whether it has been enabled or disabled
//
parse_str($_SERVER['QUERY_STRING'], $queryArray);
$previousBridgeName = $queryArray['bridge'];

//// print "Previous bridge name: '$previousBridgeName'<br/>";

$bridgeToConfig = $_POST['ConnectionName'];

if ($bridgeToConfig == "eindeutiger-verbindungs-bezeichner")
{
	exit("Bitte eine eindeutige Bezeichnung f&uuml;r die Verbindung vergeben.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

if(!preg_match('/^[a-zA-Z0-9]+$/', $bridgeToConfig)) {
	exit("Der Bezeichener f&uuml;r die Bridge ('" . htmlentities($bridgeToConfig) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9 sind erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

//// print "Bridge to configure: '$bridgeToConfig'<br/>";

// handle re-naming of bridge by scheduling deletion of the old bridge config
if ($previousBridgeName != $bridgeToConfig) {
	$previousBridgeFileName = "$bridgePrefix$previousBridgeName.conf";
	$globForFile = "/etc/mosquitto/conf.d/${previousBridgeFileName}*";

	//// print "Renaming bridge: '$previousBridgeName' -> $bridgeToConfig': Searching for '$globForFile'<br/>";

	$files = glob($globForFile);

	$len = strlen($previousBridgeName);
	foreach($files as $currentFile) {
		if (strpos($currentFile, $previousBridgeName) !== false) {
			//// print "Renaming bridge: Adding '$currentFile' to delete list<br/>";
			file_put_contents("/var/www/html/openWB/ramdisk/99-bridgesToDelete", $currentFile, FILE_APPEND);
		}
	}
}

$bridgeFileName = "$bridgePrefix$bridgeToConfig.conf";
//// print "Bridge root file name: '$bridgeFileName'<br/>";

$globForFile = "/etc/mosquitto/conf.d/${bridgeFileName}*";

//// print "Globbing for: '$globForFile'<br/>";

$files = glob($globForFile);

//// print "Config file globbing result:<br/>";
//// var_dump($files);
//// print "<br/>";

//
// if requested, only handle the deletion of the bridge and exit
//
$len = strlen($bridgeFileName);
foreach($files as $currentFile) {
	if (strpos($currentFile, $bridgeFileName) !== false) {
		//// print "Deleting: $currentFile <br/>";
		file_put_contents("/var/www/html/openWB/ramdisk/99-bridgesToDelete", $currentFile, FILE_APPEND);
	}
}

if ($_POST['action'] === 'deleteBridge') {
	echo "Rekonfiguration des MQTT-Servers wird durchgeführt, bitte nicht vom Strom trennen";
	exec("/var/www/html/openWB/runs/checkmqttconf.sh >>/var/www/html/openWB/ramdisk/checkmqttconf.log &");
?>
		<script>
			setTimeout(function() { window.location = "../index.php"; }, 8000);
		</script>
	</body>
</html>
<?php
	return;
}

//
// validate input data and assign to variables
//
$fileToUseForNewConfig = "/var/www/html/openWB/ramdisk/$bridgeFileName";
if (!isset($_POST['bridgeEnabled'])) {
	$fileToUseForNewConfig = $fileToUseForNewConfig . ".no";
}

//// print "Bridge file name for new config: '$fileToUseForNewConfig'<br/>";

$remoteHost = $_POST['RemoteAddress'];
if ($remoteHost == "entfernter.mqtt.host:8883") {
	exit("Bitte die Adresse und den Port des entfernten MQTT-Servers setzen.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}
if(!preg_match('/^([a-zA-Z0-9][a-zA-Z0-9.-]+):{0,1}([0-9]{0,5})$/', $remoteHost, $matches)) {
	exit("Der Bezeichener f&uuml;r den Namen oder die IP Adresse des entfernten MQTT-Servers ('" . htmlentities($remoteHost) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9 und Punkt sind erlaubt vor dem Doppelpunkt erlaubt. Nach dem Doppelpunkt sind nur noch Ziffern 0-9 erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

$hostOrAddress = $matches[1];
$port = $matches[2];
if (!isset($hostOrAddress) || empty($hostOrAddress)) {
	exit ("Die Address oder der Namen des entfernten MQTT-Servers ('" . htmlentities($hostOrAddress) . "') ist ung&uuml;tig oder nicht vorhanden.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

if (!isset($port) || empty($port)) {
	$port = "8883";
}

//// print "HostOrAddress '$hostOrAddress', Port '$port'<br/>";

$remoteUser = $_POST['RemoteUser'];
if ($remoteUser == "nutzername-auf-dem-entfernten-host") {
	exit("Bitte einen Benutzernamen f&uuml;r den entfernten MQTT-Servers setzen.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}
if(!preg_match('/^([a-zA-Z0-9_\-+.]+)$/', $remoteUser)) {
	exit("Der Bezeichener f&uuml;r den Benutzer auf dem entfernten MQTT-Servers ('" . htmlentities($remoteUser) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9, Punkt, Unterstrich, Minus und Plus sind erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

//// print "RemoteUser: '$remoteUser'<br/>";

$remotePass = $_POST['RemotePass'];
if(!isset($remotePass) || empty($remotePass)) {
	exit("Ung&uuml;tiges Pa&szlig;wort: Nicht vorhanden oder leer.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

//// print "RemotePass: <em>&gt;vorhanden&lt;</em><br/>";

$remotePrefix = $_POST['RemotePrefix'];
if(!preg_match('/^[a-zA-Z0-9_\-\/]+$/', $remotePrefix)) {
	exit("Der Bezeichener f&uuml;r den Topic-Pr&auml;fix auf dem entfernten MQTT-Server ('" . htmlentities($remotePrefix) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9, Unterstrich, Schr&auml;gstrich und Minus sind erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

//// print "RemotePrefix: $remotePrefix<br/>";

$mqttProtocol = $_POST['mqttProtocol'];
if(!preg_match('/^(mqttv31|mqttv311)$/', $mqttProtocol)) {
	exit("Interner Fehler: Ung&uuml;tiges MQTT Protokoll '" . htmlentities($mqttProtocol) . "'");
}

//// print "MQTT protocol: '$mqttProtocol'<br/>";

$tlsProtocol = $_POST['tlsProtocol'];
if(!preg_match('/^(tlsv1.2|tlsv1.3)$/', $tlsProtocol)) {
	exit("Interner Fehler: Ung&uuml;tiges TLS Protokoll '" . htmlentities($tlsProtocol) . "'");
}

$exportStatus = isset($_POST['exportStatus']);
$exportGraph = isset($_POST['exportGraph']);
$subscribeConfigs = isset($_POST['subscribeConfigs']);

//// print "Export Status: '$exportStatus'<br/>";
//// print "Export Graph: '$exportGraph'<br/>";
//// print "Subscribe Configs: '$subscribeConfigs'<br/>";

if (!$exportStatus && !$exportGraph && !$subscribeConfigs) {
	exit("Es macht keinen Sinn eine MQTT-Br&uuml;cke zu konfigurieren welche weder Daten publiziert noch Konfigurationen empf&auml;ngt.<br/>Bitte mindestens eine Checkbox bei 'Zum entfernten Server weiterleiten' oder 'Konfiguration der openWB durch entfernten Server erm&ouml;glichen' aktivieren.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

//
// create the new config file
//
$configFile = fopen($fileToUseForNewConfig, 'w');
if (!$configFile) {
	exit("Interner Fehler: Kann die Konfigurationsdatei f&uuml;r die Br&uuml;cke nicht erzeugen.");
}

//// print "Openend '$fileToUseForNewConfig' and now writing configuration to it<br/>";

fwrite($configFile, <<<EOS
# bridge to $remoteHost
#

# Just a name of subsequently configured the bridge.
connection $bridgeToConfig

# The host name or IP address and port number of the remote MQTT server.
address $hostOrAddress:$port


###################################################################
## Below choose what to share (bridge to) the remote MQTT server ##
###################################################################
EOS
);

if ($exportStatus) {
	fwrite($configFile, <<<EOS
# export global data to remote
topic openWB/global/# out 2 "" $remotePrefix

# export global data to remote
topic openWB/system/# out 2 "" $remotePrefix

# export all EVU data to remote
topic openWB/evu/# out 2 "" $remotePrefix

# export all charge point data to remote
topic openWB/lp/# out 2 "" $remotePrefix

# export all charge point data to remote
topic openWB/housebattery/# out 2 "" $remotePrefix

# export all charge point data to remote
topic openWB/pv/# out 2 "" $remotePrefix
EOS
	);
}

if ($exportGraph) {
	fwrite($configFile, <<<EOS

# export global data to remote
topic openWB/config/get/# out 2 "" $remotePrefix
topic openWB/SmartHome/# out 2 "" $remotePrefix


EOS
	);
}

fwrite($configFile, <<<EOS



##################################################################################################
## Below choose what to subscribe on  the remote MQTT server in order to receive setting data   ##
## You may comment everything in order to not allow any MQTT remote configuration of the openWB ##
##################################################################################################

EOS
);

if ($subscribeConfigs) {
	fwrite($configFile, <<<EOS
topic openWB/set/# both 2 "" $remotePrefix
topic openWB/config/set/# both 2 "" $remotePrefix


EOS
	);
}

fwrite($configFile, <<<EOS


##############################
## Remote server settings   ##
##############################

# Client ID that appears in local MQTT server's log data.
# Setting it might simplify debugging.
local_clientid bridgeClient$bridgeToConfig

# User name to for logging in to the remote MQTT server.
remote_username $remoteUser

# Password for logging in to the remote MQTT server.
remote_password $remotePass

# Client ID that appears in remote MQTT server's log data.
# Setting it might simplify debugging.
# Commenting uses a random ID and thus gives more privacy.
remote_clientid openwbBridge$bridgeToConfig-$randomnr

# MQTT protocol to use - ideally leave at latest version (mqttv311).
# Only change if remote doesn't support mqtt protocol version 3.11.
bridge_protocol_version $mqttProtocol

# TLS version to use for transport encryption to the remote MQTT server.
# Use at least tlsv1.2. Comment to disable encryption (NOT RECOMMENDED).
bridge_tls_version $tlsProtocol

# Verify TLS remote host name (false).
# Only change if you know what you're doing!
bridge_insecure false

# Indicate to remote that we're a bridge.
# Only change if you know what you're doing!
try_private true

# How often a "ping" is sent to the remote server to indicate that we're still alive and keep firewalls open.
keepalive_interval 63

# Path to a directory with the certificate for verifying TLS connections.
# The default will work for official certificates (including LetsEncrypt ones).
# Don't change unless you're using self-signed certificates.
bridge_capath /etc/ssl/certs



###################################################################
## don't change below unless you _really_ know what you're doing ##
###################################################################

# Automatically connect to the remote MQTT server.
# There a restart_timeout parameter which defaults to jitters with a base of 5 seconds and a cap of 30 seconds so the
# local side doesn't get overloaded trying to reconnect to a non-available remote.
start_type automatic

notifications false
cleansession false

EOS
);

//// print "Now closing '$configFile' ('$fileToUseForNewConfig')";

fclose($configFile);

echo "Rekonfiguration des MQTT-Servers wird durchgeführt, bitte nicht vom Strom trennen";
exec("/var/www/html/openWB/runs/checkmqttconf.sh >>/var/www/html/openWB/ramdisk/checkmqttconf.log &");
?>
		<script>
			setTimeout(function() { window.location = "../index.php"; }, 8000);
		</script>
	</body>
</html>
