import socket

host = '10.0.1.12'
port = 13337 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, (client_ip, client_port) = s.accept()

while True:
    try:
        print(f"Un client vient de se co et son IP c'est {client_ip}.")

        data = conn.recv(1024).decode("utf-8")
        if not data: break

        if "meo" in data:
            conn.sendall(str.encode("Meo à toi confrère.", "utf-8"))
        elif "waf" in data:
            conn.sendall(b"ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

conn.close()
