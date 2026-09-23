from django.db import models
from django.conf import settings
from voitures.models import Voiture

class Trajet(models.Model):
    class StatutTrajet(models.TextChoices):
        PLANIFIE = 'PLANIFIE', 'Planifié'
        EN_COURS = 'EN_COURS', 'En cours'
        TERMINE = 'TERMINE', 'Terminé'
        ANNULE = 'ANNULE', 'Annulé'


    CLASS_PREFERENCES = [
        ('NON_FUMEUR', 'Non fumeur'),
        ('ANIMAUX_OK', 'Animaux ok'),
        ('GROS_BAGAGES', 'Gros bagages'),
        ('MUSIQUE_OK', 'Musique autorisée'),
    ]    

    conducteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trajets_publies', verbose_name="Conducteur")
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, related_name='trajets', verbose_name="Voiture utilisée")
    lieu_depart = models.CharField(max_length=255, verbose_name="Lieu de départ")
    destination = models.CharField(max_length=255, verbose_name="Lieu d'arrivée")
    date = models.DateField(verbose_name="Date de départ")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    places_disponibles = models.PositiveIntegerField(verbose_name="Places disponibles")
    prix_par_place = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix par place (FCFA)")
    description = models.TextField(blank=True, null=True, verbose_name="Note aux passagers")
    statut = models.CharField( max_length=20,  choices=StatutTrajet.choices,  default=StatutTrajet.PLANIFIE)
    preferences = models.JSONField(default=list, blank=True, verbose_name="Préférences du trajet")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ['date']

    def __str__(self):
        return f"{self.lieu_depart} ➔ {self.destination} ({self.date.strftime('%d/%m/%Y')} à {self.heure_depart.strftime('%H:%M')})"


    def reserver_places(self, nombre):
        if nombre > self.places_disponibles:
            raise ValueError("Nombre de places insuffisant.")
        self.places_disponibles -= nombre
        self.save()

    def liberer_places(self, nombre):
        self.places_disponibles += nombre
        self.save()