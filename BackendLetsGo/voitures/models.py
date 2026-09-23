from django.db import models
from django.conf import settings

class Voiture(models.Model):
    # Relation nécessaire : Propriétaire du véhicule (Conducteur)
    conducteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='voitures',verbose_name="Conducteur")
    model_voiture = models.CharField(max_length=50, verbose_name="Modèle du véhicule", help_text="Ex: Corolla, 208")
    marque_voiture = models.CharField(max_length=50, verbose_name="Marque du véhicule", help_text="Ex: Toyota, Peugeot")
    plaque = models.CharField(max_length=20, unique=True, verbose_name="Plaque d'immatriculation")
    nombres_de_places = models.PositiveIntegerField(default=4, verbose_name="Nombre de places disponibles")
    couleur = models.CharField(max_length=30,  blank=True,  null=True, verbose_name="Couleur")
    est_climatisee = models.BooleanField( default=False, verbose_name="Véhicule climatisé")
    photo_voiture = models.ImageField(upload_to='voitures/', blank=True, null=True, verbose_name="Photo de la voiture")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_Maj = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.marque_voiture} {self.model_voiture} ({self.plaque})"