#!/bin/bash

python3 /var/www/html/openWB/modules/speicher_http/read_http.py "${speichersoc_http}" "${speicherleistung_http}" "${speicherikwh_http}" "${speicherekwh_http}"
