import socket, sys

numero_port_serveur = 8080
masque_acces = ''

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ma_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ma_socket.bind((masque_acces, numero_port_serveur))
    ma_socket.listen(socket.SOMAXCONN)
    print("Serveur en attente de client...")
    
    (nouvelle_connexion, tsap_depuis) = ma_socket.accept()
    print ("Client connecté depuis", tsap_depuis)

    def lecture_ligne(sock):
        ligne = b""
        while True:
            car = sock.recv(1)
            if not car: break
            ligne += car
            if car == b'\n': break
        return ligne
    
    while 1:
        message_client = lecture_ligne(nouvelle_connexion)
        if not message_client:
            print("Le client a fermé la connexion.")
            break
        
        print("Client >", message_client.decode('UTF-8'), end='')
        
        reponse_serveur = input("Serveur > ")
        if not reponse_serveur:
            break
            
        nouvelle_connexion.sendall(bytes(reponse_serveur, encoding='UTF-8') + b'\n')

finally:
    if 'nouvelle_connexion' in locals():
        nouvelle_connexion.close()
    ma_socket.close()