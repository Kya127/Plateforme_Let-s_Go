from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Evaluation
from .serializers import EvaluationSerializer


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trajet = serializer.validated_data.get("trajet")
        destinataire = serializer.validated_data.get("destinataire")

        # Règle stricte : un passager ne peut évaluer qu'une seule fois le même trajet
        existing = Evaluation.objects.filter(
            trajet=trajet,
            auteur=request.user,
            destinataire=destinataire
        ).first()

        if existing:
            return Response(
                {"error": "Vous avez déjà évalué ce trajet. Une seule évaluation est autorisée par trajet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

    @action(detail=False, methods=['get'], url_path='verifier', permission_classes=[permissions.IsAuthenticated])
    def verifier(self, request):
        """Vérifie si l'utilisateur connecté a déjà évalué ce trajet."""
        trajet_id = request.query_params.get("trajet")
        if not trajet_id:
            return Response({"deja_evalue": False})

        deja_evalue = Evaluation.objects.filter(
            trajet_id=trajet_id,
            auteur=request.user
        ).exists()

        return Response({"deja_evalue": deja_evalue, "trajet_id": trajet_id})

    def get_queryset(self):
        queryset = Evaluation.objects.all()
        # Permet de filtrer les avis reçus par un utilisateur spécifique ex: /api/evaluations/?destinataire=2
        destinataire_id = self.request.query_params.get("destinataire")
        if destinataire_id:
            queryset = queryset.filter(destinataire_id=destinataire_id)
        trajet_id = self.request.query_params.get("trajet")
        if trajet_id:
            queryset = queryset.filter(trajet_id=trajet_id)
        auteur_id = self.request.query_params.get("auteur")
        if auteur_id:
            queryset = queryset.filter(auteur_id=auteur_id)
        return queryset