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

    # Nouveaux champs pour la complétude du profil
    is_verified = models.BooleanField(default=False)  # Validé par l'admin après vérification des papiers
    permis_conduire = models.FileField(upload_to='documents/permis/', blank=True, null=True)
    carte_grise = models.FileField(upload_to='documents/cni/', blank=True, null=True)
    assurance = models.FileField(upload_to='documents/cg/', blank=True, null=True)
    photo = models.ImageField(upload_to='photos_profil/', blank=True, null=True)

    # On utilise l'email comme identifiant principal pour la connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'telephone']

    @property
    def is_profile_complete(self):
            # 1. Vérification de base pour tout le monde (Passager & Conducteur)
            base_complete = bool(self.first_name and self.last_name and self.telephone and self.email)
            
            # 2. Si l'utilisateur est Conducteur (ou demande à le devenir), il faut TOUS les documents
            if self.role == self.Role.CONDUCTEUR:
                return base_complete and bool(self.permis_conduire and self.carte_grise and self.assurance and self.photo)
            
            # 3. Pour un Passager, la base suffit
            return base_complete

    
    #     """Vérifie si les informations de base sont renseignées."""
    #     return bool(self.first_name and self.last_name and self.telephone and self.email)

    def __str__(self):
         return f"{self.first_name} {self.last_name} ({self.role})"

