from django.db import models
from django.conf import settings
from trajets.models import Trajet 

class Commission(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
    ]

    # Relation vers le trajet concerné
    trajet = models.OneToOneField('trajets.Trajet', on_delete=models.CASCADE, related_name='commission')
    
    # Conducteur redevable de la commission
    conducteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='commissions'
    )
    
    # Attributs selon le diagramme UML
    taux_applique = models.DecimalField(max_digits=5, decimal_places=2, default=10.00) # Ex: 10%
    montant = models.DecimalField(max_digits=10, decimal_places=2) # Montant calculé en FCFA
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_paiement = models.DateTimeField(null=True, blank=True)
    methode_paiement = models.CharField(max_length=50, null=True, blank=True) # Ex: 'Wave', 'Orange Money'
    reference_transaction = models.CharField(max_length=255, null=True, blank=True, unique=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission Trajet #{self.trajet.id} - {self.conducteur} - {self.statut}"