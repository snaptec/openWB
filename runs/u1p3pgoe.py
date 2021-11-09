#!/usr/bin/python
import requests
import sys
import os
import time
import argparse
import traceback

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", required=True, type=str, help="ip address")
parser.add_argument("-p", "--phases", required=True, type=int, choices=[1, 3], help="phases to activate")
parser.add_argument("-m", "--minampere", required=False, type=int, help="minimum ampere")
parser.add_argument("-v", "--verbose", required=False, action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("Go-e mit IP %s Umschaltung auf %d Phasen" % (args.address, args.phases))

try:
    status_goe = requests.get('http://'+args.address+'/status', timeout=5).json()
except requests.exceptions.ConnectionError:
        print("Connection to go-e failed")
        exit(1)

if(args.verbose):
    try:
        print("go-e serial number: %s" % (status_goe['sse']))
    except KeyError:
        traceback.print_exc()
        exit(1)

# check whether fsp param exists => go-e charger has HW V3 and therefore 1to3 phase switch capability
if ( "fsp" in status_goe):
	try:
		if(args.verbose):
			print  ("Phaseneinstellung fsp vorher: %d"%(int(status_goe['fsp'])))
		if ( args.phases == 1 and int(status_goe['fsp']) != 1):
			set_fsp_goe = requests.get('http://'+args.address+'/mqtt?payload=fsp=1', timeout = 5).json()
			#Using API V2 the respective call would be /api/set?psm=1
			if (int(set_fsp_goe['fsp']) == 1 and args.verbose):
				print ("Umschaltung auf 1 Phase erfolgreich: fsp=%d"%(int(set_fsp_goe['fsp'])))
		if ( args.phases == 3 and int(status_goe['fsp']) != 0 ):
			if (args.minampere and args.minampere >= 5 and args.minampere <= 32):
				set_amx_goe = requests.get('http://'+args.address+'/mqtt?payload=amx='+str(args.minampere), timeout = 5).json()
				#Using API V2 the respective call would be /api/set?ama=args.minampere
				if (int(set_amx_goe['amx']) == args.minampere and args.verbose):
					print ("Setzen von MinAmpere erfolgreich: amx=%d"%(int(set_amx_goe['amx'])))
			set_fsp_goe = requests.get('http://'+args.address+'/mqtt?payload=fsp=0', timeout = 5).json()
			#Using API V2 the respective call would be /api/set?psm=2
			if (int(set_fsp_goe['fsp']) == 0 and args.verbose):
				print ("Umschaltung auf 3 Phasen erfolgreich: fsp=%d"%(int(set_fsp_goe['fsp'])))
	except:
		traceback.print_exc()
		exit(1)
else :
	if(args.verbose):
		print ("Phasenumschaltung von go-e Charger nicht unterstuetzt (V2 HW ?!)")