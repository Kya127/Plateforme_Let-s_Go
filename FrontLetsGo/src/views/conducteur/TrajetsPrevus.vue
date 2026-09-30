<template>
  <div class="trips-page">
    <!-- =====================================================
         HEADER
    ====================================================== -->
    <header class="page-header">
      <h1>Trajets prévus</h1>
      <p>Gérez vos trajets proposés</p>
    </header>

    <!-- =====================================================
         TABS
    ====================================================== -->
    <nav class="tabs" aria-label="Filtrer les trajets">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="tab"
        :class="{ 'tab--active': activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <span>{{ tab.label }}</span>
        <span v-if="tab.count > 0" class="tab-count">{{ tab.count }}</span>
      </button>
    </nav>

    <!-- =====================================================
         CONTENT
    ====================================================== -->
    <main class="page-content">
      <!-- Aucun trajet -->
      <section v-if="filteredTrips.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M5 5h14v14H5z" />
            <path d="M8 9h8" />
            <path d="M8 13h5" />
          </svg>
        </div>
        <h2>Aucun trajet</h2>
        <p>Vous n'avez aucun trajet dans cette catégorie.</p>
      </section>

      <!-- Liste des cartes de trajets (Composant Modulaire) -->
      <section v-else class="trips-list" aria-label="Liste des trajets">
        <CarteTrajetPrevu
          v-for="trip in filteredTrips"
          :key="trip.id"
          :trip="trip"
          @view="viewTrip"
        />
      </section>
    </main>

    <!-- =====================================================
         ADD TRIP
    ====================================================== -->
    <button
      type="button"
      class="add-trip-button"
      aria-label="Publier un nouveau trajet"
      @click="createTrip"
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 5v14" />
        <path d="M5 12h14" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import CarteTrajetPrevu from '@/components/conducteur/CarteTrajetPrevu.vue'

/* =========================================================
   ROUTER
========================================================= */
const router = useRouter()

/* =========================================================
   TABS
========================================================= */
const activeTab = ref('upcoming')

const tabs = [
  { id: 'upcoming', label: 'À venir' },
  { id: 'completed', label: 'Terminés' },
  { id: 'cancelled', label: 'Annulés' },
]

/* =========================================================
   DATA
   Exemple temporaire DRF / Django.
========================================================= */
const trips = ref([
  {
    id: 1,
    status: 'upcoming',
    departureLabel: 'DEMAIN',
    departureTime: '08:30',
    departure: 'Keur Massar',
    arrivalLabel: 'ARRIVÉE',
    arrivalTime: '11:45',
    destination: 'Ouakam',
    price: 1500,
    seatsTotal: 3,
    seatsTaken: 2,
    passengers: [
      {
        id: 101,
        firstName: 'Awa',
        lastName: 'Ndiaye',
        profilePhoto: '/images/passagers/awa.jpg',
      },
      {
        id: 102,
        firstName: 'Mamadou',
        lastName: 'Diop',
        profilePhoto: null,
      },
    ],
  },
  {
    id: 2,
    status: 'upcoming',
    departureLabel: '24 JANV.',
    departureTime: '14:00',
    departure: 'Parcelles Assainies',
    arrivalLabel: 'ARRIVÉE',
    arrivalTime: '15:15',
    destination: 'Plateau',
    price: 2000,
    seatsTotal: 4,
    seatsTaken: 1,
    passengers: [
      {
        id: 103,
        firstName: 'Fatou',
        lastName: 'Sow',
        profilePhoto: null,
      },
    ],
  },
  {
    id: 3,
    status: 'completed',
    departureLabel: '20 JANV.',
    departureTime: '09:00',
    departure: 'Guédiawaye',
    arrivalLabel: 'ARRIVÉE',
    arrivalTime: '10:30',
    destination: 'Almadies',
    price: 2500,
    seatsTotal: 3,
    seatsTaken: 3,
    passengers: [
      { id: 104, firstName: 'Ibrahima', lastName: 'Diallo', profilePhoto: null },
      { id: 105, firstName: 'Aminata', lastName: 'Ba', profilePhoto: null },
      { id: 106, firstName: 'Cheikh', lastName: 'Fall', profilePhoto: null },
    ],
  },
  {
    id: 4,
    status: 'cancelled',
    departureLabel: '15 JANV.',
    departureTime: '07:30',
    departure: 'Rufisque',
    arrivalLabel: 'ARRIVÉE',
    arrivalTime: '09:00',
    destination: 'Colobane',
    price: 1500,
    seatsTotal: 3,
    seatsTaken: 0,
    passengers: [],
  },
])

/* =========================================================
   COMPUTED
========================================================= */
const filteredTrips = computed(() => {
  return trips.value.filter((trip) => trip.status === activeTab.value)
})

/* =========================================================
   ACTIONS
========================================================= */
const viewTrip = (trip) => {
  router.push({
    name: 'trip-details',
    params: { id: trip.id },
  })
}

const createTrip = () => {
  router.push('/conducteur/publier-trajet')
}
</script>

<style scoped>
/* =========================================================
   DESIGN TOKENS & PAGE CONTAINER
========================================================= */
.trips-page {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;
  --black: #111627;
  --dark-gray: #374151;
  --text: #111627;
  --text-secondary: #8d939d;
  --text-muted: #aeb3bb;
  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;
  --white: #ffffff;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;
  overflow-x: hidden;
  background: #f9fafb;
  color: var(--text);
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  box-sizing: border-box;
}

.trips-page *,
.trips-page *::before,
.trips-page *::after {
  box-sizing: border-box;
}

/* =========================================================
   HEADER
========================================================= */
.page-header {
  width: min(calc(100% - 48px), 654px);
  margin: 0 auto;
  padding-top: 54px;
}

.page-header h1 {
  margin: 0;
  color: var(--black);
  font-size: 43px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -1.5px;
}

.page-header p {
  margin: 11px 0 0;
  color: #8b919b;
  font-size: 25px;
  line-height: 1.35;
  font-weight: 500;
  letter-spacing: -0.5px;
}

/* =========================================================
   TABS
========================================================= */
.tabs {
  width: 100%;
  display: flex;
  align-items: flex-end;
  margin-top: 62px;
  padding: 0 max(24px, calc((100vw - 654px) / 2));
  border-bottom: 1px solid #e2e4e7;
}

.tab {
  position: relative;
  flex: 1;
  min-width: 0;
  height: 73px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0 12px;
  border: 0;
  background: transparent;
  color: #acb1b9;
  font-family: inherit;
  font-size: 25px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
  transition: color 180ms ease, background-color 180ms ease;
}

.tab:hover {
  color: #7f858e;
}

.tab--active {
  color: var(--black);
}

.tab--active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -1px;
  width: 48px;
  height: 6px;
  transform: translateX(-50%);
  border-radius: 999px;
  background: var(--brand);
}

.tab-count {
  font-size: 13px;
  font-weight: 700;
}

/* =========================================================
   CONTENT
========================================================= */
.page-content {
  width: min(calc(100% - 48px), 654px);
  margin: 0 auto;
  padding: 62px 0 170px;
}

.trips-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* =========================================================
   ADD BUTTON
========================================================= */
.add-trip-button {
  position: fixed;
  z-index: 20;
  left: 50%;
  bottom: 42px;
  width: 112px;
  height: 112px;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0;
  border-radius: 30px;
  background: var(--brand);
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 7px 16px rgba(255, 77, 45, 0.06);
  transition: background-color 180ms ease, transform 180ms ease, box-shadow 180ms ease;
}

.add-trip-button:hover {
  background: var(--brand-hover);
  transform: translateX(-50%) translateY(-1px);
  box-shadow: 0 9px 18px rgba(255, 77, 45, 0.07);
}

.add-trip-button:active {
  background: var(--brand-active);
  transform: translateX(-50%) translateY(0);
  box-shadow: 0 4px 10px rgba(255, 77, 45, 0.04);
}

.add-trip-button:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.20);
  outline-offset: 4px;
}

.add-trip-button svg {
  width: 42px;
  height: 42px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  transition: transform 180ms ease;
}

.add-trip-button:hover svg {
  transform: rotate(90deg);
}

/* =========================================================
   EMPTY STATE
========================================================= */
.empty-state {
  min-height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  border: 1px solid #e5e7eb;
  border-radius: 30px;
  background: #ffffff;
  text-align: center;
}

.empty-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: #f3f4f6;
  color: #9ca3af;
}

.empty-icon svg {
  width: 27px;
  height: 27px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.empty-state h2 {
  margin: 18px 0 0;
  font-size: 22px;
  font-weight: 700;
}

.empty-state p {
  max-width: 300px;
  margin: 8px 0 0;
  color: #9ca3af;
  font-size: 14px;
  line-height: 1.5;
}

/* =========================================================
   TABLET RESPONSIVE (max-width: 700px)
========================================================= */
@media (max-width: 700px) {
  .page-header {
    width: calc(100% - 40px);
    padding-top: 40px;
  }

  .page-header h1 {
    font-size: 36px;
  }

  .page-header p {
    font-size: 21px;
  }

  .tabs {
    padding-left: 20px;
    padding-right: 20px;
    margin-top: 45px;
  }

  .tab {
    height: 62px;
    font-size: 20px;
  }

  .page-content {
    width: calc(100% - 40px);
    padding-top: 45px;
  }
}

/* =========================================================
   MOBILE RESPONSIVE (max-width: 520px)
========================================================= */
@media (max-width: 520px) {
  .trips-page {
    width: 100%;
    min-width: 0;
    overflow-x: hidden;
  }

  .page-header {
    width: 100%;
    padding: 34px 20px 0;
  }

  .page-header h1 {
    font-size: 32px;
    letter-spacing: -1px;
  }

  .page-header p {
    margin-top: 8px;
    font-size: 19px;
    line-height: 1.3;
  }

  .tabs {
    width: 100%;
    margin-top: 39px;
    padding: 0 10px;
    overflow: hidden;
  }

  .tab {
    flex: 1;
    height: 57px;
    padding: 0 6px;
    font-size: 17px;
    white-space: nowrap;
  }

  .tab--active::after {
    width: 42px;
    height: 5px;
  }

  .page-content {
    width: 100%;
    padding: 38px 16px 145px;
  }

  .trips-list {
    width: 100%;
    gap: 16px;
  }

  .add-trip-button {
    width: 76px;
    height: 76px;
    bottom: 28px;
    border-radius: 22px;
    box-shadow: 0 5px 12px rgba(255, 77, 45, 0.06);
  }

  .add-trip-button:hover {
    box-shadow: 0 7px 14px rgba(255, 77, 45, 0.07);
  }

  .add-trip-button svg {
    width: 30px;
    height: 30px;
  }
}

/* =========================================================
   SMALL MOBILE RESPONSIVE (max-width: 360px)
========================================================= */
@media (max-width: 360px) {
  .page-header {
    padding-left: 16px;
    padding-right: 16px;
  }

  .page-content {
    padding-left: 12px;
    padding-right: 12px;
  }

  .page-header h1 {
    font-size: 29px;
  }

  .page-header p {
    font-size: 17px;
  }

  .tab {
    font-size: 15px;
  }
}
</style>