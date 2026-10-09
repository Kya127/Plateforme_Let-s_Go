import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { serviceAuth } from '@/services/api'
import { getAvatarUrl } from '@/utils/avatar'

export const useAuthentificationStore = defineStore('authentification', () => {
  const estConnecte = ref(!!localStorage.getItem('letsgo_access_token'))
  const profilComplet = ref(false)
  const chargement = ref(false)
  const erreur = ref(null)

  // Utilisateur par défaut
  const utilisateur = ref({
    id: null,
    prenom: '',
    nom: '',
    nomComplet: '',
    email: '',
    telephone: '',
    photoUrl: null,
    role: 'passager', // 'passager' ou 'conducteur'
    note: 5.0,
    estConducteurVerifie: false,
  })

  // Mémorise la route demandée avant redirection vers la connexion
  const intentionRedirection = ref('')

  const nomAffiche = computed(() => {
    return utilisateur.value?.prenom || utilisateur.value?.nomComplet || 'Utilisateur'
  })

  const avatarActif = computed(() => {
    const prenom = (utilisateur.value?.prenom || '').trim()
    const nom = (utilisateur.value?.nom || '').trim()
    if (prenom && nom) {
      return getAvatarUrl(utilisateur.value?.photoUrl, prenom, nom)
    }
    const nomComplet = (utilisateur.value?.nomComplet || prenom || nom || 'Utilisateur').trim()
    return getAvatarUrl(utilisateur.value?.photoUrl, nomComplet)
  })

  const estConducteur = computed(() => {
    return utilisateur.value?.role === 'conducteur'
  })

  // Synchronise le profil depuis l'API
  function mapperUtilisateur(donnees) {
    if (!donnees) return
    const prenom = (donnees.first_name || donnees.prenom || '').trim()
    const nom = (donnees.last_name || donnees.nom || '').trim()
    const nomComplet = `${prenom} ${nom}`.trim() || donnees.email || 'Utilisateur'
    utilisateur.value = {
      id: donnees.id,
      prenom,
      nom,
      nomComplet,
      email: donnees.email || '',
      telephone: donnees.telephone || '',
      photoUrl: donnees.photo || null,
      role: donnees.role || 'passager',
      note: donnees.note || 4.8,
      estConducteurVerifie: donnees.is_verified || false,
    }
    profilComplet.value = !!donnees.is_profile_complete
    estConnecte.value = true
    localStorage.setItem('letsgo_utilisateur', JSON.stringify(utilisateur.value))
  }


  // Initialisation au démarrage de l'app
  async function initialiserSession() {
    const token = localStorage.getItem('letsgo_access_token')
    if (!token) {
      estConnecte.value = false
      return
    }

    // Restaurer le cache local d'abord pour un affichage instantané
    const cache = localStorage.getItem('letsgo_utilisateur')
    if (cache) {
      try {
        const u = JSON.parse(cache)
        if (u) {
          const prenom = (u.prenom || u.first_name || '').trim()
          const nom = (u.nom || u.last_name || '').trim()
          u.prenom = prenom
          u.nom = nom
          if (!u.nomComplet || u.nomComplet === prenom) {
            u.nomComplet = `${prenom} ${nom}`.trim() || u.email || 'Utilisateur'
          }
          utilisateur.value = u
          estConnecte.value = true
        }
      } catch (e) {
        console.error('Erreur parsing cache utilisateur:', e)
      }
    }

    try {
      const profil = await serviceAuth.getProfil()
      mapperUtilisateur(profil)
    } catch (e) {
      console.warn('Session expirée ou profil inaccessible:', e)
      // Si le token est invalide, déconnecter
      if (e.response?.status === 401) {
        deconnecter()
      }
    }
  }

  // Connexion réelle via JWT (support Email et Téléphone sénégalais)
  async function connecter(identifiant, motDePasse) {
    chargement.value = true
    erreur.value = null
    try {
      const data = await serviceAuth.connexion({
        identifiant: identifiant,
        email: identifiant,
        username: identifiant,
        telephone: identifiant,
        password: motDePasse,
      })

      localStorage.setItem('letsgo_access_token', data.access)
      if (data.refresh) {
        localStorage.setItem('letsgo_refresh_token', data.refresh)
      }

      estConnecte.value = true

      // Charger le profil réel
      const profil = await serviceAuth.getProfil()
      mapperUtilisateur(profil)
      return { succes: true }
    } catch (err) {
      console.error('Erreur de connexion:', err)
      const dataErr = err.response?.data || {}
      const detail = dataErr.detail
      const message = Array.isArray(detail)
        ? detail[0]
        : (typeof detail === 'string' ? detail : (detail || 'Identifiants incorrects. Veuillez vérifier votre adresse e-mail ou numéro de téléphone et mot de passe.'))
      
      const nonVerifie = Boolean(dataErr.non_verifie?.[0] ?? dataErr.non_verifie)
      const emailNonVerifie = Array.isArray(dataErr.email) ? dataErr.email[0] : (dataErr.email || '')

      erreur.value = message
      return { 
        succes: false, 
        erreur: message,
        nonVerifie: nonVerifie,
        email: emailNonVerifie
      }
    } finally {
      chargement.value = false
    }
  }

  // Inscription réelle
  async function inscrire(donnees) {
    chargement.value = true
    erreur.value = null
    try {
      const reponse = await serviceAuth.inscription(donnees)
      return { succes: true, data: reponse }
    } catch (err) {
      console.error("Erreur d'inscription:", err)
      let message = "Impossible de créer le compte. Veuillez vérifier les informations saisies."

      const emailErr = err.response?.data?.email?.[0]
      const phoneErr = err.response?.data?.telephone?.[0]
      const detailErr = err.response?.data?.detail

      if (emailErr && emailErr.toLowerCase().includes('already exists')) {
        message = "Un compte existe déjà avec cette adresse e-mail. Vous pouvez vous connecter directement."
      } else if (phoneErr && phoneErr.toLowerCase().includes('already exists')) {
        message = "Ce numéro de téléphone est déjà associé à un compte existant."
      } else if (emailErr) {
        message = emailErr
      } else if (phoneErr) {
        message = phoneErr
      } else if (detailErr) {
        message = Array.isArray(detailErr) ? detailErr[0] : detailErr
      }

      erreur.value = message
      return { succes: false, erreur: message }
    } finally {
      chargement.value = false
    }
  }

  // Vérification de code OTP d'activation de compte
  async function verifierCode(donnees) {
    chargement.value = true
    erreur.value = null
    try {
      const reponse = await serviceAuth.verifierCode(donnees)
      // Le compte est activé avec succès en base.
      // L'utilisateur est ensuite redirigé vers /connexion pour saisir son mot de passe ou utiliser l'autofill.
      return { 
        succes: true, 
        message: reponse.message, 
        dejaActif: reponse.deja_actif,
        tokens: reponse.tokens,
      }
    } catch (err) {
      console.error("Erreur vérification code:", err)
      const msg = err.response?.data?.detail || "Code incorrect ou expiré. Veuillez vérifier et réessayer."
      erreur.value = msg
      return { succes: false, erreur: msg }
    } finally {
      chargement.value = false
    }
  }

  // Renvoyer le code OTP de confirmation
  async function renvoyerCode(email) {
    chargement.value = true
    erreur.value = null
    try {
      const reponse = await serviceAuth.renvoyerCode({ email })
      return { succes: true, message: reponse.message, dejaActif: reponse.deja_actif }
    } catch (err) {
      console.error("Erreur renvoi code:", err)
      const msg = err.response?.data?.detail || "Impossible de renvoyer le code. Veuillez patienter avant de réessayer."
      erreur.value = msg
      return { succes: false, erreur: msg }
    } finally {
      chargement.value = false
    }
  }

  // Déconnexion
  async function deconnecter() {
    const refresh = localStorage.getItem('letsgo_refresh_token')
    await serviceAuth.deconnexion(refresh)
    estConnecte.value = false
    profilComplet.value = false
    intentionRedirection.value = ''
    utilisateur.value = {
      id: null,
      prenom: '',
      nom: '',
      nomComplet: '',
      email: '',
      telephone: '',
      photoUrl: null,
      role: 'passager',
      note: 5.0,
      estConducteurVerifie: false,
    }
  }

  function marquerProfilComplet() {
    profilComplet.value = true
  }

  function definirIntentionRedirection(routeCible) {
    intentionRedirection.value = routeCible
  }

  function consommerIntentionRedirection(routeDefaut = '/conducteur/infos-personnelles') {
    const cible = intentionRedirection.value || routeDefaut
    intentionRedirection.value = ''
    return cible
  }

  // Demande de réinitialisation de mot de passe (envoi du code OTP)
  async function demanderResetMotDePasse(email) {
    chargement.value = true
    erreur.value = null
    try {
      const reponse = await serviceAuth.demanderResetMotDePasse({ email })
      return { 
        succes: true, 
        message: reponse.message,
        dejaEnvoye: !!reponse.deja_envoye,
        secondesRestantes: reponse.secondes_restantes || 60,
      }
    } catch (err) {
      console.error("Erreur demande reset mdp:", err)
      const msg = err.response?.data?.detail || "Impossible d'envoyer le code de réinitialisation. Veuillez réessayer."
      erreur.value = msg
      return { succes: false, erreur: msg }
    } finally {
      chargement.value = false
    }
  }

  // Vérification intermédiaire du code OTP pour reset mot de passe (Étape 1)
  async function verifierCodeReset(donnees) {
    chargement.value = true
    erreur.value = null
    try {
      const reponse = await serviceAuth.verifierCodeReset(donnees)
      return { succes: true, message: reponse.message }
    } catch (err) {
      console.error("Erreur vérification code reset:", err)
      const msg = err.response?.data?.detail || "Code invalide ou expiré. Veuillez vérifier et réessayer."
      erreur.value = msg
      return { succes: false, erreur: msg }
    } finally {
      chargement.value = false
    }
  }

  // Validation finale du code et définition du nouveau mot de passe (Étape 2)
  async function reinitialiserMotDePasse(donnees) {
    chargement.value = true
    erreur.value = null
    try {
      const reponse = await serviceAuth.reinitialiserMotDePasse(donnees)
      return { succes: true, message: reponse.message }
    } catch (err) {
      console.error("Erreur validation reset mdp:", err)
      const msg = err.response?.data?.detail || "Code invalide ou expiré. Veuillez vérifier et réessayer."
      erreur.value = msg
      return { succes: false, erreur: msg }
    } finally {
      chargement.value = false
    }
  }

  return {
    estConnecte,
    profilComplet,
    chargement,
    erreur,
    utilisateur,
    nomAffiche,
    avatarActif,
    estConducteur,
    intentionRedirection,
    initialiserSession,
    connecter,
    inscrire,
    deconnecter,
    marquerProfilComplet,
    definirIntentionRedirection,
    consommerIntentionRedirection,
    verifierCode,
    renvoyerCode,
    demanderResetMotDePasse,
    verifierCodeReset,
    reinitialiserMotDePasse,
  }
})

// Alias pour compatibilité
export const useAuthStore = useAuthentificationStore
