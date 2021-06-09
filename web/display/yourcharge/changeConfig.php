

<?php
$fileName = $_SERVER['DOCUMENT_ROOT'] . '/openWB/openwb.conf';
$file = file_get_contents($fileName);

function changeConfig($requestKey, $key, $file)
{
	if (array_key_exists($requestKey, $_REQUEST)) {
		$value = $_REQUEST[$requestKey];
		if ($value == "") {
			exit("0");
		}
		return preg_replace('/(' . $key . '=)(.+)/', '${1}' . $value, $file);
	}
	return $file;
}

$file = changeConfig("pin", "displaypincode", $file);
$file = changeConfig("displayTimeout", "displaysleep", $file);

file_put_contents($fileName, $file);
echo "1";
