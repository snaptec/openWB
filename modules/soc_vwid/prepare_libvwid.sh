echo "downloading libvwid.py  from github to libvwid.org"
curl -sS -o libvwid.org https://raw.githubusercontent.com/skagmo/ha_vwid/main/custom_components/vwid/libvwid.py
# replace f-strings, not supported on stretch/python 3.5
sed '
/status_url =/s/status_url.*$/status_url = API_BASE + "\/vehicles\/" + self.vin + "\/selectivestatus?jobs=" + self.jobs_string/
/(f"/s/({/("+str(/
/(f"/s/})/)+")/
/(f"/s/(f"/("/
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

