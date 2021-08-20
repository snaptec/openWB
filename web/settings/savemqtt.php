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
$debug = false;

$bridgePrefix = "99-bridge-";
$bridgeOperationDuration = 15;
$randomnr = rand(1, 1000000);

function debugPrint($message){
	global $debug;
	if( $debug ){
		echo $message . "<br/>";
	}
}

function cleanAndExit($message){
	// delete bridges-to-delete file, so that a bridge can't be deleted accidentally
	$fileToClean = "/var/www/html/openWB/ramdisk/99-bridgesToDelete";
	if(is_writable($fileToClean)){
		debugPrint("deleting $fileToClean");
		unlink($fileToClean);
	}
	exit($message);
}

if( $debug ){ ?>
		<h3>Request parameters:</h3>
		<pre>
			<?php print_r( $_REQUEST ); ?>
		</pre>
<?php }

//
// validate bridge name and check if it had already been configured and
// if it has already been configured, whether it has been enabled or disabled
//
$previousBridgeName = $_POST['bridge'];

debugPrint("Previous bridge name: '$previousBridgeName'");

$bridgeToConfig = $_POST['ConnectionName'];

if ($bridgeToConfig == "eindeutiger-verbindungs-bezeichner")
{
	cleanAndExit("Bitte eine eindeutige Bezeichnung f&uuml;r die Verbindung vergeben.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

if(!preg_match('/^[a-zA-Z0-9]+$/', $bridgeToConfig)) {
	cleanAndExit("Der Bezeichener f&uuml;r die Bridge ('" . htmlentities($bridgeToConfig) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9 sind erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

debugPrint("Bridge to configure: '$bridgeToConfig'");

// handle re-naming of bridge by scheduling deletion of the old bridge config
if ($previousBridgeName != $bridgeToConfig) {
	$previousBridgeFileName = "$bridgePrefix$previousBridgeName.conf";
	$globForFile = "/etc/mosquitto/conf.d/${previousBridgeFileName}*";

	debugPrint("Renaming bridge: '$previousBridgeName' -> $bridgeToConfig': Searching for '$globForFile'");

	$files = glob($globForFile);

	$len = strlen($previousBridgeName);
	foreach($files as $currentFile) {
		if (strpos($currentFile, $previousBridgeName) !== false) {
			//// print "Renaming bridge: Adding '$currentFile' to delete list<br/>";
			file_put_contents("/var/www/html/openWB/ramdisk/99-bridgesToDelete", "$currentFile\n", FILE_APPEND);
		}
	}
}

$bridgeFileName = "$bridgePrefix$bridgeToConfig.conf";
debugPrint("Bridge root file name: '$bridgeFileName'");

$globForFile = "/etc/mosquitto/conf.d/${bridgeFileName}*";

debugPrint("Globbing for: '$globForFile'");

$files = glob($globForFile);

//
// if requested, only handle the deletion of the bridge and exit
//
$len = strlen($bridgeFileName);
foreach($files as $currentFile) {
	if (strpos($currentFile, $bridgeFileName) !== false) {
		debugPrint("Deleting: $currentFile");
		file_put_contents("/var/www/html/openWB/ramdisk/99-bridgesToDelete", "$currentFile\n", FILE_APPEND);
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
if (!isset($_POST['bridgeEnabled']) || ($_POST['bridgeEnabled'] == 0)) {
	$fileToUseForNewConfig = $fileToUseForNewConfig . ".no";
}

debugPrint("Bridge file name for new config: '$fileToUseForNewConfig'");

$remoteHost = $_POST['RemoteAddress'];
if ($remoteHost == "entfernter.mqtt.host:8883") {
	cleanAndExit("Bitte die Adresse und den Port des entfernten MQTT-Servers setzen.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}
if(!preg_match('/^([a-zA-Z0-9][a-zA-Z0-9.-]+):([1-9][0-9]*)$/', $remoteHost, $matches)) {
	cleanAndExit("Der Bezeichener f&uuml;r den Namen oder die IP Adresse des entfernten MQTT-Servers ('" . htmlentities($remoteHost) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9 und Punkt sind vor dem Doppelpunkt erlaubt. Nach dem Doppelpunkt sind nur noch Ziffern 0-9 erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

$hostOrAddress = $matches[1];
$port = $matches[2];
if (!isset($hostOrAddress) || empty($hostOrAddress)) {
	cleanAndExit ("Die Address oder der Namen des entfernten MQTT-Servers ('" . htmlentities($hostOrAddress) . "') ist ung&uuml;tig oder nicht vorhanden.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

if (!isset($port) || empty($port)) {
	$port = "8883";
}

debugPrint("HostOrAddress '$hostOrAddress', Port '$port'");

$remoteUser = $_POST['RemoteUser'];
if ($remoteUser == "nutzername-auf-dem-entfernten-host") {
	cleanAndExit("Bitte einen Benutzernamen f&uuml;r den entfernten MQTT-Servers setzen.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}
if(!preg_match('/^([a-zA-Z0-9_\-+.]+)$/', $remoteUser)) {
	cleanAndExit("Der Bezeichener f&uuml;r den Benutzer auf dem entfernten MQTT-Servers ('" . htmlentities($remoteUser) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9, Punkt, Unterstrich, Minus und Plus sind erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

debugPrint("RemoteUser: '$remoteUser'");

$remotePass = $_POST['RemotePass'];
if(!isset($remotePass) || empty($remotePass)) {
	cleanAndExit("Ung&uuml;tiges Pa&szlig;wort: Nicht vorhanden oder leer.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

debugPrint("RemotePass: <em>&gt;vorhanden&lt;</em>");

$remotePrefix = $_POST['RemotePrefix'];
if(!preg_match('/^[a-zA-Z0-9_\-\/]+$/', $remotePrefix)) {
	cleanAndExit("Der Bezeichener f&uuml;r den Topic-Pr&auml;fix auf dem entfernten MQTT-Server ('" . htmlentities($remotePrefix) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9, Unterstrich, Schr&auml;gstrich und Minus sind erlaubt.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

debugPrint("RemotePrefix: $remotePrefix");

$mqttProtocol = $_POST['mqttProtocol'];
if(!preg_match('/^(mqttv31|mqttv311)$/', $mqttProtocol)) {
	cleanAndExit("Interner Fehler: Ung&uuml;tiges MQTT Protokoll '" . htmlentities($mqttProtocol) . "'");
}

debugPrint("MQTT protocol: '$mqttProtocol'");

$tlsProtocol = $_POST['tlsProtocol'];
if(!preg_match('/^(tlsv1.2|tlsv1.3)$/', $tlsProtocol)) {
	cleanAndExit("Interner Fehler: Ung&uuml;tiges TLS Protokoll '" . htmlentities($tlsProtocol) . "'");
}

$tryPrivate = isset($_POST['tryPrivate']) && ($_POST['tryPrivate'] == 1) ? "true" : "false";
$exportStatus = isset($_POST['exportStatus']) && ($_POST['exportStatus'] == 1);
$exportGraph = isset($_POST['exportGraph']) && ($_POST['exportGraph'] == 1);
$subscribeConfigs = isset($_POST['subscribeConfigs']) && ($_POST['subscribeConfigs'] == 1);

if (!$exportStatus && !$exportGraph && !$subscribeConfigs) {
	cleanAndExit("Es macht keinen Sinn eine MQTT-Br&uuml;cke zu konfigurieren welche weder Daten publiziert noch Konfigurationen empf&auml;ngt.<br/>Bitte mindestens eine Checkbox bei 'Zum entfernten Server weiterleiten' oder 'Konfiguration der openWB durch entfernten Server erm&ouml;glichen' aktivieren.<br/>Verwende die &quot;Zur&uuml;ck&quot;-Funktion des Webbrowsers um zur&uuml;ck zum Formular zu kommen.");
}

//
// create the new config file
//
$configFile = fopen($fileToUseForNewConfig, 'w');
if (!$configFile) {
	cleanAndExit("Interner Fehler: Kann die Konfigurationsdatei f&uuml;r die Br&uuml;cke nicht erzeugen.");
}

debugPrint("Openend '$fileToUseForNewConfig' and now writing configuration to it");

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

# Indicate to remote that we're a bridge. Only compatible with remote Mosquitto brokers.
# Only change if you know what you're doing!
try_private $tryPrivate

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

debugPrint("Now closing '$configFile' ('$fileToUseForNewConfig')");

fclose($configFile);

echo "Rekonfiguration des MQTT-Servers wird durchgeführt, bitte nicht vom Strom trennen";
exec("/var/www/html/openWB/runs/checkmqttconf.sh >>/var/www/html/openWB/ramdisk/checkmqttconf.log &");
?>
		<script>
			setTimeout(function() { window.location = "../index.php"; }, 8000);
		</script>
	</body>
</html>
