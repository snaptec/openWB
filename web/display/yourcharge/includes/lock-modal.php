<!-- modal lock-window -->
<script>
</script>
<div class="modal" data-backdrop="static" id="lockModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <!-- modal header -->
            <div class="modal-header">
                <div class="col justify-content-center">
                    <div class="modal-title text-dark text-center">
                        <img class="logo" src="display/yourcharge/logo.png" />
                    </div>
                </div>
            </div>
            <!-- modal body -->
            <div class="modal-body">
                <span class="headline">Pin eingeben</span>
                <div id="successIcon" class="PINbutton success successIcon">
                    <div class="icon">
                        <?= file_get_contents("yourcharge/icons/check-solid.svg"); ?>
                    </div>
                </div>
                <div id="Lockcode" class="text-center">
                    <input id="Lockbox" type="password" value="" name="Lockbox" disabled="disabled" class="text-center display-4" size="4" />
                    <input type="button" class="PINbutton" name="1" value="1" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="2" value="2" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="3" value="3" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="4" value="4" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="5" value="5" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="6" value="6" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="7" value="7" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="8" value="8" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="9" value="9" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <input type="button" class="PINbutton clear" name="-" value="C" onclick="clearForm($('#Lockbox'));" />
                    <input type="button" class="PINbutton" name="0" value="0" onclick="addLockNumber(this,$('#Lockbox'));" />
                    <button class="PINbutton enter" name="+" value="enter" onclick="submitLockForm(this,getOpts());">
                        <div class="icon">
                            <?= file_get_contents("yourcharge/icons/check-solid.svg"); ?>
                        </div>
                    </button>
                </div>
            </div>
            <!-- /modal body -->
        </div>
    </div>
    <script>
        function addLockNumber(e, tempLockbox) {
            var v = tempLockbox.val();
            tempLockbox.val(v + e.value);
        }

        function clearLockForm(e, tempLockbox) {
            tempLockbox.val("");
        }


        const closeLockModal = () => {
            const {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            } = getOpts();
            $("#successIcon").addClass("show");
            lockModal.find(".modal-body").removeClass("bg-success");
            lockCode.find(".enter").prop("disabled", false);
            lockbox.val("");
            lockModal.modal("hide");
            $("#successIcon").removeClass("show");
            lockbox.css("opacity", 1);
            lockCode.find(".PINbutton").css("opacity", 1);
        }

        const getOpts = () => {

            const lockCode = $("#Lockcode");
            const lockbox = $("#Lockbox");
            const lockModal = $("#lockModal");
            const clearButton = $("#Lockbox,#lockModal .clear");
            const enterButton = $("#lockModal .enter");
            return {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            }
        }


        function submitLockForm(e, opts) {
            const {
                lockCode,
                lockbox,
                lockModal,
                clearButton,
                enterButton
            } = opts;
            $.get({
                    url: "display/yourcharge/checklock.php?pin=" + lockbox.val(),
                    cache: false,
                },
                function(data) {
                    if (data == 1) {
                        lockDisplay(false);
                        lockCode.find(".PINbutton").css("opacity", 0);
                        lockbox.css("opacity", 0);
                        lockCode.find(".enter").prop("disabled", true);
                        $("#successIcon").addClass("show");
                        setTimeout(closeLockModal, 1000);
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
