import os,socket,sys


adresse_serveur = socket.gethostbyname('localhost') # réalise une requête DNS
numero_port = 8080
ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    ma_socket.connect((adresse_serveur, numero_port))
except Exception as e:
    print ("Probleme de connexion", e.args)
sys.exit(1)

while 1:
    ligne = ma_socket.recv(1024) # réception d'au plus 1024 caracteres
    if not ligne:
        break
    print (ligne)
ma_socket.close()