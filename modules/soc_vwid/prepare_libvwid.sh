echo "downloading libvwid.py  from github to libvwid.org"
curl -sS -o libvwid.org https://raw.githubusercontent.com/skagmo/ha_vwid/main/custom_components/vwid/libvwid.py
sed '
/vehicles/s/status/selectivestatus?jobs=all/
' < libvwid.org > libvwid.mod
diff libvwid.py libvwid.mod
echo "replace libvwid.py by libvwid.mod?(Y)"
read a
if [ "$a" == "Y" ]
then
	mv libvwid.mod libvwid.py
	echo "libvwid.py is replaced by version from github/skagmo"
	chmod +x libvwid.py
else
	echo "libvwid.py is not replaced"
fi

