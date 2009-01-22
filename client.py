#! /usr/local/bin/python
#-*- coding: utf_8 -*-

import sys
import time
import socket
import hashlib
import operator
import threading

class Client(object):
    def __init__(self, adresseDistante, portDistant):
        self.adresseDistante = adresseDistante
        self.portDistant = portDistant
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.adresseDistante, self.portDistant))

        self.lecture = threading.Thread(None, self.receive)
        self.lecture.setDaemon(True)
        self.lecture.start()
        #self.lecture.join()

    def receive(self):
        data = self.sock.recv(1024)

    def send(self, message):

        self.sock.send(message)
        #s.close()
        #print 'Received', repr(data)

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
    return nombre_aleatoire + reduce(operator.add, [int(nombre) + 69 for nombre in str(abs(nombre_aleatoire - 42))])


if __name__ == '__main__':
    # Point d'entrée en exécution.
    if len(sys.argv) > 2:
        adresse, action = str(sys.argv[1]), str(sys.argv[2])
    elif len(sys.argv) == 2:
        adresse, action = '127.0.0.1', str(sys.argv[1])
    else:
        print "Usage : python2.5 " + sys.argv[0] + " adresseIP [open|clos]"
        exit(1)

    port = generatePort()
    print "Tentative de connexion sur :", (adresse, port)
    client = Client(adresse, port)

    # génération du mot de passe pseudo-aléatoire
    hashSHA224 = hashlib.sha224()
    hashSHA224.update(str(generateNumber()))
    data = hashSHA224.hexdigest()

    data = action+":"+data # demande l'ouverture/fermeture du port ssh

    print "Envoie de", data
    client.send(data) # envoie la demande