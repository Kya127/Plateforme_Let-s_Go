<template>
  <div class="results-page">

    <!-- =====================================================
         HEADER / ZONE SUPÉRIEURE
    ====================================================== -->
    <header class="results-header">
      <div class="results-header-inner">
        <!-- Retour -->
        <button
          type="button"
          class="back-button"
          aria-label="Retour"
          @click="goBack"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M15 18L9 12L15 6" />
          </svg>
        </button>

        <!-- Trajet recherché -->
        <div class="route-pill">
          <span class="route-point">{{ departureLabel }}</span>
          <span class="route-arrow" aria-hidden="true">→</span>
          <span class="route-point route-point--destination">{{ destinationLabel }}</span>
        </div>

        <!-- Espace droit pour garder le centrage -->
        <div class="header-spacer"></div>
      </div>
    </header>

    <!-- =====================================================
         CONTENU
    ====================================================== -->
    <main class="results-content">

      <!-- ===================================================
           TITRE
      ==================================================== -->
      <section class="results-intro">
        <div>
          <h1>
            {{ trips.length }}
            {{ trips.length > 1 ? 'trajets disponibles' : 'trajet disponible' }}
          </h1>

          <p v-if="dateLabel" class="results-date">
            {{ dateLabel }}
          </p>
        </div>
      </section>

      <!-- Indicateur de chargement -->
      <div v-if="chargement" class="results-loading-state">
        <span class="spinner-circle"></span>
        <p>Recherche des trajets disponibles...</p>
      </div>

      <!-- ===================================================
           LISTE DES TRAJETS (Composant Modulaire CarteResultatTrajet)
      ==================================================== -->
      <section
        v-else-if="trips.length"
        class="trips-list"
        aria-label="Résultats de recherche"
      >
        <CarteResultatTrajet
          v-for="trip in trips"
          :key="trip.id"
          :trip="trip"
          @select="selectTrip"
        />
      </section>

      <!-- ===================================================
           AUCUN TRAJET
      ==================================================== -->
      <EtatAucunTrajet
        v-else
        titre="Aucun trajet disponible"
        description="Aucun trajet ne correspond actuellement à votre recherche."
        bouton-texte="Modifier ma recherche"
        @action="goBack"
      />

    </main>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { serviceTrajets } from '@/services/api'
import CarteResultatTrajet from '@/components/passager/CarteResultatTrajet.vue'
import EtatAucunTrajet from '@/components/common/EtatAucunTrajet.vue'

/* =========================================================
   ROUTER
========================================================= */
const route = useRoute()
const router = useRouter()

/* =========================================================
   CRITÈRES DE RECHERCHE
========================================================= */
const querySearch = computed(() => {
  return String(route.query.q || '').trim()
})

const departure = computed(() => {
  return String(route.query.depart || '').trim()
})

const destination = computed(() => {
  return String(route.query.destination || '').trim()
})

const searchedDate = computed(() => {
  return String(route.query.date || '').trim()
})

const searchedTime = computed(() => {
  return String(route.query.heure || '').trim()
})

const passengerCount = computed(() => {
  const value = Number(route.query.passagers)
  if (!Number.isFinite(value) || value < 1) {
    return 1
  }
  return Math.min(value, 8)
})

/* =========================================================
   LABELS
========================================================= */
const departureLabel = computed(() => {
  if (departure.value) return departure.value.toUpperCase()
  if (querySearch.value) return 'RECHERCHE'
  return 'TOUS LES DÉPARTS'
})

const destinationLabel = computed(() => {
  if (destination.value) return destination.value.toUpperCase()
  if (querySearch.value) return querySearch.value.toUpperCase()
  return 'TOUTES DESTINATIONS'
})

const dateLabel = computed(() => {
  if (!searchedDate.value) {
    return ''
  }

  const rawDate = searchedDate.value

  if (
    rawDate.toLowerCase() === 'demain' ||
    rawDate.toLowerCase() === "aujourd'hui" ||
    rawDate.toLowerCase() === 'aujourdhui'
  ) {
    return rawDate
  }

  const date = new Date(rawDate)

  if (Number.isNaN(date.getTime())) {
    return rawDate
  }

  return date.toLocaleDateString('fr-FR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  })
})

/* =========================================================
   DONNÉES TRAJETS EN BASE DE DONNÉES
========================================================= */
const trips = ref([])
const chargement = ref(true)
const aujourdhui = new Date().toISOString().split('T')[0]

async function chargerResultats() {
  chargement.value = true
  try {
    const filtres = {
      statut: 'PLANIFIE',
    }
    if (querySearch.value) filtres.q = querySearch.value
    if (departure.value) filtres.lieu_depart = departure.value
    if (destination.value) filtres.destination = destination.value
    if (searchedDate.value) filtres.date = searchedDate.value
    if (passengerCount.value > 1) filtres.passagers = passengerCount.value

    const data = await serviceTrajets.lister(filtres)
    const liste = Array.isArray(data) ? data : data.results || []

    // Filtrer strictement les trajets disponibles non expirés avec places_disponibles >= 1
    const disponibles = liste.filter(
      (t) => (t.places_disponibles ?? 0) >= 1 && (!t.date || t.date >= aujourdhui)
    )

    trips.value = disponibles.map((t) => ({
      id: t.id,
      driver: t.conducteur_nom || "Conducteur Let's Go",
      rating: Number(t.conducteur_note) || 4.9,
      reviews: t.conducteur_avis_count || 12,
      price: Number(t.prix_par_place) || 0,
      time: t.heure_depart ? t.heure_depart.substring(0, 5) : '08:00',
      duration: '60 min',
      availableSeats: Number(t.places_disponibles) || 0,
      photo: t.conducteur_photo || '',
      departure: t.lieu_depart,
      destination: t.destination,
    }))
  } catch (err) {
    console.error('Erreur chargement des résultats de recherche BDD:', err)
    trips.value = []
  } finally {
    chargement.value = false
  }
}

onMounted(() => {
  chargerResultats()
})

watch(
  () => [
    route.query.depart,
    route.query.destination,
    route.query.date,
    route.query.passagers,
    route.query.q,
  ],
  () => {
    chargerResultats()
  }
)

/* =========================================================
   ACTIONS
========================================================= */
const selectTrip = (trip) => {
  router.push({
    path: `/trajet/${trip.id}`,
    query: {
      depart: departure.value || trip.departure,
      destination: destination.value || trip.destination,
      date: searchedDate.value,
      passagers: passengerCount.value,
    },
  })
}

const goBack = () => {
  router.push('/accueil')
}
</script>

<style scoped>
/* =========================================================
   VARIABLES & CONTAINER
========================================================= */
.results-page {
  --brand: #ff4d2d;
  --brand-dark: #ed4327;
  --black: #111627;
  --text: #111627;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --soft-gray: #e5e7eb;
  --light-gray: #f3f4f6;
  --white: #ffffff;

  min-height: 100svh;
  background: linear-gradient(180deg, #edf0f1 0%, #f8f9fa 16%, #f8f9fa 100%);
  color: var(--text);
  font-family: 'Plus Jakarta Sans', Arial, sans-serif;
  box-sizing: border-box;
}

.results-page *,
.results-page *::before,
.results-page *::after {
  box-sizing: border-box;
}

/* =========================================================
   HEADER
========================================================= */
.results-header {
  width: 100%;
  background: linear-gradient(
    180deg,
    #aeb1b4 0%,
    #bfc1c3 44%,
    #d8dcdd 72%,
    rgba(244, 246, 247, 0.7) 100%
  );
  min-height: 210px;
  position: relative;
}

.results-header-inner {
  width: 100%;
  max-width: 1160px;
  margin: 0 auto;
  padding: 34px 30px 0;
  display: grid;
  grid-template-columns: 64px minmax(220px, 1fr) 64px;
  align-items: start;
}

/* =========================================================
   BOUTON RETOUR
========================================================= */
.back-button {
  width: 64px;
  height: 64px;
  border: none;
  border-radius: 19px;
  background: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 5px 14px rgba(17, 22, 39, 0.04);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.back-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 7px 18px rgba(17, 22, 39, 0.06);
}

.back-button:active {
  transform: scale(0.98);
}

.back-button svg {
  width: 27px;
  height: 27px;
  fill: none;
  stroke: var(--black);
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* =========================================================
   ROUTE PILL
========================================================= */
.route-pill {
  justify-self: center;
  min-height: 64px;
  padding: 0 30px;
  border-radius: 21px;
  background: rgba(255, 255, 255, 0.94);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  box-shadow: 0 4px 12px rgba(17, 22, 39, 0.032);
  white-space: nowrap;
}

.route-point {
  font-size: 18px;
  line-height: 1;
  font-weight: 800;
  color: #9aa2ae;
  text-transform: uppercase;
}

.route-point--destination {
  color: var(--black);
}

.route-arrow {
  color: var(--brand);
  font-size: 24px;
  font-weight: 800;
  line-height: 1;
  transform: translateY(-1px);
}

/* =========================================================
   CONTENU & INTRO
========================================================= */
.results-content {
  width: min(calc(100% - 48px), 980px);
  margin: -1px auto 0;
  padding: 0 0 50px;
}

.results-intro {
  padding: 18px 16px 22px;
}

.results-intro h1 {
  margin: 0;
  font-size: 18px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.7px;
  color: var(--black);
}

.results-date {
  margin: 8px 0 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: capitalize;
}

/* =========================================================
   GRILLE LISTE
========================================================= */
.trips-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px;
}

/* =========================================================
   LOADING STATE
========================================================= */
.results-loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  color: #6b7280;
  font-size: 14px;
  gap: 14px;
}

.results-loading-state .spinner-circle {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 77, 45, 0.15);
  border-top-color: #FF4D2D;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* =========================================================
   EMPTY STATE
========================================================= */
.empty-results {
  min-height: 350px;
  border-radius: 28px;
  background: var(--white);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 35px;
  border: 1px solid rgba(17, 22, 39, 0.05);
  box-shadow: 0 4px 12px rgba(17, 22, 39, 0.028);
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: rgba(255, 77, 45, 0.08);
  color: var(--brand);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
}

.empty-icon svg {
  width: 28px;
  height: 28px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
}

.empty-results h2 {
  margin: 0;
  font-size: 21px;
  font-weight: 800;
}

.empty-results p {
  max-width: 420px;
  margin: 10px 0 20px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.5;
}

.empty-button {
  height: 46px;
  padding: 0 20px;
  border: none;
  border-radius: 14px;
  background: var(--brand);
  color: white;
  font: inherit;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

/* =========================================================
   RESPONSIVE TABLET (max-width: 820px)
========================================================= */
@media (max-width: 820px) {
  .results-header {
    min-height: 188px;
  }

  .results-header-inner {
    padding: 26px 22px 0;
    grid-template-columns: 54px minmax(0, 1fr) 54px;
  }

  .back-button {
    width: 54px;
    height: 54px;
    border-radius: 17px;
  }

  .back-button svg {
    width: 24px;
    height: 24px;
  }

  .route-pill {
    min-height: 58px;
    padding: 0 22px;
    border-radius: 18px;
  }

  .route-point {
    font-size: 16px;
  }

  .route-arrow {
    font-size: 21px;
  }

  .results-content {
    width: min(calc(100% - 32px), 680px);
  }

  .trips-list {
    grid-template-columns: 1fr;
  }
}

/* =========================================================
   RESPONSIVE MOBILE (max-width: 560px)
========================================================= */
@media (max-width: 560px) {
  .results-page {
    min-height: 100svh;
    background: linear-gradient(180deg, #f1f2f3 0%, #f8f9fa 21%, #f8f9fa 100%);
  }

  .results-header {
    min-height: 214px;
    background: linear-gradient(
      180deg,
      #aeb1b4 0%,
      #c2c4c6 42%,
      #daddde 68%,
      #f1f3f4 100%
    );
  }

  .results-header-inner {
    padding: 24px 18px 0;
    grid-template-columns: 58px minmax(0, 1fr) 58px;
  }

  .back-button {
    width: 58px;
    height: 58px;
    border-radius: 17px;
  }

  .back-button svg {
    width: 25px;
    height: 25px;
  }

  .route-pill {
    min-height: 58px;
    padding: 0 18px;
    gap: 7px;
    border-radius: 18px;
    max-width: 100%;
    overflow: hidden;
  }

  .route-point {
    max-width: 105px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 15px;
  }

  .route-arrow {
    font-size: 20px;
  }

  .results-content {
    width: calc(100% - 32px);
    margin: -3px auto 0;
    padding-bottom: 30px;
  }

  .results-intro {
    padding: 5px 14px 20px;
  }

  .results-intro h1 {
    font-size: 18px;
    letter-spacing: -0.5px;
  }

  .results-date {
    font-size: 13px;
  }

  .trips-list {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
}

/* =========================================================
   PETITS ÉCRANS (max-width: 390px)
========================================================= */
@media (max-width: 390px) {
  .results-header-inner {
    grid-template-columns: 52px minmax(0, 1fr) 52px;
  }

  .back-button {
    width: 52px;
    height: 52px;
  }

  .route-pill {
    min-height: 54px;
    padding: 0 14px;
  }

  .route-point {
    font-size: 13px;
    max-width: 90px;
  }

  .route-arrow {
    font-size: 18px;
  }
}
</style>