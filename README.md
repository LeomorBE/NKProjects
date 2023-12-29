# Écran d'affichage des départs de trains de la SNCF

## Concept
Lorsque je me déplacais en train, je me suis souvent embêter à rechercher la référence d'un train sur l'application de la SNCF, de plus j'ai toujours voulu avoir une affichage des trains/bus en temps réel. C'est pour cela que j'ai voulu recréer cet écran d'affichage.
Ce projet a été testé avec un Raspberry pi 3B+ équipé de l'iso Raspbian Bookworm, d'un écran 4.3 pouces. Le projet est en Python avec l'utilisation du Framework PyQt5.

## Spécification
Ce projet tourne sous un python3.10 ou plus (car certaines parties/concepts inclu dans cette version de python sont utilisés).

Les modules utilisés sont:
- PyQt5 (Framework)
- requests
- PyCryptodome

Pour pouvoir l'utiliser, vous devez être en possession d'une clé API fourni par la SNCF (gratuit pour les particuliers) et mettre dans le module threadSNCF.py, ajouter la clé à la ligne 8 de la classe SNCFDepartures()

## Configuration Raspberry pi
Utilisation de l'iso Rasbian Bookworm recommendé (ou bien nécessite Python3.10 minimum).
Avec Bookworm il faudra utiliser `apt-get install python-pycryptodome` qui installera une ancienne version (dans le code il faudra utiliser Cryptodome au lien de Crypto).

`sudo apt-get install build-essential`
`sudo apt-get install python3-pyqt5`
`sudo apt-get install pyqt5-dev pyqt5-dev-tools`
`sudo apt-get install build-essential`
`sudo apt-get install qt5-qmake`
`sudo apt-get install qtcreate`
`sudo apt-get install qtbase5-examples`
`sudo apt-get install libfontconfig1-dev libdbus-1-dev libfreetype6-dev libicu-dev libudev-dev libinput-dev libxkbcommon-dev libssl-dev libpng-dev libjpeg-dev libglib2.0-dev libraspberrypi-dev`
`sudo apt-get install bluez libbluetooth-dev`
`sudo apt-get install --reinstall libxcb-xinerama0`

## Author
*Mora Leonardo Rafael*
This code is open for everyone **ONLY** for non commercial usage.
