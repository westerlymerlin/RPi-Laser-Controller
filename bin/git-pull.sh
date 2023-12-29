#!/bin/bash

# Script to pull the master branch from github
echo "
**** pulling the master branch from github ****
"
cd ~/github/UCL-Laser-Controller/
git pull origin master
cd ~

echo "
******** git pull completed ********
"
