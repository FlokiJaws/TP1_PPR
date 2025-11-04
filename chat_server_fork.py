import socket, sys, os

numero_port_serveur = 8080
masque_acces = ''   # '' = toutes les interfaces

def lecture_ligne(sock):
    ligne = b''
    while True:
        car = sock.recv(1)
        if not car:
            return b''
        ligne += car
        if car == b'\n':
            return ligne

def boucle_reception(sock):
    while True:
        ligne = lecture_ligne(sock)
        if not ligne:
            print("\n[Serveur] Connexion fermée par le client.")
            break
        print("\nClient > ", ligne.decode('UTF-8'), end='')

def boucle_emission(sock):
    while True:
        try:
            texte = input("\nServeur > ")
        except EOFError:
            break

        if not texte:
            break

        sock.sendall(texte.encode('UTF-8') + b'\n')

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ma_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ma_socket.bind((masque_acces, numero_port_serveur))
    ma_socket.listen(socket.SOMAXCONN)
    print("Serveur en attente de client...")

    (nouvelle_connexion, tsap_depuis) = ma_socket.accept()
    print("Client connecté depuis", tsap_depuis)

    pid = os.fork()
    if pid == 0:
        boucle_emission(nouvelle_connexion)
        nouvelle_connexion.close()
        sys.exit(0)
    else:
        boucle_reception(nouvelle_connexion)
        nouvelle_connexion.close()

finally:
    ma_socket.close()
