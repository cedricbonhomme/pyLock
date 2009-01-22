#!/bin/sh

# Efface les regles concernant le port fourni en parametre
cat iptable | grep -v $1 > tmp
cat tmp > iptable

# Reinitialise le firewall
iptables -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

exit 0