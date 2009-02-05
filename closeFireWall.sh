#!/bin/sh

# Efface les regles concernant le port fourni en parametre
cat /home/cdjs/pyLock/iptable.sh | grep -v $1 > /home/cdjs/pyLock/tmp
cat /home/cdjs/pyLock/tmp > /home/cdjs/pyLock/iptable.sh

rm -f /home/cdjs/pyLock/tmp

# Reinitialise le firewall
iptables -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
