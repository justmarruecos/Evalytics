from dash import dcc, html

def make_layout(figures, stats_texts):
    return html.Div([
        html.H1("Tableau de bord Edutech+", style={"textAlign": "center"}),

        dcc.Tabs([
            dcc.Tab(label="Corrélation Heures / Score", children=[
                dcc.Graph(figure=figures["corr"]),
                html.P(stats_texts["corr"])
            ]),
            dcc.Tab(label="Format Cours & Certification", children=[
                dcc.Graph(figure=figures["format"]),
                html.P(stats_texts["format"])
            ]),
            dcc.Tab(label="Classes A vs B", children=[
                dcc.Graph(figure=figures["classes"]),
                html.P(stats_texts["classes"])
            ]),
            dcc.Tab(label="Méthodes Pédagogiques", children=[
                dcc.Graph(figure=figures["methods"]),
                html.P(stats_texts["methods"])
            ]),
            dcc.Tab(label="Support & Achèvement", children=[
                dcc.Graph(figure=figures["support"]),
                html.P(stats_texts["support"])
            ]),
        ])
    ])
