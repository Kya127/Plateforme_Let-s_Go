from django.urls import path
from .views import (
    InitierPaiementCommissionView,
    ObtenirOuCreerCommissionTrajetView,
    ValiderPaiementCommissionView,
    webhook_paytech
)

urlpatterns = [
    # Récupérer ou créer la commission pour un trajet
    path('trajet/<int:trajet_id>/', ObtenirOuCreerCommissionTrajetView.as_view(), name='commission-trajet'),
    
    # Initier le paiement PayTech (Wave / OM)
    path('<int:commission_id>/payer/', InitierPaiementCommissionView.as_view(), name='initier-paiement-commission'),
    
    # Valider / débiter directement le compte (Wave / OM)
    path('<int:commission_id>/valider-paiement/', ValiderPaiementCommissionView.as_view(), name='valider-paiement-commission'),
    
    # Route (Webhook) appelée automatiquement par PayTech en arrière-plan
    path('webhook-paytech/', webhook_paytech, name='webhook-paytech'),
]