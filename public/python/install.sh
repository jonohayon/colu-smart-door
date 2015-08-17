####################################
# Colu Smart Door Installer Script #
####################################

formatWifiTxt () {
	ssid=$(awk '/ESSID: */' scan.txt)
	arr=$(echo $ssid | tr ':' '\n')
	for x in $arr; do
		if [ "$x" != "ESSID" ]; then
			l=${#x}
			length=$((l = $l - 1))
			finished=${x:1:length}
			echo $length
		fi
	done
}

setupWifi () {
	sudo iwlist wlan0 scan > scan.txt
	formatWifiTxt
}

installScript () {
	setupWifi
}

echo "Welcome to the Colu Smart Door Installer Script!"
while true; do
  read -p "Would you like to install the scripts to your RPi?  " yn
  case $yn in
    [Yy]* ) echo "Installing..."; installScript;;
    [Nn]* ) echo "Bye Bye!"; break;;
    * ) echo "Please answer yes (y) or no (n)";;
  esac
done
