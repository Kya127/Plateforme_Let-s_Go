from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        PASSAGER = 'PASSAGER', 'Passager'
        CONDUCTEUR = 'CONDUCTEUR', 'Conducteur'
        ADMINISTRATEUR = 'ADMINISTRATEUR', 'Administrateur'

    email = models.EmailField(unique=True, verbose_name="Adresse email")
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PASSAGER,verbose_name="Rôle utilisateur")
    photo = models.ImageField(upload_to='photos_profil/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Validé par l'admin après vérification des papiers
    
    # On utilise l'email comme identifiant principal pour la connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'telephone']

    @property
    def is_profile_complete(self):
    # Un profil est complet si les infos de base et la photo sont fournies
        return bool(self.first_name and self.last_name and self.telephone and self.email and self.photo)
    
            # # 1. Vérification de base pour tout le monde (Passager & Conducteur)
            # base_complete = bool(self.first_name and self.last_name and self.telephone and self.email)
            
            # # 2. Si l'utilisateur est Conducteur (ou demande à le devenir), il faut TOUS les documents
            # if self.role == self.Role.CONDUCTEUR:
            #     return base_complete and bool(self.permis_conduire and self.carte_grise and self.assurance and self.photo)
            
            # # 3. Pour un Passager, la base suffit
            # return base_complete


    def __str__(self):
         return f"{self.first_name} {self.last_name} ({self.role})"



class VerificationDocument(models.Model):
    class Status(models.TextChoices):
        EN_ATTENTE = 'PENDING', 'En attente'
        APPROUVE = 'APPROVED', 'Approuvé'
        REJETE = 'REJECTED', 'Rejeté'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_documents')
    permis_conduire = models.FileField(upload_to='documents/permis/')
    carte_grise = models.FileField(upload_to='documents/carte_grise/')
    assurance = models.FileField(upload_to='documents/assurance/')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.EN_ATTENTE)
    motif_rejet = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de {self.user.email} - Status: {self.status}"