<template>
  <div class="page-mon-profil">
    <!-- Barre de navigation supérieure simplifiée -->
    <header class="entete-page-profil">
      <div class="conteneur-entete">
        <button
          type="button"
          class="bouton-retour-nav"
          :aria-label="estAdmin ? 'Retour à l\'administration' : 'Retour à l\'accueil'"
          @click="retourAccueil"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          <span>{{ estAdmin ? 'Administration' : 'Accueil' }}</span>
        </button>

        <h1 class="titre-page-profil">Mon profil</h1>

        <div class="espaceur-droite"></div>
      </div>
    </header>

    <main class="conteneur-principal-profil">

      <!-- ========================================================
           1. CARTE HERO : IDENTITÉ & AVATAR AVEC CRAYON SUSPENDU
      ========================================================= -->
      <section class="carte-hero-profil">
        <div class="zone-avatar-hero">
          <!-- Avatar avec le crayon suspendu/accroché au bord -->
          <div class="enveloppe-avatar-crayon">
            <img
              v-if="avatarUrl"
              :src="avatarUrl"
              :alt="nomComplet"
              class="avatar-hero-img"
              @error="erreurChargementAvatar"
            />
            <div v-else class="avatar-hero-initiales">
              {{ initiales }}
            </div>

            <!-- Icône crayon pendue au près du rond d'initiales -->
            <button
              type="button"
              class="crayon-pendu-avatar"
              title="Modifier ou compléter mon profil"
              aria-label="Modifier ou compléter mon profil"
              @click="allerAModifierProfil"
            >
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
              </svg>
            </button>
          </div>

          <div class="infos-hero-texte">
            <div class="ligne-nom-badge">
              <div class="nom-et-badge-verifie">
                <h2 class="nom-utilisateur-hero">{{ nomComplet }}</h2>
                <BadgeConducteurVerifie v-if="utilisateur.estConducteurVerifie" :taille="24" />
              </div>
              <span
                v-if="estAdmin"
                class="badge-statut-hero badge-admin"
              >
                Administrateur
              </span>
              <span
                v-else-if="!utilisateur.estConducteurVerifie"
                class="badge-statut-hero badge-passager"
              >
                Passager
              </span>
            </div>
            <!-- <p class="email-utilisateur-hero">{{ utilisateur.email || 'Email non renseigné' }}</p> -->
          </div>
        </div>

        <!-- Bouton d'action Modifier -->
        <!-- <button
          type="button"
          class="bouton-modifier-action"
          @click="allerAModifierProfil"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
          </svg>
          <span>Modifier le profil</span>
        </button> -->
      </section>


      <!-- ========================================================
           2. ALERTE REFUS DE DEMANDE CONDUCTEUR & RE-SOUMISSION
      ========================================================= -->
      <section v-if="estDemandeRefusee" class="carte-alerte-refus" role="alert">
        <div class="entete-alerte-refus">
          <div class="icone-alerte-boite">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#DC2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </div>
          <div class="texte-alerte-refus">
            <h3 class="titre-alerte-refus">Votre demande conducteur n'a pas été validée</h3>
            <p v-if="motifRejet" class="motif-alerte-refus">
              <strong>Motif du refus :</strong> {{ motifRejet }}
            </p>
            <p v-else class="motif-alerte-refus">
              Certaines pièces de votre dossier n'étaient pas conformes aux critères de vérification.
            </p>
          </div>
        </div>

        <div class="action-alerte-refus">
          <button
            type="button"
            class="bouton-nouvelle-demande"
            @click="lancerNouvelleDemande"
          >
            <span>Faire une nouvelle demande</span>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </button>
        </div>
      </section>

      <!-- Invitation pour un passager simple sans dossier (masquée pour admin) -->
      <section v-else-if="!estAdmin && !utilisateur.estConducteurVerifie && !dossierEnAttente" class="carte-invitation-conducteur">
        <div class="contenu-invitation">
          <div class="texte-invitation">
            <h3 class="titre-invitation">Vous souhaitez proposer des trajets ?</h3>
            <p class="description-invitation">
              Devenez conducteur vérifié sur Let's Go en quelques étapes simples pour partager vos frais de déplacement.
            </p>
          </div>
          <button
            type="button"
            class="bouton-devenir-conducteur-invitation"
            @click="lancerNouvelleDemande"
          >
            Devenir conducteur
          </button>
        </div>
      </section>

      <!-- Message si dossier en attente de vérification -->
      <section v-else-if="dossierEnAttente" class="carte-dossier-attente">
        <div class="icone-attente-boite">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </div>
        <div class="texte-attente">
          <h4 class="titre-attente">Dossier en cours d'examen</h4>
          <p class="description-attente">Vos pièces justificatives sont actuellement en cours de vérification par notre équipe.</p>
        </div>
      </section>


      <!-- ========================================================
           3. SECTION INFORMATIONS PERSONNELLES (READ-ONLY)
      ========================================================= -->
      <section class="carte-section-profil">
        <div class="entete-section-profil">
          <div class="titre-section-groupe">
            <span class="sous-titre-section">COORDONNÉES</span>
            <h3 class="titre-section">Informations personnelles</h3>
          </div>
        </div>

        <div class="grille-donnees-profil">
          <!-- Prénom -->
          <div class="item-donnee-profil">
            <span class="libelle-donnee">Prénom</span>
            <span class="valeur-donnee">{{ utilisateur.prenom || '—' }}</span>
          </div>

          <!-- Nom -->
          <div class="item-donnee-profil">
            <span class="libelle-donnee">Nom de famille</span>
            <span class="valeur-donnee">{{ utilisateur.nom || '—' }}</span>
          </div>

          <!-- Téléphone -->
          <div class="item-donnee-profil">
            <span class="libelle-donnee">Numéro de téléphone</span>
            <span class="valeur-donnee">{{ utilisateur.telephone || 'Non renseigné' }}</span>
          </div>

          <!-- Adresse de résidence -->
          <div class="item-donnee-profil">
            <span class="libelle-donnee">Adresse de résidence</span>
            <span class="valeur-donnee">{{ utilisateur.adresse || 'Non renseignée' }}</span>
          </div>

          <!-- Adresse email -->
          <div class="item-donnee-profil pleine-largeur">
            <span class="libelle-donnee">Adresse e-mail</span>
            <span class="valeur-donnee">{{ utilisateur.email || '—' }}</span>
          </div>
        </div>
      </section>


      <!-- ========================================================
           4. SECTION DOCUMENTS UPLOADÉS (CONSULTATION ÉPURÉE)
      ========================================================= -->
      <section class="carte-section-profil">
        <div class="entete-section-profil">
          <div class="titre-section-groupe">
            <span class="sous-titre-section">PIÈCES JUSTIFICATIVES</span>
            <h3 class="titre-section">Documents téléchargés</h3>
          </div>
        </div>

        <div v-if="aDesDocuments" class="bloc-documents-liste">

          <!-- 4.1 Papiers administratifs -->
          <div class="sous-groupe-documents">
            <h4 class="intitule-sous-groupe">Papiers administratifs</h4>
            <div class="grille-documents-fiches">

              <!-- Permis de conduire -->
              <div class="carte-document-apercu">
                <div class="icone-type-doc">
                  <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#64748B" stroke-width="2">
                    <rect x="3" y="4" width="18" height="16" rx="2"></rect>
                    <line x1="7" y1="8" x2="17" y2="8"></line>
                    <line x1="7" y1="12" x2="13" y2="12"></line>
                    <circle cx="16" cy="14" r="2"></circle>
                  </svg>
                </div>
                <div class="details-doc-apercu">
                  <span class="nom-doc">Permis de conduire</span>
                  <span class="statut-doc-texte">
                    {{ documents.permis_conduire ? 'Téléchargé' : 'Non fourni' }}
                  </span>
                </div>
                <button
                  v-if="documents.permis_conduire"
                  type="button"
                  class="bouton-voir-doc"
                  title="Voir le permis"
                  @click="ouvrirVisionneuse(documents.permis_conduire, 'Permis de conduire')"
                >
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2">
                    <path d="M12 2s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <span>Voir</span>
                </button>
              </div>

              <!-- Certificat d'assurance -->
              <div class="carte-document-apercu">
                <div class="icone-type-doc">
                  <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#64748B" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  </svg>
                </div>
                <div class="details-doc-apercu">
                  <span class="nom-doc">Attestation d'assurance</span>
                  <span class="statut-doc-texte">
                    {{ documents.assurance ? 'Téléchargé' : 'Non fournie' }}
                  </span>
                </div>
                <button
                  v-if="documents.assurance"
                  type="button"
                  class="bouton-voir-doc"
                  title="Voir l'assurance"
                  @click="ouvrirVisionneuse(documents.assurance, 'Attestation d\'assurance')"
                >
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2">
                    <path d="M12 2s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <span>Voir</span>
                </button>
              </div>

            </div>
          </div>

          <!-- 4.2 Documents de la voiture -->
          <div class="sous-groupe-documents">
            <h4 class="intitule-sous-groupe">Documents et visuels du véhicule</h4>
            <div class="grille-documents-fiches">

              <!-- Carte grise -->
              <div class="carte-document-apercu">
                <div class="icone-type-doc">
                  <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#64748B" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                  </svg>
                </div>
                <div class="details-doc-apercu">
                  <span class="nom-doc">Carte grise du véhicule</span>
                  <span class="statut-doc-texte">
                    {{ documents.carte_grise ? 'Téléchargé' : 'Non fournie' }}
                  </span>
                </div>
                <button
                  v-if="documents.carte_grise"
                  type="button"
                  class="bouton-voir-doc"
                  title="Voir la carte grise"
                  @click="ouvrirVisionneuse(documents.carte_grise, 'Carte grise du véhicule')"
                >
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2">
                    <path d="M12 2s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <span>Voir</span>
                </button>
              </div>

              <!-- Photo du véhicule -->
              <div class="carte-document-apercu">
                <div class="icone-type-doc">
                  <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#64748B" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                  </svg>
                </div>
                <div class="details-doc-apercu">
                  <span class="nom-doc">Photo du véhicule</span>
                  <span class="statut-doc-texte">
                    {{ documents.photo_vehicule || premierVehicule?.photo_voiture ? 'Téléchargée' : 'Non fournie' }}
                  </span>
                </div>
                <button
                  v-if="documents.photo_vehicule || premierVehicule?.photo_voiture"
                  type="button"
                  class="bouton-voir-doc"
                  title="Voir la photo du véhicule"
                  @click="ouvrirVisionneuse(documents.photo_vehicule || premierVehicule.photo_voiture, 'Photo du véhicule')"
                >
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2">
                    <path d="M12 2s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <span>Voir</span>
                </button>
              </div>

            </div>
          </div>

          <!-- Fiche récapitulative du véhicule enregistré (si présent) -->
          <div v-if="premierVehicule" class="carte-vehicule-resume">
            <div class="vehicule-resume-infos">
              <span class="libelle-vehicule-tag">VÉHICULE ASSOCIÉ</span>
              <h5 class="modele-vehicule">
                {{ premierVehicule.marque_voiture }} {{ premierVehicule.model_voiture }}
              </h5>
              <div class="meta-vehicule-ligne">
                <span class="plaque-badge">{{ premierVehicule.plaque }}</span>
                <span class="places-texte">{{ premierVehicule.nombres_de_places }} places</span>
                <span v-if="premierVehicule.couleur" class="couleur-texte">• {{ premierVehicule.couleur }}</span>
                <span v-if="premierVehicule.est_climatisee" class="clim-texte">• Climatisé</span>
              </div>
            </div>
          </div>

        </div>

        <!-- Aucun document téléversé -->
        <div v-else class="etat-aucun-document">
          <div class="icone-vide-cercle">
            <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#94A3B8" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <p class="texte-vide-docs">Aucun document n'a encore été téléversé sur votre compte.</p>
        </div>
      </section>

    </main>

    <!-- ========================================================
         5. MODALE DE VISUALISATION D'UN DOCUMENT / PLEIN ÉCRAN
    ========================================================= -->
    <Transition name="fondu-modale">
      <div v-if="documentAffiche" class="fond-sombre-visionneuse" @click.self="fermerVisionneuse">
        <div class="boite-visionneuse">
          <div class="entete-visionneuse">
            <h4 class="titre-visionneuse">{{ titreDocumentAffiche }}</h4>
            <button
              type="button"
              class="bouton-fermer-visionneuse"
              aria-label="Fermer la prévisualisation"
              @click="fermerVisionneuse"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="corps-visionneuse">
            <img
              v-if="estImage(documentAffiche)"
              :src="documentAffiche"
              :alt="titreDocumentAffiche"
              class="image-plein-ecran-visionneuse"
            />
            <div v-else class="fichier-telechargeable-boite">
              <p>Ce document est disponible au format externe.</p>
              <a
                :href="documentAffiche"
                target="_blank"
                rel="noopener noreferrer"
                class="bouton-ouvrir-onglet"
              >
                Ouvrir le document dans un nouvel onglet
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import BadgeConducteurVerifie from '@/components/common/BadgeConducteurVerifie.vue'

const router = useRouter()
const storeAuth = useAuthentificationStore()

const utilisateur = computed(() => storeAuth.utilisateur || {})

const nomComplet = computed(() => {
  const u = utilisateur.value
  const prenom = (u.prenom || '').trim()
  const nom = (u.nom || '').trim()
  return `${prenom} ${nom}`.trim() || u.nomComplet || u.email || 'Utilisateur'
})

const initiales = computed(() => {
  const u = utilisateur.value
  const prenom = (u.prenom || '').trim()
  const nom = (u.nom || '').trim()
  const p = prenom ? prenom.charAt(0).toUpperCase() : ''
  const n = nom ? nom.charAt(0).toUpperCase() : ''
  return `${p}${n}` || 'LG'
})

const avatarUrl = computed(() => {
  return utilisateur.value.photoUrl || null
})

function erreurChargementAvatar(e) {
  // Masque l'image si erreur et bascule sur les initiales
  e.target.style.display = 'none'
}

// Données documents & véhicules
const documents = computed(() => utilisateur.value.documents || null)
const voitures = computed(() => utilisateur.value.voitures || [])
const premierVehicule = computed(() => {
  return voitures.value && voitures.value.length > 0 ? voitures.value[0] : null
})

const aDesDocuments = computed(() => {
  const d = documents.value
  const v = premierVehicule.value
  return !!(d?.permis_conduire || d?.carte_grise || d?.assurance || d?.photo_vehicule || v)
})

// Détection du refus de la demande conducteur
const estDemandeRefusee = computed(() => {
  const docStatus = documents.value?.status
  return docStatus === 'REJECTED' || docStatus === 'REJETE'
})

const motifRejet = computed(() => {
  return documents.value?.motif_rejet || ''
})

const dossierEnAttente = computed(() => {
  const docStatus = documents.value?.status
  return docStatus === 'PENDING' || docStatus === 'EN_ATTENTE'
})

// Détection du rôle Administrateur
const estAdmin = computed(() => {
  const role = (utilisateur.value?.role || storeAuth.utilisateur?.role || '').toUpperCase()
  return role === 'ADMINISTRATEUR' || role === 'ADMIN' || storeAuth.estAdmin
})

// Navigation
function retourAccueil() {
  if (estAdmin.value) {
    router.push('/admin')
  } else {
    router.push('/accueil')
  }
}

function allerAModifierProfil() {
  router.push('/profil/modifier')
}

function lancerNouvelleDemande() {
  // Nettoyer d'éventuelles données résiduelles de l'onboarding pour repartir d'un dossier propre
  try {
    sessionStorage.removeItem('letsgo_onboarding_infos_perso')
    sessionStorage.removeItem('letsgo_onboarding_vehicule')
    sessionStorage.removeItem('letsgo_onboarding_documents')
  } catch (e) {
    console.warn('Nettoyage sessionStorage:', e)
  }

  // Redirection directe vers l'étape 1 du formulaire Devenir Conducteur
  router.push('/conducteur/infos-personnelles')
}

// Visionneuse de document
const documentAffiche = ref(null)
const titreDocumentAffiche = ref('')

function ouvrirVisionneuse(url, titre) {
  if (!url) return
  documentAffiche.value = url
  titreDocumentAffiche.value = titre || 'Document'
}

function fermerVisionneuse() {
  documentAffiche.value = null
  titreDocumentAffiche.value = ''
}

function estImage(url) {
  if (!url) return false
  const clean = url.split('?')[0].toLowerCase()
  return (
    clean.endsWith('.jpg') ||
    clean.endsWith('.jpeg') ||
    clean.endsWith('.png') ||
    clean.endsWith('.webp') ||
    clean.endsWith('.gif') ||
    clean.startsWith('data:image/')
  )
}

onMounted(async () => {
  // Rafraîchir les informations à jour depuis l'API backend
  await storeAuth.rafraichirProfil()
})
</script>

<style scoped>
/* ========================================================
   DESIGN SYSTEM LET'S GO (PUR, SANS OMBRES, ZERO IA FLUFF)
   ======================================================== */
.page-mon-profil {
  min-height: 100vh;
  background-color: #F8FAFC;
  color: #111627;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  padding-bottom: 60px;
}

/* En-tête haut de page */
.entete-page-profil {
  background-color: #FFFFFF;
  border-bottom: 1px solid #E2E8F0;
  position: sticky;
  top: 0;
  z-index: 50;
}

.conteneur-entete {
  max-width: 900px;
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

.titre-page-profil {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0;
  letter-spacing: -0.01em;
}

.espaceur-droite {
  width: 78px;
}

/* Conteneur principal */
.conteneur-principal-profil {
  max-width: 900px;
  margin: 24px auto 0;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================================
   CARTE HERO IDENTITÉ & AVATAR
   ======================================================== */
.carte-hero-profil {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 24px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: none !important;
}

.zone-avatar-hero {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* Enveloppe pour accrocher le crayon suspendu */
.enveloppe-avatar-crayon {
  position: relative;
  width: 76px;
  height: 76px;
  flex-shrink: 0;
}

.avatar-hero-img {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #E2E8F0;
}

.avatar-hero-initiales {
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

/* Crayon pendu auprès du rond d'initiales */
.crayon-pendu-avatar {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #FFFFFF;
  color: #FF4D2D;
  border: 1px solid #FF4D2D;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  box-shadow: none !important;
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.crayon-pendu-avatar:hover {
  background-color: #e03e1f;
  transform: scale(1.12);
  color: #FFFFFF;
  border: 2px solid #FFFFFF;
}

.crayon-pendu-avatar:active {
  transform: scale(0.95);
}

.infos-hero-texte {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ligne-nom-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.nom-et-badge-verifie {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.nom-utilisateur-hero {
  font-size: 22px;
  font-weight: 800;
  color: #111627;
  margin: 0;
  line-height: 1.2;
}

.badge-statut-hero {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 9999px;
  border: 1px solid transparent;
}

.badge-conducteur {
  background-color: #ECFDF5;
  color: #059669;
  border-color: #A7F3D0;
}

.badge-passager {
  background-color: #F1F5F9;
  color: #475569;
  border-color: #CBD5E1;
}

.badge-admin {
  background-color: #111627;
  color: #ffffff;
  border-color: #111627;
}

.email-utilisateur-hero {
  font-size: 14px;
  color: #64748B;
  margin: 0;
  font-weight: 500;
}

.bouton-modifier-action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background-color: #FFFFFF;
  color: #111627;
  border: 1px solid #CBD5E1;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: none !important;
  flex-shrink: 0;
}

.bouton-modifier-action:hover {
  background-color: #F8FAFC;
  border-color: #94A3B8;
}

/* ========================================================
   ALERTES & STATUT DEMANDE CONDUCTEUR
   ======================================================== */
.carte-alerte-refus {
  background: #FEF2F2;
  border: 1px solid #FCA5A5;
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: none !important;
}

.entete-alerte-refus {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.icone-alerte-boite {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #FEE2E2;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.titre-alerte-refus {
  font-size: 16px;
  font-weight: 800;
  color: #991B1B;
  margin: 0 0 6px 0;
}

.motif-alerte-refus {
  font-size: 14px;
  color: #7F1D1D;
  margin: 0;
  line-height: 1.45;
}

.bouton-nouvelle-demande {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #FF4D2D;
  color: #FFFFFF;
  border: none;
  border-radius: 12px;
  padding: 11px 20px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
  white-space: nowrap;
  box-shadow: none !important;
}

.bouton-nouvelle-demande:hover {
  background: #e03e1f;
}

/* Invitation conducteur */
.carte-invitation-conducteur {
  background: #FFFFFF;
  border: 1px dashed #CBD5E1;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: none !important;
}

.contenu-invitation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.titre-invitation {
  font-size: 15px;
  font-weight: 700;
  color: #111627;
  margin: 0 0 4px 0;
}

.description-invitation {
  font-size: 13.5px;
  color: #64748B;
  margin: 0;
}

.bouton-devenir-conducteur-invitation {
  background: #111627;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
  white-space: nowrap;
  box-shadow: none !important;
}

.bouton-devenir-conducteur-invitation:hover {
  background: #1e2640;
}

/* Attente */
.carte-dossier-attente {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: none !important;
}

.icone-attente-boite {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #FEF3C7;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.titre-attente {
  font-size: 14.5px;
  font-weight: 700;
  color: #92400E;
  margin: 0 0 2px 0;
}

.description-attente {
  font-size: 13px;
  color: #B45309;
  margin: 0;
}

/* ========================================================
   SECTIONS GÉNÉRIQUES DU PROFIL (INFORMATIONS & DOCUMENTS)
   ======================================================== */
.carte-section-profil {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: none !important;
}

.entete-section-profil {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #F1F5F9;
  padding-bottom: 16px;
}

.titre-section-groupe {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sous-titre-section {
  font-size: 11px;
  font-weight: 800;
  color: #FF4D2D;
  letter-spacing: 0.08em;
}

.titre-section {
  font-size: 15px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

/* Grille des informations personnelles (Read-only) */
.grille-donnees-profil {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.item-donnee-profil {
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #F8FAFC;
  border: 1px solid #EDF2F7;
  border-radius: 12px;
  padding: 14px 16px;
}

.item-donnee-profil.pleine-largeur {
  grid-column: 1 / -1;
}

.libelle-donnee {
  font-size: 12px;
  font-weight: 600;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.valeur-donnee {
  font-size: 15px;
  font-weight: 700;
  color: #111627;
}

/* ========================================================
   DOCUMENTS UPLOADÉS (CONSULTATION ÉPURÉE SANS BADGES)
   ======================================================== */
.bloc-documents-liste {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.sous-groupe-documents {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.intitule-sous-groupe {
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  margin: 0;
}

.grille-documents-fiches {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.carte-document-apercu {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 14px 16px;
}

.icone-type-doc {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #EDF2F7;
  color: #FF4D2D;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.details-doc-apercu {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
}

.nom-doc {
  font-size: 14px;
  font-weight: 700;
  color: #111627;
}

.statut-doc-texte {
  font-size: 12px;
  color:#22C55E;
  font-weight: 500;
}

.bouton-voir-doc {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12.5px;
  font-weight: 700;
  color: #111627;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: none !important;
}

.bouton-voir-doc:hover {
  background: #F1F5F9;
  border-color: #94A3B8;
}

/* Fiche véhicule résumé */
.carte-vehicule-resume {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 16px 20px;
}

.libelle-vehicule-tag {
  font-size: 11px;
  font-weight: 800;
  color: #FF4D2D;
  letter-spacing: 0.05em;
}

.modele-vehicule {
  font-size: 17px;
  font-weight: 800;
  color: #111627;
  margin: 4px 0 8px 0;
}

.meta-vehicule-ligne {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.plaque-badge {
  background: #111627;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
  letter-spacing: 0.04em;
}

.places-texte,
.couleur-texte,
.clim-texte {
  font-size: 13px;
  color: #64748B;
  font-weight: 600;
}

/* État vide */
.etat-aucun-document {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 20px;
  text-align: center;
  gap: 10px;
}

.icone-vide-cercle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #F1F5F9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.texte-vide-docs {
  font-size: 14px;
  color: #64748B;
  margin: 0;
}

/* ========================================================
   MODALE VISIONNEUSE DOCUMENT / PLEIN ÉCRAN
   ======================================================== */
.fond-sombre-visionneuse {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 20px;
  backdrop-filter: blur(2px);
}

.boite-visionneuse {
  background: #FFFFFF;
  border-radius: 16px;
  max-width: 750px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #E2E8F0;
  box-shadow: none !important;
}

.entete-visionneuse {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #E2E8F0;
}

.titre-visionneuse {
  font-size: 16px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

.bouton-fermer-visionneuse {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #64748B;
  display: flex;
  padding: 4px;
  border-radius: 6px;
  transition: color 0.15s ease;
}

.bouton-fermer-visionneuse:hover {
  color: #111627;
}

.corps-visionneuse {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #F8FAFC;
}

.image-plein-ecran-visionneuse {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
}

.fichier-telechargeable-boite {
  text-align: center;
  padding: 30px;
}

.bouton-ouvrir-onglet {
  display: inline-block;
  margin-top: 10px;
  background: #FF4D2D;
  color: #FFFFFF;
  text-decoration: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
}

/* Animations */
.fondu-modale-enter-active,
.fondu-modale-leave-active {
  transition: opacity 0.2s ease;
}

.fondu-modale-enter-from,
.fondu-modale-leave-to {
  opacity: 0;
}

/* ========================================================
   RESPONSIVE (MOBILE & TABLETTE)
   ======================================================== */
@media (max-width: 768px) {
  .carte-hero-profil {
    flex-direction: column;
    align-items: flex-start;
    padding: 20px;
  }

  .bouton-modifier-action {
    width: 100%;
    justify-content: center;
  }

  .carte-alerte-refus {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-alerte-refus {
    width: 100%;
  }

  .bouton-nouvelle-demande {
    width: 100%;
    justify-content: center;
  }

  .contenu-invitation {
    flex-direction: column;
    align-items: flex-start;
  }

  .bouton-devenir-conducteur-invitation {
    width: 100%;
    text-align: center;
  }

  .grille-donnees-profil {
    grid-template-columns: 1fr;
  }

  .grille-documents-fiches {
    grid-template-columns: 1fr;
  }

  .carte-section-profil {
    padding: 20px;
  }
}
</style>
