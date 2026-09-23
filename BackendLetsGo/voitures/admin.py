from django.contrib import admin
from .models import Voiture

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = (
        'marque_voiture', 
        'model_voiture', 
        'plaque', 
        'conducteur', 
        'nombres_de_places', 
        'est_climatisee'
    )
    list_filter = ('est_climatisee', 'marque_voiture')
    search_fields = (
        'plaque', 
        'marque_voiture', 
        'model_voiture', 
        'conducteur__email', 
        'conducteur__username'
    )
    readonly_fields = ('date_creation', 'date_Maj')
