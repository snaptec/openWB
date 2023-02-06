OPENWBBASEDIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

while read -r x; do
	value="${x#*=}"
	if [[ "${value:0:1}" == "'" ]] ; then
		value="${value:1:-1}"
		key="${x%%=*}"
		export "$key=$value"
	else
		export "$x"
	fi
done < "$OPENWBBASEDIR/openwb.conf"
