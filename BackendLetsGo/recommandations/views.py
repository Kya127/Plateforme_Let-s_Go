from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .services import get_suggestions_trajets
from .serializers import (
    SuggestionTrajetItemSerializer,
    EnregistrerRechercheInputSerializer,
    HistoriqueRechercheSerializer
)
from .models import HistoriqueRecherche


class SuggestionsTrajetsView(APIView):
    """
    Endpoint principal de suggestions dynamiques pour le haut du mur d'accueil :
    - Cas 1 (Passager avec historique) : 1 à 3 axes fréquents -> "Basé sur vos habitudes"
    - Cas 2 (Nouvel utilisateur / Cold Start) : Axes populaires -> "Trajets populaires du moment"
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Suggestions dynamiques de trajets",
        description="Retourne les trajets suggérés (habitudes ou populaires) pour l'écran d'accueil.",
        responses={200: OpenApiResponse(description="Liste des suggestions avec métadonnées")}
    )
    def get(self, request):
        user = request.user if request.user and request.user.is_authenticated else None
        
        resultat = get_suggestions_trajets(user=user, limit=6)
        
        serializer_context = {
            'request': request,
            'tag': resultat['tag'],
            'type_suggestion': resultat['type_suggestion']
        }
        
        trajets_serialises = SuggestionTrajetItemSerializer(
            resultat['trajets'],
            many=True,
            context=serializer_context
        ).data

        return Response({
            "type_suggestion": resultat['type_suggestion'],
            "tag": resultat['tag'],
            "description": resultat['description'],
            "count": len(trajets_serialises),
            "suggestions": trajets_serialises
        }, status=status.HTTP_200_OK)


class EnregistrerRechercheView(APIView):
    """
    Enregistre une recherche effectuée par un utilisateur pour enrichir son profil d'habitudes.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Enregistrer une recherche",
        request=EnregistrerRechercheInputSerializer,
        responses={201: HistoriqueRechercheSerializer}
    )
    def post(self, request):
        serializer = EnregistrerRechercheInputSerializer(data=request.data)
        if serializer.is_valid():
            dep = serializer.validated_data['lieu_depart'].strip()
            dest = serializer.validated_data['destination'].strip()
            date_voulue = serializer.validated_data.get('date_voulue')

            # Si l'utilisateur est connecté, on enregistre
            user = request.user if request.user and request.user.is_authenticated else None
            
            # Éviter de créer des doublons identiques consécutifs dans la même minute
            historique = HistoriqueRecherche.objects.create(
                user=user,
                lieu_depart=dep,
                destination=dest,
                date_voulue=date_voulue
            )

            return Response(
                HistoriqueRechercheSerializer(historique, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
