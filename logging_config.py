import logging
import json
from datetime import datetime

# Configuration de base du logging
logging.basicConfig(
    filename="project_logs.json",
    level=logging.INFO,
    format='%(message)s'  # On enregistre les logs au format brut pour les transformer en JSON
)

def log_event(module, action, details):
    """
    Enregistre un événement dans les logs avec le format JSON.
    
    Args:
        module (str): Nom du module générant le log.
        action (str): Description de l'action ou de l'événement.
        details (dict): Détails supplémentaires sur l'événement.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "action": action,
        "details": details
    }
    # Écrire le log en format JSON dans le fichier
    logging.info(json.dumps(log_entry))
