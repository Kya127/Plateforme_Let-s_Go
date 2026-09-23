import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthentificationStore = defineStore('authentification', () => {
  // Par défaut, l'utilisateur n'est pas connecté lors de sa première visite
  const estConnecte = ref(false)
  const profilComplet = ref(false)

  const utilisateur = ref({
    id: 1,
    prenom: 'Thomas',
    nom: 'Meyer',
    nomComplet: 'Thomas Meyer',
    email: 'thomas.meyer@letsgo.sn',
    telephone: '+221 77 450 12 34',
    photoUrl: '/images/avatar_thomas.jpg',
    role: 'conducteur',
    note: 4.9,
    estConducteurVerifie: true,
  })

  // Permet de mémoriser où l'utilisateur voulait aller avant d'être invité à se connecter
  const intentionRedirection = ref('')

  const nomAffiche = computed(() => {
    return utilisateur.value?.prenom || 'Conducteur'
  })

  function connecter(identifiant = '', options = {}) {
    estConnecte.value = true
    if (identifiant) {
      utilisateur.value.email = identifiant
    }
    if (options.role) {
      utilisateur.value.role = options.role
    }
  }

  function marquerProfilComplet() {
    profilComplet.value = true
  }

  function deconnecter() {
    estConnecte.value = false
    profilComplet.value = false
    intentionRedirection.value = ''
  }

  function definirIntentionRedirection(routeCible) {
    intentionRedirection.value = routeCible
  }

  function consommerIntentionRedirection(routeDefaut = '/conducteur/infos-personnelles') {
    const cible = intentionRedirection.value || routeDefaut
    intentionRedirection.value = ''
    return cible
  }

  return {
    estConnecte,
    profilComplet,
    utilisateur,
    nomAffiche,
    intentionRedirection,
    connecter,
    marquerProfilComplet,
    deconnecter,
    definirIntentionRedirection,
    consommerIntentionRedirection,
  }
})
