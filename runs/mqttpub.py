#!/usr/bin/env python3
import re
import sys
import argparse
import os
import paho.mqtt.client as mqtt


def main():
    parser = argparse.ArgumentParser(description='openWB MQTT Publisher')
    parser.add_argument('--qos', '-q', metavar='qos', type=int, help='The QOS setting', default=0)
    parser.add_argument('--retain', '-r', dest='retain', action='store_true', help='If true, retain this publish')
    parser.set_defaults(retain=False)

    args = parser.parse_args()

    client = mqtt.Client("openWB-python-bulkpublisher-" + str(os.getpid()))
    client.connect("localhost")

    for line in sys.stdin:
        m = re.match('(.*)=(.*)', line)
        if m:
            # print("Publishing '%s' :: '%s'" % (m.group(1), m.group(2)))
            client.publish(m.group(1), payload=m.group(2), qos=args.qos, retain=args.retain)

    client.loop(timeout=2.0)
    client.disconnect()


if __name__ == "__main__":
    main()
