<template>
  <div class="payment-page">
    <div class="payment-container">

      <!-- =====================================================
           HEADER HERO (RESPONSIVE DESKTOP & MOBILE)
      ====================================================== -->
      <header class="completion-hero">
        <button
          type="button"
          class="hero-back-btn"
          aria-label="Retour"
          @click="goBack"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>

        <div class="hero-content-group">
          <!-- Cercle de succès avec coche verte -->
          <div class="hero-check-circle" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>

          <div class="hero-text-block">
            <h1 class="hero-title">Trajet Terminé !</h1>
            <p class="hero-subtitle">MERCI POUR VOTRE SERVICE</p>
          </div>
        </div>
      </header>

      <!-- =====================================================
           CORPS DU DOCUMENT : GRILLE HARMONIEUSE SUR DESKTOP
      ====================================================== -->
      <main class="payment-content-grid">

        <!-- COLONNE GAUCHE (Détails du trajet, Récapitulatif, Véhicule) -->
        <div class="payment-col-left">

          <!-- 1. ITINÉRAIRE & DATE -->
          <section class="content-card section-route-date">
            <div class="route-date-labels">
              <span class="meta-label">ITINÉRAIRE</span>
              <span class="meta-label text-right">DATE</span>
            </div>
            <div class="route-date-values">
              <div class="route-text">
                <span class="city-name">{{ trip.departure }}</span>
                <span class="route-arrow" aria-hidden="true">↑</span>
                <span class="city-name">{{ trip.destination }}</span>
              </div>
              <div class="date-text">{{ trip.date }}</div>
            </div>
          </section>

          <!-- 2. RÉCAPITULATIF FINANCIER -->
          <section class="content-card section-financial">
            <h2 class="section-title">RÉCAPITULATIF FINANCIER</h2>

            <div class="financial-card">
              <div class="financial-row">
                <span class="f-label">Revenu total ({{ trip.passengers }} passagers)</span>
                <strong class="f-val">{{ formatMoney(trip.totalRevenue) }}</strong>
              </div>

              <div class="financial-row">
                <span class="f-label">Frais de plateforme ({{ trip.platformRate }}%)</span>
                <strong class="f-val text-fee">- {{ formatMoney(trip.platformFee) }}</strong>
              </div>

              <div class="financial-divider"></div>

              <div class="financial-row financial-row--net">
                <span class="f-label-net">Votre gain net</span>
                <strong class="f-val-net">{{ formatMoney(trip.netRevenue) }}</strong>
              </div>
            </div>
          </section>

          <!-- 3. ENCART DU VÉHICULE DU CONDUCTEUR -->
          <section class="content-card section-vehicle-card">
            <div class="vehicle-icon-box" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.5 2.8C2.1 11 2 11.5 2 12v4c0 .6.4 1 1 1h2"></path>
                <circle cx="7" cy="17" r="2"></circle>
                <path d="M9 17h6"></path>
                <circle cx="17" cy="17" r="2"></circle>
              </svg>
            </div>
            <div class="vehicle-info-text">
              <strong class="vehicle-name">{{ trip.vehicle.name }}</strong>
              <span class="vehicle-meta">{{ trip.vehicle.plate }} • {{ trip.vehicle.color }}</span>
            </div>
          </section>

        </div>

        <!-- COLONNE DROITE (Commission & Mode de paiement) -->
        <div class="payment-col-right">

          <!-- 4. ENCART COMMISSION EN ATTENTE (FOND ROSE/SAUMON) -->
          <section class="section-commission-card">
            <div class="commission-badge-pill">
              <span class="dot-red" aria-hidden="true"></span>
              <span>COMMISSION EN ATTENTE</span>
            </div>

            <div class="commission-amount-caption">MONTANT À RÉGLER</div>

            <div class="commission-amount-display">
              <span class="amount-digits">{{ formatNumber(trip.amountDue) }}</span>
              <span class="amount-currency">FCFA</span>
            </div>
          </section>

          <!-- 5. MODE DE PAIEMENT (WAVE / ORANGE MONEY) -->
          <section class="content-card section-payment-method">
            <div class="method-header-row">
              <h2 class="section-title">MODE DE PAIEMENT</h2>
              <span class="method-caption">Choisissez votre compte :</span>
            </div>

            <div class="method-cards-list">

              <!-- OPTION WAVE -->
              <div
                class="method-option-card"
                :class="{ 'method-option-card--active': selectedProvider === 'wave' }"
                role="radio"
                tabindex="0"
                :aria-checked="selectedProvider === 'wave'"
                @click="selectedProvider = 'wave'"
                @keydown.space.prevent="selectedProvider = 'wave'"
                @keydown.enter.prevent="selectedProvider = 'wave'"
              >
                <div class="method-left-group">
                  <div class="provider-logo-container wave-bg">
                    <img
                      src="/images/Image wave.png"
                      alt="Logo Wave"
                      class="provider-logo-img"
                      @error="fallbackWaveImg"
                    />
                  </div>
                  <div class="provider-meta">
                    <div class="provider-title-row">
                      <strong class="provider-name">Wave</strong>
                      <span class="tag-badge tag-badge--wave">Instantané</span>
                    </div>
                    <span class="provider-desc">Débit direct sans frais</span>
                  </div>
                </div>

                <!-- Case à cocher personnalisée Wave (Cyan cochée) -->
                <div
                  class="method-checkbox"
                  :class="{ 'method-checkbox--checked': selectedProvider === 'wave' }"
                  aria-hidden="true"
                >
                  <svg v-if="selectedProvider === 'wave'" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              </div>

              <!-- OPTION ORANGE MONEY -->
              <div
                class="method-option-card"
                :class="{ 'method-option-card--active': selectedProvider === 'om' }"
                role="radio"
                tabindex="0"
                :aria-checked="selectedProvider === 'om'"
                @click="selectedProvider = 'om'"
                @keydown.space.prevent="selectedProvider = 'om'"
                @keydown.enter.prevent="selectedProvider = 'om'"
              >
                <div class="method-left-group">
                  <div class="provider-logo-container om-bg">
                    <img
                      src="/images/Image orange money.png"
                      alt="Logo Orange Money"
                      class="provider-logo-img"
                      @error="fallbackOmImg"
                    />
                  </div>
                  <div class="provider-meta">
                    <div class="provider-title-row">
                      <strong class="provider-name">Orange Money</strong>
                      <span class="tag-badge tag-badge--om">OTP / USSD</span>
                    </div>
                    <span class="provider-desc">Paiement sécurisé mobile</span>
                  </div>
                </div>

                <!-- Case à cocher personnalisée Orange Money -->
                <div
                  class="method-checkbox method-checkbox--om"
                  :class="{ 'method-checkbox--checked-om': selectedProvider === 'om' }"
                  aria-hidden="true"
                >
                  <svg v-if="selectedProvider === 'om'" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              </div>

            </div>
          </section>

          <!-- MESSAGE D'ERREUR ÉVENTUEL -->
          <div v-if="errorMessage" class="error-banner" role="alert">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{{ errorMessage }}</span>
          </div>

          <!-- 6. BOUTON D'ACTION PRINCIPAL -->
          <div class="action-footer">
            <button
              type="button"
              class="btn-submit-payment"
              :disabled="isProcessing"
              @click="handlePayCommissionClick"
            >
              <span v-if="!isProcessing" class="btn-label-row">
                <span>Payer la commission</span>
                <span class="btn-amount-chip">{{ formatMoney(trip.amountDue) }}</span>
              </span>
              <span v-else class="btn-loading-row">
                <span class="spinner-dot"></span>
                <span>Redirection PayTech...</span>
              </span>
            </button>

            <p class="security-caption">
              Paiement 100% sécurisé via PayTech • Redirection instantanée
            </p>
          </div>

        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { serviceCommissions } from '@/services/api'

const router = useRouter()
const route = useRoute()

const isProcessing = ref(false)
const errorMessage = ref('')
const selectedProvider = ref('wave') // 'wave' ou 'om'

const trip = reactive({
  id: null,
  commissionId: null,
  departure: 'Fass',
  destination: 'Colobane',
  date: '4 oct. 2026',
  passengers: 3,
  totalRevenue: 3000,
  platformRate: 10,
  platformFee: 300,
  netRevenue: 2700,
  amountDue: 300,
  vehicle: {
    name: 'Hundai Tucson',
    plate: 'AB-123-CD',
    color: 'BLANC NACRÉ'
  }
})

const selectedProviderLabel = computed(() => {
  return selectedProvider.value === 'om' ? 'Orange Money' : 'Wave'
})

function fallbackWaveImg(e) {
  e.target.src = '/images/wave_logo.png'
}

function fallbackOmImg(e) {
  e.target.src = '/images/orange_money_logo.png'
}

onMounted(async () => {
  const tripId = route.query.id || route.query.trajet_id || route.params.id || 4

  // Si on reçoit déjà une notification de paiement réussi, valider et rediriger
  if (route.query.status === 'success' || route.query.ref) {
    try {
      const commId = route.query.commission_id || 1
      await serviceCommissions.validerPaiement(commId, {
        reference: route.query.ref || `COMM-${tripId}-OK`
      })
    } catch (e) {
      console.warn('Validation BDD post-PayTech :', e)
    }

    router.replace({
      path: '/vue-trajet',
      query: {
        id: String(tripId),
        status: 'success',
        ref: route.query.ref || `COMM-${tripId}-OK`,
        commission_paid: 'true'
      }
    })
    return
  }

  // Chargement des données réelles de commission et de trajet
  try {
    const data = await serviceCommissions.getCommissionTrajet(tripId)
    if (data) {
      trip.id = data.trajet_id || tripId
      trip.commissionId = data.id
      trip.departure = data.depart || trip.departure
      trip.destination = data.destination || trip.destination
      trip.passengers = data.passagers || trip.passengers
      trip.totalRevenue = data.revenu_total || trip.totalRevenue
      trip.platformRate = data.taux_commission || trip.platformRate
      trip.platformFee = data.montant_commission || trip.platformFee
      trip.netRevenue = data.gain_net || trip.netRevenue
      trip.amountDue = data.montant_commission || trip.amountDue

      if (data.date) {
        const d = new Date(data.date)
        if (!isNaN(d.getTime())) {
          trip.date = d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })
        }
      }

      if (data.voiture) {
        trip.vehicle.name = data.voiture.name || trip.vehicle.name
        trip.vehicle.plate = data.voiture.plate || trip.vehicle.plate
        trip.vehicle.color = data.voiture.color || trip.vehicle.color
      }
    }
  } catch (err) {
    console.warn('Utilisation des données de trajet par défaut :', err)
  }
})

function formatNumber(value) {
  return new Intl.NumberFormat('fr-FR').format(value || 0)
}

function formatMoney(value) {
  return `${formatNumber(value)} FCFA`
}

function goBack() {
  if (trip.id) {
    router.push({ path: '/vue-trajet', query: { id: String(trip.id) } })
  } else if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/conducteur/tableau-de-bord')
  }
}

async function handlePayCommissionClick() {
  errorMessage.value = ''
  isProcessing.value = true

  try {
    const commissionId = trip.commissionId || 1
    const initRes = await serviceCommissions.initierPaiement(commissionId, {
      methode_paiement: selectedProviderLabel.value
    })

    if (initRes && initRes.redirect_url) {
      window.location.href = initRes.redirect_url
    } else {
      throw new Error("L'URL de paiement PayTech n'a pas pu être générée.")
    }
  } catch (err) {
    console.error('Erreur initialisation paiement :', err)
    errorMessage.value = err.response?.data?.detail || err.message || 'Impossible de joindre le portail PayTech. Veuillez réessayer.'
    isProcessing.value = false
  }
}
</script>

<style scoped>
/* =========================================================
   PAGE GLOBALE (COHÉRENCE PLATEFORME SANS AUCUN BOX-SHADOW)
========================================================= */
.payment-page {
  --brand-primary: #FF4D2D;
  --brand-hover: #F04427;
  --text-dark: #111827;
  --text-muted: #64748B;
  --text-light-gray: #94A3B8;
  --border-color: #E2E8F0;
  --border-light: #F1F5F9;
  --emerald-green: #059669;
  --coral-red: #EF4444;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;
  background-color: #F8FAFC;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 0;
  margin: 0;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--text-dark);
  box-sizing: border-box;
}

@media (min-width: 900px) {
  .payment-page {
    padding: 32px 24px 60px;
  }
}

/* CONTENEUR PRINCIPAL */
.payment-container {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

@media (min-width: 900px) {
  .payment-container {
    max-width: 1000px;
    gap: 24px;
  }
}

/* =========================================================
   1. HERO SOMBRE "Trajet Terminé !"
========================================================= */
.completion-hero {
  background: linear-gradient(135deg, #182337 0%, #111927 100%);
  padding: 24px 20px 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  border-bottom: 1px solid #1E293B;
}

@media (min-width: 900px) {
  .completion-hero {
    border-radius: 20px;
    border: 1px solid #1E293B;
    padding: 24px 32px;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    text-align: left;
    gap: 24px;
  }
}

.hero-back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 38px;
  height: 38px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

@media (min-width: 900px) {
  .hero-back-btn {
    position: static;
    flex-shrink: 0;
  }
}

.hero-back-btn:hover {
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.3);
}

.hero-content-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

@media (min-width: 900px) {
  .hero-content-group {
    flex-direction: row;
    align-items: center;
    gap: 20px;
    margin-top: 0;
  }
}

.hero-check-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #C7F9E5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.hero-text-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hero-title {
  color: #FFFFFF;
  font-size: 22px;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.3px;
}

@media (min-width: 900px) {
  .hero-title {
    font-size: 24px;
  }
}

.hero-subtitle {
  color: #94A3B8;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin: 0;
}

/* =========================================================
   2. CORPS : GRILLE DESKTOP & MOBILE
========================================================= */
.payment-content-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px 16px 36px;
  background: #F8FAFC;
}

@media (min-width: 900px) {
  .payment-content-grid {
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    gap: 24px;
    align-items: start;
    padding: 0;
  }
}

.payment-col-left,
.payment-col-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* CARTE DE BASE ÉPURÉE (AUCUN BOX-SHADOW) */
.content-card {
  background: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 18px 20px;
}

/* 1. ITINÉRAIRE & DATE */
.section-route-date {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.route-date-labels {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-light-gray);
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.text-right {
  text-align: right;
}

.route-date-values {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.route-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.city-name {
  font-size: 17px;
  font-weight: 800;
  color: var(--text-dark);
}

.route-arrow {
  font-size: 16px;
  font-weight: 900;
  color: var(--text-dark);
}

.date-text {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-dark);
}

/* 2. RÉCAPITULATIF FINANCIER */
.section-financial {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  font-size: 12px;
  font-weight: 800;
  color: #1E293B;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  margin: 0;
}

.financial-card {
  background: #F8FAFC;
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.financial-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.f-label {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.f-val {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-dark);
}

.text-fee {
  color: var(--coral-red);
}

.financial-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 2px 0;
}

.financial-row--net {
  padding-top: 2px;
}

.f-label-net {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-dark);
}

.f-val-net {
  font-size: 17px;
  font-weight: 800;
  color: var(--emerald-green);
}

/* 3. VÉHICULE */
.section-vehicle-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
}

.vehicle-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #FF6B4A 0%, #FF4D2D 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.vehicle-info-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.vehicle-name {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-dark);
}

.vehicle-meta {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-light-gray);
  letter-spacing: 0.4px;
}

/* 4. COMMISSION EN ATTENTE (FOND ROSE/SAUMON ÉPURÉ) */
.section-commission-card {
  background-color: #FFF5F2;
  border: 1px solid #FFE4DC;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
}

.commission-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 77, 45, 0.08);
  color: #FF4D2D;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.5px;
  padding: 4px 12px;
  border-radius: 20px;
}

.dot-red {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #FF4D2D;
}

.commission-amount-caption {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.8px;
  margin-top: 2px;
}

.commission-amount-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 6px;
}

.amount-digits {
  font-size: 34px;
  font-weight: 900;
  color: #FF4D2D;
  line-height: 1;
  letter-spacing: -0.5px;
}

.amount-currency {
  font-size: 18px;
  font-weight: 800;
  color: #FF4D2D;
}

/* 5. MODE DE PAIEMENT */
.section-payment-method {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.method-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.method-caption {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
}

.method-cards-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.method-option-card {
  background: #FFFFFF;
  border: 1.5px solid var(--border-color);
  border-radius: 16px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease;
  user-select: none;
}

.method-option-card:hover {
  border-color: #CBD5E1;
  background: #F8FAFC;
}

.method-option-card--active {
  border-color: #0EA5E9;
  background-color: #F0F9FF;
}

.method-left-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.provider-logo-container {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
  background-color: #FFFFFF;
  border: 1px solid var(--border-light);
}

.provider-logo-img {
  width: 36px;
  height: 36px;
  object-fit: contain;
  display: block;
}

.provider-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.provider-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.provider-name {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-dark);
}

.tag-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 8px;
}

.tag-badge--wave {
  background: #E0F2FE;
  color: #0284C7;
}

.tag-badge--om {
  background: #FFEDD5;
  color: #EA580C;
}

.provider-desc {
  font-size: 11px;
  color: var(--text-muted);
}

/* CASE À COCHER */
.method-checkbox {
  width: 22px;
  height: 22px;
  border-radius: 7px;
  border: 2px solid #CBD5E1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  flex-shrink: 0;
  background: #FFFFFF;
}

.method-checkbox--checked {
  border-color: #0EA5E9;
  background-color: #0EA5E9;
}

.method-checkbox--om.method-checkbox--checked-om {
  border-color: #FF7900;
  background-color: #FF7900;
}

/* BANNIÈRE ERREUR */
.error-banner {
  background: #FEF2F2;
  border: 1px solid #FCA5A5;
  color: #B91C1C;
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 6. ACTIONS FINALES (AUCUN BOX-SHADOW) */
.action-footer {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 4px;
}

.btn-submit-payment {
  width: 100%;
  height: 50px;
  border: none;
  border-radius: 16px;
  background: var(--brand-primary);
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.15s ease, transform 0.15s ease;
}

.btn-submit-payment:hover:not(:disabled) {
  background: var(--brand-hover);
  transform: translateY(-1px);
}

.btn-submit-payment:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit-payment:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-label-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-amount-chip {
  background: rgba(255, 255, 255, 0.22);
  padding: 3px 8px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
}

.btn-loading-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner-dot {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.security-caption {
  text-align: center;
  font-size: 11px;
  color: var(--text-light-gray);
  margin: 0;
}
</style>