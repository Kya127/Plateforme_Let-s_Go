from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    BecomeDriverSerializer,
    CustomTokenObtainPairSerializer,
)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue de connexion JWT acceptant indifféremment l'adresse email ou le numéro de téléphone sénégalais.
    """
    serializer_class = CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, VerificationDocument
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # Accessible sans authentification préalable

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            },
            "message": "Compte créé avec succès !"
        }, status=status.HTTP_201_CREATED)





class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist() # Invalide le refresh token
            return Response({"message": "Déconnexion réussie !"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Token invalide ou déjà expiré."}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        # Renvoie automatiquement l'utilisateur qui a émis la requête avec son Token JWT
        return self.request.user        


class BecomeDriverView(APIView):
    """
    Endpoint permettant à un PASSAGER de soumettre ses documents 
    pour demander à devenir CONDUCTEUR.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = request.user

        # 1. Sauvegarder la photo de profil si transmise dans les fichiers
        if 'photo_profil' in request.FILES:
            user.photo = request.FILES['photo_profil']
            user.save(update_fields=['photo'])
        elif 'photo' in request.FILES:
            user.photo = request.FILES['photo']
            user.save(update_fields=['photo'])

        # 2. Vérifier si une demande est déjà en attente d'examen (mise à jour au lieu de rejet bloquant)
        existing_doc = VerificationDocument.objects.filter(
            user=user, 
            status=VerificationDocument.Status.EN_ATTENTE
        ).first()

        # 3. Validation et création ou mise à jour de la demande
        if existing_doc:
            serializer = BecomeDriverSerializer(existing_doc, data=request.data, partial=True, context={'request': request})
        else:
            serializer = BecomeDriverSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            doc = serializer.save(user=user)
            # Validation automatique après soumission des documents (règle demandée pour le flow)
            doc.status = VerificationDocument.Status.APPROUVE
            doc.save(update_fields=['status'])

            user.role = 'CONDUCTEUR'
            user.is_verified = True
            user.save(update_fields=['role', 'is_verified'])
            
            return Response({
                "message": "Votre demande pour devenir conducteur a été soumise et validée avec succès. Vous pouvez désormais publier des trajets.",
                "status": "APPROVED",
                "is_verified": True
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicDriverProfileView(APIView):
    """
    Profil public d'un conducteur avec sa note, ses statistiques, 
    son véhicule et les commentaires laissés par les passagers (mur du conducteur).
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        user = get_object_or_404(User, pk=pk)

        # Évaluations reçues
        evals = user.evaluations_recues.all()
        total_evals = evals.count()
        if total_evals > 0:
            avg_note = round(sum(e.note for e in evals) / total_evals, 1)
        else:
            avg_note = 0

        # Trajets terminés
        from trajets.models import Trajet
        from voitures.models import Voiture
        nb_trajets = Trajet.objects.filter(conducteur=user, statut=Trajet.StatutTrajet.TERMINE).count()
        if nb_trajets == 0:
            nb_trajets = Trajet.objects.filter(conducteur=user).count()

        # Voiture principale
        voiture = Voiture.objects.filter(conducteur=user).first()
        voiture_data = None
        if voiture:
            voiture_data = {
                "marque": voiture.marque_voiture,
                "modele": voiture.model_voiture,
                "couleur": voiture.couleur or "Blanc Nacré",
                "plaque": voiture.plaque or "SN AB-123-CD",
                "climatisee": voiture.est_climatisee,
                "nombres_de_places": voiture.nombres_de_places,
                "photo": request.build_absolute_uri(voiture.photo_voiture.url) if (voiture.photo_voiture and request) else None,
            }

        from evaluations.serializers import EvaluationSerializer
        evals_serialized = EvaluationSerializer(evals, many=True, context={'request': request}).data

        photo_url = None
        if user.photo:
            photo_url = request.build_absolute_uri(user.photo.url) if request else user.photo.url

        mois_noms = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        membre_depuis = "Récemment"
        if user.date_joined:
            m = mois_noms[user.date_joined.month - 1].capitalize()
            membre_depuis = f"{m} {user.date_joined.year}"

        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}".strip() or user.first_name or "Conducteur",
            "photo": photo_url,
            "telephone": user.telephone,
            "role": user.role,
            "is_verified": user.is_verified,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            "membre_depuis": membre_depuis,
            "note_moyenne": avg_note,
            "nb_evaluations": total_evals,
            "nb_trajets": nb_trajets,
            "voiture": voiture_data,
            "evaluations": evals_serialized,
        }
        return Response(data, status=status.HTTP_200_OK)



