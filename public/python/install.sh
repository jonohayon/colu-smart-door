#! /bin/bash

####################################
# Colu Smart Door Installer Script #
####################################

getScript () {
  a="http://smart-door.herokuapp.com/pi/py"
  wget $a -O "door.py"
  b="http://smart-door.herokuapp.com/pi/py2"
  wget $b -O "test.py"
  c=$(pwd)
  d="python $c/test.py"
  echo "while true; do\n
  $d\n
done
exit 0" > "/etc/rc.local"
}

installScript () {
  while true; do
    read -p "What is your server's URL (for getting the scripts)?  " url
    case $url in
      * ) getScript "$url"; break;;
    esac
  done
}

echo "Welcome to the Colu Smart Door Installer Script!"
while true; do
  read -p "Would you like to install the scripts to your RPi?  " yn
  case $yn in
    [Yy]* ) echo "Installing..."; installScript; break;;
    [Nn]* ) echo "Bye Bye!"; break;;
    * ) echo "Please answer yes (y) or no (n)";;
  esac
done
