from __future__ import annotations

import pandas as pd
import plotly.express as px
import folium


def crimes_by_compagnie(df: pd.DataFrame):
    """
    Nombre total de faits par compagnie de gendarmerie (lib_dpt).
    """
    if df.empty:
        return px.bar(title="Aucune donnée à afficher")

    grouped = df.groupby(["departement", "lib_dpt"], as_index=False)["nb_faits"].sum()
    fig = px.bar(
        grouped,
        x="lib_dpt",
        y="nb_faits",
        title="Nombre de faits par compagnie de gendarmerie (2021)",
        labels={"lib_dpt": "Compagnie de gendarmerie", "nb_faits": "Nombre de faits"},
    )
    fig.update_xaxes(tickangle=45)
    return fig


def crimes_by_type(df: pd.DataFrame, top_n: int = 20):
    """
    Répartition des faits par type d'infraction.
    """
    if df.empty or "type_delit" not in df.columns:
        return px.bar(title="Aucune donnée à afficher")

    grouped = df.groupby("type_delit", as_index=False)["nb_faits"].sum()
    grouped = grouped.sort_values("nb_faits", ascending=False).head(top_n)

    fig = px.bar(
        grouped,
        x="type_delit",
        y="nb_faits",
        title=f"Top {top_n} types d'infractions (2021)",
        labels={"type_delit": "Type d'infraction", "nb_faits": "Nombre de faits"},
    )
    fig.update_xaxes(tickangle=45)
    return fig


def top_compagnies_for_type(df: pd.DataFrame, type_delit: str, top_n: int = 15):
    """
    Top compagnies pour un type d'infraction donné.
    """
    if df.empty:
        return px.bar(title="Aucune donnée à afficher")

    sub = df[df["type_delit"] == type_delit]
    if sub.empty:
        return px.bar(title=f"Aucune donnée pour le type : {type_delit}")

    grouped = sub.groupby(["departement", "lib_dpt"], as_index=False)["nb_faits"].sum()
    grouped = grouped.sort_values("nb_faits", ascending=False).head(top_n)

    fig = px.bar(
        grouped,
        x="lib_dpt",
        y="nb_faits",
        title=f"Top {top_n} compagnies pour : {type_delit}",
        labels={"lib_dpt": "Compagnie", "nb_faits": "Nombre de faits"},
    )
    fig.update_xaxes(tickangle=45)
    return fig

def folium_choropleth_by_dept(df: pd.DataFrame, geojson: dict) -> folium.Map:
    """
    Carte Folium : nombre total de faits par département (code_dept).

    On suppose que :
    - df contient une colonne 'code_dept' (01, 2A, 971, ...)
    - le GeoJSON a une propriété 'code' ou 'code_insee' pour le département
      (à adapter si besoin selon ton fichier).
    """
    if df.empty:
        # On renvoie quand même une carte vide
        m = folium.Map(location=[46.5, 2.5], zoom_start=5)
        return m

    # Aggrégation par département
    grouped = df.groupby("code_dept", as_index=False)["nb_faits"].sum()

    m = folium.Map(location=[46.5, 2.5], zoom_start=5)

    folium.Choropleth(
        geo_data=geojson,
        data=grouped,
        columns=["code_dept", "nb_faits"],
        key_on="feature.properties.code",  # ⚠️ adapte à la propriété réelle de ton GeoJSON
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Nombre de faits (2021)",
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m