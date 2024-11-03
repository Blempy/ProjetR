import ezdxf
import json

# Charger la charte des calques depuis un fichier JSON
def load_layer_chart(chart_path):
    with open(chart_path, 'r') as file:
        layer_chart = json.load(file)
    return {layer['layer_name']: layer for layer in layer_chart}

# Appliquer la charte graphique sur le fichier DWG
def apply_layer_chart(dwg_path, chart_path, output_path):
    # Charger la charte des calques
    layer_chart = load_layer_chart(chart_path)
    
    # Charger le fichier DWG
    dwg = ezdxf.readfile(dwg_path)
    
    # Parcourir et modifier les calques selon la charte
    for layer_name, layer_properties in layer_chart.items():
        if layer_name in dwg.layers:
            # Modifier les propriétés du calque existant
            layer = dwg.layers.get(layer_name)
            layer.color = ezdxf.colors.int2rgb(layer_properties.get('color', 7))  # Default color is white (7)
            layer.lineweight = float(layer_properties.get('line_weight', 0.25))  # Default line weight
        else:
            # Ajouter un calque s'il n'existe pas
            dwg.layers.new(name=layer_name, dxfattribs={
                'color': ezdxf.colors.int2rgb(layer_properties.get('color', 7)),
                'lineweight': float(layer_properties.get('line_weight', 0.25))
            })
    
    # Sauvegarder les modifications dans un nouveau fichier DWG
    dwg.saveas(output_path)
    print(f"Le fichier a été enregistré avec succès sous {output_path}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Applique la charte graphique au fichier DWG
    apply_layer_chart("exemple.dwg", "charte_graphique.json", "exemple_modifie.dwg")
