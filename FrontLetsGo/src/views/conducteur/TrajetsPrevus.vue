<template>
  <div class="trips-page">
    <!-- =====================================================
         HEADER
    ====================================================== -->
    <header class="page-header">
      <h1>Trajets prévus</h1>

      <p>Gérez vos trajets proposés</p>
    </header>

    <!-- =====================================================
         TABS
    ====================================================== -->
    <nav
      class="tabs"
      aria-label="Filtrer les trajets"
    >
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="tab"
        :class="{
          'tab--active': activeTab === tab.id
        }"
        @click="activeTab = tab.id"
      >
        <span>{{ tab.label }}</span>

        <span
          v-if="tab.count > 0"
          class="tab-count"
        >
          {{ tab.count }}
        </span>
      </button>
    </nav>

    <!-- =====================================================
         CONTENT
    ====================================================== -->
    <main class="page-content">
      <!-- Aucun trajet -->
      <section
        v-if="filteredTrips.length === 0"
        class="empty-state"
      >
        <div class="empty-icon">
          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M5 5h14v14H5z" />
            <path d="M8 9h8" />
            <path d="M8 13h5" />
          </svg>
        </div>

        <h2>
          Aucun trajet
        </h2>

        <p>
          Vous n'avez aucun trajet
          dans cette catégorie.
        </p>
      </section>

      <!-- Liste -->
      <section
        v-else
        class="trips-list"
        aria-label="Liste des trajets"
      >
        <article
          v-for="trip in filteredTrips"
          :key="trip.id"
          class="trip-card"
        >
          <!-- =================================================
               TOP : INFORMATIONS TRAJET
          ================================================== -->
          <div class="trip-main">
            <!-- Colonne trajet -->
            <div class="route-column">
              <!-- Départ -->
              <div class="route-row">
                <div
                  class="route-marker route-marker--start"
                  aria-hidden="true"
                >
                  <span></span>
                </div>

                <div class="route-line"></div>

                <div class="route-content">
                  <span class="route-meta">
                    {{ trip.departureLabel }}
                    <span class="bullet">•</span>
                    {{ trip.departureTime }}
                  </span>

                  <h2>
                    {{ trip.departure }}
                  </h2>
                </div>
              </div>

              <!-- Arrivée -->
              <div class="route-row route-row--arrival">
                <div
                  class="route-marker route-marker--end"
                  aria-hidden="true"
                ></div>

                <div class="route-content">
                  <span class="route-meta">
                    {{ trip.arrivalLabel }}
                    <span class="bullet">•</span>
                    {{ trip.arrivalTime }}
                  </span>

                  <h2>
                    {{ trip.destination }}
                  </h2>
                </div>
              </div>
            </div>

            <!-- Prix -->
            <div class="price-block">
              <strong>
                {{ formatPrice(trip.price) }} FCFA
              </strong>

              <span>
                PAR PLACE
              </span>
            </div>
          </div>

          <!-- =================================================
               DIVIDER
          ================================================== -->
          <div class="card-divider"></div>

          <!-- =================================================
               BOTTOM
          ================================================== -->
          <div class="trip-footer">
            <!-- Passagers -->
            <div
              class="passengers"
              :aria-label="
                `${trip.seatsTaken} passager(s) sur ${trip.seatsTotal}`
              "
            >
              <!-- Profils réels -->
              <div
                v-for="passenger in visiblePassengers(
                  trip
                )"
                :key="passenger.id"
                class="passenger-avatar"
                :title="
                  `${passenger.firstName} ${passenger.lastName}`
                "
              >
                <!-- Photo disponible -->
                <img
                  v-if="passenger.profilePhoto"
                  :src="passenger.profilePhoto"
                  :alt="
                    `Photo de ${passenger.firstName} ${passenger.lastName}`
                  "
                  class="passenger-photo"
                  @error="
                    handleImageError
                  "
                />

                <!-- Initiales -->
                <span
                  v-else
                  class="passenger-initials"
                  :aria-label="
                    `Passager ${getInitials(
                      passenger.firstName,
                      passenger.lastName
                    )}`
                  "
                >
                  {{
                    getInitials(
                      passenger.firstName,
                      passenger.lastName
                    )
                  }}
                </span>
              </div>

              <!-- Place libre -->
              <div
                v-if="
                  trip.seatsTaken <
                  trip.seatsTotal
                "
                class="passenger-avatar passenger-avatar--empty"
                title="Place disponible"
                aria-label="Place disponible"
              >
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <circle
                    cx="12"
                    cy="8"
                    r="3.2"
                  />

                  <path
                    d="M5 20c.7-3.5 3-5.5 7-5.5s6.3 2 7 5.5"
                  />
                </svg>
              </div>
            </div>

            <!-- Compteur -->
            <div class="seat-summary">
              <strong>
                {{ trip.seatsTaken }}
                /
                {{ trip.seatsTotal }}
              </strong>

              <span>
                places prises
              </span>
            </div>

            <!-- Voir -->
            <button
              type="button"
              class="view-button"
              @click="viewTrip(trip)"
            >
              Voir
            </button>
          </div>
        </article>
      </section>
    </main>

    <!-- =====================================================
         ADD TRIP
    ====================================================== -->
    <button
      type="button"
      class="add-trip-button"
      aria-label="Publier un nouveau trajet"
      @click="createTrip"
    >
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path d="M12 5v14" />
        <path d="M5 12h14" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import {
  computed,
  ref
} from 'vue'

import { useRouter } from 'vue-router'

/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()

/* =========================================================
   TABS
========================================================= */

const activeTab = ref('upcoming')

const tabs = [
  {
    id: 'upcoming',
    label: 'À venir'
  },
  {
    id: 'completed',
    label: 'Terminés'
  },
  {
    id: 'cancelled',
    label: 'Annulés'
  }
]

/* =========================================================
   DATA
   Exemple temporaire.
   À remplacer ensuite par les données Django / DRF.
========================================================= */

const trips = ref([
  {
    id: 1,

    status: 'upcoming',

    departureLabel: 'DEMAIN',
    departureTime: '08:30',
    departure: 'Keur Massar',

    arrivalLabel: 'ARRIVÉE',
    arrivalTime: '11:45',
    destination: 'Ouakam',

    price: 1500,

    seatsTotal: 3,
    seatsTaken: 2,

    passengers: [
      {
        id: 101,
        firstName: 'Awa',
        lastName: 'Ndiaye',
        profilePhoto:
          '/images/passagers/awa.jpg'
      },

      {
        id: 102,
        firstName: 'Mamadou',
        lastName: 'Diop',
        profilePhoto: null
      }
    ]
  }
])

/* =========================================================
   FILTER
========================================================= */

const filteredTrips = computed(() => {
  return trips.value.filter(
    (trip) =>
      trip.status === activeTab.value
  )
})

/* =========================================================
   TAB COUNTS
========================================================= */

const getTabCount = (id) => {
  return trips.value.filter(
    (trip) =>
      trip.status === id
  ).length
}

tabs.forEach((tab) => {
  Object.defineProperty(
    tab,
    'count',
    {
      get() {
        return getTabCount(
          tab.id
        )
      }
    }
  )
})

/* =========================================================
   PRICE
========================================================= */

const formatPrice = (price) => {
  return new Intl.NumberFormat(
    'fr-FR',
    {
      maximumFractionDigits: 0
    }
  ).format(price)
}

/* =========================================================
   INITIALS
========================================================= */

const getInitials = (
  firstName,
  lastName
) => {
  const first =
    firstName
      ?.trim()
      ?.charAt(0) || ''

  const last =
    lastName
      ?.trim()
      ?.charAt(0) || ''

  return (
    `${first}${last}`
  ).toUpperCase()
}

/* =========================================================
   PASSENGERS
========================================================= */

const visiblePassengers = (
  trip
) => {
  /*
   * La maquette montre au maximum
   * 2 profils + 1 place libre.
   */
  return trip.passengers.slice(
    0,
    2
  )
}

/* =========================================================
   IMAGE FALLBACK
========================================================= */

const handleImageError = (
  event
) => {
  /*
   * Si l'image existe en DB mais ne peut
   * pas être chargée, on remplace le src
   * pour afficher les initiales.
   */
  event.target.style.display =
    'none'

  const parent =
    event.target.parentElement

  const passenger =
    parent?.dataset?.passenger

  if (passenger) {
    return
  }

  /*
   * L'affichage des initiales est déjà présent
   * uniquement lorsque profilePhoto est null.
   *
   * On évite donc d'afficher une image cassée.
   */
}

/* =========================================================
   ACTIONS
========================================================= */

const viewTrip = (
  trip
) => {
  router.push({
    name: 'trip-details',
    params: {
      id: trip.id
    }
  })
}

const createTrip = () => {
  router.push(
    '/conducteur/publier-trajet'
  )
}
</script>

<style scoped>
/* =========================================================
   DESIGN TOKENS
========================================================= */

.trips-page {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;

  --black: #111627;
  --dark-gray: #374151;

  --text: #111627;
  --text-secondary: #8d939d;
  --text-muted: #aeb3bb;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  width: 100%;
  min-height: 100vh;

  min-height: 100svh;

  overflow-x: hidden;

  background: #f9fafb;

  color: var(--text);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  box-sizing: border-box;
}

.trips-page *,
.trips-page *::before,
.trips-page *::after {
  box-sizing: border-box;
}


/* =========================================================
   HEADER
========================================================= */

.page-header {
  width: min(
    calc(100% - 48px),
    654px
  );

  margin: 0 auto;

  padding-top: 54px;
}

.page-header h1 {
  margin: 0;

  color: var(--black);

  font-size: 43px;
  line-height: 1.15;

  font-weight: 800;

  letter-spacing: -1.5px;
}

.page-header p {
  margin:
    11px
    0
    0;

  color: #8b919b;

  font-size: 25px;
  line-height: 1.35;

  font-weight: 500;

  letter-spacing: -0.5px;
}


/* =========================================================
   TABS
========================================================= */

.tabs {
  width: 100%;

  display: flex;
  align-items: flex-end;

  margin-top: 62px;

  padding:
    0
    max(24px, calc((100vw - 654px) / 2));

  border-bottom: 1px solid #e2e4e7;
}

.tab {
  position: relative;

  flex: 1;

  min-width: 0;

  height: 73px;

  display: flex;
  align-items: center;
  justify-content: center;

  gap: 6px;

  padding: 0 12px;

  border: 0;

  background: transparent;

  color: #acb1b9;

  font-family: inherit;

  font-size: 25px;
  line-height: 1;

  font-weight: 700;

  cursor: pointer;

  transition:
    color 180ms ease,
    background-color 180ms ease;
}

.tab:hover {
  color: #7f858e;
}

.tab--active {
  color: var(--black);
}

.tab--active::after {
  content: '';

  position: absolute;

  left: 50%;

  bottom: -1px;

  width: 48px;
  height: 6px;

  transform: translateX(-50%);

  border-radius: 999px;

  background: var(--brand);
}

.tab-count {
  font-size: 13px;
  font-weight: 700;
}


/* =========================================================
   CONTENT
========================================================= */

.page-content {
  width: min(
    calc(100% - 48px),
    654px
  );

  margin: 0 auto;

  padding:
    62px
    0
    170px;
}

.trips-list {
  display: flex;
  flex-direction: column;

  gap: 20px;
}


/* =========================================================
   TRIP CARD
========================================================= */

.trip-card {
  width: 100%;
  min-width: 0;

  padding:
    30px
    28px
    26px;

  border: 1px solid #dfe2e6;

  border-radius: 34px;

  background: #ffffff;

  box-shadow:
    0 2px 5px rgba(17, 22, 39, 0.025);
}


/* =========================================================
   MAIN
========================================================= */

.trip-main {
  display: grid;

  grid-template-columns:
    minmax(0, 1fr)
    auto;

  gap: 20px;
}

.route-column {
  min-width: 0;
}


/* =========================================================
   ROUTE ROW
========================================================= */

.route-row {
  position: relative;

  display: grid;

  grid-template-columns:
    36px
    minmax(0, 1fr);

  column-gap: 14px;
}

.route-row--arrival {
  margin-top: 25px;
}

.route-marker {
  position: relative;

  width: 24px;
  height: 24px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin: 2px auto 0;
}

.route-marker--start {
  border: 4px solid var(--brand);

  border-radius: 50%;

  background: #ffffff;
}

.route-marker--start span {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: var(--brand);
}

.route-marker--end {
  width: 24px;
  height: 24px;

  border-radius: 50%;

  background: var(--brand);
}


/* =========================================================
   ROUTE VERTICAL LINE
========================================================= */

.route-line {
  position: absolute;

  left: 18px;
  top: 29px;

  width: 4px;
  height: 55px;

  border-radius: 999px;

  background: #e2e5e8;
}


/* =========================================================
   ROUTE CONTENT
========================================================= */

.route-content {
  min-width: 0;
}

.route-meta {
  display: block;

  color: #b0b5bd;

  font-size: 20px;
  line-height: 1.2;

  font-weight: 700;

  letter-spacing: 0.2px;

  text-transform: uppercase;
}

.bullet {
  margin:
    0
    2px;
}

.route-content h2 {
  min-width: 0;

  margin:
    8px
    0
    0;

  color: var(--black);

  font-size: 29px;
  line-height: 1.22;

  font-weight: 700;

  letter-spacing: -0.7px;

  overflow-wrap: anywhere;
}


/* =========================================================
   PRICE
========================================================= */

.price-block {
  flex-shrink: 0;

  display: flex;
  flex-direction: column;

  align-items: flex-end;

  padding-top: 2px;

  text-align: right;
}

.price-block strong {
  color: var(--brand);

  font-size: 39px;
  line-height: 1;

  font-weight: 800;

  letter-spacing: -1px;
}

.price-block span {
  margin-top: 8px;

  color: #afb4bc;

  font-size: 16px;
  line-height: 1;

  font-weight: 700;
}


/* =========================================================
   DIVIDER
========================================================= */

.card-divider {
  width: 100%;
  height: 1px;

  margin:
    31px
    0
    22px;

  background: #eceef0;
}


/* =========================================================
   FOOTER
========================================================= */

.trip-footer {
  min-width: 0;

  display: grid;

  grid-template-columns:
    auto
    minmax(0, 1fr)
    auto;

  align-items: center;

  gap: 18px;
}


/* =========================================================
   PASSENGERS
========================================================= */

.passengers {
  display: flex;
  align-items: center;

  min-width: 0;
}

.passenger-avatar {
  width: 50px;
  height: 50px;

  flex: 0 0 50px;

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: hidden;

  margin-left: -9px;

  border: 3px solid #ffffff;

  border-radius: 50%;

  background: #f3f4f6;

  color: var(--black);
}

.passenger-avatar:first-child {
  margin-left: 0;
}

.passenger-photo {
  width: 100%;
  height: 100%;

  display: block;

  object-fit: cover;
}

.passenger-initials {
  width: 100%;
  height: 100%;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #f1f3f5;

  color: #111627;

  font-size: 13px;
  font-weight: 800;

  letter-spacing: -0.3px;
}

.passenger-avatar--empty {
  background: #f1f3f5;

  color: #afb5be;
}

.passenger-avatar--empty svg {
  width: 23px;
  height: 23px;

  fill: none;

  stroke: currentColor;
  stroke-width: 1.6;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   SEAT SUMMARY
========================================================= */

.seat-summary {
  min-width: 0;

  display: flex;
  align-items: baseline;

  gap: 5px;
}

.seat-summary strong {
  color: #374151;

  font-size: 20px;
  font-weight: 700;
}

.seat-summary span {
  color: #374151;

  font-size: 19px;
  font-weight: 500;
}


/* =========================================================
   VIEW BUTTON
========================================================= */

.view-button {
  min-width: 108px;
  height: 74px;

  padding:
    0
    20px;

  border: 0;
  border-radius: 25px;

  background: var(--black);
  color: #ffffff;

  font-family: inherit;

  font-size: 20px;
  font-weight: 700;

  cursor: pointer;

  transition:
    background-color 180ms ease,
    transform 180ms ease;
}

.view-button:hover {
  background: #1a2132;

  transform: translateY(-1px);
}

.view-button:active {
  transform: translateY(0);
}

.view-button:focus-visible {
  outline: 3px solid rgba(17, 22, 39, 0.15);
  outline-offset: 3px;
}


/* =========================================================
   ADD BUTTON
========================================================= */

.add-trip-button {
  position: fixed;

  z-index: 20;

  left: 50%;
  bottom: 42px;

  width: 112px;
  height: 112px;

  transform: translateX(-50%);

  display: flex;
  align-items: center;
  justify-content: center;

  border: 0;
  border-radius: 30px;

  background: var(--brand);

  color: #ffffff;

  cursor: pointer;

  /*
   * Shadow volontairement légère.
   */
  box-shadow:
    0 7px 16px rgba(
      255,
      77,
      45,
      0.10
    );

  transition:
    background-color 180ms ease,
    transform 180ms ease,
    box-shadow 180ms ease;
}

.add-trip-button:hover {
  background: var(--brand-hover);

  transform:
    translateX(-50%)
    translateY(-1px);

  box-shadow:
    0 9px 18px rgba(
      255,
      77,
      45,
      0.12
    );
}

.add-trip-button:active {
  background: var(--brand-active);

  transform:
    translateX(-50%)
    translateY(0);

  box-shadow:
    0 4px 10px rgba(
      255,
      77,
      45,
      0.08
    );
}

.add-trip-button:focus-visible {
  outline: 3px solid rgba(
    255,
    77,
    45,
    0.20
  );

  outline-offset: 4px;
}

.add-trip-button svg {
  width: 42px;
  height: 42px;

  fill: none;

  stroke: currentColor;
  stroke-width: 2;

  stroke-linecap: round;

  transition:
    transform 180ms ease;
}

.add-trip-button:hover svg {
  transform: rotate(90deg);
}


/* =========================================================
   EMPTY STATE
========================================================= */

.empty-state {
  min-height: 320px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  padding: 30px;

  border: 1px solid #e5e7eb;

  border-radius: 30px;

  background: #ffffff;

  text-align: center;
}

.empty-icon {
  width: 56px;
  height: 56px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 18px;

  background: #f3f4f6;

  color: #9ca3af;
}

.empty-icon svg {
  width: 27px;
  height: 27px;

  fill: none;

  stroke: currentColor;
  stroke-width: 1.7;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.empty-state h2 {
  margin:
    18px
    0
    0;

  font-size: 22px;
  font-weight: 700;
}

.empty-state p {
  max-width: 300px;

  margin:
    8px
    0
    0;

  color: #9ca3af;

  font-size: 14px;
  line-height: 1.5;
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 700px) {

  .page-header {
    width: calc(100% - 40px);

    padding-top: 40px;
  }

  .page-header h1 {
    font-size: 36px;
  }

  .page-header p {
    font-size: 21px;
  }

  .tabs {
    padding-left: 20px;
    padding-right: 20px;

    margin-top: 45px;
  }

  .tab {
    height: 62px;

    font-size: 20px;
  }

  .page-content {
    width: calc(100% - 40px);

    padding-top: 45px;
  }

  .trip-card {
    padding:
      25px
      22px
      22px;

    border-radius: 28px;
  }

  .route-meta {
    font-size: 16px;
  }

  .route-content h2 {
    font-size: 24px;
  }

  .price-block strong {
    font-size: 32px;
  }

  .price-block span {
    font-size: 13px;
  }

  .seat-summary strong {
    font-size: 17px;
  }

  .seat-summary span {
    font-size: 16px;
  }

  .view-button {
    min-width: 88px;
    height: 62px;

    border-radius: 20px;

    font-size: 17px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .trips-page {
    width: 100%;

    min-width: 0;

    overflow-x: hidden;
  }

  /* -------------------------------------------------------
     HEADER
  ------------------------------------------------------- */

  .page-header {
    width: 100%;

    padding:
      34px
      20px
      0;
  }

  .page-header h1 {
    font-size: 32px;

    letter-spacing: -1px;
  }

  .page-header p {
    margin-top: 8px;

    font-size: 19px;

    line-height: 1.3;
  }


  /* -------------------------------------------------------
     TABS
  ------------------------------------------------------- */

  .tabs {
    width: 100%;

    margin-top: 39px;

    padding:
      0
      10px;

    overflow: hidden;
  }

  .tab {
    flex: 1;

    height: 57px;

    padding:
      0
      6px;

    font-size: 17px;

    white-space: nowrap;
  }

  .tab--active::after {
    width: 42px;
    height: 5px;
  }


  /* -------------------------------------------------------
     CONTENT
  ------------------------------------------------------- */

  .page-content {
    width: 100%;

    padding:
      38px
      16px
      145px;
  }

  .trips-list {
    width: 100%;

    gap: 16px;
  }


  /* -------------------------------------------------------
     CARD
  ------------------------------------------------------- */

  .trip-card {
    width: 100%;
    min-width: 0;

    padding:
      20px
      17px
      18px;

    border-radius: 28px;
  }


  /* -------------------------------------------------------
     MAIN
  ------------------------------------------------------- */

  .trip-main {
    grid-template-columns:
      minmax(0, 1fr)
      auto;

    gap: 10px;
  }


  /* -------------------------------------------------------
     ROUTE
  ------------------------------------------------------- */

  .route-row {
    grid-template-columns:
      28px
      minmax(0, 1fr);

    column-gap: 9px;
  }

  .route-row--arrival {
    margin-top: 19px;
  }

  .route-marker {
    width: 20px;
    height: 20px;
  }

  .route-marker--start {
    border-width: 3px;
  }

  .route-marker--start span {
    width: 5px;
    height: 5px;
  }

  .route-marker--end {
    width: 20px;
    height: 20px;
  }

  .route-line {
    left: 12px;
    top: 25px;

    width: 3px;
    height: 45px;
  }

  .route-meta {
    font-size: 12px;

    line-height: 1.15;

    white-space: nowrap;
  }

  .route-content h2 {
    margin-top: 6px;

    font-size: 20px;

    line-height: 1.15;

    letter-spacing: -0.45px;
  }


  /* -------------------------------------------------------
     PRICE
  ------------------------------------------------------- */

  .price-block {
    padding-top: 1px;
  }

  .price-block strong {
    font-size: 28px;

    letter-spacing: -0.8px;
  }

  .price-block span {
    margin-top: 6px;

    font-size: 10px;
  }


  /* -------------------------------------------------------
     DIVIDER
  ------------------------------------------------------- */

  .card-divider {
    margin:
      22px
      0
      17px;
  }


  /* -------------------------------------------------------
     FOOTER
  ------------------------------------------------------- */

  .trip-footer {
    grid-template-columns:
      auto
      minmax(0, 1fr)
      auto;

    gap: 9px;
  }


  /* -------------------------------------------------------
     AVATARS
  ------------------------------------------------------- */

  .passenger-avatar {
    width: 40px;
    height: 40px;

    flex-basis: 40px;

    border-width: 2px;

    margin-left: -7px;
  }

  .passenger-avatar--empty svg {
    width: 19px;
    height: 19px;
  }

  .passenger-initials {
    font-size: 11px;
  }


  /* -------------------------------------------------------
     SEAT SUMMARY
  ------------------------------------------------------- */

  .seat-summary {
    gap: 3px;

    white-space: nowrap;
  }

  .seat-summary strong {
    font-size: 14px;
  }

  .seat-summary span {
    font-size: 13px;
  }


  /* -------------------------------------------------------
     VIEW
  ------------------------------------------------------- */

  .view-button {
    min-width: 68px;

    width: 68px;
    height: 50px;

    padding:
      0
      12px;

    border-radius: 17px;

    font-size: 15px;
  }


  /* -------------------------------------------------------
     PLUS
  ------------------------------------------------------- */

  .add-trip-button {
    width: 76px;
    height: 76px;

    bottom: 28px;

    border-radius: 22px;

    box-shadow:
      0 5px 12px rgba(
        255,
        77,
        45,
        0.10
      );
  }

  .add-trip-button:hover {
    box-shadow:
      0 7px 14px rgba(
        255,
        77,
        45,
        0.12
      );
  }

  .add-trip-button svg {
    width: 30px;
    height: 30px;
  }
}


/* =========================================================
   SMALL MOBILE
========================================================= */

@media (max-width: 360px) {

  .page-header {
    padding-left: 16px;
    padding-right: 16px;
  }

  .page-content {
    padding-left: 12px;
    padding-right: 12px;
  }

  .page-header h1 {
    font-size: 29px;
  }

  .page-header p {
    font-size: 17px;
  }

  .tab {
    font-size: 15px;
  }

  .trip-card {
    padding:
      17px
      14px
      16px;
  }

  .route-content h2 {
    font-size: 18px;
  }

  .price-block strong {
    font-size: 25px;
  }

  .seat-summary strong,
  .seat-summary span {
    font-size: 12px;
  }

  .view-button {
    width: 62px;
    min-width: 62px;

    font-size: 14px;
  }

  .passenger-avatar {
    width: 36px;
    height: 36px;

    flex-basis: 36px;
  }
}
</style>