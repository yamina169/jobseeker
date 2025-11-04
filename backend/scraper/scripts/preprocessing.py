# preprocess_jobs.py
import pandas as pd
import re, html
from pathlib import Path


INPUT = "data/offres_brutes/all_jobs_combined.csv " 


OUTPUT = "data/all_jobs_cleaned.csv"
Path("data").mkdir(exist_ok=True)

def clean_text(s):
    if pd.isna(s): return ""
    s = str(s)
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)          # enlever HTML
    s = re.sub(r"http\S+", " ", s)         # enlever URLs
    s = re.sub(r"[^\wÀ-ÖØ-öø-ÿ\s\-,.;:()']", " ", s)  # garder accents
    s = re.sub(r"\s+", " ", s).strip()
    return s

df = pd.read_csv(INPUT, dtype=str, encoding="utf-8", low_memory=False)
text_cols = ["title","company","description","education","experience","skills","region","location"]
for c in text_cols:
    if c in df.columns:
        df[c] = df[c].fillna("").apply(clean_text)

# concaténation utile pour embeddings
df["joined_text"] = (df.get("title","") + " . " + df.get("company","") + " . " + df.get("description","")).str.strip()

# supprimer doublons stricts
df.drop_duplicates(subset=["title","company","description"], inplace=True)

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
print("Saved cleaned:", OUTPUT)