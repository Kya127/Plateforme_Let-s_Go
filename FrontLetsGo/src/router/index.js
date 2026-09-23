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
      path: '/conducteur/trajets-prevus/:id',
      name: 'vue-trajet-prevu',
      component: () =>
      import(
      '@/views/conducteur/VueTrajetPrevu.vue'
     )
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
  ],
})

router.beforeEach((to, from, next) => {
  const storeAuth = useAuthentificationStore()

  if (to.meta.requiresAuth && !storeAuth.estConnecte) {
    next({
      name: 'connexion',
      query: { redirection: to.fullPath },
    })
    return
  }

  if (to.name === 'conducteur-infos-personnelles' && storeAuth.estConnecte && storeAuth.profilComplet) {
    next({ name: 'conducteur-vehicule' })
    return
  }

  next()
})

export default router
