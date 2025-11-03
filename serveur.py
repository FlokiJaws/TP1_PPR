import os,socket,sys

numero_port = 8080
ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
ma_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
ma_socket.bind(('', numero_port))
ma_socket.listen(socket.SOMAXCONN)

while 1:
    (nouvelle_connexion, TSAP_depuis) = ma_socket.accept()
    print ('Nouvelle connexion depuis ', TSAP_depuis)
    nouvelle_connexion.sendall(b'Bienvenu\n')
    nouvelle_connexion.close()

    
ma_socket.close()
