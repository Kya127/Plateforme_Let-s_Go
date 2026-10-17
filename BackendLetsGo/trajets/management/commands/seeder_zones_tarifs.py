from django.core.management.base import BaseCommand
from trajets.models import ZoneTarifaire, LieuZone, GrilleTarifaire
from trajets.services_tarification import REFERENTIEL_ZONES, MATRICE_TARIFS_FCFA


class Command(BaseCommand):
    help = "Initialise le référentiel des zones tarifaires, quartiers, repères et la matrice des tarifs fixes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Démarrage du peuplement du référentiel tarifaire..."))

        # 1. Création / Mise à jour des zones et lieux
        total_zones = 0
        total_lieux = 0

        for zone_data in REFERENTIEL_ZONES:
            zone_obj, created = ZoneTarifaire.objects.update_or_create(
                code=zone_data["code"],
                defaults={
                    "nom": zone_data["nom"],
                    "description": zone_data["description"],
                }
            )
            total_zones += 1

            for q in zone_data["quartiers"]:
                LieuZone.objects.update_or_create(
                    nom=q,
                    defaults={
                        "zone": zone_obj,
                        "type_lieu": LieuZone.TypeLieu.QUARTIER,
                    }
                )
                total_lieux += 1

            for r in zone_data["reperes"]:
                LieuZone.objects.update_or_create(
                    nom=r,
                    defaults={
                        "zone": zone_obj,
                        "type_lieu": LieuZone.TypeLieu.REPERE,
                    }
                )
                total_lieux += 1

        self.stdout.write(self.style.SUCCESS(f"{total_zones} zones et {total_lieux} lieux synchronisés."))

        # 2. Création / Mise à jour de la grille tarifaire (matrice 5x5)
        total_tarifs = 0
        zones_cache = {z.code: z for z in ZoneTarifaire.objects.all()}

        for (code_dep, code_dest), prix in MATRICE_TARIFS_FCFA.items():
            z_dep = zones_cache.get(code_dep)
            z_dest = zones_cache.get(code_dest)
            if z_dep and z_dest:
                GrilleTarifaire.objects.update_or_create(
                    zone_depart=z_dep,
                    zone_arrivee=z_dest,
                    defaults={"prix_par_place": prix}
                )
                total_tarifs += 1

        self.stdout.write(self.style.SUCCESS(f"{total_tarifs} tarifs zone-à-zone enregistrés dans la grille tarifaire."))
