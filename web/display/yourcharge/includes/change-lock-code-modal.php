<div class="modal" id="changeLockModal">
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
                <span id="changeHeadline">Neuen Code eingeben</span>


                <div id="successChangeIcon" class="PINbutton successIcon success">
                    <div class="icon">
                        <?= file_get_contents("yourcharge/icons/check-solid.svg"); ?>
                    </div>
                </div>
                <div id="changeLockcode" class="text-center">
                    <input id="changeLockbox" type="password" value="" name="Lockbox" disabled="disabled" class="text-center display-4" size="4" />
                    <br />
                    <input type="button" class="PINbutton" name="1" value="1" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="2" value="2" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="3" value="3" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <br />
                    <input type="button" class="PINbutton" name="4" value="4" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="5" value="5" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="6" value="6" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <br />
                    <input type="button" class="PINbutton" name="7" value="7" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="8" value="8" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="9" value="9" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <br />
                    <input type="button" class="PINbutton clear" name="-" value="C" onclick="clearForm($('#changeLockbox'));" />
                    <input type="button" class="PINbutton" name="0" value="0" onclick="addLockNumber(this,$('#changeLockbox'));" />
                    <button class="PINbutton enter" name="+" value="enter" onclick="submitChangeLockForm(this,getChangeOpts());">
                        <div class="icon">
                            <?= file_get_contents("yourcharge/icons/check-solid.svg"); ?>
                        </div>
                    </button>
                </div>

                <button disabled id="continue" class="PINbutton hide" onclick="closeChangeLockModal();">
                    Weiter
                </button>
                <!-- /modal body -->
            </div>
        </div>
    </div>
    <script>
        const closeChangeLockModal = () => {
            const {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            } = getChangeOpts();
            hideBlur = true;
            $("#main").removeClass("blur");
            $("#successChangeIcon").addClass("show");
            lockModal.find(".modal-body").removeClass("bg-success");
            lockCode.find(".enter").prop("disabled", false);
            lockbox.val("");
            lockModal.modal("hide");
            $("#successChangeIcon").removeClass("show");
            lockbox.css("opacity", 1);
            $("#continue").addClass("hide").prop("disabled", true);
            $("#changeHeadline").css("opacity", 1);
            lockCode.find(".PINbutton").css("opacity", 1);
            for (let i = 1; i < 7; i++) {
                $(`.PINbutton[name="${i}"]`).removeClass("hide");
            }
        }

        const getChangeOpts = () => {
            const lockCode = $("#changeLockcode");
            const lockbox = $("#changeLockbox");
            const lockModal = $("#changeLockModal");
            const clearButton = $("#changeLockbox,#changelockModal .clear");
            const enterButton = $("#changelockModal .enter");
            return {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            }
        }

        function submitChangeLockForm(e, opts) {

            const {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            } = opts;
            $.get({

                    url: "display/yourcharge/changeConfig.php?pin=" + $("#changeLockbox").val(),
                    cache: false,
                },
                function(data) {
                    hideBlur = false;
                    if (data == 1) {

                        lockDisplay(false);
                        lockCode.find(".PINbutton").css("opacity", 0);
                        lockbox.css("opacity", 0);
                        lockCode.find(".enter").prop("disabled", true);
                        for (let i = 1; i < 7; i++) {
                            $(`.PINbutton[name="${i}"]`).addClass("hide");
                        }
                        $("#continue").removeClass("hide").prop("disabled", false);
                        $("#successChangeIcon").addClass("show");
                        $("#changeHeadline").css("opacity", 0);
                    } else {
                        lockCode.find(".enter").addClass("text-danger").prop("disabled", true);
                        lockbox.val("");
                        window.setTimeout(function() {
                            lockCode.find(".enter").removeClass("text-danger").prop("disabled", false);
                        }, 3000);
                    }
                }
            );
        }
    </script>
</div>