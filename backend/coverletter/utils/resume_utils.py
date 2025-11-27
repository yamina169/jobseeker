

from jobseeker_backend.matching.logic import extract_pdf_text


import re
from collections import Counter

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

def build_resume_brief(pdf_path):
    text = extract_pdf_text(pdf_path)
    # extrait email / phone (ex)
    emails = EMAIL_RE.findall(text)
    email = emails[0] if emails else ""
    skills = _extract_skills(text)
    summary = _simple_summary(text)
    return {"raw_text": text, "email": email, "top_skills": skills, "summary": summary}

def _extract_skills(text, top_k=8):
    words = re.findall(r"\b[a-zA-Zàâééèêëîïôûùüç\-]+\b", text.lower())
    stop = {"le","la","de","des","et","en","un","une"}
    words = [w for w in words if w not in stop and len(w)>2]
    common = Counter(words).most_common()
    return [w for w,_ in common][:top_k]

def _simple_summary(text, max_sent=3):
    sents = re.split(r'(?<=[\.\?\!])\s+', text)
    return " ".join(sents[:max_sent])
