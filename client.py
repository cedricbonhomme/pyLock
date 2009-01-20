#! /usr/local/bin/python
#-*- coding: utf_8 -*-
import socket
import time, hashlib
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
    nombre_aleatoire = int(time.time() % 8000)
    modulo = nombre_aleatoire % 30
    nombre_aleatoire = abs(nombre_aleatoire - modulo)
    nombre_aleatoire = nombre_aleatoire + reduce(operator.add, [int(nombre) + 42 \
                    for nombre in str(nombre_aleatoire - 32)])
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
    return nombre_aleatoire + reduce(operator.add, [int(nombre) + 69 for nombre in str(nombre_aleatoire - 42)])


if __name__ == '__main__':
    adresse = '127.0.0.1'
    port = generatePort()
    print "Tentative de connexion sur :", (adresse, port)
    client = Client(adresse, port)

    # génération du mot de passe pseudo-aléatoire
    hashMD5 = hashlib.md5()
    hashMD5.update(str(generateNumber()))
    data = hashMD5.hexdigest()

    #data = "open:"+data # demande l'ouverture du port ssh
    data = "clos:"+data # demande la fermeture du port ssh

    print "Envoie de", data
    client.send(data) # envoie la demande
