import json
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock

import discovergy


class TestDiscovergy(unittest.TestCase):
    SAMPLE_JSON = """{
        "time":1622132613773,
        "values":{
            "energyOut":25545649812000,
            "energy2":12593551340000,
            "energy1":2210138000,
            "voltage1":233400,
            "voltage2":234600,
            "voltage3":100000,
            "energyOut1":0,
            "energyOut2":0,
            "power":1234567,
            "power1":1167000,
            "power2":2650980,
            "power3":-230000,
            "energy":12595761479000
        }
    }"""

    @patch('discovergy.write_to_ramdisk_file')
    @patch('discovergy.try_get_last_reading')
    @patch('discovergy.log')
    def test_update(self: TestCase,
                    _: MagicMock,
                    get_last_reading_mock: MagicMock,
                    write_to_ramdisk_file_mock: MagicMock):
        # setup
        get_last_reading_mock.return_value = json.loads(TestDiscovergy.SAMPLE_JSON)

        # exeuction
        discovergy.update("someUser", "somePassword", "someMeterId")

        # evaluation
        get_last_reading_mock.assert_called_once_with("someUser", "somePassword", "someMeterId")

        write_to_ramdisk_file_mock.assert_any_call("bezuga1", "5")
        write_to_ramdisk_file_mock.assert_any_call("bezuga2", "11")
        write_to_ramdisk_file_mock.assert_any_call("bezuga3", "-1")
        write_to_ramdisk_file_mock.assert_any_call("bezugkwh", "1259576")
        write_to_ramdisk_file_mock.assert_any_call("bezugw1", "1167")
        write_to_ramdisk_file_mock.assert_any_call("bezugw2", "2651")
        write_to_ramdisk_file_mock.assert_any_call("bezugw3", "-230")
        write_to_ramdisk_file_mock.assert_any_call("einspeisungkwh", "2554565")
        write_to_ramdisk_file_mock.assert_any_call("evuv1", "233")
        write_to_ramdisk_file_mock.assert_any_call("evuv2", "235")
        write_to_ramdisk_file_mock.assert_any_call("evuv3", "100")
        write_to_ramdisk_file_mock.assert_any_call("wattbezug", "1235")

    @patch('discovergy.write_to_ramdisk_file')
    @patch('discovergy.try_get_last_reading')
    @patch('discovergy.log')
    def test_update_handles_fetch_error(self: TestCase,
                                        log_mock: MagicMock,
                                        get_last_reading_mock: MagicMock,
                                        write_to_ramdisk_file_mock: MagicMock):
        # setup
        get_last_reading_mock.side_effect = Exception("some error message")

        # execution
        try:
            discovergy.update("someUser", "somePassword", "someMeterId")
        except:
            pass
        else:
            self.fail("expected exception not raised")

        # evaluation
        write_to_ramdisk_file_mock.assert_not_called()
        log_mock.assert_called_once_with("Getting last readings failed: some error message")


if __name__ == '__main__':
    unittest.main()
