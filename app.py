import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Modules internes
from utils import load_data
import analyses
import layout

# Initialisation de l'application Dash avec un thème professionnel
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Tableau de bord Edutech+"
server = app.server  # nécessaire pour déploiement éventuel

def serve_layout():
    """Génère le layout dynamique à chaque ouverture, en rechargeant les données."""
    # 1. Chargement des données depuis le JSON en ligne, avec repli local
    datasets = load_data(source="url")
    if not datasets or "studyCorrelation" not in datasets:
        print("⚠️ Échec du chargement en ligne, utilisation des données locales.")
        datasets = load_data(source="local")

    # Extraction des DataFrames préparés
    df_corr = datasets["studyCorrelation"]
    df_format = datasets["courseFormat"]
    df_mid = datasets["midtermScores"]
    df_appr = datasets["approachGains"]
    df_time = datasets["completionTimes"]

    # 2. Calcul des visualisations et des conclusions statistiques
    fig_corr, conclusion_corr = analyses.correlation_study_hours(df_corr)
    fig_format, conclusion_format = analyses.success_by_course_format(df_format)
    fig_mid, conclusion_mid = analyses.compare_midterm_scores(df_mid)
    fig_appr, conclusion_appr = analyses.analyse_gains_par_methode(df_appr)
    fig_time, conclusion_time = analyses.temps_achevement_par_support(df_time)

    # 3. Construction du layout complet avec les figures et textes générés
    figures = {
        "corr": fig_corr,
        "format": fig_format,
        "classes": fig_mid,
        "methods": fig_appr,
        "support": fig_time
    }
    texts = {
        "corr": conclusion_corr,
        "format": conclusion_format,
        "classes": conclusion_mid,
        "methods": conclusion_appr,
        "support": conclusion_time
    }

    return layout.make_layout(figures, texts)

# Affecter dynamiquement le layout à chaque chargement de la page
app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
