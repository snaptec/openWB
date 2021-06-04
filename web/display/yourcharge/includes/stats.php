<div class="card">
    <div class="card-header">
        <div class="flex-row">
            <div class="status-indicator status-1 inactive status-1-1">1</div>
            <div class="status-indicator status-1 inactive status-1-2">2</div>
            <div class="status-indicator status-1 inactive status-1-3">3</div>
        </div>
    </div>
    <div class="card-body">
        <div class="icon active" id="charger">
            <?= file_get_contents("yourcharge/icons/YourCharge_Icon-FlatWhite.svg"); ?>
        </div>
        <div class="progress">
            <div id="loadingpower" class="progress-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
        <div class="flex-row justify-content-between">

            <span>Ladeleistung</span>
            <span class="color-primary gesamtll-value">0 W</span>
            <span><span class="maxKWhAllowed">0</span> kW</span>
        </div>
    </div>
</div>
<div class="card">
    <div class="card-body flex-row justify-content-between">
        <span>Letzte Lademenge</span>
        <span class="kWhchargedsinceplugged-1">0 kWh</span>
    </div>
</div>

<div class="card">
    <div class="card-body flex-row justify-content-between">
        <span>Heute geladen</span>
        <span class="kWhDailyCharged-1">0,00 kWh</span>
    </div>
</div>

<div class="card">
    <div class="card-body flex-row justify-content-between">
        <span>Zählerstand</span>
        <span class="kWhCounter-1">0,00 kWh</span>
    </div>
</div>
<div class="card">
    <div class="card-body flex-row justify-content-between">
        <span>Version</span>
        <span class="systemVersion">Lädt..</span>
    </div>
</div>