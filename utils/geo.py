from __future__ import annotations

import json
import os
from typing import Any

# On s'attend à avoir un fichier GeoJSON des départements ici :
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
DEPT_GEOJSON = os.path.join(DATA_DIR, "departements.geojson")


def load_dept_geojson() -> Any:
    """
    Charge le GeoJSON des départements français.

    ➜ À toi de déposer un fichier 'departements.geojson' dans data/processed
       (tu peux le récupérer sur data.gouv ou un repo public).
    """
    if not os.path.exists(DEPT_GEOJSON):
        raise FileNotFoundError(
            f"Fichier GeoJSON introuvable : {DEPT_GEOJSON}\n"
            "➡ Télécharge un GeoJSON des départements français et enregistre-le à ce chemin."
        )

    with open(DEPT_GEOJSON, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    return geojson
