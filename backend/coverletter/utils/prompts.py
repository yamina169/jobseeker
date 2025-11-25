# coverletter/utils/prompts.py
LETTER_TEMPLATE = """
Tonalité: {tone}
Résumé du candidat:
{resume_summary}
Compétences clés: {skills}

Offre:
Titre: {job_title}
Entreprise: {company}
Description: {job_description}

Instructions:
- Rédige une lettre de motivation en français adaptée à l'offre.
- Ne pas inventer d'expériences.
- Sois précis et concis.
- Longueur: {length_pref}
"""
