<template>
  <div class="publish-trip-page">
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

      <h1>Publier un trajet</h1>
    </header>

    <!-- =====================================================
         CONTENT
    ====================================================== -->
    <main class="page-content">
      <form
        class="trip-form"
        @submit.prevent="handleSubmit"
      >
        <!-- =================================================
             ITINÉRAIRE
        ================================================== -->
        <section class="form-section">
          <div class="section-title">
            <span class="section-accent"></span>
            <h2>Itinéraire</h2>
          </div>

          <div class="route-fields">
            <!-- ================= DÉPART ================= -->
            <div class="location-field">
              <div class="location-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <circle cx="12" cy="12" r="7.5" />
                  <circle cx="12" cy="12" r="2.8" />
                </svg>
              </div>

              <div class="location-content">
                <label for="departure">
                  Lieu de départ
                </label>

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

            <!-- Ligne verticale -->
            <div
              class="route-line"
              aria-hidden="true"
            ></div>

            <!-- ================= DESTINATION ================= -->
            <div class="location-field">
              <div class="location-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M12 21s6.5-6.2 6.5-11A6.5 6.5 0 1 0 5.5 10c0 4.8 6.5 11 6.5 11Z"
                  />
                  <circle cx="12" cy="10" r="2.3" />
                </svg>
              </div>

              <div class="location-content">
                <label for="destination">
                  Destination
                </label>

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

        <!-- =================================================
             DATE & DÉTAILS
        ================================================== -->
        <section class="form-section">
          <div class="section-title">
            <span class="section-accent"></span>
            <h2>Date & détails</h2>
          </div>

          <div class="details-grid">
            <!-- =================================================
                 DATE
            ================================================== -->
            <div
              ref="datePickerRef"
              class="detail-field picker-field"
              :class="{
                'picker-field--open': showCalendar
              }"
            >
              <div class="detail-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <rect
                    x="4"
                    y="5.5"
                    width="16"
                    height="15"
                    rx="2"
                  />
                  <path d="M8 3.5V8" />
                  <path d="M16 3.5V8" />
                  <path d="M4 10h16" />
                </svg>
              </div>

              <div class="detail-content picker-content">
                <span class="detail-label">
                  Date
                </span>

                <button
                  type="button"
                  class="picker-trigger"
                  :aria-expanded="showCalendar"
                  aria-haspopup="dialog"
                  @click.stop="openCalendar"
                  @keydown.esc="closeCalendar"
                >
                  <span
                    class="picker-value"
                    :class="{
                      'picker-value--muted':
                        !form.date
                    }"
                  >
                    {{ formattedDate }}
                  </span>

                  <svg
                    class="picker-chevron"
                    :class="{
                      'picker-chevron--open':
                        showCalendar
                    }"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path d="M7 10l5 5 5-5" />
                  </svg>
                </button>

                <!-- ================= CALENDRIER ================= -->
                <Transition name="picker-menu">
                  <div
                    v-if="showCalendar"
                    class="calendar-menu"
                    role="dialog"
                    aria-label="Choisir une date"
                    @click.stop
                  >
                    <!-- Header calendrier -->
                    <div class="calendar-header">
                      <button
                        type="button"
                        class="calendar-nav"
                        aria-label="Mois précédent"
                        :disabled="isCurrentMonth"
                        @click="goToPreviousMonth"
                      >
                        <svg
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path d="M15 18l-6-6 6-6" />
                        </svg>
                      </button>

                      <div class="calendar-month">
                        <span
                          class="calendar-month-name"
                        >
                          {{ currentMonthLabel }}
                        </span>

                        <span class="calendar-year">
                          {{ currentYearLabel }}
                        </span>
                      </div>

                      <button
                        type="button"
                        class="calendar-nav"
                        aria-label="Mois suivant"
                        @click="goToNextMonth"
                      >
                        <svg
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path d="M9 18l6-6-6-6" />
                        </svg>
                      </button>
                    </div>

                    <!-- Jours de la semaine -->
                    <div class="calendar-weekdays">
                      <span
                        v-for="day in weekDays"
                        :key="day"
                      >
                        {{ day }}
                      </span>
                    </div>

                    <!-- Jours -->
                    <div class="calendar-grid">
                      <button
                        v-for="day in calendarDays"
                        :key="day.key"
                        type="button"
                        class="calendar-day"
                        :class="{
                          'calendar-day--outside':
                            !day.currentMonth,

                          'calendar-day--today':
                            day.isToday,

                          'calendar-day--selected':
                            day.selected,

                          'calendar-day--disabled':
                            day.disabled
                        }"
                        :disabled="day.disabled"
                        @click="selectDate(day.date)"
                      >
                        {{ day.day }}
                      </button>
                    </div>

                    <!-- Footer -->
                    <div class="calendar-footer">
                      <button
                        type="button"
                        class="calendar-today-button"
                        @click="selectToday"
                      >
                        Aujourd'hui
                      </button>
                    </div>
                  </div>
                </Transition>
              </div>
            </div>

            <!-- =================================================
                 HEURE
            ================================================== -->
            <div
              ref="timePickerRef"
              class="detail-field picker-field"
              :class="{
                'picker-field--open':
                  showTimeOptions
              }"
            >
              <div class="detail-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <circle cx="12" cy="12" r="8.5" />
                  <path d="M12 7.5V12L15 14" />
                </svg>
              </div>

              <div class="detail-content picker-content">
                <span class="detail-label">
                  Heure
                </span>

                <div class="time-input-wrapper">
                  <input
                    id="trip-time"
                    :value="form.time"
                    type="text"
                    inputmode="numeric"
                    autocomplete="off"
                    maxlength="5"
                    placeholder="08:30"
                    class="time-input"
                    aria-label="Heure du départ"
                    @input="handleTimeInput"
                    @focus="openTimeOptions"
                    @keydown.esc="closeTimeOptions"
                  />

                  <button
                    type="button"
                    class="time-trigger"
                    aria-label="Afficher les horaires"
                    :aria-expanded="
                      showTimeOptions
                    "
                    @click.stop="toggleTimeOptions"
                  >
                    <svg
                      class="picker-chevron"
                      :class="{
                        'picker-chevron--open':
                          showTimeOptions
                      }"
                      viewBox="0 0 24 24"
                      aria-hidden="true"
                    >
                      <path d="M7 10l5 5 5-5" />
                    </svg>
                  </button>
                </div>

                <!-- ================= HORAIRES ================= -->
                <Transition name="picker-menu">
                  <div
                    v-if="showTimeOptions"
                    class="time-menu"
                    @click.stop
                  >
                    <div class="time-menu-header">
                      Horaires suggérés
                    </div>

                    <div class="time-grid">
                      <button
                        v-for="time in suggestedTimes"
                        :key="time"
                        type="button"
                        class="time-option"
                        :class="{
                          'time-option--selected':
                            form.time === time
                        }"
                        @click="selectTime(time)"
                      >
                        {{ time }}
                      </button>
                    </div>

                    <div class="time-help">
                      Vous pouvez aussi saisir l'heure
                      manuellement.
                    </div>
                  </div>
                </Transition>
              </div>
            </div>

            <!-- =================================================
                 PLACES
            ================================================== -->
            <div
              ref="seatDropdownRef"
              class="detail-field picker-field seat-field"
              :class="{
                'picker-field--open':
                  showSeatOptions
              }"
            >
              <div class="detail-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <circle cx="9" cy="9" r="3.2" />
                  <path
                    d="M3.5 19c.7-3.1 2.6-4.8 5.5-4.8s4.8 1.7 5.5 4.8"
                  />
                  <circle cx="16.8" cy="9.7" r="2.4" />
                  <path
                    d="M14.5 14.8c2.7.1 4.4 1.5 5 4.2"
                  />
                </svg>
              </div>

              <div class="detail-content picker-content">
                <span class="detail-label">
                  Places
                </span>

                <button
                  type="button"
                  class="picker-trigger"
                  :aria-expanded="
                    showSeatOptions
                  "
                  aria-haspopup="listbox"
                  @click.stop="toggleSeatOptions"
                  @keydown.esc="closeSeatOptions"
                >
                  <span class="picker-value">
                    {{ form.seats }}
                    {{
                      form.seats > 1
                        ? 'places'
                        : 'place'
                    }}
                  </span>

                  <svg
                    class="picker-chevron"
                    :class="{
                      'picker-chevron--open':
                        showSeatOptions
                    }"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path d="M7 10l5 5 5-5" />
                  </svg>
                </button>

                <!-- ================= DROPDOWN ================= -->
                <Transition name="picker-menu">
                  <div
                    v-if="showSeatOptions"
                    class="seat-menu"
                    role="listbox"
                    @click.stop
                  >
                    <!-- <div class="seat-menu-header">
                      <span>Nombre de places</span>
                      <span>Passagers</span>
                    </div> -->

                    <button
                      v-for="seat in seatOptions"
                      :id="`seat-option-${seat}`"
                      :key="seat"
                      type="button"
                      role="option"
                      :aria-selected="
                        form.seats === seat
                      "
                      class="seat-option"
                      :class="{
                        'seat-option--selected':
                          form.seats === seat
                      }"
                      @click="selectSeat(seat)"
                    >
                      <span class="seat-option-left">
                        <span
                          class="seat-option-number"
                        >
                          {{ seat }}
                        </span>

                        <span
                          class="seat-option-text"
                        >
                          {{
                            seat > 1
                              ? 'places'
                              : 'place'
                          }}
                        </span>
                      </span>

                      <svg
                        v-if="form.seats === seat"
                        class="seat-check"
                        viewBox="0 0 24 24"
                        aria-hidden="true"
                      >
                        <path
                          d="M5 12.5l4.5 4.5L19 7.5"
                        />
                      </svg>
                    </button>

                    <!-- <div class="seat-menu-footer">
                      Choisissez le nombre de passagers
                      que vous pouvez accueillir.
                    </div> -->
                  </div>
                </Transition>
              </div>
            </div>

            <!-- =================================================
                 PRIX
            ================================================== -->
            <div class="detail-field">
              <div
                class="detail-icon detail-icon--accent"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M4 5.5V11l8.5 8.5a2 2 0 0 0 2.8 0l3.2-3.2a2 2 0 0 0 0-2.8L10 5H4Z"
                  />
                  <circle cx="7.5" cy="8.5" r="1.2" />
                </svg>
              </div>

              <div class="detail-content">
                <label for="price">
                  Prix / pers.
                </label>

                <div class="price-input">
                  <input
                    id="price"
                    v-model.number="form.price"
                    type="number"
                    min="0"
                    step="100"
                    placeholder="5 000"
                    required
                  />

                  <span>FCFA</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- =================================================
             DESCRIPTION
        ================================================== -->
        <section class="form-section">
          <div class="section-title">
            <span class="section-accent"></span>
            <h2>Description</h2>
          </div>

          <div class="description-field">
            <textarea
              v-model.trim="form.description"
              maxlength="500"
              placeholder="Ajoutez une précision utile pour vos passagers..."
              required
            ></textarea>

            <div class="character-count">
              {{ form.description.length }}/500
            </div>
          </div>
        </section>

        <!-- =================================================
             PRÉFÉRENCES
        ================================================== -->
        <section class="form-section">
          <div class="section-title">
            <span class="section-accent"></span>
            <h2>Préférences</h2>
          </div>

          <div class="preferences">
            <!-- NON FUMEUR -->
            <button
              type="button"
              class="preference-chip"
              :class="{
                'preference-chip--active':
                  form.preferences.includes(
                    'no-smoking'
                  )
              }"
              :aria-pressed="
                form.preferences.includes(
                  'no-smoking'
                )
              "
              @click="togglePreference('no-smoking')"
            >
              <svg
                class="preference-icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <circle cx="12" cy="12" r="9" />
                <path d="M8 15h7.5" />
                <path d="M17 15h.8" />
                <path d="M6 6l12 12" />
              </svg>

              <span>Non fumeur</span>
            </button>

            <!-- ANIMAUX -->
            <button
              type="button"
              class="preference-chip"
              :class="{
                'preference-chip--active':
                  form.preferences.includes(
                    'pets'
                  )
              }"
              :aria-pressed="
                form.preferences.includes(
                  'pets'
                )
              "
              @click="togglePreference('pets')"
            >
              <svg
                class="preference-icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M12 18c-1.6 0-2.3-1.2-3.8-1.2S5.8 18 5.8 16.2c0-1.4.8-2.3 1.9-3.2C8.4 12.2 9 11 9 9.7a3 3 0 0 1 6 0c0 1.3.6 2.5 1.3 3.3 1.1.9 1.9 1.8 1.9 3.2 0 1.8-1 2.8-2.4 2.8S13.6 18 12 18Z"
                />
                <circle cx="6.8" cy="7.2" r="1.7" />
                <circle cx="17.2" cy="7.2" r="1.7" />
                <circle cx="4.8" cy="10.7" r="1.5" />
                <circle cx="19.2" cy="10.7" r="1.5" />
              </svg>

              <span>Animaux OK</span>
            </button>

            <!-- BAGAGES -->
            <button
              type="button"
              class="preference-chip"
              :class="{
                'preference-chip--active':
                  form.preferences.includes(
                    'luggage'
                  )
              }"
              :aria-pressed="
                form.preferences.includes(
                  'luggage'
                )
               "
              @click="togglePreference('luggage')"
            >
              <svg
                class="preference-icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <rect
                  x="5"
                  y="7"
                  width="14"
                  height="12"
                  rx="2"
                />
                <path d="M9 7V5h6v2" />
                <path d="M9 10v6" />
                <path d="M15 10v6" />
              </svg>

              <span>Gros bagages</span>
            </button>
          </div>
        </section>

        <!-- =================================================
             SUBMIT
        ================================================== -->
        <section class="submit-section">
          <button
            type="submit"
            class="publish-button"
            :disabled="
              !canPublish ||
              isSubmitting
            "
          >
            <span v-if="!isSubmitting">
              Publier le trajet
            </span>

            <span
              v-else
              class="loading-state"
            >
              <span class="spinner"></span>
              Publication...
            </span>

            <svg
              v-if="!isSubmitting"
              class="publish-arrow"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M5 12h13" />
              <path d="M13 6l6 6-6 6" />
            </svg>
          </button>

          <p class="legal-text">
            En publiant ce trajet, vous acceptez nos
            <a href="#">
              Conditions Générales
            </a>
            et notre charte de bonne conduite.
          </p>
        </section>
      </form>
    </main>
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
import { useRouter } from 'vue-router'

/* =========================================================
   ROUTER / EVENTS
========================================================= */

const router = useRouter()

const emit = defineEmits([
  'back',
  'publish'
])

/* =========================================================
   HELPERS DATE
========================================================= */

const normalizeDate = (date) => {
  const result = new Date(date)

  result.setHours(12, 0, 0, 0)

  return result
}

const today = normalizeDate(
  new Date()
)

const formatDateValue = (date) => {
  const year =
    date.getFullYear()

  const month =
    String(
      date.getMonth() + 1
    ).padStart(2, '0')

  const day =
    String(
      date.getDate()
    ).padStart(2, '0')

  return `${year}-${month}-${day}`
}

/* =========================================================
   FORM
========================================================= */

const form = reactive({

  departure:
    'Dakar, Sénégal',

  destination:
    'Saint-Louis, Sénégal',

  date:
    formatDateValue(today),

  time:
    '08:30',

  seats:
    3,

  price:
    5000,

  description:
    '',

  /*
   * Les préférences visibles comme actives
   * dans la maquette.
   */
  preferences: [
    'no-smoking',
    'pets'
  ]
})

const isSubmitting = ref(false)

/* =========================================================
   OPTIONS
========================================================= */

const seatOptions = [
  1,
  2,
  3,
  4,
  5,
  6,
  7
]

const suggestedTimes = [
  '06:00',
  '06:30',
  '07:00',
  '07:30',
  '08:00',
  '08:30',
  '09:00',
  '09:30',
  '10:00',
  '11:00',
  '12:00',
  '13:00',
  '14:00',
  '15:00',
  '16:00',
  '17:00',
  '17:30',
  '18:00',
  '18:30',
  '19:00'
]

/* =========================================================
   VALIDATION
========================================================= */

const validateTime = (value) => {
  const match = String(value).match(
    /^(\d{2}):(\d{2})$/
  )

  if (!match) {
    return false
  }

  const hours =
    Number(match[1])

  const minutes =
    Number(match[2])

  return (
    hours >= 0 &&
    hours <= 23 &&
    minutes >= 0 &&
    minutes <= 59
  )
}

const canPublish = computed(() => {
  return (
    form.departure.trim().length > 0 &&
    form.destination.trim().length > 0 &&
    form.date &&
    validateTime(form.time) &&
    Number(form.seats) >= 1 &&
    Number(form.price) > 0 &&
    form.description.trim().length > 0
  )
})

/* =========================================================
   DATE PICKER
========================================================= */

const showCalendar = ref(false)
const datePickerRef = ref(null)

const currentMonth = ref(
  new Date(
    today.getFullYear(),
    today.getMonth(),
    1
  )
)

const weekDays = [
  'L',
  'M',
  'M',
  'J',
  'V',
  'S',
  'D'
]

const monthNames = [
  'Janvier',
  'Février',
  'Mars',
  'Avril',
  'Mai',
  'Juin',
  'Juillet',
  'Août',
  'Septembre',
  'Octobre',
  'Novembre',
  'Décembre'
]

const formattedDate = computed(() => {
  if (!form.date) {
    return 'Choisir une date'
  }

  const [
    year,
    month,
    day
  ] = form.date
    .split('-')
    .map(Number)

  const date = new Date(
    year,
    month - 1,
    day
  )

  return new Intl.DateTimeFormat(
    'fr-FR',
    {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    }
  ).format(date)
})

const currentMonthLabel =
  computed(() => {
    return monthNames[
      currentMonth.value.getMonth()
    ]
  })

const currentYearLabel =
  computed(() => {
    return currentMonth.value
      .getFullYear()
  })

const isCurrentMonth =
  computed(() => {
    return (
      currentMonth.value
        .getFullYear() ===
        today.getFullYear() &&
      currentMonth.value
        .getMonth() ===
        today.getMonth()
    )
  })

const isSameDate = (
  first,
  second
) => {
  return (
    first.getFullYear() ===
      second.getFullYear() &&
    first.getMonth() ===
      second.getMonth() &&
    first.getDate() ===
      second.getDate()
  )
}

const calendarDays = computed(() => {
  const year =
    currentMonth.value
      .getFullYear()

  const month =
    currentMonth.value
      .getMonth()

  const firstDay =
    new Date(
      year,
      month,
      1
    )

  /*
   * JS :
   * Dimanche = 0
   * Lundi = 1
   *
   * On transforme pour commencer par lundi.
   */
  const startOffset =
    (firstDay.getDay() + 6) % 7

  const daysInMonth =
    new Date(
      year,
      month + 1,
      0
    ).getDate()

  const previousMonthDays =
    new Date(
      year,
      month,
      0
    ).getDate()

  const result = []

  /*
   * Jours du mois précédent.
   */
  for (
    let index =
      startOffset - 1;
    index >= 0;
    index--
  ) {
    const dayNumber =
      previousMonthDays -
      index

    const date =
      new Date(
        year,
        month - 1,
        dayNumber,
        12
      )

    result.push({
      key:
        `previous-${formatDateValue(date)}`,

      date,

      day:
        dayNumber,

      currentMonth:
        false,

      isToday:
        false,

      selected:
        form.date ===
        formatDateValue(date),

      disabled:
        true
    })
  }

  /*
   * Jours du mois courant.
   */
  for (
    let dayNumber = 1;
    dayNumber <= daysInMonth;
    dayNumber++
  ) {
    const date =
      new Date(
        year,
        month,
        dayNumber,
        12
      )

    const value =
      formatDateValue(date)

    result.push({
      key: value,

      date,

      day:
        dayNumber,

      currentMonth:
        true,

      isToday:
        isSameDate(
          date,
          today
        ),

      selected:
        form.date === value,

      disabled:
        date < today
    })
  }

  /*
   * Compléter la dernière ligne.
   */
  let nextDay = 1

  while (
    result.length < 42
  ) {
    const date =
      new Date(
        year,
        month + 1,
        nextDay,
        12
      )

    result.push({
      key:
        `next-${formatDateValue(date)}`,

      date,

      day:
        nextDay,

      currentMonth:
        false,

      isToday:
        false,

      selected:
        form.date ===
        formatDateValue(date),

      disabled:
        true
    })

    nextDay++
  }

  return result
})

const openCalendar = () => {
  /*
   * Si une date est déjà sélectionnée,
   * on ouvre directement le bon mois.
   */
  if (form.date) {
    const [
      year,
      month
    ] = form.date
      .split('-')
      .map(Number)

    currentMonth.value =
      new Date(
        year,
        month - 1,
        1
      )
  }

  /*
   * Ferme l'autre dropdown.
   */
  showTimeOptions.value = false
  showSeatOptions.value = false

  showCalendar.value = true
}

const closeCalendar = () => {
  showCalendar.value = false
}

const goToPreviousMonth =
  () => {
    if (
      isCurrentMonth.value
    ) {
      return
    }

    currentMonth.value =
      new Date(
        currentMonth.value.getFullYear(),
        currentMonth.value.getMonth() - 1,
        1
      )
  }

const goToNextMonth = () => {
  currentMonth.value =
    new Date(
      currentMonth.value.getFullYear(),
      currentMonth.value.getMonth() + 1,
      1
    )
}

const selectDate = (
  date
) => {
  const normalizedDate =
    normalizeDate(date)

  if (
    normalizedDate < today
  ) {
    return
  }

  form.date =
    formatDateValue(
      normalizedDate
    )

  showCalendar.value = false
}

const selectToday = () => {
  form.date =
    formatDateValue(today)

  currentMonth.value =
    new Date(
      today.getFullYear(),
      today.getMonth(),
      1
    )

  showCalendar.value = false
}

/* =========================================================
   TIME PICKER
========================================================= */

const showTimeOptions =
  ref(false)

const timePickerRef =
  ref(null)

const openTimeOptions = () => {
  showCalendar.value = false
  showSeatOptions.value = false

  showTimeOptions.value = true
}

const toggleTimeOptions =
  () => {
    showCalendar.value = false
    showSeatOptions.value = false

    showTimeOptions.value =
      !showTimeOptions.value
  }

const closeTimeOptions =
  () => {
    showTimeOptions.value = false
  }

const selectTime = (
  time
) => {
  form.time = time

  showTimeOptions.value = false
}

const handleTimeInput =
  (event) => {
    /*
     * On autorise uniquement les chiffres.
     */
    let value =
      event.target.value
        .replace(/\D/g, '')
        .slice(0, 4)

    /*
     * Ajout automatique des deux-points.
     *
     * 0830 -> 08:30
     */
    if (
      value.length > 2
    ) {
      value =
        `${value.slice(0, 2)}:${value.slice(2)}`
    }

    form.time = value

    /*
     * On garde le menu ouvert
     * tant que l'utilisateur saisit.
     */
    showTimeOptions.value = true
  }

/* =========================================================
   SEAT DROPDOWN
========================================================= */

const showSeatOptions =
  ref(false)

const seatDropdownRef =
  ref(null)

const toggleSeatOptions =
  () => {
    showCalendar.value = false
    showTimeOptions.value = false

    showSeatOptions.value =
      !showSeatOptions.value
  }

const closeSeatOptions =
  () => {
    showSeatOptions.value = false
  }

const selectSeat = (
  seat
) => {
  form.seats = seat

  showSeatOptions.value = false
}

/* =========================================================
   PREFERENCES
========================================================= */

const togglePreference = (
  id
) => {
  const index =
    form.preferences.indexOf(id)

  if (index === -1) {
    form.preferences.push(id)
    return
  }

  form.preferences.splice(
    index,
    1
  )
}

/* =========================================================
   OUTSIDE CLICK
========================================================= */

const handleOutsideClick = (
  event
) => {
  if (
    datePickerRef.value &&
    !datePickerRef.value.contains(
      event.target
    )
  ) {
    closeCalendar()
  }

  if (
    timePickerRef.value &&
    !timePickerRef.value.contains(
      event.target
    )
  ) {
    closeTimeOptions()
  }

  if (
    seatDropdownRef.value &&
    !seatDropdownRef.value.contains(
      event.target
    )
  ) {
    closeSeatOptions()
  }
}

onMounted(() => {
  document.addEventListener(
    'click',
    handleOutsideClick
  )
})

onBeforeUnmount(() => {
  document.removeEventListener(
    'click',
    handleOutsideClick
  )
})

/* =========================================================
   NAVIGATION
========================================================= */
const showPublishedOverlay =
  ref(false)

const handleSubmit = async () => {
  if (
    !canPublish.value ||
    isSubmitting.value
  ) {
    return
  }

  isSubmitting.value = true

  const payload = {
    departure:
      form.departure.trim(),

    destination:
      form.destination.trim(),

    date:
      form.date,

    time:
      form.time,

    seats:
      Number(form.seats),

    price:
      Number(form.price),

    description:
      form.description.trim(),

    preferences:
      [...form.preferences]
  }

  try {

    /*
     * Ici :
     *
     * await tripService.createTrip(payload)
     */

    emit(
      'publish',
      payload
    )

    /*
     * Une fois la publication réussie :
     */
    showPublishedOverlay.value =
      true

  } catch (error) {

    console.error(
      'Erreur de publication :',
      error
    )

  } finally {

    isSubmitting.value = false
  }
}

const closePublishedOverlay = () => {
  showPublishedOverlay.value =
    false
}

const goToTrip = () => {
  showPublishedOverlay.value =
    false

  router.push(
    '/mes-trajets'
  )
}  

</script>

<style scoped>
/* =========================================================
   DESIGN TOKENS
========================================================= */

.publish-trip-page {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;

  --black: #111627;
  --dark-gray: #374151;

  --gray: #6b7280;
  --muted: #9ca3af;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  --accent-soft: #fff5f2;

  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 28px;
  --radius-full: 9999px;

  min-height: 100vh;

  background: #ffffff;

  color: var(--black);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  box-sizing: border-box;
}

.publish-trip-page *,
.publish-trip-page *::before,
.publish-trip-page *::after {
  box-sizing: border-box;
}


/* =========================================================
   HEADER
========================================================= */

.page-header {
  width: min(100%, 586px);

  margin: 0 auto;

  padding-top: 48px;

  display: grid;
  grid-template-columns: 58px 1fr;

  align-items: center;

  gap: 30px;
}

.page-header h1 {
  margin: 0;

  color: var(--black);

  font-size: 36px;
  line-height: 1.15;

  font-weight: 800;

  letter-spacing: -1.2px;
}


/* =========================================================
   BACK BUTTON
========================================================= */

.back-button {
  width: 58px;
  height: 58px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  border: 0;
  border-radius: 50%;

  background: #f4f5f6;

  color: var(--black);

  cursor: pointer;

  transition:
    background-color 180ms ease,
    transform 180ms ease;
}

.back-button:hover {
  background: #eceef1;

  transform: translateX(-1px);
}

.back-button:active {
  transform: translateX(0);
}

.back-button:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.2);
  outline-offset: 3px;
}

.back-button svg {
  width: 26px;
  height: 26px;

  fill: none;

  stroke: currentColor;
  stroke-width: 2.4;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   CONTENT
========================================================= */

.page-content {
  width: min(100%, 586px);

  margin: 0 auto;

  padding:
    68px
    0
    80px;
}


/* =========================================================
   FORM
========================================================= */

.trip-form {
  display: flex;
  flex-direction: column;

  gap: 70px;
}


/* =========================================================
   SECTION TITLE
========================================================= */

.section-title {
  display: flex;
  align-items: center;

  gap: 14px;

  margin-bottom: 28px;
}

.section-accent {
  width: 7px;
  height: 29px;

  flex-shrink: 0;

  border-radius: var(--radius-full);

  background: var(--brand);
}

.section-title h2 {
  margin: 0;

  color: #8b919b;

  font-size: 25px;
  line-height: 1;

  font-weight: 700;

  letter-spacing: 0.7px;

  text-transform: uppercase;
}


/* =========================================================
   ITINÉRAIRE
========================================================= */

.route-fields {
  display: flex;
  flex-direction: column;
}

.location-field {
  min-height: 120px;

  display: flex;
  align-items: center;

  gap: 22px;

  padding:
    20px
    30px;

  border-radius: 28px;

  background: var(--light-gray);
}

.location-icon {
  width: 30px;
  height: 30px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  color: var(--brand);
}

.location-icon svg {
  width: 26px;
  height: 26px;

  fill: none;

  stroke: currentColor;
  stroke-width: 2.2;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.location-content {
  min-width: 0;

  display: flex;
  flex-direction: column;

  gap: 9px;
}

.location-content label,
.detail-content label,
.detail-label {
  color: #a5aab2;

  font-size: 16px;
  line-height: 1;

  font-weight: 700;

  text-transform: uppercase;
}

.location-content input {
  width: 100%;

  padding: 0;

  border: 0;
  outline: none;

  background: transparent;

  color: var(--black);

  font-family: inherit;

  font-size: 27px;
  line-height: 1.2;

  font-weight: 500;
}

.location-content input::placeholder {
  color: var(--muted);
}


/* =========================================================
   ROUTE LINE
========================================================= */

.route-line {
  width: 4px;
  height: 30px;

  margin-left: 40px;

  background: #e5e7eb;
}


/* =========================================================
   DETAILS
========================================================= */

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 24px;
}

.detail-field {
  position: relative;

  min-height: 116px;

  display: flex;
  align-items: center;

  gap: 16px;

  padding:
    20px
    28px;

  border-radius: 26px;

  background: var(--light-gray);
}

.picker-field {
  overflow: visible;

  z-index: 2;
}

.picker-field--open {
  z-index: 50;
}

.detail-icon {
  width: 28px;
  height: 28px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  color: var(--brand);
}

.detail-icon svg {
  width: 26px;
  height: 26px;

  fill: none;

  stroke: currentColor;
  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.detail-icon svg {
  width: 26px;
  height: 26px;

  fill: none;

  stroke: currentColor;
  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.detail-icon--accent {
  color: var(--brand);
}

.detail-content {
  min-width: 0;

  display: flex;
  flex-direction: column;

  gap: 9px;
}

.picker-content {
  position: relative;

  width: 100%;
}


/* =========================================================
   GENERIC PICKER TRIGGER
========================================================= */

.picker-trigger {
  width: 100%;

  min-width: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 10px;

  padding: 0;

  border: 0;
  outline: none;

  background: transparent;

  color: var(--black);

  font-family: inherit;

  cursor: pointer;

  text-align: left;
}

.picker-value {
  min-width: 0;

  color: var(--black);

  font-size: 20px;
  line-height: 1.2;

  font-weight: 500;

  white-space: nowrap;

  overflow: hidden;
  text-overflow: ellipsis;
}

.picker-value--muted {
  color: var(--muted);
}

.picker-chevron {
  width: 20px;
  height: 20px;

  flex-shrink: 0;

  fill: none;

  stroke: #a5aab2;
  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;

  transition:
    transform 180ms ease,
    stroke 180ms ease;
}

.picker-trigger:hover .picker-chevron {
  stroke: #6b7280;
}

.picker-chevron--open {
  transform: rotate(180deg);

  stroke: var(--brand);
}


/* =========================================================
   CALENDAR
========================================================= */

.calendar-menu,
.time-menu,
.seat-menu {
  position: absolute;

  left: -12px;
  right: -12px;

  top: calc(100% + 16px);

  padding: 16px;

  border: 1px solid #eaebed;
  border-radius: 22px;

  background: #ffffff;

  box-shadow:
    0 12px 28px rgba(17, 22, 39, 0.07),
    0 2px 6px rgba(17, 22, 39, 0.035);

  z-index: 100;
}


/* Header calendrier */

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-bottom: 15px;
}

.calendar-month {
  display: flex;
  align-items: center;

  gap: 6px;
}

.calendar-month-name {
  color: var(--black);

  font-size: 15px;
  font-weight: 700;

  text-transform: capitalize;
}

.calendar-year {
  color: #9ca3af;

  font-size: 14px;
  font-weight: 600;
}

.calendar-nav {
  width: 34px;
  height: 34px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  border: 0;
  border-radius: 10px;

  background: #f3f4f6;

  color: #6b7280;

  cursor: pointer;

  transition:
    background-color 160ms ease,
    color 160ms ease;
}

.calendar-nav:hover:not(:disabled) {
  background: #eceef1;

  color: var(--black);
}

.calendar-nav:disabled {
  opacity: 0.4;

  cursor: not-allowed;
}

.calendar-nav svg {
  width: 17px;
  height: 17px;

  fill: none;

  stroke: currentColor;
  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* Jours */

.calendar-weekdays {
  display: grid;
  grid-template-columns:
    repeat(7, 1fr);

  margin-bottom: 7px;
}

.calendar-weekdays span {
  text-align: center;

  color: #a1a6ae;

  font-size: 10px;
  font-weight: 700;
}

.calendar-grid {
  display: grid;
  grid-template-columns:
    repeat(7, 1fr);

  gap: 4px;
}

.calendar-day {
  aspect-ratio: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  min-width: 0;

  padding: 0;

  border: 0;
  border-radius: 10px;

  background: transparent;

  color: var(--black);

  font-family: inherit;

  font-size: 12px;
  font-weight: 600;

  cursor: pointer;

  transition:
    background-color 150ms ease,
    color 150ms ease,
    transform 150ms ease;
}

.calendar-day:hover:not(:disabled) {
  background: #f3f4f6;

  transform: translateY(-1px);
}

.calendar-day--outside {
  color: #d0d3d7;
}

.calendar-day--disabled {
  color: #d5d8dc;

  cursor: not-allowed;
}

.calendar-day--today {
  color: var(--brand);

  font-weight: 800;
}

.calendar-day--selected {
  background: var(--brand) !important;

  color: #ffffff !important;

  font-weight: 700;
}

.calendar-day--selected:hover {
  background: var(--brand-hover) !important;

  transform: none;
}


/* Footer */

.calendar-footer {
  margin-top: 13px;

  padding-top: 12px;

  border-top: 1px solid #f0f1f2;
}

.calendar-today-button {
  width: 100%;

  min-height: 38px;

  border: 0;
  border-radius: 11px;

  background: #fff5f2;

  color: var(--brand);

  font-family: inherit;

  font-size: 12px;
  font-weight: 700;

  cursor: pointer;

  transition:
    background-color 160ms ease;
}

.calendar-today-button:hover {
  background: #ffebe6;
}


/* =========================================================
   TIME
========================================================= */

.time-input-wrapper {
  position: relative;

  display: flex;
  align-items: center;
}

.time-input {
  width: 100%;

  padding:
    0
    28px
    0
    0;

  border: 0;
  outline: none;

  background: transparent;

  color: var(--black);

  font-family: inherit;

  font-size: 20px;
  line-height: 1.2;

  font-weight: 500;
}

.time-input::placeholder {
  color: #9ca3af;
}

.time-trigger {
  position: absolute;

  right: 0;

  width: 28px;
  height: 28px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  border: 0;

  background: transparent;

  cursor: pointer;
}


/* =========================================================
   TIME MENU
========================================================= */

.time-menu {
  padding: 13px;
}

.time-menu-header {
  padding:
    5px
    8px
    11px;

  color: #9ca3af;

  font-size: 10px;

  font-weight: 700;

  letter-spacing: 0.4px;

  text-transform: uppercase;
}

.time-grid {
  display: grid;
  grid-template-columns:
    repeat(3, 1fr);

  gap: 7px;
}

.time-option {
  min-height: 40px;

  border: 0;
  border-radius: 10px;

  background: #f3f4f6;

  color: var(--black);

  font-family: inherit;

  font-size: 12px;
  font-weight: 600;

  cursor: pointer;

  transition:
    background-color 150ms ease,
    color 150ms ease,
    transform 150ms ease;
}

.time-option:hover {
  background: #eceef1;

  transform: translateY(-1px);
}

.time-option--selected {
  background: #fff1ed;

  color: var(--brand);
}

.time-option--selected:hover {
  background: #ffebe6;

  transform: none;
}

.time-help {
  margin-top: 11px;

  padding:
    10px
    8px
    2px;

  border-top: 1px solid #f0f1f2;

  color: #a0a5ad;

  font-size: 10px;
  line-height: 1.45;
}


/* =========================================================
   SEAT MENU
========================================================= */

.seat-menu {
  padding: 8px;
}

.seat-menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding:
    10px
    12px
    8px;

  color: #a1a6ae;

  font-size: 10px;
  line-height: 1.2;

  font-weight: 700;

  letter-spacing: 0.4px;

  text-transform: uppercase;
}

.seat-option {
  width: 100%;
  min-height: 46px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding:
    6px
    10px;

  border: 0;
  border-radius: 12px;

  background: transparent;

  color: var(--black);

  font-family: inherit;

  cursor: pointer;

  text-align: left;

  transition:
    background-color 160ms ease,
    color 160ms ease,
    transform 160ms ease;
}

.seat-option:hover {
  background: #f7f8f9;

  transform: translateX(1px);
}

.seat-option--selected {
  background: #fff4f1;

  color: var(--brand);
}

.seat-option--selected:hover {
  background: #ffede9;
}

.seat-option-left {
  display: flex;
  align-items: center;

  gap: 11px;
}

.seat-option-number {
  width: 30px;
  height: 30px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 9px;

  background: #f3f4f6;

  color: #374151;

  font-size: 13px;
  font-weight: 700;
}

.seat-option--selected .seat-option-number {
  background: #ffe4dd;

  color: var(--brand);
}

.seat-option-text {
  font-size: 14px;

  font-weight: 600;
}

.seat-check {
  width: 20px;
  height: 20px;

  fill: none;

  stroke: var(--brand);
  stroke-width: 2.4;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.seat-menu-footer {
  margin-top: 5px;

  padding:
    10px
    12px
    8px;

  border-top: 1px solid #f0f1f2;

  color: #a0a5ad;

  font-size: 10px;
  line-height: 1.45;
}


/* =========================================================
   PRICE
========================================================= */

.price-input {
  display: flex;
  align-items: baseline;

  gap: 7px;
}

.price-input input {
  width: 105px;

  border: 0;
  outline: none;

  background: transparent;

  color: var(--black);

  font-family: inherit;

  font-size: 23px;
  font-weight: 500;
}

.price-input input::placeholder {
  color: var(--muted);
}

.price-input input::-webkit-outer-spin-button,
.price-input input::-webkit-inner-spin-button {
  margin: 0;

  -webkit-appearance: none;
}

.price-input input[type='number'] {
  appearance: textfield;
}

.price-input span {
  color: #9ca3af;

  font-size: 21px;
  font-weight: 500;
}


/* =========================================================
   DESCRIPTION
========================================================= */

.description-field {
  position: relative;
}

.description-field textarea {
  width: 100%;
  min-height: 250px;

  resize: vertical;

  padding: 22px;

  border: 2px solid #e4e6ea;
  border-radius: 26px;

  outline: none;

  background: #fafafa;

  color: var(--black);

  font-family: inherit;

  font-size: 18px;
  line-height: 1.5;

  transition:
    border-color 180ms ease,
    background-color 180ms ease,
    box-shadow 180ms ease;
}

.description-field textarea:hover {
  background: #f8f8f9;
}

.description-field textarea:focus {
  background: #ffffff;

  border-color: rgba(255, 77, 45, 0.35);

  box-shadow:
    0 0 0 3px rgba(255, 77, 45, 0.08);
}

.description-field textarea::placeholder {
  color: #a3a7ae;
}

.character-count {
  position: absolute;

  right: 16px;
  bottom: 14px;

  color: #a6abb2;

  font-size: 12px;

  font-weight: 500;
}


/* =========================================================
   PREFERENCES
========================================================= */

.preferences {
  display: flex;
  flex-wrap: wrap;

  gap: 14px;
}

.preference-chip {
  min-height: 52px;

  display: inline-flex;
  align-items: center;

  gap: 11px;

  padding:
    0
    20px;

  border: 1px solid transparent;
  border-radius: var(--radius-full);

  background: #f3f4f6;

  color: var(--black);

  font-family: inherit;

  font-size: 17px;
  line-height: 1;

  font-weight: 700;

  cursor: pointer;

  transition:
    background-color 180ms ease,
    border-color 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.preference-chip:hover {
  background: #eceef1;

  transform: translateY(-1px);
}

.preference-chip:active {
  transform: translateY(0);
}

.preference-chip:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.18);
  outline-offset: 2px;
}

.preference-chip--active {
  border-color: #ffc1b5;

  background: #fff7f4;

  color: var(--brand);
}

.preference-chip--active:hover {
  border-color: #ffab9c;

  background: #fff0ec;
}

.preference-icon {
  width: 20px;
  height: 20px;

  flex: 0 0 auto;

  fill: none;

  stroke: currentColor;
  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   SUBMIT
========================================================= */

.submit-section {
  padding-top: 14px;

  border-top: 1px solid #f0f1f2;
}

.publish-button {
  width: 100%;
  min-height: 88px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  gap: 15px;

  border: 0;
  border-radius: 28px;

  background: var(--brand);

  color: var(--white);

  font-family: inherit;

  font-size: 25px;
  line-height: 1;

  font-weight: 700;

  cursor: pointer;

  /*
   * Shadow volontairement très discrète.
   */
  box-shadow:
    0 6px 16px rgba(
      255,
      77,
      45,
      0.10
    );

  transition:
    background-color 180ms ease,
    transform 180ms ease,
    box-shadow 180ms ease;
}

.publish-button:hover:not(:disabled) {
  background: var(--brand-hover);

  transform: translateY(-1px);

  box-shadow:
    0 8px 18px rgba(
      255,
      77,
      45,
      0.12
    );
}

.publish-button:active:not(:disabled) {
  background: var(--brand-active);

  transform: translateY(0);

  box-shadow:
    0 4px 10px rgba(
      255,
      77,
      45,
      0.08
    );
}

.publish-button:focus-visible {
  outline: 3px solid rgba(
    255,
    77,
    45,
    0.20
  );

  outline-offset: 4px;
}

.publish-button:disabled {
  opacity: 0.55;

  cursor: not-allowed;

  box-shadow: none;

  transform: none;
}

.publish-arrow {
  width: 28px;
  height: 28px;

  fill: none;

  stroke: currentColor;
  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;

  transition:
    transform 180ms ease;
}

.publish-button:hover:not(:disabled)
.publish-arrow {
  transform: translateX(2px);
}


/* =========================================================
   LOADING
========================================================= */

.loading-state {
  display: inline-flex;
  align-items: center;

  gap: 12px;
}

.spinner {
  width: 20px;
  height: 20px;

  border: 2px solid
    rgba(
      255,
      255,
      255,
      0.35
    );

  border-top-color: #ffffff;

  border-radius: 50%;

  animation:
    spin
    0.7s
    linear
    infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


/* =========================================================
   LEGAL
========================================================= */

.legal-text {
  max-width: 560px;

  margin: 25px auto 0;

  color: #b0b4bb;

  font-size: 15px;
  line-height: 1.6;

  text-align: center;
}

.legal-text a {
  color: #7f858e;

  text-decoration: underline;

  text-decoration-thickness: 1px;

  text-underline-offset: 3px;
}

.legal-text a:hover {
  color: var(--black);
}


/* =========================================================
   PICKER ANIMATION
========================================================= */

.picker-menu-enter-active,
.picker-menu-leave-active {
  transition:
    opacity 160ms ease,
    transform 180ms ease;
}

.picker-menu-enter-from,
.picker-menu-leave-to {
  opacity: 0;

  transform:
    translateY(5px)
    scale(0.985);
}


/* =========================================================
   TABLET
========================================================= */
/* =========================================================
   RESPONSIVE — TABLET
========================================================= */

@media (max-width: 700px) {

  .publish-trip-page {
    width: 100%;
    max-width: 100%;

    overflow-x: hidden;
  }

  .page-header {
    width: 100%;
    max-width: 100%;

    padding:
      30px
      24px
      0;

    grid-template-columns: 50px minmax(0, 1fr);

    gap: 18px;
  }

  .page-content {
    width: 100%;
    max-width: 100%;

    padding:
      48px
      24px
      60px;
  }

  .page-header h1 {
    min-width: 0;

    font-size: 30px;

    line-height: 1.15;

    letter-spacing: -0.9px;
  }

  .section-title h2 {
    font-size: 21px;
  }

  .location-field {
    width: 100%;
    min-width: 0;

    min-height: 106px;

    padding:
      17px
      20px;

    gap: 14px;

    border-radius: 22px;
  }

  .location-content {
    min-width: 0;
    flex: 1;
  }

  .location-content label {
    font-size: 11px;
  }

  .location-content input {
    min-width: 0;

    font-size: 21px;

    text-overflow: ellipsis;
  }

  .details-grid {
    width: 100%;

    grid-template-columns:
      minmax(0, 1fr)
      minmax(0, 1fr);

    gap: 12px;
  }

  .detail-field {
    width: 100%;
    min-width: 0;

    min-height: 96px;

    padding:
      15px
      16px;

    gap: 10px;

    border-radius: 21px;
  }

  .detail-icon {
    width: 22px;
    height: 22px;
  }

  .detail-icon svg {
    width: 20px;
    height: 20px;
  }

  .detail-content {
    min-width: 0;
    flex: 1;
  }

  .detail-label,
  .detail-content label {
    font-size: 11px;
  }

  .picker-value,
  .time-input,
  .price-input input,
  .detail-content select {
    font-size: 17px;
  }

  .picker-value {
    max-width: 100%;

    overflow: hidden;
    text-overflow: ellipsis;
  }

  .price-input {
    min-width: 0;

    gap: 5px;
  }

  .price-input input {
    width: 65px;
    min-width: 0;
  }

  .price-input span {
    white-space: nowrap;

    font-size: 14px;
  }

  .description-field textarea {
    width: 100%;
    min-height: 210px;

    font-size: 16px;
  }

  .preferences {
    gap: 10px;
  }

  .preference-chip {
    min-height: 46px;

    padding:
      0
      15px;

    font-size: 14px;
  }

  .publish-button {
    width: 100%;

    min-height: 72px;

    border-radius: 22px;

    font-size: 20px;
  }

  .legal-text {
    font-size: 12px;
  }
}


/* =========================================================
   RESPONSIVE — MOBILE
========================================================= */

@media (max-width: 520px) {

  .publish-trip-page {
    width: 100%;
    min-width: 0;
    max-width: none;

    overflow-x: hidden;
  }

  /* -------------------------------------------------------
     HEADER
  ------------------------------------------------------- */

  .page-header {
    display: flex;
    align-items: center;

    width: 100%;
    max-width: none;

    padding:
      24px
      16px
      0;

    gap: 14px;
  }

  .back-button {
    width: 44px;
    height: 44px;

    flex: 0 0 44px;
  }

  .back-button svg {
    width: 22px;
    height: 22px;
  }

  .page-header h1 {
    min-width: 0;

    font-size: 25px;

    line-height: 1.15;

    letter-spacing: -0.7px;

    white-space: nowrap;
  }


  /* -------------------------------------------------------
     CONTENT
  ------------------------------------------------------- */

  .page-content {
    width: 100%;
    max-width: none;

    padding:
      38px
      16px
      44px;
  }


  /* -------------------------------------------------------
     FORM
  ------------------------------------------------------- */

  .trip-form {
    width: 100%;
    min-width: 0;

    gap: 46px;
  }


  /* -------------------------------------------------------
     TITLES
  ------------------------------------------------------- */

  .section-title {
    width: 100%;

    margin-bottom: 20px;

    gap: 9px;
  }

  .section-accent {
    width: 5px;
    height: 25px;
  }

  .section-title h2 {
    min-width: 0;

    font-size: 18px;

    letter-spacing: 0.45px;
  }


  /* -------------------------------------------------------
     ITINERARY
  ------------------------------------------------------- */

  .route-fields {
    width: 100%;
  }

  .location-field {
    width: 100%;
    max-width: 100%;
    min-width: 0;

    min-height: 74px;

    padding:
      13px
      14px;

    gap: 10px;

    border-radius: 19px;
  }

  .location-icon {
    width: 24px;
    height: 24px;

    flex: 0 0 24px;
  }

  .location-icon svg {
    width: 19px;
    height: 19px;
  }

  .location-content {
    width: 100%;
    min-width: 0;
  }

  .location-content label {
    font-size: 9px;

    white-space: nowrap;
  }

  .location-content input {
    width: 100%;
    min-width: 0;

    padding: 0;

    font-size: 16px;

    line-height: 1.25;

    white-space: nowrap;

    overflow: hidden;
    text-overflow: ellipsis;
  }

  .route-line {
    width: 3px;
    height: 18px;

    margin-left: 25px;
  }


  /* -------------------------------------------------------
     DETAILS
  ------------------------------------------------------- */

  .details-grid {
    width: 100%;
    min-width: 0;

    grid-template-columns:
      minmax(0, 1fr)
      minmax(0, 1fr);

    gap: 10px;
  }

  .detail-field {
    width: 100%;
    min-width: 0;

    min-height: 76px;

    display: flex;
    align-items: center;

    gap: 8px;

    padding:
      12px
      12px;

    border-radius: 18px;
  }

  .detail-icon {
    width: 19px;
    height: 19px;

    flex: 0 0 19px;
  }

  .detail-icon svg {
    width: 18px;
    height: 18px;
  }

  .detail-content {
    width: 100%;
    min-width: 0;
  }

  .detail-label,
  .detail-content label {
    font-size: 9px;

    line-height: 1;
  }


  /* -------------------------------------------------------
     DATE
  ------------------------------------------------------- */

  .picker-trigger {
    width: 100%;
    min-width: 0;
  }

  .picker-value {
    min-width: 0;
    max-width: calc(100% - 18px);

    font-size: 14px;

    line-height: 1.25;

    white-space: nowrap;

    overflow: hidden;
    text-overflow: ellipsis;
  }

  .picker-chevron {
    width: 15px;
    height: 15px;
  }


  /* -------------------------------------------------------
     HEURE
  ------------------------------------------------------- */

  .time-input-wrapper {
    width: 100%;
    min-width: 0;
  }

  .time-input {
    width: 100%;
    min-width: 0;

    padding-right: 20px;

    font-size: 14px;

    line-height: 1.25;
  }

  .time-trigger {
    width: 20px;
    height: 20px;

    right: -2px;
  }


  /* -------------------------------------------------------
     PRIX
  ------------------------------------------------------- */

  .price-input {
    width: 100%;
    min-width: 0;

    gap: 4px;
  }

  .price-input input {
    width: 55px;
    min-width: 0;

    padding: 0;

    font-size: 14px;

    text-overflow: ellipsis;
  }

  .price-input span {
    font-size: 12px;

    white-space: nowrap;
  }


  /* -------------------------------------------------------
     DESCRIPTION
  ------------------------------------------------------- */

  .description-field {
    width: 100%;
  }

  .description-field textarea {
    display: block;

    width: 100%;
    min-width: 0;

    min-height: 170px;

    padding:
      15px;

    border-radius: 18px;

    font-size: 14px;

    line-height: 1.45;
  }

  .character-count {
    right: 12px;
    bottom: 10px;

    font-size: 10px;
  }


  /* -------------------------------------------------------
     PREFERENCES
  ------------------------------------------------------- */

  .preferences {
    width: 100%;

    display: flex;
    flex-wrap: wrap;

    gap: 8px;
  }

  .preference-chip {
    min-height: 40px;

    padding:
      0
      12px;

    gap: 7px;

    font-size: 12px;
  }

  .preference-icon {
    width: 16px;
    height: 16px;
  }


  /* -------------------------------------------------------
     SUBMIT
  ------------------------------------------------------- */

  .submit-section {
    width: 100%;

    padding-top: 10px;
  }

  .publish-button {
    width: 100%;
    min-width: 0;

    min-height: 64px;

    gap: 10px;

    border-radius: 19px;

    font-size: 18px;
  }

  .publish-arrow {
    width: 20px;
    height: 20px;
  }

  .legal-text {
    width: 100%;
    max-width: 100%;

    margin-top: 16px;

    font-size: 10px;

    line-height: 1.55;
  }


  /* =======================================================
     IMPORTANT :
     MENUS VERS LE HAUT
  ======================================================== */

  .calendar-menu,
  .time-menu,
  .seat-menu {
  top: auto;
  bottom: calc(100% + 10px);

    left: 0;
    right: 0;

    width: 100%;
    max-width: 100%;

    padding: 11px;

    border-radius: 17px;

    transform-origin: bottom center;
  }
}


/* =========================================================
   VERY SMALL MOBILE
========================================================= */

@media (max-width: 360px) {

  .page-header {
    padding-left: 14px;
    padding-right: 14px;
  }

  .page-content {
    padding-left: 14px;
    padding-right: 14px;
  }

  .page-header h1 {
    font-size: 23px;
  }

  .details-grid {
    gap: 8px;
  }

  .detail-field {
    padding:
      11px
      10px;
  }

  .detail-icon {
    width: 17px;
    height: 17px;
    flex-basis: 17px;
  }

  .detail-icon svg {
    width: 16px;
    height: 16px;
  }

  .picker-value,
  .time-input {
    font-size: 13px;
  }

  .price-input input {
    width: 48px;

    font-size: 13px;
  }

  .price-input span {
    font-size: 11px;
  }

  .preference-chip {
    padding:
      0
      10px;

    font-size: 11px;
  }

  .publish-button {
    font-size: 17px;
  }
}
</style>