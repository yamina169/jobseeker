import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import re
from nltk.corpus import stopwords
import nltk
from pathlib import Path

nltk.download("stopwords", quiet=True)
STOP_WORDS = set(stopwords.words("french"))

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "data" / "offres_unifiees.csv"
OUTPUT_FILE = BASE_DIR / "data" / "jobs_with_embeddings.csv.gz"

# Nettoyage léger
def fast_clean(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(w for w in text.split() if w and w not in STOP_WORDS)

# Lire CSV existant
df = pd.read_csv(CSV_FILE, dtype=str).fillna("")

# Concaténer champs pour embeddings
df["full_text"] = df.apply(lambda r: " ".join([
    (r.get("title") or "")*3,
    (r.get("skills") or "")*2,
    r.get("full_description") or "",
    r.get("experience") or "",
    r.get("region") or "",
    r.get("sector") or "",
    r.get("education") or "",
    r.get("date") or ""
]), axis=1)

df["clean_text"] = df["full_text"].apply(fast_clean)

# Calcul embeddings
model = SentenceTransformer("TechWolf/JobBERT-v2")
texts = df["clean_text"].tolist()
embeddings = model.encode(texts, batch_size=64, show_progress_bar=True, convert_to_numpy=True)

# Ajouter embeddings au DataFrame
emb_df = pd.DataFrame(embeddings.tolist(), columns=[f"dim_{i}" for i in range(embeddings.shape[1])])
jobs_emb_df = pd.concat([df.reset_index(drop=True), emb_df], axis=1)

# Sauvegarder dans un CSV compressé
jobs_emb_df.to_csv(OUTPUT_FILE, index=False, compression="gzip", encoding="utf-8-sig")
print(f"✔ Embeddings sauvegardés dans {OUTPUT_FILE} (shape={jobs_emb_df.shape})")
