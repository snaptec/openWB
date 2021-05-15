#!/bin/bash
echo "****************************************"
echo "Step 1: moving file to home directory..."
sudo cp /var/www/html/openWB/web/tools/upload/backup.tar.gz /home/pi/backup.tar.gz
cd /home/pi/
echo "****************************************"
echo "Step 2: extracting archive..."
sudo tar -vxf backup.tar.gz
echo "****************************************"
echo "Step 3: replacing old files..."
sudo cp -v -R /home/pi/var/www/html/openWB/* /var/www/html/openWB/
sudo chmod 777 /var/www/html/openWB/openwb.conf
echo "****************************************"
echo "Step 4: cleanup after restore..."
sudo rm /var/www/html/openWB/web/tools/upload/backup.tar.gz
sudo rm /home/pi/backup.tar.gz
sudo rm -R /home/pi/var
echo "****************************************"
echo "End: Restore finished."
echo "****************************************"
