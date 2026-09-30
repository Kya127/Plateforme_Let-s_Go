<script setup>
import { reactive, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import { serviceTrajets, serviceReservations } from '@/services/api'
import BarreNavigation from '@/components/layout/BarreNavigation.vue'
import RechercheUnifieeDesktop from '@/components/accueil/RechercheUnifieeDesktop.vue'
import CarteRechercheMobile from '@/components/accueil/CarteRechercheMobile.vue'
import CarteTrajet from '@/components/accueil/CarteTrajet.vue'
import CarrouselVehicules from '@/components/accueil/CarrouselVehicules.vue'
import PiedDePage from '@/components/layout/PiedDePage.vue'
import ModalReservationEnCours from '@/components/passager/ModalReservationEnCours.vue'

const routeur = useRouter()
const storeAuth = useAuthentificationStore()

/* =========================================================
   DATE D'AUJOURD'HUI (YYYY-MM-DD)
========================================================= */
const aujourdhui = new Date().toISOString().split('T')[0]

/* =========================================================
   TRAJETS DISPONIBLES (BDD)
========================================================= */
const trajetsDisponibles = ref([])
const chargementTrajets = ref(false)

async function chargerTrajetsDisponibles() {
  chargementTrajets.value = true
  try {
    const data = await serviceTrajets.lister({ statut: 'PLANIFIE' })
    const liste = Array.isArray(data) ? data : (data.results || [])
    trajetsDisponibles.value = liste.filter(t => (t.places_disponibles ?? 0) >= 1 && (!t.date || t.date >= aujourdhui))
  } catch (err) {
    console.warn('Erreur chargement des trajets disponibles BDD:', err)
    trajetsDisponibles.value = []
  } finally {
    chargementTrajets.value = false
  }
}

/* =========================================================
   RÉSERVATION ACTIVE DU PASSAGER (BDD DYNAMIQUE)
========================================================= */
const reservationActive = ref(null)
const mesReservationsTrajetIds = ref(new Set())

function estTrajetReserve(t) {
  if (!storeAuth.estConnecte || !t) return false
  if (t.est_deja_reserve) return true
  return mesReservationsTrajetIds.value.has(Number(t.id))
}

async function chargerReservationActive() {
  if (!storeAuth.estConnecte) {
    reservationActive.value = null
    mesReservationsTrajetIds.value = new Set()
    return
  }

  try {
    const resData = await serviceReservations.lister()
    const liste = Array.isArray(resData) ? resData : (resData.results || [])

    const ids = new Set()
    liste.forEach(r => {
      if (r.statut === 'CONFIRMEE') {
        const tId = r.trajet || r.trajet_id || r.trajet_details?.id
        if (tId) ids.add(Number(tId))
      }
    })
    mesReservationsTrajetIds.value = ids

    const active = liste.find(r => 
      r.statut === 'CONFIRMEE' && 
      r.trajet_details && 
      (!r.trajet_details.date || r.trajet_details.date >= aujourdhui) &&
      r.trajet_details.statut !== 'ANNULE'
    )

    if (active && active.trajet_details) {
      const td = active.trajet_details
      reservationActive.value = {
        id: active.id,
        depart: td.lieu_depart,
        arrivee: td.destination,
        arriveeDetail: td.destination,
        dateComplete: `${td.date} à ${td.heure_depart ? td.heure_depart.substring(0, 5) : '08:00'}`,
        passagers: `${active.nombre_de_places} Place${active.nombre_de_places > 1 ? 's' : ''}`,
        prixTotal: Number(td.prix_par_place || 0) * (active.nombre_de_places || 1),
        conducteur: {
          nom: td.conducteur_nom || 'Conducteur',
          voiture: td.voiture_info ? `${td.voiture_info.brand || ''} ${td.voiture_info.model || ''}`.trim() : 'Véhicule standard',
          plaque: td.voiture_info?.plate || 'DK-LET-GO',
          note: String(td.conducteur_note || '4.9'),
          telephone: td.conducteur_telephone || '',
          photo: td.conducteur_photo || ''
        }
      }
    } else {
      reservationActive.value = null
    }
  } catch (err) {
    console.warn('Impossible de charger les réservations passager:', err)
    reservationActive.value = null
  }
}

/* =========================================================
   AUTHENTIFICATION & DÉCONNEXION
========================================================= */
async function gererDeconnexion() {
  await storeAuth.deconnecter()
  reservationActive.value = null
  await chargerTrajetsDisponibles()
}

/* =========================================================
   RECHERCHE UNIFIÉE DESKTOP & MOBILE
========================================================= */
const rechercheUnifiee = reactive({
  lieu: ''
})

function lancerRechercheUnifiee() {
  const query = {}
  const lieu = rechercheUnifiee.lieu?.trim()
  if (lieu) {
    query.q = lieu
  }
  routeur.push({
    path: '/recherche-resultats',
    query
  })
}

const formulaireRecherche = reactive({
  depart: '',
  destination: '',
  date: '',
  passagers: 1,
})

function lancerRecherche() {
  const query = {}
  if (formulaireRecherche.depart?.trim()) {
    query.depart = formulaireRecherche.depart.trim()
  }
  if (formulaireRecherche.destination?.trim()) {
    query.destination = formulaireRecherche.destination.trim()
  }
  if (formulaireRecherche.date) {
    query.date = formulaireRecherche.date
  }
  if (formulaireRecherche.passagers && formulaireRecherche.passagers > 1) {
    query.passagers = String(formulaireRecherche.passagers)
  }

  routeur.push({
    path: '/recherche-resultats',
    query
  })
}

function lancerRechercheVocale() {
  routeur.push('/recherche-vocale')
}

/* =========================================================
   HELPERS & FORMATAGE
========================================================= */
function extraireVille(str) {
  if (!str) return 'SÉNÉGAL'
  const parties = str.split(',')
  return parties[parties.length - 1].trim().toUpperCase() || str.toUpperCase()
}

function calculerHeureArrivee(heureStr) {
  if (!heureStr) return '11:00'
  const [h, m] = heureStr.split(':').map(Number)
  const arriveeH = (h + 1) % 24
  const arriveeM = (m + 30) % 60
  return `${String(arriveeH).padStart(2, '0')}:${String(arriveeM).padStart(2, '0')}`
}

function naviguerVersDetailTrajet(t) {
  routeur.push(`/trajet/${t.id}`)
}

function naviguerVersPublicationConducteur() {
  routeur.push('/publier-trajet')
}

/* =========================================================
   CYCLE DE VIE & WATCHERS
========================================================= */
onMounted(() => {
  chargerTrajetsDisponibles()
  chargerReservationActive()
})

watch(() => [storeAuth.estConnecte, storeAuth.utilisateur?.estConducteurVerifie], () => {
  chargerReservationActive()
})
</script>

<template>
  <div class="page-accueil">
    <!-- 1. NAVBAR SUPÉRIEURE DESKTOP (Composant Modulaire) -->
    <BarreNavigation
      :est-connecte="storeAuth.estConnecte"
      :utilisateur="storeAuth.utilisateur"
      :avatar="storeAuth.avatarActif"
      page-active="covoiturage"
      @deconnexion="gererDeconnexion"
    />

    <!-- 2. HERO BANNER DESKTOP (Composant Modulaire) -->
    <RechercheUnifieeDesktop
      v-model="rechercheUnifiee.lieu"
      @rechercher="lancerRechercheUnifiee"
    />

    <!-- 3. CONTENU PRINCIPAL -->
    <main class="conteneur-principal">
      <!-- Formulaire de recherche mobile (Composant Modulaire) -->
      <CarteRechercheMobile
        v-model:depart="formulaireRecherche.depart"
        v-model:destination="formulaireRecherche.destination"
        v-model:date="formulaireRecherche.date"
        v-model:passagers="formulaireRecherche.passagers"
        :date-min="aujourdhui"
        @rechercher="lancerRecherche"
        @recherche-vocale="lancerRechercheVocale"
      />

      <!-- SECTION TRAJETS DISPONIBLES (Données réelles issues de la base de données Django) -->
      <section id="trajets-populaires" class="section-trajets-populaires">
        <div class="entete-section">
          <div class="titre-avec-puce">
            <span class="puce-orange"></span>
            <h3 class="titre-section">TRAJETS DISPONIBLES</h3>
          </div>
          <button
            type="button"
            class="lien-voir-tout-conducteur"
            @click="routeur.push('/recherche-resultats')"
          >
            Voir tous les trajets →
          </button>
        </div>

        <!-- Grille dynamique des trajets en base de données -->
        <div v-if="trajetsDisponibles.length > 0" class="grille-trajets">
          <CarteTrajet
            v-for="t in trajetsDisponibles"
            :key="t.id"
            :depart-ville="extraireVille(t.lieu_depart)"
            :depart-lieu="t.lieu_depart"
            :depart-heure="t.heure_depart?.substring(0, 5)"
            :arrivee-ville="extraireVille(t.destination)"
            :arrivee-lieu="t.destination"
            :arrivee-heure="calculerHeureArrivee(t.heure_depart)"
            :prix="`${Number(t.prix_par_place).toLocaleString('fr-FR')} FCFA`"
            :statut="t.places_disponibles > 0 ? 'DISPONIBLE' : 'COMPLET'"
            :conducteur-nom="t.conducteur_nom || 'Conducteur Let\'s Go'"
            :conducteur-note="t.conducteur_note || 4.9"
            :conducteur-photo="t.conducteur_photo || ''"
            :est-reserve="estTrajetReserve(t)"
            @reserver="naviguerVersDetailTrajet(t)"
          />
        </div>

        <!-- État vide propre sans données mockées -->
        <div v-else class="carte-etat-vide-bdd">
          <div class="icone-vide-cercle">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.2">
              <path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
          </div>
          <h4 class="titre-vide-bdd">Aucun trajet planifié pour le moment</h4>
          <p class="description-vide-bdd">
            Soyez le premier à proposer un trajet sur LET'S GO ou revenez un peu plus tard !
          </p>
          <button
            type="button"
            class="bouton-proposer-vide"
            @click="naviguerVersPublicationConducteur"
          >
            + Proposer le premier trajet
          </button>
        </div>
      </section>

      <!-- BANNIÈRE CONDUCTEUR ÉLARGIE (ESPACE CONDUCTEUR) -->
      <section class="banniere-conducteur-large">
        <div class="banniere-corps">
          <div class="banniere-textes">
            <span class="banniere-tag">ESPACE CONDUCTEUR</span>
            <h2 class="banniere-titre">
              Vous avez une voiture ?<br />
              Faites la travailler pour vous !
            </h2>
            <p class="banniere-description">
              Rentabilisez vos trajets quotidiens et interurbains en partageant vos places libres avec des passagers vérifiés.
            </p>
          </div>

          <div class="banniere-action">
            <button
              type="button"
              class="bouton-proposer-trajet"
              @click="naviguerVersPublicationConducteur"
            >
              <span class="icone-plus-orange">+</span>
              <span class="texte-proposer-trajet">Proposer un trajet</span>
              <span class="fleche-chevron">›</span>
            </button>
          </div>
        </div>
      </section>

      <!-- SECTION CARROUSEL DES VÉHICULES & AVANTAGES -->
      <section class="section-carrousel-bloc">
        <div class="entete-section">
          <div class="titre-avec-puce">
            <span class="puce-orange"></span>
            <h3 class="titre-section">VÉHICULES & EXPÉRIENCE DE COVOITURAGE</h3>
          </div>
        </div>
        <CarrouselVehicules />
      </section>
    </main>

    <!-- FOOTER COMPLET AVEC RÉSEAUX SOCIAUX -->
    <PiedDePage />

    <!-- BANDEAU / MODAL RÉSERVATION EN COURS DU PASSAGER (ACTIF UNIQUEMENT SI RÉSERVATION FAITE) -->
    <ModalReservationEnCours
      v-if="reservationActive"
      :reservation-data="reservationActive"
      @annule="chargerReservationActive"
    />
  </div>
</template>

<style scoped>
/* =======================================================
   DESIGN TOKENS & DISPOSITION GLOBALE
======================================================= */
.page-accueil {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;
  --black: #111627;
  --dark-gray: #374151;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;
  --white: #ffffff;

  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.page-accueil *,
.page-accueil *::before,
.page-accueil *::after {
  box-sizing: border-box;
}

/* CONTENEUR PRINCIPAL */
.conteneur-principal {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 16px 16px 36px;
  display: flex;
  flex-direction: column;
  gap: 42px;
}

@media (min-width: 768px) {
  .conteneur-principal {
    max-width: 1200px;
    padding: 36px 24px 60px;
  }
}

/* SECTION TRAJETS */
.section-trajets-populaires {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.entete-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.titre-avec-puce {
  display: flex;
  align-items: center;
  gap: 10px;
}

.puce-orange {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--brand);
}

.titre-section {
  font-size: 14px;
  font-weight: 800;
  color: var(--black);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin: 0;
}

.lien-voir-tout-conducteur {
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 700;
  color: var(--brand);
  cursor: pointer;
  transition: color 0.18s ease;
  font-family: inherit;
}

.lien-voir-tout-conducteur:hover {
  color: var(--brand-hover);
  text-decoration: underline;
}

/* GRILLE TRAJETS */
.grille-trajets {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .grille-trajets {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (min-width: 1100px) {
  .grille-trajets {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ÉTAT VIDE BDD */
.carte-etat-vide-bdd {
  background: #FFFFFF;
  border: 1px dashed #E5E7EB;
  border-radius: 24px;
  padding: 40px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.icone-vide-cercle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #FFF5F2;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.titre-vide-bdd {
  font-size: 17px;
  font-weight: 800;
  color: var(--black);
  margin: 0 0 8px;
}

.description-vide-bdd {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 360px;
  margin: 0 0 20px;
  line-height: 1.5;
}

.bouton-proposer-vide {
  padding: 10px 22px;
  background: var(--brand);
  color: #FFFFFF;
  border: none;
  border-radius: 9999px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.1);
  transition: all 0.18s ease;
  font-family: inherit;
}

.bouton-proposer-vide:hover {
  background: var(--brand-hover);
  transform: translateY(-1px);
}

/* SECTION CARROUSEL */
.section-carrousel-bloc {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* =======================================================
   BANNIÈRE CONDUCTEUR ÉLARGIE
======================================================= */
.banniere-conducteur-large {
  width: 100%;
  padding: 28px 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 26px;
  background: linear-gradient(135deg, #1A2136 0%, #111627 100%);
  box-shadow: 0 10px 25px -5px rgba(17, 22, 39, 0.07);
  box-sizing: border-box;
}

.banniere-corps {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.banniere-textes {
  display: flex;
  flex-direction: column;
}

.banniere-tag {
  display: inline-block;
  margin-bottom: 8px;
  font-size: 11px;
  font-weight: 800;
  color: var(--brand);
  letter-spacing: 1.2px;
  text-transform: uppercase;
}

.banniere-titre {
  margin: 0 0 10px;
  font-size: 22px;
  font-weight: 800;
  line-height: 1.25;
  color: #FFFFFF;
  letter-spacing: -0.5px;
}

.banniere-description {
  max-width: 560px;
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: #9CA3AF;
}

.banniere-action {
  display: flex;
  align-items: center;
}

.bouton-proposer-trajet {
  width: 100%;
  min-height: 50px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 26px;
  border: none;
  border-radius: 9999px;
  background-color: #FFFFFF;
  color: #111627;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
  font-family: inherit;
}

.bouton-proposer-trajet:hover {
  background-color: #F9FAFB;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
}

.icone-plus-orange {
  color: var(--brand);
  font-size: 20px;
  font-weight: 900;
  line-height: 1;
}

.texte-proposer-trajet {
  color: #111627;
}

.fleche-chevron {
  color: var(--brand);
  font-size: 20px;
  font-weight: 800;
  margin-left: 2px;
  line-height: 1;
}

@media (min-width: 768px) {
  .banniere-conducteur-large {
    padding: 34px 38px;
  }

  .banniere-corps {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 32px;
  }

  .banniere-titre {
    font-size: 25px;
  }

  .bouton-proposer-trajet {
    width: auto;
    min-width: 220px;
  }
}
</style>