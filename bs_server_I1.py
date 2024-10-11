import socket

host = '10.0.1.12'
port = 13337 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

while True:

    try:
        data = conn.recv(1024)

        if not data: continue

        conn.sendall(b"Hi mate !")

        print(f"Données reçues du client : {data}")

    except socket.error:
        print("Error Occured.")
        break

conn.close()
