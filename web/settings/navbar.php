<header>
	<!-- Fixed navbar -->
	<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
		<a class="navbar-brand" href="./index.php">
			<span>openWB</span>
		</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="collapsibleNavbar">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" href="./index.php">Home</a>
				</li>

				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbardropSettings" data-toggle="dropdown">
						Einstellungen
					</a>
					<div class="dropdown-menu">
						<a class="dropdown-item" id="navAllgemein" href="./settings/settings.php">Allgemein</a>
						<a class="dropdown-item" id="navPVLadeeinstellungen" href="./settings/pvconfig.php">PV-Ladeeinstellungen</a>
						<a class="dropdown-item" id="navSmartHome" href="./settings/smarthome.php">Smart Home</a>
						<a class="dropdown-item" id="navOpenwbCloud" href="./settings/cloudconfig.php">openWB Cloud</a>
						<a class="dropdown-item" id="navMqttBruecke" href="./settings/mqtt.php">MQTT-Brücke</a>
						<a class="dropdown-item" id="navModulkonfiguration" data-toggle="modal" data-target="#modulconfigConfirmationModal" style="cursor: pointer;">Modulkonfiguration</a>
					</div>
				</li>

				<li class="nav-item">
					<a class="nav-link" id="navAutolock" href="./settings/autoLock.php">Auto-Lock</a>
				</li>

				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbardropSettings2" data-toggle="dropdown">
						Erscheinungsbild
					</a>
					<div class="dropdown-menu">
						<a class="dropdown-item" id="navSetTheme" href="./settings/setTheme.php">Theme-Auswahl</a>
						<a class="dropdown-item" id="navGraphSettings" href="./settings/graphconfig.php">Graph</a>
					</div>
				</li>

				<li class="nav-item">
					<a class="nav-link" id="navVerschiedenes" href="./settings/misc.php">Verschiedenes</a>
				</li>

				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbardropSystem" data-toggle="dropdown">
						System
					</a>
					<div class="dropdown-menu">

						<a class="dropdown-item" id="navBackup" data-toggle="modal" data-target="#backupConfirmationModal" style="cursor: pointer;">Backup erstellen</a>
						<a class="dropdown-item" id="navWiederherstellen" data-toggle="modal" data-target="#restoreConfirmationModal" style="cursor: pointer;">Backup wiederherstellen</a>
						<a class="dropdown-item" id="navReboot" data-toggle="modal" data-target="#rebootConfirmationModal" style="cursor: pointer;">Reboot</a>
						<a class="dropdown-item" id="navUpdate" href="./settings/update.php">Update</a>
						<a class="dropdown-item" id="navDebugging" href="./settings/debugging.php">Debugging</a>
						<a class="dropdown-item" id="navPasswortschutz" href="./settings/setPassword.php">Passwortschutz</a>
					</div>
				</li>

			</ul>
		</div>
	</nav>
</header>

<!-- modal backup-confirmation window -->
<div class="modal fade" id="backupConfirmationModal" role="dialog">
	<div class="modal-dialog" role="document">
		<div class="modal-content">
			<!-- modal header -->
			<div class="modal-header btn-blue">
				<h4 class="modal-title text-light">Info</h4>
			</div>
			<!-- modal body -->
			<div class="modal-body text-center">
				<p>
					Das Erstellen des Backups kann einige Zeit in Anspruch nehmen.<br>
					Fortfahren?
				</p>
			</div>
			<!-- modal footer -->
			<div class="modal-footer d-flex justify-content-center">
				<button type="button" class="btn btn-green" data-dismiss="modal" onclick="window.location.href='./tools/bckredirect.html'">Backup</button>
				<button type="button" class="btn btn-red" data-dismiss="modal">Abbruch</button>
			</div>
		</div>
	</div>
</div>

<!-- modal restore-confirmation window -->
<div class="modal fade" id="restoreConfirmationModal" role="dialog">
	<div class="modal-dialog" role="document">
		<div class="modal-content">
			<!-- modal header -->
			<div class="modal-header btn-red">
				<h4 class="modal-title text-light">Achtung</h4>
			</div>
			<!-- modal body -->
			<div class="modal-body text-center">
				<p>
					Soll wirklich ein gespeichertes Backup wiederhergestellt werden?<br>
					Die Wiederherstellung kann einige Zeit in Anspruch nehmen. Aktuelle Einstellungen werden mit dem Backup überschrieben!
				</p>
				<p>
					<span class="text-danger">Fahrzeuge sind vor der Wiederherstellung abzustecken!</span>
				</p>
			</div>
			<!-- modal footer -->
			<div class="modal-footer d-flex justify-content-center">
				<button type="button" class="btn btn-green" data-dismiss="modal" onclick="window.location.href='./tools/upload.html'">Wiederherstellen</button>
				<button type="button" class="btn btn-red" data-dismiss="modal">Abbruch</button>
			</div>
		</div>
	</div>
</div>

<!-- modal reboot-confirmation window -->
<div class="modal fade" id="rebootConfirmationModal" role="dialog">
	<div class="modal-dialog" role="document">
		<div class="modal-content">
			<!-- modal header -->
			<div class="modal-header btn-red">
				<h4 class="modal-title text-light">Achtung</h4>
			</div>
			<!-- modal body -->
			<div class="modal-body text-center">
				<p>
					Soll die openWB wirklich neu gestartet werden?
				</p>
			</div>
			<!-- modal footer -->
			<div class="modal-footer d-flex justify-content-center">
				<button type="button" class="btn btn-green" data-dismiss="modal" onclick="window.location.href='./tools/reboot.html'">Reboot</button>
				<button type="button" class="btn btn-red" data-dismiss="modal">Abbruch</button>
			</div>
		</div>
	</div>
</div>

<!-- modal modulkonfig-confirmation window -->
<div class="modal fade" id="modulconfigConfirmationModal" role="dialog">
	<div class="modal-dialog" role="document">
		<div class="modal-content">
			<!-- modal header -->
			<div class="modal-header btn-red">
				<h4 class="modal-title text-light">Achtung</h4>
			</div>
			<!-- modal body -->
			<div class="modal-body text-center">
				<p>
					Nach erfolgter Einrichtung der openWB ist in der Modulkonfiguration grundsätzlich keine weitere Einstellung notwendig.<br>
					Fortfahren?
				</p>
			</div>
			<!-- modal footer -->
			<div class="modal-footer d-flex justify-content-center">
				<button type="button" class="btn btn-green" data-dismiss="modal" onclick="window.location.href='./settings/modulconfig.php'">Weiter</button>
				<button type="button" class="btn btn-red" data-dismiss="modal">Abbruch</button>
			</div>
		</div>
	</div>
</div>
