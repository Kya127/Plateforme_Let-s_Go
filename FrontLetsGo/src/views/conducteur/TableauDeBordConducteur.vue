<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import { serviceTrajets } from '@/services/api'
import CarteTrajetConducteur from '@/components/conducteur/CarteTrajetConducteur.vue'

const routeur = useRouter()
const storeAuth = useAuthentificationStore()

/* =========================================================
   GESTION DES ONGLETS
========================================================= */
const ongletActif = ref('a-venir')

const onglets = [
  { id: 'a-venir', libelle: 'À venir' },
  { id: 'termines', libelle: 'Terminés' },
  { id: 'annules', libelle: 'Annulés' },
]

function changerOnglet(id) {
  ongletActif.value = id
}

/* =========================================================
   CHARGEMENT DES TRAJETS CONDUCTEUR
========================================================= */
const trajets = ref([])
const chargement = ref(true)

async function chargerTrajets() {
  chargement.value = true
  try {
    const data = await serviceTrajets.mesTrajets()
    trajets.value = Array.isArray(data) ? data : []
  } catch (erreur) {
    console.error('Erreur chargement mes trajets:', erreur)
    trajets.value = []
  } finally {
    chargement.value = false
  }
}

onMounted(() => {
  chargerTrajets()
})

/* =========================================================
   FILTRAGE DES TRAJETS PAR ONGLET
========================================================= */
const trajetsFiltres = computed(() => {
  if (ongletActif.value === 'a-venir') {
    return trajets.value.filter((t) => t.statut === 'PLANIFIE' || t.statut === 'EN_COURS')
  }
  if (ongletActif.value === 'termines') {
    return trajets.value.filter((t) => t.statut === 'TERMINE')
  }
  if (ongletActif.value === 'annules') {
    return trajets.value.filter((t) => t.statut === 'ANNULE')
  }
  return []
})

// Compteur par statut pour les badges d'onglets
const compterTrajets = (id) => {
  if (id === 'a-venir') {
    return trajets.value.filter((t) => t.statut === 'PLANIFIE' || t.statut === 'EN_COURS').length
  }
  if (id === 'termines') {
    return trajets.value.filter((t) => t.statut === 'TERMINE').length
  }
  if (id === 'annules') {
    return trajets.value.filter((t) => t.statut === 'ANNULE').length
  }
  return 0
}

/* =========================================================
   NAVIGATION
========================================================= */
function demarrerPublicationTrajet() {
  if (storeAuth.utilisateur?.estConducteurVerifie) {
    routeur.push('/publier-trajet')
  } else {
    routeur.push('/conducteur/infos-personnelles')
  }
}

function voirDetailTrajet(id) {
  routeur.push({
    name: 'vue-trajet-prevu',
    params: { id },
  })
}

/* =========================================================
   FORMATAGE
========================================================= */
function formaterDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return dateStr
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
  })
}

function formaterHeure(heureStr) {
  if (!heureStr) return ''
  return heureStr.substring(0, 5)
}

function formaterPrix(prix) {
  if (!prix) return '0'
  return Number(prix).toLocaleString('fr-FR')
}
</script>

<template>
  <div class="page-tableau-bord">
    <div class="conteneur-conducteur">
      <!-- En-tête : Salutation & Profil Conducteur -->
      <header class="entete-conducteur">
        <div class="texte-bienvenue">
          <span class="message-salutation">Espace Conducteur</span>
          <h1 class="nom-conducteur">
            Bonjour, {{ storeAuth.utilisateur?.prenom || storeAuth.nomAffiche }}
          </h1>
        </div>

        <div class="actions-profil-conducteur">
          <button
            type="button"
            class="btn-proposer-desktop"
            @click="demarrerPublicationTrajet"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            <span>Proposer un trajet</span>
          </button>

          <!-- Avatar avec pastille en ligne -->
          <div class="enveloppe-avatar" @click="routeur.push('/accueil')" role="button" title="Retour à l'accueil">
            <img
              :src="storeAuth.avatarActif"
              :alt="storeAuth.utilisateur?.nomComplet || 'Conducteur'"
              class="avatar-photo"
            />
            <span class="pastille-en-ligne" title="En ligne"></span>
          </div>
        </div>
      </header>

      <!-- Barre d'onglets (À venir / Terminés / Annulés) -->
      <nav class="barre-onglets" aria-label="Statut des trajets">
        <button
          v-for="onglet in onglets"
          :key="onglet.id"
          type="button"
          :class="['bouton-onglet', { 'est-actif': ongletActif === onglet.id }]"
          @click="changerOnglet(onglet.id)"
        >
          <span>{{ onglet.libelle }}</span>
          <span v-if="compterTrajets(onglet.id) > 0" class="badge-compteur">
            {{ compterTrajets(onglet.id) }}
          </span>
          <span v-if="ongletActif === onglet.id" class="barre-selection"></span>
        </button>
      </nav>

      <!-- Zone centrale : Liste des trajets ou État vide -->
      <main class="zone-contenu">
        <!-- État de chargement discret -->
        <div v-if="chargement" class="zone-chargement">
          <span class="indicateur-spinner"></span>
          <p>Chargement de vos trajets...</p>
        </div>

        <!-- Liste des trajets disponibles dans l'onglet actif -->
        <div v-else-if="trajetsFiltres.length > 0" class="liste-trajets">
          <CarteTrajetConducteur
            v-for="trajet in trajetsFiltres"
            :key="trajet.id"
            :trajet="trajet"
            @voir="voirDetailTrajet"
          />
        </div>

        <!-- État vide si aucun trajet dans l'onglet -->
        <div v-else class="zone-contenu-vide">
          <div class="badge-icone-vide">
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#9CA3AF"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3 3 0 0 0 2 12v4c0 .6.4 1 1 1h2" />
              <circle cx="7" cy="17" r="2" />
              <path d="M9 17h6" />
              <circle cx="17" cy="17" r="2" />
            </svg>
          </div>
          <p class="texte-aucun-trajet">
            Vous n'avez pas de trajets
            {{ ongletActif === 'a-venir' ? 'à venir' : ongletActif === 'termines' ? 'terminés' : 'annulés' }}<br />
            pour le moment.
          </p>
          <button
            v-if="ongletActif === 'a-venir'"
            type="button"
            class="btn-proposer-vide"
            @click="demarrerPublicationTrajet"
          >
            Proposer un trajet
          </button>
        </div>
      </main>

      <!-- Bouton d'action "Proposer un trajet" épuré sans effet d'ombre visible -->
      <footer class="pied-actions-conducteur">
        <button
          type="button"
          class="grand-bouton-proposer"
          @click="demarrerPublicationTrajet"
        >
          <!-- Icône carrée '+' -->
          <div class="carre-icone-plus">
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
          </div>

          <!-- Textes du bouton -->
          <div class="textes-bouton">
            <span class="titre-bouton">Proposer un trajet</span>
            <span class="soustitre-bouton">Partagez vos frais de route</span>
          </div>

          <!-- Chevron droit -->
          <div class="chevron-droit">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.page-tableau-bord {
  min-height: 100vh;
  background-color: var(--color-white, #FFFFFF);
  display: flex;
  justify-content: center;
}

.conteneur-conducteur {
  width: 100%;
  max-width: 520px;
  min-height: 100vh;
  padding: 32px 20px 28px;
  display: flex;
  flex-direction: column;
}

/* En-tête */
.entete-conducteur {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.message-salutation {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary, #6B7280);
  display: block;
  margin-bottom: 2px;
}

.nom-conducteur {
  font-size: 24px;
  font-weight: 800;
  color: var(--color-black, #111827);
  letter-spacing: -0.4px;
  margin: 0;
}

/* Avatar */
.enveloppe-avatar {
  position: relative;
  width: 48px;
  height: 48px;
  cursor: pointer;
  flex-shrink: 0;
}

.avatar-photo {
  width: 100%;
  height: 100%;
  border-radius: 14px;
  object-fit: cover;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.pastille-en-ligne {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #10B981;
  border: 2px solid #FFFFFF;
}

/* Onglets */
.barre-onglets {
  display: flex;
  border-bottom: 1px solid #E5E7EB;
  margin-bottom: 24px;
  gap: 8px;
}

.bouton-onglet {
  position: relative;
  background: transparent;
  border: none;
  font-size: 15px;
  font-weight: 600;
  color: #9CA3AF;
  padding: 10px 14px 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: color 0.15s ease;
}

.bouton-onglet.est-actif {
  color: #111827;
  font-weight: 700;
}

.badge-compteur {
  background-color: #F3F4F6;
  color: #4B5563;
  font-size: 12px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
}

.bouton-onglet.est-actif .badge-compteur {
  background-color: #FFF1EE;
  color: var(--color-brand-accent, #FF4D2D);
}

.barre-selection {
  position: absolute;
  bottom: -1px;
  left: 10px;
  right: 10px;
  height: 3px;
  background-color: var(--color-brand-accent, #FF4D2D);
  border-radius: 3px 3px 0 0;
}

/* Zone contenu */
.zone-contenu {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Indicateur de chargement */
.zone-chargement {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 12px;
  color: #9CA3AF;
  font-size: 14px;
}

.indicateur-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #E5E7EB;
  border-top-color: var(--color-brand-accent, #FF4D2D);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Liste des cartes trajets */
.liste-trajets {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-bottom: 20px;
}

/* Zone vide (Empty State) */
.zone-contenu-vide {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px;
}

.badge-icone-vide {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.texte-aucun-trajet {
  font-size: 14px;
  line-height: 1.5;
  color: #9CA3AF;
  margin: 0;
}

/* Grand Bouton Proposer en bas (Flat, discret, sans ombre lourde) */
.pied-actions-conducteur {
  margin-top: auto;
  padding-top: 16px;
}

.grand-bouton-proposer {
  width: 100%;
  background-color: var(--color-brand-accent, #FF4D2D);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 20px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  box-shadow: none;
  transition: background-color 0.15s ease, transform 0.1s ease;
  text-align: left;
}

.grand-bouton-proposer:hover {
  background-color: #E03E20;
}

.grand-bouton-proposer:active {
  transform: scale(0.99);
}

.carre-icone-plus {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.textes-bouton {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.titre-bouton {
  font-size: 17px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.2;
}

.soustitre-bouton {
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 2px;
}

.chevron-droit {
  display: flex;
  align-items: center;
  justify-content: center;
}

.actions-profil-conducteur {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-proposer-desktop {
  display: none;
}

.btn-proposer-vide {
  margin-top: 18px;
  background-color: var(--color-brand-accent, #FF4D2D);
  color: #FFFFFF;
  border: none;
  font-size: 14px;
  font-weight: 700;
  padding: 10px 20px;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(255, 77, 45, 0.07);
  transition: all 0.2s ease;
}

.btn-proposer-vide:hover {
  background-color: #E03E20;
  transform: translateY(-1px);
}

/* Tablet & Desktop Adaptations */
@media (min-width: 640px) {
  .page-tableau-bord {
    background-color: #F8FAFC;
    padding: 32px 20px;
  }

  .conteneur-conducteur {
    background-color: #FFFFFF;
    border-radius: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.014);
    min-height: 700px;
  }
}

@media (min-width: 900px) {
  .page-tableau-bord {
    padding: 40px 28px 60px;
  }

  .conteneur-conducteur {
    max-width: 1120px;
    padding: 36px 40px 48px;
    border-radius: 28px;
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.021);
  }

  .entete-conducteur {
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid #F1F5F9;
  }

  .nom-conducteur {
    font-size: 28px;
    letter-spacing: -0.6px;
  }

  .btn-proposer-desktop {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background-color: var(--color-brand-accent, #FF4D2D);
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 700;
    padding: 10px 18px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(255, 77, 45, 0.08);
    transition: all 0.2s ease;
  }

  .btn-proposer-desktop:hover {
    background-color: #E03E20;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(255, 77, 45, 0.1);
  }

  .btn-proposer-desktop:active {
    transform: scale(0.98);
  }

  .liste-trajets {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(460px, 1fr));
    gap: 20px;
    align-items: stretch;
  }

  .carte-trajet-conducteur {
    padding: 20px;
    border-radius: 20px;
    border: 1.5px solid #EDF2F7;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.014);
    transition: border-color 0.15s ease, background-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  }

  .carte-trajet-conducteur:hover {
    border-color: #CBD5E1;
    background-color: #FAFAFA;
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.021);
  }

  .nom-lieu {
    font-size: 16px;
  }

  .prix-trajet {
    font-size: 17px;
  }

  .pied-actions-conducteur {
    display: none;
  }
}
</style>
