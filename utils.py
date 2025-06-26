import pandas as pd
import json


def load_data(source="local"):
    if source == "url":
        url = "https://edumail.fr/formations/realtimedata.json"
        try:
            data = pd.read_json(url)
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

    # 1. Corrélation : convertir en DataFrame et renommer colonnes
    sc = pd.DataFrame(data.get("studyCorrelation", []))
    sc.rename(columns={"hours": "heures_etude", "score": "score_final"}, inplace=True)
    datasets["studyCorrelation"] = sc

    # 2. Format cours
    cf = data.get("courseFormat", {})
    df_cf = []
    for format_type, stats in cf.items():
        for status, count in stats.items():
            certifie = "oui" if status == "pass" else "non"
            df_cf.append({"format_cours": format_type, "certifie": certifie, "nombre": count})
    datasets["courseFormat"] = pd.DataFrame(df_cf)

    # 3. Mi-parcours
    midterm = data.get("midtermScores", {})
    a_scores = midterm.get("class_A", [])
    b_scores = midterm.get("class_B", [])
    df_mid = pd.DataFrame({
        "classe": ["A"] * len(a_scores) + ["B"] * len(b_scores),
        "note_mi_parcours": a_scores + b_scores
    })
    datasets["midtermScores"] = df_mid

    # 4. Approche pédagogique
    ap = data.get("approachGains", {})
    rows = []
    for methode, gains in ap.items():
        for val in gains:
            rows.append({"methode": methode, "progression": val})
    datasets["approachGains"] = pd.DataFrame(rows)

    # 5. Temps d’achèvement
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
