import socket, sys, logging, time
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
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M")
        return formatter.format(record)


file_handler = logging.FileHandler(f"{LOG_DIR}/{LOG_FILE}", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M"
)
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

host = ""
port = 13337


# === FONCTIONS ===
def is_ipv4(address: str) -> bool:
    """
    Permet de check si un string est bien une IPv4
    """
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def is_ipavailable(address: str) -> bool:
    """
    Permet de check si l'adresse IP entrée existe sur la machine
    """
    interfaces_data = net_if_addrs()
    for _, addrs in interfaces_data.items():
        for a in addrs:
            if a.address == address:
                return True
    return False


def set_port(p: str):
    """
    Permet de définir le port vers lequel se connecter (Par défaut: 13337).
    """
    global port

    p = int(p)

    if not 0 < p < 65535:
        raise ValueError(
            f"ERROR -p argument invalide. Le port spécifié {p} n'est pas un port valide (de 0 à 65535)."
        )
        sys.exit(1)
    if p <= 1024:
        raise ValueError(
            f"ERROR -p argument invalide. Le port spécifié {p} est un port privilégié. Spécifiez un port au dessus de 1024."
        )
        sys.exit(2)

    port = p


def set_listen(ip: str):
    """
    Permet de définir l'IP du serveur vers lequel se connecter.
    """
    global host

    if not is_ipv4(ip):
        raise ValueError(
            f"ERROR -l argument invalide. L'adresse {ip} n'est pas une adresse IP valide."
        )
        sys.exit(3)
    if not is_ipavailable(ip):
        raise ValueError(
            f"ERROR -l argument invalide. L'adresse {ip} n'est pas l'une des adresses IP de cette machine."
        )
        sys.exit(4)
    host = ip


def show_help():
    """
    Permet d'afficher le menu d'aide
    """
    print(
        """
    Utilisation: python bs_server_II1.py -l [IP] [OPTION]...
    Permet d'ouvrir un serveur TCP sur une IP et un Port donné sur la machine

    Options disponibles:
        -p, --port [PORT]       Permet définir le port à ouvrir, par défaut 13337 (ex: -p 7777)
        -l, --listen [IP]       Permet de définir l'IP à utiliser (ex: -l 10.10.10.10)
    """
    )
    sys.exit(1)


# === COMMANDES ===
ARGS_CMD = {
    "-p": [set_port, 1],  # [Fonction, nombre d'argument]
    "--port": [set_port, 1],
    "-l": [set_listen, 1],
    "--listen": [set_listen, 1],
    "-h": [show_help, 0],
    "--help": [show_help, 0],
}

argv = sys.argv[1:]

if len(argv) <= 1:
    show_help()

i = 0
while i < len(argv):
    if argv[i] in ARGS_CMD.keys():
        cmd = ARGS_CMD[argv[i]][0]
        argNumber = ARGS_CMD[argv[i]][1]
        if argNumber == 0:
            cmd()
            i += 1
        else:
            if i + 1 >= len(argv):
                show_help()
                break
            cmd(argv[i + 1])
            i += 2
    else:
        show_help()
        i += 1

if host == "":
    show_help()


# === CONNEXION AU SERVEUR ===
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
s.settimeout(60)

logging.info(f"Le serveur tourne sur {host}:{port}")
timeSave = time.time()


while True:
    try:
        conn, (client_ip, client_port) = s.accept()

        logging.info(f"Un client ({client_ip}) s'est connecté.")
        timeSave = time.time()

        data = conn.recv(1024).decode("utf-8")
        if not data:
            continue

        logging.info(f'Le client {client_ip} a envoyé "{data}".')

        result = eval(data)

        conn.sendall(result.to_bytes(5, "little", signed=True))
        logging.info(f'Réponse envoyée au client {client_ip} : "{result}".')

        conn.close()

    except TimeoutError:
        logging.warning("Aucun client depuis plus de une minute.")
        break
    except socket.timeout:
        logging.warning("Aucun client depuis plus de une minute.")
        break
    except socket.error as e:
        print(f"Error Occured: {e}")
        break
