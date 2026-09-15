from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserProfileSerializer, BecomeDriverSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import VerificationDocument
from rest_framework.parsers import MultiPartParser, FormParser
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

        # 1. Vérifier si une demande est déjà en attente d'examen
        has_pending_request = VerificationDocument.objects.filter(
            user=user, 
            status=VerificationDocument.Status.EN_ATTENTE
        ).exists()

        if has_pending_request:
            return Response(
                {"detail": "Vous avez déjà une demande de vérification en cours de traitement."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Validation et création de la demande
        serializer = BecomeDriverSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            
            return Response({
                "message": "Votre demande pour devenir conducteur a été soumise avec succès. Elle est en cours de vérification.",
                "status": "PENDING"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

