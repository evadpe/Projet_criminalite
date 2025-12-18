# 🏛️ SafeCity — Tableau de bord sécurité urbaine

## 📋 Description
SafeCity est une application Streamlit qui permet d'explorer les données de criminalité en France
(crimes et délits), de les visualiser dans le temps et dans l'espace, et de générer des analyses
automatiques grâce à l'IA (OpenAI via LiteLLM).

## 🎯 Fonctionnalités
- Cartographie interactive des délits par zone
- Analyse temporelle des tendances
- Comparateur de territoires (départements / communes)
- Assistant IA pour analyser les tendances et générer des rapports
- Chatbot de questions / réponses sur les statistiques

## 🛠️ Installation

```bash
# Cloner le repo
git clone <url-de-votre-repo>
cd safecity-opendata

# Installer avec uv
uv sync

# Configurer les variables d'environnement
cp .env.example .env
# Puis éditer .env avec votre clé OpenAI
```

## 🚀 Lancement

```bash
uv run streamlit run app.py
```

## 📊 Sources de données (à brancher)
- [Crimes et délits - Ministère de l'Intérieur](https://www.data.gouv.fr/fr/datasets/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/)
- [Contours des départements (IGN / OSM)](https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/)
- [Population INSEE](https://www.insee.fr/fr/statistiques/1893198)

> ⚠️ Les fonctions de chargement de données sont fournies avec des exemples simplifiés.
> À vous de remplacer les exemples par les vraies données issues de data.gouv.fr.

## 👥 Équipe
- À compléter

## 📄 Licence
MIT
