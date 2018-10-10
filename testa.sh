#!/bin/bash


if [ $(dpkg-query -W -f='${Status}' php-gd 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	  sudo apt-get install 
fi





