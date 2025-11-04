import pandas as pd
import numpy as np
import re, string, os
import spacy
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from tqdm import tqdm

# === Initialisation des modèles ===
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("french"))
nlp = spacy.load("fr_core_news_sm")
model = SentenceTransformer("TechWolf/JobBERT-v2")

# === Fonctions utilitaires ===

def clean_text(text):
    if not isinstance(text, str):
        return ""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.text not in string.punctuation]
    return " ".join(tokens)

def combine_fields(row):
    parts = []
    parts.append((row.get("title", "") or "") * 3)
    parts.append((row.get("skills", "") or "") * 2)
    parts.append(row.get("description", "") or "")
    parts.append(row.get("experience", "") or "")
    parts.append(row.get("contract", "") or "")
    parts.append(row.get("region", "") or "")
    parts.append(row.get("salary", "") or "")
    parts.append(row.get("job_type", "") or "")
    parts.append(row.get("work_mode", "") or "")
    return " ".join(parts)

def extract_pdf_text(file_path):
    reader = PyPDF2.PdfReader(file_path)
    all_text = []
    for p in reader.pages:
        txt = p.extract_text()
        if txt:
            all_text.append(txt)
    return "\n".join(all_text)

def preprocess_resume(text):
    if not isinstance(text, str):
        return ""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.text not in string.punctuation]
    return " ".join(tokens)

def embed_resume(text):
    cleaned = preprocess_resume(text)
    return model.encode([cleaned])[0]

def extract_keywords_from_text(text):
    if not isinstance(text, str):
        text = str(text)
    words = re.findall(r"\b\w+\b", text.lower())
    numeric_values = re.findall(r"\d{1,2}", text)
    return set(words), numeric_values

def compute_metadata_score(row, resume_text):
    bonus = 0.0
    resume_words, resume_nums = extract_keywords_from_text(resume_text)
    job_text = " ".join(map(str, row.to_list()))
    job_words, job_nums = extract_keywords_from_text(job_text)

    if any(word in job_words for word in resume_words):
        bonus += 0.03

    common_contracts = ["cdi", "cdd", "stage", "freelance", "alternance", "intérim"]
    if any(c in resume_words and c in job_words for c in common_contracts):
        bonus += 0.03

    for n in resume_nums:
        if n in job_nums:
            bonus += 0.02
            break

    if isinstance(row.get("salary"), str) and any(
        s in row["salary"].lower() for s in ["dt", "€", "usd", "dinar", "par mois", "par an"]
    ):
        bonus += 0.01

    shared_terms = len(resume_words.intersection(job_words))
    if shared_terms > 30:
        bonus += 0.04
    elif shared_terms > 15:
        bonus += 0.02

    return min(bonus, 0.1)

def rank_jobs(resume_vec, job_vectors, jobs_df, resume_text, top_n=10):
    scores = cosine_similarity([resume_vec], job_vectors)[0]
    jobs_df = jobs_df.copy()
    jobs_df["semantic_score"] = scores
    jobs_df["metadata_bonus"] = jobs_df.apply(lambda r: compute_metadata_score(r, resume_text), axis=1)
    jobs_df["final_score"] = jobs_df["semantic_score"] + jobs_df["metadata_bonus"]
    ranked = jobs_df.sort_values("final_score", ascending=False).head(top_n)
    ranked["semantic_score"] = ranked["semantic_score"].round(3)
    ranked["metadata_bonus"] = ranked["metadata_bonus"].round(3)
    ranked["final_score"] = ranked["final_score"].round(3)
    return ranked

# === Fonction principale ===
def match_resume_with_jobs(resume_path, jobs_csv_path, top_n=10):
    jobs_df = pd.read_csv(jobs_csv_path, dtype=str).fillna("")
    cols = ["title", "company", "description", "skills", "experience",
            "contract", "region", "salary", "job_type", "work_mode"]
    jobs_df = jobs_df[cols].copy()
    jobs_df["full_text"] = jobs_df.apply(combine_fields, axis=1)
    jobs_df["clean_text"] = jobs_df["full_text"].apply(clean_text)
    job_vectors = model.encode(jobs_df["clean_text"].tolist(), batch_size=64, show_progress_bar=False)

    resume_text = extract_pdf_text(resume_path)
    resume_vec = embed_resume(resume_text)

    ranked_jobs = rank_jobs(resume_vec, job_vectors, jobs_df, resume_text, top_n)
    return ranked_jobs
