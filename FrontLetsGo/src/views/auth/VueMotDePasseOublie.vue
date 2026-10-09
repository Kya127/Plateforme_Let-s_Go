<template>
  <div class="page-reset">
    <!-- =====================================================
         LOGO DESKTOP : EN HAUT À GAUCHE
    ====================================================== -->
    <header class="entete-desktop" aria-label="Identité Let's Go">
      <router-link to="/accueil" class="logo-marque-desktop">
        <span class="logo-texte-noir">LET'S </span>
        <span class="logo-texte-orange">GO</span>
      </router-link>
    </header>

    <!-- =====================================================
         CONTENEUR PRINCIPAL DU FORMULAIRE
    ====================================================== -->
    <div class="conteneur-reset">

      <!-- =====================================================
           EN-TÊTE MOBILE : CHEVRON À GAUCHE & LOGO AU MILIEU
      ====================================================== -->
      <header class="entete-mobile">
        <button
          type="button"
          class="bouton-retour"
          aria-label="Retourner à la page de connexion"
          @click="retourConnexion"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>

        <router-link to="/accueil" class="logo-marque-mobile">
          <span class="logo-texte-noir">LET'S </span>
          <span class="logo-texte-orange">GO</span>
        </router-link>

        <div class="espaceur-retour" aria-hidden="true"></div>
      </header>

      <!-- =====================================================
           BARRE RETOUR DESKTOP
      ====================================================== -->
      <div class="barre-retour-desktop">
        <button
          type="button"
          class="bouton-retour-desktop"
          aria-label="Retourner à la connexion"
          @click="retourConnexion"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          <span>Retour à la connexion</span>
        </button>
      </div>

      <!-- =====================================================
           CARTE CENTRALE (ZERO SHADOW - DESIGN ÉPURÉ LET'S GO)
      ====================================================== -->
      <main class="carte-reset">

        <!-- Badge Icône Sécurité / Cadenas -->
        <!-- <div class="icone-badge-cercle">
           Icône sécurité pour étape code 
          <svg v-if="etapeCourante === 'code' || etapeCourante === 'email'" viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <polyline points="9 12 11 14 15 10"/>
          </svg>
           Icône cadenas pour nouveau mot de passe 
          <svg v-else viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div> -->

        <!-- ===================================================
             ÉTAPE INITIALE FACULTATIVE : IDENTIFICATION DE L'EMAIL
             (Visible seulement si aucun email n'a pu être retrouvé)
        ==================================================== -->
        <div v-if="etapeCourante === 'email'" class="contenu-etape">
          <div class="bloc-titres">
            <h1 class="titre-principal">Mot de passe oublié</h1>
            <p class="sous-titre">
              Entrez l'adresse e-mail de votre compte pour recevoir votre code de vérification à 6 chiffres.
            </p>
          </div>

          <!-- Alerte Erreur -->
          <div v-if="messageErreur" class="alerte-erreur" role="alert">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{{ messageErreur }}</span>
          </div>

          <form class="formulaire-champs" @submit.prevent="envoyerCodeInitial">
            <div class="groupe-champ">
              <label for="emailSaisi" class="label-champ">
                Adresse e-mail <span class="etoile-requise">*</span>
              </label>
              <div class="conteneur-input" :class="{ 'input-invalide': erreurEmail }">
                <span class="icone-champ" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                    <polyline points="22,6 12,13 2,6"/>
                  </svg>
                </span>
                <input
                  id="emailSaisi"
                  v-model.trim="email"
                  type="email"
                  class="input-saisie"
                  placeholder="Ex: fatou@exemple.sn"
                  autocomplete="email"
                  required
                />
              </div>
              <span v-if="erreurEmail" class="texte-erreur">{{ erreurEmail }}</span>
            </div>

            <button
              type="submit"
              class="bouton-principal"
              :disabled="estEnChargement"
            >
              <span v-if="!estEnChargement">Recevoir le code de vérification</span>
              <span v-else class="chargement-contenu">
                <span class="spinner-chargement"></span>
                Envoi en cours...
              </span>
            </button>
          </form>
        </div>

        <!-- ===================================================
             ÉTAPE 1 : VÉRIFICATION DU CODE (OTP UNIQUEMENT)
             Aucun champ mot de passe ni confirmation mot de passe.
        ==================================================== -->
        <div v-else-if="etapeCourante === 'code'" class="contenu-etape">
          <div class="bloc-titres">
            <h1 class="titre-principal">Vérification de sécurité</h1>
            <p class="sous-titre">
              Entrez le code envoyé sur l'adresse suivante :
            </p>
            <div class="badge-email-destinataire">
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <strong>{{ emailMasque }}</strong>
            </div>
          </div>

          <!-- Alertes -->
          <div v-if="messageErreur" class="alerte-erreur" role="alert">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{{ messageErreur }}</span>
          </div>

          <div v-if="messageSucces" class="alerte-succes" role="status">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <span>{{ messageSucces }}</span>
          </div>

          <!-- Formulaire OTP (Code à 6 chiffres uniquement) -->
          <form class="formulaire-champs" @submit.prevent="validerCodeOtp">
            <div class="groupe-champ">
              <div class="grille-otp" @paste="gererCollage">
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
            </div>

            <!-- Bouton Valider le code -->
            <button
              type="submit"
              class="bouton-principal"
              :disabled="!estCodeComplet || estEnChargement"
            >
              <span v-if="!estEnChargement">Valider le code</span>
              <span v-else class="chargement-contenu">
                <span class="spinner-chargement"></span>
                Vérification en cours...
              </span>
            </button>
          </form>

          <!-- Zone Renvoyer un nouveau code -->
          <div class="pied-renvoi">
            <button
              v-if="compteurSecondes === 0"
              type="button"
              class="bouton-renvoi"
              :disabled="estEnCoursRenvoi"
              @click="demanderNouveauCode"
            >
              <span v-if="estEnCoursRenvoi">Envoi en cours...</span>
              <span v-else>Renvoyer un nouveau code</span>
            </button>
            <div v-else class="timer-texte">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              <span>Renvoyer un code dans <strong>00:{{ String(compteurSecondes).padStart(2, '0') }}</strong></span>
            </div>
          </div>
        </div>

        <!-- ===================================================
             ÉTAPE 2 : NOUVEAU MOT DE PASSE (CHAMPS MDP UNIQUEMENT)
             Apparaît une fois le code validé.
        ==================================================== -->
        <div v-else-if="etapeCourante === 'nouveau_mdp'" class="contenu-etape">
          <div class="bloc-titres">
            <h1 class="titre-principal">Nouveau mot de passe</h1>
            <p class="sous-titre">
              Définissez un mot de passe sécurisé d'au moins 8 caractères pour votre compte.
            </p>
          </div>

          <!-- Alertes -->
          <div v-if="messageErreur" class="alerte-erreur" role="alert">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{{ messageErreur }}</span>
          </div>

          <div v-if="messageSucces" class="alerte-succes" role="status">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <span>{{ messageSucces }}</span>
          </div>

          <!-- Formulaire Nouveau Mot de passe -->
          <form class="formulaire-champs" @submit.prevent="enregistrerNouveauMotDePasse">

            <!-- Champ 1 : Nouveau mot de passe -->
            <div class="groupe-champ">
              <label for="nouveauMdp" class="label-champ">
                Nouveau mot de passe <span class="etoile-requise">*</span>
              </label>
              <div class="conteneur-input" :class="{ 'input-invalide': erreurMdp }">
                <span class="icone-champ" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="nouveauMdp"
                  v-model="nouveauMdp"
                  :type="mdpVisible ? 'text' : 'password'"
                  class="input-saisie"
                  placeholder="8 caractères minimum"
                  autocomplete="new-password"
                  required
                />
                <button
                  type="button"
                  class="bouton-oeil"
                  @click="mdpVisible = !mdpVisible"
                  :aria-label="mdpVisible ? 'Masquer' : 'Afficher'"
                >
                  <svg v-if="!mdpVisible" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
              <span v-if="erreurMdp" class="texte-erreur">{{ erreurMdp }}</span>
            </div>

            <!-- Champ 2 : Confirmation mot de passe -->
            <div class="groupe-champ">
              <label for="confirmerMdp" class="label-champ">
                Confirmer le mot de passe <span class="etoile-requise">*</span>
              </label>
              <div class="conteneur-input" :class="{ 'input-invalide': erreurConfirmer }">
                <span class="icone-champ" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="confirmerMdp"
                  v-model="confirmerMdp"
                  :type="mdpVisible ? 'text' : 'password'"
                  class="input-saisie"
                  placeholder="Répétez le mot de passe"
                  autocomplete="new-password"
                  required
                />
              </div>
              <span v-if="erreurConfirmer" class="texte-erreur">{{ erreurConfirmer }}</span>
            </div>

            <!-- Bouton Enregistrer et se connecter -->
            <button
              type="submit"
              class="bouton-principal"
              :disabled="estEnChargement || !estFormulaireMdpValide"
            >
              <span v-if="!estEnChargement">Enregistrer</span>
              <span v-else class="chargement-contenu">
                <span class="spinner-chargement"></span>
                Mise à jour en cours...
              </span>
            </button>
          </form>
        </div>

      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'

const router = useRouter()
const route = useRoute()
const authStore = useAuthentificationStore()

/* ==========================================================================
   NAVIGATION DES ÉTAPES :
   'code'       : Saisie du code OTP 6 chiffres (directe dès clic sur mot de passe oublié)
   'nouveau_mdp': Saisie du nouveau mot de passe (après validation du code)
   'email'      : Cas de repli si aucun e-mail n'est connu en session ou query
   ========================================================================== */
const etapeCourante = ref('code')

// Données d'authentification
const email = ref('')
const codeValide = ref('')
const erreurEmail = ref('')
const messageErreur = ref('')
const messageSucces = ref('')
const estEnChargement = ref(false)
const estEnCoursRenvoi = ref(false)

// Cases OTP
const casesOtp = ref(['', '', '', '', '', ''])
const inputsOtp = ref([])

// Champs mot de passe
const nouveauMdp = ref('')
const confirmerMdp = ref('')
const mdpVisible = ref(false)
const erreurMdp = ref('')
const erreurConfirmer = ref('')

// Compte à rebours anti-spam de 60 secondes
const compteurSecondes = ref(60)
let timer = null

/* ==========================================================================
   FORMATAGE & MASQUAGE DE L'EMAIL
   Exemple : julien@gmail.com -> jul*****@gmail.com
   ========================================================================== */
function masquerEmail(adresse) {
  if (!adresse || typeof adresse !== 'string' || !adresse.includes('@')) {
    return adresse || 'votre compte'
  }
  const [identifiant, domaine] = adresse.split('@')
  if (identifiant.length <= 2) {
    return `${identifiant}*****@${domaine}`
  }
  const visible = identifiant.slice(0, 3)
  return `${visible}*****@${domaine}`
}

const emailMasque = computed(() => masquerEmail(email.value))

const estCodeComplet = computed(() => {
  return casesOtp.value.every(c => c && c.trim() !== '')
})

const estFormulaireMdpValide = computed(() => {
  return nouveauMdp.value.length >= 8 && nouveauMdp.value === confirmerMdp.value
})

/* ==========================================================================
   GESTION DU MINUTEUR DE 60 SECONDES
   ========================================================================== */
function demarrerTimer(secondes = null) {
  arreterTimer()
  if (secondes !== null) {
    compteurSecondes.value = secondes
  } else if (compteurSecondes.value <= 0) {
    compteurSecondes.value = 60
  }
  timer = setInterval(() => {
    if (compteurSecondes.value > 0) {
      compteurSecondes.value--
    } else {
      arreterTimer()
    }
  }, 1000)
}

function arreterTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

/* ==========================================================================
   GESTION DES CASES OTP (6 CHIFFRES)
   ========================================================================== */
function gererSaisie(index, event) {
  const val = event.data || event.target.value
  messageErreur.value = ''

  if (!/^\d*$/.test(val)) {
    casesOtp.value[index] = ''
    return
  }

  if (val) {
    casesOtp.value[index] = val.slice(-1)
    if (index < 5 && inputsOtp.value[index + 1]) {
      inputsOtp.value[index + 1].focus()
    }
  }

  // Si les 6 chiffres sont complétés, déclencher automatiquement la validation
  if (estCodeComplet.value) {
    validerCodeOtp()
  }
}

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

function gererCollage(event) {
  event.preventDefault()
  const texte = (event.clipboardData || window.clipboardData).getData('text').trim()
  const chiffres = texte.replace(/\D/g, '').slice(0, 6)

  if (chiffres.length > 0) {
    for (let i = 0; i < 6; i++) {
      casesOtp.value[i] = chiffres[i] || ''
    }
    const idx = Math.min(chiffres.length, 5)
    inputsOtp.value[idx]?.focus()

    if (chiffres.length === 6) {
      validerCodeOtp()
    }
  }
}

/* ==========================================================================
   ÉTAPE 1 : VALIDATION DU CODE OTP AUPRÈS DU BACKEND
   ========================================================================== */
async function validerCodeOtp() {
  if (!estCodeComplet.value || estEnChargement.value) return

  messageErreur.value = ''
  messageSucces.value = ''
  estEnChargement.value = true

  const codeSaisi = casesOtp.value.join('')

  try {
    const res = await authStore.verifierCodeReset({
      email: email.value,
      code: codeSaisi,
    })

    if (res.succes) {
      // Code vérifié ! Mémorisation et passage immédiat à l'Étape 2
      codeValide.value = codeSaisi
      etapeCourante.value = 'nouveau_mdp'
      messageSucces.value = ''
      messageErreur.value = ''
    } else {
      messageErreur.value = res.erreur || 'Code incorrect. Veuillez vérifier les 6 chiffres.'
      casesOtp.value = ['', '', '', '', '', '']
      inputsOtp.value[0]?.focus()
    }
  } catch (err) {
    console.error('Erreur validation code reset:', err)
    messageErreur.value = 'Une erreur inattendue est survenue. Veuillez réessayer.'
  } finally {
    estEnChargement.value = false
  }
}

/* ==========================================================================
   RENVOI D'UN NOUVEAU CODE (AVEC DÉLAI 60S)
   ========================================================================== */
async function demanderNouveauCode() {
  if (compteurSecondes.value > 0 || estEnCoursRenvoi.value) return

  estEnCoursRenvoi.value = true
  messageErreur.value = ''
  messageSucces.value = ''

  try {
    const res = await authStore.demanderResetMotDePasse(email.value)
    if (res.succes) {
      messageSucces.value = res.message || 'Un nouveau code vous a été envoyé par e-mail.'
      casesOtp.value = ['', '', '', '', '', '']
      demarrerTimer(res.secondesRestantes || 60)
      inputsOtp.value[0]?.focus()
    } else {
      messageErreur.value = res.erreur || 'Impossible de renvoyer le code pour le moment.'
    }
  } catch (err) {
    messageErreur.value = 'Erreur lors du renvoi du code.'
  } finally {
    estEnCoursRenvoi.value = false
  }
}

/* ==========================================================================
   ÉTAPE 2 : DÉFINITION DU NOUVEAU MOT DE PASSE
   ========================================================================== */
async function enregistrerNouveauMotDePasse() {
  messageErreur.value = ''
  erreurMdp.value = ''
  erreurConfirmer.value = ''

  if (nouveauMdp.value.length < 8) {
    erreurMdp.value = 'Le mot de passe doit comporter au moins 8 caractères.'
    return
  }

  if (nouveauMdp.value !== confirmerMdp.value) {
    erreurConfirmer.value = 'Les deux mots de passe ne correspondent pas.'
    return
  }

  estEnChargement.value = true

  try {
    const res = await authStore.reinitialiserMotDePasse({
      email: email.value,
      code: codeValide.value,
      nouveau_mot_de_passe: nouveauMdp.value,
    })

    if (res.succes) {
      messageSucces.value = 'Votre mot de passe a été mis à jour avec succès ! Redirection...'
      setTimeout(() => {
        router.push({
          path: '/connexion',
          query: { reset: '1', email: email.value },
        })
      }, 800)
    } else {
      messageErreur.value = res.erreur || 'Impossible de mettre à jour le mot de passe.'
    }
  } catch (err) {
    console.error('Erreur réinitialisation mdp:', err)
    messageErreur.value = 'Une erreur inattendue est survenue.'
  } finally {
    estEnChargement.value = false
  }
}

/* ==========================================================================
   CAS DE REPLI : ENVOI INITIAL DU CODE SI EMAIL ÉTAIT NON DÉFINI
   ========================================================================== */
async function envoyerCodeInitial() {
  messageErreur.value = ''
  erreurEmail.value = ''

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.value) {
    erreurEmail.value = "L'adresse e-mail est obligatoire."
    return
  }
  if (!emailRegex.test(email.value)) {
    erreurEmail.value = 'Veuillez entrer une adresse e-mail valide.'
    return
  }

  estEnChargement.value = true

  try {
    const res = await authStore.demanderResetMotDePasse(email.value)
    if (res.succes) {
      localStorage.setItem('letsgo_dernier_email', email.value)
      etapeCourante.value = 'code'
      demarrerTimer()
      messageSucces.value = 'Un code de confirmation a été envoyé à votre adresse.'
      setTimeout(() => {
        inputsOtp.value[0]?.focus()
      }, 250)
    } else {
      messageErreur.value = res.erreur || "Impossible d'envoyer le code."
    }
  } catch (err) {
    messageErreur.value = 'Impossible de contacter le serveur.'
  } finally {
    estEnChargement.value = false
  }
}

function retourConnexion() {
  router.push('/connexion')
}

/* ==========================================================================
   INITIALISATION AU MONTAGE DU COMPOSANT
   ========================================================================== */
onMounted(() => {
  // 1. Récupération de l'adresse e-mail associée au compte
  const emailParam = route.query.email ? String(route.query.email).trim() : ''
  const emailSession = authStore.utilisateur?.email || localStorage.getItem('letsgo_dernier_email') || ''
  const adresseIdentifiee = (emailParam && emailParam.includes('@')) ? emailParam : (emailSession && emailSession.includes('@') ? emailSession : '')

  if (adresseIdentifiee) {
    email.value = adresseIdentifiee
    etapeCourante.value = 'code'

    // Envoi automatique du code OTP si l'utilisateur arrive sur la page
    authStore.demanderResetMotDePasse(adresseIdentifiee).then((res) => {
      if (res && res.succes) {
        demarrerTimer(res.secondesRestantes || 60)
        if (res.dejaEnvoye) {
          messageSucces.value = 'Un code vous a déjà été envoyé par e-mail. Vérifiez votre boîte de réception.'
        }
      } else if (res && res.erreur) {
        messageErreur.value = res.erreur
        demarrerTimer(60)
      }
    }).catch(err => {
      console.warn("Notification envoi code initial:", err)
      demarrerTimer(60)
    })

    setTimeout(() => {
      inputsOtp.value[0]?.focus()
    }, 250)
  } else {
    // Si aucun email n'a pu être identifié, afficher la saisie email de repli
    etapeCourante.value = 'email'
  }
})

onUnmounted(() => {
  arreterTimer()
})
</script>

<style scoped>
/* ==========================================================================
   PAGE ET FOND ZERO SHADOW - THÈME OFFICIEL LET'S GO
   ========================================================================== */
.page-reset {
  min-height: 100vh;
  min-height: 100dvh;
  width: 100%;
  background-color: #f7f9fc;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px 16px;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  position: relative;
}

/* En-tête desktop avec Logo */
.entete-desktop {
  position: absolute;
  top: 32px;
  left: 48px;
  display: none;
}

@media (min-width: 768px) {
  .entete-desktop {
    display: block;
  }
}

.logo-marque-desktop {
  text-decoration: none;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.5px;
}

.logo-texte-noir {
  color: #111827;
}

.logo-texte-orange {
  color: #ff4d2d;
}

/* Conteneur principal */
.conteneur-reset {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  z-index: 2;
}

/* En-tête mobile */
.entete-mobile {
  display: grid;
  grid-template-columns: 42px 1fr 42px;
  align-items: center;
  width: 100%;
}

@media (min-width: 768px) {
  .entete-mobile {
    display: none;
  }
}

.bouton-retour {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  color: #1e293b;
  cursor: pointer;
  box-shadow: none !important;
  transition: all 0.2s ease;
}

.bouton-retour:hover {
  background-color: #f1f5f9;
}

.logo-marque-mobile {
  text-decoration: none;
  font-size: 23px;
  font-weight: 900;
  letter-spacing: -0.5px;
  text-align: center;
  justify-self: center;
}

/* Barre retour Desktop */
.barre-retour-desktop {
  display: none;
}

@media (min-width: 768px) {
  .barre-retour-desktop {
    display: flex;
    justify-content: flex-start;
  }
}

.bouton-retour-desktop {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.2s ease;
  font-family: inherit;
}

.bouton-retour-desktop:hover {
  color: #ff4d2d;
}

/* Carte centrale (Zero shadow strict) */
.carte-reset {
  width: 100%;
  background: #ffffff;
  border-radius: 24px;
  padding: 32px 28px;
  border: 1px solid rgba(226, 232, 240, 0.85);
  box-shadow: none !important;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.icone-badge-cercle {
  width: 58px;
  height: 58px;
  border-radius: 18px;
  background: #fff5f2;
  border: 1px solid #ffe2db;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.contenu-etape {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bloc-titres {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.titre-principal {
  font-size: 24px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.5px;
  margin: 0;
}

.sous-titre {
  font-size: 13.5px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.badge-email-destinataire {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  margin: 4px auto 0;
  width: fit-content;
}

.badge-email-destinataire svg {
  color: #64748b;
}

/* Alertes épurées */
.alerte-erreur {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 13.5px;
  font-weight: 500;
  line-height: 1.4;
}

.alerte-erreur svg {
  flex-shrink: 0;
}

.alerte-succes {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 13.5px;
  font-weight: 500;
  line-height: 1.4;
}

.alerte-succes svg {
  flex-shrink: 0;
  color: #10b981;
}

/* Formulaires & Champs */
.formulaire-champs {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.groupe-champ {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-champ {
  font-size: 13.5px;
  font-weight: 600;
  color: #374151;
}

.etoile-requise {
  color: #ff4d2d;
}

.conteneur-input {
  position: relative;
  display: flex;
  align-items: center;
  background-color: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  transition: all 0.2s ease;
}

.conteneur-input:focus-within {
  background-color: #ffffff;
  border-color: #ff4d2d;
}

.input-invalide {
  border-color: #ef4444 !important;
  background-color: #fffafb;
}

.icone-champ {
  display: flex;
  align-items: center;
  padding-left: 14px;
  color: #94a3b8;
}

.input-saisie {
  flex: 1;
  width: 100%;
  padding: 13px 14px;
  border: none;
  background: transparent;
  font-size: 14.5px;
  color: #1e293b;
  outline: none;
  font-family: inherit;
}

.input-saisie::placeholder {
  color: #94a3b8;
}

.bouton-oeil {
  background: transparent;
  border: none;
  padding: 0 14px;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.bouton-oeil:hover {
  color: #475569;
}

.texte-erreur {
  font-size: 12px;
  color: #ef4444;
  font-weight: 500;
}

/* Grille OTP (6 cases proportionnées) */
.grille-otp {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  margin-top: 4px;
}

.case-otp {
  width: 100%;
  aspect-ratio: 1;
  max-height: 54px;
  text-align: center;
  font-size: 22px;
  font-weight: 800;
  color: #111627;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  outline: none;
  transition: all 0.2s ease;
  font-family: inherit;
  box-shadow: none !important;
}

.case-otp:focus {
  background: #ffffff;
  border-color: #ff4d2d;
  transform: translateY(-1px);
}

.case-remplie {
  background: #ffffff;
  border-color: #cbd5e1;
}

/* Bouton principal Let's Go */
.bouton-principal {
  width: 100%;
  padding: 14px;
  background-color: #ff4d2d;
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: none !important;
  font-family: inherit;
  margin-top: 4px;
}

.bouton-principal:hover:not(:disabled) {
  background-color: #e03e1f;
  transform: translateY(-1px);
}

.bouton-principal:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.chargement-contenu {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner-chargement {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: rotation 0.8s linear infinite;
}

@keyframes rotation {
  to {
    transform: rotate(360deg);
  }
}

/* Pied de renvoi */
.pied-renvoi {
  text-align: center;
  margin-top: -4px;
}

.bouton-renvoi {
  background: none;
  border: none;
  color: #ff4d2d;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  text-decoration: underline;
  font-family: inherit;
}

.bouton-renvoi:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.timer-texte {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
}

.timer-texte svg {
  color: #94a3b8;
}

.timer-texte strong {
  color: #111827;
}
</style>
