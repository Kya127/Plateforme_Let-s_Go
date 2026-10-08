<template>
  <div class="page-verification">
    <div class="conteneur-verification">

      <!-- =====================================================
           EN-TÊTE DE NAVIGATION (RETOUR & LOGO)
      ====================================================== -->
      <header class="entete-top">
        <button
          type="button"
          class="bouton-retour"
          aria-label="Retourner à la page précédente"
          @click="retournerEnArriere"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
<!-- 
        <div class="logo-letgo-block">
          <span class="logo-texte">LET'S GO</span>
        </div> -->

        <div class="spacer-top"></div>
      </header>

      <!-- =====================================================
           CARTE PRINCIPALE DE VÉRIFICATION OTP (ZERO SHADOW)
      ====================================================== -->
      <main class="carte-verification">

        <!-- Badge Icône Sécurité / Email -->
        <!-- <div class="icone-badge-cercle">
          <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <polyline points="9 12 11 14 15 10"/>
          </svg>
        </div> -->

        <!-- Titre & Instructions -->
        <div class="titres-groupe">
          <h1 class="titre-principal">Vérification de sécurité</h1>
          <p class="texte-description">
            Pour activer votre compte et sécuriser vos futurs trajets, veuillez saisir le code à 6 chiffres envoyé à votre adresse e-mail :
          </p>
          <div class="badge-email-destinataire">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            <strong>{{ emailAffiche }}</strong>
          </div>
        </div>

        <!-- Alerte Erreur -->
        <div v-if="messageErreur" class="banniere-erreur" role="alert">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>{{ messageErreur }}</span>
        </div>

        <!-- Alerte Succès (Renvoi de code) -->
        <div v-if="messageSucces" class="banniere-succes" role="status">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <span>{{ messageSucces }}</span>
        </div>

        <!-- ===================================================
             GRILLE DES 6 CASES DE SAISIE DU CODE OTP
        ==================================================== -->
        <form class="formulaire-otp" @submit.prevent="validerCode">
          <div class="champs-otp-grille" @paste="gererCollage">
            <input
              v-for="(chiffre, index) in casesOtp"
              :key="index"
              :ref="el => inputsOtp[index] = el"
              v-model="casesOtp[index]"
              type="text"
              inputmode="numeric"
              maxlength="1"
              autocomplete="one-time-code"
              class="case-otp"
              :class="{ 'case-remplie': casesOtp[index] }"
              :aria-label="`Chiffre ${index + 1}`"
              @input="gererSaisie(index, $event)"
              @keydown="gererTouche(index, $event)"
            />
          </div>

          <!-- Bouton de Soumission -->
          <button
            type="submit"
            class="bouton-valider"
            :disabled="!estCodeComplet || estEnCoursChargement"
          >
            <span v-if="estEnCoursChargement" class="spinner-chargement"></span>
            <span v-else>Valider et activer mon compte</span>
          </button>
        </form>

        <!-- ===================================================
             ZONE DE RENVOI DU CODE AVEC COMPTE À REBOURS
        ==================================================== -->
        <div class="pied-renvoi">
          <p class="texte-renvoi">Vous n'avez pas reçu le code de confirmation ?</p>

          <button
            v-if="compteurSecondes === 0"
            type="button"
            class="bouton-renvoyer"
            :disabled="estEnCoursRenvoi"
            @click="demanderNouveauCode"
          >
            <span v-if="estEnCoursRenvoi">Envoi en cours...</span>
            <span v-else>Renvoyer un nouveau code</span>
          </button>

          <div v-else class="timer-renvoi">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span>Renvoyer un code dans <strong>{{ formatTemps(compteurSecondes) }}</strong></span>
          </div>
        </div>

      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authentification'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Récupération de l'email depuis l'URL ou le store
const emailCible = ref(route.query.email || authStore.utilisateur?.email || '')
const emailAffiche = computed(() => emailCible.value || 'votre adresse e-mail')

// État des 6 cases OTP
const casesOtp = ref(['', '', '', '', '', ''])
const inputsOtp = ref([])

// États de chargement et alertes
const estEnCoursChargement = ref(false)
const estEnCoursRenvoi = ref(false)
const messageErreur = ref('')
const messageSucces = ref('')

// Compte à rebours 60 secondes pour renvoi
const compteurSecondes = ref(60)
let timerInterval = null

const estCodeComplet = computed(() => {
  return casesOtp.value.every(c => c && c.trim() !== '')
})

function formatTemps(sec) {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function demarrerTimer() {
  arreterTimer()
  compteurSecondes.value = 60
  timerInterval = setInterval(() => {
    if (compteurSecondes.value > 0) {
      compteurSecondes.value--
    } else {
      arreterTimer()
    }
  }, 1000)
}

function arreterTimer() {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

// Gestion de la saisie case par case
function gererSaisie(index, event) {
  const valeur = event.data || event.target.value
  messageErreur.value = ''

  if (!/^\d*$/.test(valeur)) {
    casesOtp.value[index] = ''
    return
  }

  if (valeur) {
    casesOtp.value[index] = valeur.slice(-1)
    // Déplacer le focus vers la case suivante
    if (index < 5 && inputsOtp.value[index + 1]) {
      inputsOtp.value[index + 1].focus()
    }
  }

  // Si les 6 chiffres sont saisis, déclencher automatiquement la validation
  if (estCodeComplet.value) {
    validerCode()
  }
}

// Gestion des touches du clavier (Retour arrière / Flèches)
function gererTouche(index, event) {
  if (event.key === 'Backspace') {
    if (!casesOtp.value[index] && index > 0 && inputsOtp.value[index - 1]) {
      inputsOtp.value[index - 1].focus()
    }
  } else if (event.key === 'ArrowLeft' && index > 0) {
    inputsOtp.value[index - 1]?.focus()
  } else if (event.key === 'ArrowRight' && index < 5) {
    inputsOtp.value[index + 1]?.focus()
  }
}

// Support du Copier-Coller (Ctrl+V) d'un code complet à 6 chiffres
function gererCollage(event) {
  event.preventDefault()
  const texteColle = (event.clipboardData || window.clipboardData).getData('text').trim()
  const chiffres = texteColle.replace(/\D/g, '').slice(0, 6)

  if (chiffres.length > 0) {
    for (let i = 0; i < 6; i++) {
      casesOtp.value[i] = chiffres[i] || ''
    }
    const dernierIndex = Math.min(chiffres.length, 5)
    inputsOtp.value[dernierIndex]?.focus()

    if (chiffres.length === 6) {
      validerCode()
    }
  }
}

// Soumission et vérification du code auprès de l'API Django
async function validerCode() {
  if (!estCodeComplet.value || estEnCoursChargement.value) return

  const codeConcatene = casesOtp.value.join('')
  estEnCoursChargement.value = true
  messageErreur.value = ''
  messageSucces.value = ''

  try {
    const res = await authStore.verifierCode({
      email: emailCible.value,
      code: codeConcatene
    })

    if (res.succes) {
      messageSucces.value = 'Compte vérifié avec succès ! Redirection vers la page de connexion...'
      
      // Redirection immédiate vers la page de connexion avec l'e-mail pré-rempli
      setTimeout(() => {
        router.push({
          path: '/connexion',
          query: { active: '1', email: emailCible.value }
        })
      }, 700)
    } else {
      messageErreur.value = res.erreur || 'Code incorrect. Veuillez réessayer.'
      // Réinitialiser les cases pour resaisir
      casesOtp.value = ['', '', '', '', '', '']
      inputsOtp.value[0]?.focus()
    }
  } catch (err) {
    console.error('Erreur lors de la vérification OTP :', err)
    messageErreur.value = 'Une erreur inattendue est survenue. Veuillez vérifier votre connexion.'
  } finally {
    estEnCoursChargement.value = false
  }
}

// Demande d'un nouveau code
async function demanderNouveauCode() {
  if (compteurSecondes.value > 0 || estEnCoursRenvoi.value) return

  estEnCoursRenvoi.value = true
  messageErreur.value = ''
  messageSucces.value = ''

  try {
    const res = await authStore.renvoyerCode(emailCible.value)
    if (res.succes) {
      messageSucces.value = res.message || 'Un nouveau code vous a été envoyé par e-mail.'
      casesOtp.value = ['', '', '', '', '', '']
      inputsOtp.value[0]?.focus()
      demarrerTimer()
    } else {
      messageErreur.value = res.erreur || 'Impossible de renvoyer le code pour le moment.'
    }
  } catch (err) {
    console.error('Erreur renvoi code :', err)
    messageErreur.value = 'Erreur lors de la demande du nouveau code.'
  } finally {
    estEnCoursRenvoi.value = false
  }
}

function retournerEnArriere() {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/connexion')
  }
}

onMounted(() => {
  demarrerTimer()
  // Focus sur la première case
  setTimeout(() => {
    inputsOtp.value[0]?.focus()
  }, 200)
})

onUnmounted(() => {
  arreterTimer()
})
</script>

<style scoped>
/* ==========================================================================
   MISE EN PAGE GÉNÉRALE & STYLE (ZERO SHADOW, CHARTE LET'S GO)
   ========================================================================== */
.page-verification {
  --brand-primary: #FF4D2D;
  --brand-hover: #F04427;
  --text-dark: #111627;
  --text-muted: #64748B;
  --border-light: #E2E8F0;
  --bg-page: #F8FAFC;
  --emerald-green: #10B981;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;
  background-color: var(--bg-page);
  padding: 24px 16px 60px;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--text-dark);
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
}

.conteneur-verification {
  width: 100%;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ==========================================================================
   EN-TÊTE
   ========================================================================== */
.entete-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.bouton-retour {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #FFFFFF;
  border: 1px solid var(--border-light);
  color: var(--text-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
  box-shadow: none !important;
}

.bouton-retour:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
  transform: translateX(-2px);
}

.logo-texte {
  font-size: 20px;
  font-weight: 900;
  color: var(--brand-primary);
  letter-spacing: -0.5px;
}

.spacer-top {
  width: 42px;
}

/* ==========================================================================
   CARTE PRINCIPALE (ZERO SHADOW)
   ========================================================================== */
.carte-verification {
  background: #FFFFFF;
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 36px 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: none !important;
  box-sizing: border-box;
}

@media (min-width: 640px) {
  .carte-verification {
    padding: 44px 38px;
  }
}

.icone-badge-cercle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #FFF5F2;
  border: 1px solid #FFE4DE;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.titres-groupe {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}

.titre-principal {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-dark);
  margin: 0;
  letter-spacing: -0.4px;
}

@media (min-width: 640px) {
  .titre-principal {
    font-size: 25px;
  }
}

.texte-description {
  font-size: 13.5px;
  line-height: 1.5;
  color: var(--text-muted);
  margin: 0;
  max-width: 420px;
}

.badge-email-destinataire {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #F8FAFC;
  border: 1px solid var(--border-light);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-dark);
  margin-top: 4px;
}

/* ==========================================================================
   BANNIÈRES ALERTE
   ========================================================================== */
.banniere-erreur {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #FEF2F2;
  border: 1px solid #FEE2E2;
  color: #DC2626;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 13px;
  font-weight: 600;
  text-align: left;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.banniere-succes {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #ECFDF5;
  border: 1px solid #D1FAE5;
  color: #059669;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 13px;
  font-weight: 600;
  text-align: left;
  margin-bottom: 20px;
  box-sizing: border-box;
}

/* ==========================================================================
   GRILLE DES 6 CASES OTP
   ========================================================================== */
.formulaire-otp {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 26px;
  margin-bottom: 24px;
}

.champs-otp-grille {
  display: flex;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

@media (min-width: 480px) {
  .champs-otp-grille {
    gap: 12px;
  }
}

.case-otp {
  width: 46px;
  height: 56px;
  border-radius: 14px;
  background: #F8FAFC;
  border: 1.5px solid var(--border-light);
  text-align: center;
  font-size: 24px;
  font-weight: 800;
  color: var(--text-dark);
  outline: none;
  transition: all 0.15s ease;
  box-sizing: border-box;
}

@media (min-width: 480px) {
  .case-otp {
    width: 54px;
    height: 64px;
    font-size: 28px;
  }
}

.case-otp:focus {
  border-color: var(--brand-primary);
  background: #FFFFFF;
}

.case-otp.case-remplie {
  border-color: #CBD5E1;
  background: #FFFFFF;
}

/* ==========================================================================
   BOUTON DE SOUMISSION
   ========================================================================== */
.bouton-valider {
  width: 100%;
  height: 50px;
  background: var(--brand-primary);
  color: #FFFFFF;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.18s ease, transform 0.18s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: none !important;
}

.bouton-valider:hover:not(:disabled) {
  background: var(--brand-hover);
  transform: translateY(-1px);
}

.bouton-valider:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.spinner-chargement {
  width: 20px;
  height: 20px;
  border: 2.5px solid rgba(255, 255, 255, 0.4);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: rotation 0.6s linear infinite;
}

@keyframes rotation {
  to { transform: rotate(360deg); }
}

/* ==========================================================================
   PIED : RENVOI DU CODE
   ========================================================================== */
.pied-renvoi {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding-top: 12px;
  border-top: 1px solid #F1F5F9;
}

.texte-renvoi {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
}

.bouton-renvoyer {
  background: none;
  border: none;
  color: var(--brand-primary);
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.15s ease;
}

.bouton-renvoyer:hover:not(:disabled) {
  text-decoration: underline;
  color: var(--brand-hover);
}

.bouton-renvoyer:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.timer-renvoi {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: var(--text-muted);
  background: #F1F5F9;
  padding: 5px 12px;
  border-radius: 12px;
}

.timer-renvoi strong {
  color: var(--text-dark);
}
</style>
