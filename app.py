import streamlit as st

from utils.data import (
    load_crime_data,
    get_available_crime_types,
    get_available_departements,
    Filters,
    filter_data,
)
from utils.charts import (
    crimes_by_compagnie,
    crimes_by_type,
    top_compagnies_for_type,
    folium_choropleth_by_dept,
)
from utils.geo import load_dept_geojson
from utils.chatbot import generate_analysis_summary, chatbot_answer


st.set_page_config(
    page_title="SafeCity — Délinquance gendarmerie 2021",
    layout="wide",
)


def main():
    st.title("🏛️ SafeCity — Délinquance gendarmerie (2021)")
    st.write(
        """
        Dashboard basé sur les données réelles de la gendarmerie (année 2021),
        par compagnie, et analyse automatique via IA (OpenAI / gpt-4o-mini).
        """
    )

    # --- Chargement des données ---
    try:
        df = load_crime_data()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return

    # --- Sidebar: filtres ---
    st.sidebar.header("⚙️ Filtres")

    crime_types = get_available_crime_types(df)
    selected_crime_type = st.sidebar.selectbox(
        "Type d'infraction",
        options=["(Tous)"] + crime_types,
        index=0,
    )

    departements = get_available_departements(df)
    dept_labels = [f"{code} - {name}" for code, name in departements]
    selected_depts_labels = st.sidebar.multiselect(
        "Compagnies de gendarmerie",
        options=dept_labels,
        default=dept_labels,  # toutes cochées par défaut
    )
    selected_depts_codes = [lbl.split(" - ")[0] for lbl in selected_depts_labels]

    filters = Filters(
        crime_type=None if selected_crime_type == "(Tous)" else selected_crime_type,
        departements=selected_depts_codes or None,
    )
    filtered_df = filter_data(df, filters)

    # Aperçu debug
    with st.expander("🔍 Aperçu des données filtrées"):
        st.write(f"Nombre de lignes : {len(filtered_df)}")
        st.dataframe(filtered_df.head())

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📍 Par compagnie", "📊 Par type d'infraction", "🏆 Top compagnies", "🤖 Assistant IA"]
    )

    # TAB 1 : par compagnie
    with tab1:
        st.subheader("Analyse spatiale (compagnies & départements) — 2021")

        sub1, sub2 = st.tabs(["📊 Barres par compagnie", "🗺️ Carte Folium par département"])

        with sub1:
            st.markdown("#### Répartition par compagnie de gendarmerie")
            if filtered_df.empty:
                st.warning("Aucune donnée à afficher pour ces filtres.")
            else:
                fig1 = crimes_by_compagnie(filtered_df)
                st.plotly_chart(fig1, use_container_width=True)

        with sub2:
            st.markdown("#### Carte Folium — nombre de faits par département")
            if filtered_df.empty:
                st.warning("Aucune donnée à afficher pour ces filtres.")
            else:
                try:
                    geojson = load_dept_geojson()
                    m = folium_choropleth_by_dept(filtered_df, geojson)

                    # Intégration de Folium dans Streamlit sans dépendance externe
                    from streamlit.components.v1 import html
                    html(m._repr_html_(), height=600)
                except Exception as e:
                    st.error(f"Impossible d'afficher la carte Folium : {e}")

    # TAB 2 : par type d'infraction
    with tab2:
        st.subheader("Répartition par type d'infraction (2021)")
        if filtered_df.empty:
            st.warning("Aucune donnée à afficher pour ces filtres.")
        else:
            fig2 = crimes_by_type(filtered_df, top_n=20)
            st.plotly_chart(fig2, use_container_width=True)

    # TAB 3 : top compagnies pour un type
    with tab3:
        st.subheader("Top compagnies pour un type d'infraction")
        if not crime_types:
            st.warning("Aucun type d'infraction détecté.")
        else:
            type_for_top = st.selectbox(
                "Choisir un type d'infraction",
                options=crime_types,
                index=crime_types.index(selected_crime_type)
                if selected_crime_type in crime_types
                else 0,
            )
            df_for_top = filter_data(
                df,
                Filters(crime_type=type_for_top, departements=filters.departements),
            )
            if df_for_top.empty:
                st.warning("Aucune donnée pour ce type et ces compagnies.")
            else:
                fig3 = top_compagnies_for_type(df_for_top, type_for_top, top_n=15)
                st.plotly_chart(fig3, use_container_width=True)

    # TAB 4 : IA
    with tab4:
        st.subheader("Assistant IA — Analyse automatique")

        st.markdown("#### Génération de synthèse")
        question = st.text_input(
            "Question spécifique pour l'analyse IA (optionnel)",
            value="Quelles sont les principales différences entre les compagnies sélectionnées ?",
        )

        if st.button("Générer une analyse IA"):
            if filtered_df.empty:
                st.warning("Aucune donnée pour ces filtres.")
            else:
                grouped = filtered_df.groupby(
                    ["departement", "lib_dpt", "type_delit"],
                    as_index=False,
                )["nb_faits"].sum()

                lignes = [
                    f"- {row['lib_dpt']} ({row['departement']}), {row['type_delit']}: {int(row['nb_faits'])} faits"
                    for _, row in grouped.iterrows()
                ]
                context_text = "\n".join(lignes[:120])

                with st.spinner("Appel à l'IA en cours..."):
                    try:
                        analysis = generate_analysis_summary(context_text, question)
                        st.markdown("##### Analyse générée :")
                        st.write(analysis)
                    except Exception as e:
                        st.error(f"Erreur lors de l'appel à l'IA : {e}")

        st.markdown("---")
        st.markdown("#### Chatbot statistiques")
        user_msg = st.text_input(
            "Posez une question à l'assistant :",
            value="Que peut-on dire de la répartition des infractions en 2021 ?",
        )

        if st.button("Envoyer au chatbot"):
            with st.spinner("Réponse de l'IA..."):
                try:
                    context_hint = (
                        f"Année couverte : 2021. "
                        f"Nombre de lignes filtrées : {len(filtered_df)}."
                    )
                    answer = chatbot_answer(user_msg, context_hint=context_hint)
                    st.write(answer)
                except Exception as e:
                    st.error(f"Erreur lors de l'appel au chatbot IA : {e}")


if __name__ == "__main__":
    main()
