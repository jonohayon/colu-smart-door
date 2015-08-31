#! /bin/bash

####################################
# Colu Smart Door Installer Script #
####################################

getScript () {
  curl -O --silent "https://raw.github.com/pypa/pip/master/contrib/get-pip.py"
  python "get-pip.py"
  pip install rpi.gpio
  pip install requests
  pip install pyyaml
  a="http://smartdoor-colu.elasticbeanstalk.com/pi/py"
  curl -o "door.py" --silent $a
  b="http://smartdoor-colu.elasticbeanstalk.com/pi/py2"
  curl -o "test.py" --silent $b
  c=$(pwd)
  d="python $c/test.py"
  echo "while true; do
    $d
done
exit 0" > "/etc/rc.local"
  while true; do
    read -p "What's your Heroku app name (the part in the url between http:// and .herokuapp.com)?  " appname
    case $appname in
      * ) echo "appname: $appname" > "$c/config.yml"; echo "Done! The system is going to reboot..."; reboot; break;;
    esac
  done
}

echo "+--------------------------------------------------+"
echo "| Welcome to the Colu Smart Door Installer Script! |"
echo "+--------------------------------------------------+"
while true; do
  read -p "Would you like to install the scripts to your RPi?  " yn
  case $yn in
    [Yy]* ) echo "Starting the installation process..."; getScript; break;;
    [Nn]* ) echo "Bye Bye!"; break;;
    * ) echo "Please answer yes (y) or no (n)";;
  esac
done
