import logging
import firebase_admin
from firebase_admin import credentials, messaging

logger = logging.getLogger(__name__)


def init_firebase():
    if not firebase_admin._apps:
        try:
            firebase_admin.initialize_app()
        except Exception as e:
            logger.error(f"Erreur d'initialisation Firebase: {e}")


init_firebase()


def envoyer_push_notification(user, titre, message, data=None):
    """
    Envoie une notification Push instantanée à un utilisateur via son fcm_token.
    Ne bloque pas l'exécution et ne stocke rien en base de données.
    """
    if not user or not user.fcm_token:
        logger.info(
            f"Notification non envoyée : Aucun fcm_token pour l'utilisateur {user}"
        )
        return False

    try:
        fcm_message = messaging.Message(
            notification=messaging.Notification(
                title=titre,
                body=message,
            ),
            data=data or {},
            token=user.fcm_token,
        )
        response = messaging.send(fcm_message)
        logger.info(f"Push envoyée avec succès à {user.email}: {response}")
        return True
    except Exception as e:
        logger.error(
            f"Échec de l'envoi de la notification Push à {user.email}: {e}"
        )
        return False