import re
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from accounts.models import User, VerificationDocument
from voitures.models import Voiture
from trajets.models import Trajet
from reservations.models import Reservation
from commission.models import Commission
from evaluations.models import Evaluation


class AdminPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsAdminOrStaffPermission(permissions.BasePermission):
    """
    Vérifie que l'utilisateur est authentifié et possède le rôle ADMINISTRATEUR ou le flag is_staff.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        role = getattr(user, 'role', '')
        return (
            role.upper() == User.Role.ADMINISTRATEUR or 
            user.is_staff or 
            user.is_superuser
        )


# ==============================================================================
# 1. TABLEAU DE BORD (KPIS, REVENUS, COURBE DE CROISSANCE, DERNIERS ÉLÉMENTS)
# ==============================================================================
class AdminStatsView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request):
        maintenant = timezone.now()

        # 1. Utilisateurs (exclut les administrateurs)
        base_users = User.objects.exclude(role=User.Role.ADMINISTRATEUR).exclude(is_superuser=True)
        total_utilisateurs = base_users.count()
        conducteurs_count = base_users.filter(role=User.Role.CONDUCTEUR).count()
        passagers_count = base_users.filter(role=User.Role.PASSAGER).count()

        # Nouveaux utilisateurs récents (aujourd'hui ou dernières 48h)
        debut_aujourdhui = maintenant.replace(hour=0, minute=0, second=0, microsecond=0)
        nouveaux_utilisateurs = base_users.filter(date_joined__gte=debut_aujourdhui).count()
        if nouveaux_utilisateurs == 0:
            nouveaux_utilisateurs = base_users.filter(date_joined__gte=maintenant - timedelta(days=2)).count()

        # 2. Trajets & Réservations
        trajets_count = Trajet.objects.count()
        reservations_count = Reservation.objects.count()
        demandes_en_attente = VerificationDocument.objects.filter(
            status=VerificationDocument.Status.EN_ATTENTE
        ).count()

        # 3. Revenus (Commissions encaissées ou calculées)
        total_commissions = Commission.objects.filter(statut='payee').aggregate(
            total=Sum('montant')
        )['total'] or 0

        # Si aucune commission payee n'a encore été marquée PayTech, calcul prévisionnel basé sur les réservations confirmées (10%)
        if total_commissions == 0:
            total_commissions = Commission.objects.aggregate(total=Sum('montant'))['total'] or 0
        if total_commissions == 0:
            # 10% des montants des trajets réservés confirmés
            total_calcule = sum(
                (r.nombre_de_places * r.trajet.prix_par_place * 0.10)
                for r in Reservation.objects.filter(statut=Reservation.StatutReservation.CONFIRMEE).select_related('trajet')
            )
            total_commissions = int(total_calcule)

        # 4. Évolution / Courbe de croissance (6 derniers mois)
        mois_labels = []
        croissance_utilisateurs = []
        croissance_reservations = []

        noms_mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
        for i in range(5, -1, -1):
            date_cible = maintenant - timedelta(days=i * 30)
            mois_idx = date_cible.month - 1
            label = noms_mois[mois_idx]
            mois_labels.append(label)

            # Nombre cumulé jusqu'à la fin de ce mois
            fin_mois = date_cible + timedelta(days=30)
            nb_users = base_users.filter(date_joined__lte=fin_mois).count()
            nb_res = Reservation.objects.filter(created_at__lte=fin_mois).count()
            croissance_utilisateurs.append(nb_users)
            croissance_reservations.append(nb_res)

        # 5. Derniers utilisateurs (Aperçu tableau vue d'ensemble - Hors admin)
        derniers_users_qs = base_users.order_by('-date_joined')[:5]
        derniers_users = []
        for u in derniers_users_qs:
            nom_complet = f"{u.first_name} {u.last_name}".strip() or u.username or u.email
            derniers_users.append({
                'id': u.id,
                'nom': nom_complet,
                'email': u.email,
                'photo': request.build_absolute_uri(u.photo.url) if u.photo else '',
                'role': u.role,
                'statut': 'Actif' if u.is_active else 'Suspendu',
                'is_verified': u.is_verified,
                'date_inscription': u.date_joined.strftime('%d %b %Y') if u.date_joined else '',
            })

        # 6. Trajets en cours & à venir (Aperçu tableau vue d'ensemble)
        trajets_qs = Trajet.objects.filter(
            statut__in=[Trajet.StatutTrajet.PLANIFIE, Trajet.StatutTrajet.EN_COURS]
        ).select_related('conducteur', 'voiture').order_by('date', 'heure_depart')[:5]

        trajets_apercu = []
        for t in trajets_qs:
            cond = t.conducteur
            cond_nom = f"{cond.first_name} {cond.last_name}".strip() or cond.email
            places_totales = t.voiture.nombres_de_places if t.voiture else 4
            places_prises = places_totales - t.places_disponibles
            trajets_apercu.append({
                'id': t.id,
                'code': f"TR-{t.id:04d}",
                'conducteur_id': cond.id,
                'conducteur_nom': cond_nom,
                'conducteur_photo': request.build_absolute_uri(cond.photo.url) if cond.photo else '',
                'depart': t.lieu_depart,
                'destination': t.destination,
                'itineraire': f"{t.lieu_depart} ➔ {t.destination}",
                'date': t.date.strftime('%d %b %Y') if t.date else '',
                'heure': t.heure_depart.strftime('%H:%M') if t.heure_depart else '',
                'places_prises': max(places_prises, 0),
                'places_totales': places_totales,
                'places_ratio': f"{max(places_prises, 0)} / {places_totales}",
                'statut': t.statut,
            })

        # 7. Corridors réels tirés de la base de données
        corridors_qs = (
            Reservation.objects.values('trajet__lieu_depart', 'trajet__destination')
            .annotate(volume=Count('id'))
            .order_by('-volume')[:6]
        )
        if not corridors_qs:
            corridors_qs = (
                Trajet.objects.values('lieu_depart', 'destination')
                .annotate(volume=Count('id'))
                .order_by('-volume')[:6]
            )

        corridors = []
        max_vol = max([c['volume'] for c in corridors_qs], default=1) if corridors_qs else 1
        for c in corridors_qs:
            dep = c.get('trajet__lieu_depart') or c.get('lieu_depart', '')
            dest = c.get('trajet__destination') or c.get('destination', '')
            vol = c['volume']
            share = int((vol / max_vol) * 100) if max_vol > 0 else 0
            corridors.append({
                'route': f"{dep} ➔ {dest}",
                'volume': vol,
                'share': share,
            })

        # 8. Taux de remplissage réel calculé sur les trajets
        trajets_tous = Trajet.objects.select_related('voiture').all()
        total_places_offertes = 0
        total_places_occupees = 0
        for t in trajets_tous:
            nb_places = t.voiture.nombres_de_places if t.voiture else 4
            prises = max(nb_places - t.places_disponibles, 0)
            total_places_offertes += nb_places
            total_places_occupees += prises

        taux_remplissage = round((total_places_occupees / total_places_offertes * 100), 1) if total_places_offertes > 0 else 75.0

        return Response({
            'kpis': {
                'total_utilisateurs': total_utilisateurs,
                'conducteurs': conducteurs_count,
                'passagers': passagers_count,
                'trajets_crees': trajets_count,
                'reservations': reservations_count,
                'demandes_en_attente': demandes_en_attente,
                'nouveaux_utilisateurs': nouveaux_utilisateurs,
                'revenus_mensuels': int(total_commissions),
            },
            'croissance': {
                'labels': mois_labels,
                'utilisateurs': croissance_utilisateurs,
                'reservations': croissance_reservations,
            },
            'derniers_utilisateurs': derniers_users,
            'trajets_en_cours': trajets_apercu,
            'corridors': corridors,
            'taux_remplissage': taux_remplissage,
        })


# ==============================================================================
# 2. GESTION DES UTILISATEURS (LISTE, RECHERCHE, FILTRE, SUSPENSION)
# ==============================================================================
class AdminUsersView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request):
        # Exclut systématiquement les comptes administrateurs de la liste des utilisateurs
        qs = User.objects.exclude(
            role=User.Role.ADMINISTRATEUR
        ).exclude(is_superuser=True).order_by('-date_joined')

        # Recherche textuelle multi-mots
        q = request.query_params.get('q', '').strip()
        if q:
            terms = q.split()
            q_filter = Q()
            for term in terms:
                q_filter &= (
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(email__icontains=term) |
                    Q(telephone__icontains=term)
                )
            qs = qs.filter(q_filter)

        # Filtre par rôle (Passager / Conducteur)
        role = request.query_params.get('role', '').strip().upper()
        if role in ['PASSAGER', 'CONDUCTEUR']:
            qs = qs.filter(role=role)

        # Filtre par statut (Actif / Suspendu / En attente)
        statut = request.query_params.get('statut', '').strip().lower()
        if statut == 'actif':
            qs = qs.filter(is_active=True)
        elif statut in ['suspendu', 'inactif']:
            qs = qs.filter(is_active=False)

        paginator = AdminPagination()
        page = paginator.paginate_queryset(qs, request)

        utilisateurs = []
        for u in page:
            nom_complet = f"{u.first_name} {u.last_name}".strip() or u.username or u.email
            utilisateurs.append({
                'id': u.id,
                'nom': nom_complet,
                'prenom': u.first_name,
                'nom_famille': u.last_name,
                'email': u.email,
                'telephone': u.telephone or '',
                'adresse': u.adresse or '',
                'photo': request.build_absolute_uri(u.photo.url) if u.photo else '',
                'role': u.role,
                'is_active': u.is_active,
                'statut': 'Actif' if u.is_active else 'Suspendu',
                'is_verified': u.is_verified,
                'date_inscription': u.date_joined.strftime('%d %b %Y') if u.date_joined else '',
            })

        return paginator.get_paginated_response(utilisateurs)

    def post(self, request):
        """
        Création manuelle d'un utilisateur par l'administrateur avec attribution directe de rôle
        (utile pour le service client / guichet physique).
        """
        prenom = request.data.get('prenom', '').strip()
        nom = request.data.get('nom', '').strip()
        email = request.data.get('email', '').strip().lower()
        telephone = request.data.get('telephone', '').strip()
        role = request.data.get('role', 'PASSAGER').strip().upper()
        password = request.data.get('password', '').strip()
        adresse = request.data.get('adresse', '').strip()

        if not prenom or not nom or not email or not telephone:
            return Response(
                {'detail': 'Le prénom, le nom, l\'adresse email et le numéro de téléphone sont obligatoires.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if role not in [User.Role.PASSAGER, User.Role.CONDUCTEUR]:
            return Response(
                {'detail': 'Le rôle doit être soit PASSAGER soit CONDUCTEUR.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'detail': f"Un compte avec l'adresse email '{email}' existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(telephone=telephone).exists():
            return Response(
                {'detail': f"Un compte avec le numéro de téléphone '{telephone}' existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )

        initial_password = password if password else 'Passer123'

        user = User.objects.create_user(
            username=email,
            email=email,
            password=initial_password,
            first_name=prenom,
            last_name=nom,
            telephone=telephone,
            adresse=adresse,
            role=role,
            is_active=True,
            is_verified=(role == User.Role.CONDUCTEUR),  # Auto-approuvé si inscrit physiquement par l'admin
        )

        # Si le rôle est conducteur et que des détails de véhicule sont renseignés
        if role == User.Role.CONDUCTEUR:
            marque = request.data.get('marque_voiture', '').strip()
            modele = request.data.get('model_voiture', '').strip()
            plaque = request.data.get('plaque', '').strip()
            places = request.data.get('nombres_de_places', 4)
            couleur = request.data.get('couleur', '').strip()
            climatisee = request.data.get('est_climatisee', True)

            if marque or plaque:
                Voiture.objects.create(
                    conducteur=user,
                    marque_voiture=marque or 'Toyota',
                    model_voiture=modele or 'Corolla',
                    plaque=plaque or 'DK-0000-X',
                    nombres_de_places=int(places) if str(places).isdigit() else 4,
                    couleur=couleur or 'Blanc',
                    est_climatisee=bool(climatisee),
                )

        return Response({
            'succes': True,
            'message': f"L'utilisateur {prenom} {nom} a été créé avec succès en tant que {role}.",
            'user': {
                'id': user.id,
                'nom': f"{user.first_name} {user.last_name}",
                'prenom': user.first_name,
                'nom_famille': user.last_name,
                'email': user.email,
                'telephone': user.telephone,
                'adresse': user.adresse,
                'role': user.role,
                'is_active': user.is_active,
                'statut': 'Actif',
                'is_verified': user.is_verified,
                'date_inscription': user.date_joined.strftime('%d %b %Y'),
            }
        }, status=status.HTTP_201_CREATED)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        nom_complet = f"{u.first_name} {u.last_name}".strip() or u.username or u.email

        # Statistiques réelles de cet utilisateur
        trajets_conducteur_count = Trajet.objects.filter(conducteur=u).count()
        reservations_count = Reservation.objects.filter(passager=u).count()

        # Dernier trajet (comme passager ou comme conducteur)
        dernier_trajet_obj = (
            Trajet.objects.filter(conducteur=u).order_by('-date', '-heure_depart').first() or
            Trajet.objects.filter(reservations__passager=u).order_by('-date', '-heure_depart').first()
        )
        dernier_trajet_str = ""
        if dernier_trajet_obj:
            dernier_trajet_str = f"{dernier_trajet_obj.lieu_depart} ➔ {dernier_trajet_obj.destination}"

        # Activités récentes (Trajets ou Réservations de l'utilisateur)
        activites = []
        # Réservations récentes
        reservations_qs = Reservation.objects.filter(passager=u).select_related('trajet').order_by('-created_at')[:5]
        for r in reservations_qs:
            t = r.trajet
            activites.append({
                'id': r.id,
                'code': f"TR-{t.id:04d}",
                'itineraire': f"{t.lieu_depart} ➔ {t.destination}",
                'date_heure': f"{t.date.strftime('%d %b %Y') if t.date else ''}, {t.heure_depart.strftime('%H:%M') if t.heure_depart else ''}",
                'statut': r.statut,
                'type': 'Réservation',
            })

        # Trajets publiés récents si conducteur
        trajets_publies = Trajet.objects.filter(conducteur=u).order_by('-date')[:5]
        for t in trajets_publies:
            activites.append({
                'id': t.id,
                'code': f"TR-{t.id:04d}",
                'itineraire': f"{t.lieu_depart} ➔ {t.destination}",
                'date_heure': f"{t.date.strftime('%d %b %Y') if t.date else ''}, {t.heure_depart.strftime('%H:%M') if t.heure_depart else ''}",
                'statut': t.statut,
                'type': 'Publication',
            })

        # Véhicule associé si présent
        vehicule = None
        voiture_obj = Voiture.objects.filter(conducteur=u).first()
        if voiture_obj:
            vehicule = {
                'id': voiture_obj.id,
                'marque': voiture_obj.marque_voiture,
                'modele': voiture_obj.model_voiture,
                'plaque': voiture_obj.plaque,
                'places': voiture_obj.nombres_de_places,
                'couleur': voiture_obj.couleur or '',
                'climatisee': voiture_obj.est_climatisee,
                'photo': request.build_absolute_uri(voiture_obj.photo_voiture.url) if voiture_obj.photo_voiture else '',
            }

        return Response({
            'id': u.id,
            'nom': nom_complet,
            'prenom': u.first_name,
            'nom_famille': u.last_name,
            'email': u.email,
            'telephone': u.telephone or '+221 77 000 00 00',
            'adresse': u.adresse or '',
            'photo': request.build_absolute_uri(u.photo.url) if u.photo else '',
            'role': u.role,
            'is_active': u.is_active,
            'statut': 'Actif' if u.is_active else 'Suspendu',
            'is_verified': u.is_verified,
            'date_inscription': u.date_joined.strftime('%d %B %Y') if u.date_joined else '',
            'trajets_effectues': trajets_conducteur_count + reservations_count,
            'reservations_count': reservations_count,
            'dernier_trajet': dernier_trajet_str,
            'activites': activites,
            'vehicule': vehicule,
        })


    def patch(self, request, pk):
        """
        Modification du rôle ou des informations de l'utilisateur par l'administrateur.
        Permet notamment de basculer le rôle entre PASSAGER et CONDUCTEUR.
        """
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if u.role == User.Role.ADMINISTRATEUR or u.is_superuser:
            return Response(
                {'detail': "Action non autorisée : impossible de modifier le rôle d'un compte administrateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        nouveau_role = request.data.get('role', '').strip().upper()
        if not nouveau_role:
            return Response({'detail': "Le champ 'role' est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)

        if nouveau_role not in [User.Role.PASSAGER, User.Role.CONDUCTEUR]:
            return Response({'detail': "Le rôle doit être soit PASSAGER soit CONDUCTEUR."}, status=status.HTTP_400_BAD_REQUEST)

        u.role = nouveau_role
        champs_maj = ['role']

        if nouveau_role == User.Role.CONDUCTEUR:
            u.is_verified = True
            champs_maj.append('is_verified')
        else:
            u.is_verified = False
            champs_maj.append('is_verified')

        u.save(update_fields=champs_maj)

        nom_complet = f"{u.first_name} {u.last_name}".strip() or u.email
        return Response({
            'succes': True,
            'message': f"Le rôle de {nom_complet} a été modifié en {nouveau_role} avec succès.",
            'user': {
                'id': u.id,
                'role': u.role,
                'is_verified': u.is_verified,
            }
        })

    def delete(self, request, pk):
        """
        Suppression définitive d'un utilisateur par l'administrateur.
        """
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if u.id == request.user.id:
            return Response(
                {'detail': "Action impossible : vous ne pouvez pas supprimer votre propre compte administrateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if u.role == User.Role.ADMINISTRATEUR or u.is_superuser:
            return Response(
                {'detail': "Action impossible : la suppression d'un compte administrateur est interdite."},
                status=status.HTTP_400_BAD_REQUEST
            )

        nom_complet = f"{u.first_name} {u.last_name}".strip() or u.email

        # Annuler les trajets à venir de ce conducteur pour libérer les passagers
        Trajet.objects.filter(
            conducteur=u, 
            statut__in=[Trajet.StatutTrajet.PLANIFIE, Trajet.StatutTrajet.EN_COURS]
        ).update(statut=Trajet.StatutTrajet.ANNULE)

        # Suppression définitive de l'utilisateur
        u.delete()

        return Response({
            'succes': True,
            'message': f"Le compte de {nom_complet} a été supprimé définitivement de la plateforme."
        }, status=status.HTTP_200_OK)


class AdminUserToggleStatusView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def post(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if u.id == request.user.id:
            return Response(
                {'detail': "Action impossible : vous ne pouvez pas suspendre votre propre compte administrateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Inverser le statut
        u.is_active = not u.is_active
        u.save(update_fields=['is_active'])

        # Si le compte vient d'être suspendu, annuler ses trajets futurs planifiés
        if not u.is_active:
            Trajet.objects.filter(
                conducteur=u,
                statut=Trajet.StatutTrajet.PLANIFIE
            ).update(statut=Trajet.StatutTrajet.ANNULE)

        statut_txt = 'activé' if u.is_active else 'suspendu'
        return Response({
            'succes': True,
            'message': f"Le compte de {u.first_name or u.email} a été {statut_txt} avec succès.",
            'is_active': u.is_active,
            'statut': 'Actif' if u.is_active else 'Suspendu',
        })


# ==============================================================================
# 3. GESTION DES DEMANDES CONDUCTEURS (LISTE, ONGLETS, VALIDATION, REJET)
# ==============================================================================
class AdminConducteursView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request):
        # Conducteurs ou utilisateurs ayant soumis une demande de vérification (hors admins)
        users_conducteurs = User.objects.exclude(
            role=User.Role.ADMINISTRATEUR
        ).exclude(is_superuser=True).filter(
            Q(role=User.Role.CONDUCTEUR) | 
            Q(verification_documents__isnull=False)
        ).distinct().order_by('-date_joined')

        # Compteurs globaux pour les onglets
        total_verifies = User.objects.exclude(role=User.Role.ADMINISTRATEUR).filter(role=User.Role.CONDUCTEUR, is_verified=True).count()
        total_en_attente = VerificationDocument.objects.filter(status=VerificationDocument.Status.EN_ATTENTE).count()
        total_rejetes = VerificationDocument.objects.filter(status=VerificationDocument.Status.REJETE).count()
        total_suspendus = User.objects.exclude(role=User.Role.ADMINISTRATEUR).filter(role=User.Role.CONDUCTEUR, is_active=False).count()

        # Filtre d'onglet : 'en_attente', 'tous', 'verifies', 'rejetes', 'suspendus'
        onglet = request.query_params.get('onglet', 'tous').strip().lower()

        if onglet == 'en_attente':
            # Utilisateurs ayant un dossier PENDING en attente de traitement
            users_conducteurs = users_conducteurs.filter(
                verification_documents__status=VerificationDocument.Status.EN_ATTENTE
            )
        elif onglet in ['verifies', 'approuves']:
            users_conducteurs = users_conducteurs.filter(
                Q(is_verified=True) | Q(verification_documents__status=VerificationDocument.Status.APPROUVE)
            )
        elif onglet in ['rejetes', 'refuses']:
            users_conducteurs = users_conducteurs.filter(
                verification_documents__status=VerificationDocument.Status.REJETE
            )
        elif onglet == 'suspendus':
            users_conducteurs = users_conducteurs.filter(is_active=False)

        # Recherche textuelle robuste (multi-mots : prénom, nom, email, téléphone, marque, plaque)
        q = request.query_params.get('q', '').strip()
        if q:
            terms = q.split()
            q_filter = Q()
            for term in terms:
                q_filter &= (
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(email__icontains=term) |
                    Q(telephone__icontains=term) |
                    Q(voitures__marque_voiture__icontains=term) |
                    Q(voitures__model_voiture__icontains=term) |
                    Q(voitures__plaque__icontains=term)
                )
            users_conducteurs = users_conducteurs.filter(q_filter)

        paginator = AdminPagination()
        page = paginator.paginate_queryset(users_conducteurs, request)

        liste = []
        for u in page:
            nom_complet = f"{u.first_name} {u.last_name}".strip() or u.username or u.email

            # Véhicule
            voiture = u.voitures.first()
            vehicule_str = "Aucun véhicule"
            if voiture:
                vehicule_str = f"{voiture.marque_voiture} {voiture.model_voiture}"
                if voiture.couleur:
                    vehicule_str += f" • {voiture.couleur}"
                if voiture.plaque:
                    vehicule_str += f" ({voiture.plaque})"

            # Dernier document de vérification
            dernier_doc = u.verification_documents.order_by('-created_at').first()
            if not u.is_active:
                statut_demande = 'SUSPENDU'
            elif dernier_doc and dernier_doc.status == VerificationDocument.Status.EN_ATTENTE:
                statut_demande = 'EN_ATTENTE'
            elif dernier_doc and dernier_doc.status == VerificationDocument.Status.REJETE:
                statut_demande = 'REJETE'
            elif u.is_verified or (dernier_doc and dernier_doc.status == VerificationDocument.Status.APPROUVE):
                statut_demande = 'VERIFIE'
            else:
                statut_demande = 'NON_VERIFIE'

            # Note moyenne réelle
            evals = Evaluation.objects.filter(destinataire=u)
            avg_note = evals.aggregate(Avg('note'))['note__avg']
            note_str = f"{avg_note:.1f}/5" if avg_note else "--"

            liste.append({
                'id': u.id,
                'nom': nom_complet,
                'prenom': u.first_name,
                'nom_famille': u.last_name,
                'email': u.email,
                'telephone': u.telephone or '',
                'photo': request.build_absolute_uri(u.photo.url) if u.photo else '',
                'vehicule': vehicule_str,
                'statut': statut_demande,
                'note': note_str,
                'date_inscription': u.date_joined.strftime('%d %b %Y') if u.date_joined else '',
                'dossier_id': dernier_doc.id if dernier_doc else None,
                'date_demande': dernier_doc.created_at.strftime('%d %b %Y') if dernier_doc and dernier_doc.created_at else u.date_joined.strftime('%d %b %Y'),
                'pieces_valides': {
                    'permis': bool(dernier_doc and dernier_doc.permis_conduire),
                    'carte_grise': bool(dernier_doc and dernier_doc.carte_grise),
                    'assurance': bool(dernier_doc and dernier_doc.assurance),
                    'photo_vehicule': bool(dernier_doc and dernier_doc.photo_vehicule),
                },
                'motif_rejet': dernier_doc.motif_rejet if dernier_doc else '',
            })

        reponse = paginator.get_paginated_response(liste)
        reponse.data['compteurs'] = {
            'total': User.objects.exclude(role=User.Role.ADMINISTRATEUR).filter(
                Q(role=User.Role.CONDUCTEUR) | Q(verification_documents__isnull=False)
            ).distinct().count(),
            'verifies': total_verifies,
            'en_attente': total_en_attente,
            'rejetes': total_rejetes,
            'suspendus': total_suspendus,
        }
        return reponse


class AdminConducteurVerificationView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Conducteur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        nom_complet = f"{u.first_name} {u.last_name}".strip() or u.email
        dernier_doc = u.verification_documents.order_by('-created_at').first()

        # Véhicule
        voiture = u.voitures.first()
        vehicule_info = {
            'marque_modele': f"{voiture.marque_voiture} {voiture.model_voiture}" if voiture else "Renault Clio IV",
            'immatriculation': voiture.plaque if voiture else "DK-2045-A",
            'nombre_places': f"{voiture.nombres_de_places} places passager" if voiture else "4 places passager",
            'couleur': voiture.couleur if voiture else "Blanc",
            'climatisee': voiture.est_climatisee if voiture else True,
            'photo': request.build_absolute_uri(voiture.photo_voiture.url) if voiture and voiture.photo_voiture else '',
        }

        # Documents requis (Permis, Carte grise, Assurance)
        def get_doc_url(champ):
            if dernier_doc and getattr(dernier_doc, champ, None):
                fichier = getattr(dernier_doc, champ)
                try:
                    return request.build_absolute_uri(fichier.url)
                except Exception:
                    return ""
            return ""

        documents = {
            'id': dernier_doc.id if dernier_doc else None,
            'permis_conduire': get_doc_url('permis_conduire'),
            'carte_grise': get_doc_url('carte_grise'),
            'assurance': get_doc_url('assurance'),
            'photo_vehicule': get_doc_url('photo_vehicule'),
            'status': dernier_doc.status if dernier_doc else 'PENDING',
            'motif_rejet': dernier_doc.motif_rejet if dernier_doc else '',
            'created_at': dernier_doc.created_at.strftime('%d %B %Y') if dernier_doc and dernier_doc.created_at else u.date_joined.strftime('%d %B %Y'),
        }

        return Response({
            'conducteur': {
                'id': u.id,
                'nom': nom_complet,
                'email': u.email,
                'telephone': u.telephone or '+221 77 987 65 43',
                'photo': request.build_absolute_uri(u.photo.url) if u.photo else '',
                'statut': 'EN_ATTENTE' if (dernier_doc and dernier_doc.status == 'PENDING') else ('VERIFIE' if u.is_verified else 'SUSPENDU'),
                'is_verified': u.is_verified,
                'date_inscription': u.date_joined.strftime('%d %B %Y') if u.date_joined else '',
            },
            'vehicule': vehicule_info,
            'documents': documents,
        })


class AdminConducteurApprouverView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def post(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Conducteur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        # 1. Valider le document s'il existe
        doc = u.verification_documents.order_by('-created_at').first()
        if doc:
            doc.status = VerificationDocument.Status.APPROUVE
            doc.motif_rejet = ''
            doc.save(update_fields=['status', 'motif_rejet'])

        # 2. Promouvoir l'utilisateur
        u.role = User.Role.CONDUCTEUR
        u.is_verified = True
        u.save(update_fields=['role', 'is_verified'])

        return Response({
            'succes': True,
            'message': f"Le conducteur {u.first_name or u.email} a été vérifié et approuvé avec succès !",
            'is_verified': True,
            'role': u.role,
        })


class AdminConducteurRejeterView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def post(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Conducteur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        motif = request.data.get('motif', '').strip()
        if not motif:
            return Response({'detail': 'Veuillez renseigner un motif de rejet.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Rejeter le document
        doc = u.verification_documents.order_by('-created_at').first()
        if doc:
            doc.status = VerificationDocument.Status.REJETE
            doc.motif_rejet = motif
            doc.save(update_fields=['status', 'motif_rejet'])

        # 2. Révoquer la vérification
        u.is_verified = False
        u.save(update_fields=['is_verified'])

        return Response({
            'succes': True,
            'message': f"La demande de {u.first_name or u.email} a été rejetée.",
            'motif': motif,
            'is_verified': False,
        })


# ==============================================================================
# 4. SUPERVISION DES TRAJETS
# ==============================================================================
class AdminTrajetsView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request):
        qs = Trajet.objects.all().select_related('conducteur', 'voiture').order_by('-date', '-heure_depart')

        # Filtre par statut
        statut = request.query_params.get('statut', '').strip().upper()
        if statut in ['PLANIFIE', 'EN_COURS', 'TERMINE', 'ANNULE']:
            qs = qs.filter(statut=statut)

        # Recherche textuelle
        q = request.query_params.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(lieu_depart__icontains=q) |
                Q(destination__icontains=q) |
                Q(conducteur__first_name__icontains=q) |
                Q(conducteur__last_name__icontains=q) |
                Q(conducteur__email__icontains=q)
            )

        paginator = AdminPagination()
        page = paginator.paginate_queryset(qs, request)

        trajets = []
        for t in page:
            cond = t.conducteur
            cond_nom = f"{cond.first_name} {cond.last_name}".strip() or cond.email
            places_totales = t.voiture.nombres_de_places if t.voiture else 4
            places_prises = max(places_totales - t.places_disponibles, 0)

            trajets.append({
                'id': t.id,
                'code': f"TR-{t.id:04d}",
                'conducteur': {
                    'id': cond.id,
                    'nom': cond_nom,
                    'photo': request.build_absolute_uri(cond.photo.url) if cond.photo else '',
                },
                'itineraire': f"{t.lieu_depart} ➔ {t.destination}",
                'depart': t.lieu_depart,
                'destination': t.destination,
                'date': t.date.strftime('%d %b %Y') if t.date else '',
                'heure': t.heure_depart.strftime('%H:%M') if t.heure_depart else '',
                'places_prises': places_prises,
                'places_totales': places_totales,
                'places_ratio': f"{places_prises}/{places_totales}",
                'prix_par_place': int(t.prix_par_place),
                'statut': t.statut,
            })

        return paginator.get_paginated_response(trajets)


class AdminTrajetAnnulerView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def post(self, request, pk):
        try:
            t = Trajet.objects.get(pk=pk)
        except Trajet.DoesNotExist:
            return Response({'detail': 'Trajet introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        t.statut = Trajet.StatutTrajet.ANNULE
        t.save(update_fields=['statut'])
        return Response({'succes': True, 'message': f"Le trajet TR-{t.id:04d} a été annulé."})


# ==============================================================================
# 5. SUPERVISION DES RÉSERVATIONS
# ==============================================================================
class AdminReservationsView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request):
        qs = Reservation.objects.all().select_related('passager', 'trajet', 'trajet__conducteur').order_by('-created_at')

        statut = request.query_params.get('statut', '').strip().upper()
        if statut in ['CONFIRMEE', 'ANNULEE']:
            qs = qs.filter(statut=statut)

        paginator = AdminPagination()
        page = paginator.paginate_queryset(qs, request)

        reservations = []
        for r in page:
            p = r.passager
            t = r.trajet
            c = t.conducteur if t else None
            reservations.append({
                'id': r.id,
                'code': f"RES-{r.id:04d}",
                'passager': {
                    'id': p.id,
                    'nom': f"{p.first_name} {p.last_name}".strip() or p.email,
                    'email': p.email,
                    'photo': request.build_absolute_uri(p.photo.url) if p.photo else '',
                },
                'trajet_id': t.id if t else None,
                'trajet_code': f"TR-{t.id:04d}" if t else '',
                'itineraire': f"{t.lieu_depart} ➔ {t.destination}" if t else '',
                'conducteur_nom': f"{c.first_name} {c.last_name}".strip() or c.email if c else '',
                'places': r.nombre_de_places,
                'montant': int(r.nombre_de_places * t.prix_par_place) if t else 0,
                'date_trajet': t.date.strftime('%d %b %Y') if t and t.date else '',
                'heure_trajet': t.heure_depart.strftime('%H:%M') if t and t.heure_depart else '',
                'statut': r.statut,
                'date_reservation': r.created_at.strftime('%d %b %Y %H:%M'),
            })

        return paginator.get_paginated_response(reservations)


# ==============================================================================
# 6. MODÉRATION DES AVIS & ÉVALUATIONS
# ==============================================================================
class AdminAvisView(APIView):
    permission_classes = [IsAdminOrStaffPermission]

    def get(self, request):
        qs = Evaluation.objects.all().select_related('auteur', 'destinataire', 'trajet').order_by('-created_at')

        paginator = AdminPagination()
        page = paginator.paginate_queryset(qs, request)

        avis = []
        for ev in page:
            avis.append({
                'id': ev.id,
                'auteur': {
                    'id': ev.auteur.id,
                    'nom': f"{ev.auteur.first_name} {ev.auteur.last_name}".strip() or ev.auteur.email,
                    'photo': request.build_absolute_uri(ev.auteur.photo.url) if ev.auteur.photo else '',
                },
                'destinataire': {
                    'id': ev.destinataire.id,
                    'nom': f"{ev.destinataire.first_name} {ev.destinataire.last_name}".strip() or ev.destinataire.email,
                },
                'note': ev.note,
                'commentaire': ev.commentaire or '',
                'date': ev.created_at.strftime('%d %b %Y'),
            })

        return paginator.get_paginated_response(avis)

    def delete(self, request, pk):
        try:
            ev = Evaluation.objects.get(pk=pk)
            ev.delete()
            return Response({'succes': True, 'message': 'Avis supprimé avec succès.'})
        except Evaluation.DoesNotExist:
            return Response({'detail': 'Avis introuvable.'}, status=status.HTTP_404_NOT_FOUND)
