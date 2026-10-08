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
from .models import User, VerificationDocument, CodeVerification
from .services import creer_et_envoyer_code_otp
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # Accessible sans authentification préalable

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Envoi automatique du code OTP par email
        creer_et_envoyer_code_otp(user, canal='EMAIL')

        return Response({
            "succes": True,
            "requires_verification": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "telephone": user.telephone,
                "role": user.role
            },
            "message": "Votre compte a été créé. Un code de confirmation à 6 chiffres a été envoyé à votre adresse e-mail."
        }, status=status.HTTP_201_CREATED)


class VerifierCodeView(APIView):
    """
    Vérifie le code OTP à 6 chiffres soumis par l'utilisateur pour activer son compte.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip()
        code = (request.data.get('code') or '').strip()

        if not email or not code:
            return Response(
                {"detail": "Veuillez fournir votre adresse e-mail et le code de vérification."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response(
                {"detail": "Aucun compte associé à cette adresse e-mail."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_active:
            return Response(
                {
                    "succes": True,
                    "detail": "Ce compte est déjà activé. Vous pouvez vous connecter directement.",
                    "deja_actif": True
                },
                status=status.HTTP_200_OK
            )

        # Récupérer le dernier code pour cet utilisateur
        code_obj = CodeVerification.objects.filter(user=user, est_utilise=False).order_by('-created_at').first()

        if not code_obj:
            return Response(
                {"detail": "Aucun code de confirmation actif. Veuillez demander un nouveau code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if code_obj.est_expire:
            return Response(
                {"detail": "Ce code a expiré. Veuillez demander un nouveau code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if code_obj.tentatives >= 5:
            return Response(
                {"detail": "Nombre maximum de tentatives dépassé. Veuillez demander un nouveau code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if code_obj.code != code:
            code_obj.tentatives += 1
            code_obj.save(update_fields=['tentatives'])
            restantes = max(0, 5 - code_obj.tentatives)
            return Response(
                {"detail": f"Code incorrect. Il vous reste {restantes} tentative(s)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Code validé avec succès
        code_obj.est_utilise = True
        code_obj.save(update_fields=['est_utilise'])

        user.is_active = True
        user.save(update_fields=['is_active'])

        # Générer tokens JWT pour connexion automatique
        refresh = RefreshToken.for_user(user)

        return Response({
            "succes": True,
            "message": "Votre compte a été vérifié et activé avec succès !",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "telephone": user.telephone,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)


class RenvoyerCodeView(APIView):
    """
    Renvoyer un nouveau code OTP après vérification du délai anti-spam (60 secondes).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip()
        if not email:
            return Response(
                {"detail": "Veuillez renseigner votre adresse e-mail."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response(
                {"detail": "Aucun compte associé à cette adresse e-mail."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_active:
            return Response(
                {"detail": "Ce compte est déjà activé. Vous pouvez vous connecter.", "deja_actif": True},
                status=status.HTTP_200_OK
            )

        # Vérifier le délai anti-spam (60 secondes)
        dernier_code = CodeVerification.objects.filter(user=user).order_by('-created_at').first()
        if dernier_code:
            ecoule = (timezone.now() - dernier_code.created_at).total_seconds()
            if ecoule < 60:
                attente = int(60 - ecoule)
                return Response(
                    {"detail": f"Veuillez patienter {attente} seconde(s) avant de demander un nouveau code."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

        creer_et_envoyer_code_otp(user, canal='EMAIL')

        return Response({
            "succes": True,
            "message": "Un nouveau code de confirmation a été envoyé à votre adresse e-mail."
        }, status=status.HTTP_200_OK)





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



