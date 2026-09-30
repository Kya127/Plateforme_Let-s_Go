import requests
import json
import time
import urllib.parse
from django.conf import settings

def creer_demande_paiement_paytech(commission):
    """
    Envoie la requête à l'API PayTech pour générer le lien de paiement Wave/Orange Money.
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "API_KEY": settings.PAYTECH_API_KEY,
        "API_SECRET": settings.PAYTECH_API_SECRET,
    }

    # Référence unique interne pour réconcilier le paiement lors du webhook (avec timestamp pour éviter le rejet 'ref_command existe deja')
    ref_commande = f"COMM-{commission.id}-{commission.trajet.id}-{int(time.time())}"

    # URLs de redirection après paiement ou annulation (retour direct sur la page trajet prévu)
    local_success_url = f"{settings.FRONTEND_URL}/vue-trajet?id={commission.trajet.id}&status=success&ref={ref_commande}&commission_id={commission.id}"
    local_cancel_url = f"{settings.FRONTEND_URL}/vue-trajet?id={commission.trajet.id}&status=cancelled"

    # PayTech / Intech exige une URL HTTPS valide avec un domaine public (rejette 'localhost' et 'http://').
    # En environnement de dev local (http://localhost), on utilise une passerelle de redirection HTTPS sécurisée
    # qui renvoie instantanément (302) le navigateur vers le frontend local.
    if settings.FRONTEND_URL.startswith("https://") and "localhost" not in settings.FRONTEND_URL:
        success_url = local_success_url
        cancel_url = local_cancel_url
    else:
        success_url = f"https://httpbin.org/redirect-to?url={urllib.parse.quote(local_success_url)}"
        cancel_url = f"https://httpbin.org/redirect-to?url={urllib.parse.quote(local_cancel_url)}"

    payload = {
        "item_name": f"Commission Trajet #{commission.trajet.id}",
        "item_price": int(commission.montant),  # PayTech attend un montant entier en XOF
        "currency": "XOF",
        "ref_command": ref_commande,
        "command_name": f"Paiement commission Let's Go - Trajet #{commission.trajet.id}",
        "env": "test",  # Mode sandbox/test pour les simulations
        "ipn_url": "https://votre-domaine.com/api/commissions/webhook-paytech/",
        "success_url": success_url,
        "cancel_url": cancel_url,
        "custom_field": json.dumps({
            "commission_id": commission.id,
            "conducteur_id": commission.conducteur.id
        })
    }

    try:
        response = requests.post(settings.PAYTECH_URL, json=payload, headers=headers, timeout=15)
        res_data = response.json()

        # Succès PayTech : renvoie success = 1 et le lien de redirection
        if response.status_code == 200 and res_data.get("success") == 1:
            return {
                "success": True,
                "redirect_url": res_data.get("redirect_url"),
                "token": res_data.get("token"),
                "ref_command": ref_commande
            }
        else:
            return {
                "success": False,
                "error": res_data.get("error", [response.text])
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }