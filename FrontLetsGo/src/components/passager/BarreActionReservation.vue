<script setup>
defineProps({
  totalPrice: {
    type: [Number, String],
    required: true,
  },
  availableSeats: {
    type: Number,
    default: 0,
  },
  estMonTrajet: {
    type: Boolean,
    default: false,
  },
  dejaReserve: {
    type: Boolean,
    default: false,
  },
  nombrePlacesDejaReservees: {
    type: Number,
    default: 1,
  },
  isBooking: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['reserver', 'gerer-espace-conducteur', 'voir-reservation'])

function formatPrice(val) {
  return Number(val || 0).toLocaleString('fr-FR')
}
</script>

<template>
  <aside class="trip-sidebar-column">
    <div class="sticky-booking-panel">
      <!-- En-tête prix desktop -->
      <div class="desktop-price-box">
        <span class="desktop-price-label">PRIX DU TRAJET</span>
        <div class="desktop-price-val-row">
          <span class="desktop-price-digits">{{ formatPrice(totalPrice) }}</span>
          <span class="desktop-price-curr">FCFA <small>/ place</small></span>
        </div>
        <div class="desktop-seats-pill" :class="availableSeats > 0 ? 'pill-available' : 'pill-full'">
          <span class="seats-dot"></span>
          <span>{{ availableSeats > 0 ? `${availableSeats} place(s) disponible(s)` : 'Complet' }}</span>
        </div>
      </div>

      <div class="panel-inner-divider"></div>

      <!-- Bloc CTA : Conducteur / Déjà réservé / Réserver -->
      <div class="panel-cta-zone">
        <!-- Cas 1 : L'utilisateur connecté est le conducteur du trajet -->
        <div v-if="estMonTrajet" class="conducteur-notice-box">
          <p class="conducteur-notice-txt">Vous êtes le conducteur de ce trajet.</p>
          <button
            type="button"
            class="reserve-cta-btn btn-conducteur-espace"
            @click="$emit('gerer-espace-conducteur')"
          >
            Gérer mon trajet dans mon espace
          </button>
        </div>

        <!-- Cas 2 : L'utilisateur connecté a DÉJÀ une réservation active -->
        <div v-else-if="dejaReserve" class="deja-reserve-notice-box">
          <div class="deja-reserve-header">
            <div class="deja-reserve-icon-wrapper" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="deja-reserve-text-col">
              <span class="deja-reserve-badge">PLACE DÉJÀ RÉSERVÉE</span>
              <h3 class="deja-reserve-title">Vous êtes inscrit sur ce trajet</h3>
              <p class="deja-reserve-desc">
                Vous avez réservé <strong>{{ nombrePlacesDejaReservees }} place{{ nombrePlacesDejaReservees > 1 ? 's' : '' }}</strong>. Pour éviter le surbooking et les doublons, il n'est pas possible de réserver deux fois sur le même trajet.
              </p>
            </div>
          </div>

          <button
            type="button"
            class="reserve-cta-btn btn-voir-reservation"
            @click="$emit('voir-reservation')"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon-reserve">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            Voir le reçu de ma réservation
          </button>
        </div>

        <!-- Cas 3 : Passager standard qui peut réserver -->
        <div v-else class="cta-wrapper">
          <button
            type="button"
            class="reserve-cta-btn"
            :disabled="availableSeats <= 0 || isBooking"
            @click="$emit('reserver')"
          >
            <span v-if="availableSeats <= 0">Complet</span>
            <span v-else-if="!isBooking">Réserver maintenant</span>
            <span v-else class="loading-state">
              <span class="btn-spinner"></span>
              Réservation...
            </span>
          </button>
        </div>
      </div>

      <!-- Garanties Let's Go pour rassurer le passager -->
      <div class="guarantees-list">
        <div class="guarantee-item">
          <div class="guarantee-icon-box" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
              <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
            </svg>
          </div>
          <div class="guarantee-text">
            <strong>Sécurité Let's Go</strong>
            <span>Conducteur vérifié & permis contrôlé</span>
          </div>
        </div>

        <div class="guarantee-item">
          <div class="guarantee-icon-box" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14h2v2h-2v-2zm0-10h2v8h-2V6z"/>
            </svg>
          </div>
          <div class="guarantee-text">
            <strong>Garantie anti-surbooking</strong>
            <span>Places réservées en temps réel</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.trip-sidebar-column {
  width: 100%;
}

.sticky-booking-panel {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.035);
  position: sticky;
  top: 96px;
}

.desktop-price-box {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.desktop-price-label {
  font-size: 11px;
  font-weight: 700;
  color: #9CA3AF;
  letter-spacing: 0.6px;
}

.desktop-price-val-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.desktop-price-digits {
  font-size: 32px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -0.5px;
}

.desktop-price-curr {
  font-size: 16px;
  font-weight: 700;
  color: #FF4D2D;
}

.desktop-price-curr small {
  font-size: 12px;
  color: #6B7280;
  font-weight: 500;
}

.desktop-seats-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  width: fit-content;
  margin-top: 4px;
}

.pill-available {
  background: #ECFDF5;
  color: #047857;
}

.pill-available .seats-dot {
  background: #10B981;
}

.pill-full {
  background: #FEF2F2;
  color: #B91C1C;
}

.pill-full .seats-dot {
  background: #EF4444;
}

.seats-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.panel-inner-divider {
  height: 1px;
  background: #F3F4F6;
  margin: 18px 0;
}

.panel-cta-zone {
  margin-bottom: 20px;
}

.reserve-cta-btn {
  width: 100%;
  height: 52px;
  border-radius: 16px;
  background: #FF4D2D;
  color: #FFFFFF;
  border: none;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(255, 77, 45, 0.12);
  transition: all 0.18s ease;
  font-family: inherit;
}

.reserve-cta-btn:hover:not(:disabled) {
  background: #E83F20;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(255, 77, 45, 0.16);
}

.reserve-cta-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-conducteur-espace {
  background: #111627;
  box-shadow: 0 4px 14px rgba(17, 22, 39, 0.09);
}

.btn-conducteur-espace:hover:not(:disabled) {
  background: #1E293B;
}

.conducteur-notice-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.conducteur-notice-txt {
  font-size: 13px;
  color: #6B7280;
  margin: 0;
}

.deja-reserve-notice-box {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  border-radius: 18px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.deja-reserve-header {
  display: flex;
  gap: 12px;
}

.deja-reserve-icon-wrapper {
  flex-shrink: 0;
  margin-top: 2px;
}

.deja-reserve-text-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.deja-reserve-badge {
  font-size: 10.5px;
  font-weight: 800;
  color: #059669;
  letter-spacing: 0.5px;
}

.deja-reserve-title {
  font-size: 14px;
  font-weight: 800;
  color: #064E3B;
  margin: 0;
}

.deja-reserve-desc {
  font-size: 12px;
  color: #047857;
  line-height: 1.4;
  margin: 0;
}

.btn-voir-reservation {
  background: #059669;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.1);
  font-size: 14px;
  height: 46px;
}

.btn-voir-reservation:hover:not(:disabled) {
  background: #047857;
}

.btn-icon-reserve {
  flex-shrink: 0;
}

.guarantees-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #F3F4F6;
}

.guarantee-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.guarantee-icon-box {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #F3F4F6;
  color: #4B5563;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.guarantee-text {
  display: flex;
  flex-direction: column;
}

.guarantee-text strong {
  font-size: 12px;
  color: #111627;
}

.guarantee-text span {
  font-size: 11px;
  color: #6B7280;
}

.loading-state {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
