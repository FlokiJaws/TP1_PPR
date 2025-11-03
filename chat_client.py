import socket, sys

numero_port = 8080
adresse = 'localhost'

try:
    adresse_serveur = socket.gethostbyname(adresse) # réalise une requête DNS
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ma_socket.connect((adresse_serveur, numero_port))
except Exception as e:
    print("Probleme de connexion", e.args)
    sys.exit(1)

print("Connecté au serveur de chat. Tapez vos messages.")

def lecture_ligne(sock):
    ligne = b""
    while True:
        car = sock.recv(1)
        if not car: break
        ligne += car
        if car == b'\n': break
    return ligne

while 1:
    entree_clavier = input("Client> ")
    if not entree_clavier:
        break

    ma_socket.sendall(bytes(entree_clavier, encoding='UTF-8') + b'\n')
    
    reponse_serveur = lecture_ligne(ma_socket)
    if not reponse_serveur:
        print("Connexion fermée par le serveur.")
        break

    print("Serveur >", reponse_serveur.decode('UTF-8'), end='')

ma_socket.close()

