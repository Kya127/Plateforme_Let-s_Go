<script setup>
const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['select'])

function formatPrice(price) {
  return new Intl.NumberFormat('fr-FR').format(price)
}

function getInitials(name) {
  if (!name) return 'LG'
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word.charAt(0).toUpperCase())
    .join('')
}

function handleImageError(event) {
  event.target.style.display = 'none'
}
</script>

<template>
  <article
    class="trip-card"
    tabindex="0"
    role="button"
    @click="emit('select', trip)"
    @keydown.enter="emit('select', trip)"
  >
    <!-- PROFIL + PRIX -->
    <div class="trip-top">
      <!-- Conducteur -->
      <div class="driver-block">
        <div class="driver-avatar">
          <img
            v-if="trip.photo"
            :src="trip.photo"
            :alt="`Photo de ${trip.driver}`"
            @error="handleImageError"
          />
          <span v-else>
            {{ getInitials(trip.driver) }}
          </span>
        </div>

        <div class="driver-info">
          <h2>{{ trip.driver }}</h2>

          <div class="driver-rating">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M12 3.5l2.65 5.37 5.92.86-4.28 4.17 1.01 5.9L12 17.02 6.7 19.8l1.01-5.9-4.28-4.17 5.92-.86L12 3.5Z"
              />
            </svg>
            <strong>{{ trip.rating?.toFixed(1) || '4.9' }}</strong>
            <span>({{ trip.reviews || 0 }} avis)</span>
          </div>
        </div>
      </div>

      <!-- Prix -->
      <div class="trip-price">
        <strong>{{ formatPrice(trip.price) }}</strong>
        <span>FCFA/PLACE</span>
      </div>
    </div>

    <!-- Route Départ -> Arrivée -->
    <div v-if="trip.departure && trip.destination" class="trip-route-summary">
      <span class="route-depart-txt">{{ trip.departure }}</span>
      <span class="route-arrow-txt">➔</span>
      <span class="route-arrivee-txt">{{ trip.destination }}</span>
    </div>

    <!-- Séparateur -->
    <div class="trip-divider"></div>

    <!-- HORAIRES / DURÉE / PLACES -->
    <div class="trip-bottom">
      <!-- Heure -->
      <div class="trip-time">
        {{ trip.time }}
      </div>

      <!-- Ligne verticale -->
      <div class="trip-route-line">
        <span class="route-dot route-dot--top"></span>
        <span class="route-stem"></span>
        <span class="route-dot route-dot--bottom"></span>
      </div>

      <!-- Durée -->
      <div class="trip-duration">
        {{ trip.duration }}
      </div>

      <!-- Places -->
      <div
        class="available-seats"
        :class="{ 'available-seats--full': trip.availableSeats <= 0 }"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 16.5V11l1.7-4h10.6L19 11v5.5" />
          <path d="M4 16.5h16" />
          <circle cx="7" cy="17.5" r="1.5" />
          <circle cx="17" cy="17.5" r="1.5" />
        </svg>

        <span>
          {{ trip.availableSeats }}
          {{ trip.availableSeats > 1 ? 'PLACES' : 'PLACE' }}
        </span>
      </div>
    </div>
  </article>
</template>

<style scoped>
/* =========================================================
   CARD
========================================================= */
.trip-card {
  --brand: #ff4d2d;
  --black: #111627;
  --text-secondary: #6b7280;
  --white: #ffffff;

  box-sizing: border-box;
  min-width: 0;
  background: var(--white);
  border: 1px solid rgba(17, 22, 39, 0.05);
  border-radius: 28px;
  padding: 34px 38px 30px;
  box-shadow: 0 4px 12px rgba(17, 22, 39, 0.032);
  cursor: pointer;
  outline: none;
  font-family: 'Plus Jakarta Sans', Arial, sans-serif;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  animation: resultCardIn 0.45s ease both;
}

.trip-card *,
.trip-card *::before,
.trip-card *::after {
  box-sizing: border-box;
}

.trip-card:hover,
.trip-card:focus-visible {
  transform: translateY(-2px);
  border-color: rgba(255, 77, 45, 0.14);
  box-shadow: 0 9px 22px rgba(17, 22, 39, 0.049);
}

/* TOP CARD */
.trip-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

/* CONDUCTEUR */
.driver-block {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 16px;
}

.driver-avatar {
  width: 78px;
  height: 78px;
  flex: 0 0 78px;
  border-radius: 24px;
  background: linear-gradient(135deg, #cec7ad 0%, #aaa890 100%);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--black);
  font-size: 22px;
  font-weight: 800;
}

.driver-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.driver-info {
  min-width: 0;
}

.driver-info h2 {
  margin: 0 0 7px;
  font-size: 22px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.4px;
  color: var(--black);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.driver-rating {
  display: flex;
  align-items: center;
  gap: 5px;
  min-width: 0;
}

.driver-rating svg {
  width: 18px;
  height: 18px;
  fill: var(--brand);
  flex: 0 0 auto;
}

.driver-rating strong {
  color: var(--brand);
  font-size: 15px;
  font-weight: 800;
}

.driver-rating span {
  color: #a6adb8;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

/* PRIX */
.trip-price {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding-top: 1px;
}

.trip-price strong {
  color: var(--black);
  font-size: 36px;
  line-height: 0.95;
  font-weight: 800;
  letter-spacing: -1.5px;
  white-space: nowrap;
}

.trip-price span {
  margin-top: 7px;
  color: #9ea6b1;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  white-space: nowrap;
}

/* ROUTE RESUME */
.trip-route-summary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0 10px 0;
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.route-arrow-txt {
  color: #FF4D2D;
  font-size: 12px;
}

.route-depart-txt,
.route-arrivee-txt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

/* SÉPARATEUR */
.trip-divider {
  margin: 27px 0 24px;
  border-top: 2px dashed #edf0f3;
}

/* BOTTOM CARD */
.trip-bottom {
  display: flex;
  align-items: center;
  min-width: 0;
}

.trip-time {
  flex-shrink: 0;
  color: #262d3d;
  font-size: 32px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: -1px;
}

.trip-route-line {
  position: relative;
  width: 18px;
  height: 48px;
  margin: 0 18px 0 22px;
  flex: 0 0 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.route-stem {
  position: absolute;
  top: 9px;
  bottom: 9px;
  left: 50%;
  width: 2px;
  transform: translateX(-50%);
  background: var(--brand);
}

.route-dot {
  position: relative;
  z-index: 2;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--brand);
}

.route-dot--bottom {
  background: var(--white);
  border: 2px solid var(--brand);
}

.trip-duration {
  min-width: 0;
  color: #747e8d;
  font-size: 17px;
  line-height: 1;
  font-weight: 700;
  white-space: nowrap;
}

.available-seats {
  margin-left: auto;
  min-height: 48px;
  padding: 0 20px;
  border-radius: 999px;
  background: rgba(255, 77, 45, 0.06);
  color: var(--brand);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  white-space: nowrap;
}

.available-seats svg {
  width: 22px;
  height: 22px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.available-seats span {
  font-size: 15px;
  font-weight: 800;
}

.available-seats--full {
  background: #f7f8fa;
  color: #b7bdc7;
}

/* =========================================================
   ANIMATION
========================================================= */
@keyframes resultCardIn {
  from {
    opacity: 0;
    transform: translateY(9px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* =========================================================
   RESPONSIVE TABLET (max-width: 820px)
========================================================= */
@media (max-width: 820px) {
  /* Inherits grid-template-columns: 1fr from parent */
}

/* =========================================================
   RESPONSIVE MOBILE (max-width: 560px)
========================================================= */
@media (max-width: 560px) {
  .trip-card {
    border-radius: 28px;
    padding: 28px 21px 25px;
  }

  .trip-top {
    gap: 12px;
  }

  .driver-block {
    gap: 13px;
  }

  .driver-avatar {
    width: 68px;
    height: 68px;
    flex-basis: 68px;
    border-radius: 21px;
    font-size: 19px;
  }

  .driver-info h2 {
    max-width: 150px;
    font-size: 20px;
    margin-bottom: 6px;
  }

  .driver-rating svg {
    width: 17px;
    height: 17px;
  }

  .driver-rating strong {
    font-size: 14px;
  }

  .driver-rating span {
    font-size: 13px;
  }

  .trip-price strong {
    font-size: 25px;
    letter-spacing: -1.2px;
  }

  .trip-price span {
    font-size: 12px;
    margin-top: 6px;
  }

  .trip-divider {
    margin: 24px 0 22px;
  }

  .trip-bottom {
    gap: 0;
  }

  .trip-time {
    font-size: 28px;
  }

  .trip-route-line {
    width: 16px;
    height: 44px;
    margin: 0 11px 0 12px;
  }

  .route-dot {
    width: 11px;
    height: 11px;
  }

  .trip-duration {
    font-size: 16px;
  }

  .available-seats {
    min-height: 43px;
    padding: 0 14px;
    gap: 7px;
    margin-left: auto;
  }

  .available-seats svg {
    width: 20px;
    height: 20px;
  }

  .available-seats span {
    font-size: 13px;
  }
}

/* =========================================================
   PETITS ÉCRANS (max-width: 390px)
========================================================= */
@media (max-width: 390px) {
  .trip-card {
    padding: 25px 17px 22px;
  }

  .driver-avatar {
    width: 62px;
    height: 62px;
    flex-basis: 62px;
  }

  .driver-info h2 {
    max-width: 125px;
    font-size: 18px;
  }

  .driver-rating span {
    display: none;
  }

  .trip-price strong {
    font-size: 27px;
  }

  .trip-price span {
    font-size: 11px;
  }

  .trip-time {
    font-size: 25px;
  }

  .trip-duration {
    font-size: 14px;
  }

  .available-seats {
    padding: 0 11px;
  }

  .available-seats span {
    font-size: 11px;
  }
}
</style>
