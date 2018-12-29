<?php

if (isset($_GET['jetzt'])) {
		if ($_GET['jetzt'] == "1") {
                        $config['lademodus'] = '0';
			file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 0);
                        header("Location: ../index.php");
		}
}
		if (isset($_GET['minundpv'])) {

                if ($_GET['minundpv'] == "1") {
                        $config['lademodus'] = '1';
                        file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 1);
                        header("Location: ../index.php");
		}
}
		if (isset($_GET['pvuberschuss'])) {

                if ($_GET['pvuberschuss'] == "1") {
                        $config['lademodus'] = '2';
        		 file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 2);
                        header("Location: ../index.php");
		}
}
if (isset($_GET['stop'])) {

		if ($_GET['stop'] == "1") {
                        $config['lademodus'] = '3';
        		 file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 3);
                        header("Location: ../index.php");
                }
}
if (isset($_GET['semistop'])) {

		if ($_GET['semistop'] == "1") {
                        $config['lademodus'] = '4';
        		 file_put_contents('/var/www/html/openWB/ramdisk/lademodus', 4);
                        header("Location: ../index.php");
                }
}
        ?>
