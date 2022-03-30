#!/bin/bash
if [ -e /var/www/html/openWB/openwb.conf.9 ]
	 then cp /var/www/html/openWB/openwb.conf.9 /var/www/html/openWB/openwb.conf.10
fi
if [ -e /var/www/html/openWB/openwb.conf.8 ]
	 then cp /var/www/html/openWB/openwb.conf.8 /var/www/html/openWB/openwb.conf.9
fi
if [ -e /var/www/html/openWB/openwb.conf.7 ]
	 then cp /var/www/html/openWB/openwb.conf.7 /var/www/html/openWB/openwb.conf.8
fi
if [ -e /var/www/html/openWB/openwb.conf.6 ]
	 then cp /var/www/html/openWB/openwb.conf.6 /var/www/html/openWB/openwb.conf.7
fi
if [ -e /var/www/html/openWB/openwb.conf.5 ]
	 then cp /var/www/html/openWB/openwb.conf.5 /var/www/html/openWB/openwb.conf.6
fi
if [ -e /var/www/html/openWB/openwb.conf.4 ]
	 then cp /var/www/html/openWB/openwb.conf.4 /var/www/html/openWB/openwb.conf.5
fi
if [ -e /var/www/html/openWB/openwb.conf.3 ]
	 then cp /var/www/html/openWB/openwb.conf.3 /var/www/html/openWB/openwb.conf.4
fi
if [ -e /var/www/html/openWB/openwb.conf.2 ]
	 then cp /var/www/html/openWB/openwb.conf.2 /var/www/html/openWB/openwb.conf.3
fi
if [ -e /var/www/html/openWB/openwb.conf.1 ]
	 then cp /var/www/html/openWB/openwb.conf.1 /var/www/html/openWB/openwb.conf.2
fi
if [ -e /var/www/html/openWB/openwb.conf ]
	 then cp /var/www/html/openWB/openwb.conf /var/www/html/openWB/openwb.conf.1
fi

sed -i "s,$1.*,$1$2,g" /var/www/html/openWB/openwb.conf
