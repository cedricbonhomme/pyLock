#!/bin/sh


# Ajoute l'ouverture en entree vers le port aleatoire fourni en parametre
# Remarque : aucune regle n'est donne en output, car la serrure ne repond pas au client
echo "iptables -A INPUT -p tcp -i eth0 --dport $1 -j ACCEPT" >> /home/cdjs/pyLock/iptable.sh
echo "iptables -A OUTPUT -p tcp -o eth0 --sport $1 -j ACCEPT" >> /home/cdjs/pyLock/iptable.sh
