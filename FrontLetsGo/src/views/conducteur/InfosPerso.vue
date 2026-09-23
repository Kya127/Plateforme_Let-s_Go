<template>
  <div class="driver-registration">
    <!-- Header -->
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

      <span class="step-badge">ÉTAPE 1 SUR 3</span>
    </header>

    <!-- Progress -->
    <div class="progress-wrapper">
      <div class="progress-track">
        <div class="progress-value"></div>
      </div>
    </div>

    <!-- Content -->
    <main class="content">
      <section class="intro">
        <h2>Informations personnelles</h2>
        <p>
          Certaines de ces informations seront visibles par
          tous les passagers.
        </p>
      </section>

      <form @submit.prevent="handleSubmit">
        <!-- Photo -->
        <div class="form-group photo-group">
          <label>PHOTO</label>

          <button
            type="button"
            class="photo-upload"
            @click="triggerPhotoUpload"
          >
            <input
              ref="photoInput"
              type="file"
              accept="image/*"
              class="hidden-input"
              @change="handlePhotoChange"
            />

            <div
              class="photo-preview"
              :class="{ 'has-photo': photoPreview }"
            >
              <img
                v-if="photoPreview"
                :src="photoPreview"
                alt="Photo de profil"
              />

              <svg
                v-else
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21c0-4.2 3.2-7 8-7s8 2.8 8 7" />
              </svg>
            </div>

            <span v-if="!photoPreview">
              Cliquez pour ajouter votre photo
            </span>

            <span v-else>
              Modifier votre photo
            </span>
          </button>
        </div>

        <!-- Prénom / Nom -->
        <div class="form-row">
          <div class="form-group">
            <label for="firstName">PRENOM</label>

            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              placeholder="Prénom"
              autocomplete="given-name"
            />
          </div>

          <div class="form-group">
            <label for="lastName">NOM</label>

            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              placeholder="Nom"
              autocomplete="family-name"
            />
          </div>
        </div>

        <!-- Téléphone -->
        <div class="form-group">
          <label for="phone">NUMÉRO DE TELEPHONE</label>

          <div class="phone-field">
            <div class="country-code">
              +221
            </div>

            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              inputmode="numeric"
              placeholder="77 700 00 00"
              autocomplete="tel"
              maxlength="12"
              @input="formatPhone"
            />
          </div>
        </div>

        <!-- Date de naissance -->
        <div class="form-group">
          <label for="birthDate">DATE DE NAISSANCE</label>

          <div class="input-with-icon">
            <input
              id="birthDate"
              v-model="form.birthDate"
              type="text"
              placeholder="JJ / MM / AAAA"
              maxlength="14"
              @input="formatBirthDate"
            />

            <svg viewBox="0 0 24 24" aria-hidden="true">
              <rect
                x="4"
                y="5"
                width="16"
                height="15"
                rx="2"
              />
              <path d="M8 3v4M16 3v4M4 10h16" />
            </svg>
          </div>
        </div>

        <!-- Adresse -->
        <div class="form-group">
          <label for="address">ADRESSE DE RESIDENCE</label>

          <div class="input-with-icon">
            <input
              id="address"
              v-model="form.address"
              type="text"
              placeholder="Ex: 15 Rue Dakar Mermoz"
              autocomplete="street-address"
            />

            <svg viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="10.5" cy="10.5" r="5.5" />
              <path d="M15 15l5 5" />
            </svg>
          </div>
        </div>

        <!-- Submit -->
        <div class="submit-wrapper">
          <button
            type="submit"
            class="continue-button"
            :disabled="!canContinue"
          >
            <span>Continuer</span>

            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M5 12h13M13 6l6 6-6 6" />
            </svg>
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import { computed, ref, onBeforeUnmount, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const STORAGE_KEY = 'letsgo_onboarding_infos_perso'
const router = useRouter()

const emit = defineEmits(['back', 'continue'])

const photoInput = ref(null)
const photoPreview = ref(null)
const photoFile = ref(null)

const form = ref({
  firstName: '',
  lastName: '',
  phone: '',
  birthDate: '',
  address: ''
})

const persistState = () => {
  sessionStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      form: form.value,
      photoDataUrl: photoPreview.value || null
    })
  )
}

const hydrateState = () => {
  try {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '{}')

    if (saved.form) {
      form.value = { ...form.value, ...saved.form }
    }

    if (saved.photoDataUrl) {
      photoPreview.value = saved.photoDataUrl
      photoFile.value = { name: 'photo_profil', type: 'image/jpeg' }
    }
  } catch (error) {
    console.warn('Erreur lecture état infos perso:', error)
  }
}

const isValidBirthDate = (dateValue) => {
  if (!dateValue || typeof dateValue !== 'string') return false

  const digits = dateValue.replace(/\D/g, '')
  if (digits.length !== 8) return false

  const day = Number(digits.slice(0, 2))
  const month = Number(digits.slice(2, 4))
  const year = Number(digits.slice(4, 8))

  if (!day || !month || !year) return false
  if (month < 1 || month > 12) return false

  const date = new Date(year, month - 1, day)
  if (
    date.getFullYear() !== year ||
    date.getMonth() !== month - 1 ||
    date.getDate() !== day
  ) {
    return false
  }

  const today = new Date()
  let age = today.getFullYear() - year
  const hasBirthdayPassedThisYear =
    today.getMonth() > month - 1 ||
    (today.getMonth() === month - 1 && today.getDate() >= day)

  if (!hasBirthdayPassedThisYear) {
    age -= 1
  }

  return age >= 18
}

const canContinue = computed(() => {
  const hasPhoto = !!photoFile.value || !!photoPreview.value

  return (
    hasPhoto &&
    form.value.firstName.trim() &&
    form.value.lastName.trim() &&
    form.value.phone.replace(/\s/g, '').length === 9 &&
    isValidBirthDate(form.value.birthDate) &&
    form.value.address.trim()
  )
})

const goBack = () => {
  emit('back')
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/connexion')
  }
}

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

const formatPhone = () => {
  const digits = form.value.phone.replace(/\D/g, '').slice(0, 9)
  const groups = []

  if (digits.length > 0) groups.push(digits.slice(0, 2))
  if (digits.length > 2) groups.push(digits.slice(2, 5))
  if (digits.length > 5) groups.push(digits.slice(5, 7))
  if (digits.length > 7) groups.push(digits.slice(7, 9))

  form.value.phone = groups.join(' ')
}

const formatBirthDate = () => {
  const digits = form.value.birthDate.replace(/\D/g, '').slice(0, 8)
  const formatted = []

  if (digits.length > 0) formatted.push(digits.slice(0, 2))
  if (digits.length > 2) formatted.push(digits.slice(2, 4))
  if (digits.length > 4) formatted.push(digits.slice(4, 8))

  form.value.birthDate = formatted.join(' / ')
}

const handleSubmit = () => {
  if (!canContinue.value) return

  persistState()

  emit('continue', {
    ...form.value,
    photo: photoFile.value || null
  })

  router.push('/conducteur/vehicule')
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
   DESIGN TOKENS
   ========================================================= */

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

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-full: 9999px;

  min-height: 100vh;
  background: var(--white);
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

  padding: 0 20px;

  gap: 12px;
}

.back-button {
  width: 16px;
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
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.page-header h1 {
  margin: 0;

  font-size: 16px;
  line-height: 20px;
  font-weight: 700;

  white-space: nowrap;
}

.step-badge {
  margin-left: auto;

  padding: 7px 11px;

  border-radius: var(--radius-full);

  background: #f0f1f3;
  color: #7d828b;

  font-size: 10px;
  line-height: 12px;
  font-weight: 700;

  white-space: nowrap;
}

/* =========================================================
   PROGRESS
   ========================================================= */

.progress-wrapper {
  padding: 4px 21px 0;
}

.progress-track {
  position: relative;

  width: 100%;
  height: 5px;

  overflow: hidden;

  background: #e4e7eb;
  border-radius: var(--radius-full);
}

.progress-value {
  width: 25%;

  height: 100%;

  background: var(--brand);
  border-radius: var(--radius-full);
}

/* =========================================================
   CONTENT
   ========================================================= */

.content {
  padding: 58px 21px 24px;
}

.intro {
  margin-bottom: 32px;
}

.intro h2 {
  margin: 0 0 6px;

  font-size: 20px;
  line-height: 28px;
  font-weight: 700;
  letter-spacing: -0.4px;
}

.intro p {
  max-width: 330px;

  margin: 0;

  color: #92969d;

  font-size: 13px;
  line-height: 18px;
  font-weight: 400;
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
  display: flex;
  flex-direction: column;

  gap: 9px;
}

.form-group > label {
  padding-left: 3px;

  color: #7e838b;

  font-size: 10px;
  line-height: 14px;
  font-weight: 700;

  letter-spacing: 0.7px;
}

.form-group input {
  width: 100%;
  height: 52px;

  padding: 0 14px;

  border: 1px solid transparent;
  border-radius: 14px;

  outline: none;

  background: #f2f3f5;

  color: var(--black);

  font-family: inherit;
  font-size: 14px;
  font-weight: 500;

  transition:
    border-color 0.2s ease,
    background 0.2s ease;
}

.form-group input::placeholder {
  color: #a2a6ad;
  opacity: 1;
}

.form-group input:focus {
  border-color: rgba(255, 77, 45, 0.35);
  background: #f7f7f8;
}

/* =========================================================
   PHOTO
   ========================================================= */

.photo-group {
  margin-bottom: -1px;
}

.photo-upload {
  width: 100%;
  height: 167px;

  padding: 20px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 13px;

  border: 1.5px dashed #d8dadd;
  border-radius: 19px;

  background: #f5f6f7;

  color: var(--dark-gray);

  font-family: inherit;
  font-size: 12px;
  font-weight: 600;

  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background 0.2s ease;
}

.photo-upload:hover {
  border-color: var(--brand);
  background: #fafafa;
}

.hidden-input {
  display: none !important;
}

.photo-preview {
  width: 68px;
  height: 68px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 3px solid white;
  border-radius: 19px;

  background: #f4f5f6;

  box-shadow:
    0 2px 5px rgba(17, 22, 39, 0.08),
    0 1px 2px rgba(17, 22, 39, 0.05);
}

.photo-preview svg {
  width: 43px;
  height: 43px;

  fill: none;
  stroke: #a1a7b2;
  stroke-width: 1.7;
}

.photo-preview.has-photo {
  overflow: hidden;
  border: 3px solid white;
}

.photo-preview img {
  width: 100%;
  height: 100%;

  object-fit: cover;
}

/* =========================================================
   FIRST NAME / LAST NAME
   ========================================================= */

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 14px;
}

/* =========================================================
   PHONE
   ========================================================= */

.phone-field {
  display: grid;
  grid-template-columns: 64px 1fr;

  gap: 5px;
}

.country-code {
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 14px;

  background: #f2f3f5;

  color: #a2a6ad;

  font-size: 14px;
  font-weight: 500;
}

.phone-field input {
  min-width: 0;
}

/* =========================================================
   INPUT WITH ICON
   ========================================================= */

.input-with-icon {
  position: relative;
}

.input-with-icon input {
  padding-right: 48px;
}

.input-with-icon svg {
  position: absolute;

  top: 50%;
  right: 15px;

  width: 18px;
  height: 18px;

  transform: translateY(-50%);

  fill: none;
  stroke: #9ca3af;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;

  pointer-events: none;
}

/* =========================================================
   SUBMIT
   ========================================================= */

.submit-wrapper {
  margin-top: 31px;

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

  transition:
    background 0.2s ease,
    transform 0.15s ease,
    opacity 0.2s ease;
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
  background: var(--brand-hover);
}

.continue-button:active:not(:disabled) {
  transform: scale(0.99);
}

.continue-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (min-width: 600px) {
  .driver-registration {
    max-width: 430px;
    min-height: 100vh;
    margin: 0 auto;

    border-left: 1px solid #f2f2f2;
    border-right: 1px solid #f2f2f2;
  }

  .content {
    padding-left: 28px;
    padding-right: 28px;
  }

  .page-header {
    padding-left: 28px;
    padding-right: 28px;
  }

  .progress-wrapper {
    padding-left: 28px;
    padding-right: 28px;
  }
}

@media (max-width: 350px) {
  .page-header {
    padding-left: 16px;
    padding-right: 16px;
    gap: 8px;
  }

  .page-header h1 {
    font-size: 14px;
  }

  .step-badge {
    padding: 6px 8px;
    font-size: 9px;
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
