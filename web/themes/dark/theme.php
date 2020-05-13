<!DOCTYPE html>
<html lang="de">

<head>
	<!-- dark19_01 theme for openWB -->
	<!-- 2020 Michael Ortenstein -->

	<title>openWB</title>
	<?php include ("values.php");?>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="openWB">
	<meta name="apple-mobile-web-app-status-bar-style" content="default">
	<link rel="apple-touch-startup-image" href="/openWB/web/img/favicons/splash1125x2436w.png"  />
	<link rel="apple-touch-startup-image" media="(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)" href="img/favicons/splash1125x2436w.png">
	<meta name="apple-mobile-web-app-title" content="openWB">

	<meta name="description" content="openWB">
	<meta name="keywords" content="openWB">
	<meta name="author" content="Michael Ortenstein">
	<link rel="apple-touch-icon" sizes="72x72" href="img/favicons/apple-icon-72x72.png">
	<link rel="apple-touch-icon" sizes="76x76" href="img/favicons/apple-icon-76x76.png">
	<link rel="apple-touch-icon" sizes="114x114" href="img/favicons/apple-icon-114x114.png">
	<link rel="apple-touch-icon" sizes="120x120" href="img/favicons/apple-icon-120x120.png">
	<link rel="apple-touch-icon" sizes="144x144" href="img/favicons/apple-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="152x152" href="img/favicons/apple-icon-152x152.png">
	<link rel="apple-touch-icon" sizes="180x180" href="img/favicons/apple-icon-180x180.png">
	<link rel="icon" type="image/png" sizes="192x192"  href="img/favicons/android-icon-192x192.png">
	<link rel="icon" type="image/png" sizes="32x32" href="img/favicons/favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="96x96" href="img/favicons/favicon-96x96.png">
	<link rel="icon" type="image/png" sizes="16x16" href="img/favicons/favicon-16x16.png">
	<meta name="msapplication-TileColor" content="#ffffff">
	<meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="57x57" href="img/favicons/apple-touch-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="img/favicons/apple-touch-icon-60x60.png">
	<link rel="manifest" href="manifest.json">
	<link rel="shortcut icon" href="img/favicons/favicon.ico">
	<!-- <link rel="apple-touch-startup-image" href="img/loader.gif"> -->
	<meta name="msapplication-config" content="img/favicons/browserconfig.xml">
	<meta name="theme-color" content="#ffffff">

	<!-- Bootstrap -->
	<link rel="stylesheet" type="text/css" href="css/bootstrap-4.4.1/bootstrap.min.css">
	<!-- Normalize -->
	<link rel="stylesheet" type="text/css" href="css/normalize-8.0.1.css">
	<!-- Font Awesome, all styles -->
  	<link href="fonts/font-awesome-5.8.2/css/all.css" rel="stylesheet">

    <!-- include special Theme style -->
	<link rel="stylesheet" type="text/css" href="themes/<?php echo $_COOKIE['openWBTheme'];?>/style.css?ver=20200405-b">

	<!-- important scripts to be loaded -->
	<script src="js/jquery-3.4.1.min.js"></script>
	<script src="js/bootstrap-4.4.1/bootstrap.bundle.min.js"></script>
</head>

<body>
	<?php include $_SERVER['DOCUMENT_ROOT'].'/openWB/web/themes/standard/navbar.php'; ?>
	<!-- Preloader with Progress Bar -->
	<div class="loader bg-white">
		<div class="loader-container regularTextSize">
		  	<div class="row text-black">
			  	<div class="mx-auto d-block justify-content-center">
					<img src="img/favicons/preloader-image.png" style="max-width: 300px" alt="openWB">
			  	</div>
			</div>
			<div class="row text-grey justify-content-center mt-2">
				<div class="col-10 col-sm-6">
					Bitte warten, während die Seite aufgebaut wird.
				</div>
			</div>
			<div class="row justify-content-center mt-2">
				<div class="col-10 col-sm-6">
					<div class="progress active">
						<div class="progress-bar progress-bar-success progress-bar-striped progress-bar-animated" id="preloaderbar" role="progressbar">
						</div>
					</div>
				</div>
  			</div>
		</div>
	</div>

	<!-- Landing Page -->
	<div class="container">

		<div class="row py-1 verySmallTextSize text-black bg-darkgrey">
			<div id="date" class="col text-left">
				&nbsp;
			</div>
			<div class="col-5 text-center">
				<button type="button" class="btn btn-sm btn-secondary cursor-pointer regularTextSize" id="chargeModeSelectBtn">
					<span id="chargeModeSelectBtnText">Lademodus</span>
					<span id="priorityEvBattery">
						<span class="fas fa-car" id="priorityEvBatteryIcon">&nbsp;</span>
					</span>
				</button>
			</div>
			<div id="time" class="col text-right">
				&nbsp;
			</div>
		</div>

		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="col-sm bg-lightgreen">
				PV: <span id="pvleistung">lade Daten</span><span id="pvdailyyield"></span>
			</div>
			<div id="evudiv" class="col-sm bg-rose">
				EVU: <span id="bezug">lade Daten</span>
			</div>
		</div>

		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="col-sm bg-apricot">
				Hausverbrauch: <span id="hausverbrauch">lade Daten</span>
			</div>
			<div class="col-sm bg-lightgrey">
				Ladeleistung: <span id="powerAllLp">lade Daten</span>
			</div>
		</div>
		<div id="speicher" class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="col-sm bg-orange">
				Speicher: <span id="speicherleistung">lade Daten</span><span id="speichersoc"></span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="hide col-sm bg-lightblue SmartHome" dev="1">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
			<div class="hide col-sm bg-lightblue SmartHome" dev="2">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="hide col-sm bg-lightblue SmartHome" dev="3">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
			<div class="hide col-sm bg-lightblue SmartHome" dev="4">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="hide col-sm bg-lightblue SmartHome" dev="5">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
			<div class="hide col-sm bg-lightblue SmartHome" dev="6">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="hide col-sm bg-lightblue SmartHome" dev="7">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
			<div class="hide col-sm bg-lightblue SmartHome" dev="8">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="hide col-sm bg-lightblue SmartHome" dev="9">
				 <span class="nameDevice">Device Name</span> <span class="actualPowerDevice">lade Daten</span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">
			<div class="hide bg-lightblue col-sm SmartHomeTemp" dev="1">
				<span class="actualTemp0Device"></span>
			</div>
			<div class="hide bg-lightblue col-sm SmartHomeTemp" dev="1">
				<span class="actualTemp1Device"></span>
			</div>
			<div class="hide bg-lightblue col-sm SmartHomeTemp" dev="1">
				<span class="actualTemp2Device"></span>
			</div>
		</div>
		<div class="row justify-content-center regularTextSize font-weight-bold text-center text-black">

			<div class="hide bg-lightblue col-sm SmartHomeTemp" dev="2">
				<span class="actualTemp0Device"></span>
			</div>

			<div class="hide bg-lightblue col-sm SmartHomeTemp" dev="2">
				<span class="actualTemp1Device"></span>
			</div>

			<div class="hide bg-lightblue col-sm SmartHomeTemp" dev="2">
				<span class="actualTemp2Device"></span>
			</div>
		</div>


		<div id="webhooks" class="row justify-content-center regularTextSize font-weight-bold text-center text-black bg-darkgrey">
			<div id="hook1" class="col-3 m-1 bg-danger hide">
				ext. Gerät 1
			</div>
			<div id="hook2" class="col-3 m-1 bg-danger hide">
				ext. Gerät 2
			</div>
			<div id="hook3" class="col-3 m-1 bg-danger hide">
				ext. Gerät 2
			</div>
		</div>

		<!-- interactive chart.js -->
		<!-- will be refreshed using MQTT (in live.js)-->
		<div class="row justify-content-center my-2" id="thegraph">
			<div class="col-sm-12 text-center smallTextSize" style="height: 350px;">
				<div id="waitforgraphloadingdiv">
					Graph lädt, bitte warten...
				</div>
				<canvas id="canvas"></canvas>
			</div>
			<div id="graphoptiondiv" class="hide">
				<br><br>
			</div>
		</div>

		<div class="row text-center bg-darkgrey">
			<div class="col">
				<span id="lastregelungaktiv" class="regularTextSize text-red animate-alertPulsation"></span>
			</div>
		</div>

		<!-- chargepoint info header -->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-darkgrey text-grey font-weight-bold">
			<div class="col-3 px-0">
				Ladepunkt <span id="awattarEnabledIcon" class="fa fa-chart-line hide"></span>
			</div>
			<div class="col-3 px-0">
				Ladeparameter
			</div>
			<div class="col-4 px-0">
				geladen
			</div>
			<div class="col-2 px-0">
				SoC
			</div>
		</div>

		<!-- chargepoint info data lp1-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="1">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp2-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="2">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp3-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="3">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp4-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="4">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp5-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="5">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp6-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="6">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp7-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="7">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<!-- chargepoint info data lp8-->
		<div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey" data-lp="8">
			<div class="col-3 px-0">
				<span class="fas fa-xs hide autolockConfiguredLp"></span>
				<span class="cursor-pointer font-weight-bold lpDisabledStyle enableLp nameLp">LP Name</span>
				<span class="fa fa-xs fa-plug text-lightgrey hide plugstatLp"></span>
			    <span class="fa fa-xs fa-flag-checkered hide targetChargingLp"></span>
			    <span class="fa fa-xs fa-moon hide nightChargingLp"></span>
			</div>
            <div class="col-3 px-0">
                <span class="actualPowerLp">lade Daten</span><span class="phasesInUseLp"></span><span class="targetCurrentLp"></span>
            </div>
            <div class="col-4 px-0">
                <span class="energyChargedLp">lade Daten</span><span class="kmChargedLp" consumption="0"></span>
            </div>
            <div class="col-2 px-0 socNotConfiguredLp text-center">
              --
            </div>
            <div class="col-2 px-0 hide socConfiguredLp text-center">
                <span class="socLp"></span>
            </div>
        </div>

		<hr color="white">
                <!-- SmartHome info header -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-darkgrey text-grey font-weight-bold shInfoHeader">
                        <div class="col-3 px-0">
                                Gerät
                        </div>
                        <div class="col-3 px-0">
                                Verbrauch
                        </div>
                        <div class="col-3 px-0">
                                Modus
			</div>
	                <div class="col-3 px-0">
                                Laufzeit
                        </div>

		</div>
		<!-- SmartHome Device 1 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="1">
                        <div class="col-3 px-0">
                                <span class="font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>
		</div>
		<!-- SmartHome Device 2 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="2">
                        <div class="col-3 px-0">
                                <span class="font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="3">
                        <div class="col-3 px-0">
                                <span class="font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="4">
                        <div class="col-3 px-0">
                                <span class="cursor-pointer font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="5">
                        <div class="col-3 px-0">
                                <span class="cursor-pointer font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="6">
                        <div class="col-3 px-0">
                                <span class="cursor-pointer font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="7">
                        <div class="col-3 px-0">
                                <span class="cursor-pointer font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="8">
                        <div class="col-3 px-0">
                                <span class="cursor-pointer font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>
		<!-- SmartHome Device 3 data -->
                <div class="row no-gutter py-1 py-md-0 smallTextSize text-center bg-lightgrey text-grey SmartHome" dev="9">
                        <div class="col-3 px-0">
                                <span class="cursor-pointer font-weight-bold lpEnabledStyle enableDevice nameDevice">SmartHomeDevice</span>
                        </div>
                	<div class="col-3 px-0">
                	        <span class="actualPowerDevice">lade Daten</span>
                	</div>
                	<div class="col-3 px-0">
				<span class="cursor-pointer actualModeDevice changeSHMode">lade Daten</span>
			</div>
                        <div class="col-3 px-0">
                                <span class="actualRunningTimeDevice">lade Daten</span>
                        </div>

		</div>

		<!-- depending on charge mode show options -->
	    <form id="sofortladenEinstellungen" class="hide" name="sofortll" action="./tools/sofortll.php" method="POST">

			<div class="row justify-content-center">
				<h3 class="font-weight-bold text-center text-lightgrey">Sofortladen Stromstärke <span class="nameLp"></span></h3>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="1">
				<label for="lp/1/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/1/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/1/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="2">
				<label for="lp/2/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/2/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/2/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="3">
				<label for="lp/3/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/3/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/3/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="4">
				<label for="lp/4/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/4/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/4/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="5">
				<label for="lp/5/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/5/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/5/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="6">
				<label for="lp/6/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/6/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/6/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="7">
				<label for="lp/7/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/7/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/7/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div class="form-row form-group mb-1 vaRow regularTextSize" data-lp="8">
				<label for="lp/8/current" class="col-3 col-form-label text-right"><span class="nameLp"></span>:</label>
				<div class="col">
					<input type="range" class="form-control-range rangeInput" id="lp/8/current" min="6" max="32" step="1" value="6" data-initialized="0" data-topicprefix="openWB/config/get/sofort/">
				</div>
				<label for="lp/8/current" class="col-3 col-form-label valueLabel" suffix="A"></label>
			</div>

			<div id="awattardiv" class="hide"enabled="<?php echo $settingsArray["awattaraktiv"] ?>">
				<hr color="white">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Awattar</h3>
				</div>
				<div class="row justify-content-center">
					<div class="col-sm-12 text-center" style="height: 150px;">
						<canvas id="awattarcanvas"></canvas>
					</div>
				</div>
				<div class="row vaRow justify-content-center" id="sliderawattardiv">
					<div class="col-6 col-md-4">
						<input type="range" min="-8" max="12" step="0.10" name="awattar1s" id="awattar1s" class="custom-range">
					</div>
					<div class="col-sm-5 col-md-6 regularTextSize text-center">
						<label for="awattar1">Maximaler Preis: <span id="awattar1l"></span> Cent/kWh</label>
					</div>
					<script>
						var aslider1 = document.getElementById("awattar1s");
						var aoutput1 = document.getElementById("awattar1l");
						aoutput1.innerHTML = aslider1.value;
						aslider1.oninput = function() {
							aoutput1.innerHTML = this.value;
							AwattarMaxPriceClick();
						}
					</script>
				</div>

			</div> <!--/ awattardiv -->

			<hr color="white">
			<div class="chargeLimitation" data-lp="1">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Lademengenbegrenzung <span class="nameLp"></span></label></h3>
				</div>
				<div class="form-row vaRow form-group mt-1 justify-content-center" data-lp="1">
					<div class="col btn-group btn-group-toggle" id="lp/1/chargeLimitation" data-toggle="buttons" data-topicprefix="openWB/config/get/sofort/">
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/1/chargeLimitation" data-option="0"> keine
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/1/chargeLimitation" data-option="1"> Energiemenge
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/1/chargeLimitation" data-option="2"> EV-SoC
						</label>
					</div>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="1">
					<label for="lp/1/energyToCharge" class="col-3 col-form-label text-right">Energie:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/1/energyToCharge" min="2" max="100" step="2" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/1/energyToCharge" class="col-3 col-form-label valueLabel" suffix="kWh"></label>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="2">
					<label for="lp/1/socToChargeTo" class="col-3 col-form-label text-right">SoC:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/1/socToChargeTo" min="5" max="100" step="5" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/1/socToChargeTo" class="col-3 col-form-label valueLabel" suffix="%"></label>
				</div>
				<div class="form-row vaRow mt-2 regularTextSize" data-option="1">
					<span class="col">Fortschritt: </span>
					<div class="col progress active">
						<div class="progress-bar progress-bar-success progress-bar-striped" id="test" role="progressbar">
						</div>
					</div>
					<span class="col">Restzeit: </span>
					<input class="btn btn-sm btn-primary regularTextSize" type="button" id="lp/1/resetEnergyToCharge" value="Reset" data-topicprefix="openWB/config/get/sofort/">
				</div>
			</div>

			<div class="chargeLimitation" data-lp="2">
				<hr color="white">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Lademengenbegrenzung <span class="nameLp"></span></label></h3>
				</div>
				<div class="form-row vaRow form-group mt-1 justify-content-center" data-lp="2">
					<div class="col btn-group btn-group-toggle" id="lp/2/chargeLimitation" data-toggle="buttons" data-topicprefix="openWB/config/get/sofort/">
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/2/chargeLimitation" data-option="0"> keine
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/2/chargeLimitation" data-option="1"> Energiemenge
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/2/chargeLimitation" data-option="2"> EV-SoC
						</label>
					</div>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="1">
					<label for="lp/2/energyToCharge" class="col-3 col-form-label text-right">Energie:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/2/energyToCharge" min="2" max="100" step="2" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/2/energyToCharge" class="col-3 col-form-label valueLabel" suffix="kWh"></label>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="2">
					<label for="lp/2/socToChargeTo" class="col-3 col-form-label text-right">SoC:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/2/socToChargeTo" min="5" max="100" step="5" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/2/socToChargeTo" class="col-3 col-form-label valueLabel" suffix="%"></label>
				</div>
				<div class="form-row vaRow mt-2 regularTextSize" data-option="1">
					<span class="col">Fortschritt: </span>
					<div class="col progress active">
						<div class="progress-bar progress-bar-success progress-bar-striped" id="test" role="progressbar">
						</div>
					</div>
					<span class="col">Restzeit: </span>
					<input class="btn btn-sm btn-primary regularTextSize" type="button" id="lp/2/resetEnergyToCharge" value="Reset" data-topicprefix="openWB/config/get/sofort/">
				</div>
			</div>

			<div class="chargeLimitation" data-lp="3">
				<hr color="white">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Lademengenbegrenzung <span class="nameLp"></span></label></h3>
				</div>
				<div class="form-row vaRow form-group mt-1 justify-content-center" data-lp="3">
					<div class="col btn-group btn-group-toggle" id="lp/3/chargeLimitation" data-toggle="buttons" data-topicprefix="openWB/config/get/sofort/">
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/3/chargeLimitation" data-option="0"> keine
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/3/chargeLimitation" data-option="1"> Energiemenge
						</label>
					</div>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="1">
					<label for="lp/3/energyToCharge" class="col-3 col-form-label text-right">Energie:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/3/energyToCharge" min="2" max="100" step="2" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/3/energyToCharge" class="col-3 col-form-label valueLabel" suffix="kWh"></label>
				</div>
				<div class="form-row vaRow mt-2 regularTextSize" data-option="1">
					<span class="col">Fortschritt: </span>
					<div class="col progress active">
						<div class="progress-bar progress-bar-success progress-bar-striped" id="test" role="progressbar">
						</div>
					</div>
					<span class="col">Restzeit: </span>
					<input class="btn btn-sm btn-primary regularTextSize" type="button" id="lp/3/resetEnergyToCharge" value="Reset" data-topicprefix="openWB/config/get/sofort/">
				</div>
			</div>

			<div class="chargeLimitation" data-lp="4">
				<hr color="white">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Lademengenbegrenzung <span class="nameLp"></span></label></h3>
				</div>
				<div class="form-row vaRow form-group mt-1 justify-content-center" data-lp="4">
					<div class="col btn-group btn-group-toggle" id="lp/4/chargeLimitation" data-toggle="buttons" data-topicprefix="openWB/config/get/sofort/">
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/4/chargeLimitation" data-option="0"> keine
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/4/chargeLimitation" data-option="1"> Energiemenge
						</label>
					</div>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="1">
					<label for="lp/4/energyToCharge" class="col-3 col-form-label text-right">Energie:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/4/energyToCharge" min="2" max="100" step="2" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/4/energyToCharge" class="col-3 col-form-label valueLabel" suffix="kWh"></label>
				</div>
				<div class="form-row vaRow mt-2 regularTextSize" data-option="1">
					<span class="col">Fortschritt: </span>
					<div class="col progress active">
						<div class="progress-bar progress-bar-success progress-bar-striped" id="test" role="progressbar">
						</div>
					</div>
					<span class="col">Restzeit: </span>
					<input class="btn btn-sm btn-primary regularTextSize" type="button" id="lp/4/resetEnergyToCharge" value="Reset" data-topicprefix="openWB/config/get/sofort/">
				</div>
			</div>

			<div class="chargeLimitation" data-lp="5">
				<hr color="white">
				<div class="row justify-content-center">
					<h3 class="font-weight-bold text-center text-lightgrey">Lademengenbegrenzung <span class="nameLp"></span></label></h3>
				</div>
				<div class="form-row vaRow form-group mt-1 justify-content-center" data-lp="5">
					<div class="col btn-group btn-group-toggle" id="lp/5/chargeLimitation" data-toggle="buttons" data-topicprefix="openWB/config/get/sofort/">
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/5/chargeLimitation" data-option="0"> keine
						</label>
						<label class="btn btn-sm btn-outline-info btn-toggle regularTextSize">
							<input type="radio" name="lp/5/chargeLimitation" data-option="1"> Energiemenge
						</label>
					</div>
				</div>
				<div class="form-row form-group mb-1 vaRow regularTextSize" data-option="1">
					<label for="lp/5/energyToCharge" class="col-3 col-form-label text-right">Energie:</label>
					<div class="col">
						<input type="range" class="form-control-range rangeInput" id="lp/5/energyToCharge" min="2" max="100" step="2" value="" data-topicprefix="openWB/config/get/sofort/">
					</div>
					<label for="lp/5/energyToCharge" class="col-3 col-form-label valueLabel" suffix="kWh"></label>
				</div>
				<div class="form-row vaRow mt-2 regularTextSize" data-option="1">
					<span class="col">Fortschritt: </span>
					<div class="col progress active">
						<div class="progress-bar progress-bar-success progress-bar-striped" id="test" role="progressbar">
						</div>
					</div>
					<span class="col">Restzeit: </span>
					<input class="btn btn-sm btn-primary regularTextSize" type="button" id="lp/5/resetEnergyToCharge" value="Reset" data-topicprefix="openWB/config/get/sofort/">
				</div>
			</div>

		</form>

	<!-- modal chargemode-select-window -->
	<div class="modal fade" id="chargeModeModal">
		<div class="modal-dialog">
			<div class="modal-content">

				<!-- modal header -->
				<div class="modal-header bg-success">
					<h4 class="modal-title">Lademodus-Auswahl</h4>
				</div>

				<!-- modal body -->
				<div class="modal-body">
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeSofortBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" chargeMode="0">Sofort</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 order-first order-sm-last py-1">
							<button id="chargeModePVBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" chargeMode="2">PV</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeMinPVBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" chargeMode="1">Min + PV</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeStdbyBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" chargeMode="4">Standby</button>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="chargeModeStopBtn" type="button" class="chargeModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" chargeMode="3">Stop</button>
						</div>
					</div>
					<span id='priorityModeBtns'>
						<hr>
						<div class="row">
							<div class="col text-center text-grey">
								Vorrang im Lademodus PV-Laden:
							</div>
						</div>
						<div class="row justify-content-center">
							<div class="col-sm-5 py-1">
								<button id="evPriorityBtn" type="button" class="priorityModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" priority="1">
									EV <span class="fas fa-car">&nbsp;</span>
								</button>
							</div>
						</div>
						<div class="row justify-content-center">
							<div class="col-sm-5 py-1">
								<button id="batteryPriorityBtn" type="button" class="priorityModeBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal" priority="0">
									Speicher <span class="fas fa-car-battery">&nbsp;</span>
								</button>
							</div>
						</div>
					</span>
					<hr>

					<div class="row">
						<div class="col text-center text-grey">
							70% beachten im Lademodus PV-Laden:
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-sm-5 py-1">
							<button id="70PvBtn" type="button" class=" 70PvBtn btn btn-lg btn-block btn-secondary" data-dismiss="modal">
								70 % beachten
							</button>
						</div>
					</div>


				</div> <!-- /modal body -->

				<!-- no modal footer -->
			</div>
		</div>
	</div>


	<!-- load Chart.js library -->
	<script src="js/Chart.bundle.js"></script>

	<!-- load mqtt library -->
	<script src = "js/mqttws31.js" ></script>

	<!-- load respective Chart.js definition -->
	<script src="themes/<?php echo $themeCookie ?>/livechart.js?ver=20200506-a"></script>
	<script src="themes/<?php echo $themeCookie ?>/awattarchart.js?ver=20200331-a"></script>
	<!-- some helper functions-->
	<script src="themes/<?php echo $themeCookie ?>/helperFunctions.js?ver=20200512-a"></script>
	<!-- data refresher -->
	<script src="themes/<?php echo $themeCookie ?>/processAllMqttMsg.js?ver=20200506-b"></script>

	<!-- some scripts -->
	<script type="text/javascript">

		var timeOfLastMqttMessage = 0;  // holds timestamp of last received message
		var landingpageShown = false;  // holds flag for landing page being shown

		function AwattarMaxPriceClick() {
			publish(document.getElementById("awattar1l").innerHTML,"openWB/set/awattar/MaxPriceForCharging");
		}

		function chargeLimitationOptionsShowHide(btnGrp, option) {
			// show/hide all option-parameters in form-rows for selected option
			var parent = btnGrp.closest('.chargeLimitation[data-lp]');  // get parent div element for charge limitation options
			$(parent).find('.form-row[data-option*=' + option + ']').show();  // now show option elements for selected option
			$(parent).find('.form-row[data-option]').not('[data-option*=' + option + ']').hide();  // hide all other option elements
		}

		function processPreloader(mqttTopic) {
			// sets flag for topic received in topic-array
			// and updates the preloader progress bar
			if ( !landingpageShown ) {
				var countTopicsReceived = 0;
				for ( var index = 0; index < topicsToSubscribe.length; index ++) {
					if ( topicsToSubscribe[index][0] == mqttTopic && topicsToSubscribe[index][1] == 0 ) {
						// topic found in array
						topicsToSubscribe[index][1] = 1;  // mark topic as received
					};
					if ( topicsToSubscribe[index][1] > 0 ) {
						countTopicsReceived++;
					}
				};
				var percentageReceived = (countTopicsReceived / topicsToSubscribe.length * 100).toFixed(0);
				var timeBetweenTwoMesagges = Date.now() - timeOfLastMqttMessage;
				if ( timeBetweenTwoMesagges > 3000 ) {
					// latest after 3 sec without new messages
					percentageReceived = 100;
					// debug output
					topicsToSubscribe.forEach((item, i) => {
						if ( item[1] == 0 ) {
							console.log('not received: ' + item[0]);
						}
					});

				}
				timeOfLastMqttMessage = Date.now();
				$("#preloaderbar").width(percentageReceived+"%");
				$("#preloaderbar").text(percentageReceived+" %");
				if ( percentageReceived == 100 ) {
					landingpageShown = true;
					setTimeout(function (){
						// delay a little bit
						$(".loader").fadeOut(1000);
					}, 500);
				}
			}
		}

		var delayUserInput = (function () {
			// sets a timeout on call and resets timout if called again for same id before timeout fires
			var timeoutHandles = {};
			return function (id, callback, ms) {
				if ( timeoutHandles[id] ) {
					clearTimeout(timeoutHandles[id]);
				};
				timeoutHandles[id] = setTimeout(function(){
					delete timeoutHandles[id];
					callback(id);
				}, ms);
			};
		})();

		$(document).ready(function(){

			$.getScript("themes/<?php echo $themeCookie ?>/setupMqttServices.js?ver=20200506-a");

			$('.enableLp').click(function(event){
				// send mqtt set to enable/disable charge point after click
				var lp = parseInt($(this).closest('[lp]').attr('lp'));  // get attribute lp-# of parent element
				if ( !isNaN(lp) && lp > 0 && lp < 9 ) {
					var isEnabled = $(this).hasClass("lpEnabledStyle")
					if ( isEnabled ) {
						publish("0", "openWB/set/lp/" + lp + "/ChargePointEnabled");
					} else {
						publish("1", "openWB/set/lp/" + lp + "/ChargePointEnabled");
					}
				}
			});

			$('.enableDevice').click(function(event){
				// send mqtt set to enable/disable Device after click
				var dev = parseInt($(this).closest('[dev]').attr('dev'));  // get attribute device-# of parent element
				var isLocked = $(this).hasClass("locked")
				if ( isLocked ) {
					if ( !isNaN(dev) && dev > 0 && dev < 9 ) {
						var isEnabled = $(this).hasClass("lpEnabledStyle")
						if ( isEnabled ) {
							publish("0", "openWB/config/set/SmartHome/Device" + dev + "/device_manual_control");
							$(this).removeClass('lpEnabledStyle').removeClass('lpDisabledStyle').addClass('lpWaitingStyle');
						} else {
							publish("1", "openWB/config/set/SmartHome/Device" + dev + "/device_manual_control");
							$(this).removeClass('lpEnabledStyle').removeClass('lpDisabledStyle').addClass('lpWaitingStyle');

						}
					}
				}
			});

			$('.changeSHMode').click(function(event){
				// send mqtt set to enable/disable Device after click
				var dev = parseInt($(this).closest('[dev]').attr('dev'));  // get attribute device-# of parent element
				if ( $(this).text() == "Automatik" ) {
						publish("1", "openWB/config/set/SmartHome/Devices/" + dev + "/mode");
					} else {
						publish("0", "openWB/config/set/SmartHome/Devices/" + dev + "/mode");
				}
			});

			$('#chargeModeSelectBtn').click(function(event){
				$("#chargeModeModal").modal("show");
			});

			$('.chargeModeBtn').click(function(event){
				var chargeMode = $(this).attr("chargeMode")
				publish(chargeMode, "openWB/set/ChargeMode");
			});

			$('.priorityModeBtn').click(function(event){
				// prio: 0 = battery, 1 = ev
				var priority = $(this).attr('priority');
				if ( priority == '0' || priority == '1' ) {
					publish(priority, 'openWB/set/system/priorityModeEVBattery');
				}
			});

			$('.70PvBtn').click(function(event){
				// 0 deaktiviert, 1 aktiviert
				var element = document.getElementById('70PvBtn');
				if ( element.classList.contains("btn-success") ) {
					publish("0", "openWB/set/pv/NurPV70Status");
				} else {
					publish("1", "openWB/set/pv/NurPV70Status");
				}
			});

			$('.btn[value="Reset"]').click(function(event){
				var topic = getTopicToSendTo($(this).attr('id'));
				console.log(topic);
				//publish("1", topic);
    		});

			$('.sofortladenLadezielSelektor').change(function(event){
			    // switches the visibility of the settings-divs according to dropdown selection
			    var selectorId = '#' + event.target.id;
			    var divAusId = selectorId.slice(0, 8) + 'n' + selectorId.slice(8);
			    var divSocId = selectorId.slice(0, 8) + 's' + selectorId.slice(8);
			    var divMengeId = selectorId.slice(0, 8) + 'm' + selectorId.slice(8);
			    switch ($(selectorId).val()) {
			        case '0':
			            $(divAusId).show();
			            $(divSocId).hide();
			            $(divMengeId).hide();
			            break;
			        case '1':
			            $(divAusId).hide();
			            $(divSocId).hide();
			            $(divMengeId).show();
			            break;
			        case '2':
			            $(divAusId).hide();
			            $(divSocId).show();
			            $(divMengeId).hide();
			            break;
			    }
			});

			$('.btn-group-toggle').change(function(event){
				// only charge limitation has class btn-group-toggle so far
				// option: 0 = keine, 1 = Energiemenge, 2 = EV-SoC
				var elementId = $(this).attr('id');
				var option = $('input[name="' + elementId + '"]:checked').data('option').toString();
				var topic = getTopicToSendTo(elementId);
				publish(option, topic);
				// show/hide respective option-values and progress
				chargeLimitationOptionsShowHide(this, option);
			});

			$('.rangeInput').on('input', function() {
				// show slider value in label of class valueLabel
				var elementId = $(this).attr('id');
				updateLabel(elementId);
				var element = $('#' + $.escapeSelector(elementId));
				var label = $('label[for="' + elementId + '"].valueLabel');
				label.addClass('text-danger');
				delayUserInput(elementId, function (id) {
					// gets executed on callback, 2000ms after last input-change
					// changes label color back to normal and sends input-value by mqtt
					var elem = $('#' + $.escapeSelector(id));
					var value = elem.val();
					var topic = getTopicToSendTo(id);
					publish(value, topic);
					var label = $('label[for="' + id + '"].valueLabel');
     				label.removeClass('text-danger');
  				}, 2000);
			});

			// register an event listener for changes in visibility
			let hidden;
			let visibilityChange;
			if (typeof document.hidden !== 'undefined') { // Opera 12.10 and Firefox 18 and later support
				hidden = 'hidden';
				visibilityChange = 'visibilitychange';
			} else if (typeof document.msHidden !== 'undefined') {
				hidden = 'msHidden';
				visibilityChange = 'msvisibilitychange';
			} else if (typeof document.webkitHidden !== 'undefined') {
				hidden = 'webkitHidden';
				visibilityChange = 'webkitvisibilitychange';
			}
			window.document.addEventListener(visibilityChange, () => {
				if (!document[hidden]) {
					// once page is unhidden... reload graph completety
					initialread = 0;
					all1 = 0;
					all2 = 0;
					all3 = 0;
					all4 = 0;
					all5 = 0;
					all6 = 0;
					all7 = 0;
					all8 = 0;
					subscribeMqttGraphSegments();
				}
			});

		});  // end document ready
	</script>

</body>

</html>
