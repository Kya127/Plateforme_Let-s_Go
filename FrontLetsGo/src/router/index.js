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
}
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
