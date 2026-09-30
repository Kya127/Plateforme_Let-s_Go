<template>
  <div class="trip-detail-page">
    <!-- 1. HEADER STANDARDISÉ (Composant Modulaire) -->
    <EnTetePage
      titre="Trajet prévu"
      @retour="goBack"
    >
      <template #badge>
        <BadgeStatut :statut="trip.statut" />
      </template>
    </EnTetePage>

    <!-- 2. CONTENU PRINCIPAL -->
    <main class="page-content">
      <!-- État de chargement initial -->
      <div v-if="chargement" class="loading-state-container">
        <span class="spinner-circle"></span>
        <p>Chargement des détails du trajet...</p>
      </div>

      <!-- Contenu principal une fois chargé -->
      <div v-else class="trip-content-layout">
        <!-- Colonne Gauche (Desktop) : Résumé de route & Passagers -->
        <div class="trip-colonne-principale">
          <!-- Résumé de l'Itinéraire (Composant Modulaire) -->
          <TripSummaryRoute
            :departure="trip.departure"
            :departure-time="trip.departureTime"
            :destination="trip.destination"
            :date="trip.date"
            :price-per-seat="trip.price"
          />

          <!-- Préférences & Description du conducteur -->
          <CartePreferencesDescription
            :preferences="trip.preferences"
            :description="trip.description"
            mode="conducteur"
            :editable="trip.statut === 'PLANIFIE'"
            @modifier="modifierTrajet"
          />

          <!-- Gestion des Réservations (Composant Modulaire) -->
          <PassengerList
            :passengers="trip.passengers"
            :reserved-seats="reservedSeats"
            :total-seats="trip.totalSeats"
          />
        </div>

        <!-- Colonne Droite (Desktop) : Commandes Trajet, Commission & Actions -->
        <div class="trip-colonne-laterale">
          <!-- Contrôles conducteur (Composant Modulaire) -->
          <TripActionsCard
            :statut="trip.statut"
            :en-action="enAction"
            :is-commission-paid="isCommissionPaid"
            :commission-amount="commissionAmount"
            @basculer-statut="basculerStatutTrajet"
            @payer-commission="allerAuPaiementCommission"
            @modifier="modifierTrajet"
            @annuler="openCancelModal"
          />
        </div>
      </div>
    </main>

    <!-- 3. MODALE CONFIRMATION ANNULATION (Composant Modulaire) -->
    <ModalConfirmation
      :visible="showCancelModal"
      type="danger"
      titre="Annuler ce trajet ?"
      message="Êtes-vous sûr de vouloir annuler ce trajet ? Les passagers ayant réservé seront automatiquement notifiés. Cette action est irréversible."
      texte-confirmer="Confirmer l'annulation"
      texte-annuler="Retour"
      :en-chargement="isCancelling"
      @confirmer="confirmCancel"
      @annuler="closeCancelModal"
      @fermer="closeCancelModal"
    />



    <!-- 5. MODALE FEEDBACK : PAIEMENT RÉUSSI -->
    <ModalConfirmation
      :visible="showPaymentSuccessModal"
      type="succes"
      titre="Paiement effectué"
      message="Votre paiement a été validé avec succès."
      texte-confirmer="Fermer"
      :afficher-annuler="false"
      @confirmer="showPaymentSuccessModal = false"
      @fermer="showPaymentSuccessModal = false"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { serviceTrajets, serviceCommissions } from '@/services/api'
import EnTetePage from '@/components/layout/EnTetePage.vue'
import BadgeStatut from '@/components/common/BadgeStatut.vue'
import ModalConfirmation from '@/components/common/ModalConfirmation.vue'
import TripSummaryRoute from '@/components/conducteur/TripSummaryRoute.vue'
import PassengerList from '@/components/conducteur/PassengerList.vue'
import TripActionsCard from '@/components/conducteur/TripActionsCard.vue'
import CartePreferencesDescription from '@/components/common/CartePreferencesDescription.vue'

const route = useRoute()
const router = useRouter()

/* =========================================================
   ÉTATS DE LA VUE & CYCLE DE VIE
========================================================= */
const chargement = ref(true)
const enAction = ref(false)
const showCancelModal = ref(false)
const isCancelling = ref(false)

// Modales de feedback
const showPaymentSuccessModal = ref(false)
const isCommissionPaid = ref(false)

/* =========================================================
   DONNÉES DU TRAJET
========================================================= */
const trip = reactive({
  id: null,
  departure: 'Keur Massar',
  destination: 'Ouakam',
  departureTime: '08:30',
  date: '',
  price: 1500,
  totalSeats: 4,
  statut: 'PLANIFIE',
  description: '',
  preferences: [],
  passengers: []
})

const tripId = computed(() => route.params.id || route.query.id)

async function chargerTrajet() {
  if (!tripId.value) {
    chargement.value = false
    return
  }

  chargement.value = true
  try {
    const data = await serviceTrajets.getDetail(tripId.value)
    if (data) {
      trip.id = data.id
      trip.departure = data.lieu_depart || trip.departure
      trip.destination = data.destination || trip.destination
      trip.date = data.date || ''
      trip.departureTime = data.heure_depart ? data.heure_depart.substring(0, 5) : '08:30'
      trip.price = Number(data.prix_par_place || 1500)
      trip.statut = data.statut || 'PLANIFIE'
      trip.description = data.description || ''
      trip.preferences = Array.isArray(data.preferences) ? data.preferences : []
      trip.passengers = data.passagers || data.reservations || []
      const placesDispo = Number(data.places_disponibles || 0)
      trip.totalSeats = placesDispo + (trip.passengers.length || 0)
    }

    // Vérifier l'état de la commission pour ce trajet
    try {
      const comm = await serviceCommissions.getCommissionTrajet(tripId.value)
      if (comm && comm.statut === 'payee') {
        isCommissionPaid.value = true
        trip.statut = 'TERMINE'
      }
    } catch (e) {
      // Ignorer si la commission n'est pas encore créée
    }
  } catch (err) {
    console.error('Erreur chargement détail trajet:', err)
  } finally {
    chargement.value = false
  }
}

onMounted(async () => {
  await chargerTrajet()
  document.addEventListener('keydown', handleEscape)

  // Gestion du retour direct après paiement PayTech
  if (route.query.status === 'success' || route.query.ref || route.query.commission_paid) {
    isCommissionPaid.value = true
    trip.statut = 'TERMINE'
    showPaymentSuccessModal.value = true

    // Terminer le trajet en base de données si nécessaire
    try {
      if (tripId.value) {
        await serviceTrajets.terminer(tripId.value)
      }
    } catch (e) {
      // Déjà terminé
    }

    // Valider la commission en base de données
    try {
      const commId = route.query.commission_id || 1
      await serviceCommissions.validerPaiement(commId, {
        reference: route.query.ref || `COMM-${tripId.value || 1}-PAYTECH`
      })
    } catch (e) {
      console.warn('Validation commission:', e)
    }
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscape)
})

watch(tripId, () => {
  chargerTrajet()
})

/* =========================================================
   RÉSERVATIONS CALCULÉES
========================================================= */
const reservedSeats = computed(() => {
  if (!trip.passengers || trip.passengers.length === 0) return 0
  return trip.passengers.reduce((total, p) => total + Number(p.seatsReserved || 1), 0)
})

const nombrePassagers = computed(() => {
  return reservedSeats.value > 0 ? reservedSeats.value : 1
})

const totalRevenue = computed(() => {
  return nombrePassagers.value * trip.price
})

const commissionAmount = computed(() => {
  return Math.round(totalRevenue.value * 0.1) // 10%
})

const netRevenue = computed(() => {
  return totalRevenue.value - commissionAmount.value
})

/* =========================================================
   BASCULEMENT STATUT DU TRAJET
========================================================= */
async function basculerStatutTrajet() {
  if (enAction.value || !trip.id) return

  if (trip.statut === 'PLANIFIE') {
    await demarrerTrajet()
  } else if (trip.statut === 'EN_COURS') {
    await terminerTrajet()
  }
}

async function demarrerTrajet() {
  if (enAction.value || !trip.id) return
  enAction.value = true
  try {
    const res = await serviceTrajets.demarrer(trip.id)
    trip.statut = res.statut || 'EN_COURS'
  } catch (err) {
    console.error('Erreur au démarrage:', err)
    alert(err.response?.data?.error || 'Impossible de démarrer le trajet.')
  } finally {
    enAction.value = false
  }
}

async function terminerTrajet() {
  if (enAction.value || !trip.id) return
  enAction.value = true
  try {
    const res = await serviceTrajets.terminer(trip.id)
    trip.statut = res.statut || 'TERMINE'
    router.push({
      path: '/paiement',
      query: { id: String(trip.id) }
    })
  } catch (err) {
    console.error('Erreur terminaison:', err)
    alert(err.response?.data?.error || 'Impossible de terminer le trajet.')
  } finally {
    enAction.value = false
  }
}

function allerAuPaiementCommission() {
  router.push({
    path: '/paiement',
    query: { id: String(trip.id) }
  })
}

function modifierTrajet() {
  router.push({
    path: '/publier-trajet',
    query: { edit: String(trip.id) }
  })
}

function retourAuTableauDeBord() {
  showPaymentSuccessModal.value = false
  router.replace('/conducteur/tableau-de-bord')
}

/* =========================================================
   ANNULATION
========================================================= */
const openCancelModal = () => {
  showCancelModal.value = true
}

const closeCancelModal = () => {
  if (!isCancelling.value) {
    showCancelModal.value = false
  }
}

const confirmCancel = async () => {
  if (isCancelling.value || !trip.id) return
  isCancelling.value = true
  try {
    const res = await serviceTrajets.annuler(trip.id)
    trip.statut = res.statut || 'ANNULE'
    showCancelModal.value = false
  } catch (err) {
    console.error('Erreur annulation :', err)
    alert(err.response?.data?.error || 'Impossible d\'annuler ce trajet.')
  } finally {
    isCancelling.value = false
  }
}

/* =========================================================
   HELPERS & FORMATAGE
========================================================= */
const formatNombre = (val) => {
  if (!val && val !== 0) return '0'
  return new Intl.NumberFormat('fr-FR').format(val)
}

const goBack = () => {
  router.replace('/conducteur/tableau-de-bord')
}

const handleEscape = (event) => {
  if (event.key === 'Escape') {
    if (showCancelModal.value && !isCancelling.value) closeCancelModal()
  }
}
</script>

<style scoped>
.trip-detail-page {
  width: 100%;
  min-height: 100vh;
  background-color: #F8FAFC;
  padding: 24px 20px 60px;
  box-sizing: border-box;
}

.page-content {
  max-width: 1100px;
  margin: 0 auto;
}

.loading-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #6B7280;
}

.spinner-circle {
  width: 38px;
  height: 38px;
  border: 3px solid #E5E7EB;
  border-top-color: #FF4D2D;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin-bottom: 16px;
}

.trip-content-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.trip-colonne-principale {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.trip-colonne-laterale {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

@media (min-width: 900px) {
  .trip-content-layout {
    display: grid;
    grid-template-columns: 1.25fr 1fr;
    gap: 32px;
    align-items: start;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>