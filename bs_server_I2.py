import socket

host = '10.0.1.12'
port = 13337 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()

while True:
    try:
        data = conn.recv(1024)
        if not data: break

        client_hostname = socket.gethostname()
        client_ip = socket.gethostbyname(client_hostname)

        print(f"Un client vient de se co et son IP c'est {client_ip}.")

        if "meo" in data:
            conn.sendall(b"Meo à toi confrère.")
        elif "waf" in data:
            conn.sendall(b"ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

conn.close()
