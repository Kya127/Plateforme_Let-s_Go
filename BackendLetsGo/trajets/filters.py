import django_filters
from .models import Trajet

class TrajetFilter(django_filters.FilterSet):
    lieu_depart = django_filters.CharFilter(field_name='lieu_depart', lookup_expr='icontains')
    destination = django_filters.CharFilter(field_name='destination', lookup_expr='icontains')
    
    # Filtrage exact sur la Date (DateField)
    date = django_filters.DateFilter(field_name='date')

    # Nombre de places disponibles minimales demandées (gte = >=)
    passagers = django_filters.NumberFilter(field_name='places_disponibles', lookup_expr='gte')

    class Meta:
        model = Trajet
        fields = ['lieu_depart', 'destination', 'date', 'passagers']