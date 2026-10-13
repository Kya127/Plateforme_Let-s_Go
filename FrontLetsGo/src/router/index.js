import { createRouter, createWebHistory } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import EcranSplash from '../views/demarrage/EcranSplash.vue'
import EcranHero from '../views/hero/EcranHero.vue'
import EcranOnboarding from '../views/onboarding/EcranOnboarding.vue'
import VueConnexion from '../views/auth/VueConnexion.vue'
import VueInscription from '../views/auth/VueInscription.vue'
import PageAccueil from '../views/accueil/PageAccueil.vue'
import InfosPerso from '../views/conducteur/InfosPerso.vue'
import Vehicule from '../views/conducteur/Vehicule.vue'
import DocumentsConducteur from '../views/conducteur/DocumentsConducteur.vue'
import TableauDeBordConducteur from '../views/conducteur/TableauDeBordConducteur.vue'
import DriverSubmissionSuccessModal from '@/components/common/DriverSubmissionSuccessModal.vue'
import PublierTrajet from '@/views/conducteur/PublierTrajet.vue'
import TrajetsPrevus from '@/views/conducteur/TrajetsPrevus.vue'
import VueTrajetPrevu from '@/views/conducteur/VueTrajetPrevu.vue'
import PaiementCommission from '@/views/conducteur/PaiementCommission.vue'
import EvaluerTrajet from '@/views/conducteur/EvaluerTrajet.vue'
import EvaluationConfirmation from '@/views/conducteur/EvaluationConfirmation.vue'
import RechercheVocale from '@/views/Passager/RechercheVocale.vue'
import ResultatsRecherche from '@/views/Passager/ResultatsRecherche.vue'
import TrajetDetail from '@/views/Passager/TrajetDetail.vue'
import ResumeReservation from '@/views/Passager/ResumeReservation.vue'
import ReservationConfirmee from '@/views/Passager/ReservationConfirmee.vue'
import ProfilConducteur from '@/views/Passager/ProfilConducteur.vue'
import VueVerificationCompte from '../views/auth/VueVerificationCompte.vue'
import VueMotDePasseOublie from '../views/auth/VueMotDePasseOublie.vue'
import VueMonProfil from '../views/profil/VueMonProfil.vue'
import VueModifierProfil from '../views/profil/VueModifierProfil.vue'

// Vues Administration LET'S GO
import LayoutAdmin from '../views/admin/LayoutAdmin.vue'
import VueDashboardAdmin from '../views/admin/VueDashboardAdmin.vue'
import VueUtilisateursAdmin from '../views/admin/VueUtilisateursAdmin.vue'
import VueDetailUtilisateurAdmin from '../views/admin/VueDetailUtilisateurAdmin.vue'
import VueConducteursAdmin from '../views/admin/VueConducteursAdmin.vue'
import VueVerificationConducteurAdmin from '../views/admin/VueVerificationConducteurAdmin.vue'
import VueTrajetsAdmin from '../views/admin/VueTrajetsAdmin.vue'
import VueReservationsAdmin from '../views/admin/VueReservationsAdmin.vue'
import VueAvisAdmin from '../views/admin/VueAvisAdmin.vue'
import VueStatistiquesAdmin from '../views/admin/VueStatistiquesAdmin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/splash',
    },
    {
      path: '/splash',
      name: 'splash',
      component: EcranSplash,
    },
    {
      path: '/hero',
      name: 'hero',
      component: EcranHero,
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: EcranOnboarding,
    },
    {
      path: '/accueil',
      name: 'accueil',
      component: PageAccueil,
    },
    {
      path: '/connexion',
      name: 'connexion',
      component: VueConnexion,
    },
    {
      path: '/verification-compte',
      name: 'verification-compte',
      component: VueVerificationCompte,
    },
    {
      path: '/mot-de-passe-oublie',
      name: 'mot-de-passe-oublie',
      component: VueMotDePasseOublie,
    },
    {
      path: '/conducteur/infos-personnelles',
      name: 'conducteur-infos-personnelles',
      component: InfosPerso,
      meta: { requiresAuth: true },
    },
    {
      path: '/conducteur/vehicule',
      name: 'conducteur-vehicule',
      component: Vehicule,
      meta: { requiresAuth: true },
    },
    {
      path: '/conducteur/documents',
      name: 'conducteur-documents',
      component: DocumentsConducteur,
      meta: { requiresAuth: true },
    },
    {
      path: '/conducteur/confirmation',
      name: 'conducteur-confirmation',
      component: DriverSubmissionSuccessModal,
      meta: { requiresAuth: true },
    },
    {
      path: '/conducteur/tableau-de-bord',
      name: 'conducteur-tableau-de-bord',
      component: TableauDeBordConducteur,
      meta: { requiresAuth: true },
    },
    {
  path: '/recherche-resultats',
  name: 'recherche-resultats', 
  component: ResultatsRecherche
},
  {
    path: '/trajet/:id',
    name: 'vue-trajet-detail',
    component: TrajetDetail
  },
  {
    path: '/conducteur/profil/:id',
    name: 'profil-conducteur',
    component: ProfilConducteur
  },
  {
    path: '/profil',
    name: 'mon-profil',
    component: VueMonProfil,
    meta: { requiresAuth: true },
  },
  {
    path: '/profil/modifier',
    name: 'modifier-profil',
    component: VueModifierProfil,
    meta: { requiresAuth: true },
  },
  {
    path: '/reservation/resume/:id?',
    name: 'resume-reservation',
    component: ResumeReservation
  },
  {
    path: '/reservation/confirmee',
    name: 'reservation-confirmee',
    component: ReservationConfirmee
  },
  {
    path: '/passager/resume-reservation',
    redirect: '/reservation/resume'
  },
    {
      path: '/conducteur/publier',
      redirect: '/conducteur/tableau-de-bord',
    },
    {
      path: '/inscription',
      name: 'inscription',
      component: VueInscription,
    },
     {
      path: '/publier-trajet',
      name: 'publication',
      component: PublierTrajet,
      meta: { requiresAuth: true },
    },
     {
      path: '/vue-trajet',
      name: 'Vuetrajet',
      component: VueTrajetPrevu,
    },

    {
      path: '/paiement',
      name: 'paiement_commission',
      component: PaiementCommission,
    },
    {
      path: '/conducteur/commissions',
      redirect: to => ({
        path: '/paiement',
        query: to.query
      }),
    },

    {
      path: '/conducteur/trajets-prevus',
      redirect: '/conducteur/tableau-de-bord',
    },
    {
      path: '/conducteur/trajets-prevus/:id',
      name: 'vue-trajet-prevu',
      component: VueTrajetPrevu
    },
     {
      path: '/trajet-prevu',
      name: 'trajetprevu',
      component: TrajetsPrevus,
    },
    {
      path: '/login',
      redirect: '/connexion',
    },
    {
    path: '/evaluer-trajet/:id',
    name: 'evaluer-trajet',
    component:EvaluerTrajet
},

  {
  path: '/evaluation/confirmation',
  name: 'evaluation-confirmation',
  component: EvaluationConfirmation
},

{
  path: '/recherche-vocale',
  name: 'recherche-vocale',
  component: RechercheVocale
},

    // =========================================================================
    // PARCOURS ADMINISTRATEUR LET'S GO
    // =========================================================================
    {
      path: '/admin',
      component: LayoutAdmin,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: VueDashboardAdmin,
          meta: { title: "Vue d'ensemble", breadcrumbs: [{ label: "Vue d'ensemble" }] },
        },
        {
          path: 'utilisateurs',
          name: 'admin-utilisateurs',
          component: VueUtilisateursAdmin,
          meta: {
            title: 'Gestion des Utilisateurs',
            breadcrumbs: [{ label: 'Administration', to: '/admin' }, { label: 'Utilisateurs' }],
          },
        },
        {
          path: 'utilisateurs/:id',
          name: 'admin-utilisateur-detail',
          component: VueDetailUtilisateurAdmin,
          meta: {
            title: 'Fiche Utilisateur',
            breadcrumbs: [
              { label: 'Administration', to: '/admin' },
              { label: 'Utilisateurs', to: '/admin/utilisateurs' },
              { label: 'Détail utilisateur' },
            ],
          },
        },
        {
          path: 'demandes',
          name: 'admin-demandes',
          component: VueConducteursAdmin,
          meta: {
            title: 'Demandes de Conducteurs',
            breadcrumbs: [{ label: 'Administration', to: '/admin' }, { label: 'Demandes' }],
          },
        },
        {
          path: 'demandes/:id/verification',
          name: 'admin-demande-verification',
          component: VueVerificationConducteurAdmin,
          meta: {
            title: 'Vérification Conducteur',
            breadcrumbs: [
              { label: 'Administration', to: '/admin' },
              { label: 'Demandes', to: '/admin/demandes' },
              { label: 'Vérification' },
            ],
          },
        },
        // Rétrocompatibilité conducteurs -> demandes
        {
          path: 'conducteurs',
          redirect: '/admin/demandes',
        },
        {
          path: 'conducteurs/:id/verification',
          redirect: to => `/admin/demandes/${to.params.id}/verification`,
        },
        {
          path: 'trajets',
          name: 'admin-trajets',
          component: VueTrajetsAdmin,
          meta: {
            title: 'Supervision des Trajets',
            breadcrumbs: [{ label: 'Administration', to: '/admin' }, { label: 'Trajets' }],
          },
        },
        {
          path: 'reservations',
          name: 'admin-reservations',
          component: VueReservationsAdmin,
          meta: {
            title: 'Gestion des Réservations',
            breadcrumbs: [{ label: 'Administration', to: '/admin' }, { label: 'Réservations' }],
          },
        },
        {
          path: 'avis',
          name: 'admin-avis',
          component: VueAvisAdmin,
          meta: {
            title: 'Modération des Avis',
            breadcrumbs: [{ label: 'Administration', to: '/admin' }, { label: 'Avis' }],
          },
        },
        {
          path: 'statistiques',
          name: 'admin-statistiques',
          component: VueStatistiquesAdmin,
          meta: {
            title: 'Statistiques & Performance',
            breadcrumbs: [{ label: 'Administration', to: '/admin' }, { label: 'Statistiques' }],
          },
        },
      ],
    },
  ],
})

router.beforeEach((to, from) => {
  const storeAuth = useAuthentificationStore()

  // 1. Protection globale des routes nécessitant une authentification
  if (to.meta.requiresAuth && !storeAuth.estConnecte) {
    return {
      name: 'connexion',
      query: { redirection: to.fullPath },
    }
  }

  // 1.bis. Protection des routes administration : vérifie le statut admin
  if (to.matched.some((record) => record.meta.requiresAdmin)) {
    if (!storeAuth.estConnecte) {
      return {
        name: 'connexion',
        query: { redirection: to.fullPath },
      }
    }
    // Si l'utilisateur est connecté mais n'est pas encore synchronisé comme admin
    // et qu'il n'a pas de rôle admin, on le laisse si c'est le compte de test ou admin
    const role = (storeAuth.utilisateur?.role || '').toLowerCase()
    if (role && role !== 'administrateur' && role !== 'admin' && !storeAuth.estAdmin) {
      // Redirection si rôle passager strict
      return { name: 'accueil' }
    }
  }

  // 2. Publication de trajet : doit être connecté ET conducteur vérifié
  if (to.name === 'publication' || to.path === '/publier-trajet') {
    if (!storeAuth.estConnecte) {
      return {
        name: 'connexion',
        query: { redirection: '/publier-trajet' },
      }
    }

    if (!storeAuth.utilisateur?.estConducteurVerifie) {
      return {
        name: 'conducteur-infos-personnelles',
        query: { requis: 'verification-conducteur' }
      }
    }
  }

  // 3. Parcours "Devenir Conducteur" : respect strict et obligatoire des étapes
  // Étape 2 (Véhicule) : nécessite d'avoir rempli l'Étape 1 (Infos personnelles)
  if (to.name === 'conducteur-vehicule') {
    const hasStep1 = sessionStorage.getItem('letsgo_onboarding_infos_perso')
    if (!hasStep1) {
      return { name: 'conducteur-infos-personnelles' }
    }
  }

  // Étape 3 (Documents) : nécessite d'avoir rempli l'Étape 1 ET l'Étape 2
  if (to.name === 'conducteur-documents') {
    const hasStep1 = sessionStorage.getItem('letsgo_onboarding_infos_perso')
    const hasStep2 = sessionStorage.getItem('letsgo_onboarding_vehicule')
    if (!hasStep1) {
      return { name: 'conducteur-infos-personnelles' }
    }
    if (!hasStep2) {
      return { name: 'conducteur-vehicule' }
    }
  }

  return true
})

export default router
