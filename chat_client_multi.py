import socket
import sys
import os

numero_port = 8080
adresse = 'localhost'

def lecture_ligne(sock):
    ligne = b''
    while True:
        car = sock.recv(1)
        if not car:
            return b''
        ligne += car
        if car == b'\n':
            return ligne

def boucle_emission(sock):
    print("Tapez vos messages.")
    while True:
        try:
            texte = input("Vous > ")
        except EOFError:
            break
        if texte.strip() == "":
            continue
        try:
            sock.sendall(texte.encode("utf-8") + b"\n")
        except OSError:
            print("\n[Client] Erreur lors de l'envoi, connexion probablement fermée.")
            break

def boucle_reception(sock):
    while True:
        ligne = lecture_ligne(sock)
        if not ligne:
            print("\n[Client] Connexion fermée par le user.")
            break
        message = ligne.decode("utf-8").rstrip("\n")
        print(f"\nUser > {message}")

try:
    adresse_User = socket.gethostbyname(adresse)
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ma_socket.connect((adresse_User, numero_port))
except Exception as e:
    print("Problème de connexion", e.args)
    sys.exit(1)

print("Connecté au serveur de chat.")

pid = os.fork()
if pid == 0:
    boucle_emission(ma_socket)
    ma_socket.close()
    sys.exit(0)
else:
    boucle_reception(ma_socket)
    ma_socket.close()
    sys.exit(0)
