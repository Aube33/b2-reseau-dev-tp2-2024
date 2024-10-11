import socket, sys, logging, os, time
from psutil import net_if_addrs

LOG_DIR = "/var/log/bs_server"
LOG_FILE = "bs_server.log"

class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

file_handler = logging.FileHandler(f"{LOG_DIR}/{LOG_FILE}", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M")
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

host = ''
port = 13337

#=== FONCTIONS ===
def isIPv4(address:str)->bool:
    """
    Permet de check si un string est bien une IPv4
    """
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

def isIPAvailable(address:str)->bool:
    """
    Permet de check si l'adresse IP entrée existe sur la machine
    """
    interfaces_data = net_if_addrs()
    for name, addrs in interfaces_data.items():
        for a in addrs:
            if a.address == address:
                return True
    return False

def setPort(p:str):
    """
    Permet de définir le port vers lequel se connecter (Par défaut: 13337).
    """
    global port

    p = int(p)

    if not 0<p<65535:
        raise ValueError(f"ERROR -p argument invalide. Le port spécifié {p} n'est pas un port valide (de 0 à 65535).")
        sys.exit(1)
    if p<=1024:
        raise ValueError(f"ERROR -p argument invalide. Le port spécifié {p} est un port privilégié. Spécifiez un port au dessus de 1024.")
        sys.exit(2)

    port = p

def setListen(ip:str):
    """
    Permet de définir l'IP du serveur vers lequel se connecter.
    """
    global host

    if not isIPv4(ip):
        raise ValueError(f"ERROR -l argument invalide. L'adresse {ip} n'est pas une adresse IP valide.")
        sys.exit(3)
    if not isIPAvailable(ip):
        raise ValueError(f"ERROR -l argument invalide. L'adresse {ip} n'est pas l'une des adresses IP de cette machine.")
        sys.exit(4)  
    host = ip    

def showHelp():
    """
    Permet d'afficher le menu d'aide
    """
    print("""
    Utilisation: python bs_server_II1.py -l [IP] [OPTION]...
    Permet d'ouvrir un serveur TCP sur une IP et un Port donné sur la machine

    Options disponibles:
        -p, --port [PORT]       Permet définir le port à ouvrir, par défaut 13337 (ex: -p 7777)
        -l, --listen [IP]       Permet de définir l'IP à utiliser (ex: -l 10.10.10.10)
    """)
    sys.exit(1)


#=== COMMANDES ===
ARGS_CMD = {
    "-p": [setPort, 1], # [Fonction, nombre d'argument]
    "--port": [setPort, 1],
    "-l": [setListen, 1],
    "--listen": [setListen, 1],
    "-h": [showHelp, 0],
    "--help": [showHelp, 0],
}

argv = sys.argv[1:]

if len(argv)<=1:
    showHelp()

i = 0
while i < len(argv):
    if argv[i] in ARGS_CMD.keys():
        cmd = ARGS_CMD[argv[i]][0]
        argNumber = ARGS_CMD[argv[i]][1]
        if argNumber == 0:
            cmd()
            i+=1
        else:
            if i+1 >= len(argv):
                showHelp()
                break
            else:
                cmd(argv[i + 1])
                i+=2
    else:
        showHelp()
        i+=1

if host=='':
    showHelp()


#=== CONNEXION AU SERVEUR ===
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)

logging.info(f"Le serveur tourne sur {host}:{port}")
timeSave = time.time()

conn, addr = s.accept()

while True:
    print("tes tok")
    if time.time()-timeSave > 60000:
        timeSave = time.time()
        logging.warning("Aucun client depuis plus de une minute.")
    try:
        data = conn.recv(1024).decode("utf-8")
        if not data: break

        client_hostname = socket.gethostname()
        client_ip = socket.gethostbyname(client_hostname)

        logging.info(f"Un client ({client_ip}) s'est connecté.")

        logging.info(f'Le client {client_ip} a envoyé "{data}".')

        message = ""
        if "meo" in data:
            message = "Meo à toi confrère."
        elif "waf" in data:
            message = "ptdr t ki"
        else:
            message = "Mes respects humble humain."

        conn.sendall(str.encode(message, "utf-8"))
        logging.info(f'Réponse envoyée au client {client_ip} : "{message}".')

    except socket.error:
        print("Error Occured.")
        break

conn.close()
