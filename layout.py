from dash import dcc, html
import dash_bootstrap_components as dbc

def make_layout(figures, stats_texts):
    return dbc.Container([
        html.H1("Tableau de bord Edutech+", style={"textAlign": "center", "marginTop": "30px"}),

        dcc.Tabs([
            dcc.Tab(label="Corrélation Heures / Score", children=[
                dcc.Graph(figure=figures["corr"]),
                html.P(stats_texts["corr"], style={"padding": "10px"})
            ]),
            dcc.Tab(label="Format Cours & Certification", children=[
                dcc.Graph(figure=figures["format"]),
                html.P(stats_texts["format"], style={"padding": "10px"})
            ]),
            dcc.Tab(label="Classes A vs B", children=[
                dcc.Graph(figure=figures["classes"]),
                html.P(stats_texts["classes"], style={"padding": "10px"})
            ]),
            dcc.Tab(label="Méthodes Pédagogiques", children=[
                dcc.Graph(figure=figures["methods"]),
                html.P(stats_texts["methods"], style={"padding": "10px"})
            ]),
            dcc.Tab(label="Support & Achèvement", children=[
                dcc.Graph(figure=figures["support"]),
                html.P(stats_texts["support"], style={"padding": "10px"})
            ]),
        ], style={"marginTop": "30px"})
    ], fluid=True)
