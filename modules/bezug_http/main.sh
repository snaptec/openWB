#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_http/read_http.py $bezug_http_w_url $bezug_http_ikwh_url $bezug_http_ekwh_url $bezug_http_l1_url $bezug_http_l2_url $bezug_http_l3_url
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
