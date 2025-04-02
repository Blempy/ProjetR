from acad_lib.connector import AutoCADConnector
from acad_lib.layers import LayerManager
from acad_lib.charte_graph import CharteGraphique
import time

# Connexion à AutoCAD
autocad = AutoCADConnector()
autocad.connect()

# Attente pour s'assurer que AutoCAD est prêt
time.sleep(2)

if autocad.is_connected():
    doc = autocad.get_document()
    layers = LayerManager(doc)

    charte = CharteGraphique(
        layer_manager=layers,
        charte_path="charte_graphique.json",
        mapping_path="correspondance_calques.json",
        simulation=True  # Passe à True pour tester sans modifier AutoCAD
    )

    charte.appliquer_charte()
else:
    print("❌ Impossible de se connecter à AutoCAD.")
