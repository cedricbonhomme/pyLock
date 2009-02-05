#!/bin/sh

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp -i eth0 --dport ssh -j ACCEPT
iptables -A INPUT -p tcp -i eth0 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -i eth0 --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp -o eth0 --sport ssh -j ACCEPT
iptables -A OUTPUT -p tcp -o eth0 --sport 80 -j ACCEPT
iptables -A OUTPUT -p tcp -o eth0 --sport 443 -j ACCEPT

iptables -A OUTPUT -p udp -o eth0 --dport 123 -j ACCEPT
iptables -A INPUT -p udp -i eth0 --sport 123 -j ACCEPT

iptables -A OUTPUT -p tcp -o eth0 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -i eth0 --sport 80 -j ACCEPT

iptables -A OUTPUT -p udp -o eth0 --dport 53 -j ACCEPT

iptables -I INPUT 2 -i lo -j ACCEPT
iptables -I OUTPUT 2 -o lo -j ACCEPT

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
