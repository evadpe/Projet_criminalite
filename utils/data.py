from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pandas as pd

# Fichier JSON exporté depuis data.gouv (structure "Année 2021 - compagnies de gendarmerie")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
CRIME_JSON = os.path.join(DATA_DIR, "crimes_gendarmerie_2021.json")


@dataclass
class Filters:
    crime_type: Optional[str] = None   # libellé d'infraction
    departements: Optional[list[str]] = None  # codes de compagnies (01, 01.1, 2A, 971, ...)


def load_crime_data() -> pd.DataFrame:
    """
    Charge les données réelles depuis le JSON "Année 2021 - compagnies de gendarmerie".

    Structure JSON :
    - Ligne 0 : en-tête, chaque colonne = code de compagnie ("01", "01.1", "2A", ...)
                valeur = libellé de la compagnie ("CGD BELLEY", ...)
    - Lignes 1+ : chaque ligne = un type d'infraction
        - colonne "Année 2021 - compagnies de gendarmerie" = code index
        - colonne "Départements" = libellé de l'infraction
        - autres colonnes = nombre de faits pour chaque compagnie
    """
    if not os.path.exists(CRIME_JSON):
        raise FileNotFoundError(
            f"Fichier {CRIME_JSON} introuvable.\n"
            "➡ Place ton JSON exporté depuis data.gouv à cet emplacement."
        )

    # Lecture du JSON
    df_raw = pd.read_json(CRIME_JSON)

    # Nom exact des deux colonnes "spéciales" (d'après ton exemple)
    COL_INDEX = "Année 2021 - compagnies de gendarmerie"
    COL_TYPE = "Départements"

    if COL_INDEX not in df_raw.columns or COL_TYPE not in df_raw.columns:
        raise ValueError(
            f"Colonnes attendues '{COL_INDEX}' et '{COL_TYPE}' introuvables.\n"
            f"Colonnes trouvées : {list(df_raw.columns)}"
        )

    # Ligne 0 : en-tête compagnies
    header_row = df_raw.iloc[0]

    # Lignes 1+ : données
    data_rows = df_raw.iloc[1:].reset_index(drop=True)

    # Toutes les colonnes qui représentent des compagnies (codes)
    company_cols = [
        c for c in df_raw.columns
        if c not in ["__id", COL_INDEX, COL_TYPE]
    ]

    records = []

    for _, row in data_rows.iterrows():
        type_delit = str(row[COL_TYPE])  # libellé de l'infraction

        for code in company_cols:
            nb = row[code]

            # On ignore les NaN ou vides
            if pd.isna(nb):
                continue

            try:
                nb_int = int(nb)
            except Exception:
                continue

            lib_compagnie = header_row[code]

            records.append(
                {
                    "annee": 2021,                        # ce fichier ne contient que 2021
                    "departement": str(code),            # en réalité : code de compagnie
                    "lib_dpt": str(lib_compagnie),       # libellé de la compagnie
                    "type_delit": type_delit,            # libellé d'infraction
                    "nb_faits": nb_int,
                }
            )

    df = pd.DataFrame(records)

    # Normalisation basique
    df["annee"] = df["annee"].astype(int)
    df["departement"] = df["departement"].astype(str)
    df["lib_dpt"] = df["lib_dpt"].astype(str)
    df["type_delit"] = df["type_delit"].astype(str)
    df["nb_faits"] = df["nb_faits"].astype(int)
    
    def extract_dept(code: str) -> str:
        base = str(code).split(".")[0]
        return base

    df["code_dept"] = df["departement"].map(extract_dept)


    return df


def get_available_crime_types(df: pd.DataFrame) -> List[str]:
    if "type_delit" not in df.columns:
        return []
    return sorted(df["type_delit"].dropna().unique().tolist())


def get_available_departements(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """
    Retourne une liste (code, libellé) de compagnies de gendarmerie.
    (On réutilise les noms 'departement' / 'lib_dpt' pour ne pas changer tout le reste de l'app.)
    """
    if "departement" not in df.columns:
        return []
    tmp = df[["departement", "lib_dpt"]].drop_duplicates()
    return sorted(list({(str(r["departement"]), str(r["lib_dpt"])) for _, r in tmp.iterrows()}))


def filter_data(df: pd.DataFrame, filters: Filters) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)

    if filters.crime_type and "type_delit" in df.columns:
        mask &= df["type_delit"] == filters.crime_type

    if filters.departements and "departement" in df.columns:
        mask &= df["departement"].isin(filters.departements)

    return df[mask].copy()
