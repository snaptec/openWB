Die python library libvwid.py dient als Basis und wird hier gepflegt:
https://github.com/skagmo/ha_vwid/blob/main/custom_components/vwid/libvwid.py

Folgende software wird zusätzlich benötigt, diese werden in runs/atreboot.sh installiert:
sudo pip3 install lxml
sudo pip3 install aiohttp
sudo apt-get install libxslt-dev

secrets.py: ist ab Python 3.6 enthalten, daher in stretch mit Python 3.5 normalerweise nicht vorhanden.
soc_vwid enthält eine Kopie als _secrets.py, diese wird benutzt, wenn es die offizielle secrets.py nicht existiert.
