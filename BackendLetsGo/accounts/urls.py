from django.urls import path
from .views import (
    RegisterView, 
    LogoutView, 
    UserProfileView, 
    BecomeDriverView, 
    PublicDriverProfileView,
    VerifierCodeView,
    RenvoyerCodeView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verifier-code/', VerifierCodeView.as_view(), name='verifier-code'),
    path('renvoyer-code/', RenvoyerCodeView.as_view(), name='renvoyer-code'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('become-driver/', BecomeDriverView.as_view(), name='become-driver'),
    path('conducteur/<int:pk>/profil/', PublicDriverProfileView.as_view(), name='public-driver-profile'),
]