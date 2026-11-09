"""
Dashboard Ventes — application Streamlit (Jedha M8 J3)
Lancer : streamlit run streamlit.py
Thème : .streamlit/config.toml
"""

# =============================================================================
# IMPORTS
# =============================================================================
# streamlit = bibliothèque pour créer une app web avec du Python (sans HTML)
import streamlit as st

# pandas = tableaux de données (DataFrame), comme Excel en Python
import pandas as pd

# plotly.express = graphiques interactifs (zoom, survol…)
import plotly.express as px

# datetime = gestion des dates et heures
import datetime


# =============================================================================
# CONFIGURATION DE LA PAGE
# Doit être la PREMIÈRE commande Streamlit du fichier (règle officielle).
# =============================================================================
st.set_page_config(
    page_title="Dashboard Ventes",      # texte de l'onglet du navigateur
    page_icon="📊",                     # icône de l'onglet
    layout="wide",                      # "wide" = pleine largeur ; "centered" = étroit
    initial_sidebar_state="expanded",   # sidebar ouverte au démarrage
)


# =============================================================================
# MENU DE NAVIGATION (sidebar = bandeau à gauche)
# La variable `page` décide quelle section afficher plus bas.
# =============================================================================
# radio = liste verticale de choix (plus claire qu'un selectbox pour 3 pages)
page = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Analyse", "Graphiques"],
)


# =============================================================================
# PAGE 1 — ACCUEIL
# =============================================================================
if page == "Accueil":
    # Titre principal (gros texte en haut)
    st.title("Bienvenue sur le Dashboard")

    # Texte simple (markdown / texte brut)
    st.write(
        "Ceci est la page d'accueil avec un résumé des informations principales."
    )

    # Lien cliquable grâce au Markdown [texte](url)
    st.markdown(
        "Pour en savoir plus sur Streamlit, visitez "
        "[la documentation](https://docs.streamlit.io/library)."
    )

    # Image depuis une URL publique (ou un chemin local type "logo.png")
    # use_container_width=True = l'image s'adapte à la largeur disponible
    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png",
        caption="Logo Streamlit",
        use_container_width=True,
    )

    # KPI : chiffre important + variation (delta)
    st.metric(label="Nombre de visiteurs", value="3000", delta="+12%")

    st.write(
        "Ce dashboard est conçu pour vous fournir une vue d'ensemble rapide "
        "de vos données et analyses."
    )


# =============================================================================
# PAGE 2 — ANALYSE (widgets + tableau)
# =============================================================================
elif page == "Analyse":
    st.title("Analyse des données")
    st.write("Cette page contient des tableaux et statistiques des ventes.")

    # --- Widgets : l'utilisateur choisit → Streamlit RE-exécute tout le script ---
    # selectbox = menu déroulant
    option = st.selectbox(
        "Choisissez une catégorie",
        ["Catégorie A", "Catégorie B", "Catégorie C"],
    )

    # slider = curseur numérique (min, max, valeur par défaut)
    valeur = st.slider(
        "Sélectionner une valeur",
        min_value=0, max_value=100, value=50, step=1
    )

    # Affiche les choix (f-string = injecte les variables dans le texte)
    st.write(f"Catégorie sélectionnée : {option}")
    st.write(f"Valeur choisie : {valeur}")

    # Sélecteurs de date (retourne un objet datetime.date)
    st.date_input("Date de début", value=datetime.date.today() - datetime.timedelta(days=30))
    st.date_input("Date de fin", value=datetime.date.today())

    # Petit DataFrame fictif (en vrai projet : pd.read_csv(...))
    data = pd.DataFrame(
        {
            "Produit": ["Produit 1", "Produit 2", "Produit 3"],
            "Ventes": [100, 200, 150],
        }
    )

    # Tableau statique (pas de tri interactif)
    st.table(data)

    # Bouton de téléchargement CSV
    # .to_csv() → texte ; .encode("utf-8") → octets exigés par download_button
    st.download_button(
        label="Télécharger les données",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="ventes.csv",
        mime="text/csv",
    )

    # Bouton qui ouvre une URL dans un nouvel onglet
    st.link_button(
        "Voir la documentation du link_button",
        "https://docs.streamlit.io/develop/api-reference/widgets/st.link_button",
    )


# =============================================================================
# PAGE 3 — GRAPHIQUES
# =============================================================================
elif page == "Graphiques":
    st.title("Visualisations interactives")

    # Dataset simulé (jours × ventes / commandes / clients)
    df_data = pd.DataFrame(
        {
            "Jour": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
            "Ventes": [100, 150, 200, 170, 220],
            "Commandes": [15, 60, 10, 36, 87],
            "Clients": [5, 8, 12, 7, 10],
        }
    )

    # L'utilisateur choisit quelle colonne tracer
    variable = st.selectbox(
        "Choisissez la variable à visualiser",
        ["Ventes", "Commandes", "Clients"],
    )

    # Deux colonnes côte à côte (mise en page)
    col1, col2 = st.columns(2)

    # Graphique linéaire natif Streamlit (rapide, simple)
    # set_index("Jour") → l'axe X devient les jours
    col1.header(f"Évolution de {variable}")
    col1.line_chart(df_data.set_index("Jour")[variable])

    # Graphique en barres natif Streamlit
    col2.header(f"Répartition de {variable} par jour")
    col2.bar_chart(df_data.set_index("Jour")[variable])

    # Scatter Plotly (plus riche : taille, couleur, zoom)
    st.subheader(f"Scatter Plot interactif de {variable}")
    fig = px.scatter(
        df_data,
        x="Jour",
        y=variable,
        size=variable,           # taille des bulles = valeur
        color=variable,          # couleur = valeur
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=50,
        title=f"Scatter Plot de {variable} par jour",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Expander = zone repliable (détails à la demande)
    with st.expander("Détails supplémentaires"):
        st.write("Données complètes utilisées pour les visualisations :")
        st.dataframe(df_data)  # tableau interactif (tri, scroll)
