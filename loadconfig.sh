while read -r x; do
	value="${x#*=}"
	if [[ "${value:0:1}" == "'" ]] ; then
		value="${value:1:-1}"
		key="${x%%=*}"
		export "$key=$value"
	else
		export "$x"
	fi
done < /var/www/html/openWB/openwb.conf
