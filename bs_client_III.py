# pylint: disable=anomalous-backslash-in-string, invalid-name, missing-module-docstring

import socket
import sys
import re
import logging

LOG_DIR = "/var/log/bs_client"
LOG_FILE = "bs_client.log"


def is_calcul(value: str):
    """
    Permet de vérifier si la valeur entrée est bien un calcul avec soit 
    multiplication, addition, soustraction
    et avec comme valeurs max -100000 et 100000
    """
    return re.search("^(-?(100000|\d{0,5}))\s*([\+\-\*]\s*(-?(100000|\d{0,5})))*$", value)


class CustomFormatter(logging.Formatter):
    """
    Classe pour avoir un logger dans la console avec des jolies couleurs
    """
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = "%(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: log_format,
        logging.INFO: log_format,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
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

HOST = "10.0.1.12"
PORT = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))

    logging.info("Connexion réussie à %s:%d.", HOST, PORT)

    val = input("Entrez votre calcul : ")

    if isinstance(val, str):
        raise TypeError("Veuillez entrer une string !")
    if not is_calcul(val):
        raise ValueError("Veuillez un calcul valide (+,-,*, min:-100000, max:100000)")

    s.sendall(str.encode(val))
    logging.info("Message envoyé au serveur %s : %s.", HOST, val)

    data = int.from_bytes(s.recv(1024), byteorder="little", signed=True)
    logging.info("Réponse reçue du serveur %s : %d.", HOST, data)
    print("Réponse du serveur: ", data)

    s.close()
except socket.error as e:
    logging.error("Impossible de se connecter au serveur %s sur le port %d.", HOST, PORT)

sys.exit(0)
