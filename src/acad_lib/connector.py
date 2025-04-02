import win32com.client

class AutoCADConnector:
    def __init__(self):
        self.app = None
        self.doc = None

    def connect(self):
        try:
            print("🔌 Connexion à AutoCAD...")
            self.app = win32com.client.Dispatch("AutoCAD.Application")
            self.app.Visible = True  # Optionnel : met AutoCAD au premier plan

            if self.app.Documents.Count == 0:
                print("📄 Aucun dessin ouvert. Création d'un nouveau dessin...")
                self.doc = self.app.Documents.Add()
            else:
                self.doc = self.app.ActiveDocument

            print(f"✅ Connecté au document : {self.doc.Name}")

        except Exception as e:
            print("❌ Erreur de connexion à AutoCAD :", e)
            self.app = None
            self.doc = None

    def is_connected(self):
        return self.app is not None and self.doc is not None

    def get_document(self):
        return self.doc
