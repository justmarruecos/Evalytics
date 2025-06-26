# 📊 Tableau de bord interactif Edutech+

Ce projet Dash vous permet d'explorer visuellement les performances pédagogiques d'apprenants en formation hybride chez **Edutech+**, à partir d’un fichier JSON dynamique.

Le tableau de bord répond à 5 problématiques clés à l’aide de visualisations interactives et de conclusions automatisées rédigées pour des décideurs non techniques.

---

## 🎯 Objectifs
- Automatiser les analyses statistiques sur les données d'apprentissage.
- Générer des visualisations claires et pertinentes.
- Formuler des recommandations pédagogiques basées sur les données.
- Permettre une interaction fluide avec les résultats via une interface web.

---

## 🧩 Structure du projet

```
├── app.py                 # Script principal Dash
├── utils.py              # Chargement et transformation des données
├── analyses.py           # Fonctions statistiques + graphiques + conclusions
├── layout.py             # Mise en page du tableau de bord
├── requirements.txt      # Dépendances à installer
├── README.md             # Ce fichier
└── studyCorrelation.json # (Optionnel) fichier local de test
```

---

## 📥 Installation

1. **Cloner le projet ou copier les fichiers** dans un dossier local.
2. **Créer un environnement virtuel** (optionnel mais recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # sous Linux/macOS
env\Scripts\activate     # sous Windows
```
3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

---

## 🚀 Lancement de l’application

Dans le terminal :
```bash
python app.py
```

Puis ouvrir votre navigateur sur : [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 🔗 Données utilisées
Le projet tente de charger automatiquement ce fichier JSON en ligne :
```
https://edumail.fr/formations/realtimedata.json
```

En cas d’échec (connexion ou erreur JSON), un fichier local est utilisé si disponible.

### Structure attendue du JSON (voir `mission1datastructure.pdf`) :
- `studyCorrelation` : heures d’étude vs score
- `courseFormat` : stats de certification par format
- `midtermScores` : scores classes A vs B
- `approachGains` : gains par méthode pédagogique
- `completionTimes` : durées d’exercice par niveau de support

---

## 📊 Problématiques traitées

1. **Corrélation entre heures d’étude et score final**  
2. **Impact du format de cours (présentiel vs distanciel) sur la certification**  
3. **Comparaison des notes mi-parcours entre classes A et B**  
4. **Effet des approches pédagogiques sur la progression**  
5. **Influence du support sur le temps d’achèvement des exercices**

Chaque section fournit un graphique interactif et une conclusion automatisée, claire et contextualisée pour aider à la décision.

---

## ✨ Améliorations possibles
- Ajouter un bouton de rafraîchissement manuel.
- Sauvegarder les recommandations générées en PDF.
- Ajouter des filtres interactifs (ex: filtrer par classe ou support).

---
