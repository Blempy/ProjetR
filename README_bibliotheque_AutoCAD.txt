# 📚 Bibliothèque Python - AutoCAD Automation pour VRD

## 🎯 Objectif
Développer une bibliothèque Python modulaire et évolutive pour automatiser les tâches courantes liées à AutoCAD, dans le cadre d’un projet de bureau d’études VRD.

---

## 🧠 Philosophie de développement

- **Modulaire** : chaque composant a une responsabilité claire (connexion, calques, objets, export, etc.)
- **Évolutive** : elle s’enrichit progressivement selon l’avancement des modules du projet VRD.
- **Compatible** : fonctionne avec AutoCAD en direct (via COM/pyautocad) ou en lecture DXF (via `ezdxf`).
- **Utilisable par d’autres outils** : bots, interfaces web, scripts en ligne de commande.

---

## 🧱 Architecture prévue

```
acad_lib/
├── __init__.py
├── connector.py           # Connexion AutoCAD (ou mock)
├── layers.py              # Gestion des calques
├── objects.py             # Lecture et analyse d'entités géométriques
├── export.py              # Export DXF / GeoJSON / Excel
└── utils.py               # Outils communs, exceptions, logs
```

---

## 🔁 Stratégie d'évolution

| Module projet VRD              | Fonctionnalité ajoutée à la lib         | Fichier cible       |
|-------------------------------|------------------------------------------|---------------------|
| Mise à la charte graphique     | Création/modification de calques         | layers.py           |
| Calculs VRD                    | Extraction métrés (longueur/surface)     | objects.py          |
| Intégration SIG                | Export en GeoJSON                        | export.py           |
| Rapports & livrables           | Légende AutoCAD, export Excel            | export.py           |
| Analyse normative              | Détection pentes, intersections          | objects.py / utils  |

---

## ✅ Exemple d’utilisation à venir

```python
from acad_lib.connector import AutoCADConnector
from acad_lib.layers import LayerManager

acad = AutoCADConnector()
layers = LayerManager(acad.doc)
layers.rename_layer("TOPO_HAIE", "BLM_ESP_VERTS")
```

---

## ✍️ Auteur
Projet développé avec ❤️ par BLM VRD indépendant – 2025
