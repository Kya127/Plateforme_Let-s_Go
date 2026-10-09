<template>
  <div class="page-connexion">

    <!-- =====================================================
         LOGO DESKTOP : À GAUCHE EN DEHORS DU FORMULAIRE
    ====================================================== -->
    <header class="entete-desktop" aria-label="Identité Let's Go">
      <router-link to="/accueil" class="logo-marque-desktop">
        <span class="logo-texte-noir">LET'S </span>
        <span class="logo-texte-orange">GO</span>
      </router-link>
    </header>

    <!-- =====================================================
         CONTENEUR CENTRAL DU FORMULAIRE
    ====================================================== -->
    <div class="conteneur-connexion">

      <!-- =====================================================
           EN-TÊTE MOBILE : CHEVRON À GAUCHE & LOGO AU MILIEU
      ====================================================== -->
      <header class="entete-mobile">
        <!-- Bouton retour chevron (redirige vers l'accueil visiteur) -->
        <button
          type="button"
          class="bouton-retour"
          aria-label="Retourner à l'accueil"
          @click="retourArriere"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>

        <!-- Logo centré au milieu sur mobile -->
        <router-link to="/accueil" class="logo-marque-mobile">
          <span class="logo-texte-noir">LET'S </span>
          <span class="logo-texte-orange">GO</span>
        </router-link>

        <!-- Espaceur invisible pour équilibrer la grille et garantir un centrage parfait du logo -->
        <div class="espaceur-retour" aria-hidden="true"></div>
      </header>

      <!-- =====================================================
           BOUTON RETOUR DESKTOP (JUSTE AU-DESSUS DE LA CARTE)
      ====================================================== -->
      <div class="barre-retour-desktop">
        <button
          type="button"
          class="bouton-retour-desktop"
          aria-label="Retourner à l'accueil"
          @click="retourArriere"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          <span>Retour à l'accueil</span>
        </button>
      </div>

      <!-- =====================================================
           CARTE PRINCIPALE DE CONNEXION (ÉPURÉE & MODERNE)
      ====================================================== -->
      <main class="carte-connexion">

        <!-- Titre et sous-titre de bienvenue -->
        <div class="bloc-titre">
          <h1 class="titre-principal">Bon retour !</h1>
          <p class="sous-titre">Connectez-vous pour retrouver vos trajets et réservations</p>
        </div>

        <!-- Alerte de succès (ex: compte tout juste créé) -->
        <div v-if="messageSucces" class="alerte-succes" role="status">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <span>{{ messageSucces }}</span>
        </div>

        <!-- Alerte d'erreur de connexion -->
        <div v-if="messageErreur" class="alerte-erreur" role="alert">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <div class="conteneur-texte-erreur">
            <span>{{ messageErreur }}</span>
            <router-link
              v-if="compteNonVerifieEmail"
              :to="{ path: '/verification-compte', query: { email: compteNonVerifieEmail } }"
              class="lien-activer-compte"
            >
              Activer mon compte avec le code de confirmation &rarr;
            </router-link>
          </div>
        </div>

        <!-- Formulaire de connexion -->
        <form class="formulaire-champs" novalidate @submit.prevent="gererConnexion">

          <!-- Champ Identifiant (Email ou Numéro de téléphone) -->
          <div class="groupe-champ">
            <label for="identifiant" class="label-champ">
              Email ou Téléphone <span class="etoile-requise">*</span>
            </label>
            <div class="conteneur-input" :class="{ 'input-invalide': erreurs.identifiant }">
              <span class="icone-champ" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </span>
              <input
                id="identifiant"
                name="username"
                v-model.trim="formulaire.identifiant"
                type="text"
                class="input-saisie"
                placeholder="Ex: fatou@exemple.sn ou 77 123 45 67"
                autocomplete="username email"
                required
                @blur="validerIdentifiant"
              />
            </div>
            <span v-if="erreurs.identifiant" class="texte-erreur">{{ erreurs.identifiant }}</span>
          </div>

          <!-- Champ Mot de passe avec toggle Masquer/Afficher et lien Oublié -->
          <div class="groupe-champ">
            <div class="entete-label-champ">
              <label for="motDePasse" class="label-champ">
                Mot de passe <span class="etoile-requise">*</span>
              </label>
              <router-link
                :to="{ path: '/mot-de-passe-oublie', query: { email: emailPourReset } }"
                class="lien-oubli"
              >
                Mot de passe oublié ?
              </router-link>
            </div>

            <div class="conteneur-input" :class="{ 'input-invalide': erreurs.motDePasse }">
              <span class="icone-champ" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </span>

              <input
                id="motDePasse"
                name="password"
                v-model="formulaire.motDePasse"
                :type="motDePasseVisible ? 'text' : 'password'"
                class="input-saisie"
                placeholder="••••••••"
                autocomplete="current-password"
                required
                @blur="validerMotDePasse"
              />

              <!-- Bouton Afficher / Masquer mot de passe -->
              <button
                type="button"
                class="bouton-oeil"
                :aria-label="motDePasseVisible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
                @click="motDePasseVisible = !motDePasseVisible"
              >
                <!-- Œil ouvert -->
                <svg v-if="!motDePasseVisible" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <!-- Œil barré -->
                <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
            <span v-if="erreurs.motDePasse" class="texte-erreur">{{ erreurs.motDePasse }}</span>
          </div>

          <!-- Bouton principal de connexion -->
          <button
            type="submit"
            class="bouton-connexion"
            :disabled="estEnChargement"
          >
            <span v-if="!estEnChargement" class="contenu-bouton">
              <span>Se connecter</span>
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </span>
            <span v-else class="chargement-contenu">
              <span class="spinner-chargement"></span>
              Connexion en cours...
            </span>
          </button>
        </form>

        <!-- Séparateur visuel -->
        <div class="separateur">
          <span class="ligne-separateur"></span>
          <span class="texte-separateur">OU CONTINUER AVEC</span>
          <span class="ligne-separateur"></span>
        </div>

        <!-- Bouton Connexion avec Google -->
        <button
          type="button"
          class="bouton-google"
          :disabled="estEnChargement"
          @click="gererConnexionGoogle"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
          </svg>
          <span>Continuer avec Google</span>
        </button>

        <!-- Pied de carte : Redirection Inscription -->
        <footer class="pied-carte">
          <span>Nouveau sur Let's Go ?</span>
          <router-link to="/inscription" class="lien-inscription">
            Créer un compte
          </router-link>
        </footer>

      </main>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'

const routeur = useRouter()
const route = useRoute()
const storeAuth = useAuthentificationStore()

/* ==========================================================================
   ÉTATS LOCAUX
   ========================================================================== */
const motDePasseVisible = ref(false)
const estEnChargement = ref(false)
const messageErreur = ref('')
const messageSucces = ref('')
const compteNonVerifieEmail = ref('')

const formulaire = reactive({
  identifiant: '',
  motDePasse: '',
})

const emailPourReset = computed(() => {
  if (formulaire.identifiant && formulaire.identifiant.includes('@')) {
    return formulaire.identifiant.trim()
  }
  return localStorage.getItem('letsgo_dernier_email') || formulaire.identifiant || undefined
})

const erreurs = reactive({
  identifiant: '',
  motDePasse: '',
})

/* ==========================================================================
   SYNCHRONISATION AUTOMATIQUE AVEC L'URL (EX: APRÈS INSCRIPTION)
   ========================================================================== */
function synchroniserAvecUrl() {
  // Pré-remplir l'e-mail s'il provient de la redirection d'inscription ou d'activation
  if (route.query.email) {
    formulaire.identifiant = String(route.query.email).trim()
    if (formulaire.identifiant.includes('@')) {
      localStorage.setItem('letsgo_dernier_email', formulaire.identifiant)
    }
  }

  // Affichage du bandeau de confirmation d'inscription, activation ou réinitialisation
  if (route.query.reset === '1') {
    messageSucces.value = 'Votre mot de passe a été réinitialisé avec succès ! Connectez-vous avec vos nouveaux identifiants.'
  } else if (route.query.active === '1') {
    messageSucces.value = 'Votre compte a été vérifié avec succès ! Connectez-vous avec vos identifiants pour continuer.'
  } else if (route.query.inscrit === '1') {
    messageSucces.value = 'Votre compte a été créé avec succès ! Connectez-vous avec votre mot de passe pour commencer.'
  }
}

onMounted(() => {
  synchroniserAvecUrl()
  // Détection de l'autofill Google/navigateur sur les champs
  setTimeout(() => {
    const inputPass = document.getElementById('motDePasse')
    if (inputPass && inputPass.value && !formulaire.motDePasse) {
      formulaire.motDePasse = inputPass.value
    }
    const inputIdent = document.getElementById('identifiant')
    if (inputIdent && inputIdent.value && !formulaire.identifiant) {
      formulaire.identifiant = inputIdent.value.trim()
    }
  }, 350)
})

watch(
  () => route.query,
  () => {
    synchroniserAvecUrl()
  },
  { immediate: true, deep: true }
)

/* ==========================================================================
   VALIDATIONS UNITAIRES
   ========================================================================== */
function validerIdentifiant() {
  erreurs.identifiant = ''
  if (!formulaire.identifiant.trim()) {
    erreurs.identifiant = 'Veuillez saisir votre adresse e-mail ou numéro de téléphone.'
  }
}

function validerMotDePasse() {
  erreurs.motDePasse = ''
  if (!formulaire.motDePasse) {
    erreurs.motDePasse = 'Veuillez renseigner votre mot de passe.'
  }
}

function validerFormulaire() {
  // Capture de l'autofill Google s'il a été injecté
  const inputPass = document.getElementById('motDePasse')
  if (inputPass && inputPass.value && !formulaire.motDePasse) {
    formulaire.motDePasse = inputPass.value
  }
  const inputIdent = document.getElementById('identifiant')
  if (inputIdent && inputIdent.value && !formulaire.identifiant) {
    formulaire.identifiant = inputIdent.value.trim()
  }

  validerIdentifiant()
  validerMotDePasse()
  return !erreurs.identifiant && !erreurs.motDePasse
}

/* ==========================================================================
   SOUMISSION DU FORMULAIRE DE CONNEXION (JWT DJANGO)
   ========================================================================== */
async function gererConnexion() {
  messageErreur.value = ''
  compteNonVerifieEmail.value = ''

  if (!validerFormulaire()) {
    return
  }

  estEnChargement.value = true

  try {
    const resultat = await storeAuth.connecter(
      formulaire.identifiant.trim(),
      formulaire.motDePasse
    )

    if (resultat.succes) {
      // Redirection vers l'intention précédente ou la page d'accueil
      const redirectionCible =
        route.query.redirection ||
        storeAuth.consommerIntentionRedirection('/accueil')

      routeur.push(redirectionCible)
    } else {
      if (resultat.nonVerifie) {
        compteNonVerifieEmail.value = resultat.email || formulaire.identifiant.trim()
      }
      messageErreur.value =
        resultat.erreur ||
        'Identifiant ou mot de passe incorrect. Veuillez vérifier vos accès.'
    }
  } catch (err) {
    console.error('Erreur connexion:', err)
    messageErreur.value = 'Impossible de contacter le serveur. Vérifiez votre connexion.'
  } finally {
    estEnChargement.value = false
  }
}

/* ==========================================================================
   CONNEXION SOCIALE GOOGLE (SIMULÉE)
   ========================================================================== */
function gererConnexionGoogle() {
  estEnChargement.value = true
  setTimeout(() => {
    estEnChargement.value = false
    const redirectionCible =
      route.query.redirection ||
      storeAuth.consommerIntentionRedirection('/accueil')
    routeur.push(redirectionCible)
  }, 600)
}

/* ==========================================================================
   NAVIGATION : RETOUR VERS LA PAGE D'ACCUEIL (NON CONNECTÉ)
   ========================================================================== */
function retourArriere() {
  routeur.push('/accueil')
}

function motDePasseOublie() {
  alert('La réinitialisation de mot de passe sera bientôt disponible.')
}
</script>

<style scoped>
/* ==========================================================================
   MISE EN PAGE GLOBALE & FOND
   ========================================================================== */
.page-connexion {
  min-height: 100vh;
  min-height: 100dvh;
  width: 100%;
  background-color: #f7f9fc;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px 16px 40px;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #111827;
  position: relative;
  -webkit-font-smoothing: antialiased;
}

/* ==========================================================================
   LOGO DESKTOP : À GAUCHE EN DEHORS DU FORMULAIRE
   ========================================================================== */
.entete-desktop {
  display: none; /* Masqué par défaut sur mobile */
}

@media (min-width: 768px) {
  .entete-desktop {
    display: block;
    position: absolute;
    top: 36px;
    left: 48px;
    z-index: 10;
  }

  .logo-marque-desktop {
    text-decoration: none;
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.6px;
    display: inline-block;
    transition: transform 0.2s ease;
  }

  .logo-marque-desktop:hover {
    transform: scale(1.03);
  }
}

/* ==========================================================================
   CONTENEUR PRINCIPAL DU FORMULAIRE
   ========================================================================== */
.conteneur-connexion {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  z-index: 2;
}

/* ==========================================================================
   EN-TÊTE MOBILE : CHEVRON À GAUCHE & LOGO PARFAITEMENT CENTRÉ AU MILIEU
   ========================================================================== */
.entete-mobile {
  display: grid;
  grid-template-columns: 42px 1fr 42px;
  align-items: center;
  width: 100%;
  padding: 0 4px;
}

@media (min-width: 768px) {
  .entete-mobile {
    display: none; /* Masqué sur Desktop car le logo passe à gauche hors formulaire */
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
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.021);
}

.bouton-retour:hover {
  background-color: #f1f5f9;
  transform: translateX(-2px);
}

.logo-marque-mobile {
  text-decoration: none;
  font-size: 23px;
  font-weight: 900;
  letter-spacing: -0.5px;
  text-align: center;
  justify-self: center;
}

.espaceur-retour {
  width: 42px;
  height: 42px;
}

.logo-texte-noir {
  color: #111827;
}

.logo-texte-orange {
  color: #ff4820;
}

/* ==========================================================================
   BARRE RETOUR DESKTOP (AU-DESSUS DU FORMULAIRE)
   ========================================================================== */
.barre-retour-desktop {
  display: none;
}

@media (min-width: 768px) {
  .barre-retour-desktop {
    display: flex;
    justify-content: flex-start;
    padding-left: 2px;
  }

  .bouton-retour-desktop {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: none;
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 8px;
    transition: all 0.2s ease;
  }

  .bouton-retour-desktop:hover {
    color: #111827;
    background-color: rgba(226, 232, 240, 0.5);
    transform: translateX(-2px);
  }
}

/* ==========================================================================
   CARTE PRINCIPALE DE CONNEXION
   ========================================================================== */
.carte-connexion {
  background-color: #ffffff;
  border-radius: 28px;
  padding: 34px 28px;
  box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.035),
              0 2px 8px -2px rgba(15, 23, 42, 0.014);
  border: 1px solid rgba(226, 232, 240, 0.8);
  display: flex;
  flex-direction: column;
  gap: 22px;
  box-sizing: border-box;
}

.bloc-titre {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.titre-principal {
  font-size: 26px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.6px;
  margin: 0;
}

.sous-titre {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.45;
}

/* ==========================================================================
   ALERTES DE RETOUR (SUCCÈS / ERREUR)
   ========================================================================== */
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
  animation: apparaitreMessage 0.25s ease-out;
}

.alerte-succes svg {
  flex-shrink: 0;
  color: #10b981;
}

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
  animation: apparaitreMessage 0.25s ease-out;
}

.alerte-erreur svg {
  flex-shrink: 0;
  color: #ef4444;
}

.conteneur-texte-erreur {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.lien-activer-compte {
  color: #ff4d2d;
  font-weight: 700;
  font-size: 13px;
  text-decoration: underline;
  cursor: pointer;
  width: fit-content;
  transition: opacity 0.2s ease;
}

.lien-activer-compte:hover {
  opacity: 0.85;
}

@keyframes apparaitreMessage {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ==========================================================================
   CHAMPS DE FORMULAIRE & LABELS
   ========================================================================== */
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

.entete-label-champ {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label-champ {
  font-size: 13.5px;
  font-weight: 600;
  color: #334155;
}

.etoile-requise {
  color: #ef4444;
}

.lien-oubli {
  font-size: 12.5px;
  font-weight: 600;
  color: #ff4820;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.lien-oubli:hover {
  opacity: 0.8;
  text-decoration: underline;
}

/* ==========================================================================
   INPUTS DE SAISIE AVEC ICÔNE & FOCUS GLOW
   ========================================================================== */
.conteneur-input {
  display: flex;
  align-items: center;
  background-color: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  padding: 0 14px;
  height: 50px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
}

.conteneur-input:focus-within {
  background-color: #ffffff;
  border-color: #ff4820;
  box-shadow: 0 0 0 3.5px rgba(255, 72, 32, 0.07);
}

.conteneur-input.input-invalide {
  border-color: #ef4444;
  background-color: #fffafb;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.06);
}

.icone-champ {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  margin-right: 10px;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.conteneur-input:focus-within .icone-champ {
  color: #ff4820;
}

.input-saisie {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14.5px;
  color: #0f172a;
  width: 100%;
  font-family: inherit;
}

.input-saisie::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.bouton-oeil {
  background: transparent;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: color 0.2s ease;
}

.bouton-oeil:hover {
  color: #334155;
}

.texte-erreur {
  font-size: 12px;
  color: #ef4444;
  font-weight: 500;
  margin-top: 2px;
}

/* ==========================================================================
   BOUTON DE CONNEXION PRINCIPAL
   ========================================================================== */
.bouton-connexion {
  height: 52px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #ff4820 0%, #ff6239 100%);
  color: #ffffff;
  font-size: 15.5px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.042); /* Ombre très discrète au niveau des champs */
  transition: all 0.2s ease;
  margin-top: 4px;
}

.bouton-connexion:hover:not(:disabled) {
  background: linear-gradient(135deg, #f03f17 0%, #fa552b 100%);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.bouton-connexion:active:not(:disabled) {
  transform: translateY(0);
}

.bouton-connexion:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.contenu-bouton {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chargement-contenu {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner-chargement {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: rotationSpinner 0.8s linear infinite;
}

@keyframes rotationSpinner {
  to {
    transform: rotate(360deg);
  }
}

/* ==========================================================================
   SÉPARATEUR DE SECTION
   ========================================================================== */
.separateur {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 2px 0;
}

.ligne-separateur {
  flex: 1;
  height: 1px;
  background-color: #e2e8f0;
}

.texte-separateur {
  font-size: 11.5px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

/* ==========================================================================
   BOUTON SOCIAL GOOGLE
   ========================================================================== */
.bouton-google {
  height: 48px;
  border-radius: 14px;
  border: 1.5px solid #e2e8f0;
  background-color: #ffffff;
  color: #1e293b;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.2s ease;
}

.bouton-google:hover:not(:disabled) {
  background-color: #f8fafc;
  border-color: #cbd5e1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.021);
}

/* ==========================================================================
   PIED DE CARTE (REDIRECTION INSCRIPTION)
   ========================================================================== */
.pied-carte {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
  color: #64748b;
  padding-top: 4px;
}

.lien-inscription {
  color: #ff4820;
  font-weight: 700;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.lien-inscription:hover {
  opacity: 0.85;
  text-decoration: underline;
}

/* ==========================================================================
   RESPONSIVITÉ & ADAPTATIONS
   ========================================================================== */
@media (max-width: 480px) {
  .page-connexion {
    padding: 16px 12px 32px;
  }

  .carte-connexion {
    padding: 26px 18px;
    border-radius: 24px;
  }

  .titre-principal {
    font-size: 23px;
  }
}
</style>
