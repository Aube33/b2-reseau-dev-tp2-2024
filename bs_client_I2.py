import socket, sys

host = '10.0.1.12'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

val = input("Que veux-tu envoyer au serveur : ")

try:
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
    s.sendall(str.encode(val))
    data = s.recv(1024).decode("utf-8")

    s.close()
except:
    print("Une erreur a eu lieu !")

print("Réponse du serveur: ", data)
sys.exit(0)