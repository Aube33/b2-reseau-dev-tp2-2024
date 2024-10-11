import socket, sys, re

host = '10.0.1.12'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")

    val = input("Que veux-tu envoyer au serveur : ")

    if type(val) is not str:
        raise TypeError("Veuillez entrer une string !")
    elif not re.search("^.*(meo|waf).*$", val):
        raise ValueError("Mauvaise valeur entrée, soit waf soit meo !")


    s.sendall(str.encode(val))
    data = s.recv(1024).decode("utf-8")

    print("Réponse du serveur: ", data)

    s.close()
except:
    print("Impossible de se connecter au serveur !")

sys.exit(0)