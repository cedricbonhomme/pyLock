#!/bin/sh

# Ajoute l'ouverture en entree vers le port aleatoire fourni en parametre
# Remarque : aucune regle n'est donne en output, car la serrure ne repond pas au client
echo "iptables -A INPUT -p tcp -i eth0 --dport $1 -j ACCEPT" >> iptable
