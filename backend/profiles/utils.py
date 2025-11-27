# profiles/utils.py
def profile_completeness(user):
    """
    Version simplifiée et sécurisée du calcul de complétude
    """
    try:
        # Vérifications de base avec gestion des erreurs
        has_experiences = user.experiences.exists() if hasattr(user, 'experiences') else False
        has_formations = user.formations.exists() if hasattr(user, 'formations') else False
        has_skills = user.skills.exists() if hasattr(user, 'skills') else False
        has_cv = bool(user.cv) if hasattr(user, 'cv') else False
        
        
        
        has_personal_info = hasattr(user, 'personal_info') and all([
            user.personal_info.phone,
            user.personal_info.address,
            user.personal_info.city,
            user.personal_info.country,
            user.personal_info.postal_code,
            user.personal_info.date_of_birth,
            user.personal_info.nationality,
            user.personal_info.linkedin_url,
            user.personal_info.github_url,
            user.personal_info.portfolio_url

        ])

        has_lunguages = user.languages.exists() if hasattr(user, 'languages') else False
        has_certifications = user.certifications.exists() if hasattr(user, 'certifications') else False
        has_projects = user.projects.exists() if hasattr(user, 'projects') else False


        
        filled_fields = sum([has_experiences, has_formations, has_skills, has_cv, has_personal_info, has_lunguages, has_certifications, has_projects])
        percentage = (filled_fields / 8) * 100
        
        return int(percentage)
        
    except Exception as e:
        print(f"Erreur dans profile_completeness: {e}")
        # Retourner une valeur par défaut en cas d'erreur
        return 0