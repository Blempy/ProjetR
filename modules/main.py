# main.py

from modules.mise_a_la_charte import apply_layer_chart_with_mapping
from modules.calculs_vrd import CalculsVRD

def main():
    # Application de la charte graphique
    print("Application de la Charte Graphique")
    dwg_path = "C:\\ProjetR\\exemple.dwg"
    chart_path = "C:\\ProjetR\\charte_graphique.json"
    apply_layer_chart_with_mapping(dwg_path, chart_path)

    # Calculs VRD
    print("Calculs VRD")
    calculs = CalculsVRD()
    layer_name = "Layer_Name"  # Remplace par un calque spécifique
    surface = calculs.calcul_surface(layer_name)
    volume = calculs.calcul_volume(layer_name, profondeur=2.5)
    longueur = calculs.calcul_longueur(layer_name)

    # Export des résultats
    results = [
        {"Type": "Surface", "Valeur": surface, "Unité": "m²"},
        {"Type": "Volume", "Valeur": volume, "Unité": "m³"},
        {"Type": "Longueur", "Valeur": longueur, "Unité": "m"}
    ]
    calculs.export_results(results)

if __name__ == "__main__":
    main()
