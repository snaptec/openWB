<?php
require '../config.php';
                
		if ($_GET['jetzt'] == "1") {
                        $config['lademodus'] = '0';
                        file_put_contents('../config.php', '<?php $config = ' . var_export($config, true) . ';');
			file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 0);
                        header("Location: ../index.php");
                }
                if ($_GET['minundpv'] == "1") {
                        $config['lademodus'] = '1';
                        file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 1);
                        file_put_contents('../config.php', '<?php $config = ' . var_export($config, true) . ';');
                        header("Location: ../index.php");
                }
                if ($_GET['pvuberschuss'] == "1") {
                        $config['lademodus'] = '2';
        		 file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 2);
	                file_put_contents('../config.php', '<?php $config = ' . var_export($config, true) . ';');
                        header("Location: ../index.php");
                }
        ?>
