import socket
import select

HOST = ''
PORT = 8080



serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind((HOST, PORT))
serveur.listen()
print(f"Serveur de chat multi-clients en écoute sur le port {PORT}...")

sockets_liste = [serveur]
clients = {}

while True:
    read_sockets, _, _ = select.select(sockets_liste, [], [])

    for sock in read_sockets:
        if sock is serveur:
            # Nouvelle connexion entrante
            client_socket, client_address = serveur.accept()
            print(f"Nouvelle connexion de {client_address}")
            sockets_liste.append(client_socket)
            clients[client_socket] = client_address
        else:
            # Données reçues d'un client existant
            try:
                data = sock.recv(1024)
            except ConnectionResetError:
                data = b''

            if not data:
                # Client déconnecté
                print(f"Client {clients[sock]} déconnecté.")
                sockets_liste.remove(sock)
                del clients[sock]
                sock.close()
                continue

            message = data.decode('utf-8')
            addr = clients[sock]
            print(f"Reçu de {addr} : {message.strip()}")

            # Diffuser à tous les autres clients
            for other in sockets_liste:
                if other is not serveur and other is not sock:
                    try:
                        other.sendall(message.encode('utf-8'))
                    except OSError:
                        # au cas où un client se ferme brutalement
                        pass


