from django.urls import path
from .views import SuggestionsTrajetsView, EnregistrerRechercheView

app_name = 'recommandations'

urlpatterns = [
    path('suggestions/', SuggestionsTrajetsView.as_view(), name='suggestions-trajets'),
    path('recherches/', EnregistrerRechercheView.as_view(), name='enregistrer-recherche'),
]
