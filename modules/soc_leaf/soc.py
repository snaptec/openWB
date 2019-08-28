#!/usr/bin/env
import sys
import time


leaftimer = open('/var/www/html/openWB/ramdisk/soctimer', 'r')
leaftimer = int(leaftimer.read())
thecommand=str('python3 /var/www/html/openWB/modules/soc_leaf/getsoc.py')
thestring=str( sys.argv[1] + ' ' + sys.argv[2] + ' &') 
if ( leaftimer < 181 ):
    leaftimer += 1
    f = open('/var/www/html/openWB/ramdisk/soctimer', 'w')
    f.write(str(leaftimer))
    f.close()
    if ( leaftimer == 10 ):
        from subprocess import call
        exit_code = call(thecommand + ' ' + thestring, shell=True)
    if ( leaftimer == 60 ):
        from subprocess import call
        exit_code = call(thecommand + ' ' + thestring, shell=True)


else:
    f = open('/var/www/html/openWB/ramdisk/soctimer', 'w')
    f.write(str(0))
    f.close()
    from subprocess import call
    exit_code = call(thecommand + ' ' + thestring, shell=True)


    
    


