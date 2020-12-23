<?php
	switch ( $wizzarddoneold ) {
		case 0: // start of wizzard
			echo "<!-- wizzard -- start -->";
			include($_SERVER['DOCUMENT_ROOT'] . '/openWB/web/tools/wizzardstart.html');
			break;
		case 1: // EVU
			echo "<!-- wizzard -- step 1 -->";
			include($_SERVER['DOCUMENT_ROOT'] . '/openWB/web/settings/modulconfigevu.php');
			break;
		case 2: // PV
			echo "<!-- wizzard -- step 2 -->";
			include($_SERVER['DOCUMENT_ROOT'] . '/openWB/web/settings/modulconfigpv.php');
			break;
		case 3: // BAT
			echo "<!-- wizzard -- step 3 -->";
			include($_SERVER['DOCUMENT_ROOT'] . '/openWB/web/settings/modulconfigbat.php');
			break;
		default: // end of wizzard
			echo "<!-- wizzard -- end -->";
			include($_SERVER['DOCUMENT_ROOT'] . '/openWB/web/tools/wizzardend.html');
	}
?>
