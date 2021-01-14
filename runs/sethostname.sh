#!/bin/sh

newHostname=$1
echo "Changing hostname to $newHostname..."
touch /tmp/tmphostname
echo $newHostname > /tmp/tmphostname
mv /tmp/tmphostname /etc/hostname
sed -i "s/127.0.1.1.*/127.0.1.1    $newHostname/" /etc/hosts
echo "done"
