import socket, sys, os

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
    while True:
        try:
            texte = input("\nClient > ")
        except EOFError:
            break

        if not texte:
            break
        sock.sendall(texte.encode('UTF-8') + b'\n')

def boucle_reception(sock):
    while True:
        ligne = lecture_ligne(sock)
        if not ligne:
            print("\n[Client] Connexion fermée par le serveur.")
            break
        print("\nServeur >", ligne.decode('UTF-8'), end='')

try:
    adresse_serveur = socket.gethostbyname(adresse)  # requête DNS
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ma_socket.connect((adresse_serveur, numero_port))
except Exception as e:
    print("Probleme de connexion", e.args)
    sys.exit(1)

print("Connecté au serveur de chat. Tapez vos messages.")

pid = os.fork()
if pid == 0:
    boucle_emission(ma_socket)
    ma_socket.close()
    sys.exit(0)
else:
    boucle_reception(ma_socket)
    ma_socket.close()
