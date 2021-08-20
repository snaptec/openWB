#!/bin/bash
if [[ $alphav123 == "1" ]]; then
	python /var/www/html/openWB/modules/wr_alphaess/readv123.py
else
	python /var/www/html/openWB/modules/wr_alphaess/readalpha.py
fi
