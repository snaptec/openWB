sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/openwb.key -out /etc/ssl/certs/openwb.crt -subj ''/CN=$1/O=OpenWB/C=DE''
