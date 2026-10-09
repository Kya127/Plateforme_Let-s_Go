<template>
  <div class="page-inscription">

    <!-- =====================================================
         LOGO DESKTOP : À GAUCHE EN DEHORS DU FORMULAIRE
         (Même niveau et position que sur la page de connexion)
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
    <div class="conteneur-inscription">

      <!-- =====================================================
           EN-TÊTE MOBILE : CHEVRON À GAUCHE & LOGO AU MILIEU
      ====================================================== -->
      <header class="entete-mobile">
        <button
          type="button"
          class="bouton-retour"
          aria-label="Retourner à la page de connexion"
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

        <!-- Espaceur invisible pour un centrage parfait du logo -->
        <div class="espaceur-retour" aria-hidden="true"></div>
      </header>

      <!-- =====================================================
           BARRE RETOUR DESKTOP (AU-DESSUS DE LA CARTE)
      ====================================================== -->
      <div class="barre-retour-desktop">
        <button
          type="button"
          class="bouton-retour-desktop"
          aria-label="Retourner à la page de connexion"
          @click="retourArriere"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          <span>Se connecter</span>
        </button>
      </div>

      <!-- =====================================================
           CARTE PRINCIPALE DU FORMULAIRE D'INSCRIPTION
      ====================================================== -->
      <main class="carte-inscription">
        <!-- Titre et sous-titre de bienvenue -->
        <div class="bloc-titre">
          <h1 class="titre-principal">Créer un compte</h1>
          <p class="sous-titre">Rejoignez la communauté de covoiturage au Sénégal</p>
        </div>

        <!-- Message d'erreur global (ex: email déjà pris ou retour API) -->
        <div v-if="erreurGlobale" class="alerte-erreur" role="alert">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>{{ erreurGlobale }}</span>
        </div>

        <!-- Formulaire d'inscription -->
        <form class="formulaire-champs" novalidate @submit.prevent="gererInscription">

          <!-- Ligne 1 : Prénom et Nom (2 colonnes responsives) -->
          <div class="grille-noms">
            <!-- Champ Prénom -->
            <div class="groupe-champ">
              <label for="prenom" class="label-champ">
                Prénom <span class="etoile-requise">*</span>
              </label>
              <div class="conteneur-input" :class="{ 'input-invalide': erreurs.prenom }">
                <span class="icone-champ" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </span>
                <input
                  id="prenom"
                  v-model.trim="formulaire.prenom"
                  type="text"
                  class="input-saisie"
                  placeholder="Ex: Fatou"
                  autocomplete="given-name"
                  required
                  @blur="validerChamp('prenom')"
                />
              </div>
              <span v-if="erreurs.prenom" class="texte-erreur">{{ erreurs.prenom }}</span>
            </div>

            <!-- Champ Nom -->
            <div class="groupe-champ">
              <label for="nom" class="label-champ">
                Nom <span class="etoile-requise">*</span>
              </label>
              <div class="conteneur-input" :class="{ 'input-invalide': erreurs.nom }">
                <span class="icone-champ" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </span>
                <input
                  id="nom"
                  v-model.trim="formulaire.nom"
                  type="text"
                  class="input-saisie"
                  placeholder="Ex: Ndiaye"
                  autocomplete="family-name"
                  required
                  @blur="validerChamp('nom')"
                />
              </div>
              <span v-if="erreurs.nom" class="texte-erreur">{{ erreurs.nom }}</span>
            </div>
          </div>

          <!-- Ligne 2 : Numéro de téléphone Sénégal (Indicatif fixe + 9 chiffres) -->
          <div class="groupe-champ">
            <label for="telephone" class="label-champ">
              Téléphone mobile <span class="etoile-requise">*</span>
            </label>
            <div class="conteneur-input input-telephone-groupe" :class="{ 'input-invalide': erreurs.telephone }">
              <!-- Indicatif Sénégal 🇸🇳 +221 -->
              <div class="badge-indicatif" aria-label="Indicatif Sénégal">
                <span class="drapeau-sn" aria-hidden="true">🇸🇳</span>
                <span class="texte-indicatif">+221</span>
              </div>
              <span class="separateur-vertical" aria-hidden="true"></span>

              <!-- Champ de saisie : format XX XXX XX XX (12 caractères avec espaces) -->
              <input
                id="telephone"
                v-model="formulaire.telephoneAffiche"
                type="tel"
                inputmode="numeric"
                class="input-saisie input-telephone"
                placeholder="77 123 45 67"
                maxlength="12"
                autocomplete="tel-national"
                required
                @input="surSaisieTelephone"
                @blur="validerChamp('telephone')"
              />
            </div>
            <span v-if="erreurs.telephone" class="texte-erreur">{{ erreurs.telephone }}</span>
          </div>

          <!-- Ligne 3 : Adresse E-mail -->
          <div class="groupe-champ">
            <label for="email" class="label-champ">
              Adresse e-mail <span class="etoile-requise">*</span>
            </label>
            <div class="conteneur-input" :class="{ 'input-invalide': erreurs.email }">
              <span class="icone-champ" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                  <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
                </svg>
              </span>
              <input
                id="email"
                v-model.trim="formulaire.email"
                type="email"
                class="input-saisie"
                placeholder="fatou.ndiaye@exemple.sn"
                autocomplete="email"
                required
                @blur="validerChamp('email')"
              />
            </div>
            <span v-if="erreurs.email" class="texte-erreur">{{ erreurs.email }}</span>
          </div>

          <!-- Ligne 4 : Mot de passe -->
          <div class="groupe-champ">
            <label for="motDePasse" class="label-champ">
              Mot de passe <span class="etoile-requise">*</span>
            </label>
            <div class="conteneur-input" :class="{ 'input-invalide': erreurs.motDePasse }">
              <span class="icone-champ" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </span>
              <input
                id="motDePasse"
                v-model="formulaire.motDePasse"
                :type="motDePasseVisible ? 'text' : 'password'"
                class="input-saisie"
                placeholder="8 caractères minimum"
                autocomplete="new-password"
                required
                @blur="validerChamp('motDePasse')"
              />
              <!-- Bouton Afficher / Masquer mot de passe -->
              <button
                type="button"
                class="bouton-oeil"
                :aria-label="motDePasseVisible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
                @click="motDePasseVisible = !motDePasseVisible"
              >
                <!-- Œil ouvert -->
                <svg v-if="!motDePasseVisible" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <!-- Œil barré -->
                <svg v-else viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
            <span v-if="erreurs.motDePasse" class="texte-erreur">{{ erreurs.motDePasse }}</span>
          </div>

          <!-- Bouton de soumission principal (Ombre très discrète au niveau des champs) -->
          <button
            type="submit"
            class="bouton-inscription"
            :disabled="estEnCoursEnvoi"
          >
            <span v-if="!estEnCoursEnvoi">Créer mon compte</span>
            <span v-else class="chargement-contenu">
              <span class="spinner-chargement"></span>
              Création en cours...
            </span>
          </button>

          <!-- Liens légaux -->
          <p class="texte-conditions">
            En créant un compte, vous acceptez nos
            <a href="#" class="lien-texte">Conditions d'utilisation</a> et notre
            <a href="#" class="lien-texte">Politique de confidentialité</a>.
          </p>
        </form>

        <!-- Redirection vers la page de connexion -->
        <div class="pied-carte">
          <span>Vous avez déjà un compte ?</span>
          <router-link to="/connexion" class="lien-connexion">
            Se connecter
          </router-link>
        </div>
      </main>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'

const router = useRouter()
const authStore = useAuthentificationStore()

/* ==========================================================================
   ÉTATS DU FORMULAIRE ET DES ERREURS
   ========================================================================== */
const motDePasseVisible = ref(false)
const estEnCoursEnvoi = ref(false)
const erreurGlobale = ref('')

const formulaire = reactive({
  prenom: '',
  nom: '',
  telephoneAffiche: '', // Format lisible : "77 123 45 67"
  telephoneBrut: '',    // 9 chiffres exacts : "771234567"
  email: '',
  motDePasse: ''
})

const erreurs = reactive({
  prenom: '',
  nom: '',
  telephone: '',
  email: '',
  motDePasse: ''
})

/* ==========================================================================
   FORMATAGE INTELLIGENT DU NUMÉRO SÉNÉGALAIS (+221 - 9 CHIFFRES)
   ========================================================================== */
const surSaisieTelephone = (e) => {
  let valeur = e.target.value
  let chiffres = valeur.replace(/\D/g, '')

  if (chiffres.startsWith('00221') && chiffres.length > 5) {
    chiffres = chiffres.slice(5)
  } else if (chiffres.startsWith('221') && chiffres.length > 3) {
    chiffres = chiffres.slice(3)
  }

  chiffres = chiffres.slice(0, 9)
  formulaire.telephoneBrut = chiffres

  const groupes = []
  if (chiffres.length > 0) groupes.push(chiffres.slice(0, 2))
  if (chiffres.length > 2) groupes.push(chiffres.slice(2, 5))
  if (chiffres.length > 5) groupes.push(chiffres.slice(5, 7))
  if (chiffres.length > 7) groupes.push(chiffres.slice(7, 9))

  formulaire.telephoneAffiche = groupes.join(' ')

  if (chiffres.length === 9) {
    erreurs.telephone = ''
  }
}

/* ==========================================================================
   VALIDATION UNITAIRE DES CHAMPS
   ========================================================================== */
const validerChamp = (champ) => {
  erreurs[champ] = ''

  if (champ === 'prenom') {
    if (!formulaire.prenom) {
      erreurs.prenom = 'Veuillez saisir votre prénom.'
    } else if (formulaire.prenom.length < 2) {
      erreurs.prenom = 'Le prénom doit contenir au moins 2 caractères.'
    }
  }

  if (champ === 'nom') {
    if (!formulaire.nom) {
      erreurs.nom = 'Veuillez saisir votre nom.'
    } else if (formulaire.nom.length < 2) {
      erreurs.nom = 'Le nom doit contenir au moins 2 caractères.'
    }
  }

  if (champ === 'telephone') {
    const chiffres = formulaire.telephoneBrut
    if (!chiffres) {
      erreurs.telephone = 'Le numéro de téléphone est obligatoire.'
    } else if (chiffres.length !== 9) {
      erreurs.telephone = `Le numéro doit comporter exactement 9 chiffres (${chiffres.length}/9).`
    } else {
      const prefixe = chiffres.slice(0, 2)
      const prefixesValides = ['70', '75', '76', '77', '78', '72', '33']
      if (!prefixesValides.includes(prefixe)) {
        erreurs.telephone = 'Préfixe invalide (utilisez 77, 78, 76, 70, 75).'
      }
    }
  }

  if (champ === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!formulaire.email) {
      erreurs.email = "L'adresse e-mail est obligatoire."
    } else if (!emailRegex.test(formulaire.email)) {
      erreurs.email = 'Veuillez entrer une adresse e-mail valide.'
    }
  }

  if (champ === 'motDePasse') {
    if (!formulaire.motDePasse) {
      erreurs.motDePasse = 'Le mot de passe est obligatoire.'
    } else if (formulaire.motDePasse.length < 8) {
      erreurs.motDePasse = 'Le mot de passe doit comporter au moins 8 caractères.'
    }
  }
}

/* ==========================================================================
   VALIDATION GLOBALE ET SOUMISSION API (DJANGO DRF)
   ========================================================================== */
const validerFormulaire = () => {
  ['prenom', 'nom', 'telephone', 'email', 'motDePasse'].forEach(validerChamp)
  return !Object.values(erreurs).some(Boolean)
}

const gererInscription = async () => {
  erreurGlobale.value = ''

  if (!validerFormulaire()) {
    return
  }

  estEnCoursEnvoi.value = true

  try {
    const numeroInternational = `+221${formulaire.telephoneBrut}`

    const reponse = await authStore.inscrire({
      first_name: formulaire.prenom,
      last_name: formulaire.nom,
      telephone: numeroInternational,
      email: formulaire.email,
      password: formulaire.motDePasse,
    })

    if (reponse.succes) {
      // Sauvegarder l'e-mail du compte pour les flux d'activation et mot de passe oublié
      localStorage.setItem('letsgo_dernier_email', formulaire.email.trim())
      // Redirection immédiate vers la page de vérification par code OTP
      router.push({
        path: '/verification-compte',
        query: { email: formulaire.email },
      })
    } else {
      erreurGlobale.value = reponse.erreur || "Une erreur est survenue lors de l'inscription."
    }
  } catch (err) {
    console.error('Erreur inscription:', err)
    erreurGlobale.value = "Impossible de joindre le serveur. Vérifiez votre connexion."
  } finally {
    estEnCoursEnvoi.value = false
  }
}

const retourArriere = () => {
  router.push('/connexion')
}
</script>

<style scoped>
/* ==========================================================================
   PAGE & MISE EN PAGE RESPONSIVE
   ========================================================================== */
.page-inscription {
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
   (Identique à la page de connexion)
   ========================================================================== */
.entete-desktop {
  display: none;
}

@media (min-width: 768px) {
  /* Page fixe et parfaitement centrée sans scroll sur Desktop */
  .page-inscription {
    height: 100vh;
    max-height: 100vh;
    overflow: hidden;
    padding: 16px;
  }

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
   CONTENEUR CENTRAL DU FORMULAIRE
   ========================================================================== */
.conteneur-inscription {
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
    display: none; /* Masqué sur Desktop car le logo est à gauche hors formulaire */
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
   BARRE RETOUR DESKTOP (AU-DESSUS DE LA CARTE)
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
    font-size: 13.5px;
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
   CARTE PRINCIPALE DU FORMULAIRE (COMPACTE & ÉLÉGANTE SUR DESKTOP)
   ========================================================================== */
.carte-inscription {
  background-color: #ffffff;
  border-radius: 28px;
  padding: 30px 26px;
  box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.035),
              0 2px 8px -2px rgba(15, 23, 42, 0.014);
  border: 1px solid rgba(226, 232, 240, 0.8);
  display: flex;
  flex-direction: column;
  gap: 18px;
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .carte-inscription {
    padding: 24px 28px;
    gap: 14px;
    border-radius: 24px;
  }
}

.bloc-titre {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.titre-principal {
  font-size: 24px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.6px;
  margin: 0;
}

.sous-titre {
  font-size: 13.5px;
  color: #64748b;
  margin: 0;
  line-height: 1.35;
}

@media (min-width: 768px) {
  .titre-principal {
    font-size: 22px;
  }
  .sous-titre {
    font-size: 13px;
  }
}

/* Alerte d'erreur globale */
.alerte-erreur {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 10px 12px;
  border-radius: 12px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
}

.alerte-erreur svg {
  flex-shrink: 0;
}

/* ==========================================================================
   CHAMPS DE SAISIE DESIGN & SOIGNÉS
   ========================================================================== */
.formulaire-champs {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

@media (min-width: 768px) {
  .formulaire-champs {
    gap: 10px;
  }
}

.grille-noms {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.groupe-champ {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.label-champ {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  letter-spacing: -0.1px;
}

.etoile-requise {
  color: #ef4444;
}

.conteneur-input {
  display: flex;
  align-items: center;
  background-color: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 13px;
  padding: 0 12px;
  height: 48px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .conteneur-input {
    height: 42px;
    border-radius: 12px;
  }
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
  margin-right: 8px;
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
  font-size: 14px;
  color: #0f172a;
  width: 100%;
  font-family: inherit;
}

.input-saisie::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

/* Champ Téléphone spécifique */
.input-telephone-groupe {
  padding-left: 10px;
}

.badge-indicatif {
  display: flex;
  align-items: center;
  gap: 5px;
  user-select: none;
  flex-shrink: 0;
}

.drapeau-sn {
  font-size: 15px;
  line-height: 1;
}

.texte-indicatif {
  font-size: 13.5px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.2px;
}

.separateur-vertical {
  width: 1px;
  height: 20px;
  background-color: #cbd5e1;
  margin: 0 10px;
  flex-shrink: 0;
}

.input-telephone {
  letter-spacing: 0.3px;
  font-weight: 500;
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
  font-size: 11px;
  font-weight: 600;
  color: #ef4444;
  margin-top: 1px;
}

/* ==========================================================================
   BOUTON SOUMETTRE (OMBRE TRÈS DISCRÈTE AU MÊME NIVEAU QUE LES CHAMPS)
   ========================================================================== */
.bouton-inscription {
  margin-top: 4px;
  width: 100%;
  height: 48px;
  background-color: #ff4820;
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.042); /* Ombre très discrète */
  transition: all 0.2s ease;
}

@media (min-width: 768px) {
  .bouton-inscription {
    height: 44px;
    font-size: 14.5px;
    margin-top: 2px;
  }
}

.bouton-inscription:hover:not(:disabled) {
  background-color: #e63e18;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.bouton-inscription:active:not(:disabled) {
  transform: translateY(0);
}

.bouton-inscription:disabled {
  opacity: 0.75;
  cursor: not-allowed;
}

.chargement-contenu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner-chargement {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
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
   CONDITIONS LÉGALES & PIED DE PAGE
   ========================================================================== */
.texte-conditions {
  font-size: 11px;
  color: #94a3b8;
  line-height: 1.35;
  margin: 0;
  text-align: center;
}

.lien-texte {
  color: #64748b;
  text-decoration: underline;
}

.pied-carte {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13.5px;
  color: #64748b;
  padding-top: 0;
}

.lien-connexion {
  color: #ff4820;
  font-weight: 700;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.lien-connexion:hover {
  opacity: 0.85;
  text-decoration: underline;
}

/* ==========================================================================
   RESPONSIVITÉ PETITS ÉCRANS MOBILE
   ========================================================================== */
@media (max-width: 480px) {
  .page-inscription {
    padding: 16px 12px 32px;
  }

  .carte-inscription {
    padding: 24px 18px;
    border-radius: 24px;
    gap: 16px;
  }

  .grille-noms {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}
</style>