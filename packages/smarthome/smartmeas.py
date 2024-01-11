from smarthome.smartbase0 import Sbase0
from typing import Dict, Tuple
from modules.common import modbus
from modules.common import sdm, b23
from modules.common import lovato
import logging
log = logging.getLogger(__name__)


class Slbase(Sbase0):
    def __init__(self) -> None:
        #
        # setting
        super().__init__()
        self.device_nummer = 0
        self.device_name = 'none'
        self.device_type = 'none'
        self.temp0 = '300'
        self.temp1 = '300'
        self.temp2 = '300'
        self.device_temperatur_configured = 0
        self.devuberschuss = 0
        self.newwatt = 0
        self.newwattk = 0
        self.relais = 0
        self._smart_param = {}  # type: Dict[str, str]
        self._device_differentmeasureoment = 0
        self._device_configured = '0'
        self._device_ip = 'none'
        self._device_measuretype = 'none'
        self._device_measureip = 'none'
        self._device_measureportsdm = 8899
        self._device_measureid = 0
        self._device_measuresmaser = '123'
        self._device_measuresmaage = 15
        self._device_leistungurl = 'none'
        self._device_stateurl = 'none'
        self._device_measureurl = 'none'
        self._device_measureurlc = 'none'
        self._device_measurejsonurl = 'none'
        self._device_measurejsonpower = 'none'
        self._device_measurejsoncounter = 'none'
        self._device_measureavmactor = 'none'
        self._device_measureavmusername = 'none'
        self._device_measureavmpassword = 'none'
        self._device_actor = 'none'
        self._device_username = 'none'
        self._device_password = 'none'
        self._device_measchan = 0
        self._device_chan = 0
        self._device_measureavmusername = 'none'
        self._device_measureavmpassword = 'none'
        self._device_measureshusername = 'none'
        self._device_measureshpassword = 'none'
        self._device_measureshauth = 0
        self._device_shpassword = 'none'
        self._device_shusername = 'none'
        self._device_shauth = 0

    def updatepar(self, input_param: Dict[str, str]) -> None:
        self._smart_param = input_param.copy()
        self.device_nummer = int(self._smart_param.get('device_nummer', '0'))
        for key, value in self._smart_param.items():
            try:
                valueint = int(value)
            except Exception:
                valueint = 0
            # params known to be used in sbase, to avoid logging
            if (key in ['device_nummer', 'device_mineinschaltdauer',
                        'device_finishTime', 'device_ausschaltschwelle',
                        'device_manual_control', 'device_canSwitch',
                        'device_standbyDuration', 'device_startTime',
                        'device_onuntilTime', 'device_einschaltverzoegerung',
                        'device_standbyPower', 'device_einschaltschwelle',
                        'device_ausschaltverzoegerung',
                        'device_speichersocbeforestop',
                        'device_homeConsumtion',
                        'device_deactivateWhileEvCharging',
                        'device_startupMulDetection', 'device_onTime',
                        'device_speichersocbeforestart', 'device_endTime',
                        'device_maxeinschaltdauer', 'mode',
                        'WHImported_temp', 'RunningTimeToday',
                        'oncountnor', 'OnCntStandby', 'device_deactivateper',
                        'device_startupDetection']):
                pass
            elif (key == 'device_differentMeasurement'):
                self._device_differentmeasurement = valueint
            elif (key == 'device_type'):
                self.device_type = value
            elif (key == 'device_configured'):
                self._device_configured = value
            elif (key == 'device_name'):
                self.device_name = value
            elif (key == 'device_temperatur_configured'):
                self.device_temperatur_configured = valueint
            elif (key == 'device_ip'):
                self._device_ip = value
            elif (key == 'device_measureType'):
                self._device_measuretype = value
            elif (key == 'device_measureip'):
                self._device_measureip = value
            elif (key == 'device_measurePortSdm'):
                self._device_measureportsdm = valueint
            elif (key == 'device_measuresmaage'):
                self._device_measuresmaage = valueint
            elif (key == 'device_measchan'):
                self._device_measchan = valueint
            elif (key == 'device_chan'):
                self._device_chan = valueint
            elif (key == 'device_measuresmaser'):
                self._device_measuresmaser = value
            elif (key == 'device_measureid'):
                self._device_measureid = valueint
            elif (key == 'device_leistungurl'):
                self._device_leistungurl = value
            elif (key == 'device_measureurl'):
                self._device_measureurl = value
            elif (key == 'device_measureurlc'):
                self._device_measureurlc = value
            elif (key == 'device_measurejsonurl'):
                self._device_measurejsonurl = value
            elif (key == 'device_measurejsonpower'):
                self._device_measurejsonpower = value
            elif (key == 'device_measurejsoncounter'):
                self._device_measurejsoncounter = value
            elif (key == 'device_measureavmactor'):
                self._device_measureavmactor = value
            elif (key == 'device_measureavmusername'):
                self._device_measureavmusername = value
            elif (key == 'device_measureavmpassword'):
                self._device_measureavmpassword = value
            elif (key == 'device_actor'):
                self._device_actor = value
            elif (key == 'device_username'):
                self._device_username = value
            elif (key == 'device_password'):
                self._device_password = value
            elif (key == 'device_stateurl'):
                self._device_stateurl = value
            elif (key == 'device_measureshusername'):
                self._device_measureshusername = value
            elif (key == 'device_measureshpassword'):
                self._device_measureshpassword = value
            elif (key == 'device_measureshauth'):
                self._device_measureshauth = valueint
            elif (key == 'device_shusername'):
                self._device_shusername = value
            elif (key == 'device_shpassword'):
                self._device_shpassword = value
            elif (key == 'device_shauth'):
                self._device_shauth = valueint
            else:
                log.info("(" + str(self.device_nummer) + ") "
                         + "Slbase überlesen " + key +
                         " " + value)


class Slmqtt(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwattread(self) -> None:
        self._watt(self._device_ip)

    def sepwattread(self) -> Tuple[int, int]:
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip: str) -> None:
        argumentList = ['python3', self._prefixpy + 'mqtt/watt.py',
                        str(self.device_nummer), str(ip),
                        str(self.devuberschuss)]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('mqtt', self.device_nummer, ip, str(e1)))


class Slshelly(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwattread(self) -> None:
        self._watt(self._device_ip, self._device_chan,  self._device_shauth,
                   self._device_shusername, self._device_shpassword)

    def sepwattread(self) -> Tuple[int, int]:
        self._watt(self._device_measureip, self._device_measchan, self._device_measureshauth,
                   self._device_measureshusername, self._device_measureshpassword)
        return self.newwatt, self.newwattk

    def _watt(self, ip: str, chan: int, shaut: int, shuser: str, shpw: str) -> None:
        argumentList = ['python3', self._prefixpy + 'shelly/watt.py',
                        str(self.device_nummer), str(ip), '0',
                        str(chan), str(shaut), shuser, shpw]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
            if (self.device_temperatur_configured > 0):
                self.temp0 = str(answer['temp0'])
                with open(self._basePath+'/ramdisk/device' +
                          str(self.device_nummer) + '_temp0', 'w') as f:
                    f.write(str(self.temp0))
            else:
                self.temp0 = '300'
            if (self.device_temperatur_configured > 1):
                self.temp1 = str(answer['temp1'])
                with open(self._basePath+'/ramdisk/device' +
                          str(self.device_nummer) + '_temp1', 'w') as f:
                    f.write(str(self.temp1))
            else:
                self.temp1 = '300'
            if (self.device_temperatur_configured > 2):
                self.temp2 = str(answer['temp2'])
                with open(self._basePath+'/ramdisk/device' +
                          str(self.device_nummer) + '_temp2', 'w') as f:
                    f.write(str(self.temp2))
            else:
                self.temp2 = '300'
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Shelly', self.device_nummer, ip, str(e1)))


class Slavm(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwattread(self) -> None:
        self._watt(self._device_ip, self._device_actor,
                   self._device_username,
                   self._device_password)

    def sepwattread(self) -> Tuple[int, int]:
        self._watt(self._device_measureip,
                   self._device_measureavmactor,
                   self._device_measureavmusername,
                   self._device_measureavmpassword)
        return self.newwatt, self.newwattk

    def _watt(self, ip: str, act: str, user: str, pw: str) -> None:
        argumentList = ['python3', self._prefixpy +
                        'avmhomeautomation/watt.py',
                        str(self.device_nummer), str(ip),
                        '0', '0',
                        act, user, pw]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Avm ', self.device_nummer, ip, str(e1)))


class Sltasmota(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwattread(self) -> None:
        self._watt(self._device_ip)

    def sepwattread(self) -> Tuple[int, int]:
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip: str) -> None:
        argumentList = ['python3', self._prefixpy + 'tasmota/watt.py',
                        str(self.device_nummer), str(ip), '0']
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Tasmota', self.device_nummer, ip, str(e1)))


class Slhttp(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwattread(self) -> None:
        self._watt(self._device_leistungurl, 'none',
                   self._device_stateurl)

    def sepwattread(self) -> Tuple[int, int]:
        self._watt(self._device_measureurl, self._device_measureurlc,
                   'none')
        return self.newwatt, self.newwattk

    def _watt(self, url: str, urlc: str, urls: str) -> None:
        argumentList = ['python3', self._prefixpy + 'http/watt.py',
                        str(self.device_nummer), '0',
                        str(self.devuberschuss), url, urlc,
                        '0', '0', urls]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d Fehlermeldung: %s "
                        % ('http', self.device_nummer, str(e1)))


class Slmystrom(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwattread(self) -> None:
        self._watt(self._device_ip)

    def sepwattread(self) -> Tuple[int, int]:
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip: str) -> None:
        argumentList = ['python3', self._prefixpy + 'mystrom/watt.py',
                        str(self.device_nummer), str(ip), '0']
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
            if (self.device_temperatur_configured > 0):
                self.temp0 = str(answer['temp0'])
                with open(self._basePath+'/ramdisk/device' +
                          str(self.device_nummer) + '_temp0', 'w') as f:
                    f.write(str(self.temp0))
            else:
                self.temp0 = '300'
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Mystrom', self.device_nummer, ip, str(e1)))


class Slsmaem(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        argumentList = ['python3', self._prefixpy + 'smaem/watt.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measuresmaser),
                        str(self._device_measuresmaage)]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('smaem ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slwe514(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        argumentList = ['python3', self._prefixpy + 'we514/watt.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measureid)]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('we514 ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Sljson(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        argumentList = ['python3', self._prefixpy + 'json/watt.py',
                        str(self.device_nummer),
                        self._device_measurejsonurl,
                        self._device_measurejsonpower,
                        self._device_measurejsoncounter]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %s Fehlermeldung: %s "
                        % ('json ', self.device_nummer, str(e1)))
        return self.newwatt, self.newwattk


class Slfronius(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        argumentList = ['python3', self._prefixpy + 'fronius/watt.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measureid)]
        try:
            self.callpro(argumentList)
            answer = self.readret()
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('fronius ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Sllovato(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        try:
            # neu aus openwb 2.0
            with modbus.ModbusTcpClient_(self._device_measureip, self._device_measureportsdm) as tcp_client:
                lov = lovato.Lovato(self._device_measureid, tcp_client)
                _, newwatt = lov.get_power()
                self.newwatt = int(newwatt)
                self.newwattk = 0
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Lovato ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slb23(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        try:
            # neu aus openwb 2.0
            with modbus.ModbusTcpClient_(self._device_measureip, self._device_measureportsdm) as tcp_client:
                b23inst = b23.B23(self._device_measureid, tcp_client)
                # log.warning(" b23inst id %s " % ( str(id(b23inst))))
                _, newwatt = b23inst.get_power()
                self.newwatt = int(newwatt)
                self.newwattk = int(b23inst.get_imported())
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('b23 ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slsdm630(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        try:
            # neu aus openwb 2.0
            with modbus.ModbusTcpClient_(self._device_measureip, self._device_measureportsdm) as tcp_client:
                sdm630 = sdm.Sdm630(self._device_measureid, tcp_client)
                # log.warning(" sdm630 id %s " % ( str(id(sdm630))))
                _, newwatt = sdm630.get_power()
                self.newwatt = int(newwatt)
                self.newwattk = int(sdm630.get_imported())
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Sdm630 ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slsdm120(Slbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def sepwattread(self) -> Tuple[int, int]:
        try:
            # neu aus openwb 2.0
            with modbus.ModbusTcpClient_(self._device_measureip, self._device_measureportsdm) as tcp_client:
                sdm120 = sdm.Sdm120(self._device_measureid, tcp_client)
                _, newwatt = sdm120.get_power()
                self.newwatt = int(newwatt)
                self.newwattk = int(sdm120.get_imported())
        except Exception as e1:
            log.warning("Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Sdm120 ', self.device_nummer,
                           str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk
