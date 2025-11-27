# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re, string
import spacy
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from pathlib import Path

# === Initialisation des modèles ===
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("french"))

# Spacy léger pour tokenisation
nlp = spacy.load("fr_core_news_sm")

# Sentence Transformer
model = SentenceTransformer("TechWolf/JobBERT-v2")

# === Préparation rapide du texte ===
def fast_clean(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = [w for w in text.split() if w not in stop_words]
    return " ".join(tokens)

# === Concaténer les champs utiles pour le matching ===
def combine_fields(row):
    parts = []
    parts.append((row.get("title", "") or "") * 3)
    parts.append((row.get("skills", "") or "") * 2)
    parts.append(row.get("full_description", "") or "")
    parts.append(row.get("experience", "") or "")
    parts.append(row.get("region", "") or "")
    parts.append(row.get("sector", "") or "")
    parts.append(row.get("education", "") or "")
    parts.append(row.get("date", "") or "")
    return " ".join(parts)

# === Extraire texte PDF CV ===
def extract_pdf_text(file_path):
    reader = PyPDF2.PdfReader(file_path)
    all_text = []
    for p in reader.pages:
        txt = p.extract_text()
        if txt:
            all_text.append(txt)
    return "\n".join(all_text)

# === Prétraitement du CV ===
def preprocess_resume(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = [w for w in text.split() if w not in stop_words]
    return " ".join(tokens)

def embed_resume(text):
    cleaned = preprocess_resume(text)
    return model.encode([cleaned])[0]

# === Score bonus simple basé sur mots communs et chiffres ===
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

    # correspondance chiffres (expérience, date)
    for n in resume_nums:
        if n in job_nums:
            bonus += 0.02
            break

    # mots communs
    shared_terms = len(resume_words.intersection(job_words))
    if shared_terms > 30:
        bonus += 0.04
    elif shared_terms > 15:
        bonus += 0.02

    return min(bonus, 0.1)

# === Ranking final ===
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

# === PRE-CALCUL DES EMBEDDINGS JOBS (à faire une seule fois) ===
def prepare_jobs_embeddings(jobs_csv_path, embeddings_path=None):
    jobs_df = pd.read_csv(jobs_csv_path, dtype=str).fillna("")

    matching_cols = ["title", "skills", "full_description", "experience", "region", "sector", "education", "date"]
    for col in matching_cols:
        if col not in jobs_df.columns:
            jobs_df[col] = ""

    jobs_df["full_text"] = jobs_df.apply(combine_fields, axis=1)
    jobs_df["clean_text"] = jobs_df["full_text"].apply(fast_clean)

    job_vectors = model.encode(jobs_df["clean_text"].tolist(), batch_size=64, show_progress_bar=True)

    if embeddings_path:
        np.save(embeddings_path, job_vectors)

    return jobs_df, job_vectors

# === Fonction principale (API rapide) ===
def match_resume_with_jobs(resume_path, jobs_csv_path, top_n=10, embeddings_path=None):
    # Charger CSV + embeddings pré-calculés
    jobs_df = pd.read_csv(jobs_csv_path, dtype=str).fillna("")
    if embeddings_path and Path(embeddings_path).exists():
        job_vectors = np.load(embeddings_path)
    else:
        # fallback : calculer embeddings si fichier manquant
        matching_cols = ["title", "skills", "full_description", "experience", "region", "sector", "education", "date"]
        for col in matching_cols:
            if col not in jobs_df.columns:
                jobs_df[col] = ""
        jobs_df["full_text"] = jobs_df.apply(combine_fields, axis=1)
        jobs_df["clean_text"] = jobs_df["full_text"].apply(fast_clean)
        job_vectors = model.encode(jobs_df["clean_text"].tolist(), batch_size=64, show_progress_bar=True)

    # Extraire et encoder le CV
    resume_text = extract_pdf_text(resume_path)
    resume_vec = embed_resume(resume_text)

    ranked_jobs = rank_jobs(resume_vec, job_vectors, jobs_df, resume_text, top_n)
    return ranked_jobs
