import pandas as pd
import numpy as np
import re, string, os
import spacy
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

# === Initialisation des modèles ===
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("french"))

# Charger spaCy et le modèle seulement une fois (évite rechargement à chaque appel)
_nlp = None
_model = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("fr_core_news_sm", disable=["ner", "parser"])
    return _nlp

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("TechWolf/JobBERT-v2")
    return _model

# === Fonctions utilitaires ===
def clean_text(text):
    if not isinstance(text, str):
        return ""
    nlp = get_nlp()
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.text not in string.punctuation]
    return " ".join(tokens)

def combine_fields(row):
    fields = [
        (row.get("title", "") or "") * 3,
        (row.get("skills", "") or "") * 2,
        row.get("description", ""),
        row.get("experience", ""),
        row.get("contract", ""),
        row.get("region", ""),
        row.get("salary", ""),
        row.get("job_type", ""),
        row.get("work_mode", ""),
    ]
    return " ".join(fields)

def extract_pdf_text(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text = "\n".join([p.extract_text() or "" for p in reader.pages])
    return text

def preprocess_resume(text):
    if not isinstance(text, str):
        return ""
    nlp = get_nlp()
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.text not in string.punctuation]
    return " ".join(tokens)

def embed_resume(text):
    model = get_model()
    cleaned = preprocess_resume(text)
    return model.encode([cleaned], show_progress_bar=False, convert_to_numpy=True)[0]

def compute_metadata_score(row, resume_words, resume_nums):
    job_text = " ".join(map(str, row.to_list()))
    job_words = set(re.findall(r"\b\w+\b", job_text.lower()))
    job_nums = re.findall(r"\d{1,2}", job_text)

    bonus = 0.0
    if resume_words & job_words:
        bonus += 0.03

    if any(c in resume_words and c in job_words for c in ["cdi", "cdd", "stage", "freelance", "alternance", "intérim"]):
        bonus += 0.03

    if any(n in job_nums for n in resume_nums):
        bonus += 0.02

    if isinstance(row.get("salary"), str) and any(s in row["salary"].lower() for s in ["dt", "€", "usd", "dinar", "par mois", "par an"]):
        bonus += 0.01

    shared_terms = len(resume_words & job_words)
    if shared_terms > 30:
        bonus += 0.04
    elif shared_terms > 15:
        bonus += 0.02

    return min(bonus, 0.1)

def rank_jobs(resume_vec, job_vectors, jobs_df, resume_words, resume_nums, top_n=10):
    scores = cosine_similarity([resume_vec], job_vectors)[0]
    jobs_df = jobs_df.copy()
    jobs_df["semantic_score"] = scores

    # Calcul vectorisé pour le bonus via map (plus rapide que apply avec nlp)
    jobs_df["metadata_bonus"] = [compute_metadata_score(row, resume_words, resume_nums) for _, row in jobs_df.iterrows()]
    jobs_df["final_score"] = jobs_df["semantic_score"] + jobs_df["metadata_bonus"]

    ranked = jobs_df[jobs_df["final_score"] >= 0.6].nlargest(top_n, "final_score")
    return ranked.round(3)

def match_resume_with_jobs(resume_path, jobs_csv_path, top_n=10):
    model = get_model()
    jobs_df = pd.read_csv(jobs_csv_path, dtype=str).fillna("")

    cols = ["title", "company", "description", "skills", "experience", "contract", "region", "salary", "job_type", "work_mode"]
    jobs_df = jobs_df[cols]

    jobs_df["full_text"] = jobs_df.apply(combine_fields, axis=1)

    # Nettoyage plus rapide : éviter NLP complet si non nécessaire
    jobs_df["clean_text"] = jobs_df["full_text"].str.lower().str.replace(rf"[{string.punctuation}]", "", regex=True)

    # Encodage des offres (mise en cache possible)
    job_vectors = model.encode(jobs_df["clean_text"].tolist(), batch_size=128, show_progress_bar=False, convert_to_numpy=True)

    # Prétraitement et encodage du CV
    resume_text = extract_pdf_text(resume_path)
    resume_vec = embed_resume(resume_text)

    resume_words = set(re.findall(r"\b\w+\b", resume_text.lower()))
    resume_nums = re.findall(r"\d{1,2}", resume_text)

    ranked_jobs = rank_jobs(resume_vec, job_vectors, jobs_df, resume_words, resume_nums, top_n)
    return ranked_jobs