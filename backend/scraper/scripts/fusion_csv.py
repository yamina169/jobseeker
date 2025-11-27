# -*- coding: utf-8 -*-
import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_DIR = BASE_DIR / "data" / "offres_brutes"

CSV_FILES = {
    "emploitunisie": CSV_DIR / "emploitunisie.csv",
    "farojob": CSV_DIR / "farojob.csv",
    "keejob": CSV_DIR / "keejob.csv",
}

OUTPUT_FILE = BASE_DIR / "data" / "offres_unifiees.csv"

UNIFIED_COLUMNS = [
    "job_id",
    "source",
    "title",
    "company",
    "region",
    "sector",
    "short_description",
    "full_description",
    "education",
    "experience",
    "contract",
    "skills",
    "salary",
    "date",
    "url"
]

MAX_JOBS = 500  # Limite maximale du fichier unifié

def normalize_dataframe(df, source):
    """Standardise les colonnes uniquement pour le fichier unifié."""
    df = df.copy().astype(str).fillna("")

    if source == "emploitunisie":
        df.rename(columns={"description": "short_description"}, inplace=True)
        df["full_description"] = df.get("full_description", "")
        df["salary"] = ""
    elif source == "farojob":
        df.rename(columns={
            "location": "region",
            "category": "sector",
            "description": "full_description",
            "date_posted": "date"
        }, inplace=True)
        df["short_description"] = ""
        df["education"] = ""
        df["experience"] = ""
        df["contract"] = ""
        df["skills"] = ""
        df["salary"] = ""
    elif source == "keejob":
        if "date" not in df.columns:
            df["date"] = df.get("date", "")

    # S'assurer que toutes les colonnes existent dans le dataframe
    for col in UNIFIED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df["source"] = source
    return df

def fusion_csv():
    dfs = []
    files_used = []

    for source, path in CSV_FILES.items():
        if not path.exists():
            print(f"[INFO] Fichier manquant : {path}")
            continue

        df = pd.read_csv(path, dtype=str, encoding="utf-8").fillna("")
        df = normalize_dataframe(df, source)

        dfs.append(df)
        files_used.append(str(path))

    if not dfs:
        print("⚠ Aucun CSV à fusionner.")
        return

    merged = pd.concat(dfs, ignore_index=True, sort=False)
    merged = merged.fillna("")

    # Lire le fichier existant pour limiter le nombre total
    if OUTPUT_FILE.exists():
        existing = pd.read_csv(OUTPUT_FILE, dtype=str, encoding="utf-8").fillna("")
        new_jobs = merged.copy()  # nouvelles offres à ajouter
        total_after_merge = pd.concat([existing, new_jobs], ignore_index=True, sort=False)

        if len(total_after_merge) > MAX_JOBS:
            # Supprimer les plus anciens pour accueillir toutes les nouvelles offres
            nb_new = len(new_jobs)
            total_after_merge = total_after_merge.iloc[nb_new:].reset_index(drop=True)

        merged = total_after_merge

    # Recalculer les job_id
    merged["job_id"] = range(1, len(merged) + 1)

    # Réordonner colonnes : UNIFIED_COLUMNS en tête, puis le reste
    other_cols = [c for c in merged.columns if c not in UNIFIED_COLUMNS]
    merged = merged[UNIFIED_COLUMNS + other_cols]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"✔ Fusion terminée : {len(merged)} jobs dans {OUTPUT_FILE}")
    return {
        "status": "ok",
        "merged": len(merged),
        "output": str(OUTPUT_FILE),
        "files": files_used
    }

if __name__ == "__main__":
    fusion_csv()
