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
parser.add_argument("-v", "--verbose", required=False, action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("Go-e mit IP %s Umschaltung auf %d Phasen"%(args.address, args.phases))
	
status_goe = requests.get('http://'+args.address+'/status', timeout = 5).json()	
if(args.verbose):
	try:
		print  ("go-e serial number: %s"%(status_goe['sse']))
	except:
		traceback.print_exc()
		exit(1)

if ( "fsp" in status_goe):
	try:
		if(args.verbose):
			print  ("fsp before: %d"%(int(status_goe['fsp'])))
	except:
		traceback.print_exc()
		exit(1)
	if ( args.phases == 1 ):
		set_fsp_goe = requests.get('http://'+args.address+'/mqtt?payload=fsp=0', timeout = 5).json()
		try: 
			if (int(set_fsp_goe['fsp']) == 0 and args.verbose):
				print ("Switch to 1Phase succeeded: fsp=%d"%(int(set_fsp_goe['fsp'])))
		except:
			traceback.print_exc()
			exit(1)
	if ( args.phases == 3 ):
		set_fsp_goe = requests.get('http://'+args.address+'/mqtt?payload=fsp=1', timeout = 5).json()
		try:
			if (int(set_fsp_goe['fsp']) == 1 and args.verbose):
				print ("Switch to 3Phases succeeded: fsp=%d"%(int(set_fsp_goe['fsp'])))
		except:
			traceback.print_exc()
			exit(1)