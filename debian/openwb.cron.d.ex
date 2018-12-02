#
# Regular cron jobs for the openwb package
#
0 4	* * *	root	[ -x /usr/bin/openwb_maintenance ] && /usr/bin/openwb_maintenance
