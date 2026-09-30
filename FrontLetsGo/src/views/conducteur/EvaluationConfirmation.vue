<template>
  <div class="evaluation-confirmation">
    <main class="confirmation-container">

      <!-- ==================================================
           ILLUSTRATION
      =================================================== -->
      <section class="illustration-section">
        <div class="illustration-glow">
          <div class="illustration-circle">
            <div class="illustration-card">
              <img
                v-if="illustrationImage"
                :src="illustrationImage"
                alt="Conducteur souriant"
                class="illustration-image"
                @error="illustrationImage = null"
              />

              <div
                v-else
                class="illustration-fallback"
              >
                <svg
                  viewBox="0 0 120 120"
                  aria-hidden="true"
                >
                  <circle
                    cx="60"
                    cy="60"
                    r="28"
                  />

                  <path
                    d="M35 102c4-19 14-28 25-28s21 9 25 28"
                  />

                  <circle
                    cx="50"
                    cy="56"
                    r="3"
                    fill="currentColor"
                  />

                  <circle
                    cx="70"
                    cy="56"
                    r="3"
                    fill="currentColor"
                  />

                  <path
                    d="M49 67c7 6 15 6 22 0"
                  />
                </svg>
              </div>
            </div>
          </div>

          <!-- Check -->
          <div
            class="success-badge"
            aria-hidden="true"
          >
            <svg
              viewBox="0 0 24 24"
            >
              <path d="M5 12.5l4.2 4.2L19 7" />
            </svg>
          </div>
        </div>
      </section>


      <!-- ==================================================
           MESSAGE
      =================================================== -->
      <section class="confirmation-message">

        <span class="confirmation-kicker">
          ÉVALUATION ENVOYÉE
        </span>

        <h1>
          Merci pour votre
          <span>évaluation !</span>
        </h1>

        <p>
          Votre avis sur <strong>{{ driverName }}</strong> aide la communauté
          <strong>LET’S GO</strong>
          à rester fiable.
        </p>

      </section>


      <!-- ==================================================
           SUMMARY CARD
      =================================================== -->
      <section class="feedback-card">

        <div
          class="feedback-stars"
          :aria-label="`${userRating} étoiles`"
        >
          <svg
            v-for="star in 5"
            :key="star"
            viewBox="0 0 24 24"
            aria-hidden="true"
            :style="{ fill: star <= userRating ? '#FF4D2D' : '#E2E8F0' }"
          >
            <path
              d="M12 3.5l2.63 5.32 5.87.85-4.25 4.15 1 5.86L12 16.92l-5.25 2.76 1-5.86L3.5 9.67l5.87-.85L12 3.5Z"
            />
          </svg>
        </div>

        <div class="feedback-message">
          <p>
            "{{ feedbackMessage }}"
          </p>
        </div>

      </section>


      <!-- ==================================================
           ACTION
      =================================================== -->
      <section class="confirmation-action">

        <button
          v-if="driverId"
          type="button"
          class="wall-button"
          @click="goToDriverWall"
        >
          <span>
            Voir le profil & mur du conducteur
          </span>

          <svg
            viewBox="0 0 24 24"
            width="20"
            height="20"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>

        <button
          type="button"
          class="home-button"
          @click="goHome"
        >
          <span>
            Retour à l'accueil
          </span>

          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M5 12h13" />
            <path d="M13 6l6 6-6 6" />
          </svg>
        </button>

      </section>

    </main>
  </div>
</template>


<script setup>
import {
  computed,
  onMounted,
  ref
} from 'vue'

import { useRouter, useRoute } from 'vue-router'


/* =========================================================
   ROUTER & QUERY
========================================================= */

const router = useRouter()
const route = useRoute()

const driverName = computed(() => route.query.driverName || 'le conducteur')
const userRating = computed(() => Number(route.query.rating) || 5)
const driverId = computed(() => route.query.conducteurId || '')
const trajetId = computed(() => route.query.trajetId || '')


/* =========================================================
   DONNÉES
========================================================= */

const illustrationImage = ref(
  '/images/image_6.jpg'
)

const feedbackMessage = ref(
  userRating.value >= 4
    ? 'Super trajet, conducteur très prudent et ponctuel !'
    : 'Merci pour votre retour d\'expérience sur ce trajet.'
)


/* =========================================================
   NAVIGATION
========================================================= */

const goHome = () => {
  router.push('/accueil')
}

const goToDriverWall = () => {
  if (driverId.value) {
    router.push({
      path: `/conducteur/profil/${driverId.value}`,
      query: trajetId.value ? { trajet_id: trajetId.value } : {}
    })
  } else {
    router.push('/accueil')
  }
}


/* =========================================================
   SCROLL TOP
========================================================= */

onMounted(() => {
  window.scrollTo({
    top: 0,
    behavior: 'instant'
  })
})
</script>


<style scoped>
/* =========================================================
   DESIGN SYSTEM
========================================================= */

.evaluation-confirmation {
  --brand: #ff4d2d;
  --brand-hover: #f04427;

  --black: #111627;
  --dark-gray: #374151;

  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  --soft-gray: #e5e7eb;
  --light-gray: #f3f4f6;

  --success: #12b878;
  --success-soft: #d7f8e8;

  --white: #ffffff;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;

  background: #ffffff;

  color: var(--black);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  overflow-x: hidden;

  box-sizing: border-box;
}

.evaluation-confirmation *,
.evaluation-confirmation *::before,
.evaluation-confirmation *::after {
  box-sizing: border-box;
}


/* =========================================================
   CONTAINER
========================================================= */

.confirmation-container {
  width: min(
    calc(100% - 48px),
    760px
  );

  min-height: 100vh;

  margin: 0 auto;

  padding:
    52px
    0
    58px;

  display: flex;

  flex-direction: column;

  align-items: center;
}


/* =========================================================
   ILLUSTRATION
========================================================= */

.illustration-section {
  width: 100%;

  display: flex;

  justify-content: center;

  animation:
    illustration-enter
    500ms
    cubic-bezier(
      0.2,
      0.85,
      0.3,
      1.15
    )
    both;
}

.illustration-glow {
  position: relative;

  width: 360px;
  height: 360px;

  display: flex;

  align-items: center;
  justify-content: center;
}

.illustration-circle {
  width: 310px;
  height: 310px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(
        255,
        227,
        222,
        0.96
      )
      0%,
      rgba(
        255,
        239,
        236,
        0.68
      )
      54%,
      rgba(
        255,
        248,
        246,
        0
      )
      100%
    );
}

.illustration-card {
  position: relative;

  width: 250px;
  height: 250px;

  overflow: hidden;

  border-radius: 48px;

  background:
    #f1f3f5;

  box-shadow:
    0 5px 12px
    rgba(17, 22, 39, 0.042);
}

.illustration-image {
  width: 100%;
  height: 100%;

  display: block;

  object-fit: cover;
}

.illustration-fallback {
  width: 100%;
  height: 100%;

  display: flex;

  align-items: center;
  justify-content: center;

  color:
    #707887;

  background:
    linear-gradient(
      145deg,
      #eef1f3,
      #dfe4e8
    );
}

.illustration-fallback svg {
  width: 110px;
  height: 110px;

  fill: none;

  stroke: currentColor;

  stroke-width: 2.1;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   SUCCESS BADGE
========================================================= */

.success-badge {
  position: absolute;

  right: 28px;
  bottom: 18px;

  width: 88px;
  height: 88px;

  display: flex;

  align-items: center;
  justify-content: center;

  border:
    5px solid
    #ffffff;

  border-radius: 28px;

  background:
    var(--success);

  color:
    #ffffff;

  box-shadow:
    0 4px 10px
    rgba(17, 22, 39, 0.049);

  animation:
    badge-enter
    500ms
    180ms
    cubic-bezier(
      0.2,
      0.85,
      0.3,
      1.15
    )
    both;
}

.success-badge svg {
  width: 51px;
  height: 51px;

  fill: none;

  stroke: currentColor;

  stroke-width: 3;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   MESSAGE
========================================================= */

.confirmation-message {
  width: 100%;

  max-width: 700px;

  margin-top: 36px;

  text-align: center;

  animation:
    fade-up
    500ms
    130ms
    ease
    both;
}

.confirmation-kicker {
  display: inline-block;

  color:
    var(--brand);

  font-size: 10px;

  line-height: 1;

  font-weight: 800;

  letter-spacing: 1.7px;
}

.confirmation-message h1 {
  max-width: 650px;

  margin:
    15px
    auto
    0;

  color:
    var(--black);

  font-size: 50px;

  line-height: 1.12;

  font-weight: 800;

  letter-spacing:
    -1.8px;
}

.confirmation-message h1 span {
  display: inline;
}

.confirmation-message p {
  max-width: 570px;

  margin:
    23px
    auto
    0;

  color:
    var(--text-secondary);

  font-size: 21px;

  line-height: 1.55;

  font-weight: 500;
}

.confirmation-message p strong {
  color:
    var(--brand);

  font-weight: 800;
}


/* =========================================================
   FEEDBACK CARD
========================================================= */

.feedback-card {
  width: 100%;

  max-width: 650px;

  margin-top: 72px;

  padding:
    47px
    34px
    45px;

  border:
    1px solid
    #eceef1;

  border-radius: 34px;

  background:
    #fbfcfd;

  text-align: center;

  animation:
    fade-up
    500ms
    230ms
    ease
    both;
}


/* =========================================================
   STARS
========================================================= */

.feedback-stars {
  display: flex;

  align-items: center;
  justify-content: center;

  gap: 12px;
}

.feedback-stars svg {
  width: 46px;
  height: 46px;

  fill:
    #ffcb05;

  stroke:
    #ffcb05;

  stroke-width: 0.5;
}


/* =========================================================
   MESSAGE CARD
========================================================= */

.feedback-message {
  width: 100%;

  margin-top: 34px;

  padding:
    28px
    24px;

  border:
    1px solid
    #f0f1f3;

  border-radius: 28px;

  background:
    #ffffff;

  box-shadow:
    0 2px 5px
    rgba(17, 22, 39, 0.017);
}

.feedback-message p {
  margin: 0;

  color:
    #596271;

  font-size: 21px;

  line-height: 1.55;

  font-weight: 500;

  font-style: italic;
}


/* =========================================================
   ACTION
========================================================= */

.confirmation-action {
  width: 100%;

  max-width: 650px;

  margin-top: 50px;
  display: flex;
  flex-direction: column;
  gap: 14px;

  animation:
    fade-up
    500ms
    320ms
    ease
    both;
}

.wall-button {
  width: 100%;
  min-height: 62px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  border: 1.5px solid var(--brand);
  border-radius: 20px;
  background: #FFF5F2;
  color: var(--brand);
  font-family: inherit;
  font-size: 17px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: none;
  transition: all 170ms ease;
}

.wall-button:hover {
  background: var(--brand);
  color: #ffffff;
  transform: translateY(-1px);
}

.home-button {
  width: 100%;

  min-height: 62px;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 14px;

  border: 1px solid #E2E8F0;

  border-radius: 20px;

  background:
    var(--black);

  color:
    #ffffff;

  font-family:
    inherit;

  font-size: 17px;

  font-weight: 800;

  cursor: pointer;

  box-shadow: none;

  transition:
    background-color 170ms ease,
    transform 170ms ease;
}

.home-button:hover {
  background:
    #1e2538;

  transform:
    translateY(-1px);
}

.home-button:active {
  transform:
    translateY(0);
}

.home-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.20
    );

  outline-offset: 4px;
}

.home-button svg {
  width: 25px;
  height: 25px;

  fill: none;

  stroke:
    currentColor;

  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;

  transition:
    transform 170ms ease;
}

.home-button:hover svg {
  transform:
    translateX(3px);
}


/* =========================================================
   ANIMATIONS
========================================================= */

@keyframes illustration-enter {
  from {
    opacity: 0;

    transform:
      translateY(14px)
      scale(0.96);
  }

  to {
    opacity: 1;

    transform:
      translateY(0)
      scale(1);
  }
}

@keyframes badge-enter {
  from {
    opacity: 0;

    transform:
      scale(0.75);
  }

  to {
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


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 700px) {

  .confirmation-container {
    width:
      calc(100% - 40px);

    padding:
      42px
      0
      48px;
  }

  .illustration-glow {
    width: 320px;
    height: 320px;
  }

  .illustration-circle {
    width: 275px;
    height: 275px;
  }

  .illustration-card {
    width: 225px;
    height: 225px;

    border-radius: 42px;
  }

  .success-badge {
    width: 80px;
    height: 80px;

    right: 23px;
    bottom: 14px;

    border-radius: 25px;
  }

  .success-badge svg {
    width: 47px;
    height: 47px;
  }

  .confirmation-message h1 {
    font-size: 41px;
  }

  .confirmation-message p {
    font-size: 18px;
  }

  .feedback-card {
    margin-top: 57px;
  }

  .confirmation-action {
    margin-top: 60px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .confirmation-container {
    width: 100%;

    padding:
      30px
      16px
      34px;
  }


  /* -----------------------------------------------
     ILLUSTRATION
  ------------------------------------------------ */

  .illustration-glow {
    width: 285px;
    height: 285px;
  }

  .illustration-circle {
    width: 250px;
    height: 250px;
  }

  .illustration-card {
    width: 195px;
    height: 195px;

    border-radius: 38px;
  }

  .success-badge {
    width: 72px;
    height: 72px;

    right: 18px;
    bottom: 11px;

    border-width: 4px;

    border-radius: 23px;
  }

  .success-badge svg {
    width: 43px;
    height: 43px;
  }


  /* -----------------------------------------------
     MESSAGE
  ------------------------------------------------ */

  .confirmation-message {
    margin-top: 28px;
  }

  .confirmation-kicker {
    font-size: 8px;

    letter-spacing: 1.4px;
  }

  .confirmation-message h1 {
    max-width: 350px;

    margin-top: 11px;

    font-size: 34px;

    line-height: 1.12;

    letter-spacing:
      -1px;
  }

  .confirmation-message p {
    max-width: 340px;

    margin-top: 16px;

    font-size: 17px;

    line-height: 1.5;
  }


  /* -----------------------------------------------
     FEEDBACK CARD
  ------------------------------------------------ */

  .feedback-card {
    width: 100%;

    margin-top: 43px;

    padding:
      32px
      15px
      34px;

    border-radius: 25px;
  }

  .feedback-stars {
    gap: 5px;
  }

  .feedback-stars svg {
    width: 39px;
    height: 39px;
  }

  .feedback-message {
    margin-top: 25px;

    padding:
      23px
      14px;

    border-radius: 24px;
  }

  .feedback-message p {
    font-size: 17px;

    line-height: 1.55;
  }


  /* -----------------------------------------------
     ACTION
  ------------------------------------------------ */

  .confirmation-action {
    width: 100%;

    margin-top: 45px;
  }

  .home-button {
    min-height: 63px;

    border-radius: 18px;

    font-size: 17px;

    gap: 10px;
  }

  .home-button svg {
    width: 21px;
    height: 21px;
  }
}


/* =========================================================
   VERY SMALL MOBILE
========================================================= */

@media (max-width: 360px) {

  .confirmation-container {
    padding-left: 12px;
    padding-right: 12px;
  }

  .illustration-glow {
    width: 260px;
    height: 260px;
  }

  .illustration-circle {
    width: 225px;
    height: 225px;
  }

  .illustration-card {
    width: 178px;
    height: 178px;

    border-radius: 34px;
  }

  .success-badge {
    width: 64px;
    height: 64px;

    right: 15px;
    bottom: 8px;
  }

  .success-badge svg {
    width: 38px;
    height: 38px;
  }

  .confirmation-message h1 {
    font-size: 30px;
  }

  .confirmation-message p {
    font-size: 15px;
  }

  .feedback-card {
    padding:
      27px
      12px
      29px;
  }

  .feedback-stars svg {
    width: 35px;
    height: 35px;
  }

  .feedback-message p {
    font-size: 15px;
  }

  .home-button {
    font-size: 15px;
  }
}


/* =========================================================
   ACCESSIBILITÉ
========================================================= */

@media (prefers-reduced-motion: reduce) {

  .illustration-section,
  .success-badge,
  .confirmation-message,
  .feedback-card,
  .confirmation-action {
    animation: none !important;
  }

  .home-button,
  .home-button svg {
    transition: none !important;
  }
}
</style>