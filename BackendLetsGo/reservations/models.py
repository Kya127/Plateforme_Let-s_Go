from django.db import models
from django.conf import settings
from trajets.models import Trajet

class Reservation(models.Model):
    class StatutReservation(models.TextChoices):
        CONFIRMEE = 'CONFIRMEE', 'Confirmée'
        ANNULEE = 'ANNULEE', 'Annulée'

    passager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Passager"
    )
    trajet = models.ForeignKey(
        Trajet,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Trajet"
    )
    nombre_de_places = models.PositiveIntegerField(
        default=1,
        verbose_name="Nombre de places réservées"
    )
    statut = models.CharField(
        max_length=20,
        choices=StatutReservation.choices,
        default=StatutReservation.CONFIRMEE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Réservation #{self.id} par {self.passager} ({self.statut})"