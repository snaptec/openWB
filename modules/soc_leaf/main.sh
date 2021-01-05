#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
        username=$leafusernames1
        password=$leafpassworts1
		;;
	*)
		# defaults to first charge point for backward compatibility
		username=$leafusername
        password=$leafpasswort
        ;;
esac

sudo python /var/www/html/openWB/modules/soc_leaf/soc.py $username $password
