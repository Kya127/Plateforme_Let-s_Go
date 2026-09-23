<template>
  <main class="register-page">
    <section class="register-card" aria-labelledby="register-title">
      <!-- Header -->
      <header class="register-header">
        <button
          type="button"
          class="back-button"
          aria-label="Retour"
          @click="goBack"
        >
          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              d="M15 18L9 12L15 6"
              fill="none"
              stroke="currentColor"
              stroke-width="2.4"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>

        <h1 id="register-title">
          Inscription
        </h1>
      </header>

      <!-- Intro -->
      <div class="register-intro">
        <p>
          Rejoignez la communauté Let's Go dès
          aujourd'hui.
        </p>
      </div>

      <!-- Form -->
      <form
        class="register-form"
        novalidate
        @submit.prevent="handleSubmit"
      >
        <!-- Prénom / Nom -->
        <div class="name-grid">
          <div class="field">
            <label for="firstName">
              Prénom
            </label>

            <input
              id="firstName"
              v-model.trim="form.firstName"
              name="firstName"
              type="text"
              autocomplete="given-name"
              placeholder="Ex. Fatou"
              maxlength="50"
              required
              :aria-invalid="!!errors.firstName"
              @blur="validateField('firstName')"
            />

            <span
              v-if="errors.firstName"
              class="field-error"
            >
              {{ errors.firstName }}
            </span>
          </div>

          <div class="field">
            <label for="lastName">
              Nom
            </label>

            <input
              id="lastName"
              v-model.trim="form.lastName"
              name="lastName"
              type="text"
              autocomplete="family-name"
              placeholder="Ex. Ndiaye"
              maxlength="50"
              required
              :aria-invalid="!!errors.lastName"
              @blur="validateField('lastName')"
            />

            <span
              v-if="errors.lastName"
              class="field-error"
            >
              {{ errors.lastName }}
            </span>
          </div>
        </div>

        <!-- Téléphone -->
        <div class="field">
          <label for="phone">
            Téléphone
          </label>

          <div
            class="input-wrapper"
            :class="{ 'has-error': errors.phone }"
          >
            <span class="country-code">
              +221
            </span>

            <span class="phone-divider" aria-hidden="true"></span>

            <input
              id="phone"
              v-model="form.phone"
              name="phone"
              type="tel"
              inputmode="numeric"
              autocomplete="tel"
              placeholder="77 123 45 67"
              maxlength="11"
              required
              :aria-invalid="!!errors.phone"
              @input="formatPhone"
              @blur="validateField('phone')"
            />
          </div>

          <span
            v-if="errors.phone"
            class="field-error"
          >
            {{ errors.phone }}
          </span>
        </div>

        <!-- Email -->
        <div class="field">
          <label for="email">
            Adresse e-mail
          </label>

          <input
            id="email"
            v-model.trim="form.email"
            name="email"
            type="email"
            autocomplete="email"
            placeholder="fatou.ndiaye@exemple.sn"
            required
            :aria-invalid="!!errors.email"
            @blur="validateField('email')"
          />

          <span
            v-if="errors.email"
            class="field-error"
          >
            {{ errors.email }}
          </span>
        </div>

        <!-- Mot de passe -->
        <div class="field">
          <label for="password">
            Mot de passe
          </label>

          <div
            class="password-wrapper"
            :class="{ 'has-error': errors.password }"
          >
            <input
              id="password"
              v-model="form.password"
              name="password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="8 caractères minimum"
              minlength="8"
              required
              :aria-invalid="!!errors.password"
              @blur="validateField('password')"
            />

            <button
              type="button"
              class="password-toggle"
              :aria-label="
                showPassword
                  ? 'Masquer le mot de passe'
                  : 'Afficher le mot de passe'
              "
              @click="showPassword = !showPassword"
            >
              <svg
                v-if="!showPassword"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M2.5 12s3.5-5.5 9.5-5.5S21.5 12 21.5 12s-3.5 5.5-9.5 5.5S2.5 12 2.5 12Z"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <circle
                  cx="12"
                  cy="12"
                  r="2.8"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
              </svg>

              <svg
                v-else
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M3 3L21 21"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                />
                <path
                  d="M10.6 6.6A10.8 10.8 0 0 1 12 6.5c6 0 9.5 5.5 9.5 5.5a17.2 17.2 0 0 1-3.2 3.6M6.7 6.9C4 8.5 2.5 12 2.5 12s3.5 5.5 9.5 5.5c1.4 0 2.7-.3 3.8-.8"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                />
              </svg>
            </button>
          </div>

          <span
            v-if="errors.password"
            class="field-error"
          >
            {{ errors.password }}
          </span>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="submit-button"
          :disabled="isSubmitting"
        >
          <span v-if="!isSubmitting">
            S'inscrire
          </span>

          <span
            v-else
            class="loading-content"
          >
            <span class="spinner"></span>
            Création du compte...
          </span>
        </button>

        <!-- Legal -->
        <p class="legal-text">
          En vous inscrivant, vous acceptez nos
          <a href="#">
            Conditions d'utilisation
          </a>
          et notre
          <a href="#">
            Politique de confidentialité
          </a>.
        </p>
      </form>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'

const router = useRouter()
const authStore = useAuthentificationStore()

const emit = defineEmits([
  'back',
  'submit'
])

const showPassword = ref(false)
const isSubmitting = ref(false)

const form = reactive({
  firstName: '',
  lastName: '',
  phone: '',
  email: '',
  password: ''
})

const errors = reactive({
  firstName: '',
  lastName: '',
  phone: '',
  email: '',
  password: ''
})

const formatPhone = () => {
  const digits = form.phone.replace(/\D/g, '').slice(0, 9)
  const groups = []

  if (digits.length > 0) groups.push(digits.slice(0, 2))
  if (digits.length > 2) groups.push(digits.slice(2, 5))
  if (digits.length > 5) groups.push(digits.slice(5, 7))
  if (digits.length > 7) groups.push(digits.slice(7, 9))

  form.phone = groups.join(' ')
}

const validateField = (field) => {
  errors[field] = ''

  if (field === 'firstName' && !form.firstName) {
    errors.firstName = 'Veuillez renseigner votre prénom.'
  }

  if (field === 'lastName' && !form.lastName) {
    errors.lastName = 'Veuillez renseigner votre nom.'
  }

  if (field === 'phone') {
    const phone = form.phone.replace(/\D/g, '')

    if (!phone) {
      errors.phone = 'Veuillez renseigner votre numéro.'
    } else if (phone.length !== 9) {
      errors.phone = 'Entrez un numéro sénégalais à 9 chiffres.'
    }
  }

  if (field === 'email') {
    if (!form.email) {
      errors.email = 'Veuillez renseigner votre adresse e-mail.'
    } else if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)
    ) {
      errors.email = 'Veuillez saisir une adresse e-mail valide.'
    }
  }

  if (field === 'password') {
    if (!form.password) {
      errors.password = 'Veuillez choisir un mot de passe.'
    } else if (form.password.length < 8) {
      errors.password = 'Le mot de passe doit contenir au moins 8 caractères.'
    }
  }
}

const validateForm = () => {
  Object.keys(errors).forEach((field) => {
    validateField(field)
  })

  return !Object.values(errors).some(Boolean)
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isSubmitting.value = true

  try {
    /*
     * Exemple pour ton backend Django / DRF :
     *
     * await authService.register({
     *   first_name: form.firstName,
     *   last_name: form.lastName,
     *   phone: `+221${form.phone.replace(/\s/g, '')}`,
     *   email: form.email,
     *   password: form.password
     * })
     *
     * emit('submit', response)
     */

    emit('submit', {
      firstName: form.firstName,
      lastName: form.lastName,
      phone: `+221${form.phone.replace(/\s/g, '')}`,
      email: form.email,
      password: form.password
    })

    authStore.connecter(form.email, { role: 'conducteur' })
    router.push('/conducteur/infos-personnelles')
  } finally {
    isSubmitting.value = false
  }
}

const goBack = () => {
  emit('back')
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/connexion')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: #f3f4f6;
}

.register-page {
  min-height: 100vh;
  min-height: 100svh;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;

  background:
    radial-gradient(
      circle at top,
      rgba(255, 77, 45, 0.04),
      transparent 35%
    ),
    #f3f4f6;
}

/* =====================================================
   CARD
===================================================== */

.register-card {
  width: min(100%, 680px);

  background: #ffffff;

  border-radius: 48px;

  padding: 64px 66px 62px;

  box-shadow:
    0 24px 70px rgba(17, 22, 39, 0.10);

  border: 1px solid rgba(17, 22, 39, 0.03);
}

/* =====================================================
   HEADER
===================================================== */

.register-header {
  display: flex;
  align-items: center;
  gap: 28px;
}

.register-header h1 {
  margin: 0;

  color: #111627;

  font-size: clamp(38px, 6vw, 52px);
  font-weight: 800;
  line-height: 1.1;

  letter-spacing: -1.6px;
}

.back-button {
  flex: 0 0 auto;

  width: 80px;
  height: 80px;

  border: 0;
  border-radius: 24px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #111627;
  background: #f3f4f6;

  cursor: pointer;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.back-button:hover {
  background: #e9eaed;
  transform: translateX(-2px);
}

.back-button:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.28);
  outline-offset: 3px;
}

.back-button svg {
  width: 34px;
  height: 34px;
}

/* =====================================================
   INTRO
===================================================== */

.register-intro {
  margin-top: 48px;
}

.register-intro p {
  margin: 0;

  max-width: 570px;

  color: #374151;

  font-size: 25px;
  line-height: 1.55;
  font-weight: 400;

  letter-spacing: -0.4px;
}

/* =====================================================
   FORM
===================================================== */

.register-form {
  margin-top: 48px;
}

.name-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.field {
  margin-bottom: 31px;
}

.field label {
  display: block;

  margin: 0 0 11px 8px;

  color: #6b7280;

  font-size: 17px;
  line-height: 1.2;
  font-weight: 700;

  text-transform: uppercase;

  letter-spacing: 0.1px;
}

.field input {
  width: 100%;
  height: 76px;

  padding: 0 24px;

  border: 2px solid transparent;
  border-radius: 24px;

  background: #f3f4f6;

  color: #111627;

  font-family: inherit;
  font-size: 20px;
  font-weight: 500;

  outline: none;

  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.field input::placeholder {
  color: #9ca3af;
  opacity: 1;
}

.field input:hover {
  background: #eef0f3;
}

.field input:focus {
  background: #ffffff;

  border-color: #ff4d2d;

  box-shadow:
    0 0 0 4px rgba(255, 77, 45, 0.10);
}

.field input[aria-invalid='true'] {
  border-color: #ffb4a7;
  background: #fff8f6;
}

.field input[aria-invalid='true']:focus {
  border-color: #ff4d2d;

  box-shadow:
    0 0 0 4px rgba(255, 77, 45, 0.10);
}

/* =====================================================
   PHONE
===================================================== */

.input-wrapper {
  height: 76px;

  display: flex;
  align-items: center;

  padding: 0 22px;

  background: #f3f4f6;

  border: 2px solid transparent;
  border-radius: 24px;

  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.input-wrapper:focus-within {
  background: #ffffff;
  border-color: #ff4d2d;

  box-shadow:
    0 0 0 4px rgba(255, 77, 45, 0.10);
}

.input-wrapper.has-error {
  border-color: #ffb4a7;
  background: #fff8f6;
}

.country-code {
  color: #111627;

  font-size: 18px;
  font-weight: 700;

  white-space: nowrap;
}

.phone-divider {
  width: 1px;
  height: 30px;

  margin: 0 16px;

  background: #d1d5db;
}

.input-wrapper input {
  height: 100%;

  padding: 0;

  border: 0;
  background: transparent;

  box-shadow: none;
}

.input-wrapper input:hover,
.input-wrapper input:focus {
  background: transparent;
  border: 0;
  box-shadow: none;
}

/* =====================================================
   PASSWORD
===================================================== */

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-right: 68px;
}

.password-toggle {
  position: absolute;
  top: 50%;
  right: 18px;

  width: 42px;
  height: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  transform: translateY(-50%);

  border: 0;
  border-radius: 12px;

  background: transparent;

  color: #9ca3af;

  cursor: pointer;

  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.password-toggle:hover {
  color: #111627;
  background: #e9eaed;
}

.password-toggle:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.20);
}

.password-toggle svg {
  width: 22px;
  height: 22px;
}

/* =====================================================
   ERROR
===================================================== */

.field-error {
  display: block;

  margin: 8px 8px 0;

  color: #dc2626;

  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
}

/* =====================================================
   SUBMIT
===================================================== */

.submit-button {
  width: 100%;
  height: 82px;

  margin-top: 32px;

  border: 0;
  border-radius: 26px;

  background: #111627;
  color: #ffffff;

  font-family: inherit;
  font-size: 25px;
  font-weight: 700;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  background: #1a2132;

  transform: translateY(-1px);

  box-shadow:
    0 12px 26px rgba(17, 22, 39, 0.15);
}

.submit-button:active:not(:disabled) {
  transform: translateY(0);
}

.submit-button:focus-visible {
  outline: 4px solid rgba(17, 22, 39, 0.14);
  outline-offset: 3px;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* =====================================================
   LOADING
===================================================== */

.loading-content {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.spinner {
  width: 20px;
  height: 20px;

  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;

  border-radius: 50%;

  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* =====================================================
   LEGAL
===================================================== */

.legal-text {
  max-width: 540px;

  margin: 30px auto 0;

  color: #9ca3af;

  font-size: 15px;
  line-height: 1.65;
  font-weight: 400;

  text-align: center;
}

.legal-text a {
  color: #ff4d2d;

  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

.legal-text a:hover {
  color: #e74325;
}

/* =====================================================
   RESPONSIVE
===================================================== */

@media (max-width: 700px) {
  .register-page {
    padding: 12px;
    align-items: flex-start;
  }

  .register-card {
    min-height: calc(100vh - 24px);

    border-radius: 34px;

    padding: 34px 24px 34px;
  }

  .register-header {
    gap: 18px;
  }

  .back-button {
    width: 58px;
    height: 58px;

    border-radius: 18px;
  }

  .back-button svg {
    width: 28px;
    height: 28px;
  }

  .register-header h1 {
    font-size: 34px;
    letter-spacing: -1px;
  }

  .register-intro {
    margin-top: 34px;
  }

  .register-intro p {
    font-size: 20px;
    line-height: 1.5;
  }

  .register-form {
    margin-top: 36px;
  }

  .name-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .field {
    margin-bottom: 24px;
  }

  .field label {
    margin-bottom: 9px;
    font-size: 14px;
  }

  .field input,
  .input-wrapper {
    height: 64px;
    border-radius: 20px;
  }

  .field input {
    font-size: 17px;
    padding: 0 20px;
  }

  .country-code {
    font-size: 16px;
  }

  .phone-divider {
    margin: 0 12px;
  }

  .submit-button {
    height: 70px;

    margin-top: 24px;

    border-radius: 21px;

    font-size: 20px;
  }

  .legal-text {
    margin-top: 24px;

    font-size: 13px;
  }
}
</style>