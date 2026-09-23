<template>
  <div class="payment-page">

    <!-- =====================================================
         HEADER / HERO TERMINÉ
    ====================================================== -->
    <section class="completion-hero">
      <div class="completion-background"></div>

      <div class="completion-content">

        <!-- Icône succès -->
        <div
          class="success-icon"
          aria-hidden="true"
        >
          <svg viewBox="0 0 64 64">
            <path
              d="M18 33L27 42L47 21"
            />
          </svg>
        </div>

        <h1>
          Trajet Terminé !
        </h1>

        <p>
          MERCI POUR VOTRE SERVICE
        </p>
      </div>
    </section>


    <!-- =====================================================
         CONTENT
    ====================================================== -->
    <main class="payment-content">

      <!-- ===================================================
           RÉSUMÉ DU TRAJET
      ==================================================== -->
      <section class="trip-summary">

        <div class="summary-route">
          <span class="summary-label">
            ITINÉRAIRE
          </span>

          <div class="summary-route-line">
            <strong>
              {{ trip.departure }}
            </strong>

            <span
              class="route-arrow"
              aria-hidden="true"
            >
              ↑
            </span>

            <strong>
              {{ trip.destination }}
            </strong>
          </div>
        </div>

        <div class="summary-date">
          <span class="summary-label">
            DATE
          </span>

          <strong>
            {{ trip.date }}
          </strong>
        </div>

      </section>


      <!-- ===================================================
           SÉPARATEUR
      ==================================================== -->
      <div class="section-divider"></div>


      <!-- ===================================================
           RÉCAPITULATIF FINANCIER
      ==================================================== -->
      <section class="financial-section">

        <h2>
          RÉCAPITULATIF FINANCIER
        </h2>

        <div class="financial-card">

          <div class="financial-line">
            <span>
              Revenu total
              ({{ trip.passengers }} passagers)
            </span>

            <strong>
              {{ formatMoney(trip.totalRevenue) }}
            </strong>
          </div>

          <div class="financial-line">
            <span>
              Frais de plateforme
              ({{ trip.platformRate }}%)
            </span>

            <strong class="financial-fee">
              - {{ formatMoney(trip.platformFee) }}
            </strong>
          </div>

          <div class="financial-divider"></div>

          <div class="financial-line financial-line--net">
            <span>
              Votre gain net
            </span>

            <strong class="financial-net">
              {{ formatMoney(trip.netRevenue) }}
            </strong>
          </div>

        </div>

      </section>


      <!-- ===================================================
           COMMISSION
      ==================================================== -->
      <section class="commission-card">

        <div class="commission-status">
          <span
            class="status-dot"
            aria-hidden="true"
          ></span>

          COMMISSION EN ATTENTE
        </div>

        <span class="commission-label">
          MONTANT À RÉGLER
        </span>

        <div class="commission-amount">
          <strong>
            {{ formatNumber(trip.amountDue) }}
          </strong>

          <span>
            FCFA
          </span>
        </div>

        <p class="commission-helper">
          Réglez votre commission maintenant
          ou revenez plus tard depuis votre espace conducteur.
        </p>

      </section>


      <!-- ===================================================
           VÉHICULE
      ==================================================== -->
      <section class="vehicle-card">

        <div class="vehicle-icon">
          <div></div>
        </div>

        <div class="vehicle-info">
          <strong>
            {{ trip.vehicle.name }}
          </strong>

          <span>
            {{ trip.vehicle.plate }}
            <span class="vehicle-separator">•</span>
            {{ trip.vehicle.color }}
          </span>
        </div>

        <svg
          class="vehicle-side-icon"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            d="M12 3C9.8 6.1 6 9.6 6 14a6 6 0 0 0 12 0c0-4.4-3.8-7.9-6-11Z"
          />
        </svg>

      </section>


      <!-- ===================================================
           ACTIONS PAIEMENT
      ==================================================== -->
      <section
        class="payment-actions"
        :class="{
          'payment-actions--ready':
            buttonsReady
        }"
      >

        <!-- -----------------------------------------------
             PAYER MAINTENANT
        ------------------------------------------------ -->
        <button
          type="button"
          class="payment-button payment-button--primary"
          :disabled="isProcessing"
          @click="payNow"
        >
          <span
            v-if="!isProcessing"
            class="button-content"
          >
            <span>
              Payer maintenant
            </span>

            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M5 12h13" />
              <path d="M13 6l6 6-6 6" />
            </svg>
          </span>

          <span
            v-else
            class="button-loading"
          >
            <span class="spinner"></span>
            Traitement...
          </span>
        </button>


        <!-- -----------------------------------------------
             PAYER PLUS TARD
        ------------------------------------------------ -->
        <button
          type="button"
          class="payment-button payment-button--secondary"
          :disabled="isProcessing"
          @click="payLater"
        >
          <span class="button-content">
            <span>
              Payer plus tard
            </span>
          </span>
        </button>

      </section>

    </main>
  </div>
</template>


<script setup>
import {
  onBeforeUnmount,
  onMounted,
  reactive,
  ref
} from 'vue'

import { useRouter } from 'vue-router'


/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()


/* =========================================================
   ÉTAT
========================================================= */

const isProcessing =
  ref(false)

const buttonsReady =
  ref(false)

let animationTimer = null


/* =========================================================
   DONNÉES DU TRAJET
   Données de démonstration correspondant à la maquette.
   À remplacer ensuite avec les données Django / DRF.
========================================================= */

const trip = reactive({

  departure:
    'Keur Massar',

  destination:
    'Ouakam',

  date:
    '24 Jan. 2024',

  passengers:
    3,

  totalRevenue:
    6000,

  platformRate:
    10,

  platformFee:
    600,

  netRevenue:
    5400,

  amountDue:
    600,

  vehicle: {
    name:
      'Tesla Model 3',

    plate:
      'AB-123-CD',

    color:
      'BLANC'
  }
})


/* =========================================================
   FORMATAGE
========================================================= */

const formatNumber = (
  value
) => {
  return new Intl.NumberFormat(
    'fr-FR'
  ).format(value)
}


const formatMoney = (
  value
) => {
  return `${formatNumber(value)} FCFA`
}


/* =========================================================
   ANIMATION D'APPARITION
========================================================= */

onMounted(() => {

  animationTimer =
    window.setTimeout(() => {
      buttonsReady.value =
        true
    }, 120)
})


onBeforeUnmount(() => {
  if (animationTimer) {
    window.clearTimeout(
      animationTimer
    )
  }
})


/* =========================================================
   PAIEMENT IMMÉDIAT
========================================================= */

const payNow = async () => {

  if (isProcessing.value) {
    return
  }

  isProcessing.value =
    true

  try {

    /*
     * Ici viendra ton appel Django / DRF
     * vers ton service de paiement.
     *
     * Exemple :
     *
     * await paiementService.initier({
     *   trajetId: trip.id,
     *   montant: trip.amountDue
     * })
     *
     * Puis redirection vers le moyen
     * de paiement choisi.
     */

    await new Promise(
      (resolve) =>
        window.setTimeout(
          resolve,
          800
        )
    )

    /*
     * Pour le moment, on simule
     * une navigation vers une page
     * de confirmation.
     */
    router.push(
      '/conducteur/paiement/succes'
    )

  } catch (error) {

    console.error(
      'Erreur de paiement :',
      error
    )

  } finally {

    isProcessing.value =
      false
  }
}


/* =========================================================
   PAIEMENT PLUS TARD
========================================================= */

const payLater = () => {

  /*
   * Le statut du trajet reste terminé
   * mais la commission reste "en attente".
   *
   * Plus tard, cette action pourra appeler
   * Django pour enregistrer le statut.
   */

  router.push(
    '/conducteur/trajets-prevus'
  )
}
</script>


<style scoped>
/* =========================================================
   TOKENS
========================================================= */

.payment-page {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;

  --success: #13b878;
  --success-soft: #d8f8e9;

  --black: #111627;
  --dark-gray: #374151;

  --secondary: #727a88;
  --muted: #9ca3af;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;

  background:
    #f9fafb;

  color:
    var(--black);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  overflow-x: hidden;

  box-sizing: border-box;
}

.payment-page *,
.payment-page *::before,
.payment-page *::after {
  box-sizing: border-box;
}


/* =========================================================
   HERO
========================================================= */

.completion-hero {
  position: relative;

  width: 100%;

  min-height: 370px;

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: hidden;

  background:
    #374151;
}

.completion-background {
  position: absolute;

  inset: 0;

  /*
   * Remplace ce background par ton image
   * de carte lorsque celle-ci sera disponible.
   */
  background:
    linear-gradient(
      rgba(17, 22, 39, 0.58),
      rgba(17, 22, 39, 0.68)
    );
}

.completion-content {
  position: relative;

  z-index: 1;

  display: flex;

  flex-direction: column;

  align-items: center;

  text-align: center;

  padding:
    40px
    20px;
}

.success-icon {
  width: 118px;
  height: 118px;

  display: flex;

  align-items: center;
  justify-content: center;

  margin-bottom: 34px;

  border-radius: 50%;

  background:
    var(--success-soft);

  color:
    var(--success);

  animation:
    success-pop
    600ms
    cubic-bezier(
      0.2,
      0.9,
      0.3,
      1.2
    )
    both;
}

.success-icon svg {
  width: 68px;
  height: 68px;

  fill: none;

  stroke: currentColor;

  stroke-width: 3.2;

  stroke-linecap: round;

  stroke-linejoin: round;
}

.completion-content h1 {
  margin: 0;

  color:
    #ffffff;

  font-size: 44px;

  line-height: 1.15;

  font-weight: 800;

  letter-spacing:
    -1.3px;

  animation:
    fade-up
    500ms
    120ms
    ease
    both;
}

.completion-content p {
  margin:
    14px
    0
    0;

  color:
    rgba(
      255,
      255,
      255,
      0.72
    );

  font-size: 16px;

  line-height: 1.3;

  font-weight: 700;

  letter-spacing:
    1.3px;

  animation:
    fade-up
    500ms
    180ms
    ease
    both;
}


/* =========================================================
   CONTENT
========================================================= */

.payment-content {
  width: min(
    calc(100% - 48px),
    654px
  );

  margin: -38px auto 0;

  position: relative;

  z-index: 2;

  padding:
    30px
    28px
    50px;

  border-radius:
    34px
    34px
    0
    0;

  background:
    #ffffff;
}


/* =========================================================
   TRIP SUMMARY
========================================================= */

.trip-summary {
  display: grid;

  grid-template-columns:
    minmax(0, 1fr)
    auto;

  align-items: start;

  gap: 24px;
}

.summary-route {
  min-width: 0;
}

.summary-label {
  display: block;

  margin-bottom: 11px;

  color:
    #727a88;

  font-size: 14px;

  line-height: 1;

  font-weight: 800;

  letter-spacing:
    1.1px;

  text-transform:
    uppercase;
}

.summary-route-line {
  min-width: 0;

  display: flex;

  align-items: center;

  gap: 10px;

  flex-wrap: wrap;
}

.summary-route-line strong {
  color:
    var(--black);

  font-size: 25px;

  line-height: 1.2;

  font-weight: 800;

  letter-spacing:
    -0.5px;
}

.route-arrow {
  color:
    var(--black);

  font-size: 28px;

  line-height: 1;

  font-weight: 600;
}

.summary-date {
  text-align: right;
}

.summary-date strong {
  color:
    var(--black);

  font-size: 21px;

  line-height: 1.2;

  font-weight: 700;

  white-space: nowrap;
}


/* =========================================================
   DIVIDER
========================================================= */

.section-divider {
  width: 100%;
  height: 1px;

  margin:
    27px
    0
    30px;

  background:
    #e7e9ec;
}


/* =========================================================
   FINANCIAL
========================================================= */

.financial-section h2 {
  margin:
    0
    0
    20px;

  color:
    var(--black);

  font-size: 21px;

  line-height: 1.2;

  font-weight: 800;

  letter-spacing:
    0.8px;
}

.financial-card {
  padding:
    25px
    22px;

  border:
    1px solid
    #e0e4e8;

  border-radius: 27px;

  background:
    #fbfcfd;
}

.financial-line {
  display: grid;

  grid-template-columns:
    minmax(0, 1fr)
    auto;

  gap: 18px;

  align-items: center;
}

.financial-line + .financial-line {
  margin-top: 21px;
}

.financial-line span {
  color:
    #747d8b;

  font-size: 17px;

  line-height: 1.35;

  font-weight: 500;
}

.financial-line strong {
  color:
    var(--black);

  font-size: 18px;

  font-weight: 800;

  white-space: nowrap;
}

.financial-fee {
  color:
    var(--brand) !important;
}

.financial-divider {
  width: 100%;
  height: 1px;

  margin:
    22px
    0;

  background:
    #e2e5e8;
}

.financial-line--net span {
  color:
    var(--black);

  font-size: 20px;

  font-weight: 800;
}

.financial-net {
  color:
    #18a866 !important;

  font-size: 25px !important;
}


/* =========================================================
   COMMISSION
========================================================= */

.commission-card {
  margin-top: 38px;

  padding:
    27px
    24px
    28px;

  border:
    1px solid
    #ffd8cf;

  border-radius: 28px;

  background:
    #fff8f6;

  text-align: center;
}

.commission-status {
  width: fit-content;

  margin:
    0
    auto
    29px;

  min-height: 39px;

  display: inline-flex;

  align-items: center;

  gap: 9px;

  padding:
    0
    18px;

  border-radius:
    999px;

  background:
    #ffe2db;

  color:
    var(--brand);

  font-size: 14px;

  font-weight: 800;

  letter-spacing:
    0.5px;
}

.status-dot {
  width: 10px;
  height: 10px;

  border-radius: 50%;

  background:
    var(--brand);
}

.commission-label {
  display: block;

  color:
    #6f7784;

  font-size: 15px;

  line-height: 1.2;

  font-weight: 800;

  letter-spacing:
    1.1px;

  text-transform:
    uppercase;
}

.commission-amount {
  margin-top: 19px;

  display: flex;

  align-items: baseline;

  justify-content: center;

  gap: 13px;

  color:
    var(--brand);
}

.commission-amount strong {
  font-size: 67px;

  line-height: 0.95;

  font-weight: 800;

  letter-spacing:
    -2px;
}

.commission-amount span {
  font-size: 29px;

  line-height: 1;

  font-weight: 800;
}

.commission-helper {
  max-width: 390px;

  margin:
    25px
    auto
    0;

  color:
    #989fa9;

  font-size: 13px;

  line-height: 1.55;

  font-weight: 500;
}


/* =========================================================
   VEHICLE
========================================================= */

.vehicle-card {
  min-height: 99px;

  margin-top: 36px;

  display: flex;

  align-items: center;

  gap: 18px;

  padding:
    16px
    21px;

  border:
    1px solid
    #dee2e7;

  border-radius: 24px;

  background:
    #ffffff;
}

.vehicle-icon {
  width: 70px;
  height: 70px;

  flex: 0 0 70px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 18px;

  background:
    #ffffff;

  box-shadow:
    0 2px 7px
    rgba(
      17,
      22,
      39,
      0.045
    );
}

.vehicle-icon div {
  width: 31px;
  height: 31px;

  background:
    var(--brand);
}

.vehicle-info {
  min-width: 0;

  flex: 1;

  display: flex;

  flex-direction: column;

  gap: 6px;
}

.vehicle-info strong {
  color:
    var(--black);

  font-size: 20px;

  line-height: 1.2;

  font-weight: 800;
}

.vehicle-info span {
  color:
    #79818d;

  font-size: 15px;

  line-height: 1.2;

  font-weight: 600;

  letter-spacing:
    0.8px;
}

.vehicle-separator {
  padding:
    0
    4px;
}

.vehicle-side-icon {
  width: 23px;
  height: 23px;

  flex: 0 0 23px;

  fill:
    var(--black);

  stroke:
    var(--black);

  stroke-width:
    1.5;
}


/* =========================================================
   PAYMENT ACTIONS
========================================================= */

.payment-actions {
  display: flex;

  flex-direction: column;

  gap: 14px;

  margin-top: 30px;

  padding-top: 25px;

  border-top:
    1px solid
    #eceef0;
}


/* =========================================================
   BUTTON BASE
========================================================= */

.payment-button {
  position: relative;

  width: 100%;

  min-height: 72px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 21px;

  font-family:
    inherit;

  font-size: 20px;

  font-weight: 800;

  cursor: pointer;

  transition:
    background-color 180ms ease,
    border-color 180ms ease,
    color 180ms ease,
    transform 180ms ease,
    box-shadow 180ms ease,
    opacity 180ms ease;
}

.payment-button:disabled {
  cursor: not-allowed;

  opacity: 0.75;
}

.payment-button:hover:not(:disabled) {
  transform:
    translateY(-1px);
}

.payment-button:active:not(:disabled) {
  transform:
    translateY(0);
}

.payment-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 4px;
}


/* =========================================================
   PRIMARY
========================================================= */

.payment-button--primary {
  border: 0;

  background:
    var(--brand);

  color:
    #ffffff;

  box-shadow:
    0 6px 14px
    rgba(
      255,
      77,
      45,
      0.08
    );

  opacity: 0;

  transform:
    translateY(10px);
}

.payment-actions--ready
.payment-button--primary {
  animation:
    button-enter
    520ms
    80ms
    cubic-bezier(
      0.2,
      0.8,
      0.3,
      1
    )
    forwards;
}

.payment-button--primary:hover:not(:disabled) {
  background:
    var(--brand-hover);

  box-shadow:
    0 8px 16px
    rgba(
      255,
      77,
      45,
      0.10
    );
}


/* =========================================================
   SECONDARY
========================================================= */

.payment-button--secondary {
  border:
    1.5px solid
    var(--brand);

  background:
    #ffffff;

  color:
    var(--brand);

  opacity: 0;

  transform:
    translateY(10px);
}

.payment-actions--ready
.payment-button--secondary {
  animation:
    button-enter
    520ms
    190ms
    cubic-bezier(
      0.2,
      0.8,
      0.3,
      1
    )
    forwards;
}

.payment-button--secondary:hover:not(:disabled) {
  background:
    #fff8f6;

  border-color:
    var(--brand-hover);

  color:
    var(--brand-hover);
}


/* =========================================================
   BUTTON CONTENT
========================================================= */

.button-content {
  display: inline-flex;

  align-items: center;

  justify-content: center;

  gap: 13px;
}

.button-content svg {
  width: 25px;
  height: 25px;

  fill: none;

  stroke: currentColor;

  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;

  transition:
    transform 180ms ease;
}

.payment-button:hover
.button-content svg {
  transform:
    translateX(3px);
}


/* =========================================================
   LOADING
========================================================= */

.button-loading {
  display: inline-flex;

  align-items: center;

  gap: 10px;
}

.spinner {
  width: 18px;
  height: 18px;

  border:
    2px solid
    rgba(
      255,
      255,
      255,
      0.35
    );

  border-top-color:
    #ffffff;

  border-radius: 50%;

  animation:
    spin
    0.7s
    linear
    infinite;
}


/* =========================================================
   ANIMATIONS
========================================================= */

@keyframes success-pop {
  0% {
    opacity: 0;

    transform:
      scale(0.75);
  }

  70% {
    transform:
      scale(1.04);
  }

  100% {
    opacity: 1;

    transform:
      scale(1);
  }
}

@keyframes fade-up {
  from {
    opacity: 0;

    transform:
      translateY(10px);
  }

  to {
    opacity: 1;

    transform:
      translateY(0);
  }
}

@keyframes button-enter {
  from {
    opacity: 0;

    transform:
      translateY(10px);
  }

  to {
    opacity: 1;

    transform:
      translateY(0);
  }
}

@keyframes spin {
  to {
    transform:
      rotate(360deg);
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .completion-hero {
    min-height: 315px;
  }

  .completion-content {
    padding:
      35px
      18px;
  }

  .success-icon {
    width: 92px;
    height: 92px;

    margin-bottom: 26px;
  }

  .success-icon svg {
    width: 53px;
    height: 53px;
  }

  .completion-content h1 {
    font-size: 32px;

    letter-spacing:
      -0.9px;
  }

  .completion-content p {
    font-size: 12px;

    letter-spacing:
      0.9px;
  }


  /* CONTENT */

  .payment-content {
    width: 100%;

    margin-top: -28px;

    padding:
      24px
      16px
      36px;

    border-radius:
      27px
      27px
      0
      0;
  }


  /* SUMMARY */

  .trip-summary {
    grid-template-columns:
      minmax(0, 1fr)
      auto;

    gap: 12px;
  }

  .summary-label {
    margin-bottom: 8px;

    font-size: 10px;
  }

  .summary-route-line {
    gap: 6px;
  }

  .summary-route-line strong {
    font-size: 18px;
  }

  .route-arrow {
    font-size: 21px;
  }

  .summary-date strong {
    font-size: 16px;
  }


  /* FINANCIAL */

  .section-divider {
    margin:
      24px
      0
      27px;
  }

  .financial-section h2 {
    font-size: 16px;

    margin-bottom: 15px;
  }

  .financial-card {
    padding:
      19px
      15px;

    border-radius: 21px;
  }

  .financial-line {
    gap: 10px;
  }

  .financial-line + .financial-line {
    margin-top: 17px;
  }

  .financial-line span {
    font-size: 13px;
  }

  .financial-line strong {
    font-size: 14px;
  }

  .financial-line--net span {
    font-size: 15px;
  }

  .financial-net {
    font-size: 19px !important;
  }


  /* COMMISSION */

  .commission-card {
    margin-top: 26px;

    padding:
      22px
      16px
      24px;

    border-radius: 23px;
  }

  .commission-status {
    margin-bottom: 22px;

    min-height: 34px;

    padding:
      0
      14px;

    font-size: 11px;
  }

  .status-dot {
    width: 8px;
    height: 8px;
  }

  .commission-label {
    font-size: 11px;
  }

  .commission-amount {
    margin-top: 14px;

    gap: 8px;
  }

  .commission-amount strong {
    font-size: 49px;

    letter-spacing:
      -1.5px;
  }

  .commission-amount span {
    font-size: 22px;
  }

  .commission-helper {
    margin-top: 19px;

    font-size: 11px;
  }


  /* VEHICLE */

  .vehicle-card {
    min-height: 80px;

    margin-top: 25px;

    gap: 12px;

    padding:
      11px
      13px;

    border-radius: 19px;
  }

  .vehicle-icon {
    width: 55px;
    height: 55px;

    flex-basis: 55px;

    border-radius: 14px;
  }

  .vehicle-icon div {
    width: 25px;
    height: 25px;
  }

  .vehicle-info {
    gap: 4px;
  }

  .vehicle-info strong {
    font-size: 16px;
  }

  .vehicle-info span {
    font-size: 11px;
  }

  .vehicle-side-icon {
    width: 19px;
    height: 19px;
  }


  /* ACTIONS */

  .payment-actions {
    gap: 11px;

    margin-top: 24px;

    padding-top: 21px;
  }

  .payment-button {
    min-height: 61px;

    border-radius: 18px;

    font-size: 16px;
  }

  .button-content {
    gap: 9px;
  }

  .button-content svg {
    width: 20px;
    height: 20px;
  }
}


/* =========================================================
   VERY SMALL MOBILE
========================================================= */

@media (max-width: 360px) {

  .payment-content {
    padding-left: 12px;
    padding-right: 12px;
  }

  .summary-route-line strong {
    font-size: 16px;
  }

  .summary-date strong {
    font-size: 14px;
  }

  .financial-line span {
    font-size: 12px;
  }

  .financial-line strong {
    font-size: 13px;
  }

  .commission-amount strong {
    font-size: 44px;
  }

  .commission-amount span {
    font-size: 20px;
  }

  .payment-button {
    font-size: 15px;
  }
}


/* =========================================================
   ACCESSIBILITÉ : RÉDUCTION DES ANIMATIONS
========================================================= */

@media (prefers-reduced-motion: reduce) {

  .success-icon,
  .completion-content h1,
  .completion-content p,
  .payment-button--primary,
  .payment-button--secondary {
    animation: none !important;

    opacity: 1 !important;

    transform: none !important;
  }

  .payment-button,
  .payment-button svg {
    transition: none !important;
  }
}
</style>