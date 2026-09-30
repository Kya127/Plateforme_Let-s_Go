from rest_framework import permissions, viewsets, status
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
        note = serializer.validated_data.get("note")
        commentaire = serializer.validated_data.get("commentaire", "")

        # Si l'utilisateur a déjà laissé un avis pour ce trajet et ce destinataire, on le met à jour
        existing = Evaluation.objects.filter(
            trajet=trajet,
            auteur=request.user,
            destinataire=destinataire
        ).first()

        if existing:
            existing.note = note
            if commentaire:
                existing.commentaire = commentaire
            existing.save()
            data = self.get_serializer(existing).data
            return Response(data, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

    def get_queryset(self):
        queryset = Evaluation.objects.all()
        # Permet de filtrer les avis reçus par un utilisateur spécifique ex: /api/evaluations/?destinataire=2
        destinataire_id = self.request.query_params.get("destinataire")
        if destinataire_id:
            queryset = queryset.filter(destinataire_id=destinataire_id)
        return queryset