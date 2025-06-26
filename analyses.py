import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, ttest_ind, f_oneway

# 1. Corrélation heures d’étude / score
def correlation_study_hours(df):
    df = df.dropna(subset=['heures_etude', 'score_final'])
    corr, p_value = pearsonr(df['heures_etude'], df['score_final'])
    fig = px.scatter(df, x='heures_etude', y='score_final',
                     title='Heures d’étude vs Score final',
                     labels={'heures_etude': 'Heures d’étude', 'score_final': 'Score final'})
    conclusion = f"Corrélation de {corr:.2f} (p = {p_value:.4f}). " + (
        "Lien significatif." if p_value < 0.05 else "Pas de lien significatif."
    )
    return fig, conclusion

# 2. Présentiel vs distanciel → taux de certification
def success_by_course_format(df):
    pivot = df.pivot_table(index='format_cours', columns='certifie', values='nombre', fill_value=0)
    pivot_percent = pivot.div(pivot.sum(axis=1), axis=0) * 100
    fig = px.bar(pivot_percent.reset_index(), x='format_cours', y=['oui', 'non'],
                 title="Taux de certification selon le format de cours",
                 labels={'value': 'Pourcentage', 'format_cours': 'Format de cours'},
                 barmode='stack')
    conclusion = "Le graphique montre les différences de certification entre cours présentiels et distanciels."
    return fig, conclusion

# 3. Comparaison notes mi-parcours classes A vs B
def compare_midterm_scores(df):
    a = df[df['classe'] == 'A']['note_mi_parcours']
    b = df[df['classe'] == 'B']['note_mi_parcours']
    stat, pval = ttest_ind(a, b, nan_policy='omit')
    fig = px.box(df, x='classe', y='note_mi_parcours',
                 title="Notes de mi-parcours : Classe A vs B")
    conclusion = f"Test t : t = {stat:.2f}, p = {pval:.4f}. " + (
        "Différence significative." if pval < 0.05 else "Aucune différence significative."
    )
    return fig, conclusion

# 4. Approche pédagogique → progression
def analyse_gains_par_methode(df):
    df['progression'] = df['progression'].astype(float)
    groups = [group['progression'].dropna() for _, group in df.groupby('methode')]
    stat, pval = f_oneway(*groups)
    fig = px.box(df, x='methode', y='progression',
                 title="Progression par méthode pédagogique")
    conclusion = f"ANOVA : F = {stat:.2f}, p = {pval:.4f}. " + (
        "Il existe des différences significatives." if pval < 0.05 else "Pas de différence significative."
    )
    return fig, conclusion

# 5. Support pédagogique → temps d’achèvement
def temps_achevement_par_support(df):
    df = df.dropna(subset=['temps_achevement', 'niveau_support'])
    group_means = df.groupby('niveau_support')['temps_achevement'].mean()
    groups = [group['temps_achevement'].dropna() for _, group in df.groupby('niveau_support')]
    stat, pval = f_oneway(*groups)
    fig = px.bar(group_means.reset_index(), x='niveau_support', y='temps_achevement',
                 title="Temps moyen d’achèvement selon le niveau du support",
                 labels={'niveau_support': 'Support', 'temps_achevement': 'Temps moyen (min)'})
    conclusion = f"ANOVA : F = {stat:.2f}, p = {pval:.4f}. " + (
        "Différences de temps significatives." if pval < 0.05 else "Pas de différences significatives."
    )
    return fig, conclusion
