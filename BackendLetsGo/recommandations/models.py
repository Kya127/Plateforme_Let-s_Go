from django.db import models
from django.conf import settings


class HistoriqueRecherche(models.Model):
    """
    Enregistre les recherches de trajets (manuelles et vocales)
    pour alimenter le moteur de suggestions dynamiques.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recherches_trajets',
        null=True,
        blank=True,
        verbose_name="Utilisateur"
    )
    lieu_depart = models.CharField(max_length=255, verbose_name="Lieu de départ")
    destination = models.CharField(max_length=255, verbose_name="Lieu d'arrivée")
    date_voulue = models.DateField(null=True, blank=True, verbose_name="Date souhaitée")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de recherche")

    class Meta:
        verbose_name = "Historique de recherche"
        verbose_name_plural = "Historiques de recherches"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['lieu_depart', 'destination']),
        ]

    def __str__(self):
        user_nom = self.user.get_full_name() if self.user else "Visiteur anonyme"
        return f"[{self.created_at.strftime('%d/%m/%Y %H:%M')}] {user_nom} : {self.lieu_depart} ➔ {self.destination}"
