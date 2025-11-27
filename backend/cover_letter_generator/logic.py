import ollama
from fpdf import FPDF
from PyPDF2 import PdfReader

def safe_ollama_generate(model, prompt):
    try:
        return ollama.generate(model=model, prompt=prompt)["response"]
    except Exception as e:
        raise RuntimeError(f"Ollama error: {str(e)}")

def clean_text(text):
    replacements = {
        "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def create_pdf(content, filename, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Arial", "", 12)
    content = clean_text(content)
    pdf.multi_cell(0, 8, content)
    pdf.output(filename)
    return filename

def extract_name_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    first_page = reader.pages[0]
    text = first_page.extract_text()
    if not text:
        return None
    # Exemple simple: on prend la première ligne comme nom
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if len(line.split()) >= 2:  # prénom + nom
            return line
    return None

def generate_cover_letter(name, cv_file, job_description, model_name="gemma3"):
    # Extraire contenu texte du CV pour l'utiliser
    reader = PdfReader(cv_file)
    cv_text = ""
    for page in reader.pages:
        cv_text += page.extract_text() + "\n"

    prompt = f"""
Write a professional cover letter for {name} applying for this job:
{job_description}

CV content:
{cv_text}

Address it to 'Dear Hiring Manager,' and close with 'Sincerely, {name}'.
Keep it concise and professional.
"""
    return safe_ollama_generate(model_name, prompt)
