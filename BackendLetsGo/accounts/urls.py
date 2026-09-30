from django.urls import path
from .views import (
    RegisterView, 
    LogoutView, 
    UserProfileView, 
    BecomeDriverView, 
    PublicDriverProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('become-driver/', BecomeDriverView.as_view(), name='become-driver'),
    path('conducteur/<int:pk>/profil/', PublicDriverProfileView.as_view(), name='public-driver-profile'),
]