import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from utils import load_data
import analyses

# Initialisation de l'app
app = dash.Dash(__name__)
app.title = "Analyse pédagogique"
server = app.server  # Pour déploiement si besoin

# Chargement des données depuis fichier local
datasets = load_data(source="local")

# Accès aux différents DataFrames
df_corr = datasets["studyCorrelation"]
df_format = datasets["courseFormat"]
df_mid = datasets["midtermScores"]
df_appr = datasets["approachGains"]
df_time = datasets["completionTimes"]

# Définition du layout de l'application
app.layout = html.Div([
    html.H1("Dashboard d’analyse pédagogique", style={'textAlign': 'center'}),

    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Heures d’étude vs Score", value="tab-1"),
        dcc.Tab(label="Format de cours vs Certification", value="tab-2"),
        dcc.Tab(label="Comparaison Classe A/B", value="tab-3"),
        dcc.Tab(label="Progression par Méthode", value="tab-4"),
        dcc.Tab(label="Temps d’Achèvement", value="tab-5"),
    ]),

    html.Div(id="tab-content")
])


# Callbacks pour afficher le contenu selon l’onglet choisi
@app.callback(Output("tab-content", "children"),
              Input("tabs", "value"))
def render_content(tab):
    if tab == "tab-1":
        fig, conclusion = analyses.correlation_study_hours(df_corr)
        return html.Div([
            html.H3("Corrélation entre les heures d’étude et le score"),
            dcc.Graph(figure=fig),
            html.P(conclusion)
        ])
    elif tab == "tab-2":
        fig, conclusion = analyses.success_by_course_format(df_format)
        return html.Div([
            html.H3("Impact du format de cours sur la certification"),
            dcc.Graph(figure=fig),
            html.P(conclusion)
        ])
    elif tab == "tab-3":
        fig, conclusion = analyses.compare_midterm_scores(df_mid)
        return html.Div([
            html.H3("Scores de mi-parcours : Classe A vs Classe B"),
            dcc.Graph(figure=fig),
            html.P(conclusion)
        ])
    elif tab == "tab-4":
        fig, conclusion = analyses.analyse_gains_par_methode(df_appr)
        return html.Div([
            html.H3("Progression moyenne selon la méthode pédagogique"),
            dcc.Graph(figure=fig),
            html.P(conclusion)
        ])
    elif tab == "tab-5":
        fig, conclusion = analyses.temps_achevement_par_support(df_time)
        return html.Div([
            html.H3("Temps d’achèvement selon le support pédagogique"),
            dcc.Graph(figure=fig),
            html.P(conclusion)
        ])
    else:
        return html.Div([html.H3("Onglet inconnu.")])


# Exécution de l'application
if __name__ == "__main__":
    app.run(debug=True)
