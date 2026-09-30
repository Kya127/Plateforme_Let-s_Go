<script setup>
defineProps({
  departure: {
    type: String,
    required: true,
  },
  departureTime: {
    type: String,
    default: '08:00',
  },
  destination: {
    type: String,
    required: true,
  },
  date: {
    type: String,
    default: '',
  },
  pricePerSeat: {
    type: [Number, String],
    required: true,
  },
})

function formaterDate(dateStr) {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('fr-FR', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
    })
  } catch (e) {
    return dateStr
  }
}

function formatNombre(val) {
  return Number(val || 0).toLocaleString('fr-FR')
}
</script>

<template>
  <section class="trip-summary">
    <!-- ROUTE -->
    <div class="route-column">
      <!-- DÉPART -->
      <div class="route-row">
        <div class="route-marker route-marker--start" aria-hidden="true">
          <span></span>
        </div>

        <div class="route-connector" aria-hidden="true"></div>

        <div class="route-information">
          <span class="route-meta">
            DÉPART
            <span class="route-dot">•</span>
            {{ departureTime }}
          </span>

          <h2 class="route-city-name">{{ departure }}</h2>
        </div>
      </div>

      <!-- ARRIVÉE -->
      <div class="route-row route-row--arrival">
        <div class="route-marker route-marker--arrival" aria-hidden="true"></div>

        <div class="route-information">
          <span class="route-meta">
            ARRIVÉE
            <span v-if="date" class="route-dot">•</span>
            {{ formaterDate(date) }}
          </span>

          <h2 class="route-city-name">{{ destination }}</h2>
        </div>
      </div>
    </div>

    <!-- PRIX PAR PLACE -->
    <div class="price-summary">
      <strong class="price-amount">{{ formatNombre(pricePerSeat) }} FCFA</strong>
      <span class="price-label">PAR PLACE</span>
    </div>
  </section>
</template>

<style scoped>
.trip-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.035);
}

.route-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  flex: 1;
}

.route-row {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  position: relative;
}

.route-marker {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
  z-index: 2;
}

.route-marker--start {
  background: #FFF5F2;
  border: 2px solid #FF4D2D;
}

.route-marker--start span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #FF4D2D;
}

.route-marker--arrival {
  background: #111627;
  border: 2px solid #111627;
}

.route-connector {
  position: absolute;
  top: 22px;
  left: 10px;
  width: 2px;
  height: calc(100% + 10px);
  background: #E5E7EB;
  z-index: 1;
}

.route-information {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.route-meta {
  font-size: 11px;
  font-weight: 700;
  color: #6B7280;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.route-dot {
  padding: 0 4px;
}

.route-city-name {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0;
  line-height: 1.25;
}

.price-summary {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
  flex-shrink: 0;
}

.price-amount {
  font-size: 20px;
  font-weight: 800;
  color: #FF4D2D;
  line-height: 1;
}

.price-label {
  font-size: 11px;
  font-weight: 700;
  color: #9CA3AF;
  letter-spacing: 0.6px;
  margin-top: 4px;
}

@media (max-width: 640px) {
  .trip-summary {
    padding: 18px;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .price-summary {
    align-items: flex-start;
    text-align: left;
    width: 100%;
    padding-top: 12px;
    border-top: 1px dashed #E5E7EB;
  }
  .route-city-name {
    font-size: 16px;
  }
}
</style>
