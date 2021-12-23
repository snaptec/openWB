<div class="modal" id="changeDisplayTimeoutModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <!-- modal header -->
            <div class="modal-header">

                <div class="close text-danger" data-dismiss="modal">X</div>

                <!-- <div class="col justify-content-center">
                    <div class="modal-title text-dark text-center">
                        <img class="logo" src="display/yourcharge/logo.png" />
                    </div>
                </div> -->
            </div>
            <!-- modal body -->
            <div class="modal-body">
                <span id="changeDisplayTimeoutHeadline">Ruhezustand in Sek.</span>


                <div id="successChangeDisplayTimeoutIcon" class="PINbutton successIcon success">
                    <div class="icon">
                        <?= file_get_contents("yourcharge/icons/check-solid.svg"); ?>
                    </div>
                </div>
                <div id="changeDisplayTimeout" class="text-center">
                    <input id="changeDisplayTimeoutBox" type="number" value="<?= $displayTimeout; ?>" name="Lockbox" disabled="disabled" class="text-center display-4" size="4" />
                    <br />
                    <input type="button" class="PINbutton" name="1" value="1" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="2" value="2" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="3" value="3" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <br />
                    <input type="button" class="PINbutton" name="4" value="4" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="5" value="5" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="6" value="6" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <br />
                    <input type="button" class="PINbutton" name="7" value="7" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="8" value="8" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="9" value="9" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <br />
                    <input type="button" class="PINbutton clear" name="-" value="C" onclick="clearForm($('#changeDisplayTimeoutBox'));" />
                    <input type="button" class="PINbutton" name="0" value="0" onclick="addLockNumber(this,$('#changeDisplayTimeoutBox'));" />
                    <button class="PINbutton enter" name="+" value="enter" onclick="submitChangeDisplayTimeout(this,getChangeDisplayTimeoutOpts());">
                        <div class="icon">
                            <?= file_get_contents("yourcharge/icons/check-solid.svg"); ?>
                        </div>
                    </button>
                </div>

                <button disabled id="continueDisplayTimeout" class="PINbutton hide" onclick="closeChangeDisplayTimeout();">
                    Weiter
                </button>
                <!-- /modal body -->
            </div>
        </div>
    </div>
    <script>
        const clearForm = (lockbox) => {

            const val = lockbox.val();
            lockbox.val(val.substring(0, val.length - 1))
        }
        const closeChangeDisplayTimeout = () => {
            const {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            } = getChangeDisplayTimeoutOpts();
            $("#successChangeDisplayTimeoutIcon").addClass("show");
            hideBlur = true;
            $("#main").removeClass("blur");
            lockModal.find(".modal-body").removeClass("bg-success");
            lockCode.find(".enter").prop("disabled", false);
            lockModal.modal("hide");
            $("#successChangeDisplayTimeoutIcon").removeClass("show");
            lockbox.css("opacity", 1);
            $("#continueDisplayTimeout").addClass("hide").prop("disabled", true);
            $("#changeDisplayTimeoutHeadline").css("opacity", 1);
            lockCode.find(".PINbutton").css("opacity", 1);
            for (let i = 1; i < 7; i++) {
                $(`.PINbutton[name="${i}"]`).removeClass("hide");
            }
        }

        const getChangeDisplayTimeoutOpts = () => {
            const lockCode = $("#changeDisplayTimeout");
            const lockbox = $("#changeDisplayTimeoutBox");
            const lockModal = $("#changeDisplayTimeoutModal");
            const clearButton = $("#changeDisplayTimeout,#changeDisplayTimeoutModal .clear");
            const enterButton = $("#changeDisplayTimeoutModal .enter");
            return {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            }
        }

        function submitChangeDisplayTimeout(e, opts) {

            const {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            } = opts;
            const displayTimeout = $("#changeDisplayTimeoutBox").val();
            $.get({

                    url: "display/yourcharge/changeConfig.php?displayTimeout=" + displayTimeout,
                    cache: false,
                },
                function(data) {
                    hideBlur = true;
                    if (data == 1) {
                        inactivityTimeout = displayTimeout * 1000
                        lockDisplay(false);
                        lockCode.find(".PINbutton").css("opacity", 0);
                        lockbox.css("opacity", 0);
                        lockCode.find(".enter").prop("disabled", true);
                        for (let i = 1; i < 7; i++) {
                            $(`.PINbutton[name="${i}"]`).addClass("hide");
                        }
                        $("#continueDisplayTimeout").removeClass("hide").prop("disabled", false);
                        $("#successChangeDisplayTimeoutIcon").addClass("show");
                        $("#changeDisplayTimeoutHeadline").css("opacity", 0);
                    } else {
                        lockCode.find(".enter").addClass("text-danger").prop("disabled", true);
                        window.setTimeout(function() {
                            lockCode.find(".enter").removeClass("text-danger").prop("disabled", false);
                        }, 3000);
                    }
                }
            );
        }
    </script>
</div>