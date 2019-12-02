<!DOCTYPE html>
<html lang="en">

<head>
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

parse_str($_SERVER['QUERY_STRING'], $queryArray);
$previousBridgeName = $queryArray['bridge'];

print "Previous bridge name: '$previousBridgeName'<br/>";

$bridgeToConfig = $_POST['ConnectionName'];

if(!preg_match('/^[a-zA-Z0-9_]+$/', $bridgeToConfig)) {
    exit("Der Bezeichener f&uuml;r die Bridge ('" . htmlentities($bridgeToConfig) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9 und Unterstrich sind erlaubt");
}

print "Bridge to configure: '$bridgeToConfig'<br/>";

$bridgeFileName = "99-bridge-$bridgeToConfig.conf";
print "Bridge root file name: '$bridgeFileName'<br/>";

$globForFile = "/etc/mosquitto/conf.d/${bridgeFileName}*";

print "Globbing for: '$globForFile'<br/>";

$files = glob($globForFile);

print "Config file globbing result:<br/>";
var_dump($files);
print "<br/>";

$files = glob($globForFile);

// if requested, handle the deletion of the bridge and exit
if ($_POST['action'] === 'deleteBridge')
{
	$len = strlen($bridgeFileName); 
	foreach($files as $currentFile)
	{
		if (strpos($currentFile, $bridgeFileName) !== false)
		{
			print "Would now delete the file '$currentFile'";
		}
	}

	return;
}

$fileToUseForNewConfig = $bridgeFileName;
if (!isset($_POST['bridgeEnabled']))
{
	$fileToUseForNewConfig = $bridgeFileName . ".no";
}

print "Bridge file name for new config: '$fileToUseForNewConfig'<br/>";

$remoteHost = $_POST['RemoteAddress'];
if(!preg_match('/^([a-zA-Z0-9][a-zA-Z0-9.-]+):{0,1}([0-9]{0,5})$/', $remoteHost, $matches)) {
    exit("Der Bezeichener f&uuml;r den Namen oder die IP Adresse des entfernten MQTT-Servers ('" . htmlentities($remoteHost) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9 und Punkt sind erlaubt vor dem Doppelpunkt erlaubt. Nach dem Doppelpunkt sind nur noch Ziffern 0-9 erlaubt.");
}

$hostOrAddress = $matches[1];
$port = $matches[2];
if (!isset($hostOrAddress) || empty($hostOrAddress))
{
	exit ("Die Address oder der Namen des entfernten MQTT-Servers ('" . htmlentities($hostOrAddress) . "') ist ung&uuml;tig oder nicht vorhanden");
}

if (!isset($port) || empty($port))
{
	$port = "8883";
}

print "Matches:<br/>";
var_dump($matches);
print "<br/>";
print "HostOrAddress '$hostOrAddress', Port '$port'<br/>";

$remoteUser = $_POST['RemoteUser'];
if(!preg_match('/^([a-zA-Z0-9_\-+.]+)$/', $remoteUser)) {
    exit("Der Bezeichener f&uuml;r den Benutzer auf dem entfernten MQTT-Servers ('" . htmlentities($remoteUser) . "') enth&auml;t ung&uuml;tige Zeichen. Nur a-z, A-Z, 0-9, Punkt, Unterstrich, Minus und Plus sind erlaubt.");
}

print "RemoteUser: '$remoteUser'<br/>";

$mqttProtocol = $_POST['mqttProtocol'];
if(!preg_match('/^(mqttv31|mqttv311)$/', $mqttProtocol)) {
    exit("Interner Fehler: Ung&uuml;tiges MQTT Protokoll '" . htmlentities($mqttProtocol) . "'");
}

print "MQTT protocl: '$mqttProtocol'<br/>";



// header("Location: ../index.php");
?>

</body>