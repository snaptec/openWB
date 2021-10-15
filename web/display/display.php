<?php
include("../values.php");

if ($isssold == 1) {
	if ($ssdisplayold == 1) {
		include './parentwb/index.html';
	} else {
		include './minimal/index.php';
	}
} else {
	if ($simplemodeold == 1) {
		include 'simple/index.php';
	} else {
		// das gewählte Theme einbinden
		switch ($displaythemeold) {
			case 1:
				include './gauges/index.php';
				break;
			case 2:
				include './minimal/index.php';
				break;
			case 3:
				include './gauges/index.php';
				break;
			case 4:
				include './yourcharge/index.php';
				break;
			case 5:
				include './colors/index.html';
				break;
			default:
				include './cards/index.html';
				break;
		}
	}
}
