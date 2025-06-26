import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, ttest_ind, f_oneway

# 1. Corrélation heures d’étude / score
def correlation_study_hours(df):
    df = df.dropna(subset=['heures_etude', 'score_final'])
    corr, p_value = pearsonr(df['heures_etude'], df['score_final'])
    fig = px.scatter(df, x='heures_etude', y='score_final', trendline='ols',
                     title='Heures d’étude vs Score final',
                     labels={'heures_etude': 'Heures d’étude', 'score_final': 'Score final'})
    conclusion = (
        f"Le nombre d’heures d’étude hebdomadaires et le score final sont corrélés positivement (r = {corr:.2f}). "
        f"La relation est statistiquement {'significative' if p_value < 0.05 else 'non significative'} (p = {p_value:.4f}). "
        + ("Cela suggère que les étudiants qui étudient plus ont tendance à obtenir de meilleurs scores."
           if p_value < 0.05 else
           "On ne peut pas conclure qu’un plus grand nombre d’heures d’étude améliore le score.")
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
    taux_presentiel = pivot_percent.loc['presentiel', 'oui'] if 'presentiel' in pivot_percent.index else 0
    taux_distanciel = pivot_percent.loc['distanciel', 'oui'] if 'distanciel' in pivot_percent.index else 0
    conclusion = (
        f"En présentiel, environ {taux_presentiel:.1f}% des apprenants ont obtenu la certification, "
        f"contre {taux_distanciel:.1f}% en distanciel. "
        "Cela suggère que le format présentiel est potentiellement plus favorable à la réussite."
    )
    return fig, conclusion

# 3. Comparaison notes mi-parcours classes A vs B
def compare_midterm_scores(df):
    a = df[df['classe'] == 'A']['note_mi_parcours']
    b = df[df['classe'] == 'B']['note_mi_parcours']
    stat, pval = ttest_ind(a, b, nan_policy='omit')
    fig = px.box(df, x='classe', y='note_mi_parcours',
                 title="Notes de mi-parcours : Classe A vs B",
                 labels={'classe': 'Classe', 'note_mi_parcours': 'Note'})
    conclusion = (
        f"La classe A a une moyenne de {a.mean():.2f}, la classe B une moyenne de {b.mean():.2f}. "
        f"La différence est {'significative' if pval < 0.05 else 'non significative'} (p = {pval:.4f}). "
        + ("Cela peut refléter un déséquilibre pédagogique ou organisationnel."
           if pval < 0.05 else
           "Les performances sont équivalentes entre les deux classes.")
    )
    return fig, conclusion

# 4. Approche pédagogique → progression
def analyse_gains_par_methode(df):
    df['progression'] = df['progression'].astype(float)
    groups = [group['progression'].dropna() for _, group in df.groupby('methode')]
    means = df.groupby('methode')['progression'].mean().sort_values(ascending=False)
    stat, pval = f_oneway(*groups)
    fig = px.box(df, x='methode', y='progression',
                 title="Progression par méthode pédagogique",
                 labels={'methode': 'Méthode', 'progression': 'Progression'})
    meilleur = means.idxmax()
    conclusion = (
        f"La progression moyenne varie selon les méthodes. La méthode {meilleur} montre les meilleurs gains avec {means.max():.2f} points en moyenne. "
        f"L’ANOVA indique que cette différence est {'significative' if pval < 0.05 else 'non significative'} (p = {pval:.4f}). "
        + ("Il est conseillé d’explorer les bonnes pratiques de cette méthode pour en tirer des leçons pédagogiques."
           if pval < 0.05 else
           "Aucune méthode ne se démarque clairement en termes d’efficacité.")
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
    plus_rapide = group_means.idxmin()
    conclusion = (
        f"Les apprenants avec un support '{plus_rapide}' terminent les exercices en moyenne plus rapidement ({group_means.min():.1f} min). "
        f"L’analyse statistique montre que ces différences sont {'significatives' if pval < 0.05 else 'non significatives'} (p = {pval:.4f}). "
        + ("Cela confirme l’intérêt d’un accompagnement pédagogique adapté."
           if pval < 0.05 else
           "Le niveau de support n’a pas d’impact statistique fort sur la rapidité d’achèvement.")
    )
    return fig, conclusion
