<template>
  <div class="driver-registration">
    <!-- HEADER (Identique et cohérent avec Étape 1 & 2) -->
    <header class="page-header">
      <button
        type="button"
        class="back-button"
        aria-label="Retour"
        @click="goBack"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>

      <h1>Devenir Conducteur</h1>

      <span class="step-badge">ÉTAPE 3 SUR 3</span>
    </header>

    <!-- BARRE DE PROGRESSION 3 SEGMENTS UNIFIÉE -->
    <div class="progress-wrapper">
      <div class="progress-grid">
        <span class="progress-segment is-active"></span>
        <span class="progress-segment is-active"></span>
        <span class="progress-segment is-active"></span>
      </div>
    </div>

    <!-- CONTENU -->
    <main class="content">
      <section class="intro">
        <h2>Documents requis</h2>
        <p>
          Veuillez télécharger les documents nécessaires pour valider votre profil conducteur.
        </p>
      </section>

      <!-- Message d'erreur éventuel -->
      <div v-if="errorMessage" class="error-banner">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <!-- LISTE DES DOCUMENTS À TÉLÉCHARGER -->
      <section class="documents-list">
        <DocumentUploadCard
          title="Permis de conduire"
          description="Format JPG, PNG ou PDF"
          icon="license"
          :uploaded="!!uploadedFiles.license"
          :file-name="fileNames.license"
          @upload="handleUpload('license', $event)"
        />

        <DocumentUploadCard
          title="Carte Grise du véhicule"
          description="Format JPG, PNG ou PDF"
          icon="carte"
          :uploaded="!!uploadedFiles.registration"
          :file-name="fileNames.registration"
          @upload="handleUpload('registration', $event)"
        />

        <DocumentUploadCard
          title="Certificat d'assurance"
          description="Doit être en cours de validité"
          icon="insurance"
          :uploaded="!!uploadedFiles.insurance"
          :file-name="fileNames.insurance"
          @upload="handleUpload('insurance', $event)"
        />
      </section>

      <!-- CONSEIL PHOTO PROPRE ET DISCRET -->
      <aside class="photo-tip">
        <div class="tip-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
        </div>

        <div class="tip-content">
          <h3>Conseil Photo</h3>
          <p>
            Prenez des photos bien éclairées et lisibles sans reflets pour accélérer la validation de votre dossier.
          </p>
        </div>
      </aside>

      <!-- BOUTON D'ACTION (DÉSACTIVÉ TANT QUE LES 3 DOCUMENTS NE SONT PAS CHARGÉS) -->
      <div class="submit-wrapper">
        <button
          type="button"
          class="finish-button"
          :disabled="!canSubmitDocuments || isSubmitting"
          @click="finishRegistration"
        >
          <span v-if="!isSubmitting">Finaliser mon inscription</span>
          <span v-else class="button-loading">
            <span class="spinner"></span>
            Envoi en cours...
          </span>

          <svg v-if="!isSubmitting" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M5 12h13M13 6l6 6-6 6" />
          </svg>
        </button>
      </div>
    </main>

    <!-- MODAL DE FEEDBACK MODERNE & UI/UX -->
    <DriverSubmissionSuccessModal
      v-model="showSuccessModal"
      @home="goHome"
      @close="goHome"
    />
  </div>
</template>

<script setup>
import { computed, reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { serviceAuth, serviceVoitures } from '@/services/api'
import { useAuthentificationStore } from '@/stores/authentification'

import DocumentUploadCard from '@/components/common/DocumentUploadCard.vue'
import DriverSubmissionSuccessModal from '@/components/common/DriverSubmissionSuccessModal.vue'

const STORAGE_KEY = 'letsgo_onboarding_documents'
const router = useRouter()
const storeAuth = useAuthentificationStore()

const showSuccessModal = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

const uploadedFiles = reactive({
  license: null,
  registration: null,
  insurance: null
})

const fileNames = reactive({
  license: '',
  registration: '',
  insurance: ''
})

const canSubmitDocuments = computed(() => {
  return !!uploadedFiles.license && !!uploadedFiles.registration && !!uploadedFiles.insurance
})

const handleUpload = (type, file) => {
  if (!file) return
  uploadedFiles[type] = file
  fileNames[type] = file.name || 'Document sélectionné'
  errorMessage.value = ''
}

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/conducteur/vehicule')
  }
}

// Convertit un DataURL base64 stocké en objet File pour l'envoi multipart
function dataUrlToFile(dataUrl, filename) {
  try {
    const arr = dataUrl.split(',')
    const mimeMatch = arr[0].match(/:(.*?);/)
    const mime = mimeMatch ? mimeMatch[1] : 'image/jpeg'
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n)
    }
    return new File([u8arr], filename, { type: mime })
  } catch (err) {
    console.warn('Impossible de convertir le dataURL:', err)
    return null
  }
}

const finishRegistration = async () => {
  if (!canSubmitDocuments.value || isSubmitting.value) return

  isSubmitting.value = true
  errorMessage.value = ''

  try {
    // 1. Récupération des données sauvegardées des étapes 1 et 2
    let savedInfos = null
    let savedVehicle = null

    try {
      savedInfos = JSON.parse(sessionStorage.getItem('letsgo_onboarding_infos_perso') || '{}')
      savedVehicle = JSON.parse(sessionStorage.getItem('letsgo_onboarding_vehicule') || '{}')
    } catch (e) {
      console.warn('Lecture sessionStorage:', e)
    }

    // 2. Enregistrement du véhicule dans le backend (si non déjà enregistré)
    if (savedVehicle?.form && savedVehicle.form.brand && savedVehicle.form.plate) {
      try {
        const vehicleData = new FormData()
        vehicleData.append('marque_voiture', savedVehicle.form.brand.trim())
        vehicleData.append('model_voiture', savedVehicle.form.model.trim())
        vehicleData.append('plaque', savedVehicle.form.plate.trim().toUpperCase())
        vehicleData.append('couleur', savedVehicle.form.color || 'Blanc')
        vehicleData.append('nombres_de_places', String(savedVehicle.form.seats || 4))
        vehicleData.append('est_climatisee', 'true')

        if (savedVehicle.photoDataUrl) {
          const vehiculeFile = dataUrlToFile(savedVehicle.photoDataUrl, 'vehicule.jpg')
          if (vehiculeFile) {
            vehicleData.append('photo_voiture', vehiculeFile)
          }
        }

        await serviceVoitures.ajouter(vehicleData)
      } catch (errVoiture) {
        console.warn('Note enregistrement véhicule (déjà existant ou validé):', errVoiture.response?.data || errVoiture)
      }
    }

    // 3. Préparation et envoi des documents de vérification conducteur
    const formData = new FormData()
    formData.append('permis_conduire', uploadedFiles.license)
    formData.append('carte_grise', uploadedFiles.registration)
    formData.append('assurance', uploadedFiles.insurance)

    // Joindre la photo du véhicule
    if (savedVehicle?.photoDataUrl) {
      const vehiculePhoto = dataUrlToFile(savedVehicle.photoDataUrl, 'photo_vehicule.jpg')
      if (vehiculePhoto) {
        formData.append('photo_vehicule', vehiculePhoto)
      }
    } else {
      // Fallback au permis si pas de photo spécifique
      formData.append('photo_vehicule', uploadedFiles.license)
    }

    // Joindre la photo de profil si disponible dans l'étape 1
    if (savedInfos?.photoDataUrl) {
      const photoProfil = dataUrlToFile(savedInfos.photoDataUrl, 'photo_profil.jpg')
      if (photoProfil) {
        formData.append('photo_profil', photoProfil)
        // Mettre à jour aussi le profil user direct
        const profileForm = new FormData()
        profileForm.append('photo', photoProfil)
        serviceAuth.mettreAJourProfil(profileForm).catch(() => {})
      }
    }

    // Appel API DRF pour enregistrer les documents
    await serviceAuth.devenirConducteur(formData)

    // Synchroniser l'état auth
    await storeAuth.initialiserSession()

    // Nettoyer les clés de l'onboarding temporaire
    sessionStorage.removeItem('letsgo_onboarding_infos_perso')
    sessionStorage.removeItem('letsgo_onboarding_vehicule')
    sessionStorage.removeItem('letsgo_onboarding_documents')

    // Afficher la modale moderne de feedback
    showSuccessModal.value = true
  } catch (error) {
    console.error('Erreur soumission documents:', error)
    const backendDetail = error.response?.data?.detail || error.response?.data?.message
    if (backendDetail) {
      errorMessage.value = backendDetail
    } else if (error.response?.data && typeof error.response.data === 'object') {
      const firstKey = Object.keys(error.response.data)[0]
      const firstVal = error.response.data[firstKey]
      errorMessage.value = Array.isArray(firstVal) ? firstVal[0] : String(firstVal)
    } else {
      errorMessage.value = "Une erreur est survenue lors de l'enregistrement de vos documents. Veuillez réessayer."
    }
  } finally {
    isSubmitting.value = false
  }
}

const goHome = () => {
  showSuccessModal.value = false
  router.push('/accueil')
}

onMounted(() => {
  // Vérifier si le profil a déjà un véhicule ou des infos
  storeAuth.initialiserSession()
})
</script>

<style scoped>
.driver-registration {
  --brand: #ff4d2d;
  --brand-hover: #ed4327;
  --black: #111627;
  --dark-gray: #374151;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;
  --border: #e8eaed;
  --white: #ffffff;
  --radius-full: 9999px;

  min-height: 100vh;
  background: var(--white);
  color: var(--black);
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  box-sizing: border-box;
}

@media (min-width: 600px) {
  .driver-registration {
    max-width: 440px;
    margin: 0 auto;
    border-left: 1px solid #f0f0f0;
    border-right: 1px solid #f0f0f0;
  }
}

/* HEADER */
.page-header {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
}

.back-button {
  width: 32px;
  height: 32px;
  padding: 0;
  margin: 0;
  border: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
}

.back-button svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: #8d949f;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.page-header h1 {
  margin: 0;
  font-size: 16px;
  line-height: 20px;
  font-weight: 700;
  color: #111627;
  white-space: nowrap;
}

.step-badge {
  margin-left: auto;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  background: #f0f1f3;
  color: #6b7280;
  font-size: 11px;
  line-height: 1;
  font-weight: 700;
  white-space: nowrap;
}

/* PROGRESS */
.progress-wrapper {
  padding: 4px 24px 0;
}

.progress-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  width: 100%;
}

.progress-segment {
  height: 5px;
  border-radius: var(--radius-full);
  background: #e5e7eb;
  transition: background-color 0.25s ease;
}

.progress-segment.is-active {
  background: var(--brand);
}

/* CONTENT */
.content {
  padding: 32px 24px 32px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.intro h2 {
  margin: 0 0 6px;
  font-size: 20px;
  line-height: 28px;
  font-weight: 700;
  color: #111627;
  letter-spacing: -0.3px;
}

.intro p {
  margin: 0;
  color: #92969d;
  font-size: 13px;
  line-height: 19px;
  font-weight: 400;
}

/* ERROR BANNER */
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #b91c1c;
  font-size: 13px;
  line-height: 1.4;
}

.error-banner svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

/* DOCUMENTS LIST */
.documents-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* PHOTO TIP */
.photo-tip {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: #f8fafc;
  border: 1px solid #edf2f7;
  border-radius: 14px;
}

.tip-icon {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  background: #ffedd5;
  color: #ea580c;
  border-radius: 8px;
  flex-shrink: 0;
}

.tip-icon svg {
  width: 16px;
  height: 16px;
}

.tip-content h3 {
  margin: 0 0 3px;
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
}

.tip-content p {
  margin: 0;
  font-size: 12px;
  line-height: 1.45;
  color: #64748b;
}

/* SUBMIT */
.submit-wrapper {
  margin-top: 10px;
}

.finish-button {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: 0;
  border-radius: 14px;
  background: var(--brand);
  color: #ffffff;
  font-family: inherit;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: none;
  transition: background-color 0.2s ease, opacity 0.2s ease, transform 0.15s ease;
}

.finish-button svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.finish-button:hover:not(:disabled) {
  background: var(--brand-hover);
}

.finish-button:active:not(:disabled) {
  transform: scale(0.99);
}

.finish-button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.button-loading {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>