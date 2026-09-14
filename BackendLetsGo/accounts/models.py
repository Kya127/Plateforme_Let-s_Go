from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        PASSAGER = 'PASSAGER', 'Passager'
        CONDUCTEUR = 'CONDUCTEUR', 'Conducteur'
        ADMINISTRATEUR = 'ADMINISTRATEUR', 'Administrateur'

    email = models.EmailField(unique=True, verbose_name="Adresse email")
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone")
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.PASSAGER,
        verbose_name="Rôle utilisateur"
    )

    # On utilise l'email comme identifiant principal pour la connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'telephone']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"