#!/bin/bash

# Script to pull the master branch from github
echo "
**** pulling the master branch from github ****
"
mkdir ~/rpi.lgpio
cd ~/rpi.lgpio/
wget http://abyz.me.uk/lg/lg.zip
unzip lg.zip
cd ~/rpi.lgpio/lg
make
sudo make install
echo "**** lg-rpigpio ready for python - use PIP install rpi-lgpio ****

