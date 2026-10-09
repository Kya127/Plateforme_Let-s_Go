import axios from 'axios'

/* ==========================================================================
   CONFIGURATIONS DES URLS DE BASE
   ========================================================================== */
export const DJANGO_BASE_URL = 'http://127.0.0.1:8000/api/'
export const IA_BASE_URL = 'http://127.0.0.1:8001/'

/* ==========================================================================
   INSTANCE 1 : CLIENT BACKEND DJANGO REST FRAMEWORK
   ========================================================================== */
export const apiBackend = axios.create({
  baseURL: DJANGO_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

/* ==========================================================================
   INSTANCE 2 : CLIENT SERVICE IA FASTAPI (WHISPER)
   ========================================================================== */
export const apiIA = axios.create({
  baseURL: IA_BASE_URL,
  timeout: 30000, // Traitement audio potentiellement plus long
})

/* ==========================================================================
   INTERCEPTEURS REQUÊTES : INJECTION AUTOMATIQUE DU TOKEN JWT
   ========================================================================== */
apiBackend.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('letsgo_access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/* ==========================================================================
   INTERCEPTEURS RÉPONSES : REFRESH AUTOMATIQUE DU TOKEN SI EXPIRÉ (401)
   ========================================================================== */
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

apiBackend.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      // Éviter de boucler sur les endpoints de login / refresh
      if (
        originalRequest.url?.includes('auth/token/') ||
        originalRequest.url?.includes('auth/register/')
      ) {
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return apiBackend(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = localStorage.getItem('letsgo_refresh_token')

      if (!refreshToken) {
        isRefreshing = false
        localStorage.removeItem('letsgo_access_token')
        localStorage.removeItem('letsgo_refresh_token')
        return Promise.reject(error)
      }

      try {
        const { data } = await axios.post(`${DJANGO_BASE_URL}auth/token/refresh/`, {
          refresh: refreshToken,
        })

        const newAccessToken = data.access
        localStorage.setItem('letsgo_access_token', newAccessToken)

        if (data.refresh) {
          localStorage.setItem('letsgo_refresh_token', data.refresh)
        }

        apiBackend.defaults.headers.common.Authorization = `Bearer ${newAccessToken}`
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

        processQueue(null, newAccessToken)
        return apiBackend(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        localStorage.removeItem('letsgo_access_token')
        localStorage.removeItem('letsgo_refresh_token')
        localStorage.removeItem('letsgo_utilisateur')
        window.location.href = '/connexion'
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

/* ==========================================================================
   SERVICES MÉTIER CENTRALISÉS
   ========================================================================== */

// 1. Authentification & Utilisateur
export const serviceAuth = {
  // Connexion JWT (retourne { access, refresh })
  async connexion(credentials) {
    // credentials: { username/email, password }
    const response = await apiBackend.post('auth/token/', credentials)
    return response.data
  },

  // Connexion Google OAuth (reçoit le credential ID token de Google)
  async connexionGoogle(credential) {
    const response = await apiBackend.post('auth/google/', { credential })
    return response.data
  },

  // Inscription
  async inscription(donnees) {
    const response = await apiBackend.post('auth/register/', donnees)
    return response.data
  },

  // Vérification de code OTP d'activation de compte
  async verifierCode(donnees) {
    const response = await apiBackend.post('auth/verifier-code/', donnees)
    return response.data
  },

  // Renvoyer le code de vérification
  async renvoyerCode(donnees) {
    const response = await apiBackend.post('auth/renvoyer-code/', donnees)
    return response.data
  },

  // Demande de réinitialisation de mot de passe (envoi code OTP)
  async demanderResetMotDePasse(donnees) {
    const response = await apiBackend.post('auth/mot-de-passe-oublie/', donnees)
    return response.data
  },

  // Vérification intermédiaire du code OTP pour le reset de mot de passe
  async verifierCodeReset(donnees) {
    const response = await apiBackend.post('auth/verifier-code-reset/', donnees)
    return response.data
  },

  // Validation finale du code OTP et nouveau mot de passe
  async reinitialiserMotDePasse(donnees) {
    const response = await apiBackend.post('auth/reinitialiser-mot-de-passe/', donnees)
    return response.data
  },

  // Profil complet de l'utilisateur connecté
  async getProfil() {
    const response = await apiBackend.get('auth/profile/')
    return response.data
  },

  // Mise à jour du profil (avec support multipart pour la photo)
  async mettreAJourProfil(formData) {
    const isFormData = formData instanceof FormData
    const response = await apiBackend.patch('auth/profile/', formData, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : undefined,
    })
    return response.data
  },

  // Devenir conducteur / Soumettre documents
  async devenirConducteur(formData) {
    const response = await apiBackend.post('auth/become-driver/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  // Profil public d'un conducteur avec ses avis et évaluations (Mur conducteur)
  async getProfilPublicConducteur(conducteurId) {
    const response = await apiBackend.get(`auth/conducteur/${conducteurId}/profil/`)
    return response.data
  },

  // Déconnexion
  async deconnexion(refreshToken) {
    try {
      if (refreshToken) {
        await apiBackend.post('auth/logout/', { refresh: refreshToken })
      }
    } catch (e) {
      console.warn('Erreur lors du logout backend:', e)
    } finally {
      localStorage.removeItem('letsgo_access_token')
      localStorage.removeItem('letsgo_refresh_token')
      localStorage.removeItem('letsgo_utilisateur')
    }
  },
}

// 2. Trajets
export const serviceTrajets = {
  // Lister et filtrer les trajets (ex: { depart, destination, date })
  async lister(filtres = {}) {
    const response = await apiBackend.get('trajets/trajets/', { params: filtres })
    return response.data
  },

  // Obtenir mes trajets publiés en tant que conducteur
  async mesTrajets() {
    const response = await apiBackend.get('trajets/trajets/mes_trajets/')
    return response.data
  },

  // Obtenir le détail d'un trajet par ID
  async getDetail(id) {
    const response = await apiBackend.get(`trajets/trajets/${id}/`)
    return response.data
  },

  // Publier un nouveau trajet
  async publier(trajet) {
    const response = await apiBackend.post('trajets/trajets/', trajet)
    return response.data
  },

  // Modifier un trajet
  async modifier(id, donnees) {
    const response = await apiBackend.patch(`trajets/trajets/${id}/`, donnees)
    return response.data
  },

  // Démarrer un trajet
  async demarrer(id) {
    const response = await apiBackend.patch(`trajets/trajets/${id}/demarrer/`)
    return response.data
  },

  // Marquer un trajet comme terminé
  async terminer(id) {
    const response = await apiBackend.patch(`trajets/trajets/${id}/terminer/`)
    return response.data
  },

  // Annuler un trajet
  async annuler(id) {
    const response = await apiBackend.patch(`trajets/trajets/${id}/annuler/`)
    return response.data
  },
}

// 3. Réservations
export const serviceReservations = {
  // Créer une réservation
  async creer(donnees) {
    // donnees: { trajet: id, places_reservees: 1, ... }
    const response = await apiBackend.post('reservations/reservations/', donnees)
    return response.data
  },

  // Lister les réservations
  async lister() {
    const response = await apiBackend.get('reservations/reservations/')
    return response.data
  },

  // Détail d'une réservation
  async getDetail(id) {
    const response = await apiBackend.get(`reservations/reservations/${id}/`)
    return response.data
  },

  // Annuler une réservation
  async annuler(id) {
    const response = await apiBackend.patch(`reservations/reservations/${id}/annuler/`)
    return response.data
  },
}

// 4. Évaluations / Avis
export const serviceEvaluations = {
  // Laisser un avis
  async creer(avis) {
    const response = await apiBackend.post('avis/evaluations/', avis)
    return response.data
  },

  // Lister les avis
  async lister(filtres = {}) {
    const response = await apiBackend.get('avis/evaluations/', { params: filtres })
    return response.data
  },
}

// 5. Véhicules
export const serviceVoitures = {
  async lister() {
    const response = await apiBackend.get('voitures/voitures/')
    return response.data
  },

  async ajouter(formData) {
    const response = await apiBackend.post('voitures/voitures/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
}

// 6. Microservice IA Vocal & Analyse Sémantique
export const serviceIA = {
  // Option 2 : Envoi du texte transcrit pour extraction sémantique des critères (FastAPI)
  async extraireCriteres(texte) {
    const response = await apiIA.post('extract-criteria/', { text: texte })
    return response.data
  },

  // Option 1 : Envoi du flux audio binaire pour transcription et extraction (Whisper)
  async transcrireAudio(blobAudio) {
    const formData = new FormData()
    formData.append('file', blobAudio, 'enregistrement.webm')

    const response = await apiIA.post('process-audio/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
}

// 7. Commissions & Paiements
export const serviceCommissions = {
  // Récupérer ou créer la commission pour un trajet donné
  async getCommissionTrajet(trajetId) {
    const response = await apiBackend.get(`commissions/trajet/${trajetId}/`)
    return response.data
  },

  // Initier le paiement PayTech (Wave / Orange Money)
  async initierPaiement(commissionId, donnees = {}) {
    const response = await apiBackend.post(`commissions/${commissionId}/payer/`, donnees)
    return response.data
  },

  // Valider et débiter le compte Mobile Money
  async validerPaiement(commissionId, donnees = {}) {
    const response = await apiBackend.post(`commissions/${commissionId}/valider-paiement/`, donnees)
    return response.data
  },
}

export default {
  backend: apiBackend,
  ia: apiIA,
  auth: serviceAuth,
  trajets: serviceTrajets,
  reservations: serviceReservations,
  evaluations: serviceEvaluations,
  voitures: serviceVoitures,
  commissions: serviceCommissions,
}
