<div class="sidenav">
    <a class="btn btn-toggle active" href="#dashboard" onclick="return false;">
        <div class="icon">
            <?= file_get_contents("yourcharge/icons/chart-line-solid.svg"); ?>
        </div>
        Dashboard
    </a>
    <div class="btn " id="changeCode">
        <div class="icon">
            <?= file_get_contents("yourcharge/icons/lock-solid.svg"); ?>
        </div>
        Code ändern
    </div>
    <div class="btn " id="changeTimeout">
        <div class="icon">
            <?= file_get_contents("yourcharge/icons/clock-regular.svg"); ?>
        </div>
        Timeout ändern
    </div>
    <div class="btn " id="displaylock">
        <div class="icon">
            <?= file_get_contents("yourcharge/icons/lock-open-solid.svg"); ?>
        </div>
        sperren
    </div>

</div>