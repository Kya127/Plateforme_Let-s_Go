from django.db import models
from django.conf import settings
from voitures.models import Voiture


# ==============================================================================
# MODÈLES DE TARIFICATION ET RÉFÉRENTIEL DES ZONES
# ==============================================================================

class ZoneTarifaire(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Code de la zone")
    nom = models.CharField(max_length=150, verbose_name="Nom complet de la zone")
    description = models.CharField(max_length=255, blank=True, verbose_name="Description de la zone")

    class Meta:
        verbose_name = "Zone tarifaire"
        verbose_name_plural = "Zones tarifaires"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.nom}"


class LieuZone(models.Model):
    class TypeLieu(models.TextChoices):
        QUARTIER = 'QUARTIER', 'Quartier / Cité / Commune'
        REPERE = 'REPERE', 'Repère / Carrefour / Équipement'

    zone = models.ForeignKey(
        ZoneTarifaire,
        on_delete=models.CASCADE,
        related_name='lieux',
        verbose_name="Zone tarifaire associée"
    )
    nom = models.CharField(max_length=150, unique=True, verbose_name="Nom du lieu ou repère")
    type_lieu = models.CharField(
        max_length=50,
        choices=TypeLieu.choices,
        default=TypeLieu.QUARTIER,
        verbose_name="Type de lieu"
    )

    class Meta:
        verbose_name = "Lieu de zone"
        verbose_name_plural = "Lieux de zones"
        ordering = ['zone__code', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.zone.code})"


class GrilleTarifaire(models.Model):
    zone_depart = models.ForeignKey(
        ZoneTarifaire,
        on_delete=models.CASCADE,
        related_name='tarifs_depart',
        verbose_name="Zone de départ"
    )
    zone_arrivee = models.ForeignKey(
        ZoneTarifaire,
        on_delete=models.CASCADE,
        related_name='tarifs_arrivee',
        verbose_name="Zone d'arrivée"
    )
    prix_par_place = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix par place fixé (FCFA)"
    )

    class Meta:
        verbose_name = "Tarif zone à zone"
        verbose_name_plural = "Grille tarifaire"
        unique_together = ('zone_depart', 'zone_arrivee')

    def __str__(self):
        return f"{self.zone_depart.code} ➔ {self.zone_arrivee.code} : {int(self.prix_par_place)} FCFA"


# ==============================================================================
# MODÈLE TRAJET PRINCIPAL
# ==============================================================================

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

    conducteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trajets_publies',
        verbose_name="Conducteur"
    )
    voiture = models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name='trajets',
        verbose_name="Voiture utilisée"
    )
    lieu_depart = models.CharField(max_length=255, verbose_name="Lieu de départ")
    destination = models.CharField(max_length=255, verbose_name="Lieu d'arrivée")
    zone_depart = models.ForeignKey(
        ZoneTarifaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trajets_depart',
        verbose_name="Zone de départ"
    )
    zone_destination = models.ForeignKey(
        ZoneTarifaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trajets_arrivee',
        verbose_name="Zone d'arrivée"
    )
    date = models.DateField(verbose_name="Date de départ")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    places_disponibles = models.PositiveIntegerField(verbose_name="Places disponibles")
    prix_par_place = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix par place (FCFA)"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Note aux passagers")
    statut = models.CharField(
        max_length=20,
        choices=StatutTrajet.choices,
        default=StatutTrajet.PLANIFIE
    )
    preferences = models.JSONField(default=list, blank=True, verbose_name="Préférences du trajet")

    # Télémétrie et Géolocalisation en direct
    latitude_actuelle = models.FloatField(null=True, blank=True, verbose_name="Latitude actuelle du véhicule")
    longitude_actuelle = models.FloatField(null=True, blank=True, verbose_name="Longitude actuelle du véhicule")
    cap_actuel = models.FloatField(null=True, blank=True, verbose_name="Cap / Orientation (degrés)")
    vitesse_actuelle = models.FloatField(null=True, blank=True, verbose_name="Vitesse actuelle (km/h)")
    tracking_actif = models.BooleanField(default=False, verbose_name="Tracking en direct actif")
    derniere_position_at = models.DateTimeField(null=True, blank=True, verbose_name="Horodatage dernière position")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ['date']

    def __str__(self):
        return f"{self.lieu_depart} ➔ {self.destination} ({self.date.strftime('%d/%m/%Y')} à {self.heure_depart.strftime('%H:%M')})"

    def save(self, *args, **kwargs):
        # Sécurisation et forçage du prix par place selon la grille officielle de la plateforme
        from .services_tarification import resoudre_prix_trajet, trouver_zone_pour_lieu
        if self.lieu_depart and self.destination:
            prix_officiel = resoudre_prix_trajet(self.lieu_depart, self.destination)
            if prix_officiel is not None:
                self.prix_par_place = prix_officiel
            code_dep = trouver_zone_pour_lieu(self.lieu_depart)
            code_dest = trouver_zone_pour_lieu(self.destination)
            if code_dep and not self.zone_depart_id:
                self.zone_depart = ZoneTarifaire.objects.filter(code=code_dep).first()
            if code_dest and not self.zone_destination_id:
                self.zone_destination = ZoneTarifaire.objects.filter(code=code_dest).first()
        super().save(*args, **kwargs)

    def reserver_places(self, nombre):
        if nombre > self.places_disponibles:
            raise ValueError("Nombre de places insuffisant.")
        self.places_disponibles -= nombre
        self.save()

    def liberer_places(self, nombre):
        self.places_disponibles += nombre
        self.save()