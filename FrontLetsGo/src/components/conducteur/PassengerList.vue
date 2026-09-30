<script setup>
defineProps({
  passengers: {
    type: Array,
    default: () => [],
  },
  reservedSeats: {
    type: Number,
    default: 0,
  },
  totalSeats: {
    type: Number,
    default: 4,
  },
})

function getFullName(passenger) {
  if (!passenger) return 'Passager'
  return `${passenger.firstName || ''} ${passenger.lastName || ''}`.trim() || 'Passager'
}

function getInitials(passenger) {
  if (!passenger) return 'P'
  const first = passenger.firstName ? passenger.firstName[0] : ''
  const last = passenger.lastName ? passenger.lastName[0] : ''
  return (first + last).toUpperCase() || 'P'
}

function handlePhotoError(passenger) {
  passenger.profilePhoto = ''
}
</script>

<template>
  <div class="passengers-container">
    <!-- CAS A : IL Y A DES RÉSERVATIONS -->
    <section v-if="passengers && passengers.length > 0" class="reservations-section">
      <!-- Compteur de réservations -->
      <div class="reservation-badge">
        {{ reservedSeats }}/{{ totalSeats }} réservations confirmées
      </div>

      <!-- Liste des passagers confirmés -->
      <div class="passengers-list">
        <article
          v-for="passenger in passengers"
          :key="passenger.id"
          class="passenger-card"
        >
          <div class="passenger-header">
            <div class="passenger-identity">
              <!-- Photo ou initiales -->
              <div class="passenger-avatar">
                <img
                  v-if="passenger.profilePhoto"
                  :src="passenger.profilePhoto"
                  :alt="`Photo de ${getFullName(passenger)}`"
                  class="passenger-photo"
                  @error="handlePhotoError(passenger)"
                />
                <span v-else class="passenger-initials">
                  {{ getInitials(passenger) }}
                </span>
              </div>

              <div class="passenger-name-phone">
                <h3 class="passenger-full-name">{{ getFullName(passenger) }}</h3>
                <span v-if="passenger.telephone" class="passenger-phone">
                  {{ passenger.telephone }}
                </span>
              </div>
            </div>

            <!-- Places réservées -->
            <div class="passenger-seats">
              <svg viewBox="0 0 24 24" aria-hidden="true" width="16" height="16" fill="currentColor">
                <circle cx="12" cy="8" r="3.2" />
                <path d="M5 20c.7-3.5 3-5.5 7-5.5s6.3 2 7 5.5" />
              </svg>
              <span>
                {{ passenger.seatsReserved }}
                {{ passenger.seatsReserved > 1 ? 'places' : 'place' }}
              </span>
            </div>
          </div>

          <!-- Message optionnel du passager -->
          <div v-if="passenger.message" class="passenger-message">
            <p>"{{ passenger.message }}"</p>
          </div>
        </article>
      </div>
    </section>

    <!-- CAS B : AUCUNE RÉSERVATION -->
    <section v-else class="empty-reservation-state" aria-live="polite">
      <div class="empty-state-icon" aria-hidden="true">
        <svg viewBox="0 0 64 64" fill="none" width="48" height="48">
          <path d="M13 39h38" stroke="currentColor" stroke-width="3" stroke-linecap="round" />
          <path d="M17 39V31L21.5 21h21L47 31v8" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M22 28h20" stroke="currentColor" stroke-width="3" stroke-linecap="round" />
          <circle cx="21" cy="43" r="4" fill="currentColor" />
          <circle cx="43" cy="43" r="4" fill="currentColor" />
        </svg>
      </div>

      <h2 class="empty-title">Aucune réservation</h2>
      <p class="empty-state-text">
        Votre trajet est publié et reste disponible pour les passagers.
      </p>
    </section>
  </div>
</template>

<style scoped>
.passengers-container {
  display: flex;
  flex-direction: column;
}

.reservations-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reservation-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  background: #ECFDF5;
  color: #047857;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 700;
  width: fit-content;
}

.passengers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.passenger-card {
  padding: 16px 20px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.028);
}

.passenger-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.passenger-identity {
  display: flex;
  align-items: center;
  gap: 14px;
}

.passenger-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}

.passenger-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.passenger-initials {
  font-size: 15px;
  font-weight: 800;
  color: #4B5563;
}

.passenger-name-phone {
  display: flex;
  flex-direction: column;
}

.passenger-full-name {
  font-size: 15px;
  font-weight: 800;
  color: #111627;
  margin: 0;
  line-height: 1.25;
}

.passenger-phone {
  font-size: 12px;
  color: #6B7280;
  font-weight: 600;
  margin-top: 2px;
}

.passenger-seats {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #FF4D2D;
  background: #FFF5F2;
  padding: 6px 12px;
  border-radius: 9999px;
  flex-shrink: 0;
}

.passenger-message {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed #E5E7EB;
  font-size: 13px;
  font-style: italic;
  color: #4B5563;
}

.passenger-message p {
  margin: 0;
}

.empty-reservation-state {
  text-align: center;
  padding: 40px 24px;
  background: #FFFFFF;
  border: 1px dashed #E5E7EB;
  border-radius: 24px;
}

.empty-state-icon {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: #F8FAFC;
  color: #9CA3AF;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0 0 6px;
}

.empty-state-text {
  font-size: 13.5px;
  color: #6B7280;
  margin: 0;
}
</style>
