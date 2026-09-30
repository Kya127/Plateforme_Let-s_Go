<template>
  <div class="trip-page">
    <div class="trip-container">

      <!-- =====================================================
           CARTE / FOND DE MAP & BOUTON RETOUR
      ====================================================== -->
      <section class="map-section">
        <!-- SVG Carte stylisée d'arrière-plan (légère, ultra-rapide, responsive) -->
        <svg class="map-vector" viewBox="0 0 400 320" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="mapBg" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#EBE7DF" />
              <stop offset="60%" stop-color="#E5E1D8" />
              <stop offset="100%" stop-color="#D7E7DC" />
            </linearGradient>
            <linearGradient id="hillGreen" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#D0E9DA" />
              <stop offset="100%" stop-color="#B8DFC8" />
            </linearGradient>
          </defs>

          <!-- Fond de carte -->
          <rect width="400" height="320" fill="url(#mapBg)" />

          <!-- Routes douces stylisées -->
          <path d="M-20,90 Q90,70 190,130 T420,110" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.65" />
          <path d="M-10,180 Q120,160 210,210 T430,170" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.5" />
          <path d="M160,-20 Q170,120 180,190 T240,340" fill="none" stroke="#F5F3ED" stroke-width="5" opacity="0.7" />
          <path d="M310,-10 Q280,100 290,200 T360,330" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.4" />

          <!-- Collines / Zones vertes d'eau comme sur la maquette -->
          <path d="M-20,240 Q100,210 200,245 T420,200 L420,330 L-20,330 Z" fill="url(#hillGreen)" opacity="0.85" />
          <path d="M-10,270 Q140,240 260,270 T420,235 L420,330 L-10,330 Z" fill="#A7D7BC" opacity="0.7" />
        </svg>

        <!-- Bouton retour flottant -->
        <button
          type="button"
          class="floating-back-btn"
          aria-label="Retour"
          @click="goBack"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
      </section>

      <!-- =====================================================
           CARTE CONTENU PRINCIPALE (BLANCHE ARRONDIE)
      ====================================================== -->
      <main class="trip-sheet">
        <div class="trip-sheet-body">

          <!-- Colonne Principale (Gauche sur Desktop) -->
          <div class="trip-main-column">
            <!-- Ligne Trajet & Prix -->
            <div class="header-info-group">
              <!-- Badge Date / Heure -->
              <div class="time-badge">
                {{ trip.dateLabel }}, {{ trip.time }}
              </div>

              <div class="route-price-row">
                <!-- Trajet : Départ → Arrivée -->
                <div class="route-title">
                  <span class="route-point">{{ trip.departure }}</span>
                  <span class="route-arrow" aria-hidden="true">→</span>
                  <span class="route-point">{{ trip.destination }}</span>
                </div>

                <!-- Prix (visible uniquement sur mobile, sur desktop il est dans le panneau sticky) -->
                <div class="price-container mobile-price-container">
                  <div class="price-amount">{{ formatPrice(trip.totalPrice) }}</div>
                  <div class="price-label">FCFA TOTAL</div>
                </div>
              </div>
            </div>

            <!-- Points clés (Places & Durée) -->
            <div class="highlight-cards-grid">
              <!-- Places disponibles -->
              <div class="highlight-card">
                <div class="highlight-icon seat-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="20" height="20" fill="#FF4820">
                    <path d="M4 18v3h3v-3h10v3h3v-3c1.1 0 2-.9 2-2v-5c0-1.1-.9-2-2-2h-1V7c0-2.21-1.79-4-4-4h-4c-2.21 0-4 1.79-4 4v2H6c-1.1 0-2 .9-2 2v5c0 1.1.9 2 2 2zm4-11c0-1.1.9-2 2-2h4c1.1 0 2 .9 2 2v2H8V7zm-2 4h12v5H6v-5z"/>
                  </svg>
                </div>
                <div class="highlight-content">
                  <span class="highlight-value">{{ trip.availableSeats }} places</span>
                  <span class="highlight-sub">DISPONIBLES</span>
                </div>
              </div>

              <!-- Durée estimée -->
              <div class="highlight-card">
                <div class="highlight-icon clock-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="20" height="20" fill="#FF4820">
                    <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm4.2 14.2L11 13V7h1.5v5.2l4.5 2.7-.8 1.3z"/>
                  </svg>
                </div>
                <div class="highlight-content">
                  <span class="highlight-value">{{ trip.duration }}</span>
                  <span class="highlight-sub">ESTIMATION</span>
                </div>
              </div>
            </div>

            <!-- Section Conducteur -->
            <section class="info-section">
              <h2 class="section-title">CONDUCTEUR</h2>

              <CarteConducteurProfil
                :id="trip.driver.id"
                :nom="trip.driver.name"
                :photo="trip.driver.photo"
                :note="trip.driver.rating"
                :telephone="trip.driver.phone"
                @voir-profil="voirProfilConducteur"
                @appeler="callDriver"
                @ecrire="messageDriver"
              />
            </section>

            <!-- Section Véhicule -->
            <section class="info-section">
              <div class="section-titre-flex">
                <h2 class="section-title">VÉHICULE</h2>
                <span v-if="trip.vehicle.isAirConditioned" class="badge-clim">
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                  </svg>
                  Climatisé
                </span>
              </div>

              <div class="vehicle-card-enhanced">
                <!-- Haut de la carte : Icône + Marque & Modèle + Badge plaque -->
                <div class="vehicle-header-row">
                  <div class="vehicle-icon-box" aria-hidden="true">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="#FF4D2D">
                      <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.85 7h10.29l1.08 3.11H5.77L6.85 7zM7.5 15c-.83 0-1.5-.67-1.5-1.5S6.67 12 7.5 12s1.5.67 1.5 1.5S8.33 15 7.5 15zm9 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
                    </svg>
                  </div>

                  <div class="vehicle-title-col">
                    <h3 class="vehicle-brand-model">{{ trip.vehicle.brand }} {{ trip.vehicle.model }}</h3>
                    <span class="plate-pill">
                      <span class="sn-flag" aria-hidden="true">🇸🇳</span>
                      <strong>{{ trip.vehicle.plate }}</strong>
                    </span>
                  </div>
                </div>

                <!-- Grille des caractéristiques clés : Modèle, Couleur, Plaque -->
                <div class="vehicle-attributes-grid">
                  <div class="attribute-box">
                    <span class="attr-label">MODÈLE</span>
                    <span class="attr-val">{{ trip.vehicle.model || 'Standard' }}</span>
                  </div>

                  <div class="attribute-box">
                    <span class="attr-label">COULEUR</span>
                    <span class="attr-val color-val">
                      <span class="color-dot" :style="{ backgroundColor: getCouleurPastille(trip.vehicle.color) }"></span>
                      {{ trip.vehicle.color || 'Gris métallisé' }}
                    </span>
                  </div>

                  <div class="attribute-box">
                    <span class="attr-label">PLAQUE</span>
                    <span class="attr-val plate-val">{{ trip.vehicle.plate || 'DK-LET-GO' }}</span>
                  </div>
                </div>
              </div>
            </section>

            <!-- Section Préférences & Précisions du conducteur -->
            <section class="info-section">
              <CartePreferencesDescription
                :preferences="trip.preferences"
                :description="trip.description"
                mode="passager"
              />
            </section>
          </div>

          <!-- Colonne Latérale : Carte Sticky de Réservation & Garanties (Composant Modulaire) -->
          <!-- <BarreActionReservation
            :total-price="trip.totalPrice"
            :available-seats="trip.availableSeats"
            :est-mon-trajet="estMonTrajet"
            :deja-reserve="dejaReserve"
            :nombre-places-deja-reservees="maReservation?.nombre_de_places || 1"
            :is-booking="isBooking"
            @reserver="reserveTrip"
            @gerer-espace-conducteur="router.push({ name: 'vue-trajet-prevu', params: { id: trip.id } })"
            @voir-reservation="voirMaReservation"
          /> -->

        </div>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { serviceTrajets } from '@/services/api'
import { useAuthentificationStore } from '@/stores/authentification'
import CarteConducteurProfil from '@/components/passager/CarteConducteurProfil.vue'
import BarreActionReservation from '@/components/passager/BarreActionReservation.vue'
import CartePreferencesDescription from '@/components/common/CartePreferencesDescription.vue'

const router = useRouter()
const route = useRoute()
const storeAuth = useAuthentificationStore()

const isBooking = ref(false)

const estMonTrajet = computed(() => {
  return storeAuth.estConnecte && Number(storeAuth.utilisateur?.id) === Number(trip.value.driver?.id)
})

const trip = ref({
  id: route.params.id || 1,
  departure: 'Chargement...',
  destination: '',
  dateLabel: "AUJOURD'HUI",
  time: '08:00',
  totalPrice: 0,
  availableSeats: 0,
  duration: '1h 15m',
  driver: {
    name: 'Conducteur Let\'s Go',
    rating: 4.9,
    photo: '',
    phone: '+221 77 000 00 00'
  },
  vehicle: {
    brand: 'Véhicule',
    model: 'Confort',
    color: 'Standard',
    plate: 'DK-LET-GO'
  },
  description: '',
  preferences: [],
  est_deja_reserve: false,
  ma_reservation: null,
  passagers: []
})

const dejaReserve = computed(() => {
  if (!storeAuth.estConnecte) return false
  if (trip.value.est_deja_reserve) return true
  const userId = Number(storeAuth.utilisateur?.id)
  if (userId && Array.isArray(trip.value.passagers)) {
    return trip.value.passagers.some(p => Number(p.passengerId) === userId)
  }
  return false
})

const maReservation = computed(() => {
  if (trip.value.ma_reservation) return trip.value.ma_reservation
  const userId = Number(storeAuth.utilisateur?.id)
  if (userId && Array.isArray(trip.value.passagers)) {
    const found = trip.value.passagers.find(p => Number(p.passengerId) === userId)
    if (found) {
      return {
        id: found.id,
        nombre_de_places: found.seatsReserved || 1,
        statut: 'CONFIRMEE'
      }
    }
  }
  return null
})

const formaterDateLabel = (dateStr) => {
  if (!dateStr) return "AUJOURD'HUI"
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  const today = new Date().toISOString().split('T')[0]
  if (dateStr === today) return "AUJOURD'HUI"
  return d.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' }).toUpperCase()
}

onMounted(async () => {
  const tripId = route.params.id
  if (tripId) {
    try {
      const data = await serviceTrajets.getDetail(tripId)
      if (data) {
        trip.value = {
          id: data.id,
          departure: data.lieu_depart,
          destination: data.destination,
          dateLabel: formaterDateLabel(data.date),
          time: data.heure_depart ? data.heure_depart.substring(0, 5) : '08:00',
          totalPrice: Number(data.prix_par_place) || 0,
          availableSeats: Number(data.places_disponibles) || 0,
          duration: '1h 15m',
          driver: {
            id: data.conducteur,
            name: data.conducteur_nom || `${data.conducteur_prenom || ''} Conducteur`.trim(),
            rating: Number(data.conducteur_note) || 4.9,
            photo: data.conducteur_photo || '',
            phone: data.conducteur_telephone || '+221 77 000 00 00'
          },
          vehicle: {
            brand: 'Véhicule',
            model: 'Confort',
            color: 'Blanc',
            plate: 'DK-LET-GO',
            isAirConditioned: true
          }
        }

        const vInfo = data.voiture_info || data.voiture_details || {}
        let vBrand = 'Véhicule'
        let vModel = 'Confort'
        let vColor = 'Gris argenté'
        let vPlate = 'DK-LET-GO'
        let vClim = true

        if (typeof vInfo === 'object') {
          vBrand = vInfo.brand || vInfo.marque || 'Véhicule'
          vModel = vInfo.model || vInfo.modele || 'Confort'
          vColor = vInfo.color || vInfo.couleur || 'Gris argenté'
          vPlate = vInfo.plate || vInfo.plaque || 'DK-LET-GO'
          vClim = vInfo.climatisee ?? vInfo.isAirConditioned ?? true
        } else if (typeof vInfo === 'string' && vInfo.trim()) {
          const matchPlate = vInfo.match(/\(([^)]+)\)/)
          if (matchPlate) vPlate = matchPlate[1]
          vModel = vInfo.replace(/\([^)]+\)/, '').trim()
        }

        trip.value.est_deja_reserve = Boolean(data.est_deja_reserve)
        trip.value.ma_reservation = data.ma_reservation || null
        trip.value.passagers = data.passagers || []
        trip.value.description = data.description || ''
        trip.value.preferences = Array.isArray(data.preferences) ? data.preferences : []

        trip.value.vehicle = {
          brand: vBrand,
          model: vModel,
          color: vColor,
          plate: vPlate,
          isAirConditioned: vClim
        }
      }
    } catch (err) {
      console.error('Erreur chargement détail trajet BDD:', err)
    }
  }
})

const getCouleurPastille = (nomCouleur) => {
  if (!nomCouleur) return '#94A3B8'
  const c = nomCouleur.toLowerCase().trim()
  if (c.includes('blanc')) return '#F8FAFC'
  if (c.includes('noir')) return '#0F172A'
  if (c.includes('gris') || c.includes('argent')) return '#94A3B8'
  if (c.includes('bleu')) return '#2563EB'
  if (c.includes('rouge')) return '#DC2626'
  if (c.includes('vert')) return '#16A34A'
  if (c.includes('jaune') || c.includes('or')) return '#EAB308'
  if (c.includes('marron')) return '#78350F'
  return '#64748B'
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-FR').format(price)
}

const handleDriverImageError = (e) => {
  e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(trip.value.driver.name)}&background=1E293B&color=fff&size=120`
}

const goBack = () => {
  // Navigation de retour propre vers l'accueil (ou recherche) sans jamais boucler vers le profil conducteur
  if (route.query.from === 'recherche') {
    router.push({ name: 'recherche-resultats' })
  } else {
    router.push('/accueil')
  }
}

const voirProfilConducteur = () => {
  const driverId = trip.value.driver?.id || 2
  router.push({
    name: 'profil-conducteur',
    params: { id: driverId },
    query: { trajet_id: String(trip.value.id) }
  })
}

const callDriver = () => {
  if (trip.value.driver.phone) {
    window.location.href = `tel:${trip.value.driver.phone}`
  } else {
    alert(`Numéro de téléphone non disponible pour ${trip.value.driver.name}`)
  }
}

const messageDriver = () => {
  alert(`Messagerie avec ${trip.value.driver.name} disponible dès confirmation de votre place.`)
}

const reserveTrip = () => {
  if (trip.value.availableSeats <= 0 || isBooking.value) return
  isBooking.value = true

  router.push({
    name: 'resume-reservation',
    params: { id: trip.value.id }
  })
}

const voirMaReservation = () => {
  const resId = maReservation.value?.id || trip.value.id
  router.push({
    name: 'reservation-confirmee',
    query: {
      ref: `LG-${resId}`,
      depart: trip.value.departure,
      arrivee: trip.value.destination,
      heure: trip.value.time,
      places: `${maReservation.value?.nombre_de_places || 1} Place${(maReservation.value?.nombre_de_places || 1) > 1 ? 's' : ''}`,
      reservationId: String(resId),
      trajetId: String(trip.value.id)
    }
  })
}
</script>

<style scoped>
/* -------------------------------------------------------------
 * Conteneur Global & Responsivité
 * ----------------------------------------------------------- */
.trip-page {
  min-height: 100vh;
  min-height: 100dvh;
  width: 100%;
  background-color: #f3f5f8;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #111827;
  -webkit-font-smoothing: antialiased;
}

.trip-container {
  width: 100%;
  max-width: 420px; /* Largeur optimale mobile, élégamment centrée sur desktop */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.021);
}

/* -------------------------------------------------------------
 * Section Carte d'Arrière-plan
 * ----------------------------------------------------------- */
.map-section {
  position: relative;
  width: 100%;
  height: 250px;
  background-color: #ebe7df;
  overflow: hidden;
}

.map-vector {
  width: 100%;
  height: 100%;
  display: block;
}

.floating-back-btn {
  position: absolute;
  top: 24px;
  left: 20px;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  border: none;
  background-color: #ffffff;
  color: #1e293b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid #E2E8F0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.028);
  transition: all 0.2s ease;
  z-index: 10;
}

.floating-back-btn:hover {
  transform: scale(1.05);
  background-color: #f8fafc;
}

/* -------------------------------------------------------------
 * Feuille Blanche Principale (Bords supérieurs arrondis)
 * ----------------------------------------------------------- */
.trip-sheet {
  position: relative;
  margin-top: -36px;
  background-color: #ffffff;
  border-radius: 36px 36px 0 0;
  padding: 24px 22px 36px;
  display: flex;
  flex-direction: column;
  box-shadow: none;
  border-top: 1px solid #f1f5f9;
  z-index: 2;
  flex-grow: 1;
}

/* -------------------------------------------------------------
 * En-tête : Badge Date, Trajet & Prix
 * ----------------------------------------------------------- */
.header-info-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.time-badge {
  align-self: flex-start;
  padding: 5px 12px;
  background-color: #fff1ee;
  color: #ff4820;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.6px;
  border-radius: 10px;
  text-transform: uppercase;
}

.route-price-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.route-title {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 23px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.route-arrow {
  color: #ff4820;
  font-size: 22px;
}

.price-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  flex-shrink: 0;
}

.price-amount {
  font-size: 28px;
  font-weight: 800;
  color: #ff4820;
  letter-spacing: -0.8px;
  line-height: 1;
}

.price-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #9ca3af;
  margin-top: 4px;
}

/* -------------------------------------------------------------
 * Grille des Cartes Points Clés (Places & Temps)
 * ----------------------------------------------------------- */
.highlight-cards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 22px;
}

.highlight-card {
  background-color: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 18px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.highlight-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.028);
}

.highlight-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.highlight-value {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.highlight-sub {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #9ca3af;
  text-transform: uppercase;
}

/* -------------------------------------------------------------
 * Sections d'Information (Conducteur & Véhicule)
 * ----------------------------------------------------------- */
.info-section {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
}

.section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #9ca3af;
  text-transform: uppercase;
  margin: 0 0 12px;
}

/* Carte Conducteur */
.driver-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.driver-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.driver-photo {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: none;
  border: 1px solid #F1F5F9;
}

.driver-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.driver-name {
  font-size: 17px;
  font-weight: 800;
  color: #111827;
  margin: 0;
  line-height: 1.2;
}

.driver-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
}

.star-icon {
  margin-top: -1px;
}

/* Boutons d'actions rondes (Appel et Chat) */
.driver-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-circle-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background-color: #f1f4f9;
  color: #111827;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-circle-btn:hover {
  background-color: #e2e8f0;
  transform: translateY(-1px);
}

.action-circle-btn:active {
  transform: scale(0.96);
}

/* Carte Véhicule Complète & Élégante */
.section-titre-flex {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-titre-flex .section-title {
  margin-bottom: 0;
}

.badge-clim {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ecfdf5;
  color: #059669;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.vehicle-card-enhanced {
  background-color: #ffffff;
  border: 1.5px solid #edf2f7;
  border-radius: 20px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: none;
}

.vehicle-header-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.vehicle-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(255, 77, 45, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 77, 45, 0.15);
}

.vehicle-title-col {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.vehicle-brand-model {
  font-size: 17px;
  font-weight: 800;
  color: #111827;
  margin: 0;
  line-height: 1.2;
}

.plate-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  width: fit-content;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  padding: 2px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: 0.5px;
  font-family: 'Courier New', Courier, monospace, sans-serif;
}

.vehicle-attributes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding-top: 12px;
  border-top: 1px dashed #e2e8f0;
}

.attribute-box {
  background: #f8fafc;
  border-radius: 12px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  text-align: left;
}

.attr-label {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.attr-val {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.color-val {
  display: flex;
  align-items: center;
  gap: 6px;
}

.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
}

.plate-val {
  font-family: 'Courier New', Courier, monospace, sans-serif;
  font-weight: 800;
  color: #ff4d2d;
}

/* -------------------------------------------------------------
 * CTA Réserver
 * ----------------------------------------------------------- */
.cta-wrapper {
  margin-top: 32px;
}

.conducteur-notice-box {
  margin-top: 32px;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 16px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.conducteur-notice-txt {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  margin: 0;
}

.deja-reserve-notice-box {
  margin-top: 28px;
  background-color: #f0fdf4;
  border: 1.5px solid #bbf7d0;
  border-radius: 20px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: none;
}

.deja-reserve-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.deja-reserve-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background-color: #dcfce7;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.deja-reserve-text-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: left;
}

.deja-reserve-badge {
  display: inline-block;
  align-self: flex-start;
  background-color: #dcfce7;
  color: #15803d;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.6px;
  padding: 3px 8px;
  border-radius: 6px;
}

.deja-reserve-title {
  font-size: 15px;
  font-weight: 800;
  color: #14532d;
  margin: 2px 0 0;
  line-height: 1.3;
}

.deja-reserve-desc {
  font-size: 13px;
  font-weight: 500;
  color: #166534;
  margin: 0;
  line-height: 1.45;
}

.btn-voir-reservation {
  background-color: #059669 !important;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.07) !important;
}

.btn-voir-reservation:hover {
  background-color: #047857 !important;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.09) !important;
}

.btn-icon-reserve {
  margin-right: 8px;
  flex-shrink: 0;
}

.btn-conducteur-espace {
  background-color: #1e293b !important;
  box-shadow: 0 2px 8px rgba(30, 41, 59, 0.06) !important;
}

.btn-conducteur-espace:hover {
  background-color: #0f172a !important;
}

.reserve-cta-btn {
  width: 100%;
  height: 56px;
  background-color: #ff4820;
  color: #ffffff;
  border: none;
  border-radius: 18px;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.2px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(255, 72, 32, 0.07);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.reserve-cta-btn:hover:not(:disabled) {
  background-color: #e63e18;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 72, 32, 0.09);
}

.reserve-cta-btn:active:not(:disabled) {
  transform: scale(0.985);
}

.reserve-cta-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-state {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* -------------------------------------------------------------
 * Panneau Latéral & Éléments Desktop
 * ----------------------------------------------------------- */
.trip-sheet-body {
  width: 100%;
}

.desktop-price-box {
  display: none;
}

.panel-inner-divider {
  display: none;
}

.guarantees-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
  padding: 16px;
  background-color: #f8fafc;
  border-radius: 16px;
  border: 1px solid #f1f5f9;
}

.guarantee-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.guarantee-icon-box {
  width: 30px;
  height: 30px;
  border-radius: 9px;
  background-color: #ffffff;
  color: #ff4820;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: none;
}

.guarantee-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: left;
}

.guarantee-text strong {
  font-size: 13px;
  font-weight: 700;
  color: #111827;
}

.guarantee-text span {
  font-size: 11px;
  color: #64748b;
  line-height: 1.3;
}

/* -------------------------------------------------------------
 * Version Desktop Avancée (@media min-width: 900px)
 * ----------------------------------------------------------- */
@media (min-width: 900px) {
  .trip-page {
    padding: 36px 20px 48px;
    align-items: flex-start;
  }

  .trip-container {
    max-width: 1080px;
    min-height: auto;
    border-radius: 28px;
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.021);
    border: 1px solid #e2e8f0;
    overflow: hidden;
  }

  .map-section {
    height: 180px;
    border-radius: 28px 28px 0 0;
  }

  .floating-back-btn {
    top: 24px;
    left: 28px;
    border-radius: 12px;
  }

  .trip-sheet {
    margin-top: -32px;
    border-radius: 28px;
    padding: 36px 40px 44px;
  }

  .trip-sheet-body {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 40px;
    align-items: flex-start;
  }

  .route-title {
    font-size: 26px;
  }

  .mobile-price-container {
    display: none !important;
  }

  .sticky-booking-panel {
    position: sticky;
    top: 24px;
    background-color: #ffffff;
    border: 1.5px solid #edf2f7;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.021);
    display: flex;
    flex-direction: column;
  }

  .desktop-price-box {
    display: flex;
    flex-direction: column;
    gap: 6px;
    text-align: left;
  }

  .desktop-price-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #94a3b8;
    text-transform: uppercase;
  }

  .desktop-price-val-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .desktop-price-digits {
    font-size: 32px;
    font-weight: 800;
    color: #ff4820;
    letter-spacing: -0.8px;
    line-height: 1;
  }

  .desktop-price-curr {
    font-size: 14px;
    font-weight: 700;
    color: #64748b;
  }

  .desktop-price-curr small {
    font-size: 12px;
    font-weight: 500;
    color: #94a3b8;
  }

  .desktop-seats-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    width: fit-content;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 4px;
  }

  .pill-available {
    background: #ecfdf5;
    color: #059669;
  }

  .pill-full {
    background: #fef2f2;
    color: #dc2626;
  }

  .seats-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
  }

  .panel-inner-divider {
    display: block;
    height: 1px;
    background: #f1f5f9;
    margin: 18px 0;
  }

  .guarantees-list {
    margin-top: 20px;
    padding-top: 18px;
    background: transparent;
    border: none;
    border-top: 1px dashed #e2e8f0;
    border-radius: 0;
    padding-left: 0;
    padding-right: 0;
    padding-bottom: 0;
  }
}

/* -------------------------------------------------------------
 * Ajustements Mobile Écrans Très Étroits
 * ----------------------------------------------------------- */
@media (max-width: 360px) {
  .trip-sheet {
    padding: 20px 16px 28px;
  }
  .route-title {
    font-size: 19px;
  }
  .price-amount {
    font-size: 23px;
  }
  .highlight-cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>