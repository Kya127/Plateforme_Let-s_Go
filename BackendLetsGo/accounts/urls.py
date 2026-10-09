from django.urls import path
from .views import (
    RegisterView, 
    LogoutView, 
    UserProfileView, 
    BecomeDriverView, 
    PublicDriverProfileView,
    VerifierCodeView,
    RenvoyerCodeView,
    DemandeResetMotDePasseView,
    VerifierCodeResetView,
    ReinitialiserMotDePasseView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verifier-code/', VerifierCodeView.as_view(), name='verifier-code'),
    path('renvoyer-code/', RenvoyerCodeView.as_view(), name='renvoyer-code'),
    path('mot-de-passe-oublie/', DemandeResetMotDePasseView.as_view(), name='demande-reset-mdp'),
    path('verifier-code-reset/', VerifierCodeResetView.as_view(), name='verifier-code-reset'),
    path('reinitialiser-mot-de-passe/', ReinitialiserMotDePasseView.as_view(), name='reinitialiser-mdp'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('become-driver/', BecomeDriverView.as_view(), name='become-driver'),
    path('conducteur/<int:pk>/profil/', PublicDriverProfileView.as_view(), name='public-driver-profile'),
]