declare -r PersitedStatusDestination="/var/www/html/openWB/web/logging/data/persistedStatus"
declare -r -i NumberOfPersistedCps=8

# store volatile (ramdisk) data at a temporary, persistent location
persistStatus() {

	mkdir -p ${PersitedStatusDestination}

	echo "Persisting status for ${NumberOfPersistedCps} to '${PersitedStatusDestination}: Starting"

	for ((currentCp=1; currentCp<=NumberOfPersistedCps; currentCp++)); do

		cp -v "/var/www/html/openWB/ramdisk/lp${currentCp}enabled" "${PersitedStatusDestination}"
		cp -v "/var/www/html/openWB/ramdisk/lp${currentCp}phasen" "${PersitedStatusDestination}"
		cp -v "/var/www/html/openWB/ramdisk/lp${currentCp}sofortll" "${PersitedStatusDestination}"

	done

	echo "Persisting status for ${NumberOfPersistedCps} to '${PersitedStatusDestination}: Done"

	exit 0
}

restorePersistedStatusOrDefaults() {

	echo "Restoring persisted stati for ${NumberOfPersistedCps} to '${PersitedStatusDestination}: Starting"

	for ((currentCp=1; currentCp<=NumberOfPersistedCps; currentCp++)); do

		restoreIfExistsOrSetValue "${PersitedStatusDestination}/lp${currentCp}enabled" "/var/www/html/openWB/ramdisk/lp${currentCp}enabled" 1
		restoreIfExistsOrSetValue "${PersitedStatusDestination}/lp${currentCp}phasen" "/var/www/html/openWB/ramdisk/lp${currentCp}phasen" 0
		restoreIfExistsOrSetValue "${PersitedStatusDestination}/lp${currentCp}sofortll" "/var/www/html/openWB/ramdisk/lp${currentCp}sofortll" 10

	done

	echo "Restoring persisted stati for ${NumberOfPersistedCps} to '${PersitedStatusDestination}: Done"
}

restoreIfExistsOrSetValue() {

	local persitedValueFile="$1"
	local volatileDestination="$2"
	local defaultValue="$3"

    if [ -f "${persitedValueFile}" ]; then
		echo "Restoring '${persitedValueFile}' to '${volatileDestination}'"
		mv -v "${persitedValueFile}" "${volatileDestination}"
	else
		echo "No persisted value for '${volatileDestination}', setting default '${defaultValue}'"
		echo $defaultValue > "${volatileDestination}"
	fi
}
