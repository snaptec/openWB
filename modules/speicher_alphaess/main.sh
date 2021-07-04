#!/bin/bash
if [[ $alphav123 == "1" ]]; then
	python /var/www/html/openWB/modules/speicher_alphaess/readv123.py
else
	python /var/www/html/openWB/modules/speicher_alphaess/readalpha.py
fi
