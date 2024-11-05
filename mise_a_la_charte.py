import json
import subprocess
import time
from pyautocad import Autocad
from logging_config import log_event
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Règles de mappage spécifiques pour des calques particuliers
SPECIFIC_MAPPING = {
    "mobilier": "PR_MOBILIER",
    # Ajouter d'autres règles spécifiques si nécessaire
}

# Mappage par mot-clé pour chaque calque de la charte
KEYWORD_MAP = {
    "PR_CLOTURES": ["CLOTURE", "clôture", "barrière", "sécurité"],
    "PR_MOBILIER": ["banc", "table", "mobilier"],
    "PR_VOIRIE": ["ALLER", "BORDURE", ],
    "PR_RSX_ASSAINISSEMENT" : ["ASSAINISSEMENT", "ASSAINIS"],
    "PR_BATIMENT" : ["BATI", ],
    "PR_COTATION" : ["COTATION", ],
    # Ajouter d'autres mots-clés pour chaque calque
}

COLOR_MAP = {
    "red": 1,
    "yellow": 2,
    "green": 3,
    "cyan": 4,
    "blue": 5,
    "magenta": 6,
    "white": 7,
    "black": 7
}

AUTOCAD_PATH = r"C:\Program Files\Autodesk\AutoCAD 2021\acad.exe"

def validate_and_apply_attributes(layer, chart_layer):
    """Valider et appliquer la couleur et l'épaisseur de ligne du calque en fonction de la charte."""
    color_name = chart_layer.get('color', 'black').lower()
    color_code = COLOR_MAP.get(color_name, 7)  # Utiliser noir par défaut si la couleur n'est pas dans COLOR_MAP
    
    try:
        layer.color = color_code
    except Exception as e:
        print(f"Erreur d'application de la couleur {color_name} sur le calque {layer.Name}: {e}")
        log_event(module="Mise à la Charte Graphique", action="Erreur couleur", details={"calque": layer.Name, "couleur": color_name, "erreur": str(e)})
    
    line_weight = chart_layer.get('line_weight', '0.25')
    try:
        layer.lineweight = float(line_weight)  # Conversion en flottant si possible
    except ValueError:
        print(f"Erreur d'application de l'épaisseur de ligne {line_weight} sur le calque {layer.Name}: valeur non valide, utilisation de 0.25 par défaut.")
        layer.lineweight = 0.25
        log_event(module="Mise à la Charte Graphique", action="Erreur épaisseur", details={"calque": layer.Name, "épaisseur": line_weight, "erreur": "Valeur non valide"})

def clean_layer_name(layer_name):
    """Supprime le préfixe avant le premier tiret pour obtenir le nom principal du calque."""
    return layer_name.split('-')[-1].strip().lower()

def map_incoming_layers_to_chart(incoming_layers, layer_chart):
    """Fonction pour mapper les calques entrants à la charte en utilisant plusieurs stratégies."""
    mapped_layers = {}

    for incoming_layer in incoming_layers:
        incoming_name = clean_layer_name(incoming_layer.Name)  # Nettoyer le nom pour extraire la partie pertinente
        
        # Stratégie 1 : Mappage spécifique pour des calques particuliers
        if incoming_name in SPECIFIC_MAPPING:
            mapped_layers[incoming_layer.Name] = SPECIFIC_MAPPING[incoming_name]
        elif incoming_name in layer_chart:
            # Stratégie 2 : Correspondance exacte avec la charte
            mapped_layers[incoming_layer.Name] = incoming_name
        else:
            # Stratégie 3 : Correspondance par mots-clés
            for chart_layer_name, keywords in KEYWORD_MAP.items():
                if any(keyword in incoming_name for keyword in keywords):
                    mapped_layers[incoming_layer.Name] = chart_layer_name
                    break
            else:
                # Stratégie 4 : Correspondance floue (fuzzy matching) pour des correspondances approximatives
                possible_match = process.extractOne(incoming_name, layer_chart.keys(), scorer=fuzz.token_set_ratio)
                mapped_layers[incoming_layer.Name] = possible_match[0] if possible_match and possible_match[1] >= 80 else "Aucun mapping trouvé"
    
    return mapped_layers

def load_layer_chart(chart_path):
    """Charge la charte graphique des calques depuis un fichier JSON."""
    with open(chart_path, 'r') as file:
        layer_chart_data = json.load(file)
    layer_chart = {}
    for category, layers in layer_chart_data.items():
        for layer in layers:
            layer_chart[layer['layer_name']] = layer  # Associe chaque calque à son nom
    log_event(module="Mise à la Charte Graphique", action="Chargement de la charte", details={"fichier_charte": chart_path, "status": "succès"})
    return layer_chart

def close_all_autocad_instances():
    """Ferme toutes les instances d'AutoCAD pour éviter les conflits COM."""
    try:
        subprocess.call("taskkill /f /im acad.exe", shell=True)
        print("Toutes les instances d'AutoCAD ont été fermées.")
    except Exception as e:
        print(f"Erreur lors de la fermeture d'AutoCAD : {e}")
        log_event(module="Mise à la Charte Graphique", action="Erreur fermeture AutoCAD", details={"erreur": str(e)})

def start_autocad():
    """Démarre AutoCAD après avoir fermé toutes les instances précédentes."""
    close_all_autocad_instances()
    time.sleep(5)  # Attente pour s'assurer que toutes les instances sont fermées
    
    try:
        subprocess.Popen(AUTOCAD_PATH)
        log_event(module="Mise à la Charte Graphique", action="Lancement d'AutoCAD", details={"status": "succès"})
        time.sleep(30)  # Augmenter le délai pour s'assurer qu'AutoCAD est complètement chargé
        acad = Autocad(create_if_not_exists=True)
        return acad
    except Exception as e:
        print(f"Erreur lors du démarrage d'AutoCAD : {e}")
        log_event(module="Mise à la Charte Graphique", action="Erreur démarrage AutoCAD", details={"erreur": str(e)})
        return None

def ensure_autocad_ready(acad, retries=5, wait_time=5):
    """Vérifie qu'AutoCAD est prêt avant chaque commande."""
    for attempt in range(retries):
        try:
            acad.prompt("Vérification de l'état d'AutoCAD.\n")
            print("AutoCAD est prêt.")
            return True
        except Exception:
            print(f"Tentative {attempt + 1} : AutoCAD n'est pas prêt, attente de {wait_time} secondes.")
            time.sleep(wait_time)
    print("AutoCAD ne répond toujours pas après plusieurs tentatives.")
    return False

def apply_layer_chart_with_mapping(dwg_path, chart_path):
    """Appliquer la charte graphique avec vérification unique du démarrage d'AutoCAD."""
    print("Début de l'application de la charte graphique avec mappage des calques")
    layer_chart = load_layer_chart(chart_path)
    acad = start_autocad()
    if acad is None or not ensure_autocad_ready(acad):
        print("AutoCAD ne répond pas. Impossible de continuer.")
        return

    try:
        acad.Application.Documents.Open(dwg_path)
        log_event(module="Mise à la Charte Graphique", action="Ouverture du fichier DWG", details={"fichier": dwg_path})
        print(f"Fichier {dwg_path} ouvert avec succès dans AutoCAD")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier DWG : {e}")
        log_event(module="Mise à la Charte Graphique", action="Erreur ouverture fichier", details={"fichier": dwg_path, "erreur": str(e)})
        return

    time.sleep(5)

    incoming_layers = acad.doc.Layers
    layer_mapping = map_incoming_layers_to_chart(incoming_layers, layer_chart)

    for incoming_layer_name, chart_layer_name in layer_mapping.items():
        if chart_layer_name != "Aucun mapping trouvé":
            try:
                # Rechercher ou créer le calque dans AutoCAD
                if chart_layer_name in acad.doc.Layers:
                    layer = acad.doc.Layers.Item(chart_layer_name)  # Le calque existe déjà
                    print(f"Calque existant {chart_layer_name} trouvé, modification en cours.")
                else:
                    # Créer le calque s'il n'existe pas déjà
                    layer = acad.doc.Layers.Add(chart_layer_name)
                    print(f"Calque {chart_layer_name} créé.")
                
                # Appliquer les attributs sans renommer
                validate_and_apply_attributes(layer, layer_chart[chart_layer_name])
                log_event(module="Mise à la Charte Graphique", action="Application des paramètres", details={"calque": layer.Name, "status": "modifié"})
                print(f"Calque {incoming_layer_name} mappé et modifié vers {layer.Name}")

            except Exception as e:
                print(f"Erreur lors de la modification ou création du calque {chart_layer_name}: {e}")
                log_event(module="Mise à la Charte Graphique", action="Erreur", details={"calque": chart_layer_name, "erreur": str(e)})
        else:
            print(f"Calque {incoming_layer_name} n'a pas de correspondance dans la charte graphique.")

    # Sauvegarde du fichier avec gestion d'erreurs
    try:
        acad.doc.SaveAs("C:\\ProjetR\\topo_001_mise_a_jour.dwg")
        log_event(module="Mise à la Charte Graphique", action="Enregistrement", details={"fichier": "C:\\ProjetR\\topo_001_mise_a_jour.dwg"})
        print(f"Le fichier {dwg_path} a été mis à jour et enregistré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier DWG : {e}")
        log_event(module="Mise à la Charte Graphique", action="Erreur enregistrement", details={"fichier": dwg_path, "erreur": str(e)})
    finally:
        acad.doc.Close()


if __name__ == "__main__":
    print("Le programme démarre")
    apply_layer_chart_with_mapping("C:\\ProjetR\\topo_001.dwg", "charte_graphique.json")
