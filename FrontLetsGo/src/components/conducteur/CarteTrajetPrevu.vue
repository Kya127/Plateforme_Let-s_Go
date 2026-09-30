<script setup>
const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['view'])

function formatPrice(price) {
  return new Intl.NumberFormat('fr-FR', {
    maximumFractionDigits: 0,
  }).format(price)
}

function getInitials(firstName, lastName) {
  const first = firstName?.trim()?.charAt(0) || ''
  const last = lastName?.trim()?.charAt(0) || ''
  return `${first}${last}`.toUpperCase()
}

function visiblePassengers(trip) {
  if (!trip?.passengers) return []
  return trip.passengers.slice(0, 2)
}

function handleImageError(event) {
  event.target.style.display = 'none'
}

const mapLabels = {
  NON_FUMEUR: 'Non fumeur',
  'no-smoking': 'Non fumeur',
  ANIMAUX_OK: 'Animaux OK',
  pets: 'Animaux OK',
  GROS_BAGAGES: 'Gros bagages',
  luggage: 'Gros bagages',
  MUSIQUE_OK: 'Musique',
  music: 'Musique',
  CLIMATISEE: 'Climatisé',
  ac: 'Climatisé',
}

function normaliserPreferences(prefs) {
  if (!Array.isArray(prefs)) return []
  return prefs.map((p) => mapLabels[p] || String(p).replace(/_/g, ' '))
}
</script>

<template>
  <article class="trip-card">
    <!-- TOP : INFORMATIONS TRAJET -->
    <div class="trip-main">
      <!-- Colonne trajet -->
      <div class="route-column">
        <!-- Départ -->
        <div class="route-row">
          <div class="route-marker route-marker--start" aria-hidden="true">
            <span></span>
          </div>

          <div class="route-line"></div>

          <div class="route-content">
            <span class="route-meta">
              {{ trip.departureLabel }}
              <span class="bullet">•</span>
              {{ trip.departureTime }}
            </span>

            <h2>{{ trip.departure }}</h2>
          </div>
        </div>

        <!-- Arrivée -->
        <div class="route-row route-row--arrival">
          <div class="route-marker route-marker--end" aria-hidden="true"></div>

          <div class="route-content">
            <span class="route-meta">
              {{ trip.arrivalLabel }}
              <span class="bullet">•</span>
              {{ trip.arrivalTime }}
            </span>

            <h2>{{ trip.destination }}</h2>
          </div>
        </div>
      </div>

      <!-- Prix -->
      <div class="price-block">
        <strong>{{ formatPrice(trip.price) }} FCFA</strong>
        <span>PAR PLACE</span>
      </div>
    </div>

    <!-- PRÉFÉRENCES & DESCRIPTION SI EXISTANTES -->
    <div v-if="(trip.preferences && trip.preferences.length > 0) || trip.description" class="card-details-preview">
      <div v-if="trip.preferences && trip.preferences.length > 0" class="chips-row">
        <span
          v-for="(pref, pIdx) in normaliserPreferences(trip.preferences)"
          :key="pIdx"
          class="pref-tag"
        >
          {{ pref }}
        </span>
      </div>
      <p v-if="trip.description" class="desc-preview">
        {{ trip.description }}
      </p>
    </div>

    <!-- DIVIDER -->
    <div class="card-divider"></div>

    <!-- BOTTOM : PASSAGERS & ACTIONS -->
    <div class="trip-footer">
      <!-- Passagers -->
      <div
        class="passengers"
        :aria-label="`${trip.seatsTaken} passager(s) sur ${trip.seatsTotal}`"
      >
        <!-- Profils réels -->
        <div
          v-for="passenger in visiblePassengers(trip)"
          :key="passenger.id"
          class="passenger-avatar"
          :title="`${passenger.firstName} ${passenger.lastName}`"
        >
          <!-- Photo disponible -->
          <img
            v-if="passenger.profilePhoto"
            :src="passenger.profilePhoto"
            :alt="`Photo de ${passenger.firstName} ${passenger.lastName}`"
            class="passenger-photo"
            @error="handleImageError"
          />

          <!-- Initiales -->
          <span
            v-else
            class="passenger-initials"
            :aria-label="`Passager ${getInitials(passenger.firstName, passenger.lastName)}`"
          >
            {{ getInitials(passenger.firstName, passenger.lastName) }}
          </span>
        </div>

        <!-- Place libre -->
        <div
          v-if="trip.seatsTaken < trip.seatsTotal"
          class="passenger-avatar passenger-avatar--empty"
          title="Place disponible"
          aria-label="Place disponible"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="8" r="3.2" />
            <path d="M5 20c.7-3.5 3-5.5 7-5.5s6.3 2 7 5.5" />
          </svg>
        </div>
      </div>

      <!-- Compteur -->
      <div class="seat-summary">
        <strong>{{ trip.seatsTaken }} / {{ trip.seatsTotal }}</strong>
        <span>places prises</span>
      </div>

      <!-- Voir -->
      <button
        type="button"
        class="view-button"
        @click="emit('view', trip)"
      >
        Voir
      </button>
    </div>
  </article>
</template>

<style scoped>
/* =========================================================
   VARIABLES & DESIGN TOKENS
========================================================= */
.trip-card {
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

  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  padding: 30px 28px 26px;
  border: 1px solid #dfe2e6;
  border-radius: 34px;
  background: #ffffff;
  box-shadow: 0 2px 5px rgba(17, 22, 39, 0.017);
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.trip-card *,
.trip-card *::before,
.trip-card *::after {
  box-sizing: border-box;
}

/* =========================================================
   MAIN
========================================================= */
.trip-main {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
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
  grid-template-columns: 36px minmax(0, 1fr);
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
  margin: 0 2px;
}

.route-content h2 {
  min-width: 0;
  margin: 8px 0 0;
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
  margin: 31px 0 22px;
  background: #eceef0;
}

/* =========================================================
   FOOTER
========================================================= */
.trip-footer {
  min-width: 0;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
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
  padding: 0 20px;
  border: 0;
  border-radius: 25px;
  background: var(--black);
  color: #ffffff;
  font-family: inherit;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 180ms ease, transform 180ms ease;
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
   TABLET (max-width: 700px)
========================================================= */
@media (max-width: 700px) {
  .trip-card {
    padding: 25px 22px 22px;
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
   MOBILE (max-width: 520px)
========================================================= */
@media (max-width: 520px) {
  .trip-card {
    padding: 20px 17px 18px;
    border-radius: 28px;
  }

  .trip-main {
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 10px;
  }

  .route-row {
    grid-template-columns: 28px minmax(0, 1fr);
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

  .card-divider {
    margin: 22px 0 17px;
  }

  .trip-footer {
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 9px;
  }

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

  .view-button {
    min-width: 68px;
    width: 68px;
    height: 50px;
    padding: 0 12px;
    border-radius: 17px;
    font-size: 15px;
  }
}

/* =========================================================
   SMALL MOBILE (max-width: 360px)
========================================================= */
@media (max-width: 360px) {
  .trip-card {
    padding: 17px 14px 16px;
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

.card-details-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #F9FAFB;
  border-radius: 14px;
  padding: 10px 14px;
  border: 1px solid #F3F4F6;
  margin: 12px 0 6px 0;
}

.chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.pref-tag {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  color: #374151;
}

.desc-preview {
  margin: 0;
  font-size: 12px;
  color: #4B5563;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
