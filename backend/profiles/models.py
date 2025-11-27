from django.db import models


from accounts.models import JobSeeker

class Experience(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        
        
        return f"{self.title} chez {self.company}"


class Formation(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='formations')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Skill(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')])

    def __str__(self):
        return f"{self.name} ({self.level})"



# profiles/models.py - Ajouter ce modèle
class CVHistory(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='cv_histories')
    cv = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.file_name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if self.cv:
            self.file_name = self.cv.name
        super().save(*args, **kwargs)












class PersonalInfo(models.Model):
    user = models.OneToOneField(JobSeeker, on_delete=models.CASCADE, related_name='personal_info')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return f"Personal info - {self.user.user.email}"

class Language(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Débutant'),
        ('Intermediate', 'Intermédiaire'),
        ('Fluent', 'Courant'),
        ('Native', 'Natif')
    ]
    
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.level})"

class Project(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.CharField(max_length=500, help_text="Technologies utilisées (séparées par des virgules)")
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Certification(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"