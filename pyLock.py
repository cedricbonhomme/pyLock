#! /usr/local/bin/python
#-*- coding: utf-8 -*-

import os
import time
import socket
import hashlib
import operator
import threading

class Serveur(object):
    def __init__(self, portLocal):
        """
        Initialise le socket
        """
        self.host = "127.0.0.1"
        self.port = portLocal
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.settimeout(1)
        self.have_to_stop = threading.Event()
        self.sock.bind((self.host, self.port))

    def receive(self):
        """
        Attend la connexion d'un client.
        """
        while not self.have_to_stop.isSet():
            self.sock.listen(5)
            try:
                self.conn, addr = self.sock.accept()
                self.conn.setblocking(1)

                print 'Connected by', addr
                data = self.conn.recv(1024)
                if not data:
                    break
                print "Donnée reçu :", data
                hashSHA224 = hashlib.sha224()
                hashSHA224.update(str(generateNumber()))

                if data[5:] == hashSHA224.hexdigest():
                    if data[:4] == "open":
                        os.system("/etc/init.d/ssh start")
                        print "SSH lancé ..."
                    elif data[:4] == "clos":
                        os.system("/etc/init.d/ssh stop")
                        print "SSH fermé ..."
                else:
                    print "Mauvaise phrase de passe."

            except socket.timeout:
                pass
        self.sock.close()

    def close(self):
        """
        Déconnexion.
        """
        try:
            self.have_to_stop.set()
            self.sock.close()
        except:
            print "Oups..."

def generatePort():
    """
    Génère un port aléatoirement.
    Basé sur EPOCH (temps passé depuis 1970).
    """
    heure = int(time.strftime("%H", time.localtime()))
    jour = int(time.strftime("%d", time.localtime()))
    nombre_aleatoire = int(time.time() % 8000)
    modulo = nombre_aleatoire % 30
    nombre_aleatoire = abs(nombre_aleatoire - modulo)
    nombre_aleatoire = nombre_aleatoire + reduce(operator.add, [int(nombre) + heure \
                    for nombre in str(abs(nombre_aleatoire - jour))])
    if nombre_aleatoire < 1024:
        nombre_aleatoire = nombre_aleatoire + 1024
    return nombre_aleatoire

def generateNumber():
    """
    Génère un nombre aléatoirement.
    Basé sur EPOCH (temps passé depuis 1970).
    """
    nombre_aleatoire = int(time.time() % 8000)
    modulo = nombre_aleatoire % 5
    nombre_aleatoire = abs(nombre_aleatoire - modulo)
    return nombre_aleatoire + reduce(operator.add, [int(nombre) + 69 \
                    for nombre in str(abs(nombre_aleatoire - 42))])


if __name__ == '__main__':
    while True:
        # génération du port aléatoire
        numero_port = generatePort()
        print "Création serveur sur port", numero_port

        # le firewall autorise la connexion sur le nouveau port
        os.system('./openFireWall.sh '+str(numero_port))

        # ouverture du port et création du socket
        serveur = Serveur(numero_port)
        a = threading.Thread(None, serveur.receive, None,)
        a.setDaemon(True)
        print "Lancement serveur"
        a.start()

        time.sleep(30)

        # fermeture du port
        print "Destruction serveur"
        serveur.close()
        del serveur
        del a

        # réinitialisation du firewall
        os.system('./closeFireWall.sh '+str(numero_port))