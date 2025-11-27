import re
import PyPDF2
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


# -------------------------------------------------------
# 🔹 Charger modèle PHI-2 (2.7B) optimisé pour CPU
# -------------------------------------------------------

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)



# -------------------------------------------------------
# 🔹 Extraction texte PDF
# -------------------------------------------------------
def extract_pdf_text(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text = []
    for page in reader.pages:
        p = page.extract_text()
        if p:
            text.append(p)
    return "\n".join(text)


# -------------------------------------------------------
# 🔹 Extraction des informations du CV
# -------------------------------------------------------
def extract_cv_info(cv_text):
    info = {}

    info["name"] = cv_text.split("\n")[0].strip()

    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", cv_text)
    info["email"] = email.group(0) if email else ""

    phone = re.search(r"\+?\d[\d\s-]{7,}", cv_text)
    info["phone"] = phone.group(0) if phone else ""

    city = re.search(r"Tunis|Sousse|Sfax|[A-Z][a-z]+", cv_text)
    info["city"] = city.group(0) if city else ""

    skills = re.search(
        r"(SKILLS|COMPÉTENCES)\s*(.*?)\s*(LANGUAGES|EXPERIENCE|EXPERIENCES|FORMATION)",
        cv_text,
        re.DOTALL | re.IGNORECASE
    )
    info["skills"] = skills.group(2).replace("\n", ", ") if skills else ""

    edu = re.search(
        r"(EDUCATION|FORMATION)\s*(.*?)\s*(SKILLS|COMPÉTENCES|EXPERIENCE)",
        cv_text,
        re.DOTALL | re.IGNORECASE
    )
    info["education"] = edu.group(2).replace("\n", ", ") if edu else ""

    return info





# -------------------------------------------------------
# 🔹 Génération lettre
# -------------------------------------------------------
def generate_cover_letter_from_job(cv_path=None, cv_text=None, ranked_jobs=None, job_index=0):
    if cv_text:
        text = cv_text
    elif cv_path:
        text = extract_pdf_text(cv_path)
    else:
        raise ValueError("cv_path ou cv_text est requis")

    cv_info = extract_cv_info(text)

    if ranked_jobs is None or ranked_jobs.empty:
        return "Aucun job trouvé."

    job_info = ranked_jobs.iloc[job_index].to_dict()

    

    prompt = f"Écris une lettre de motivation courte pour {job_info['title']} chez {job_info['company']} avec le candidat  {cv_info['name']} qui a {cv_info['skills']} ."



    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)



    
    outputs = model.generate(
    **inputs,
    max_new_tokens=200,  # Réduit pour plus de cohérence
    temperature=0.3,  # Moins créatif, plus déterministe
    top_p=0.7,  # Contrôle la diversité
    repetition_penalty=2.0,  # Détourne les répétitions
    no_repeat_ngram_size=5,  # Empêche les répétitions de phrases
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

    
    # Extraction de la réponse seulement

 

    
  


    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 🔹 Extraire seulement la lettre
    if "Madame, Monsieur" in full_output:
        letter = full_output.split("Madame, Monsieur", 1)[1]
        letter = "Madame, Monsieur" + letter
    else:
        letter = full_output.strip()

    return letter




