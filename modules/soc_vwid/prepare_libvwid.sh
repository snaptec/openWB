echo "downloading libvwid.py  from github to libvwid.org"
curl -sS -o libvwid.org https://raw.githubusercontent.com/skagmo/ha_vwid/main/custom_components/vwid/libvwid.py
diff libvwid.py libvwid.org
echo "replace libvwid.py by libvwid.mod?(Y)"
read a
if [ "$a" == "Y" ]
then
	mv libvwid.org libvwid.py
	echo "libvwid.py is replaced by version from github/skagmo"
	chmod +x libvwid.py
else
	echo "libvwid.py is not replaced"
fi

