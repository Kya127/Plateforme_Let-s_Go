<template>
  <div class="page-modifier-profil">
    <!-- Barre de navigation supérieure -->
    <header class="entete-modifier-nav">
      <div class="conteneur-entete">
        <button
          type="button"
          class="bouton-retour-nav"
          aria-label="Retour au profil"
          @click="annulerModifications"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          <span>Annuler</span>
        </button>

        <h1 class="titre-nav">Mon profil</h1>

        <div class="espaceur-droite"></div>
      </div>
    </header>

    <main class="conteneur-central">
      <div class="carte-formulaire-edition">

        <!-- En-tête de section -->
        <div class="en-tete-carte">
          <!-- <h2 class="titre-formulaire">Informations personnelles</h2> -->
          <!-- <p class="description-formulaire">
            Modifiez vos coordonnées. Ces informations permettent aux autres membres de la communauté de vous identifier.
          </p> -->
        </div>

        <!-- Notification d'erreur éventuelle -->
        <div v-if="messageErreur" class="alerte-erreur-edition" role="alert">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>{{ messageErreur }}</span>
        </div>

        <!-- Formulaire de modification -->
        <form class="formulaire-edition" novalidate @submit.prevent="enregistrerModifications">

          <!-- SECTION 1 : MODIFICATION PHOTO DE PROFIL -->
          <div class="zone-photo-upload">
            <div class="enveloppe-avatar-apercu">
              <img
                v-if="apercuPhoto || avatarActuel"
                :src="apercuPhoto || avatarActuel"
                alt="Aperçu photo de profil"
                class="photo-profil-apercu"
                @error="gererErreurPhoto"
              />
              <div v-else class="initiales-photo-apercu">
                {{ initialesCalculees }}
              </div>

              <!-- Input fichier masqué -->
              <input
                ref="refInputFichier"
                type="file"
                accept="image/png, image/jpeg, image/webp"
                class="input-fichier-cache"
                @change="surChangementFichierPhoto"
              />
            </div>

            <div class="actions-photo-texte">
              <button
                type="button"
                class="bouton-changer-photo"
                @click="declencherSelectionPhoto"
              >
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>{{ apercuPhoto ? 'Remplacer la photo' : 'Ajouter la photo' }}</span>
              </button>
              <!-- <span class="indice-format-photo">Format JPG, PNG ou WEBP (max. 5 Mo)</span> -->
            </div>
          </div>

          <div class="separateur-ligne"></div>

          <!-- SECTION 2 : CHAMPS TEXTES (PRÉNOM & NOM) -->
          <div class="grille-deux-colonnes">
            <!-- Prénom -->
            <div class="groupe-saisie">
              <label for="prenom" class="label-champ">
                Prénom <span class="etoile-obligatoire">*</span>
              </label>
              <div class="boite-input" :class="{ 'input-invalide': erreurs.prenom }">
                <input
                  id="prenom"
                  v-model.trim="form.prenom"
                  type="text"
                  class="champ-input"
                  placeholder="Ex: Racky"
                  required
                />
              </div>
              <span v-if="erreurs.prenom" class="message-erreur">{{ erreurs.prenom }}</span>
            </div>

            <!-- Nom -->
            <div class="groupe-saisie">
              <label for="nom" class="label-champ">
                Nom <span class="etoile-obligatoire">*</span>
              </label>
              <div class="boite-input" :class="{ 'input-invalide': erreurs.nom }">
                <input
                  id="nom"
                  v-model.trim="form.nom"
                  type="text"
                  class="champ-input"
                  placeholder="Ex: Bilal"
                  required
                />
              </div>
              <span v-if="erreurs.nom" class="message-erreur">{{ erreurs.nom }}</span>
            </div>
          </div>

          <!-- SECTION 3 : TÉLÉPHONE SÉNÉGAL -->
          <div class="groupe-saisie">
            <label for="telephone" class="label-champ">
              Numéro de téléphone <span class="etoile-obligatoire">*</span>
            </label>
            <div class="boite-input groupe-input-telephone" :class="{ 'input-invalide': erreurs.telephone }">
              <div class="badge-indicatif-sn" aria-label="Indicatif Sénégal">
                <span class="drapeau-sn" aria-hidden="true">🇸🇳</span>
                <span class="texte-indicatif">+221</span>
              </div>
              <span class="separateur-barre" aria-hidden="true"></span>
              <input
                id="telephone"
                v-model="form.telephoneAffiche"
                type="tel"
                inputmode="numeric"
                class="champ-input champ-tel-saisie"
                placeholder="77 123 45 67"
                maxlength="12"
                required
                @input="formaterTelephoneSaisie"
              />
            </div>
            <span v-if="erreurs.telephone" class="message-erreur">{{ erreurs.telephone }}</span>
          </div>

          <!-- SECTION 4 : ADRESSE DE RÉSIDENCE -->
          <div class="groupe-saisie">
            <label for="adresse" class="label-champ">
              Adresse de résidence
            </label>
            <div class="boite-input">
              <span class="icone-champ-adresse" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
              </span>
              <input
                id="adresse"
                v-model.trim="form.adresse"
                type="text"
                class="champ-input champ-avec-icone"
                placeholder="Ex: Mermoz, Dakar"
              />
            </div>
            <span class="indice-champ">Facultatif : Quartier, ville ou adresse habituelle.</span>
          </div>

          <!-- SECTION 5 : BOUTONS ENREGISTRER ET ANNULER -->
          <div class="barre-actions-formulaire">
            <!-- Bouton Annuler -->
            <button
              type="button"
              class="bouton-action-annuler"
              :disabled="enCoursEnregistrement"
              @click="annulerModifications"
            >
              Annuler
            </button>

            <!-- Bouton Enregistrer -->
            <button
              type="submit"
              class="bouton-action-enregistrer"
              :disabled="enCoursEnregistrement"
            >
              <span v-if="!enCoursEnregistrement" class="contenu-btn-enregistrer">
                
                <span>Enregistrer</span>
              </span>
              <span v-else class="contenu-chargement">
                <span class="spinner-chargement"></span>
                <span>Enregistrement...</span>
              </span>
            </button>
          </div>

        </form>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import { serviceAuth } from '@/services/api'

const router = useRouter()
const storeAuth = useAuthentificationStore()

const refInputFichier = ref(null)
const fichierPhotoSelectionne = ref(null)
const apercuPhoto = ref(null)

const enCoursEnregistrement = ref(false)
const messageErreur = ref('')

const form = reactive({
  prenom: '',
  nom: '',
  telephoneAffiche: '',
  adresse: '',
})

const erreurs = reactive({
  prenom: '',
  nom: '',
  telephone: '',
})

const avatarActuel = computed(() => {
  return storeAuth.utilisateur?.photoUrl || null
})

const initialesCalculees = computed(() => {
  const p = (form.prenom || storeAuth.utilisateur?.prenom || '').trim()
  const n = (form.nom || storeAuth.utilisateur?.nom || '').trim()
  const pInitial = p ? p.charAt(0).toUpperCase() : ''
  const nInitial = n ? n.charAt(0).toUpperCase() : ''
  return `${pInitial}${nInitial}` || 'LG'
})

function gererErreurPhoto(e) {
  e.target.style.display = 'none'
}

// Initialisation des données depuis le store
function initialiserChamps() {
  const u = storeAuth.utilisateur || {}
  form.prenom = u.prenom || ''
  form.nom = u.nom || ''
  form.adresse = u.adresse || ''

  // Nettoyage et formatage du numéro existant
  const telBrut = (u.telephone || '').replace(/^\+221/, '').replace(/\s+/g, '')
  if (telBrut) {
    appliquerFormatageTelephone(telBrut)
  } else {
    form.telephoneAffiche = ''
  }
}

// Formatage du numéro de téléphone (XX XXX XX XX)
function appliquerFormatageTelephone(val) {
  const digits = val.replace(/\D/g, '').slice(0, 9)
  let f = ''
  if (digits.length > 0) f = digits.slice(0, 2)
  if (digits.length > 2) f += ' ' + digits.slice(2, 5)
  if (digits.length > 5) f += ' ' + digits.slice(5, 7)
  if (digits.length > 7) f += ' ' + digits.slice(7, 9)
  form.telephoneAffiche = f
}

function formaterTelephoneSaisie() {
  appliquerFormatageTelephone(form.telephoneAffiche)
  if (erreurs.telephone) erreurs.telephone = ''
}

// Gestion de la sélection photo
function declencherSelectionPhoto() {
  if (refInputFichier.value) {
    refInputFichier.value.click()
  }
}

function surChangementFichierPhoto(e) {
  const fichier = e.target.files && e.target.files[0]
  if (!fichier) return

  // Vérification de la taille (max. 5 Mo)
  if (fichier.size > 5 * 1024 * 1024) {
    messageErreur.value = 'La taille de la photo ne doit pas dépasser 5 Mo.'
    return
  }

  fichierPhotoSelectionne.value = fichier
  apercuPhoto.value = URL.createObjectURL(fichier)
  messageErreur.value = ''
}

// Validation des champs
function validerFormulaire() {
  let valide = true
  erreurs.prenom = ''
  erreurs.nom = ''
  erreurs.telephone = ''
  messageErreur.value = ''

  if (!form.prenom.trim()) {
    erreurs.prenom = 'Le prénom est obligatoire.'
    valide = false
  }

  if (!form.nom.trim()) {
    erreurs.nom = 'Le nom de famille est obligatoire.'
    valide = false
  }

  const digitsTel = form.telephoneAffiche.replace(/\D/g, '')
  if (!digitsTel) {
    erreurs.telephone = 'Le numéro de téléphone est obligatoire.'
    valide = false
  } else if (digitsTel.length !== 9) {
    erreurs.telephone = 'Le numéro doit comporter 9 chiffres (ex: 77 123 45 67).'
    valide = false
  }

  return valide
}

// Enregistrement des modifications
async function enregistrerModifications() {
  if (!validerFormulaire()) return

  enCoursEnregistrement.value = true
  messageErreur.value = ''

  try {
    const formData = new FormData()
    formData.append('first_name', form.prenom.trim())
    formData.append('last_name', form.nom.trim())

    const digitsTel = form.telephoneAffiche.replace(/\D/g, '')
    formData.append('telephone', `+221${digitsTel}`)
    formData.append('adresse', (form.adresse || '').trim())

    // Si une nouvelle photo a été choisie
    if (fichierPhotoSelectionne.value) {
      formData.append('photo', fichierPhotoSelectionne.value)
    }

    // Appel API PATCH /auth/profile/
    await serviceAuth.mettreAJourProfil(formData)

    // Synchronisation du profil dans le store Pinia
    await storeAuth.rafraichirProfil()

    // Redirection vers la page de consultation Mon Profil
    router.push('/profil')
  } catch (err) {
    console.error('Erreur mise à jour profil:', err)
    const errData = err.response?.data
    if (errData?.detail) {
      messageErreur.value = errData.detail
    } else if (errData?.telephone) {
      erreurs.telephone = Array.isArray(errData.telephone) ? errData.telephone[0] : String(errData.telephone)
    } else if (typeof errData === 'object' && errData !== null) {
      const firstKey = Object.keys(errData)[0]
      const firstVal = errData[firstKey]
      messageErreur.value = Array.isArray(firstVal) ? firstVal[0] : String(firstVal)
    } else {
      messageErreur.value = 'Une erreur est survenue lors de la mise à jour de votre profil.'
    }
  } finally {
    enCoursEnregistrement.value = false
  }
}

// Annuler et revenir à la page profil
function annulerModifications() {
  router.push('/profil')
}

onMounted(() => {
  initialiserChamps()
})
</script>

<style scoped>
/* ========================================================
   DESIGN SYSTEM LET'S GO (PUR, SANS OMBRES, ZERO FLUFF)
   ======================================================== */
.page-modifier-profil {
  min-height: 100vh;
  background-color: #F8FAFC;
  color: #111627;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  padding-bottom: 60px;
}

/* En-tête haut de page */
.entete-modifier-nav {
  background-color: #FFFFFF;
  border-bottom: 1px solid #E2E8F0;
  position: sticky;
  top: 0;
  z-index: 50;
}

.conteneur-entete {
  max-width: 800px;
  margin: 0 auto;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bouton-retour-nav {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: 0px solid #E2E8F0;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: none !important;
}

.bouton-retour-nav:hover {
  background-color: #F1F5F9;
  color: #111627;
  border-color: #CBD5E1;
}

.titre-nav {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0;
  letter-spacing: -0.01em;
}

.espaceur-droite {
  width: 78px;
}

/* Conteneur formulaire central */
.conteneur-central {
  max-width: 800px;
  margin: 28px auto 0;
  padding: 0 20px;
}

.carte-formulaire-edition {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 32px;
  box-shadow: none !important;
}

.en-tete-carte {
  margin-bottom: 24px;
}

.titre-formulaire {
  font-size: 20px;
  font-weight: 800;
  color: #111627;
  margin: 0 0 6px 0;
}

.description-formulaire {
  font-size: 14px;
  color: #64748B;
  margin: 0;
  line-height: 1.5;
}

/* Alerte d'erreur */
.alerte-erreur-edition {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: #FEF2F2;
  border: 1px solid #FCA5A5;
  color: #991B1B;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 24px;
}

/* Zone Photo Upload */
.zone-photo-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 6px 0 10px 0;
}

.enveloppe-avatar-apercu {
  width: 76px;
  height: 76px;
  position: relative;
  flex-shrink: 0;
}

.photo-profil-apercu {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #E2E8F0;
}

.initiales-photo-apercu {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background-color: #FF4D2D;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 0.05em;
  border: 2px solid #FFFFFF;
}

.input-fichier-cache {
  display: none;
}

.actions-photo-texte {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.bouton-changer-photo {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 20px;
  padding: 8px 14px;
  font-size: 13.5px;
  font-weight: 700;
  color: #111627;
  cursor: pointer;
  transition: all 0.15s ease;
  width: fit-content;
  box-shadow: none !important;
}

.bouton-changer-photo:hover {
  background: #F8FAFC;
  border-color: #94A3B8;
}

.indice-format-photo {
  font-size: 12px;
  color: #94A3B8;
}

.separateur-ligne {
  height: 1px;
  background: #F1F5F9;
  margin: 20px 0 24px 0;
}

/* Formulaire & Champs */
.formulaire-edition {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.grille-deux-colonnes {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.groupe-saisie {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-champ {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
}

.etoile-obligatoire {
  color: #EF4444;
}

.boite-input {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 12px;
  transition: border-color 0.15s ease;
  overflow: hidden;
}

.boite-input:focus-within {
  border-color: #FF4D2D;
}

.boite-input.input-invalide {
  border-color: #EF4444;
}

.champ-input {
  width: 100%;
  padding: 12px 14px;
  font-size: 14.5px;
  color: #111627;
  border: none;
  background: transparent;
  font-family: inherit;
  outline: none;
}

.champ-input::placeholder {
  color: #94A3B8;
}

.icone-champ-adresse {
  padding-left: 14px;
  display: flex;
  align-items: center;
  color: #94A3B8;
}

.champ-avec-icone {
  padding-left: 10px;
}

/* Téléphone spécialisé Sénégal */
.groupe-input-telephone {
  display: flex;
  align-items: center;
}

.badge-indicatif-sn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 12px;
  user-select: none;
}

.drapeau-sn {
  font-size: 17px;
}

.texte-indicatif {
  font-size: 14px;
  font-weight: 700;
  color: #111627;
}

.separateur-barre {
  width: 1px;
  height: 24px;
  background: #E2E8F0;
}

.champ-tel-saisie {
  padding-left: 12px;
  letter-spacing: 0.03em;
}

.message-erreur {
  font-size: 12px;
  font-weight: 600;
  color: #EF4444;
  margin-top: 2px;
}

.indice-champ {
  font-size: 12px;
  color: #94A3B8;
  margin-top: 2px;
}

/* ========================================================
   BARRE ACTIONS : ANNULER & ENREGISTRER
   ======================================================== */
.barre-actions-formulaire {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 16px;
  padding-top: 24px;
  border-top: 1px solid #F1F5F9;
}

.bouton-action-annuler {
  padding: 12px 24px;
  background: #FFFFFF;
  color: #475569;
  border: 1px solid #CBD5E1;
  border-radius: 12px;
  font-size: 14.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: none !important;
}

.bouton-action-annuler:hover:not(:disabled) {
  background: #F1F5F9;
  color: #111627;
  border-color: #94A3B8;
}

.bouton-action-enregistrer {
  padding: 12px 28px;
  background: #FF4D2D;
  color: #FFFFFF;
  border: none;
  border-radius: 12px;
  font-size: 14.5px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: none !important;
}

.bouton-action-enregistrer:hover:not(:disabled) {
  background: #e03e1f;
}

.bouton-action-enregistrer:disabled,
.bouton-action-annuler:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.contenu-btn-enregistrer,
.contenu-chargement {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.spinner-chargement {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: tourner 0.8s linear infinite;
}

@keyframes tourner {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 640px) {
  .carte-formulaire-edition {
    padding: 20px;
  }

  .grille-deux-colonnes {
    grid-template-columns: 1fr;
  }

  .barre-actions-formulaire {
    flex-direction: column-reverse;
    gap: 10px;
  }

  .bouton-action-annuler,
  .bouton-action-enregistrer {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
}
</style>
