# 🏛️ SafeCity --- Analyse de la délinquance (Gendarmerie 2021)

Application interactive permettant d'explorer, analyser et visualiser
les données officielles de la **gendarmerie nationale (année 2021)**,
avec cartographie interactive, graphiques Plotly et analyse automatique
via **IA (OpenAI / gpt-4o-mini)**.

Ce projet a été réalisé dans le cadre du module **Open Data & IA**
(IPSSI).

------------------------------------------------------------------------

## 📊 Fonctionnalités

### 🔍 Exploration des données

-   Types d'infractions
-   Compagnies et départements
-   Filtrage dynamique multi-critères

### 🗺️ Cartographie interactive

-   Carte Folium (GeoJSON départemental)
-   Choroplèthe dynamique

### 📈 Visualisations interactives

-   Répartition par compagnie
-   Répartition par type d'infraction
-   Top compagnies
-   Graphiques Plotly Express

### 🤖 IA intégrée (OpenAI)

-   Résumés statistiques auto-générés
-   Chatbot interactif
-   Modèle utilisé : **gpt-4o-mini**

------------------------------------------------------------------------

## 🗂️ Structure du projet

    app.py
    utils/
      data.py
      charts.py
      geo.py
      chatbot.py
    data/
      processed/
        crimes_2021.json
        departements.geojson

------------------------------------------------------------------------

## 📦 Installation

### 1. Cloner le dépôt

``` bash
git clone https://github.com/evadpe/Projet_criminalite
cd Projet_criminalite
```

### 2. Installer les dépendances

``` bash
uv sync
```

### 3. Configurer l'environnement

``` bash
cp .env.example .env
```

Ajouter votre clé OpenAI :

    OPENAI_API_KEY="votre_clef"
    OPENAI_MODEL="gpt-4o-mini"

------------------------------------------------------------------------

## 🚀 Lancement

``` bash
uv run streamlit run app.py
```

L'application démarre sur :\
👉 http://localhost:8501/

------------------------------------------------------------------------

## 📊 Sources de données

-   Données officielles (gendarmerie 2021) --- Data.gouv\
-   GeoJSON départements --- IGN / OSM (france-geojson)

------------------------------------------------------------------------

## 🛠️ Technologies

### Backend

-   Python 3.13\
-   Pandas\
-   DuckDB\
-   OpenAI API

### Frontend

-   Streamlit\
-   Plotly Express\
-   Folium

------------------------------------------------------------------------

## 👥 Équipe

-   Louis\

-   -   noms restants si applicable

------------------------------------------------------------------------

## 📄 Licence

MIT
