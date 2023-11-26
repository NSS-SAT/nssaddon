#!/bin/sh
##DESCRIPTION=This script downloads latest CCcam keys & provider info.
#channelinfo="http://www.lokumsat.esy.es/CaMs-EmU/CCcam.channelinfo"
#prio="http://www.lokumsat.esy.es/CaMs-EmU/CCcam.prio"
#providers="http://www.lokumsat.esy.es/CaMs-EmU/CCcam.providers"
softcam="https://raw.githubusercontent.com/pablitodrito/prova-pablito/master/SoftCam.Key"
#autoroll="http://depo.dreamosat-forum.com/CaMs-EmU/CCcam/AutoRoll.Key"
#vubiss="http://www.lokumsat.esy.es/CaMs-EmU/SoftCam.Key"
#oscam="http://www.lokumsat.esy.es/CaMs-EmU/oscam.keys"
#wicard="http://onlinecolor.ml/keys/SoftCam.Key"
#ee="http://onlinecolor.ml/center/ee.bin"
#ee36="http://onlinecolor.ml/center/ee.bin"
#ee56="http://onlinecolor.ml/sibir/ee.bin"
#autokeysbylokum="http://www.lokumsat.esy.es/CaMs-EmU/autokeysbylokum.sh"
# SoftcamKeys="http://sat-linux.com/addons/SoftCam.Key"
# Constant="http://sat-linux.com/addons/constant.cw"
KeysUpdater="http://levi45.spdns.eu/Addons/Multicam/Keys_Updater.sh"
SoftcamKeys="http://levi45.spdns.eu/Addons/SoftCam.Key"
Constantcw="http://levi45.spdns.eu/Addons/constant.cw"
OscamKeys="http://levi45.spdns.eu/Addons/oscam.keys"
Oscamconstantcw="http://levi45.spdns.eu/Addons/oscam.constant.cw"
echo ""
echo ""
# echo "Downloading ${KeysUpdater}"
# wget ${KeysUpdater} -O /usr/lib/enigma2/python/Plugins/Extensions/Manager/emu/Keys_Updater.sh || echo "Error: Couldn't connect to ${KeysUpdater}"
# echo ""
# chmod 775 /usr/lib/enigma2/python/Plugins/Extensions/Manager/emu/Keys_Updater.sh
# echo ""
echo "Downloading ${SoftcamKeys}"
wget ${SoftcamKeys} -O /usr/keys/SoftCam.Key || echo "Error: Couldn't connect to ${SoftcamKeys}"
echo ""
echo "Downloading ${SoftcamKeys}"
wget ${SoftcamKeys} -O /etc/tuxbox/config/SoftCam.Key || echo "Error: Couldn't connect to ${SoftcamKeys}"
echo ""
echo "Downloading ${Constantcw}"
wget ${Constantcw} -O /etc/tuxbox/config/constant.cw || echo "Error: Couldn't connect to ${Constantcw}"
echo ""
echo "Downloading ${Constantcw}"
wget ${Constantcw} -O /usr/keys/constant.cw || echo "Error: Couldn't connect to ${Constantcw}"
echo ""
echo "Downloading ${OscamKeys}"
wget ${OscamKeys} -O /etc/tuxbox/config/oscam.keys || echo "Error: Couldn't connect to ${OscamKeys}"
echo ""
echo "Downloading ${Oscamconstantcw}"
wget ${Oscamconstantcw} -O /etc/tuxbox/config/oscam.constant.cw || echo "Error: Couldn't connect to ${Oscamconstantcw}"
echo ""
echo ""
echo ""
# echo "Downloading ${softcam}"
# # wget ${softcam} -O /etc/tuxbox/config/SoftCam.Key || echo "Error: Couldn't connect to ${softcam}"
# wget ${softcam} -O /usr/keys/SoftCam.Key || echo "Error: Couldn't connect to ${softcam}"
echo ""

echo ""
echo "* Installed Successfully *"
echo "* E2 Restart Is Required *"
KeyDate=`/bin/date -r /usr/keys/SoftCam.Key +%d.%m.%y-%H:%M:%S`
	echo ""
	echo "DATA E ORA AGGIORNAMENTO: $KeyDate"
	echo ""
exit 0

wget https://raw.githubusercontent.com/pablitodrito/prova-pablito/master/SoftCam.Key -O /usr/keys/SoftCam.Key