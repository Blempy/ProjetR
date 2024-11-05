import logging
import json
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os

# Chemin vers le fichier de log
log_directory = "C:\\ProjetR\\logs"
log_file_path = os.path.join(log_directory, "project_logs.json")

# Créer le répertoire de logs s'il n'existe pas
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Créer un gestionnaire de log avec rotation
file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.INFO)

# Formatter personnalisé pour JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "details": record.args if record.args else None
        }
        return json.dumps(log_entry)

# Appliquer le formateur JSON au gestionnaire de fichier
file_handler.setFormatter(JsonFormatter())

# Configuration de base du logger
logger = logging.getLogger("project_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

def log_event(module, action, details, level=logging.INFO):
    """
    Enregistre un événement dans les logs avec le format JSON.
    
    Args:
        module (str): Nom du module générant le log.
        action (str): Description de l'action ou de l'événement.
        details (dict): Détails supplémentaires sur l'événement.
        level (int): Niveau de log (e.g., logging.INFO, logging.ERROR).
    """
    logger.log(level, f"{action} - {details}", {"module": module})
