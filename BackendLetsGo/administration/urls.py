from django.urls import path
from .views import (
    AdminStatsView,
    AdminUsersView,
    AdminUserDetailView,
    AdminUserToggleStatusView,
    AdminConducteursView,
    AdminConducteurVerificationView,
    AdminConducteurApprouverView,
    AdminConducteurRejeterView,
    AdminTrajetsView,
    AdminTrajetAnnulerView,
    AdminReservationsView,
    AdminAvisView,
)

urlpatterns = [
    # Tableau de bord
    path('stats/', AdminStatsView.as_view(), name='admin-stats'),

    # Utilisateurs
    path('utilisateurs/', AdminUsersView.as_view(), name='admin-users'),
    path('utilisateurs/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('utilisateurs/<int:pk>/toggle-statut/', AdminUserToggleStatusView.as_view(), name='admin-user-toggle-status'),

    # Conducteurs, Demandes & Vérification
    path('demandes/', AdminConducteursView.as_view(), name='admin-demandes'),
    path('demandes/<int:pk>/verification/', AdminConducteurVerificationView.as_view(), name='admin-demande-verification'),
    path('demandes/<int:pk>/approuver/', AdminConducteurApprouverView.as_view(), name='admin-demande-approuver'),
    path('demandes/<int:pk>/rejeter/', AdminConducteurRejeterView.as_view(), name='admin-demande-rejeter'),
    path('conducteurs/', AdminConducteursView.as_view(), name='admin-conducteurs'),
    path('conducteurs/<int:pk>/verification/', AdminConducteurVerificationView.as_view(), name='admin-conducteur-verification'),
    path('conducteurs/<int:pk>/approuver/', AdminConducteurApprouverView.as_view(), name='admin-conducteur-approuver'),
    path('conducteurs/<int:pk>/rejeter/', AdminConducteurRejeterView.as_view(), name='admin-conducteur-rejeter'),

    # Trajets
    path('trajets/', AdminTrajetsView.as_view(), name='admin-trajets'),
    path('trajets/<int:pk>/annuler/', AdminTrajetAnnulerView.as_view(), name='admin-trajet-annuler'),

    # Réservations
    path('reservations/', AdminReservationsView.as_view(), name='admin-reservations'),

    # Avis
    path('avis/', AdminAvisView.as_view(), name='admin-avis'),
    path('avis/<int:pk>/', AdminAvisView.as_view(), name='admin-avis-detail'),
]
