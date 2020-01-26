<header>
    <!-- Fixed navbar -->
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
        <a class="navbar-brand" href="./index.php">
            openWB
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
                        <a class="dropdown-item" href="./settings/settings.php">Allgemein</a>
                        <a class="dropdown-item" href="./settings/pvconfig.php">PV-Ladeeinstellungen</a>
                        <a class="dropdown-item" href="./settings/smarthome.php">Smart Home</a>
                        <a class="dropdown-item" href="./settings/mqtt.php">MQTT-Brücke</a>
                        <a class="dropdown-item" href="./settings/modulconfig.php">Modulkonfiguration</a>
                    </div>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="./settings/autoLock.php">Auto-Lock</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="./settings/setTheme.php">Theme</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="./settings/misc.php">Verschiedenes</a>
                </li>

                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbardropSystem" data-toggle="dropdown">
                        System
                    </a>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="./settings/update.php">Update</a>
                        <a class="dropdown-item" data-toggle="modal" data-target="#downgradeConfirmationModal">Downgrade</a>
                        <a class="dropdown-item" data-toggle="modal" data-target="#rebootConfirmationModal">Reboot</a>
                        <!-- href="./settings/reboot.php">Reboot</a> -->
                    </div>
                </li>

            </ul>
        </div>
    </nav>
</header>

<!-- modal reboot-confirmation window -->
<div class="modal fade" id="rebootConfirmationModal">
    <div class="modal-dialog">
        <div class="modal-content">

            <!-- modal header -->
            <div class="modal-header btn-red">
                <h4 class="modal-title text-light">Achtung</h4>
            </div>

            <!-- modal body -->
            <div class="modal-body text-center">
                Soll die openWB wirklich neu gestartet werden?
            </div>

            <!-- modal footer -->
            <div class="modal-footer d-flex justify-content-center">
                <button type="button" class="btn btn-lg btn-green" data-dismiss="modal" onclick="window.location.href='./tools/reboot.html'">Reboot</button>
                <button type="button" class="btn btn-lg btn-red" data-dismiss="modal">Abbruch</button>
            </div>

        </div>
    </div>
</div>

<!-- modal reboot-confirmation window -->
<div class="modal fade" id="downgradeConfirmationModal">
    <div class="modal-dialog">
        <div class="modal-content">

            <!-- modal header -->
            <div class="modal-header btn-red">
                <h4 class="modal-title text-light">Achtung</h4>
            </div>

            <!-- modal body -->
            <div class="modal-body text-center">
                        Aktuelle Version: <?php echo file_get_contents('/var/www/html/openWB/web/version'); ?><br>
                        <br>
                        Soll wirklich ein Downgrade der openWB auf<br>
                        <b>Version 1.5 stable</b><br>
                        erfolgen?<br>
                        <br>
                        Das Downgrade kann einige Zeit in Anspruch nehmen. Alle Einstellungen bleiben erhalten.
                        Einige Optionen/Features der aktuellen Version sind nach erfolgreichem Downgrade ggf. nicht mehr verfügbar!<br>
                        <br>
                        <b>
                            Es wird empfohlen, zur Sicherheit zuvor ein Backup zu erstellen.<br>
                            <span class="text-danger">Fahrzeuge sind vor dem Downgrade abzustecken!</span>
                        </b>
            </div>

            <!-- modal footer -->
            <div class="modal-footer d-flex justify-content-center">
                <button type="button" class="btn btn-lg btn-green" data-dismiss="modal" onclick="window.location.href='./tools/updateredirect15.html'">Downgrade</button>
                <button type="button" class="btn btn-lg btn-red" data-dismiss="modal">Abbruch</button>
            </div>

        </div>
    </div>
</div>


<script type="text/javascript">

</script>
