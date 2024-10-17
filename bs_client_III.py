import socket, sys, re, logging

LOG_DIR = "/var/log/bs_client"
LOG_FILE = "bs_client.log"


def isCalcul(val: str):
    return re.search("^(-?(100000|\d{0,5}))\s*([\+\-\*]\s*(-?(100000|\d{0,5})))*$", val)


class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


file_handler = logging.FileHandler(f"{LOG_DIR}/{LOG_FILE}", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M"
)
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

host = "10.0.1.12"
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))

    logging.info(f"Connexion réussie à {host}:{port}.")

    val = input("Entrez votre calcul : ")

    if type(val) is not str:
        raise TypeError("Veuillez entrer une string !")
    elif not isCalcul(val):
        raise ValueError("Veuillez un calcul valide (+,-,*, min:-100000, max:100000)")

    s.sendall(str.encode(val))
    logging.info(f"Message envoyé au serveur {host} : {val}.")

    data = int.from_bytes(s.recv(1024), byteorder="little", signed=True)
    logging.info(f"Réponse reçue du serveur {host} : {data}.")
    print("Réponse du serveur: ", data)

    s.close()
except socket.error as e:
    logging.error(f"Impossible de se connecter au serveur {host} sur le port {port}.")
except Exception as e:
    print(e)

sys.exit(0)
