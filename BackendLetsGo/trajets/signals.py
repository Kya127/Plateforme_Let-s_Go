from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Trajet
from reservations.models import Reservation
from .services import envoyer_push_notification


@receiver(post_save, sender=Reservation)
def notification_reservation_evenements(sender, instance, created, **kwargs):
    conducteur = instance.trajet.conducteur
    passager = instance.passager

    if created:
        titre = "Nouvelle réservation !"
        message = f"{passager.first_name or 'Un passager'} a réservé {instance.nombre_places} place(s) pour votre trajet {instance.trajet.lieu_depart} ➔ {instance.trajet.destination}."
        envoyer_push_notification(
            conducteur,
            titre,
            message,
            data={"trajet_id": str(instance.trajet.id)},
        )
    elif instance.statut == "ANNULEE":
        titre = "Réservation annulée"
        message = f"{passager.first_name or 'Un passager'} a annulé sa réservation sur votre trajet {instance.trajet.lieu_depart} ➔ {instance.trajet.destination}."
        envoyer_push_notification(
            conducteur,
            titre,
            message,
            data={"trajet_id": str(instance.trajet.id)},
        )


@receiver(pre_save, sender=Trajet)
def notification_statut_trajet(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_trajet = Trajet.objects.get(pk=instance.pk)
    except Trajet.DoesNotExist:
        return

    if old_trajet.statut == instance.statut:
        return

    reservations_confirmees = instance.reservations.filter(statut="CONFIRMEE")
    passagers = [res.passager for res in reservations_confirmees]

    if instance.statut == Trajet.StatutTrajet.EN_COURS:
        titre = "Trajet démarré !"
        message = f"Votre conducteur {instance.conducteur.first_name} a démarré le trajet vers {instance.destination}. Bon voyage !"
        for passager in passagers:
            envoyer_push_notification(
                passager,
                titre,
                message,
                data={
                    "trajet_id": str(instance.id),
                    "action": "TRAJET_DEMARRE",
                },
            )
    elif instance.statut == Trajet.StatutTrajet.TERMINE:
        titre = "Vous êtes arrivé !"
        message = f"Vous êtes arrivé à {instance.destination}. Laissez un avis sur {instance.conducteur.first_name} pour aider la communauté."
        for passager in passagers:
            envoyer_push_notification(
                passager,
                titre,
                message,
                data={"trajet_id": str(instance.id), "action": "EVALUATION"},
            )