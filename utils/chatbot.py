from __future__ import annotations

import os
from typing import List, Dict

from litellm import completion


PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "gpt-4o-mini")
SECONDARY_MODEL = os.getenv("SECONDARY_MODEL", "gpt-4.1-mini")


def _call_llm(messages: List[Dict[str, str]], model: str | None = None) -> str:
    model = model or PRIMARY_MODEL
    resp = completion(
        model=model,
        messages=messages,
    )
    return resp.choices[0].message["content"]  # type: ignore[attr-defined]


def generate_analysis_summary(context_text: str, question: str | None = None) -> str:
    """Génère une analyse textuelle des données filtrées."""
    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un assistant data analyst spécialisé en sécurité urbaine. "
                "Tu expliques les tendances de façon claire, nuancée et compréhensible "
                "pour des non-statisticiens. Donne des ordres de grandeur, compare aux "
                "autres territoires si c'est pertinent, et reste prudent sur les "
                "interprétations causales."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Voici un résumé des données filtrées :\n{context_text}\n"
                f"Question spécifique : {question or 'Explique les principaux enseignements.'}"
            ),
        },
    ]
    return _call_llm(messages, model=PRIMARY_MODEL)


def chatbot_answer(user_message: str, context_hint: str | None = None) -> str:
    """Chatbot général sur les statistiques de criminalité."""
    base_context = (
        "Tu es un assistant qui répond aux questions sur des statistiques de "
        "criminalité en France. Tu n'inventes pas de chiffres précis si on ne te "
        "fournit pas les données correspondantes, mais tu peux expliquer comment "
        "interpréter les indicateurs, les limites des données, et les comparaisons "
        "entre territoires."
    )
    if context_hint:
        base_context += "\nContexte additionnel : " + context_hint

    messages = [
        {"role": "system", "content": base_context},
        {"role": "user", "content": user_message},
    ]
    # On montre l'usage d'un deuxième modèle possible
    return _call_llm(messages, model=SECONDARY_MODEL)
