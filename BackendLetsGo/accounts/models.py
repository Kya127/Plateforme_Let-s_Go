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
    fcm_token = models.CharField(max_length=255, blank=True, null=True, verbose_name="Token Firebase FCM")
    
    # On utilise l'email comme identifiant principal pour la connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'telephone']

    @property
    def is_profile_complete(self):
    # Un profil est complet si les infos de base et la photo sont fournies
        return bool(self.first_name and self.last_name and self.telephone and self.email and self.photo)


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
    photo_vehicule = models.ImageField(upload_to='verification_vehicles/',null=True, blank=True,help_text="Photo du véhicule pour la vérification initiale de son état.")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.EN_ATTENTE)
    motif_rejet = models.TextField(blank=True, null=True, help_text="Motif expliquant le rejet du dossier (rempli par l'administrateur)." )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de {self.user.email} - Status: {self.status}"