<template>
  <div class="publish-trip-page">
    <div class="publish-page-container">
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
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M15 18L9 12L15 6" />
          </svg>
        </button>

        <div class="header-titles">
          <h1>{{ isEditMode ? 'Modifier le trajet' : 'Proposer un trajet' }}</h1>
          <p class="header-subtitle">
            {{ isEditMode ? 'Ajustez les détails et conditions de votre trajet' : 'Partagez votre itinéraire et réduisez vos frais de déplacement' }}
          </p>
        </div>
      </header>

      <!-- =====================================================
           CONTENT
      ====================================================== -->
      <main class="page-content">
        <form
          class="trip-form-layout"
          @submit.prevent="handleSubmit"
        >
          <!-- ===================================================
               COLONNE GAUCHE : FORMULAIRE PRINCIPAL
          ==================================================== -->
          <div class="form-colonne-principale">
            <!-- 1. ITINÉRAIRE -->
            <section class="form-card">
              <div class="card-header">
                <div class="card-icon-pill">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
                  </svg>
                </div>
                <div class="card-titles">
                  <h2>Itinéraire du trajet</h2>
                  <p>Définissez précisément vos points de départ et d'arrivée</p>
                </div>
              </div>

              <div class="route-inputs-container">
                <!-- DÉPART -->
                <div class="route-field-row">
                  <div class="route-point-marker marker--start" aria-hidden="true">
                    <span></span>
                  </div>
                  <div class="route-field-content">
                    <label for="departure">Lieu de départ</label>
                    <input
                      id="departure"
                      v-model.trim="form.departure"
                      type="text"
                      autocomplete="street-address"
                      placeholder="Ex. Parcelles Assainies, Dakar"
                      required
                    />
                  </div>
                </div>

                <!-- Ligne de liaison -->
                <div class="route-connector-line" aria-hidden="true"></div>

                <!-- DESTINATION -->
                <div class="route-field-row">
                  <div class="route-point-marker marker--end" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M12 21s6.5-6.2 6.5-11A6.5 6.5 0 1 0 5.5 10c0 4.8 6.5 11 6.5 11Z" />
                      <circle cx="12" cy="10" r="2.2" />
                    </svg>
                  </div>
                  <div class="route-field-content">
                    <label for="destination">Destination</label>
                    <input
                      id="destination"
                      v-model.trim="form.destination"
                      type="text"
                      autocomplete="street-address"
                      placeholder="Ex. Plateau, Dakar"
                      required
                    />
                  </div>
                </div>
              </div>
            </section>

            <!-- 2. DATE, HORAIRES & TARIFICATION -->
            <section class="form-card">
              <div class="card-header">
                <div class="card-icon-pill">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                    <line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                  </svg>
                </div>
                <div class="card-titles">
                  <h2>Planning & Modalités</h2>
                  <p>Déterminez la date, l'horaire, les places et votre tarif</p>
                </div>
              </div>

              <div class="details-grid">
                <!-- ================= DATE ================= -->
                <div
                  ref="datePickerRef"
                  class="detail-input-card picker-field"
                  :class="{ 'picker-field--open': showCalendar }"
                >
                  <label>Date de départ</label>
                  <button
                    type="button"
                    class="picker-trigger-btn"
                    :aria-expanded="showCalendar"
                    @click.stop="openCalendar"
                  >
                    <div class="trigger-val-row">
                      <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" />
                        <line x1="16" y1="2" x2="16" y2="6" />
                        <line x1="8" y1="2" x2="8" y2="6" />
                        <line x1="3" y1="10" x2="21" y2="10" />
                      </svg>
                      <span class="val-text" :class="{ 'val-text--placeholder': !form.date }">
                        {{ formattedDate }}
                      </span>
                    </div>
                    <svg class="chevron-icon" :class="{ 'chevron--open': showCalendar }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>

                  <!-- Popover Calendrier -->
                  <Transition name="picker-menu">
                    <div v-if="showCalendar" class="calendar-menu-popover" @click.stop>
                      <div class="calendar-header">
                        <button
                          type="button"
                          class="calendar-nav-btn"
                          :disabled="isCurrentMonth"
                          @click="goToPreviousMonth"
                        >
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6" /></svg>
                        </button>
                        <div class="calendar-month-display">
                          <strong>{{ currentMonthLabel }}</strong>
                          <span>{{ currentYearLabel }}</span>
                        </div>
                        <button
                          type="button"
                          class="calendar-nav-btn"
                          @click="goToNextMonth"
                        >
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6" /></svg>
                        </button>
                      </div>

                      <div class="calendar-weekdays-row">
                        <span v-for="d in weekDays" :key="d">{{ d }}</span>
                      </div>

                      <div class="calendar-days-grid">
                        <button
                          v-for="day in calendarDays"
                          :key="day.key"
                          type="button"
                          class="calendar-day-btn"
                          :class="{
                            'day--outside': !day.currentMonth,
                            'day--today': day.isToday,
                            'day--selected': day.selected,
                            'day--disabled': day.disabled
                          }"
                          :disabled="day.disabled"
                          @click="selectDate(day.date)"
                        >
                          {{ day.day }}
                        </button>
                      </div>

                      <div class="calendar-footer-row">
                        <button type="button" class="btn-today-shortcut" @click="selectToday">
                          Aujourd'hui
                        </button>
                      </div>
                    </div>
                  </Transition>
                </div>

                <!-- ================= HEURE ================= -->
                <div
                  ref="timePickerRef"
                  class="detail-input-card picker-field"
                  :class="{ 'picker-field--open': showTimeOptions }"
                >
                  <label for="trip-time">Heure de départ</label>
                  <div class="time-input-group">
                    <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12 6 12 12 16 14" />
                    </svg>
                    <input
                      id="trip-time"
                      :value="form.time"
                      type="text"
                      inputmode="numeric"
                      maxlength="5"
                      placeholder="08:30"
                      class="time-input-field"
                      @input="handleTimeInput"
                      @focus="openTimeOptions"
                      @keydown.esc="closeTimeOptions"
                    />
                    <button
                      type="button"
                      class="time-chevron-btn"
                      @click.stop="toggleTimeOptions"
                    >
                      <svg class="chevron-icon" :class="{ 'chevron--open': showTimeOptions }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M6 9l6 6 6-6" />
                      </svg>
                    </button>
                  </div>

                  <!-- Popover Horaires -->
                  <Transition name="picker-menu">
                    <div v-if="showTimeOptions" class="time-menu-popover" @click.stop>
                      <span class="time-menu-title">Horaires fréquents</span>
                      <div class="suggested-times-grid">
                        <button
                          v-for="t in suggestedTimes"
                          :key="t"
                          type="button"
                          class="time-chip-btn"
                          :class="{ 'time-chip--active': form.time === t }"
                          @click="selectTime(t)"
                        >
                          {{ t }}
                        </button>
                      </div>
                    </div>
                  </Transition>
                </div>

                <!-- ================= PLACES ================= -->
                <div
                  ref="seatDropdownRef"
                  class="detail-input-card picker-field"
                  :class="{ 'picker-field--open': showSeatOptions }"
                >
                  <label>Nombre de places</label>
                  <button
                    type="button"
                    class="picker-trigger-btn"
                    :aria-expanded="showSeatOptions"
                    @click.stop="toggleSeatOptions"
                  >
                    <div class="trigger-val-row">
                      <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                        <circle cx="9" cy="7" r="4" />
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                      </svg>
                      <span class="val-text">
                        {{ form.seats }} place{{ form.seats > 1 ? 's' : '' }}
                      </span>
                    </div>
                    <svg class="chevron-icon" :class="{ 'chevron--open': showSeatOptions }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>

                  <!-- Popover Places -->
                  <Transition name="picker-menu">
                    <div v-if="showSeatOptions" class="seat-menu-popover" @click.stop>
                      <button
                        v-for="seat in seatOptions"
                        :key="seat"
                        type="button"
                        class="seat-item-btn"
                        :class="{ 'seat-item--selected': form.seats === seat }"
                        @click="selectSeat(seat)"
                      >
                        <span class="seat-num">{{ seat }}</span>
                        <span class="seat-label">{{ seat > 1 ? 'places disponibles' : 'place disponible' }}</span>
                        <svg v-if="form.seats === seat" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      </button>
                    </div>
                  </Transition>
                </div>

                <!-- ================= PRIX ================= -->
                <div class="detail-input-card price-field-card">
                  <label for="price">Prix par passager</label>
                  <div class="price-input-row">
                    <svg class="field-icon field-icon--brand" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="12" y1="1" x2="12" y2="23" />
                      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                    </svg>
                    <input
                      id="price"
                      v-model.number="form.price"
                      type="number"
                      min="0"
                      step="100"
                      placeholder="5000"
                      class="price-number-input"
                      required
                    />
                    <span class="price-currency-suffix">FCFA</span>
                  </div>
                </div>
              </div>
            </section>

            <!-- 3. DESCRIPTION & PRÉFÉRENCES -->
            <section class="form-card">
              <div class="card-header">
                <div class="card-icon-pill">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" y1="13" x2="8" y2="13" />
                    <line x1="16" y1="17" x2="8" y2="17" />
                    <polyline points="10 9 9 9 8 9" />
                  </svg>
                </div>
                <div class="card-titles">
                  <h2>Préférences & Précisions</h2>
                  <p>Règles à bord et instructions pour vos passagers</p>
                </div>
              </div>

              <!-- Préférences chips -->
              <div class="preferences-block">
                <label class="field-sublabel">Règles et conditions à bord</label>
                <div class="preferences-chips-row">
                  <!-- Non Fumeur -->
                  <button
                    type="button"
                    class="pref-chip-btn"
                    :class="{ 'pref-chip--active': form.preferences.includes('no-smoking') }"
                    @click="togglePreference('no-smoking')"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
                    </svg>
                    <span>Non fumeur</span>
                  </button>

                  <!-- Animaux OK -->
                  <button
                    type="button"
                    class="pref-chip-btn"
                    :class="{ 'pref-chip--active': form.preferences.includes('pets') }"
                    @click="togglePreference('pets')"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 18c-1.6 0-2.3-1.2-3.8-1.2S5.8 18 5.8 16.2c0-1.4.8-2.3 1.9-3.2C8.4 12.2 9 11 9 9.7a3 3 0 0 1 6 0c0 1.3.6 2.5 1.3 3.3 1.1.9 1.9 1.8 1.9 3.2 0 1.8-1 2.8-2.4 2.8S13.6 18 12 18Z" />
                      <circle cx="7" cy="7" r="1.5" />
                      <circle cx="17" cy="7" r="1.5" />
                    </svg>
                    <span>Animaux OK</span>
                  </button>

                  <!-- Gros bagages -->
                  <button
                    type="button"
                    class="pref-chip-btn"
                    :class="{ 'pref-chip--active': form.preferences.includes('luggage') }"
                    @click="togglePreference('luggage')"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="6" width="18" height="15" rx="2" />
                      <path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />
                    </svg>
                    <span>Gros bagages</span>
                  </button>
                </div>
              </div>

              <!-- Message libre -->
              <div class="description-block">
                <div class="desc-label-row">
                  <label for="description" class="field-sublabel">Informations complémentaires (optionnel)</label>
                  <span class="char-count-text">{{ form.description.length }}/500</span>
                </div>
                <textarea
                  id="description"
                  v-model.trim="form.description"
                  maxlength="500"
                  rows="3"
                  placeholder="Ex. Rendez-vous devant la pharmacie, arrêt de 10 min prévu à mi-chemin..."
                  class="description-textarea"
                ></textarea>
              </div>
            </section>

            <!-- BOUTON SUBMIT (VISIBLE SUR MOBILE SEULEMENT) -->
            <div class="mobile-submit-box">
              <p v-if="publishError" class="publish-error-alert">{{ publishError }}</p>
              <button
                type="submit"
                class="btn-primary-publish"
                :disabled="!canPublish || isSubmitting"
              >
                <span v-if="!isSubmitting" class="btn-publish-content">
                  <span>{{ isEditMode ? 'Enregistrer les modifications' : 'Publier ce trajet' }}</span>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="9 18 15 12 9 6" />
                  </svg>
                </span>
                <span v-else class="btn-spinner-state">
                  <span class="btn-spinner"></span> Enregistrement...
                </span>
              </button>
              <p class="terms-note">
                En publiant, vous acceptez nos conditions d'utilisation et la charte de sécurité Let's Go.
              </p>
            </div>
          </div>

          <!-- ===================================================
               COLONNE DROITE : APERÇU EN DIRECT & PUBLICATION (DESKTOP)
          ==================================================== -->
          <aside class="sidebar-recap-desktop">
            <div class="recap-card-sticky">
              <div class="recap-header">
                <h3>Récapitulatif de l'annonce</h3>
              </div>

              <!-- Résumé visuel de l'itinéraire -->
              <div class="recap-route-box">
                <div class="recap-route-row">
                  <span class="recap-dot start-dot"></span>
                  <div class="recap-route-info">
                    <small>DÉPART</small>
                    <strong>{{ form.departure || 'Lieu de départ' }}</strong>
                  </div>
                </div>
                <div class="recap-route-line"></div>
                <div class="recap-route-row">
                  <span class="recap-dot end-dot"></span>
                  <div class="recap-route-info">
                    <small>ARRIVÉE</small>
                    <strong>{{ form.destination || 'Destination' }}</strong>
                  </div>
                </div>
              </div>

              <!-- Métadonnées du trajet -->
              <div class="recap-meta-grid">
                <div class="meta-item">
                  <span class="meta-label">Date</span>
                  <strong class="meta-value">{{ formattedDate }}</strong>
                </div>
                <div class="meta-item">
                  <span class="meta-label">Heure</span>
                  <strong class="meta-value">{{ form.time || '--:--' }}</strong>
                </div>
                <div class="meta-item">
                  <span class="meta-label">Places</span>
                  <strong class="meta-value">{{ form.seats }} dispo</strong>
                </div>
              </div>

              <!-- Estimation des revenus -->
              <div class="recap-revenue-box">
                <div class="revenue-line">
                  <span>Prix unitaire</span>
                  <strong>{{ Number(form.price || 0).toLocaleString('fr-FR') }} FCFA</strong>
                </div>
                <div class="revenue-line total">
                  <div>
                    <span>Recette max. estimée</span>
                    <small>{{ form.seats }} places × {{ Number(form.price || 0).toLocaleString('fr-FR') }}</small>
                  </div>
                  <strong class="gain-highlight">
                    {{ Number((form.price || 0) * (form.seats || 1)).toLocaleString('fr-FR') }} FCFA
                  </strong>
                </div>
              </div>

              <!-- Erreur éventuelle -->
              <p v-if="publishError" class="publish-error-alert">{{ publishError }}</p>

              <!-- Bouton Principal de Publication (Desktop) -->
              <button
                type="submit"
                class="btn-primary-publish btn-desktop"
                :disabled="!canPublish || isSubmitting"
              >
                <span v-if="!isSubmitting" class="btn-publish-content">
                  <span>{{ isEditMode ? 'Enregistrer les modifications' : 'Publier ce trajet' }}</span>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="9 18 15 12 9 6" />
                  </svg>
                </span>
                <span v-else class="btn-spinner-state">
                  <span class="btn-spinner"></span> Enregistrement...
                </span>
              </button>

              <p class="recap-disclaimer">
                En publiant, vous confirmez détenir un permis de conduire valide et un véhicule assuré en conformité avec la réglementation.
              </p>
            </div>
          </aside>
        </form>
      </main>
    </div>
  </div>

  <PublishedOverlay
    v-model="showPublishedOverlay"
    @view-trip="goToTrip"
    @close="closePublishedOverlay"
  />
</template>

<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  reactive,
  ref
} from 'vue'
import PublishedOverlay from '@/components/common/PublishedOverlay.vue'
import { useRoute, useRouter } from 'vue-router'
import { serviceTrajets } from '@/services/api'

/* =========================================================
   ROUTER / EVENTS
========================================================= */
const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => !!route.query.edit)
const editTripId = computed(() => route.query.edit)

const emit = defineEmits([
  'back',
  'publish'
])

const goBack = () => {
  if (isEditMode.value) {
    router.replace({
      name: 'vue-trajet-prevu',
      params: { id: editTripId.value }
    })
  } else if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/conducteur/tableau-de-bord')
  }
}

/* =========================================================
   HELPERS DATE
========================================================= */
const normalizeDate = (date) => {
  const result = new Date(date)
  result.setHours(12, 0, 0, 0)
  return result
}

const today = normalizeDate(new Date())

const formatDateValue = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

/* =========================================================
   FORM REACTIVE DATA
========================================================= */
const form = reactive({
  departure: 'Dakar, Sacré-coeur',
  destination: 'Dakar, Plateau',
  date: formatDateValue(today),
  time: '08:30',
  seats: 3,
  price: 5000,
  description: '',
  preferences: ['no-smoking', 'pets']
})

const isSubmitting = ref(false)

/* =========================================================
   OPTIONS & VALIDATION
========================================================= */
const seatOptions = [1, 2, 3, 4, 5, 6, 7]

const suggestedTimes = [
  '06:00', '06:30', '07:00', '07:30', '08:00', '08:30',
  '09:00', '09:30', '10:00', '11:00', '12:00', '13:00',
  '14:00', '15:00', '16:00', '17:00', '17:30', '18:00',
  '18:30', '19:00'
]

const validateTime = (value) => {
  const match = String(value).match(/^(\d{2}):(\d{2})$/)
  if (!match) return false
  const hours = Number(match[1])
  const minutes = Number(match[2])
  return hours >= 0 && hours <= 23 && minutes >= 0 && minutes <= 59
}

const canPublish = computed(() => {
  return (
    form.departure.trim().length > 0 &&
    form.destination.trim().length > 0 &&
    form.date &&
    validateTime(form.time) &&
    Number(form.seats) >= 1 &&
    Number(form.price) > 0
  )
})

/* =========================================================
   DATE PICKER LOGIC
========================================================= */
const showCalendar = ref(false)
const datePickerRef = ref(null)

const currentMonth = ref(
  new Date(today.getFullYear(), today.getMonth(), 1)
)

const weekDays = ['L', 'M', 'M', 'J', 'V', 'S', 'D']

const monthNames = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]

const formattedDate = computed(() => {
  if (!form.date) return 'Choisir une date'
  const [year, month, day] = form.date.split('-').map(Number)
  const date = new Date(year, month - 1, day)
  return new Intl.DateTimeFormat('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }).format(date)
})

const currentMonthLabel = computed(() => monthNames[currentMonth.value.getMonth()])
const currentYearLabel = computed(() => currentMonth.value.getFullYear())

const isCurrentMonth = computed(() => {
  return (
    currentMonth.value.getFullYear() === today.getFullYear() &&
    currentMonth.value.getMonth() === today.getMonth()
  )
})

const isSameDate = (first, second) => {
  return (
    first.getFullYear() === second.getFullYear() &&
    first.getMonth() === second.getMonth() &&
    first.getDate() === second.getDate()
  )
}

const calendarDays = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const firstDayIndex = (firstDay.getDay() + 6) % 7
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const daysInPreviousMonth = new Date(year, month, 0).getDate()
  const days = []

  // Jours du mois précédent
  for (let i = firstDayIndex - 1; i >= 0; i--) {
    const dayNumber = daysInPreviousMonth - i
    const date = normalizeDate(new Date(year, month - 1, dayNumber))
    days.push({
      key: `prev-${dayNumber}`,
      day: dayNumber,
      date,
      currentMonth: false,
      isToday: isSameDate(date, today),
      selected: form.date === formatDateValue(date),
      disabled: date < today
    })
  }

  // Jours du mois actuel
  for (let dayNumber = 1; dayNumber <= daysInMonth; dayNumber++) {
    const date = normalizeDate(new Date(year, month, dayNumber))
    days.push({
      key: `curr-${dayNumber}`,
      day: dayNumber,
      date,
      currentMonth: true,
      isToday: isSameDate(date, today),
      selected: form.date === formatDateValue(date),
      disabled: date < today
    })
  }

  // Compléter la dernière semaine
  const remainingDays = (7 - (days.length % 7)) % 7
  for (let dayNumber = 1; dayNumber <= remainingDays; dayNumber++) {
    const date = normalizeDate(new Date(year, month + 1, dayNumber))
    days.push({
      key: `next-${dayNumber}`,
      day: dayNumber,
      date,
      currentMonth: false,
      isToday: isSameDate(date, today),
      selected: form.date === formatDateValue(date),
      disabled: date < today
    })
  }

  return days
})

const openCalendar = () => {
  showSeatOptions.value = false
  showTimeOptions.value = false
  showCalendar.value = true
}

const closeCalendar = () => {
  showCalendar.value = false
}

const goToPreviousMonth = () => {
  if (isCurrentMonth.value) return
  currentMonth.value = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth() - 1,
    1
  )
}

const goToNextMonth = () => {
  currentMonth.value = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth() + 1,
    1
  )
}

const selectDate = (date) => {
  form.date = formatDateValue(date)
  closeCalendar()
}

const selectToday = () => {
  currentMonth.value = new Date(today.getFullYear(), today.getMonth(), 1)
  selectDate(today)
}

/* =========================================================
   TIME PICKER LOGIC
========================================================= */
const showTimeOptions = ref(false)
const timePickerRef = ref(null)

const openTimeOptions = () => {
  showCalendar.value = false
  showSeatOptions.value = false
  showTimeOptions.value = true
}

const closeTimeOptions = () => {
  showTimeOptions.value = false
}

const toggleTimeOptions = () => {
  showCalendar.value = false
  showSeatOptions.value = false
  showTimeOptions.value = !showTimeOptions.value
}

const selectTime = (time) => {
  form.time = time
  closeTimeOptions()
}

const handleTimeInput = (event) => {
  let value = event.target.value.replace(/[^\d:]/g, '')
  if (value.length > 5) value = value.slice(0, 5)
  if (value.length > 2 && !value.includes(':')) {
    value = `${value.slice(0, 2)}:${value.slice(2)}`
  }
  form.time = value
  showTimeOptions.value = true
}

/* =========================================================
   SEAT DROPDOWN LOGIC
========================================================= */
const showSeatOptions = ref(false)
const seatDropdownRef = ref(null)

const toggleSeatOptions = () => {
  showCalendar.value = false
  showTimeOptions.value = false
  showSeatOptions.value = !showSeatOptions.value
}

const closeSeatOptions = () => {
  showSeatOptions.value = false
}

const selectSeat = (seat) => {
  form.seats = seat
  showSeatOptions.value = false
}

/* =========================================================
   PREFERENCES TOGGLE
========================================================= */
const togglePreference = (id) => {
  const index = form.preferences.indexOf(id)
  if (index === -1) {
    form.preferences.push(id)
  } else {
    form.preferences.splice(index, 1)
  }
}

/* =========================================================
   OUTSIDE CLICK LISTENER
========================================================= */
const handleOutsideClick = (event) => {
  if (datePickerRef.value && !datePickerRef.value.contains(event.target)) {
    closeCalendar()
  }
  if (timePickerRef.value && !timePickerRef.value.contains(event.target)) {
    closeTimeOptions()
  }
  if (seatDropdownRef.value && !seatDropdownRef.value.contains(event.target)) {
    closeSeatOptions()
  }
}

onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)

  // Si on est en mode édition d'un trajet existant
  if (isEditMode.value && editTripId.value) {
    try {
      const trip = await serviceTrajets.getDetail(editTripId.value)
      if (trip) {
        form.departure = trip.lieu_depart || ''
        form.destination = trip.destination || ''
        form.date = trip.date || formatDateValue(today)
        form.time = trip.heure_depart ? trip.heure_depart.substring(0, 5) : '08:30'
        form.seats = Number(trip.places_disponibles) || 1
        form.price = Number(trip.prix_par_place) || 0
        form.description = trip.description || ''
        if (Array.isArray(trip.preferences)) {
          const prefRevMap = {
            'NON_FUMEUR': 'no-smoking',
            'ANIMAUX_OK': 'pets',
            'GROS_BAGAGES': 'luggage',
          }
          form.preferences = trip.preferences.map((p) => prefRevMap[p] || p)
        }
      }
    } catch (e) {
      console.error('Erreur chargement trajet à modifier:', e)
      publishError.value = "Impossible de charger les données du trajet."
    }
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick)
})

/* =========================================================
   PUBLICATION & API SUBMISSION
========================================================= */
const showPublishedOverlay = ref(false)
const createdTripId = ref(null)
const publishError = ref('')

const mapPreferences = {
  'no-smoking': 'NON_FUMEUR',
  'pets': 'ANIMAUX_OK',
  'luggage': 'GROS_BAGAGES',
}

const handleSubmit = async () => {
  if (!canPublish.value || isSubmitting.value) return

  isSubmitting.value = true
  publishError.value = ''

  const payload = {
    lieu_depart: form.departure.trim(),
    destination: form.destination.trim(),
    date: form.date,
    heure_depart: form.time.length === 5 ? `${form.time}:00` : form.time,
    places_disponibles: Number(form.seats),
    prix_par_place: Number(form.price),
    description: form.description.trim(),
    preferences: form.preferences.map((p) => mapPreferences[p] || p),
  }

  // 1. Mode modification
  if (isEditMode.value && editTripId.value) {
    try {
      const trajetModifie = await serviceTrajets.modifier(editTripId.value, payload)
      emit('publish', trajetModifie)
      router.replace({
        name: 'vue-trajet-prevu',
        params: { id: editTripId.value },
      })
    } catch (error) {
      console.error('Erreur modification trajet :', error)
      const errData = error.response?.data
      if (errData) {
        if (typeof errData === 'string') {
          publishError.value = errData
        } else if (errData.detail) {
          publishError.value = errData.detail
        } else if (errData.non_field_errors) {
          publishError.value = errData.non_field_errors.join(' ')
        } else {
          publishError.value = Object.entries(errData)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
            .join(' | ')
        }
      } else {
        publishError.value = 'Une erreur est survenue lors de la modification du trajet.'
      }
    } finally {
      isSubmitting.value = false
    }
    return
  }

  // 2. Mode création
  try {
    const nouveauTrajet = await serviceTrajets.publier(payload)
    createdTripId.value = nouveauTrajet.id
    emit('publish', nouveauTrajet)
    showPublishedOverlay.value = true
  } catch (error) {
    console.error('Erreur de publication :', error)
    const errData = error.response?.data
    if (errData) {
      if (typeof errData === 'string') {
        publishError.value = errData
      } else if (errData.detail) {
        publishError.value = errData.detail
      } else if (errData.non_field_errors) {
        publishError.value = errData.non_field_errors.join(' ')
      } else {
        publishError.value = Object.entries(errData)
          .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
          .join(' | ')
      }
    } else {
      publishError.value = 'Une erreur est survenue lors de la publication.'
    }
  } finally {
    isSubmitting.value = false
  }
}

const closePublishedOverlay = () => {
  showPublishedOverlay.value = false
  router.replace('/accueil')
}

const goToTrip = () => {
  showPublishedOverlay.value = false
  if (createdTripId.value) {
    router.replace({
      name: 'vue-trajet-prevu',
      params: { id: createdTripId.value }
    })
  } else {
    router.replace('/conducteur/tableau-de-bord')
  }
}
</script>

<style scoped>
/* =========================================================
   BASE PAGE & LAYOUT
========================================================= */
.publish-trip-page {
  min-height: 100vh;
  background-color: #F8FAFC;
  color: #111625;
  box-sizing: border-box;
}

.publish-page-container {
  width: min(calc(100% - 32px), 640px);
  margin: 0 auto;
  padding: 24px 0 60px;
}

/* =========================================================
   HEADER
========================================================= */
.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.back-button {
  width: 44px;
  height: 44px;
  flex: 0 0 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 1px solid #E2E8F0;
  background: #FFFFFF;
  color: #111625;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.028);
  transition: all 0.2s ease;
}

.back-button:hover {
  background-color: #F1F5F9;
  border-color: #CBD5E1;
  transform: translateX(-1px);
}

.back-button svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 2.2;
  fill: none;
}

.header-titles h1 {
  font-size: 24px;
  font-weight: 800;
  color: #111625;
  margin: 0;
  letter-spacing: -0.4px;
}

.header-subtitle {
  font-size: 13px;
  color: #64748B;
  margin: 2px 0 0;
}

/* =========================================================
   FORM CARDS
========================================================= */
.trip-form-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-colonne-principale {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 22px 24px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.014);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid #F1F5F9;
}

.card-icon-pill {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #FFF1EE;
  color: #FF4D2D;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon-pill svg {
  width: 19px;
  height: 19px;
}

.card-titles h2 {
  font-size: 16px;
  font-weight: 800;
  color: #111625;
  margin: 0;
}

.card-titles p {
  font-size: 12px;
  color: #64748B;
  margin: 1px 0 0;
}

/* =========================================================
   1. ITINÉRAIRE
========================================================= */
.route-inputs-container {
  display: flex;
  flex-direction: column;
}

.route-field-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.route-point-marker {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.marker--start {
  background: #FFF1EE;
  border: 2px solid #FF4D2D;
}

.marker--start span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #FF4D2D;
}

.marker--end {
  background: #111625;
  color: #FFFFFF;
}

.marker--end svg {
  width: 16px;
  height: 16px;
}

.route-connector-line {
  width: 2px;
  height: 18px;
  background: #CBD5E1;
  margin-left: 15px;
  margin-top: 2px;
  margin-bottom: 2px;
}

.route-field-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.route-field-content label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748B;
}

.route-field-content input {
  width: 100%;
  height: 46px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  font-size: 14px;
  font-weight: 600;
  color: #111625;
  outline: none;
  transition: all 0.15s ease;
}

.route-field-content input:focus {
  border-color: #FF4D2D;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(255, 77, 45, 0.04);
}

.route-field-content input::placeholder {
  color: #94A3B8;
  font-weight: 400;
}

/* =========================================================
   2. DETAILS GRID (DATE, HEURE, PLACES, PRIX)
========================================================= */
.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.detail-input-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-input-card label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748B;
}

.picker-trigger-btn {
  width: 100%;
  height: 48px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.15s ease;
}

.picker-trigger-btn:hover {
  border-color: #CBD5E1;
  background: #FFFFFF;
}

.trigger-val-row {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.field-icon {
  width: 18px;
  height: 18px;
  color: #64748B;
  flex-shrink: 0;
}

.field-icon--brand {
  color: #FF4D2D;
}

.val-text {
  font-size: 14px;
  font-weight: 600;
  color: #111625;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.val-text--placeholder {
  color: #94A3B8;
  font-weight: 400;
}

.chevron-icon {
  width: 16px;
  height: 16px;
  color: #94A3B8;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.chevron--open {
  transform: rotate(180deg);
  color: #FF4D2D;
}

/* Time Input */
.time-input-group {
  position: relative;
  height: 48px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  display: flex;
  align-items: center;
  padding: 0 10px;
  gap: 8px;
  transition: all 0.15s ease;
}

.time-input-group:focus-within {
  border-color: #FF4D2D;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(255, 77, 45, 0.04);
}

.time-input-field {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  font-weight: 600;
  color: #111625;
  outline: none;
  width: 100%;
}

.time-chevron-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

/* Price Input */
.price-input-row {
  height: 48px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 8px;
  transition: all 0.15s ease;
}

.price-input-row:focus-within {
  border-color: #FF4D2D;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(255, 77, 45, 0.04);
}

.price-number-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 15px;
  font-weight: 700;
  color: #111625;
  outline: none;
  width: 100%;
}

.price-currency-suffix {
  font-size: 11px;
  font-weight: 800;
  color: #64748B;
  letter-spacing: 0.5px;
}

/* =========================================================
   POPOVERS (CALENDAR, TIME, SEAT)
========================================================= */
.picker-field {
  position: relative;
}

.picker-field--open {
  z-index: 50;
}

.calendar-menu-popover,
.time-menu-popover,
.seat-menu-popover {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
  padding: 14px;
  z-index: 100;
}

.calendar-menu-popover {
  width: 290px;
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.calendar-month-display {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #111625;
}

.calendar-month-display strong {
  text-transform: capitalize;
}

.calendar-nav-btn {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #475569;
}

.calendar-nav-btn:hover:not(:disabled) {
  background: #F1F5F9;
}

.calendar-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.calendar-nav-btn svg {
  width: 14px;
  height: 14px;
}

.calendar-weekdays-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  margin-bottom: 6px;
  text-align: center;
  font-size: 11px;
  font-weight: 700;
  color: #94A3B8;
}

.calendar-days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day-btn {
  height: 32px;
  border-radius: 8px;
  border: none;
  background: transparent;
  font-size: 12px;
  font-weight: 600;
  color: #111625;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-day-btn:hover:not(:disabled) {
  background: #F1F5F9;
}

.day--outside {
  color: #CBD5E1;
}

.day--today {
  border: 1px solid #FF4D2D;
  color: #FF4D2D;
}

.day--selected {
  background: #FF4D2D !important;
  color: #FFFFFF !important;
}

.day--disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.calendar-footer-row {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #F1F5F9;
  text-align: center;
}

.btn-today-shortcut {
  background: none;
  border: none;
  font-size: 12px;
  font-weight: 700;
  color: #FF4D2D;
  cursor: pointer;
}

/* Time popover */
.time-menu-popover {
  width: 250px;
}

.time-menu-title {
  display: block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: #64748B;
  margin-bottom: 8px;
}

.suggested-times-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.time-chip-btn {
  padding: 6px;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  font-size: 12px;
  font-weight: 600;
  color: #111625;
  cursor: pointer;
  transition: all 0.15s ease;
}

.time-chip-btn:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
}

.time-chip--active {
  background: #FFF1EE;
  border-color: #FF4D2D;
  color: #FF4D2D;
}

/* Seat Popover */
.seat-menu-popover {
  width: 230px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.seat-item-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 10px;
  border: none;
  background: transparent;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.seat-item-btn:hover {
  background: #F1F5F9;
}

.seat-num {
  width: 22px;
  font-size: 14px;
  font-weight: 800;
  color: #111625;
}

.seat-label {
  flex: 1;
  font-size: 13px;
  color: #475569;
}

.check-icon {
  width: 15px;
  height: 15px;
  color: #FF4D2D;
}

.seat-item--selected {
  background: #FFF1EE;
}

.seat-item--selected .seat-num,
.seat-item--selected .seat-label {
  color: #FF4D2D;
  font-weight: 700;
}

/* =========================================================
   3. PRÉFÉRENCES & DESCRIPTION
========================================================= */
.preferences-block {
  margin-bottom: 16px;
}

.field-sublabel {
  display: block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748B;
  margin-bottom: 8px;
}

.preferences-chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pref-chip-btn {
  height: 38px;
  padding: 0 14px;
  border-radius: 10px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}

.pref-chip-btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
}

.pref-chip-btn:hover {
  border-color: #CBD5E1;
  background: #FFFFFF;
}

.pref-chip--active {
  background: #FFF1EE;
  border-color: #FF4D2D;
  color: #FF4D2D;
  font-weight: 700;
}

.description-block {
  display: flex;
  flex-direction: column;
}

.desc-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.char-count-text {
  font-size: 11px;
  color: #94A3B8;
}

.description-textarea {
  width: 100%;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  font-size: 13px;
  font-family: inherit;
  color: #111625;
  outline: none;
  resize: vertical;
  min-height: 72px;
  transition: all 0.15s ease;
}

.description-textarea:focus {
  border-color: #FF4D2D;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(255, 77, 45, 0.04);
}

.description-textarea::placeholder {
  color: #94A3B8;
}

/* =========================================================
   BOUTONS DE PUBLICATION
========================================================= */
.btn-primary-publish {
  width: 100%;
  height: 50px;
  border-radius: 14px;
  border: none;
  background: #FF4D2D;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(255, 77, 45, 0.09);
  transition: all 0.2s ease;
  padding: 0 16px;
}

.btn-publish-content {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

.btn-publish-content svg {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.btn-primary-publish:hover:not(:disabled) .btn-publish-content svg {
  transform: translateX(3px);
}

.btn-primary-publish:hover:not(:disabled) {
  background: #E03E20;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.11);
}

.btn-primary-publish:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.btn-spinner-state {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.publish-error-alert {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #DC2626;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 14px;
  border-radius: 10px;
  margin-bottom: 12px;
  text-align: center;
}

.terms-note {
  font-size: 11px;
  color: #94A3B8;
  text-align: center;
  margin-top: 10px;
  line-height: 1.4;
}

/* Sidebar desktop cachée sur mobile */
.sidebar-recap-desktop {
  display: none;
}

/* =========================================================
   VERSION DESKTOP (@media min-width: 960px)
========================================================= */
@media (min-width: 960px) {
  .publish-page-container {
    width: min(calc(100% - 64px), 1120px);
    max-width: 1120px;
    padding: 36px 0 72px;
  }

  .header-titles h1 {
    font-size: 28px;
  }

  .header-subtitle {
    font-size: 14px;
  }

  .trip-form-layout {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 32px;
    align-items: flex-start;
  }

  /* Cacher le bouton mobile sur desktop */
  .mobile-submit-box {
    display: none;
  }

  /* Sidebar récapitulative visible sur desktop */
  .sidebar-recap-desktop {
    display: block;
    position: sticky;
    top: 24px;
  }

  .recap-card-sticky {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.014);
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .recap-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .recap-header h3 {
    margin: 0;
    font-size: 19px;
    font-weight: 800;
    color: #111625;
    letter-spacing: -0.3px;
  }

  .recap-route-box {
    background: #F8FAFC;
    border: 1px solid #EDF2F7;
    border-radius: 14px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .recap-route-row {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .recap-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .start-dot {
    background: #FF4D2D;
  }

  .end-dot {
    background: #111625;
  }

  .recap-route-line {
    width: 2px;
    height: 12px;
    background: #CBD5E1;
    margin-left: 4px;
  }

  .recap-route-info small {
    display: block;
    font-size: 9px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
  }

  .recap-route-info strong {
    display: block;
    font-size: 13px;
    color: #111625;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .recap-meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    padding-bottom: 14px;
    border-bottom: 1px solid #F1F5F9;
  }

  .meta-item {
    background: #F8FAFC;
    border: 1px solid #EDF2F7;
    border-radius: 10px;
    padding: 8px;
    text-align: center;
  }

  .meta-label {
    display: block;
    font-size: 10px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
  }

  .meta-value {
    display: block;
    font-size: 12px;
    color: #111625;
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .recap-revenue-box {
    background: #F0FDF4;
    border: 1px solid #DCFCE7;
    border-radius: 14px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .revenue-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #166534;
  }

  .revenue-line.total {
    padding-top: 6px;
    border-top: 1px dashed #BBF7D0;
    font-size: 13px;
    font-weight: 700;
  }

  .revenue-line.total small {
    display: block;
    font-size: 10px;
    color: #15803D;
    font-weight: 500;
  }

  .gain-highlight {
    font-size: 16px;
    font-weight: 800;
    color: #15803D;
  }

  .recap-disclaimer {
    font-size: 11px;
    color: #94A3B8;
    line-height: 1.45;
    margin: 0;
    text-align: center;
  }
}

/* Animations transition picker */
.picker-menu-enter-active,
.picker-menu-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.picker-menu-enter-from,
.picker-menu-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>