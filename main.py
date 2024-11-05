from modules.mise_a_la_charte import apply_layer_chart_with_mapping
from modules.calculs_vrd import CalculsVRD
import sys

def afficher_menu():
    print("\n--- Menu Principal ---")
    print("1. Lancer le Module de Mise à la Charte Graphique")
    print("2. Lancer le Module de Calculs VRD")
    print("3. Quitter le programme")
    choix = input("Veuillez choisir une option : ")
    return choix

def main():
    while True:
        choix = afficher_menu()

        if choix == "1":
            print("\nLancement du Module de Mise à la Charte Graphique...")
            # Exécution du module Mise à la Charte
            apply_layer_chart_with_mapping("C:\\ProjetR\\dwg_dxf\\topo_001.dwg", "charte_graphique.json")
            print("Module de Mise à la Charte Graphique terminé.")

        elif choix == "2":
            print("\nLancement du Module de Calculs VRD...")
            # Exécution du module Calculs VRD
            calculs_vrd = CalculsVRD()
            # Exemple d'utilisation du module Calculs VRD (adapter selon le contenu du module)
            surface_totale = calculs_vrd.calcul_surface("LayerName")
            print(f"Surface totale calculée : {surface_totale}")
            print("Module de Calculs VRD terminé.")

        elif choix == "3":
            print("Programme terminé. Au revoir !")
            sys.exit()

        else:
            print("Choix non valide. Veuillez entrer un nombre entre 1 et 3.")

if __name__ == "__main__":
    main()
