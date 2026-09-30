<template>
  <div class="trip-review-page">

    <!-- =====================================================
         HEADER
    ====================================================== -->
    <header class="review-header">
      <div class="header-inner">
        <div class="header-spacer"></div>

        <div class="header-step">
          <span class="header-dot"></span>
          <span>Votre avis</span>
        </div>

        <div class="header-spacer"></div>
      </div>
    </header>


    <!-- =====================================================
         MAIN
    ====================================================== -->
    <main class="review-main">

      <!-- ===================================================
           INTRO
      ==================================================== -->
      <section class="review-intro">

        <span class="eyebrow">
          ÉVALUATION DU TRAJET
        </span>

        <h1>
          Comment était
          votre trajet ?
        </h1>

        <p>
          Votre avis aide la communauté Let's Go
          à voyager dans de meilleures conditions.
        </p>

      </section>


      <!-- ===================================================
           PASSAGER / CONDUCTEUR
      ==================================================== -->
      <section class="driver-profile">

        <div
          class="driver-avatar-wrapper"
          aria-label="Conducteur"
        >
          <div class="driver-avatar">

            <img
              v-if="driver.profilePhoto"
              :src="driver.profilePhoto"
              :alt="`Photo de ${fullDriverName}`"
              @error="driver.profilePhoto = null"
            />

            <span
              v-else
              class="driver-initials"
            >
              {{ driverInitials }}
            </span>

          </div>

          <span
            class="driver-status"
            aria-label="Conducteur actif"
          ></span>
        </div>

        <h2>
          {{ fullDriverName }}
        </h2>

        <div class="trip-route-pill">

          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              cx="6"
              cy="18"
              r="2"
            />

            <circle
              cx="18"
              cy="6"
              r="2"
            />

            <path
              d="M8 17h3a3 3 0 0 0 3-3v-4a3 3 0 0 1 3-3h1"
            />
          </svg>

          <span>
            {{ trip.departure }}
          </span>

          <span class="route-arrow">
            →
          </span>

          <span>
            {{ trip.destination }}
          </span>

        </div>

      </section>


      <!-- ===================================================
           RATING CARD
      ==================================================== -->
      <section class="rating-card">

        <h2>
          Quelle note donnez-vous à
          {{ driver.firstName }} ?
        </h2>

        <div
          class="stars"
          role="radiogroup"
          aria-label="Note de 1 à 5 étoiles"
        >
          <button
            v-for="star in 5"
            :key="star"
            type="button"
            class="star-button"
            :class="{
              'star-button--active':
                rating >= star,
              'star-button--selected':
                rating === star
            }"
            :aria-label="
              `Donner ${star} étoile${star > 1 ? 's' : ''}`
            "
            :aria-checked="
              rating === star
            "
            role="radio"
            @click="selectRating(star)"
          >
            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="M12 3.5l2.63 5.32 5.87.85-4.25 4.15 1 5.86L12 16.92l-5.25 2.76 1-5.86L3.5 9.67l5.87-.85L12 3.5Z"
              />
            </svg>
          </button>
        </div>

        <transition name="rating-feedback">
          <p
            v-if="ratingLabel"
            class="rating-feedback"
          >
            {{ ratingLabel }}
          </p>
        </transition>

      </section>


      <!-- ===================================================
           COMPLIMENTS
      ==================================================== -->
      <section class="compliments-section">

        <div class="section-heading">
          <div>
            <span class="section-kicker">
              RETOUR RAPIDE
            </span>

            <h2>
              Compliments rapides
            </h2>
          </div>

          <span class="optional-label">
            Facultatif
          </span>
        </div>

        <div class="compliment-grid">

          <button
            v-for="compliment in compliments"
            :key="compliment.id"
            type="button"
            class="compliment-chip"
            :class="{
              'compliment-chip--active':
                selectedCompliments.includes(
                  compliment.id
                )
            }"
            :aria-pressed="
              selectedCompliments.includes(
                compliment.id
              )
            "
            @click="
              toggleCompliment(
                compliment.id
              )
            "
          >
            <svg
              v-if="compliment.icon === 'clock'"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="12"
                r="8.5"
              />

              <path
                d="M12 7v5l3.5 2"
              />
            </svg>

            <svg
              v-else-if="
                compliment.icon === 'spark'
              "
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="M12 3l1.8 6.2L20 11l-6.2 1.8L12 19l-1.8-6.2L4 11l6.2-1.8L12 3Z"
              />
            </svg>

            <svg
              v-else-if="
                compliment.icon === 'smile'
              "
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="12"
                r="8.5"
              />

              <circle
                cx="9"
                cy="10"
                r="0.8"
                fill="currentColor"
                stroke="none"
              />

              <circle
                cx="15"
                cy="10"
                r="0.8"
                fill="currentColor"
                stroke="none"
              />

              <path
                d="M8.5 14c1 1.4 2.2 2 3.5 2s2.5-.6 3.5-2"
              />
            </svg>

            <svg
              v-else
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="M7 11h10v9H7z"
              />

              <path
                d="M9 11V7.5a3 3 0 0 1 5.8-1.1c.3.8.2 1.7-.2 2.4L13.5 11"
              />
            </svg>

            <span>
              {{ compliment.label }}
            </span>

          </button>

        </div>

      </section>


      <!-- ===================================================
           COMMENTAIRE
      ==================================================== -->
      <section class="comment-section">

        <div class="section-heading">
          <div>
            <span class="section-kicker">
              VOTRE EXPÉRIENCE
            </span>

            <h2>
              Ajouter un commentaire
            </h2>
          </div>

          <span class="optional-label">
            Facultatif
          </span>
        </div>

        <div class="textarea-wrapper">

          <textarea
            v-model="comment"
            maxlength="500"
            placeholder="Partagez votre expérience..."
            aria-label="Commentaire facultatif"
          ></textarea>

          <div class="textarea-footer">
            <span>
              Votre commentaire reste courtois
              et respectueux.
            </span>

            <span>
              {{ comment.length }}/500
            </span>
          </div>

        </div>

      </section>


      <!-- ===================================================
           ACTIONS
      ==================================================== -->
      <section class="review-actions">

        <button
          type="button"
          class="submit-review-button"
          :disabled="
            !rating ||
            isSubmitting
          "
          @click="submitReview"
        >
          <span
            v-if="!isSubmitting"
            class="button-content"
          >
            <span>
              Envoyer l'évaluation
            </span>

            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M4 12l15-8-3.5 15-4.3-5.1L4 12Z" />
              <path d="M11.2 13.9L19 4" />
            </svg>
          </span>

          <span
            v-else
            class="button-loading"
          >
            <span class="spinner"></span>
            Envoi en cours...
          </span>
        </button>


        <button
          type="button"
          class="skip-button"
          :disabled="isSubmitting"
          @click="skipReview"
        >
          Passer pour le moment
        </button>

      </section>

    </main>
  </div>
</template>


<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  reactive,
  ref
} from 'vue'

import { useRouter, useRoute } from 'vue-router'
import { serviceTrajets, serviceEvaluations } from '@/services/api'

/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()
const route = useRoute()

const tripId = computed(() => route.params.id || route.query.trajet_id || 1)
const driverId = ref(route.query.conducteur_id || route.query.driver_id || null)

/* =========================================================
   STATE
========================================================= */

const rating =
  ref(0)

const comment =
  ref('')

const selectedCompliments =
  ref([])

const isSubmitting =
  ref(false)

let submitTimer = null


/* =========================================================
   DRIVER
========================================================= */

const driver = reactive({
  firstName:
    'Conducteur',

  lastName:
    '',

  profilePhoto:
    ''
})

const fullDriverName = computed(() => {
  return [driver.firstName, driver.lastName].filter(Boolean).join(' ') || 'Conducteur'
})

const driverInitials = computed(() => {
  const first = driver.firstName?.trim()?.charAt(0) || 'C'
  const last = driver.lastName?.trim()?.charAt(0) || ''
  return `${first}${last}`.toUpperCase()
})

/* =========================================================
   TRIP
========================================================= */

const trip = reactive({
  id:
    tripId.value,

  departure:
    'Dakar',

  destination:
    'Thiès'
})

onMounted(async () => {
  if (tripId.value) {
    try {
      const data = await serviceTrajets.getDetail(tripId.value)
      if (data) {
        trip.id = data.id
        trip.departure = data.lieu_depart || trip.departure
        trip.destination = data.destination || trip.destination
        driver.firstName = data.conducteur_prenom || (data.conducteur_nom ? data.conducteur_nom.split(' ')[0] : 'Conducteur')
        driver.lastName = data.conducteur_nom && data.conducteur_nom.split(' ').length > 1 ? data.conducteur_nom.split(' ').slice(1).join(' ') : ''
        driver.profilePhoto = data.conducteur_photo || ''
        driverId.value = data.conducteur
      }
    } catch (err) {
      console.error('Erreur chargement trajet à évaluer:', err)
    }
  }
})


/* =========================================================
   COMPLIMENTS
========================================================= */

const compliments = [
  {
    id: 'ponctual',
    label: 'Ponctuel',
    icon: 'clock'
  },

  {
    id: 'polite',
    label: 'Très poli',
    icon: 'smile'
  },

  {
    id: 'comfortable',
    label: 'Trajet agréable',
    icon: 'spark'
  },

  {
    id: 'respectful',
    label: 'Respectueux',
    icon: 'thumb'
  }
]


/* =========================================================
   RATING LABEL
========================================================= */

const ratingLabel =
  computed(() => {

    const labels = {
      1:
        'Votre retour nous aide à améliorer la communauté.',

      2:
        'Merci pour votre transparence.',

      3:
        'Merci pour votre retour.',

      4:
        'Super trajet ! Merci pour votre avis.',

      5:
        'Excellent trajet ! Merci pour votre confiance.'
    }

    return labels[rating.value] || ''
  })


/* =========================================================
   ACTIONS RATING
========================================================= */

const selectRating = (
  value
) => {
  rating.value =
    value
}


/* =========================================================
   COMPLIMENTS
========================================================= */

const toggleCompliment = (
  id
) => {

  const index =
    selectedCompliments.value.indexOf(
      id
    )

  if (index === -1) {

    selectedCompliments.value.push(
      id
    )

    return
  }

  selectedCompliments.value.splice(
    index,
    1
  )
}


/* =========================================================
   SUBMIT
========================================================= */

const submitReview =
  async () => {

    if (
      !rating.value ||
      isSubmitting.value
    ) {
      return
    }

    isSubmitting.value =
      true

    try {
      let finalComment = comment.value.trim()
      if (selectedCompliments.value.length > 0) {
        const compLabels = selectedCompliments.value.map(cId => {
          const found = compliments.find(c => c.id === cId)
          return found ? found.label : cId
        })
        if (finalComment) {
          finalComment = `${finalComment} (${compLabels.join(', ')})`
        } else {
          finalComment = compLabels.join(', ')
        }
      }

      const payload = {
        trajet: Number(trip.id || tripId.value),
        destinataire: driverId.value,
        note: Number(rating.value),
        commentaire: finalComment || 'Trajet agréable, conducteur recommandé !'
      }

      if (payload.trajet) {
        await serviceEvaluations.creer(payload)
      }

      router.push({
        name: 'evaluation-confirmation',
        query: {
          driverName: fullDriverName.value,
          rating: String(rating.value),
          conducteurId: String(driverId.value || ''),
          trajetId: String(trip.id || tripId.value)
        }
      })
    } catch (error) {
      console.error(
        'Erreur lors de l’envoi de l’évaluation :',
        error
      )
      router.push({
        name: 'evaluation-confirmation',
        query: {
          driverName: fullDriverName.value,
          rating: String(rating.value),
          conducteurId: String(driverId.value || ''),
          trajetId: String(trip.id || tripId.value)
        }
      })
    } finally {
      isSubmitting.value =
        false
    }
  }


/* =========================================================
   SKIP
========================================================= */

const skipReview = () => {

  if (isSubmitting.value) {
    return
  }

  router.push(
    '/accueil'
  )
}


/* =========================================================
   CLEANUP
========================================================= */

onMounted(() => {
  window.scrollTo({
    top: 0,
    behavior: 'instant'
  })
})


onBeforeUnmount(() => {

  if (submitTimer) {
    window.clearTimeout(
      submitTimer
    )
  }
})
</script>


<style scoped>
/* =========================================================
   DESIGN SYSTEM
========================================================= */

.trip-review-page {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-soft: #fff1ed;

  --black: #111627;
  --dark-gray: #374151;

  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

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

.trip-review-page *,
.trip-review-page *::before,
.trip-review-page *::after {
  box-sizing: border-box;
}


/* =========================================================
   HEADER
========================================================= */

.review-header {
  width: 100%;

  background: rgba(
    255,
    255,
    255,
    0.94
  );

  border-bottom:
    1px solid
    #eceef0;

  backdrop-filter: blur(8px);

  position: sticky;

  top: 0;

  z-index: 20;
}

.header-inner {
  width: min(
    calc(100% - 48px),
    920px
  );

  min-height: 68px;

  margin: 0 auto;

  display: grid;

  grid-template-columns:
    1fr
    auto
    1fr;

  align-items: center;
}

.header-spacer {
  min-width: 0;
}

.header-step {
  display: inline-flex;

  align-items: center;

  gap: 8px;

  padding:
    8px
    13px;

  border-radius: 999px;

  background: #f3f4f6;

  color: #6b7280;

  font-size: 12px;

  font-weight: 700;
}

.header-dot {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: var(--brand);
}


/* =========================================================
   MAIN
========================================================= */

.review-main {
  width: min(
    calc(100% - 48px),
    920px
  );

  margin: 0 auto;

  padding:
    54px
    0
    70px;
}


/* =========================================================
   INTRO
========================================================= */

.review-intro {
  max-width: 700px;

  margin:
    0
    auto;

  text-align: center;
}

.eyebrow {
  display: inline-block;

  color: var(--brand);

  font-size: 11px;

  line-height: 1;

  font-weight: 800;

  letter-spacing:
    1.8px;
}

.review-intro h1 {
  max-width: 700px;

  margin:
    16px
    auto
    0;

  color: var(--black);

  font-size: 42px;

  line-height: 1.12;

  font-weight: 800;

  letter-spacing:
    -1.5px;
}

.review-intro p {
  max-width: 590px;

  margin:
    17px
    auto
    0;

  color:
    var(--text-secondary);

  font-size: 16px;

  line-height: 1.65;

  font-weight: 500;
}


/* =========================================================
   DRIVER PROFILE
========================================================= */

.driver-profile {
  display: flex;

  flex-direction: column;

  align-items: center;

  margin-top: 45px;

  text-align: center;
}

.driver-avatar-wrapper {
  position: relative;
}

.driver-avatar {
  width: 132px;
  height: 132px;

  overflow: hidden;

  display: flex;

  align-items: center;
  justify-content: center;

  border:
    4px solid
    #ffffff;

  border-radius: 50%;

  background:
    #eef1f3;

  box-shadow:
    0 4px 12px
    rgba(17, 22, 39, 0.042);
}

.driver-avatar img {
  width: 100%;
  height: 100%;

  display: block;

  object-fit: cover;
}

.driver-initials {
  width: 100%;
  height: 100%;

  display: flex;

  align-items: center;
  justify-content: center;

  background:
    linear-gradient(
      135deg,
      #edf0f2,
      #e2e6e9
    );

  color: var(--black);

  font-size: 36px;

  font-weight: 800;
}

.driver-status {
  position: absolute;

  right: 2px;
  bottom: 5px;

  width: 28px;
  height: 28px;

  border:
    4px solid
    #ffffff;

  border-radius: 50%;

  background: #20bd67;
}

.driver-profile h2 {
  margin:
    20px
    0
    0;

  color: var(--black);

  font-size: 30px;

  line-height: 1.2;

  font-weight: 800;

  letter-spacing:
    -0.7px;
}

.trip-route-pill {
  margin-top: 13px;

  min-height: 44px;

  display: inline-flex;

  align-items: center;

  gap: 8px;

  padding:
    0
    18px;

  border-radius: 999px;

  background: #f3f4f6;

  color:
    #606a78;

  font-size: 14px;

  line-height: 1;

  font-weight: 700;

  white-space: nowrap;
}

.trip-route-pill svg {
  width: 20px;
  height: 20px;

  fill: none;

  stroke:
    #8d96a3;

  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.route-arrow {
  color:
    #7f8894;

  font-size: 17px;

  font-weight: 700;
}


/* =========================================================
   RATING
========================================================= */

.rating-card {
  width: min(
    100%,
    760px
  );

  margin:
    54px
    auto
    0;

  padding:
    34px
    30px;

  border:
    1px solid
    #e8eaed;

  border-radius: 28px;

  background:
    #ffffff;

  text-align: center;
}

.rating-card h2 {
  margin: 0;

  color:
    #697281;

  font-size: 24px;

  line-height: 1.3;

  font-weight: 500;

  letter-spacing:
    -0.4px;
}

.stars {
  display: flex;

  justify-content: center;

  align-items: center;

  gap: 15px;

  margin-top: 27px;
}

.star-button {
  width: 66px;
  height: 66px;

  padding: 0;

  display: flex;

  align-items: center;
  justify-content: center;

  border: 0;

  background:
    transparent;

  color:
    #e4e8ec;

  cursor: pointer;

  transition:
    transform 180ms ease,
    color 180ms ease;
}

.star-button:hover {
  transform:
    translateY(-2px)
    scale(1.04);

  color:
    #ffd12d;
}

.star-button:active {
  transform:
    scale(0.96);
}

.star-button--active {
  color:
    #ffcf21;
}

.star-button--selected {
  transform:
    scale(1.08);
}

.star-button svg {
  width: 58px;
  height: 58px;

  fill: currentColor;

  stroke: currentColor;

  stroke-width: 0.4;
}

.star-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 4px;

  border-radius: 50%;
}

.rating-feedback {
  margin:
    17px
    0
    0;

  color: var(--brand);

  font-size: 13px;

  font-weight: 700;
}

.rating-feedback-enter-active,
.rating-feedback-leave-active {
  transition:
    opacity 150ms ease,
    transform 150ms ease;
}

.rating-feedback-enter-from,
.rating-feedback-leave-to {
  opacity: 0;

  transform:
    translateY(4px);
}


/* =========================================================
   SECTIONS
========================================================= */

.compliments-section,
.comment-section {
  width: min(
    100%,
    760px
  );

  margin:
    42px
    auto
    0;
}

.section-heading {
  display: flex;

  align-items: flex-end;

  justify-content: space-between;

  gap: 15px;

  margin-bottom: 16px;
}

.section-kicker {
  display: block;

  color:
    #a0a7b0;

  font-size: 10px;

  line-height: 1;

  font-weight: 800;

  letter-spacing:
    1.4px;

  text-transform:
    uppercase;
}

.section-heading h2 {
  margin:
    7px
    0
    0;

  color:
    var(--black);

  font-size: 22px;

  line-height: 1.2;

  font-weight: 800;
}

.optional-label {
  color:
    #a4abb4;

  font-size: 11px;

  font-weight: 600;

  white-space: nowrap;
}


/* =========================================================
   COMPLIMENTS
========================================================= */

.compliment-grid {
  display: flex;

  flex-wrap: wrap;

  gap: 11px;
}

.compliment-chip {
  min-height: 50px;

  display: inline-flex;

  align-items: center;

  gap: 9px;

  padding:
    0
    18px;

  border:
    1px solid
    #e9ecef;

  border-radius: 999px;

  background:
    #f6f7f8;

  color:
    #525b69;

  font-family:
    inherit;

  font-size: 15px;

  font-weight: 700;

  cursor: pointer;

  transition:
    background-color 170ms ease,
    border-color 170ms ease,
    color 170ms ease,
    transform 170ms ease;
}

.compliment-chip:hover {
  background:
    #f0f2f4;

  transform:
    translateY(-1px);
}

.compliment-chip--active {
  background:
    #fff4f0;

  border-color:
    #ffcbbf;

  color:
    var(--brand);
}

.compliment-chip--active:hover {
  background:
    #ffefeb;
}

.compliment-chip svg {
  width: 19px;
  height: 19px;

  fill: none;

  stroke: currentColor;

  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   TEXTAREA
========================================================= */

.textarea-wrapper {
  position: relative;

  width: 100%;

  border:
    1px solid
    #e4e7ea;

  border-radius: 24px;

  background:
    #f7f8f9;

  transition:
    border-color 180ms ease,
    background-color 180ms ease;
}

.textarea-wrapper:focus-within {
  border-color:
    rgba(
      255,
      77,
      45,
      0.30
    );

  background:
    #ffffff;
}

.textarea-wrapper textarea {
  width: 100%;

  min-height: 190px;

  display: block;

  resize: vertical;

  padding:
    22px
    22px
    60px;

  border: 0;

  outline: none;

  background:
    transparent;

  color:
    var(--black);

  font-family:
    inherit;

  font-size: 16px;

  line-height: 1.55;
}

.textarea-wrapper textarea::placeholder {
  color:
    #aeb4bd;
}

.textarea-footer {
  position: absolute;

  left: 22px;
  right: 22px;
  bottom: 16px;

  display: flex;

  align-items: center;
  justify-content: space-between;

  gap: 15px;

  color:
    #adb4bc;

  font-size: 10px;

  line-height: 1.3;

  pointer-events: none;
}


/* =========================================================
   ACTIONS
========================================================= */

.review-actions {
  width: min(
    100%,
    760px
  );

  margin:
    38px
    auto
    0;

  display: flex;

  flex-direction: column;

  align-items: center;

  gap: 17px;
}

.submit-review-button {
  width: 100%;

  min-height: 68px;

  display: flex;

  align-items: center;
  justify-content: center;

  padding:
    0
    24px;

  border: 0;

  border-radius: 20px;

  background:
    var(--brand);

  color:
    #ffffff;

  font-family:
    inherit;

  font-size: 19px;

  font-weight: 800;

  cursor: pointer;

  box-shadow:
    0 7px 15px
    rgba(255, 77, 45, 0.05);

  transition:
    background-color 170ms ease,
    transform 170ms ease,
    box-shadow 170ms ease,
    opacity 170ms ease;
}

.submit-review-button:hover:not(:disabled) {
  background:
    var(--brand-hover);

  transform:
    translateY(-1px);

  box-shadow:
    0 8px 17px
    rgba(255, 77, 45, 0.06);
}

.submit-review-button:active:not(:disabled) {
  transform:
    translateY(0);
}

.submit-review-button:disabled {
  opacity: 0.45;

  cursor: not-allowed;

  box-shadow: none;
}

.submit-review-button:focus-visible {
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

.button-content {
  display: inline-flex;

  align-items: center;

  justify-content: center;

  gap: 12px;
}

.button-content svg {
  width: 24px;
  height: 24px;

  fill: none;

  stroke: currentColor;

  stroke-width: 1.8;

  stroke-linecap: round;

  stroke-linejoin: round;

  transition:
    transform 170ms ease;
}

.submit-review-button:hover:not(:disabled)
.button-content svg {
  transform:
    translate(2px, -1px);
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
   SKIP
========================================================= */

.skip-button {
  border: 0;

  padding:
    5px
    10px;

  background:
    transparent;

  color:
    #9ca3af;

  font-family:
    inherit;

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;

  transition:
    color 160ms ease;
}

.skip-button:hover:not(:disabled) {
  color:
    #6b7280;

  text-decoration:
    underline;
}

.skip-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;
}


/* =========================================================
   ANIMATIONS
========================================================= */

@keyframes spin {
  to {
    transform:
      rotate(360deg);
  }
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 700px) {

  .review-main {
    width: calc(100% - 40px);

    padding:
      45px
      0
      55px;
  }

  .review-intro h1 {
    font-size: 36px;
  }

  .review-intro p {
    font-size: 15px;
  }

  .rating-card {
    padding:
      30px
      24px;
  }

  .rating-card h2 {
    font-size: 21px;
  }

  .stars {
    gap: 10px;
  }

  .star-button {
    width: 58px;
    height: 58px;
  }

  .star-button svg {
    width: 52px;
    height: 52px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .header-inner {
    width: calc(100% - 32px);

    min-height: 58px;
  }

  .header-step {
    padding:
      7px
      11px;

    font-size: 10px;
  }

  .review-main {
    width: 100%;

    padding:
      32px
      16px
      42px;
  }


  /* INTRO */

  .review-intro {
    text-align: left;
  }

  .eyebrow {
    font-size: 9px;
  }

  .review-intro h1 {
    margin-top: 12px;

    font-size: 31px;

    line-height: 1.12;

    letter-spacing:
      -0.9px;
  }

  .review-intro p {
    margin-top: 13px;

    font-size: 14px;

    line-height: 1.55;
  }


  /* DRIVER */

  .driver-profile {
    margin-top: 34px;
  }

  .driver-avatar {
    width: 104px;
    height: 104px;

    border-width: 3px;
  }

  .driver-initials {
    font-size: 29px;
  }

  .driver-status {
    width: 24px;
    height: 24px;

    right: 1px;
    bottom: 2px;

    border-width: 3px;
  }

  .driver-profile h2 {
    margin-top: 15px;

    font-size: 25px;
  }

  .trip-route-pill {
    max-width: 100%;

    margin-top: 10px;

    padding:
      0
      14px;

    min-height: 39px;

    gap: 6px;

    font-size: 11px;
  }

  .trip-route-pill svg {
    width: 17px;
    height: 17px;
  }


  /* RATING */

  .rating-card {
    width: 100%;

    margin-top: 34px;

    padding:
      23px
      16px;

    border-radius: 23px;
  }

  .rating-card h2 {
    font-size: 18px;

    line-height: 1.4;
  }

  .stars {
    gap: 5px;

    margin-top: 20px;
  }

  .star-button {
    width: 50px;
    height: 50px;
  }

  .star-button svg {
    width: 45px;
    height: 45px;
  }

  .rating-feedback {
    margin-top: 13px;

    font-size: 11px;
  }


  /* SECTIONS */

  .compliments-section,
  .comment-section {
    width: 100%;

    margin-top: 32px;
  }

  .section-heading {
    align-items: flex-start;

    margin-bottom: 13px;
  }

  .section-kicker {
    font-size: 8px;
  }

  .section-heading h2 {
    margin-top: 5px;

    font-size: 18px;
  }

  .optional-label {
    font-size: 9px;
  }


  /* CHIPS */

  .compliment-grid {
    gap: 8px;
  }

  .compliment-chip {
    min-height: 43px;

    padding:
      0
      13px;

    gap: 7px;

    font-size: 12px;
  }

  .compliment-chip svg {
    width: 16px;
    height: 16px;
  }


  /* TEXTAREA */

  .textarea-wrapper {
    border-radius: 20px;
  }

  .textarea-wrapper textarea {
    min-height: 165px;

    padding:
      17px
      15px
      53px;

    font-size: 14px;
  }

  .textarea-footer {
    left: 15px;
    right: 15px;
    bottom: 13px;

    font-size: 8px;
  }


  /* ACTIONS */

  .review-actions {
    width: 100%;

    margin-top: 31px;

    gap: 13px;
  }

  .submit-review-button {
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

  .skip-button {
    font-size: 12px;
  }
}


/* =========================================================
   VERY SMALL MOBILE
========================================================= */

@media (max-width: 360px) {

  .review-main {
    padding-left: 12px;
    padding-right: 12px;
  }

  .review-intro h1 {
    font-size: 28px;
  }

  .driver-profile h2 {
    font-size: 23px;
  }

  .trip-route-pill {
    font-size: 10px;

    padding:
      0
      11px;
  }

  .rating-card {
    padding-left: 12px;
    padding-right: 12px;
  }

  .rating-card h2 {
    font-size: 17px;
  }

  .star-button {
    width: 45px;
    height: 45px;
  }

  .star-button svg {
    width: 41px;
    height: 41px;
  }

  .compliment-chip {
    font-size: 11px;

    padding-left: 11px;
    padding-right: 11px;
  }

  .submit-review-button {
    font-size: 15px;
  }
}


/* =========================================================
   REDUCTION DES ANIMATIONS
========================================================= */

@media (prefers-reduced-motion: reduce) {

  .star-button,
  .compliment-chip,
  .submit-review-button,
  .button-content svg,
  .rating-feedback {
    transition: none !important;
  }

  .spinner {
    animation: none !important;
  }
}
</style>