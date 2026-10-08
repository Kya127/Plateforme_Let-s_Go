import secrets
import string
import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CodeVerification

logger = logging.getLogger(__name__)

def generer_code_otp(longueur=6):
    """Génère un code numérique cryptographiquement sécurisé à 6 chiffres."""
    return "".join(secrets.choice(string.digits) for _ in range(longueur))


def creer_et_envoyer_code_otp(user, canal='EMAIL'):
    """
    Génère un nouveau code OTP de vérification pour l'utilisateur,
    l'enregistre en base de données et l'envoie par e-mail.
    """
    # 1. Invalider les anciens codes non utilisés pour cet utilisateur
    CodeVerification.objects.filter(user=user, est_utilise=False).update(est_utilise=True)

    # 2. Générer un nouveau code valable 15 minutes
    code = generer_code_otp(6)
    expires_at = timezone.now() + timedelta(minutes=15)

    code_obj = CodeVerification.objects.create(
        user=user,
        code=code,
        canal=canal,
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
          <div class="code-meta">⏱ Valable pendant 15 minutes</div>
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
