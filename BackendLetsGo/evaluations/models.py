from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from trajets.models import Trajet


class Evaluation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="evaluations")
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="evaluations_donnees",)
    destinataire = models.ForeignKey(
    settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="evaluations_recues",)
    note = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    commentaire = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un utilisateur ne peut évaluer qu'une seule fois la même personne sur un même trajet
        unique_together = ("trajet", "auteur", "destinataire")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note {self.note}/5 par {self.auteur.first_name} pour {self.destinataire.first_name}"