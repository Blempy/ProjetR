# 📝 TODO – Reprise du projet VRD Automation

## 🔁 Avant de coder

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/TonPseudo/ProjetR.git
   cd ProjetR
   ```

2. Créer et activer l’environnement virtuel :
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## ✅ Avancement actuel

- Connexion AutoCAD via COM (win32com)
- Classe LayerManager fonctionnelle :
  - lister / créer / modifier / renommer calques
- Module `CharteGraphique` opérationnel :
  - mapping JSON + fallback intelligent
  - mode simulation
  - log texte
  - calques inconnus envoyés vers `Z_A_CLASSER`

---

## 🔮 À faire ensuite

- [ ] Tester le script en mode réel (`simulation=False`)
- [ ] Ajouter une option pour supprimer les anciens calques renommés
- [ ] Générer un rapport d’audit (HTML, CSV ou Excel)
- [ ] Ajouter des fonctions dans `LayerManager` :
  - [ ] suppression de calques
  - [ ] vérification de doublons
  - [ ] regroupement automatique
- [ ] Isoler les modules métiers dans `modules/charte_graph/`
