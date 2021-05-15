#!/usr/bin/python
import sys
import os
import time
import getopt

watt2 = int(sys.argv[1])
pref = str(sys.argv[2])
importfn = str(sys.argv[3])
exportfn = str(sys.argv[4])

# emulate import  export
seconds2= time.time()
watt1=0
seconds1=0.0
if os.path.isfile('/var/www/html/openWB/ramdisk/'+pref+'sec0'): 
    f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'r')
    seconds1=float(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'r')
    watt1=int(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0pos', 'r')
    wattposh=int(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0neg', 'r')
    wattnegh=int(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'w')
    value1 = "%22.6f" % seconds2
    f.write(str(value1))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'w')
    f.write(str(watt2))
    f.close()
    seconds1=seconds1+1
    deltasec = seconds2- seconds1
    deltasectrun =int(deltasec* 1000) / 1000
    stepsize = int((watt2-watt1)/deltasec)
    while seconds1 <= seconds2:
        if watt1 < 0:
            wattnegh= wattnegh + watt1
        else:
            wattposh= wattposh + watt1
        watt1 = watt1 + stepsize
        if stepsize < 0:
            watt1 = max(watt1,watt2)
        else:
            watt1 = min(watt1,watt2)
        seconds1= seconds1 +1
    rest= deltasec - deltasectrun
    seconds1= seconds1  - 1 + rest
    if rest > 0:
        watt1 = int(watt1 * rest)
        if watt1 < 0:
            wattnegh= wattnegh + watt1
        else:
            wattposh= wattposh + watt1
    wattposkh=wattposh/3600
    wattnegkh=(wattnegh*-1)/3600
    f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0pos', 'w')
    f.write(str(wattposh))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0neg', 'w')
    f.write(str(wattnegh))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+ importfn,'w')
    f.write(str(wattposkh))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/' +exportfn , 'w')
    f.write(str(wattnegkh))
    f.close()
else: 
    f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'w')
    value1 = "%22.6f" % seconds2
    f.write(str(value1))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'w')
    f.write(str(watt2))
    f.close()
  
