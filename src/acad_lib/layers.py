class LayerManager:
    def __init__(self, doc):
        self.doc = doc
        self.layers = doc.Layers

    def lister_calques(self):
        try:
            return [layer.Name for layer in self.layers]
        except Exception as e:
            print("❌ Erreur lors de la lecture des calques :", e)
            return []

    def renommer_calque(self, ancien_nom, nouveau_nom):
        try:
            layer = self.layers.Item(ancien_nom)
            layer.Name = nouveau_nom
            print(f"✅ Calque renommé : {ancien_nom} → {nouveau_nom}")
        except Exception as e:
            print(f"❌ Erreur de renommage ({ancien_nom} → {nouveau_nom}) :", e)

    def modifier_calque(self, nom, props):
        try:
            layer = self.layers.Item(nom)
            if "couleur" in props:
                layer.Color = int(props["couleur"])
            if "gelé" in props:
                layer.Freeze = props["gelé"]
            if "verrouillé" in props:
                layer.Lock = props["verrouillé"]
            print(f"⚙️ Calque modifié : {nom} → {props}")
        except Exception as e:
            print(f"❌ Erreur modification calque {nom} :", e)

    def creer_calque(self, nom, props=None):
        try:
            new_layer = self.layers.Add(nom)
            print(f"🆕 Calque créé : {nom}")
            if props:
                self.modifier_calque(nom, props)
        except Exception as e:
            print(f"❌ Erreur création calque {nom} :", e)
