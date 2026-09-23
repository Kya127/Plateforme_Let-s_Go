<template>
  <main class="driver-page">
    <section class="driver-screen">

      <!-- HEADER -->
      <header class="page-header">
        <div class="header-top">
          <button
            class="back-button"
            type="button"
            aria-label="Retour"
            @click="goBack"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="M15 5L8 12L15 19"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>

          <div class="header-title">
            <h1>Devenir Conducteur</h1>

            <span class="step-badge">
              ÉTAPE 3 SUR 3
            </span>
          </div>
        </div>

        <div
          class="progress-bar"
          aria-label="Étape 3 sur 3"
        >
          <span class="progress-segment is-completed"></span>
          <span class="progress-segment is-completed"></span>
          <span class="progress-segment is-active"></span>
        </div>
      </header>

      <!-- CONTENU -->
      <div class="page-content">

        <section class="intro">
          <h2>Documents</h2>

          <p>
            Veuillez télécharger les documents nécessaires
            pour valider votre profil conducteur.
          </p>
        </section>

        <section class="documents-list">

          <DocumentUploadCard
            title="Permis de conduite"
            description="Format JPG, PNG ou PDF"
            icon="license"
            :uploaded="documents.license"
            @upload="handleUpload('license', $event)"
          />

          <DocumentUploadCard
            title="Carte Grise du véhicule"
            description="Format JPG, PNG ou PDF"
            icon="carte"
            :uploaded="documents.registration"
            @upload="handleUpload('registration', $event)"
          />

          <DocumentUploadCard
            title="Certificat d'assurance"
            description="Doit être en cours de validité"
            icon="insurance"
            :uploaded="documents.insurance"
            @upload="handleUpload('insurance', $event)"
          />

        </section>

        <!-- CONSEIL -->
        <aside class="photo-tip">
          <div class="tip-icon">
            <svg viewBox="0 0 48 48" fill="none">
              <path
                d="M28.5 4L8 26.5H21L18 44L40 19H27L28.5 4Z"
                fill="currentColor"
              />
            </svg>
          </div>

          <div class="tip-content">
            <h3>Conseil Photo</h3>

            <p>
              Prenez des photos bien éclairées sans reflets
              pour accélérer la validation de votre profil
              par nos équipes.
            </p>
          </div>
        </aside>

        <!-- CTA -->
        <button
          class="finish-button"
          type="button"
          :disabled="!canSubmitDocuments"
          @click="finishRegistration"
        >
          Finaliser mon inscription
        </button>

      </div>
    </section>

    <!-- ===============================
         POPUP DE CONFIRMATION
    ================================== -->
    <DriverSubmissionSuccessModal
      v-model="showSuccessModal"
      @home="goHome"
    />
  </main>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import DocumentUploadCard from '@/components/common/DocumentUploadCard.vue'
import DriverSubmissionSuccessModal from '@/components/common/DriverSubmissionSuccessModal.vue'

const STORAGE_KEY = 'letsgo_onboarding_documents'
const router = useRouter()

const showSuccessModal = ref(false)

const documents = reactive({
  license: false,
  registration: false,
  insurance: false
})

const uploadedFiles = reactive({
  license: null,
  registration: null,
  insurance: null
})

const persistState = () => {
  sessionStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ documents: { ...documents } })
  )
}

const hydrateState = () => {
  try {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '{}')

    if (saved.documents) {
      Object.keys(documents).forEach((key) => {
        documents[key] = Boolean(saved.documents[key])
      })
    }
  } catch (error) {
    console.warn('Erreur lecture état documents:', error)
  }
}

const canSubmitDocuments = computed(() => {
  return Object.values(documents).every(Boolean)
})

const handleUpload = (type, file) => {
  uploadedFiles[type] = file
  documents[type] = !!file
  persistState()
}

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/conducteur/vehicule')
  }
}

const finishRegistration = async () => {
  if (!canSubmitDocuments.value) return

  /*
   * Ici :
   *
   * 1. Appel API Django / DRF
   * 2. Upload des documents
   * 3. Enregistrement de la demande conducteur
   * 4. Une fois l'API validée :
   */

  persistState()
  showSuccessModal.value = true
}

const goHome = () => {
  router.push('/')
}

onMounted(() => {
  hydrateState()
})

watch(
  documents,
  () => {
    persistState()
  },
  { deep: true }
)
</script>

<style scoped>
.driver-page {
  min-height: 100vh;

  display: flex;
  justify-content: center;

  background: #f3f4f6;

  font-family:
    "Plus Jakarta Sans",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}

.driver-screen {
  width: min(100%, 828px);
  min-height: 100vh;

  background: #ffffff;

  border-radius: 40px;

  overflow: hidden;

  box-shadow:
    0 12px 40px rgba(17, 22, 39, 0.08);
}

/* =====================================================
   HEADER
===================================================== */

.page-header {
  padding: 52px 80px 30px;

  border-bottom: 1px solid #e6e8ec;
}

.header-top {
  display: flex;
  align-items: center;
  gap: 26px;
}

.back-button {
  width: 40px;
  height: 40px;

  flex-shrink: 0;

  display: grid;
  place-items: center;

  padding: 0;

  border: 0;
  background: transparent;

  color: #708099;

  cursor: pointer;
}

.back-button svg {
  width: 32px;
  height: 32px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 14px;

  flex-wrap: wrap;
}

.header-title h1 {
  margin: 0;

  color: #111627;

  font-size: 16px;
  line-height: 1.2;
  font-weight: 700;

  letter-spacing: -0.4px;
}

.step-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  padding: 7px 11px;

  border-radius: var(--radius-full);
  background: #f2f3f5;

  color: #737c8a;

  font-size: 10px;
  line-height: 1;
  font-weight: 700;

  white-space: nowrap;
}

/* =====================================================
   PROGRESS
===================================================== */
.progress-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
  margin-top: 36px;
}

.progress-segment {
  height: 11px;
  border-radius: 999px;
  background: #e5e7eb;
}

.progress-segment.is-completed,
.progress-segment.is-active {
  background: #ff4d2d;
}
/* =====================================================
   CONTENT
===================================================== */

.page-content {
  padding: 66px 80px 76px;
}

/* =====================================================
   INTRO
===================================================== */

.intro h2 {
  margin: 0;

  color: #111627;

  font-size: 20px;
  line-height: 1.15;
  font-weight: 800;

  letter-spacing: -1.5px;
}

.intro p {
  max-width: 650px;

  margin: 25px 0 0;

  color: #737c8a;

  font-size: 31px;
  line-height: 1.48;
  font-weight: 400;

  letter-spacing: -0.7px;
}

/* =====================================================
   DOCUMENTS
===================================================== */

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 30px;

  margin-top: 76px;
}

/* =====================================================
   PHOTO TIP
===================================================== */

.photo-tip {
  display: flex;
  align-items: flex-start;
  gap: 26px;

  margin-top: 60px;
  padding: 45px 44px;

  border-radius: 48px;

  background: #fff5f2;
}

.tip-icon {
  flex: 0 0 55px;

  width: 55px;
  height: 55px;

  color: #ff4d2d;
}

.tip-icon svg {
  width: 100%;
  height: 100%;
}

.tip-content {
  min-width: 0;
}

.tip-content h3 {
  margin: 0 0 13px;

  color: #ff4d2d;

  font-size: 27px;
  line-height: 1.2;
  font-weight: 800;

  letter-spacing: -0.5px;
}

.tip-content p {
  margin: 0;

  color: #354157;

  font-size: 23px;
  line-height: 1.6;
  font-weight: 400;
}

/* =====================================================
   BUTTON
===================================================== */

.finish-button {
  width: 100%;
  min-height: 120px;

  margin-top: 74px;

  border: 0;
  border-radius: 34px;

  background: #ff4d2d;
  color: #ffffff;

  font-family: inherit;
  font-size: 30px;
  font-weight: 800;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color 0.2s ease;
}

.finish-button:hover {
  background: #f94728;
  transform: translateY(-2px);

  box-shadow:
    0 14px 30px rgba(255, 77, 45, 0.22);
}

.finish-button:active {
  transform: translateY(0);
}

.finish-button:focus-visible {
  outline: 4px solid rgba(255, 77, 45, 0.25);
  outline-offset: 4px;
}

/* =====================================================
   RESPONSIVE
===================================================== */

@media (max-width: 700px) {
  .driver-screen {
    border-radius: 0;
  }

  .page-header {
    padding: 28px 24px 22px;
  }

  .header-top {
    gap: 12px;
  }

  .header-title {
    gap: 10px;
  }

  .header-title h1 {
    font-size: 25px;
  }

  .step-badge {
    padding: 8px 12px;
    font-size: 13px;
  }

  .progress-bar {
    margin-top: 25px;
  }

  .progress-segment {
    height: 8px;
  }

  .page-content {
    padding: 42px 24px 50px;
  }

  .intro h2 {
    font-size: 34px;
  }

  .intro p {
    margin-top: 17px;
    font-size: 21px;
    line-height: 1.48;
  }

  .documents-list {
    margin-top: 42px;
    gap: 18px;
  }

  .photo-tip {
    margin-top: 36px;
    padding: 30px 24px;
    gap: 18px;
    border-radius: 30px;
  }

  .tip-icon {
    flex-basis: 38px;
    width: 38px;
    height: 38px;
  }

  .tip-content h3 {
    font-size: 20px;
  }

  .tip-content p {
    font-size: 17px;
    line-height: 1.55;
  }

  .finish-button {
    min-height: 82px;
    margin-top: 46px;
    border-radius: 25px;
    font-size: 21px;
  }
}
</style>