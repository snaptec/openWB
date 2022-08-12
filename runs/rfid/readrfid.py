#!/usr/bin/env python3
import evdev
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device", type=str, required=True, help="device to bind to")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

input_device = evdev.InputDevice("/dev/input/" + args.device)

scan_codes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

key_string = ""
for event in input_device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)
        if data.keystate == 1:
            key_lookup = scan_codes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)
            key_string += str(format(key_lookup))
            if "CRLF" in key_string:
                key_string = key_string[:-4]
                if(args.verbose):
                    print(key_string)
                with open('/var/www/html/openWB/ramdisk/readtag', 'w') as tag_file:
                    tag_file.write(key_string)
                key_string = ""
