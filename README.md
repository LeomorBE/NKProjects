# Écran d'affichage des départs de trains de la SNCF

## Concept
Lorsque je me déplacais en train, je me suis souvent embêter à rechercher la référence d'un train sur l'application de la SNCF, de plus j'ai toujours voulu avoir une affichage des trains/bus en temps réel. C'est pour cela que j'ai voulu recréer cet écran d'affichage.

## Spécification
Ce projet tourne sous un python3.10 ou plus (car certaines parties/concepts inclu dans cette version de python sont utilisés).

Les modules utilisés sont:
- PyQt5
- requests

Pour pouvoir l'utiliser, vous devez être en possession d'une clé API fourni par la SNCF (gratuit pour les particuliers) et mettre dans le module threadSNCF.py, ajouter la clé à la ligne 8 de la classe SNCFDepartures()

## Author
*Mora Leonardo Rafael*
This code is open for everyone **ONLY** for non commercial usage.
