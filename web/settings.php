<?php
require 'config.php';
echo $config['sofortladen'];
echo $config['minundpv'];
echo $config['pvuberschuss'];
$config['sofortladen'] = '2';
$config['minundpv'] = '2';
$config['pvuberschuss'] = '2';
echo $config['minundpv'];
echo "hello";
file_put_contents('./config.php', '<?php $config = ' . var_export($config, true) . ';');



?>
