import secrets
import string
import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CodeVerification
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

def generer_code_otp(longueur=6):
    """Génère un code numérique cryptographiquement sécurisé à 6 chiffres."""
    return "".join(secrets.choice(string.digits) for _ in range(longueur))


def creer_et_envoyer_code_otp(user, canal='EMAIL'):
    """
    Génère un nouveau code OTP de vérification pour l'utilisateur,
    l'enregistre en base de données et l'envoie par e-mail.
    """
    # 1. Invalider les anciens codes d'activation non utilisés pour cet utilisateur
    CodeVerification.objects.filter(
        user=user, 
        type_code=CodeVerification.TypeCode.ACTIVATION, 
        est_utilise=False
    ).update(est_utilise=True)

    # 2. Générer un nouveau code valable 15 minutes
    code = generer_code_otp(6)
    expires_at = timezone.now() + timedelta(minutes=15)

    code_obj = CodeVerification.objects.create(
        user=user,
        code=code,
        canal=canal,
        type_code=CodeVerification.TypeCode.ACTIVATION,
        expires_at=expires_at
    )

    # 3. Préparer l'e-mail
    sujet = f"Code de vérification LET'S GO : {code}"
    
    prenom = user.first_name or "Passager"
    
    corps_texte = f"""Bonjour {prenom},

Merci de vous être inscrit sur LET'S GO, la plateforme de covoiturage au Sénégal.

Votre code de confirmation pour activer votre compte est :
{code}

Ce code est valable pendant 15 minutes. Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail.

L'équipe LET'S GO
https://letsgo.sn
"""

    corps_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Code de confirmation LET'S GO</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #F8FAFC;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          color: #111627;
        }}
        .email-container {{
          max-width: 540px;
          margin: 30px auto;
          background: #FFFFFF;
          border-radius: 20px;
          border: 1px solid #E2E8F0;
          padding: 36px 32px;
          box-sizing: border-box;
        }}
        .header-brand {{
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 24px;
        }}
        .brand-logo {{
          font-size: 24px;
          font-weight: 900;
          color: #FF4D2D;
          letter-spacing: -0.5px;
          text-decoration: none;
        }}
        .greeting {{
          font-size: 18px;
          font-weight: 700;
          color: #111627;
          margin-bottom: 12px;
        }}
        .paragraph {{
          font-size: 14px;
          line-height: 1.6;
          color: #475569;
          margin-bottom: 24px;
        }}
        .code-box {{
          background: #FFF5F2;
          border: 2px dashed #FF4D2D;
          border-radius: 16px;
          padding: 20px;
          text-align: center;
          margin: 28px 0;
        }}
        .code-number {{
          font-size: 38px;
          font-weight: 900;
          color: #FF4D2D;
          letter-spacing: 8px;
          display: inline-block;
          font-family: monospace, Courier;
        }}
        .code-meta {{
          font-size: 12px;
          color: #64748B;
          margin-top: 8px;
        }}
        .footer {{
          margin-top: 32px;
          padding-top: 20px;
          border-top: 1px solid #F1F5F9;
          font-size: 12px;
          color: #94A3B8;
          text-align: center;
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="header-brand">
          <span class="brand-logo">LET'S GO</span>
        </div>
        <div class="greeting">Bonjour {prenom},</div>
        <p class="paragraph">
          Bienvenue sur <strong>LET'S GO</strong> ! Pour sécuriser votre compte et finaliser votre inscription, veuillez renseigner le code de vérification suivant :
        </p>
        <div class="code-box">
          <div class="code-number">{code}</div>
          <div class="code-meta"> Valable pendant 15 minutes</div>
        </div>
        <p class="paragraph">
          Saisissez ces 6 chiffres sur l'écran de confirmation pour activer immédiatement votre accès.
        </p>
        <div class="footer">
          Si vous n'avez pas demandé cette création de compte, vous pouvez ignorer ce message en toute sécurité.<br>
          © 2026 LET'S GO — Covoiturage fiable & sécurisé.
        </div>
      </div>
    </body>
    </html>
    """

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', "LET'S GO <no-reply@letsgo.sn>")

    try:
        send_mail(
            subject=sujet,
            message=corps_texte,
            from_email=from_email,
            recipient_list=[user.email],
            html_message=corps_html,
            fail_silently=False
        )
        logger.info(f"[OTP] Code envoyé avec succès à {user.email} : {code}")
        print(f"\n=========================================\n[OTP LET'S GO] Code pour {user.email} : {code}\n=========================================\n")
    except Exception as e:
        logger.error(f"[OTP] Erreur lors de l'envoi du mail à {user.email} : {e}")
        # En mode dev ou si SMTP non connecté, on logue et affiche le code dans le terminal
        print(f"\n=========================================\n[OTP LET'S GO - DEV FALLBACK] Code pour {user.email} : {code}\n(Erreur SMTP : {e})\n=========================================\n")

    return code_obj


def creer_et_envoyer_code_reset_mdp(user, canal='EMAIL'):
    """
    Génère un code OTP de réinitialisation de mot de passe pour l'utilisateur,
    l'enregistre en base de données et l'envoie par e-mail avec un template dédié.
    """
    # 1. Invalider les anciens codes de réinitialisation non utilisés pour cet utilisateur
    CodeVerification.objects.filter(
        user=user,
        type_code=CodeVerification.TypeCode.RESET_PASSWORD,
        est_utilise=False
    ).update(est_utilise=True)

    # 2. Générer un nouveau code valable 15 minutes
    code = generer_code_otp(6)
    expires_at = timezone.now() + timedelta(minutes=15)

    code_obj = CodeVerification.objects.create(
        user=user,
        code=code,
        canal=canal,
        type_code=CodeVerification.TypeCode.RESET_PASSWORD,
        expires_at=expires_at
    )

    # 3. Préparer l'e-mail de réinitialisation
    sujet = f"Réinitialisation de votre mot de passe LET'S GO : {code}"
    prenom = user.first_name or "Passager"

    corps_texte = f"""Bonjour {prenom},

Vous avez demandé la réinitialisation de votre mot de passe sur LET'S GO.

Voici votre code de confirmation à 6 chiffres :
{code}

Ce code est valable pendant 15 minutes. Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail, votre mot de passe actuel reste inchangé.

L'équipe LET'S GO
https://letsgo.sn
"""

    corps_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Réinitialisation de votre mot de passe LET'S GO</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #F8FAFC;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          color: #111627;
        }}
        .email-container {{
          max-width: 540px;
          margin: 30px auto;
          background: #FFFFFF;
          border-radius: 20px;
          border: 1px solid #E2E8F0;
          padding: 36px 32px;
          box-sizing: border-box;
        }}
        .header-brand {{
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 24px;
        }}
        .brand-logo {{
          font-size: 24px;
          font-weight: 900;
          color: #FF4D2D;
          letter-spacing: -0.5px;
          text-decoration: none;
        }}
        .greeting {{
          font-size: 18px;
          font-weight: 700;
          color: #111627;
          margin-bottom: 12px;
        }}
        .paragraph {{
          font-size: 14px;
          line-height: 1.6;
          color: #475569;
          margin-bottom: 24px;
        }}
        .code-box {{
          background: #FFF5F2;
          border: 2px dashed #FF4D2D;
          border-radius: 16px;
          padding: 20px;
          text-align: center;
          margin: 28px 0;
        }}
        .code-number {{
          font-size: 38px;
          font-weight: 900;
          color: #FF4D2D;
          letter-spacing: 8px;
          display: inline-block;
          font-family: monospace, Courier;
        }}
        .code-meta {{
          font-size: 12px;
          color: #64748B;
          margin-top: 8px;
        }}
        .security-note {{
          background: #FFFBEB;
          border: 1px solid #FDE68A;
          border-radius: 12px;
          padding: 12px 16px;
          font-size: 13px;
          color: #92400E;
          margin-top: 24px;
        }}
        .footer {{
          margin-top: 32px;
          padding-top: 20px;
          border-top: 1px solid #F1F5F9;
          font-size: 12px;
          color: #94A3B8;
          text-align: center;
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="header-brand">
          <span class="brand-logo">LET'S GO</span>
        </div>
        <div class="greeting">Bonjour {prenom},</div>
        <p class="paragraph">
          Vous avez demandé la réinitialisation de votre mot de passe sur <strong>LET'S GO</strong>.
          Voici votre code de sécurité à 6 chiffres :
        </p>
        <div class="code-box">
          <div class="code-number">{code}</div>
          <div class="code-meta"> Valable pendant 15 minutes</div>
        </div>
        <p class="paragraph">
          Saisissez ce code ainsi que votre nouveau mot de passe sur la page de réinitialisation pour retrouver l'accès à votre compte.
        </p>
        <div class="security-note">
           <strong>Sécurité :</strong> Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail. Votre mot de passe actuel ne sera pas modifié.
        </div>
        <div class="footer">
          © 2026 LET'S GO — Covoiturage fiable & sécurisé au Sénégal.
        </div>
      </div>
    </body>
    </html>
    """

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', "LET'S GO <no-reply@letsgo.sn>")

    try:
        send_mail(
            subject=sujet,
            message=corps_texte,
            from_email=from_email,
            recipient_list=[user.email],
            html_message=corps_html,
            fail_silently=False
        )
        logger.info(f"[RESET_MDP] Code envoyé avec succès à {user.email} : {code}")
        print(f"\n=========================================\n[RESET MDP LET'S GO] Code pour {user.email} : {code}\n=========================================\n")
    except Exception as e:
        logger.error(f"[RESET_MDP] Erreur lors de l'envoi du mail de réinitialisation à {user.email} : {e}")
        print(f"\n=========================================\n[RESET MDP LET'S GO - DEV FALLBACK] Code pour {user.email} : {code}\n(Erreur SMTP : {e})\n=========================================\n")

    return code_obj



User = get_user_model()

def verifier_et_authentifier_token_google(token_recu):
    """
    Vérifie la validité du token Google auprès de Google et retourne l'utilisateur
    existant ou nouvellement créé, ainsi que ses tokens JWT.
    """
    try:
        client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '').strip()
        if not client_id:
            logger.error("[Google Auth] GOOGLE_CLIENT_ID non configuré dans settings.")
            return None

        # 1. Validation cryptographique auprès des serveurs Google
        id_info = id_token.verify_oauth2_token(
            token_recu,
            google_requests.Request(),
            client_id
        )

        # 2. Extraction des données profil certifiées par Google
        email = id_info.get('email', '').strip().lower()
        prenom = id_info.get('given_name', '')
        nom = id_info.get('family_name', '')
        photo_url = id_info.get('picture', None)

        if not email:
            raise ValueError("L'adresse e-mail n'a pas été fournie par Google.")

        # 3. Récupérer ou créer l'utilisateur dans MySQL
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': prenom,
                'last_name': nom,
                'telephone': None,
                'role': User.Role.PASSAGER,
                'is_verified': True,
                'is_active': True,
            }
        )

        # Si nouvel utilisateur, définir un mot de passe inutilisable sécurisé
        if created:
            user.set_unusable_password()
            user.save()
        else:
            # S'il existait déjà mais n'était pas activé ou vérifié
            champs_a_sauvegarder = []
            if not user.is_active:
                user.is_active = True
                champs_a_sauvegarder.append('is_active')
            if not user.is_verified:
                user.is_verified = True
                champs_a_sauvegarder.append('is_verified')
            if not user.first_name and prenom:
                user.first_name = prenom
                champs_a_sauvegarder.append('first_name')
            if not user.last_name and nom:
                user.last_name = nom
                champs_a_sauvegarder.append('last_name')
            if champs_a_sauvegarder:
                user.save(update_fields=champs_a_sauvegarder)

        # 4. Générer les jetons JWT standard LET'S GO
        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'is_new': created,
            'needs_phone': not bool(user.telephone),
            'photo_google': photo_url,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    except Exception as e:
        logger.error(f"[Google Auth] Échec de validation du token Google : {e}")
        return None

