#!/usr/bin/env python3
import re
import time

if __name__ == "__main__":
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import pub
    from helpermodules import timecheck
    import set_values
    import tesla_lib
else:
    from ...helpermodules import log
    from ...helpermodules import pub
    from ...helpermodules import timecheck
    from . import set_values
    from . import tesla_lib


class module(set_values.set_values):
    def __init__(self, num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["set"] = {}
        self.num = num

    def read(self, plug_state, charge_state):
        try:
            request_soc = self.check_interval(self.data, plug_state, charge_state)
            if request_soc == True:
                ret = self._check_token()
                if ret == 0:
                    if charge_state == False:
                        ret = self._wake_up_car()
                        if ret != 0:
                            return
                    soc = self.getAndWriteSoc()
                    if 0 <= soc <= 100:
                        timestamp = timecheck.create_timestamp()
                        values = [soc, timestamp]
                        self.set(self.num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def _check_token(self):
        try:
            # check if token is present
            try:
                with open(self.data["config"]["tokenfile"], "r") as f:
                    ret = 0
            except:
                log.log_comp("error", "EV "+str(self.num)+": No token found.", self.ramdisk, file="soc")
                self.set_state(self.ramdisk, 0, self.num, "Keine Zugangsdaten eingetragen")
                ret = 2
            return ret
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def _wake_up_car(self):
        try:
            log.log_comp("info", "Lp"+str(self.num)+": Waking up car.", self.ramdisk, file="soc")
            counter = 0
            while counter <= 12:
                response = tesla_lib.lib(email=self.data["config"]["username"], ev_num=self.num, p_ramdisk=self.ramdisk, tokensfile=self.data["config"]["tokenfile"], vehicle=self.data["config"]["tesla_ev_num"], command="vehicles/#/wake_up")
                if response != 0:
                    response = response.json()
                    state = response["response"]["state"]
                    if state == "online":
                        break
                    counter = counter+1
                    time.sleep(5)
                    log.log_comp("error", "EV "+str(self.num)+": Loop: $counter State: "+str(state), self.ramdisk, file="soc")
                else:
                    self.set_state(self.ramdisk, 1, self.num, "EV "+str(self.num)+": WakeUp fehlgeschlagen")
                    return 1
            log.log_comp("info", "EV "+str(self.num)+": Car state after wakeup: "+str(state), self.ramdisk, file="soc")
            if state != "online":
                self.set_state(self.ramdisk, 1, self.num, "EV "+str(self.num)+": WakeUp fehlgeschlagen")
                return 1
            else:
                return 0
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def getAndWriteSoc(self):
        try:
            regex = '^-?[0-9]+$'
            response = tesla_lib.lib(email=self.data["config"]["username"], ev_num=self.num, p_ramdisk=self.ramdisk, tokensfile=self.data["config"]["tokenfile"], vehicle=self.data["config"]["tesla_ev_num"], data="vehicles/#/vehicle_data")
            if response != 0:
                # current state of car
                response = response.json()
                state = response["response"]["state"]
                log.log_comp("error", "EV "+str(self.num)+": State: "+str(state), self.ramdisk, file="soc")
                soc = response["response"]["charge_state"]["battery_level"]
                log.log_comp("error", "EV "+str(self.num)+": SoC: "+str(soc), self.ramdisk, file="soc")
                if re.search(regex, str(soc)) != None:
                    if soc != 0:
                        if self.ramdisk == True:
                            # bei Aufruf aus 1.9 wird die read-Methode nicht aufgerufen
                            values = [soc, "0"]
                            self.set(self.num, values, self.ramdisk)
                            self.set_state(self.ramdisk, 0, self.num, "EV "+str(self.num)+": SoC-Abfrage erfolgreich")
                        else:
                            return soc
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    # unused
    # clearPassword(){
    #     openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Removing password from config."
    #     sed -i "s/$passwordConfigText=.*/$passwordConfigText=''/" $CONFIGFILE
    # }

    # setTokenPassword(){
    #     openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Writing token password to config."
    #     sed -i "s/$passwordConfigText=.*/$passwordConfigText='$TOKENPASSWORD'/" $CONFIGFILE
    #     sed -i "s/$mfaPasscodeConfigText=.*/$mfaPasscodeConfigText=XXX/" $CONFIGFILE
    # }


if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
        mod = module(num, True)
        mod.data["config"] = {}
        username = str(sys.argv[2])
        mod.data["config"]["username"] = username
        tokenfile = str(sys.argv[3])
        mod.data["config"]["tokenfile"] = tokenfile
        tesla_ev_num = str(sys.argv[4])
        mod.data["config"]["tesla_ev_num"] = tesla_ev_num
        wake_up = int(sys.argv[5])

        ret = mod._check_token()
        if ret == 0:
            if wake_up == True:
                ret = mod._wake_up_car()
                if ret != 0:
                    sys.exit(0)
            mod.getAndWriteSoc()
    except Exception as e:
        log.log_exception_comp(e, True)
