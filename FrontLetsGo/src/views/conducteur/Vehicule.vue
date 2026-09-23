<template>
  <div class="driver-registration">
    <!-- ================= HEADER ================= -->
    <header class="page-header">
      <button
        type="button"
        class="back-button"
        aria-label="Retour"
        @click="goBack"
      >
        <svg viewBox="0 0 24 24">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>

      <h1>Devenir Conducteur</h1>

      <span class="step-badge">
        ÉTAPE 2 SUR 3
      </span>
    </header>

    <!-- ================= PROGRESS ================= -->
    <div class="progress-wrapper">
      <div class="progress-track">
        <div class="progress-value"></div>
      </div>
    </div>

    <!-- ================= CONTENT ================= -->
    <main class="content">

      <section class="intro">
        <h2>Informations du véhicule</h2>

        <p>
          Parlez-nous de la voiture que vous utiliserez pour
          vos trajets.
        </p>
      </section>

      <form @submit.prevent="handleSubmit">

        <!-- ================= PHOTO VEHICULE ================= -->
        <div class="form-group vehicle-photo-group">
          <label>PHOTO DU VÉHICULE</label>

          <button
  type="button"
  class="vehicle-photo"
  :class="{ 'has-photo': photoPreview }"
  @click="triggerPhotoUpload"
>
  <input
    ref="photoInput"
    type="file"
    accept="image/jpeg,image/png,image/webp"
    class="hidden-input"
    @change="handlePhotoChange"
  />

  <!--
    Image par défaut depuis /public/images/
    puis image uploadée lorsqu'elle existe
  -->
  <img
    :src="photoPreview || defaultVehicleImage"
    :alt="photoPreview ? 'Photo du véhicule sélectionnée' : 'Exemple de véhicule'"
    class="vehicle-image"
  />

  <!-- Voile uniquement lorsque aucune photo personnelle n'est uploadée -->
  <div
    v-if="!photoPreview"
    class="photo-overlay"
  ></div>

  <!-- Action -->
  <div class="photo-action">
    <div class="search-icon">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle
          cx="11"
          cy="11"
          r="6.5"
        />
        <path d="m16 16 4 4" />
      </svg>
    </div>

    <span>
      {{
        photoPreview
          ? 'Modifier la photo'
          : 'Cliquez pour ajouter une photo'
      }}
    </span>
  </div>
</button>
        </div>

        <!-- ================= MARQUE / MODELE ================= -->
        <div class="form-row">

          <div class="form-group">
            <label for="brand">MARQUE</label>

            <input
              id="brand"
              v-model="form.brand"
              type="text"
              placeholder="Marque"
            />
          </div>

          <div class="form-group">
            <label for="model">MODÈLE</label>

            <input
              id="model"
              v-model="form.model"
              type="text"
              placeholder="Modèle"
            />
          </div>

        </div>

        <!-- ================= PLAQUE ================= -->
        <div class="form-group">
          <label for="plate">
            NUMÉRO DE PLAQUE
          </label>

          <div class="plate-field">
            <input
              id="plate"
              v-model="form.plate"
              type="text"
              placeholder="AB-123-CD"
              maxlength="12"
              @input="formatPlate"
            />

            <span class="plate-country">
              FR
            </span>
          </div>
        </div>

        <!-- ================= COULEUR / SIEGES ================= -->
        <div class="form-row">

          <div class="form-group">
            <label>COULEUR</label>

            <button
              type="button"
              class="select-field"
              @click="toggleColor"
            >
              <span class="color-circle"></span>

              <span class="select-value">
                {{ form.color }}
              </span>
            </button>

            <div
              v-if="showColorOptions"
              class="color-options"
            >
              <button
                type="button"
                @click="selectColor('Blanc Nacré')"
              >
                <span class="color-circle white"></span>
                Blanc Nacré
              </button>

              <button
                type="button"
                @click="selectColor('Noir')"
              >
                <span class="color-circle black"></span>
                Noir
              </button>

              <button
                type="button"
                @click="selectColor('Gris')"
              >
                <span class="color-circle gray"></span>
                Gris
              </button>
            </div>
          </div>

          <div class="form-group">
            <label for="seats">SIÈGES</label>

            <div class="input-with-seat-icon">
              <input
                id="seats"
                v-model="form.seats"
                type="number"
                min="1"
                max="9"
              />

              <svg viewBox="0 0 24 24">
                <path
                  d="M5 17v-4.5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2V17"
                />
                <path d="M4 17h16v3H4z" />
                <path d="M7 10V7a2 2 0 0 1 2-2h2v5" />
              </svg>
            </div>
          </div>

        </div>

        <!-- ================= SECURITY CARD ================= -->
        <section class="security-card">

          <div class="security-icon">
            <svg viewBox="0 0 24 24">
              <path
                d="M12 3 5 6v5c0 4.5 2.9 8.3 7 10 4.1-1.7 7-5.5 7-10V6l-7-3Z"
              />
              <path d="M12 7v9" />
            </svg>
          </div>

          <div class="security-content">
            <h3>
              Vérification de sécurité
            </h3>

            <p>
              Les informations de votre véhicule sont
              nécessaires pour garantir un trajet
              sécurisé à nos passagers.
            </p>
          </div>

        </section>

        <!-- ================= SUBMIT ================= -->
        <div class="submit-wrapper">
          <button
            type="submit"
            class="continue-button"
            :disabled="!canContinue"
          >
            <span>Continuer</span>

            <svg viewBox="0 0 24 24">
              <path d="M5 12h13" />
              <path d="m13 6 6 6-6 6" />
            </svg>
          </button>
        </div>

      </form>
    </main>
  </div>
</template>

<script setup>
import {
  computed,
  ref,
  onBeforeUnmount,
  onMounted,
  watch
} from 'vue'
import { useRouter } from 'vue-router'

const STORAGE_KEY = 'letsgo_onboarding_vehicule'
const router = useRouter()

const emit = defineEmits([
  'back',
  'continue'
])

const photoInput = ref(null)
const photoPreview = ref(null)
const photoFile = ref(null)
const defaultVehicleImage = '/images/image_voiture.jpg'

const showColorOptions = ref(false)

const form = ref({
  brand: '',
  model: '',
  plate: '',
  color: 'Blanc Nacré',
  seats: ''
})

const persistState = () => {
  const payload = {
    form: form.value,
    photoDataUrl: photoPreview.value || null
  }

  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
}

const hydrateState = () => {
  try {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '{}')

    if (saved.form) {
      form.value = { ...form.value, ...saved.form }
    }

    if (saved.photoDataUrl) {
      photoPreview.value = saved.photoDataUrl
      photoFile.value = { name: 'photo_vehicule', type: 'image/jpeg' }
    }
  } catch (error) {
    console.warn('Erreur lecture état véhicule:', error)
  }
}

const canContinue = computed(() => {
  const seatsValue = Number(form.value.seats)
  const hasPhoto = !!photoFile.value || !!photoPreview.value

  return (
    hasPhoto &&
    form.value.brand.trim() &&
    form.value.model.trim() &&
    form.value.plate.trim().length >= 5 &&
    form.value.color &&
    Number.isFinite(seatsValue) &&
    seatsValue >= 1
  )
})

/*
 * Navigation
 */
const goBack = () => {
  emit('back')
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/conducteur/infos-personnelles')
  }
}

/*
 * Photo
 */
const triggerPhotoUpload = () => {
  photoInput.value?.click()
}

const handlePhotoChange = (event) => {
  const file = event.target.files?.[0]

  if (!file) return

  if (photoPreview.value && photoPreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(photoPreview.value)
  }

  photoFile.value = file

  const reader = new FileReader()
  reader.onload = () => {
    photoPreview.value = String(reader.result)
    persistState()
  }
  reader.readAsDataURL(file)
}

/*
 * Plaque
 */
const formatPlate = (event) => {
  let value = event.target.value
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, '')

  value = value.slice(0, 8)

  if (value.length > 5) {
    value =
      value.slice(0, 2) +
      '-' +
      value.slice(2, 5) +
      '-' +
      value.slice(5)
  } else if (value.length > 2) {
    value =
      value.slice(0, 2) +
      '-' +
      value.slice(2)
  }

  form.value.plate = value
}

/*
 * Couleur
 */
const toggleColor = () => {
  showColorOptions.value =
    !showColorOptions.value
}

const selectColor = (color) => {
  form.value.color = color
  showColorOptions.value = false
}

/*
 * Submit
 */
const handleSubmit = () => {
  if (!canContinue.value) return

  persistState()

  emit('continue', {
    ...form.value,
    photo: photoFile.value || null
  })

  router.push('/conducteur/documents')
}

onMounted(() => {
  hydrateState()
})

watch(
  form,
  () => {
    persistState()
  },
  { deep: true }
)

watch(photoPreview, () => {
  persistState()
})

onBeforeUnmount(() => {
  if (photoPreview.value && photoPreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(photoPreview.value)
  }
})
</script>

<style scoped>
/* =========================================================
   TOKENS
   ========================================================= */

.driver-registration {
  --brand: #ff4d2d;
  --brand-dark: #ed4327;

  --black: #111627;
  --dark-gray: #374151;

  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  min-height: 100vh;

  background: #fff;
  color: var(--black);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  box-sizing: border-box;
}

.driver-registration *,
.driver-registration *::before,
.driver-registration *::after {
  box-sizing: border-box;
}

/* =========================================================
   HEADER
   ========================================================= */

.page-header {
  height: 68px;

  display: flex;
  align-items: center;

  padding: 0 21px;

  gap: 12px;
}

.back-button {
  width: 18px;
  height: 30px;

  padding: 0;

  border: 0;
  background: transparent;

  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;
}

.back-button svg {
  width: 19px;
  height: 19px;

  fill: none;
  stroke: #9298a1;
  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.page-header h1 {
  margin: 0;

  font-size: 15px;
  line-height: 20px;
  font-weight: 700;

  white-space: nowrap;
}

.step-badge {
  margin-left: auto;

  padding: 7px 10px;

  border-radius: 999px;

  background: #f1f2f4;
  color: #777d85;

  font-size: 10px;
  line-height: 12px;
  font-weight: 700;

  white-space: nowrap;
}

/* =========================================================
   PROGRESS
   ========================================================= */

.progress-wrapper {
  padding: 0 21px;
}

.progress-track {
  width: 100%;
  height: 5px;

  overflow: hidden;

  background: #e5e7eb;

  border-radius: 999px;
}

.progress-value {
  width: 50%;
  height: 100%;

  background: var(--brand);

  border-radius: 999px;
}

/* =========================================================
   CONTENT
   ========================================================= */

.content {
  padding: 38px 21px 25px;
}

.intro {
  margin-bottom: 33px;
}

.intro h2 {
  margin: 0 0 6px;

  font-size: 20px;
  line-height: 28px;

  font-weight: 700;
  letter-spacing: -0.4px;
}

.intro p {
  max-width: 320px;

  margin: 0;

  color: #92969d;

  font-size: 13px;
  line-height: 18px;
}

/* =========================================================
   FORM
   ========================================================= */

form {
  display: flex;
  flex-direction: column;

  gap: 23px;
}

.form-group {
  position: relative;

  display: flex;
  flex-direction: column;

  gap: 9px;
}

.form-group > label {
  padding-left: 3px;

  color: #7c828a;

  font-size: 10px;
  line-height: 14px;

  font-weight: 700;

  letter-spacing: 0.7px;
}

.form-group input {
  width: 100%;
  height: 50px;

  padding: 0 14px;

  border: 1px solid transparent;
  border-radius: 14px;

  outline: none;

  background: #f2f3f5;

  color: var(--black);

  font-family: inherit;

  font-size: 14px;
  font-weight: 500;

  transition: 0.2s ease;
}

.form-group input:focus {
  border-color: rgba(255, 77, 45, 0.3);
}

.form-group input::placeholder {
  color: #a1a5ac;
}

/* =========================================================
   ROW
   ========================================================= */

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 14px;
}

/* =========================================================
   VEHICLE PHOTO
   ========================================================= */

.vehicle-photo-group {
  gap: 10px;
}

.vehicle-photo {
  position: relative;

  width: 100%;
  height: 166px;

  padding: 0;

  overflow: hidden;

  border: 0;
  border-radius: 18px;

  background: #e9eaec;

  cursor: pointer;

  font-family: inherit;
}
.vehicle-photo {
  position: relative;

  width: 100%;
  height: 166px;

  padding: 0;

  overflow: hidden;

  border: 0;
  border-radius: 18px;

  background: #e9eaec;

  cursor: pointer;

  font-family: inherit;

  isolation: isolate;
}

.vehicle-image {
  position: absolute;
  inset: 0;

  width: 100%;
  height: 100%;

  display: block;

  object-fit: cover;

  /*
   * L'image de démonstration est volontairement
   * très claire pour se rapprocher de la maquette.
   */
  opacity: 0.34;

  filter: saturate(0.35);

  transition:
    opacity 0.25s ease,
    filter 0.25s ease,
    transform 0.25s ease;

  z-index: 1;
}

/* Lorsqu'une vraie photo est sélectionnée */
.vehicle-photo.has-photo .vehicle-image {
  opacity: 1;
  filter: none;

  transform: scale(1.01);
}

.photo-overlay {
  position: absolute;
  inset: 0;

  background:
    linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.20),
      rgba(255, 255, 255, 0.58)
    );

  z-index: 2;

  pointer-events: none;
}

.photo-action {
  position: absolute;
  inset: 0;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 11px;

  color: #374151;

  font-size: 12px;
  font-weight: 600;

  z-index: 3;

  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.vehicle-photo.has-photo .photo-action {
  opacity: 0;
  pointer-events: none;
}

.search-icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #ffffff;

  box-shadow:
    0 4px 12px rgba(17, 22, 39, 0.12);
}

.search-icon svg {
  width: 23px;
  height: 23px;

  fill: none;

  stroke: #111627;
  stroke-width: 2.2;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.hidden-input {
  display: none;
}

.vehicle-image {
  position: absolute;
  inset: 0;

  width: 100%;
  height: 100%;

  display: block;
  object-fit: cover;
  opacity: 1;
  border-radius: 18px;
}

.vehicle-photo.has-photo .vehicle-image {
  opacity: 1;
}

.photo-overlay {
  position: absolute;
  inset: 0;

  background: rgba(244, 245, 246, 0.42);
  opacity: 1;
  transition: opacity 0.2s ease;
}

.vehicle-photo.has-photo .photo-overlay {
  opacity: 0;
}

.photo-action {
  position: absolute;
  inset: 0;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 11px;

  color: #374151;

  font-size: 12px;
  font-weight: 600;
  transition: opacity 0.2s ease;
}

.vehicle-photo.has-photo .photo-action {
  opacity: 0;
  pointer-events: none;
}

.search-icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: white;

  box-shadow:
    0 2px 5px rgba(17, 22, 39, 0.08);
}

.search-icon svg {
  width: 23px;
  height: 23px;

  fill: none;
  stroke: #111627;
  stroke-width: 2.2;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.hidden-input {
  display: none;
}

/* =========================================================
   PLAQUE
   ========================================================= */

.plate-field {
  position: relative;
}

.plate-field input {
  padding-right: 55px;
}

.plate-country {
  position: absolute;

  right: 8px;
  top: 50%;

  transform: translateY(-50%);

  min-width: 28px;
  height: 25px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 5px;

  background: #fff;

  color: #858a92;

  font-size: 9px;
  font-weight: 600;
}

/* =========================================================
   COLOR
   ========================================================= */

.select-field {
  width: 100%;
  height: 50px;

  display: flex;
  align-items: center;

  gap: 10px;

  padding: 0 14px;

  border: 0;
  border-radius: 14px;

  background: #f2f3f5;

  color: var(--black);

  font-family: inherit;

  font-size: 12px;
  font-weight: 500;

  cursor: pointer;

  text-align: left;
}

.color-circle {
  width: 14px;
  height: 14px;

  flex-shrink: 0;

  border-radius: 50%;

  background: white;

  border: 1px solid #e0e1e3;
}

.color-circle.black {
  background: #111627;
  border-color: #111627;
}

.color-circle.gray {
  background: #9ca3af;
  border-color: #9ca3af;
}

.color-options {
  position: absolute;

  z-index: 10;

  top: 77px;
  left: 0;
  right: 0;

  padding: 7px;

  border-radius: 12px;

  background: white;

  box-shadow:
    0 8px 24px rgba(17, 22, 39, 0.12);
}

.color-options button {
  width: 100%;

  display: flex;
  align-items: center;

  gap: 9px;

  padding: 9px;

  border: 0;
  border-radius: 8px;

  background: transparent;

  font-family: inherit;
  font-size: 11px;

  text-align: left;

  cursor: pointer;
}

.color-options button:hover {
  background: #f3f4f6;
}

/* =========================================================
   SEATS
   ========================================================= */

.input-with-seat-icon {
  position: relative;
}

.input-with-seat-icon input {
  padding-right: 40px;
}

.input-with-seat-icon svg {
  position: absolute;

  right: 12px;
  top: 50%;

  width: 16px;
  height: 16px;

  transform: translateY(-50%);

  fill: #111627;
  stroke: #111627;
  stroke-width: 1.2;

  pointer-events: none;
}

/* =========================================================
   SECURITY CARD
   ========================================================= */

.security-card {
  min-height: 109px;

  display: flex;

  gap: 13px;

  padding: 17px 16px;

  border-radius: 19px;

  background: #fff7ed;
}

.security-icon {
  width: 35px;
  height: 35px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 11px;

  background: #ffe7d9;
}

.security-icon svg {
  width: 19px;
  height: 19px;

  fill: none;

  stroke: #111627;
  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.security-content h3 {
  margin: 0 0 5px;

  color: #111627;

  font-size: 12px;
  line-height: 17px;

  font-weight: 700;
}

.security-content p {
  max-width: 240px;

  margin: 0;

  color: #96918c;

  font-size: 10px;
  line-height: 17px;
}

/* =========================================================
   SUBMIT
   ========================================================= */

.submit-wrapper {
  margin-top: 55px;

  padding-top: 20px;

  border-top: 1px solid #f0f0f1;
}

.continue-button {
  width: 100%;
  height: 49px;

  display: flex;
  align-items: center;
  justify-content: center;

  gap: 9px;

  border: 0;
  border-radius: 14px;

  background: var(--brand);

  color: white;

  font-family: inherit;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;

  box-shadow:
    0 5px 12px rgba(255, 77, 45, 0.16);

  transition: 0.2s ease;
}

.continue-button svg {
  width: 17px;
  height: 17px;

  fill: none;

  stroke: currentColor;
  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.continue-button:hover:not(:disabled) {
  background: var(--brand-dark);
}

.continue-button:active:not(:disabled) {
  transform: scale(0.99);
}

.continue-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (min-width: 600px) {
  .driver-registration {
    max-width: 430px;

    margin: auto;

    border-left: 1px solid #f2f2f2;
    border-right: 1px solid #f2f2f2;
  }

  .page-header,
  .progress-wrapper {
    padding-left: 28px;
    padding-right: 28px;
  }

  .content {
    padding-left: 28px;
    padding-right: 28px;
  }
}

@media (max-width: 350px) {
  .page-header {
    padding-left: 16px;
    padding-right: 16px;
  }

  .content {
    padding-left: 16px;
    padding-right: 16px;
  }

  .form-row {
    gap: 8px;
  }
}
</style>
