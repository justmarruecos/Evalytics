import pandas as pd
import json
import requests  # Pour charger proprement le JSON depuis l'URL


def load_data(source="local"):
    """
    Charge les données depuis un fichier local ou une URL, puis transforme chaque bloc en DataFrame.
    """
    if source == "url":
        url = "https://rnddf-185-226-32-80.a.free.pinggy.link/data"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lève une erreur si l'URL échoue (ex : 404)
            data = json.loads(response.text)  # Convertit le texte JSON en dictionnaire Python
        except Exception as e:
            print("Erreur de chargement depuis l'URL :", e)
            return {}
    else:
        try:
            with open("studyCorrelation.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("Erreur de chargement depuis fichier local :", e)
            return {}

    datasets = {}

    # === 1. Corrélation heures / score ===
    sc = pd.DataFrame(data.get("studyCorrelation", []))
    sc.rename(columns={"hours": "heures_etude", "score": "score_final"}, inplace=True)
    datasets["studyCorrelation"] = sc

    # === 2. Format cours (présentiel/distanciel) ===
    cf = data.get("courseFormat", {})
    df_cf = []
    for format_type, stats in cf.items():
        for status, count in stats.items():
            certifie = "oui" if status == "pass" else "non"
            df_cf.append({
                "format_cours": format_type,
                "certifie": certifie,
                "nombre": count
            })
    datasets["courseFormat"] = pd.DataFrame(df_cf)

    # === 3. Mi-parcours classes A vs B ===
    midterm = data.get("midtermScores", {})
    a_scores = midterm.get("class_A", [])
    b_scores = midterm.get("class_B", [])
    df_mid = pd.DataFrame({
        "classe": ["A"] * len(a_scores) + ["B"] * len(b_scores),
        "note_mi_parcours": a_scores + b_scores
    })
    datasets["midtermScores"] = df_mid

    # === 4. Progression selon méthode pédagogique ===
    ap = data.get("approachGains", {})
    rows = []
    for methode, gains in ap.items():
        for val in gains:
            rows.append({"methode": methode, "progression": val})
    datasets["approachGains"] = pd.DataFrame(rows)

    # === 5. Temps d’achèvement selon support pédagogique ===
    ct = data.get("completionTimes", {})
    rows = []
    for niveau, temps in ct.items():
        label = {
            "None": "Sans support",
            "Simple": "Support basique",
            "Advanced": "Support détaillé"
        }.get(niveau, niveau)
        for val in temps:
            rows.append({"niveau_support": label, "temps_achevement": val})
    datasets["completionTimes"] = pd.DataFrame(rows)

    return datasets
