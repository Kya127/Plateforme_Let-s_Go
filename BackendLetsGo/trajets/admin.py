from django.contrib import admin
from .models import Trajet, ZoneTarifaire, LieuZone, GrilleTarifaire


@admin.register(ZoneTarifaire)
class ZoneTarifaireAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'description')
    search_fields = ('code', 'nom')


@admin.register(LieuZone)
class LieuZoneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'zone', 'type_lieu')
    list_filter = ('zone', 'type_lieu')
    search_fields = ('nom',)


@admin.register(GrilleTarifaire)
class GrilleTarifaireAdmin(admin.ModelAdmin):
    list_display = ('zone_depart', 'zone_arrivee', 'prix_par_place')
    list_filter = ('zone_depart', 'zone_arrivee')


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ('lieu_depart', 'destination', 'date', 'heure_depart', 'prix_par_place', 'statut')
    list_filter = ('statut', 'date')
    search_fields = ('lieu_depart', 'destination', 'conducteur__telephone')
