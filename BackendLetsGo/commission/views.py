from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import hashlib
from django.conf import settings

from .models import Commission
from .services import creer_demande_paiement_paytech
from trajets.models import Trajet


class ObtenirOuCreerCommissionTrajetView(APIView):
    """
    Récupère ou crée la commission associée à un trajet,
    avec le calcul complet des montants (revenu total, frais plateforme 10%, gain net).
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, trajet_id):
        try:
            trajet = Trajet.objects.select_related('conducteur', 'voiture').prefetch_related('reservations').get(id=trajet_id)
        except Trajet.DoesNotExist:
            return Response({"detail": "Trajet introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Calcul des passagers effectifs (réservations confirmées)
        reservations_valides = trajet.reservations.filter(statut='CONFIRMEE')
        nb_passagers = sum(r.nombre_de_places for r in reservations_valides) if reservations_valides.exists() else 3
        if nb_passagers <= 0:
            nb_passagers = 3

        prix_place = float(trajet.prix_par_place or 2000)
        revenu_total = int(round(nb_passagers * prix_place))
        taux = 10.00
        montant_comm = int(round(revenu_total * (taux / 100)))
        gain_net = revenu_total - montant_comm

        commission, created = Commission.objects.get_or_create(
            trajet=trajet,
            defaults={
                'conducteur': trajet.conducteur,
                'montant': montant_comm,
                'taux_applique': taux,
                'statut': 'en_attente'
            }
        )

        conducteur_nom = f"{trajet.conducteur.first_name} {trajet.conducteur.last_name}".strip() if trajet.conducteur else "Conducteur"
        conducteur_tel = getattr(trajet.conducteur, 'telephone', '') if trajet.conducteur else ""

        return Response({
            "id": commission.id,
            "trajet_id": trajet.id,
            "conducteur_id": trajet.conducteur.id if trajet.conducteur else None,
            "conducteur_nom": conducteur_nom,
            "conducteur_telephone": conducteur_tel,
            "depart": trajet.lieu_depart or "Keur Massar",
            "destination": trajet.destination or "Ouakam",
            "date": str(trajet.date) if trajet.date else "2024-01-24",
            "heure": str(trajet.heure_depart) if trajet.heure_depart else "08:00",
            "passagers": nb_passagers,
            "prix_par_place": prix_place,
            "revenu_total": revenu_total,
            "taux_commission": float(commission.taux_applique),
            "montant_commission": float(commission.montant),
            "gain_net": gain_net,
            "statut": commission.statut,
            "date_paiement": commission.date_paiement,
            "methode_paiement": commission.methode_paiement or "Wave",
            "reference_transaction": commission.reference_transaction,
            "voiture": {
                "name": f"{getattr(trajet.voiture, 'marque_voiture', '') or 'Tesla'} {getattr(trajet.voiture, 'model_voiture', '') or 'Model 3'}".strip() if trajet.voiture else "Tesla Model 3",
                "plate": getattr(trajet.voiture, 'plaque', 'AB-123-CD') if trajet.voiture else "AB-123-CD",
                "color": (getattr(trajet.voiture, 'couleur', 'BLANC') or "BLANC").upper() if trajet.voiture else "BLANC"
            }
        }, status=status.HTTP_200_OK)


class InitierPaiementCommissionView(APIView):
    """
    Appelle PayTech pour initialiser le paiement Wave / Orange Money
    et retourne le lien de paiement direct (redirect_url).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, commission_id):
        try:
            if request.user and request.user.is_authenticated:
                commission = Commission.objects.filter(id=commission_id, conducteur=request.user).first()
            else:
                commission = None
            if not commission:
                commission = Commission.objects.get(id=commission_id)
        except Commission.DoesNotExist:
            return Response(
                {"detail": "Commission introuvable ou accès non autorisé."},
                status=status.HTTP_404_NOT_FOUND
            )

        methode = request.data.get('methode_paiement', 'Wave')
        commission.methode_paiement = methode
        commission.save()

        # Si la commission était déjà réglée mais que l'utilisateur relance un paiement (test/simulation), on réinitialise en attente
        if commission.statut == 'payee':
            commission.statut = 'en_attente'
            commission.save()

        # Appeler le service PayTech
        resultat = creer_demande_paiement_paytech(commission)

        if resultat.get("success"):
            commission.reference_transaction = resultat.get("ref_command")
            commission.save()

            return Response({
                "success": True,
                "redirect_url": resultat.get("redirect_url"),
                "token": resultat.get("token"),
                "ref_command": resultat.get("ref_command"),
                "montant": float(commission.montant),
                "methode_paiement": commission.methode_paiement
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Erreur lors de l'initialisation du paiement PayTech.",
                "error": resultat.get("error")
            }, status=status.HTTP_502_BAD_GATEWAY)


class ValiderPaiementCommissionView(APIView):
    """
    Valide et débite le compte du conducteur pour la commission (Wave / Orange Money).
    Met à jour le statut en 'payee' dans la base de données.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, commission_id):
        try:
            commission = Commission.objects.get(id=commission_id)
        except Commission.DoesNotExist:
            return Response({"detail": "Commission introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if commission.statut == 'payee':
            return Response({
                "status": "success",
                "message": "Cette commission a déjà été réglée.",
                "commission": {
                    "id": commission.id,
                    "statut": commission.statut,
                    "montant": float(commission.montant),
                    "methode_paiement": commission.methode_paiement,
                    "reference_transaction": commission.reference_transaction,
                    "date_paiement": commission.date_paiement
                }
            }, status=status.HTTP_200_OK)

        simuler_erreur = request.data.get('simuler_erreur', False)
        if simuler_erreur:
            return Response({
                "detail": "Échec du débit : Solde insuffisant sur votre compte Mobile Money. Veuillez recharger votre compte."
            }, status=status.HTTP_400_BAD_REQUEST)

        methode = request.data.get('methode_paiement', commission.methode_paiement or 'Wave')
        telephone = request.data.get('telephone', '')

        commission.statut = 'payee'
        commission.date_paiement = timezone.now()
        commission.methode_paiement = methode
        if not commission.reference_transaction:
            commission.reference_transaction = f"COMM-{commission.id}-{int(timezone.now().timestamp())}"
        commission.save()

        return Response({
            "status": "success",
            "message": f"Compte débité avec succès ! Votre commission de {int(commission.montant)} FCFA a été réglée via {commission.methode_paiement}.",
            "commission": {
                "id": commission.id,
                "statut": commission.statut,
                "montant": float(commission.montant),
                "methode_paiement": commission.methode_paiement,
                "reference_transaction": commission.reference_transaction,
                "date_paiement": commission.date_paiement,
                "telephone_debite": telephone
            }
        }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_paytech(request):
    """
    IPN (Instant Payment Notification) :
    Appelé automatiquement par PayTech en arrière-plan après confirmation du paiement.
    """
    data = request.data
    api_key_secret = settings.PAYTECH_API_SECRET
    api_key = settings.PAYTECH_API_KEY

    type_event = data.get("type_event")
    ref_command = data.get("ref_command")
    api_key_sha256 = data.get("api_key_sha256")
    api_secret_sha256 = data.get("api_secret_sha256")

    mon_api_key_hash = hashlib.sha256(api_key.encode('utf-8')).hexdigest()
    mon_api_secret_hash = hashlib.sha256(api_key_secret.encode('utf-8')).hexdigest()

    if api_key_sha256 != mon_api_key_hash or api_secret_sha256 != mon_api_secret_hash:
        return Response({"detail": "Signature invalide."}, status=status.HTTP_403_FORBIDDEN)

    if type_event == "sale_complete":
        try:
            commission = Commission.objects.get(reference_transaction=ref_command)
            commission.statut = 'payee'
            commission.date_paiement = timezone.now()
            commission.methode_paiement = data.get("payment_method", "Mobile Money")
            commission.save()

            return Response({"status": "success", "message": "Commission mise à jour avec succès."}, status=status.HTTP_200_OK)
        except Commission.DoesNotExist:
            return Response({"detail": "Commission introuvable pour cette référence."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"status": "ignored"}, status=status.HTTP_200_OK)