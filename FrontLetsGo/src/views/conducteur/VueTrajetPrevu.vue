<template>
  <div class="trip-detail-page">
    <!-- =====================================================
         HEADER
    ====================================================== -->
    <header class="page-header">
      <button
        type="button"
        class="back-button"
        aria-label="Retour"
        @click="goBack"
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path d="M15 18L9 12L15 6" />
        </svg>
      </button>

      <h1>Trajet prévu</h1>
    </header>

    <!-- =====================================================
         MAIN
    ====================================================== -->
    <main class="page-content">

      <!-- ===================================================
           RÉSUMÉ DU TRAJET
      ==================================================== -->
      <section class="trip-summary">

        <!-- ROUTE -->
        <div class="route-column">

          <!-- ================= DÉPART ================= -->
          <div class="route-row">
            <div
              class="route-marker route-marker--start"
              aria-hidden="true"
            >
              <span></span>
            </div>

            <div
              class="route-connector"
              aria-hidden="true"
            ></div>

            <div class="route-information">
              <span class="route-meta">
                {{ trip.departureLabel }}
                <span class="route-dot">•</span>
                {{ trip.departureTime }}
              </span>

              <h2>
                {{ trip.departure }}
              </h2>
            </div>
          </div>

          <!-- ================= ARRIVÉE ================= -->
          <div class="route-row route-row--arrival">
            <div
              class="route-marker route-marker--arrival"
              aria-hidden="true"
            ></div>

            <div class="route-information">
              <span class="route-meta">
                {{ trip.arrivalLabel }}
                <span class="route-dot">•</span>
                {{ trip.arrivalTime }}
              </span>

              <h2>
                {{ trip.destination }}
              </h2>
            </div>
          </div>
        </div>

        <!-- ================= PRIX ================= -->
        <div class="price-summary">
          <strong>
            {{ formattedPrice }}
          </strong>

          <span>
            PAR PLACE
          </span>
        </div>
      </section>

      <!-- ===================================================
           ÉTAT AVEC RÉSERVATIONS
      ==================================================== -->
      <section
        v-if="hasReservations"
        class="reservations-section"
      >
        <!-- Compteur -->
        <div class="reservation-badge">
          {{ reservedSeats }}/{{ trip.totalSeats }}
          réservations
        </div>

        <!-- Liste des passagers -->
        <div class="passengers-list">
          <article
            v-for="passenger in trip.passengers"
            :key="passenger.id"
            class="passenger-card"
          >
            <!-- ================= IDENTITÉ ================= -->

            <div class="passenger-header">

              <div class="passenger-identity">

                <div class="passenger-avatar">

                  <!-- Photo disponible -->
                  <img
                    v-if="passenger.profilePhoto"
                    :src="passenger.profilePhoto"
                    :alt="
                      `Photo de ${getFullName(passenger)}`
                    "
                    class="passenger-photo"
                    @error="
                      handlePhotoError(passenger)
                    "
                  />

                  <!-- Initiales si aucune photo -->
                  <span
                    v-else
                    class="passenger-initials"
                  >
                    {{ getInitials(passenger) }}
                  </span>

                </div>

                <h3>
                  {{ getFullName(passenger) }}
                </h3>
              </div>

              <!-- Places réservées -->
              <div class="passenger-seats">

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

                <span>
                  {{ passenger.seatsReserved }}
                  {{
                    passenger.seatsReserved > 1
                      ? 'places'
                      : 'place'
                  }}
                </span>

              </div>
            </div>

            <!-- ================= MESSAGE ================= -->

            <div
              v-if="passenger.message"
              class="passenger-message"
            >
              <div
                class="message-icon"
                aria-hidden="true"
              >
                <svg
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M5 7a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v3a4 4 0 0 1-4 4h-3.8L7 18v-4.3A4 4 0 0 1 5 10V7Z"
                  />

                  <circle
                    cx="9"
                    cy="8.5"
                    r="0.8"
                  />

                  <circle
                    cx="12"
                    cy="8.5"
                    r="0.8"
                  />

                  <circle
                    cx="15"
                    cy="8.5"
                    r="0.8"
                  />
                </svg>
              </div>

              <p>
                "{{ passenger.message }}"
              </p>
            </div>
          </article>
        </div>
      </section>

      <!-- ===================================================
           ÉTAT SANS RÉSERVATION
      ==================================================== -->
      <section
        v-else
        class="empty-reservation-state"
        aria-live="polite"
      >
        <!-- Icône -->
        <div
          class="empty-state-icon"
          aria-hidden="true"
        >
          <svg
            viewBox="0 0 64 64"
            fill="none"
          >
            <!-- carrosserie -->
            <path
              d="M13 39h38"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
            />

            <path
              d="M17 39V31L21.5 21h21L47 31v8"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <!-- pare-brise -->
            <path
              d="M22 28h20"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
            />

            <!-- roues -->
            <circle
              cx="21"
              cy="43"
              r="4"
              fill="currentColor"
            />

            <circle
              cx="43"
              cy="43"
              r="4"
              fill="currentColor"
            />
          </svg>
        </div>

        <!-- Message principal -->
        <h2>
          Aucune réservation
        </h2>

        <p class="empty-state-text">
          Votre trajet est publié et reste disponible
          pour les passagers.
        </p>
      </section>

      <!-- ===================================================
           ACTIONS
      ==================================================== -->
      <section class="trip-actions">

        <!-- Modifier -->
        <button
          type="button"
          class="action-button action-button--primary"
          @click="editTrip"
        >
          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              d="M4 20h4l10.5-10.5a2.1 2.1 0 0 0-4-2.1L4 18v2Z"
            />

            <path d="M13.5 8.5l2 2" />
          </svg>

          <span>
            Modifier le trajet
          </span>
        </button>

        <!-- Annuler -->
        <button
          type="button"
          class="action-button action-button--danger"
          @click="openCancelModal"
        >
          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M6 6l12 12" />
            <path d="M18 6L6 18" />
          </svg>

          <span>
            Annuler le trajet
          </span>
        </button>
      </section>
    </main>

    <!-- =====================================================
         MODALE DE CONFIRMATION
    ====================================================== -->
    <Teleport to="body">
      <Transition name="cancel-modal">
        <div
          v-if="showCancelModal"
          class="cancel-overlay"
          role="dialog"
          aria-modal="true"
          aria-labelledby="cancel-title"
          @click.self="closeCancelModal"
        >
          <div class="cancel-modal">

            <!-- Icone -->
            <div
              class="cancel-icon"
              aria-hidden="true"
            >
              <svg
                viewBox="0 0 24 24"
              >
                <path
                  d="M12 3l9 17H3L12 3Z"
                />

                <path d="M12 9v4" />

                <circle
                  cx="12"
                  cy="16.5"
                  r="0.8"
                />
              </svg>
            </div>

            <!-- Titre -->
            <h2 id="cancel-title">
              Annuler ce trajet ?
            </h2>

            <!-- Explication -->
            <p>
              Le trajet sera retiré de vos trajets
              prévus et ne pourra plus recevoir
              de nouvelles réservations.
            </p>

            <!-- Actions -->
            <div class="cancel-actions">

              <button
                type="button"
                class="modal-secondary-button"
                :disabled="isCancelling"
                @click="closeCancelModal"
              >
                Retour
              </button>

              <button
                type="button"
                class="modal-danger-button"
                :disabled="isCancelling"
                @click="confirmCancel"
              >
                <span v-if="!isCancelling">
                  Annuler le trajet
                </span>

                <span
                  v-else
                  class="loading-state"
                >
                  <span class="spinner"></span>
                  Annulation...
                </span>
              </button>

            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>


<script setup>
import {
  computed,
  onMounted,
  onBeforeUnmount,
  reactive,
  ref
} from 'vue'

import { useRouter } from 'vue-router'


/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()


/* =========================================================
   ÉTAT MODALE
========================================================= */

const showCancelModal =
  ref(false)

const isCancelling =
  ref(false)


/* =========================================================
   TRAJET
   Données temporaires pour reproduire la maquette.
   Elles seront ensuite remplacées par Django / DRF.
========================================================= */

const trip = reactive({

  id: 1,

  departureLabel:
    'DEMAIN',

  departureTime:
    '08:30',

  departure:
    'Keur Massar',

  arrivalLabel:
    'ARRIVÉE',

  arrivalTime:
    '11:45',

  destination:
    'Ouakam',

  price:
    1500,

  totalSeats:
    5,

  /*
   * État demandé par ta maquette :
   * aucune réservation.
   *
   * Pour tester l'autre état, ajoute des passagers ici.
   */
  passengers: []
})


/* =========================================================
   RÉSERVATIONS
========================================================= */

const hasReservations =
  computed(() => {
    return trip.passengers.length > 0
  })


const reservedSeats =
  computed(() => {
    return trip.passengers.reduce(
      (total, passenger) => {
        return (
          total +
          Number(
            passenger.seatsReserved || 0
          )
        )
      },
      0
    )
  })


/* =========================================================
   PRIX
========================================================= */

const formattedPrice =
  computed(() => {
    return (
      new Intl.NumberFormat(
        'fr-FR'
      ).format(trip.price) +
      ' FCFA'
    )
  })


/* =========================================================
   PASSAGER
========================================================= */

const getFullName = (
  passenger
) => {
  return [
    passenger.firstName,
    passenger.lastName
  ]
    .filter(Boolean)
    .join(' ')
}


const getInitials = (
  passenger
) => {
  const first =
    passenger.firstName
      ?.trim()
      ?.charAt(0) || ''

  const last =
    passenger.lastName
      ?.trim()
      ?.charAt(0) || ''

  return (
    `${first}${last}`
  ).toUpperCase()
}


/*
 * Si une image de profil ne peut pas être
 * chargée, on repasse automatiquement aux initiales.
 */
const handlePhotoError = (
  passenger
) => {
  passenger.profilePhoto = null
}


/* =========================================================
   NAVIGATION
========================================================= */

const goBack = () => {
  if (
    window.history.length > 1
  ) {
    router.back()
    return
  }

  router.push(
    '/conducteur/trajets-prevus'
  )
}


const editTrip = () => {
  router.push({
    path:
      '/conducteur/publier-trajet',

    query: {
      edit:
        String(trip.id)
    }
  })
}


const goHome = () => {
  router.push('/')
}


/* =========================================================
   ANNULATION
========================================================= */

const openCancelModal = () => {
  showCancelModal.value =
    true
}


const closeCancelModal = () => {
  if (
    isCancelling.value
  ) {
    return
  }

  showCancelModal.value =
    false
}


const confirmCancel = async () => {
  if (
    isCancelling.value
  ) {
    return
  }

  isCancelling.value =
    true

  try {

    /*
     * Plus tard :
     *
     * await tripService.cancelTrip(trip.id)
     */

    console.log(
      'Annulation du trajet :',
      trip.id
    )

    /*
     * Une fois l'API confirmée :
     */
    showCancelModal.value =
      false

    router.push(
      '/conducteur/trajets-prevus'
    )

  } catch (error) {

    console.error(
      'Erreur lors de l’annulation :',
      error
    )

  } finally {

    isCancelling.value =
      false
  }
}


/* =========================================================
   ESCAPE
========================================================= */

const handleEscape = (
  event
) => {
  if (
    event.key === 'Escape' &&
    showCancelModal.value &&
    !isCancelling.value
  ) {
    closeCancelModal()
  }
}


onMounted(() => {
  document.addEventListener(
    'keydown',
    handleEscape
  )
})


onBeforeUnmount(() => {
  document.removeEventListener(
    'keydown',
    handleEscape
  )
})
</script>


<style scoped>
/* =========================================================
   TOKENS
========================================================= */

.trip-detail-page {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;

  --black: #111627;
  --dark-gray: #374151;

  --secondary: #8d939d;
  --muted: #aeb4bc;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;

  overflow-x: hidden;

  background: #f9fafb;

  color: var(--black);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  box-sizing: border-box;
}

.trip-detail-page *,
.trip-detail-page *::before,
.trip-detail-page *::after {
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

  padding-top: 44px;

  display: flex;
  align-items: center;

  gap: 20px;
}

.page-header h1 {
  margin: 0;

  color: var(--black);

  font-size: 36px;
  line-height: 1.15;

  font-weight: 800;

  letter-spacing: -1.2px;
}


/* =========================================================
   BACK BUTTON
========================================================= */

.back-button {
  width: 52px;
  height: 52px;

  flex: 0 0 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  border: 0;
  border-radius: 50%;

  background: #f0f1f3;

  color: var(--black);

  cursor: pointer;

  transition:
    background-color 180ms ease,
    transform 180ms ease;
}

.back-button:hover {
  background: #e8eaed;

  transform: translateX(-1px);
}

.back-button:active {
  transform: translateX(0);
}

.back-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 3px;
}

.back-button svg {
  width: 25px;
  height: 25px;

  fill: none;

  stroke: currentColor;

  stroke-width: 2.3;

  stroke-linecap: round;
  stroke-linejoin: round;
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
    60px
    0
    70px;
}


/* =========================================================
   TRIP SUMMARY
========================================================= */

.trip-summary {
  width: 100%;

  display: grid;

  grid-template-columns:
    minmax(0, 1fr)
    auto;

  gap: 22px;

  align-items: start;
}

.route-column {
  min-width: 0;
}


/* =========================================================
   ROUTE
========================================================= */

.route-row {
  position: relative;

  display: grid;

  grid-template-columns:
    32px
    minmax(0, 1fr);

  column-gap: 13px;
}

.route-row--arrival {
  margin-top: 26px;
}

.route-marker {
  width: 22px;
  height: 22px;

  margin-top: 2px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
}

.route-marker--start {
  border:
    4px solid
    var(--brand);

  background: #ffffff;
}

.route-marker--start span {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: var(--brand);
}

.route-marker--arrival {
  background: var(--brand);
}


/* =========================================================
   ROUTE CONNECTOR
========================================================= */

.route-connector {
  position: absolute;

  left: 9px;
  top: 28px;

  width: 4px;
  height: 61px;

  border-radius: 999px;

  background: #e2e5e8;
}


/* =========================================================
   ROUTE TEXT
========================================================= */

.route-information {
  min-width: 0;
}

.route-meta {
  display: block;

  color: #aeb4bc;

  font-size: 18px;
  line-height: 1.2;

  font-weight: 700;

  text-transform: uppercase;
}

.route-dot {
  margin:
    0
    2px;
}

.route-information h2 {
  min-width: 0;

  margin:
    7px
    0
    0;

  color: var(--black);

  font-size: 27px;
  line-height: 1.18;

  font-weight: 700;

  letter-spacing: -0.7px;

  overflow-wrap: anywhere;
}


/* =========================================================
   PRICE
========================================================= */

.price-summary {
  display: flex;
  flex-direction: column;

  align-items: flex-end;

  padding-top: 3px;

  text-align: right;
}

.price-summary strong {
  color: var(--brand);

  font-size: 34px;
  line-height: 1;

  font-weight: 800;

  letter-spacing: -1px;

  white-space: nowrap;
}

.price-summary span {
  margin-top: 8px;

  color: var(--muted);

  font-size: 14px;
  line-height: 1;

  font-weight: 700;

  white-space: nowrap;
}


/* =========================================================
   EMPTY STATE
========================================================= */

.empty-reservation-state {
  min-height: 430px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  padding:
    40px
    20px
    20px;

  text-align: center;
}

.empty-state-icon {
  width: 72px;
  height: 72px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 20px;

  background: #adb3bc;

  color: #ffffff;
}

.empty-state-icon svg {
  width: 48px;
  height: 48px;
}

.empty-reservation-state h2 {
  margin:
    22px
    0
    0;

  color: #969ca5;

  font-size: 22px;
  line-height: 1.3;

  font-weight: 600;
}

.empty-state-text {
  max-width: 360px;

  margin:
    10px
    auto
    0;

  color: #b2b7be;

  font-size: 14px;
  line-height: 1.55;

  font-weight: 500;
}


/* =========================================================
   RESERVATIONS
========================================================= */

.reservations-section {
  margin-top: 76px;
}

.reservation-badge {
  display: inline-flex;
  align-items: center;

  min-height: 50px;

  padding:
    0
    23px;

  border-radius: 999px;

  background: var(--black);

  color: #ffffff;

  font-size: 16px;
  font-weight: 700;
}

.passengers-list {
  display: flex;
  flex-direction: column;

  gap: 16px;

  margin-top: 18px;
}


/* =========================================================
   PASSENGER CARD
========================================================= */

.passenger-card {
  width: 100%;
  min-width: 0;

  padding:
    24px;

  border:
    1px solid
    #e1e4e8;

  border-radius: 27px;

  background: #ffffff;

  /*
   * Très faible pour garder le rendu propre.
   */
  box-shadow:
    0 2px 5px
    rgba(
      17,
      22,
      39,
      0.025
    );
}


/* =========================================================
   PASSENGER HEADER
========================================================= */

.passenger-header {
  min-width: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 16px;
}

.passenger-identity {
  min-width: 0;

  display: flex;
  align-items: center;

  gap: 16px;
}

.passenger-identity h3 {
  min-width: 0;

  margin: 0;

  color: var(--black);

  font-size: 22px;
  line-height: 1.2;

  font-weight: 700;

  overflow-wrap: anywhere;
}


/* =========================================================
   AVATAR
========================================================= */

.passenger-avatar {
  width: 68px;
  height: 68px;

  flex: 0 0 68px;

  overflow: hidden;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 19px;

  background: #f1f3f5;
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

  background:
    linear-gradient(
      135deg,
      #f0f2f4,
      #e5e8eb
    );

  color: var(--black);

  font-size: 20px;
  font-weight: 800;

  letter-spacing: -0.5px;
}


/* =========================================================
   PLACES
========================================================= */

.passenger-seats {
  min-height: 44px;

  display: inline-flex;
  align-items: center;

  gap: 8px;

  padding:
    0
    15px;

  border-radius: 14px;

  background: #fff0ec;

  color: var(--brand);

  font-size: 15px;

  font-weight: 700;

  white-space: nowrap;
}

.passenger-seats svg {
  width: 19px;
  height: 19px;

  fill: none;

  stroke: currentColor;

  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   PASSENGER MESSAGE
========================================================= */

.passenger-message {
  display: grid;

  grid-template-columns:
    48px
    minmax(0, 1fr);

  gap: 13px;

  margin-top: 21px;
}

.message-icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #f3f4f6;

  color: #a5abb3;
}

.message-icon svg {
  width: 22px;
  height: 22px;

  fill: none;

  stroke: currentColor;

  stroke-width: 1.7;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.passenger-message p {
  min-width: 0;

  margin: 0;

  color: #565d68;

  font-size: 16px;

  line-height: 1.55;

  font-style: italic;

  overflow-wrap: anywhere;
}


/* =========================================================
   ACTIONS
========================================================= */

.trip-actions {
  display: flex;
  flex-direction: column;

  gap: 15px;

  margin-top: 24px;
}

.action-button {
  width: 100%;
  min-height: 78px;

  display: flex;
  align-items: center;
  justify-content: center;

  gap: 13px;

  border-radius: 24px;

  font-family: inherit;

  font-size: 21px;

  font-weight: 700;

  cursor: pointer;

  transition:
    background-color 180ms ease,
    border-color 180ms ease,
    color 180ms ease,
    transform 180ms ease,
    box-shadow 180ms ease;
}

.action-button svg {
  width: 26px;
  height: 26px;

  fill: none;

  stroke: currentColor;

  stroke-width: 1.9;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.action-button:hover {
  transform: translateY(-1px);
}

.action-button:active {
  transform: translateY(0);
}

.action-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 3px;
}


/* =========================================================
   MODIFIER
========================================================= */

.action-button--primary {
  border: 0;

  background: var(--brand);

  color: #ffffff;

  box-shadow:
    0 6px 16px
    rgba(
      255,
      77,
      45,
      0.10
    );
}

.action-button--primary:hover {
  background: var(--brand-hover);

  box-shadow:
    0 8px 18px
    rgba(
      255,
      77,
      45,
      0.12
    );
}


/* =========================================================
   ANNULER
========================================================= */

.action-button--danger {
  border:
    1.5px solid
    var(--brand);

  background: #ffffff;

  color: var(--brand);
}

.action-button--danger:hover {
  background: #fff7f4;

  border-color: var(--brand-hover);

  color: var(--brand-hover);
}


/* =========================================================
   CANCEL OVERLAY
========================================================= */

.cancel-overlay {
  position: fixed;

  inset: 0;

  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;

  background:
    rgba(
      17,
      22,
      39,
      0.42
    );

  backdrop-filter: blur(4px);

  -webkit-backdrop-filter: blur(4px);
}


/* =========================================================
   CANCEL MODAL
========================================================= */

.cancel-modal {
  width: min(
    100%,
    470px
  );

  padding:
    32px
    28px
    28px;

  border-radius: 30px;

  background: #ffffff;

  text-align: center;

  /*
   * Shadow légère, pas de gros effet flottant.
   */
  box-shadow:
    0 12px 30px
    rgba(
      17,
      22,
      39,
      0.08
    );
}

.cancel-icon {
  width: 58px;
  height: 58px;

  margin: 0 auto;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 17px;

  background: #fff0ec;

  color: var(--brand);
}

.cancel-icon svg {
  width: 29px;
  height: 29px;

  fill: none;

  stroke: currentColor;

  stroke-width: 1.9;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.cancel-modal h2 {
  margin:
    21px
    0
    0;

  color: var(--black);

  font-size: 25px;

  line-height: 1.2;

  font-weight: 800;
}

.cancel-modal > p {
  margin:
    12px
    0
    0;

  color: #6b7280;

  font-size: 15px;

  line-height: 1.55;
}

.cancel-actions {
  display: grid;

  grid-template-columns:
    1fr
    1fr;

  gap: 10px;

  margin-top: 26px;
}

.modal-secondary-button,
.modal-danger-button {
  min-height: 51px;

  border-radius: 15px;

  font-family: inherit;

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;

  transition:
    background-color 180ms ease,
    color 180ms ease,
    opacity 180ms ease;
}

.modal-secondary-button {
  border:
    1px solid
    #e1e4e8;

  background: #f3f4f6;

  color: var(--black);
}

.modal-secondary-button:hover:not(:disabled) {
  background: #e9ebee;
}

.modal-danger-button {
  border: 0;

  background: var(--brand);

  color: #ffffff;
}

.modal-danger-button:hover:not(:disabled) {
  background: var(--brand-hover);
}

.modal-secondary-button:disabled,
.modal-danger-button:disabled {
  opacity: 0.6;

  cursor: not-allowed;
}


/* =========================================================
   LOADING
========================================================= */

.loading-state {
  display: inline-flex;
  align-items: center;

  gap: 9px;
}

.spinner {
  width: 17px;
  height: 17px;

  border:
    2px solid
    rgba(
      255,
      255,
      255,
      0.35
    );

  border-top-color: #ffffff;

  border-radius: 50%;

  animation:
    spin
    0.7s
    linear
    infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


/* =========================================================
   MODAL TRANSITION
========================================================= */

.cancel-modal-enter-active,
.cancel-modal-leave-active {
  transition:
    opacity 180ms ease;
}

.cancel-modal-enter-active
.cancel-modal,
.cancel-modal-leave-active
.cancel-modal {
  transition:
    opacity 180ms ease,
    transform 220ms ease;
}

.cancel-modal-enter-from,
.cancel-modal-leave-to {
  opacity: 0;
}

.cancel-modal-enter-from
.cancel-modal,
.cancel-modal-leave-to
.cancel-modal {
  opacity: 0;

  transform:
    translateY(8px)
    scale(0.98);
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 700px) {

  .page-header {
    width: calc(100% - 40px);

    padding-top: 34px;
  }

  .page-header h1 {
    font-size: 31px;
  }

  .page-content {
    width: calc(100% - 40px);

    padding-top: 46px;
  }

  .route-meta {
    font-size: 15px;
  }

  .route-information h2 {
    font-size: 23px;
  }

  .price-summary strong {
    font-size: 30px;
  }

  .price-summary span {
    font-size: 12px;
  }

  .empty-reservation-state {
    min-height: 380px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .page-header {
    width: 100%;

    padding:
      26px
      16px
      0;

    gap: 13px;
  }

  .back-button {
    width: 44px;
    height: 44px;

    flex-basis: 44px;
  }

  .back-button svg {
    width: 22px;
    height: 22px;
  }

  .page-header h1 {
    font-size: 25px;

    letter-spacing: -0.7px;
  }


  /* CONTENT */

  .page-content {
    width: 100%;

    padding:
      42px
      16px
      40px;
  }


  /* ROUTE */

  .trip-summary {
    grid-template-columns:
      minmax(0, 1fr)
      auto;

    gap: 8px;
  }

  .route-row {
    grid-template-columns:
      27px
      minmax(0, 1fr);

    column-gap: 8px;
  }

  .route-row--arrival {
    margin-top: 20px;
  }

  .route-marker {
    width: 19px;
    height: 19px;

    margin-top: 1px;
  }

  .route-marker--start {
    border-width: 3px;
  }

  .route-marker--start span {
    width: 5px;
    height: 5px;
  }

  .route-marker--arrival {
    width: 19px;
    height: 19px;
  }

  .route-connector {
    left: 8px;
    top: 24px;

    width: 3px;
    height: 45px;
  }

  .route-meta {
    font-size: 11px;
  }

  .route-information h2 {
    margin-top: 5px;

    font-size: 18px;

    line-height: 1.2;
  }

  .price-summary strong {
    font-size: 23px;

    letter-spacing: -0.5px;
  }

  .price-summary span {
    margin-top: 5px;

    font-size: 9px;
  }


  /* EMPTY */

  .empty-reservation-state {
    min-height: 370px;

    padding:
      30px
      15px
      10px;
  }

  .empty-state-icon {
    width: 62px;
    height: 62px;

    border-radius: 17px;
  }

  .empty-state-icon svg {
    width: 42px;
    height: 42px;
  }

  .empty-reservation-state h2 {
    margin-top: 18px;

    font-size: 18px;
  }

  .empty-state-text {
    max-width: 280px;

    font-size: 12px;
  }


  /* RESERVATIONS */

  .reservations-section {
    margin-top: 50px;
  }

  .reservation-badge {
    min-height: 43px;

    padding:
      0
      17px;

    font-size: 13px;
  }

  .passenger-card {
    padding:
      17px
      15px;

    border-radius: 22px;
  }

  .passenger-header {
    gap: 9px;
  }

  .passenger-identity {
    gap: 11px;
  }

  .passenger-avatar {
    width: 55px;
    height: 55px;

    flex-basis: 55px;

    border-radius: 16px;
  }

  .passenger-initials {
    font-size: 16px;
  }

  .passenger-identity h3 {
    font-size: 17px;
  }

  .passenger-seats {
    min-height: 37px;

    gap: 6px;

    padding:
      0
      10px;

    border-radius: 12px;

    font-size: 12px;
  }

  .passenger-seats svg {
    width: 16px;
    height: 16px;
  }


  /* MESSAGE */

  .passenger-message {
    grid-template-columns:
      40px
      minmax(0, 1fr);

    gap: 10px;

    margin-top: 18px;
  }

  .message-icon {
    width: 40px;
    height: 40px;
  }

  .message-icon svg {
    width: 18px;
    height: 18px;
  }

  .passenger-message p {
    font-size: 14px;
  }


  /* ACTIONS */

  .trip-actions {
    gap: 12px;

    margin-top: 24px;
  }

  .action-button {
    min-height: 64px;

    border-radius: 19px;

    font-size: 17px;
  }

  .action-button svg {
    width: 22px;
    height: 22px;
  }


  /* CANCEL MODAL */

  .cancel-overlay {
    padding:
      18px
      14px;
  }

  .cancel-modal {
    padding:
      28px
      20px
      22px;

    border-radius: 26px;
  }

  .cancel-modal h2 {
    font-size: 21px;
  }

  .cancel-modal > p {
    font-size: 13px;
  }

  .cancel-actions {
    grid-template-columns: 1fr;
  }
}


/* =========================================================
   VERY SMALL MOBILE
========================================================= */

@media (max-width: 360px) {

  .page-header {
    padding-left: 14px;
    padding-right: 14px;
  }

  .page-content {
    padding-left: 12px;
    padding-right: 12px;
  }

  .page-header h1 {
    font-size: 23px;
  }

  .route-meta {
    font-size: 9px;
  }

  .route-information h2 {
    font-size: 16px;
  }

  .price-summary strong {
    font-size: 20px;
  }

  .price-summary span {
    font-size: 8px;
  }

  .passenger-identity h3 {
    font-size: 16px;
  }

  .passenger-seats {
    padding:
      0
      8px;

    font-size: 10px;
  }

  .action-button {
    font-size: 15px;
  }
}
</style>