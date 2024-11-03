import json
import subprocess
import time
from pyautocad import Autocad
from logging_config import log_event

# Chemin vers l'exécutable d'AutoCAD - modifie ce chemin selon ton installation
AUTOCAD_PATH = r"C:\Program Files\Autodesk\AutoCAD 2023\acad.exe"

# Charger la charte des calques depuis un fichier JSON
def load_layer_chart(chart_path):
    with open(chart_path, 'r') as file:
        layer_chart = json.load(file)
    log_event(
        module="Mise à la Charte Graphique",
        action="Chargement de la charte des calques",
        details={"fichier_charte": chart_path, "status": "succès"}
    )
    return {layer['layer_name']: layer for layer in layer_chart}

# Fonction pour démarrer AutoCAD si ce n'est pas déjà ouvert
def start_autocad():
    try:
        # Vérifie si AutoCAD est déjà lancé
        acad = Autocad(create_if_not_exists=True)
        acad.prompt("AutoCAD est déjà lancé.\n")
        log_event(
            module="Mise à la Charte Graphique",
            action="Vérification d'AutoCAD",
            details={"status": "AutoCAD déjà ouvert"}
        )
    except Exception:
        # Lancer AutoCAD avec subprocess
        subprocess.Popen(AUTOCAD_PATH)
        log_event(
            module="Mise à la Charte Graphique",
            action="Lancement d'AutoCAD",
            details={"status": "succès", "chemin": AUTOCAD_PATH}
        )
        # Attendre quelques secondes pour qu'AutoCAD soit 
