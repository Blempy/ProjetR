import math
import pandas as pd
import logging
from pyautocad import Autocad

# Configuration du logging
logging.basicConfig(filename='calculs_vrd.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

class CalculsVRD:
    def __init__(self):
        self.acad = Autocad(create_if_not_exists=True)
    
    def log_event(self, action, details):
        """Logging with additional details."""
        logging.info(f"{action} - {details}")

    def calcul_surface(self, layer_name):
        """Calculate total area for a specific layer."""
        surface_total = 0
        try:
            for entity in self.acad.iter_objects(layer=layer_name):
                if entity.EntityName == "AcDbPolyline" and entity.Closed:
                    surface_total += entity.Area
            self.log_event("Calcul de surface", {"calque": layer_name, "surface_totale": surface_total})
        except Exception as e:
            self.log_event("Erreur dans le calcul de surface", {"calque": layer_name, "erreur": str(e)})
        return surface_total

    def calcul_longueur(self, layer_name):
        """Calculate total length for linear entities in a specific layer."""
        longueur_total = 0
        try:
            for entity in self.acad.iter_objects(layer=layer_name):
                if entity.EntityName in ["AcDbPolyline", "AcDbLine"]:
                    longueur_total += entity.Length
            self.log_event("Calcul de longueur", {"calque": layer_name, "longueur_totale": longueur_total})
        except Exception as e:
            self.log_event("Erreur dans le calcul de longueur", {"calque": layer_name, "erreur": str(e)})
        return longueur_total

    def export_results(self, results, filename='results.xlsx'):
        """Export calculation results to an Excel file."""
        try:
            df = pd.DataFrame(results)
            df.to_excel(filename, index=False)
            self.log_event("Exportation des résultats", {"fichier": filename, "résultats": results})
        except Exception as e:
            self.log_event("Erreur lors de l'export des résultats", {"fichier": filename, "erreur": str(e)})

# Exemple d'utilisation
calculs = CalculsVRD()
surface = calculs.calcul_surface("LayerName")
longueur = calculs.calcul_longueur("LayerName")
results = [{"Calque": "LayerName", "Surface Totale": surface, "Longueur Totale": longueur}]
calculs.export_results(results)
