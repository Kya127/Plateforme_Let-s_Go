<script setup>
import { computed, ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { serviceTrajets } from '@/services/api'

const props = defineProps({
  trajetId: {
    type: [Number, String],
    required: true
  },
  lieuDepart: {
    type: String,
    default: 'Point de départ'
  },
  destination: {
    type: String,
    default: 'Destination'
  },
  heureDepart: {
    type: String,
    default: '08:30'
  },
  statut: {
    type: String,
    default: 'PLANIFIE'
  }
})

const emit = defineEmits(['fermer', 'eta-change', 'termine'])

// Référentiel des coordonnées GPS réelles de Dakar & presqu'île
const COORDS_DAKAR = {
  'medina': [14.6853, -17.4502],
  'médina': [14.6853, -17.4502],
  'hlm5': [14.6780, -17.4420],
  'hlm': [14.6780, -17.4420],
  'plateau': [14.6677, -17.4337],
  'mermoz': [14.7083, -17.4722],
  'thiaroye': [14.7640, -17.3710],
  'ouakam': [14.7228, -17.4894],
  'almadies': [14.7456, -17.5186],
  'ngor': [14.7550, -17.5140],
  'yoff': [14.7597, -17.4667],
  'parcelles': [14.7550, -17.4350],
  'pikine': [14.7500, -17.3950],
  'rufisque': [14.7167, -17.2667],
  'colobane': [14.6990, -17.4450],
  'fass': [14.6930, -17.4530],
  'sacré-cœur': [14.7140, -17.4650],
  'fann': [14.6910, -17.4680],
  'dakar': [14.6937, -17.4440]
}

function resoudreCoords(nomLieu, fallback = [14.6853, -17.4502]) {
  if (!nomLieu) return fallback
  const cle = nomLieu.toLowerCase().trim()
  for (const [k, coords] of Object.entries(COORDS_DAKAR)) {
    if (cle.includes(k) || k.includes(cle)) {
      return coords
    }
  }
  return fallback
}

// État de télémétrie & Leaflet Layers
const mapEl = ref(null)
let mapInstance = null
let topoTileLayer = null
let markerVehicule = null
let markerDepart = null
let markerDestination = null
let polylineRouteCasing = null
let polylineRoute = null
const intervalId = ref(null)

const initialEstEnCours = props.statut === 'EN_COURS'
const telemetrie = ref({
  statut: props.statut || 'PLANIFIE',
  tracking_actif: initialEstEnCours,
  badge_texte: initialEstEnCours
    ? 'En route • Arrivée dans 12 min'
    : `Trajet planifié • Départ prévu à ${props.heureDepart || '08:30'}`,
  temps_restant_minutes: 12,
  heure_arrivee_estimee: '08:45',
  distance_restante_km: 3.5,
  distance_totale_km: 7.2,
  departCoords: resoudreCoords(props.lieuDepart, [14.6853, -17.4502]),
  destCoords: resoudreCoords(props.destination, [14.6780, -17.4420]),
  vehiculeCoords: resoudreCoords(props.lieuDepart, [14.6853, -17.4502])
})

// États calculés pour l'affichage dynamique
const estEnMouvement = computed(() => {
  return telemetrie.value.statut === 'EN_COURS' && !!telemetrie.value.tracking_actif
})

const estTermine = computed(() => {
  return telemetrie.value.statut === 'TERMINE'
})

const estPlanifie = computed(() => {
  return !estEnMouvement.value && !estTermine.value
})

// Détermine si le badge supérieur doit être affiché
// "une fois arrivé au point de départ, le badge est masqué, il ne restera que le suivi du tracé"
const badgeVisible = computed(() => {
  if (estTermine.value) return false
  if (telemetrie.value.statut === 'ARRIVE_AU_DEPART') return false
  // Si le temps restant jusqu'au point de ralliement est écoulé
  if (estEnMouvement.value && telemetrie.value.temps_restant_minutes !== undefined && telemetrie.value.temps_restant_minutes <= 0) {
    return false
  }
  return true
})

// Texte du badge épuré (suppression de "au point de ralliement" en trop)
const badgeTexteFormate = computed(() => {
  let texte = telemetrie.value.badge_texte || ''
  // Nettoyage systématique de la mention en trop
  texte = texte.replace(' au point de ralliement', '').trim()

  if (texte) return texte

  if (estTermine.value) {
    return 'Trajet terminé'
  }
  if (estEnMouvement.value) {
    const temps = telemetrie.value.temps_restant_minutes || 12
    return `En route • Arrivée dans ${temps} min`
  }
  const hDep = props.heureDepart || '08:30'
  return `Trajet planifié • Départ prévu à ${hDep}`
})

/* =========================================================
   FABRIQUE D'ICÔNES : POINT DE DÉPART ET ICÔNE LOCALISATION
========================================================= */

// 1. Icône de Départ : Pastille d'origine avec anneau noir et point vert central
function creerIconeDepart() {
  return L.divIcon({
    className: 'marker-depart-custom',
    html: `
      <div class="pin-depart-wrapper">
        <div class="pin-depart-badge">
          <span class="pin-depart-dot"></span>
        </div>
        <div class="pin-depart-anchor"></div>
      </div>
    `,
    iconSize: [26, 30],
    iconAnchor: [13, 27]
  })
}

// 2. Icône de Destination : Véritable icône de géolocalisation (Pin gouttelette orange vif)
function creerIconeDestination() {
  return L.divIcon({
    className: 'marker-destination-custom',
    html: `
      <div class="pin-destination-wrapper">
        <svg viewBox="0 0 24 32" width="28" height="36" class="destination-pin-svg">
          <path d="M12 1C6.48 1 2 5.48 2 11c0 7.5 10 20 10 20s10-12.5 10-20c0-5.52-4.48-10-10-10z" fill="#FF4D2D" stroke="#FFFFFF" stroke-width="2" />
          <circle cx="12" cy="11" r="4.2" fill="#FFFFFF" />
        </svg>
      </div>
    `,
    iconSize: [28, 36],
    iconAnchor: [14, 34]
  })
}

// 3. Icône Voiture avec rotation orientée le long du tracé
function creerIconeVehicule(enMouvement, angleDeg = 0) {
  return L.divIcon({
    className: 'marker-vehicule-custom',
    html: `
      <div class="vehicule-marker-wrapper ${enMouvement ? 'en-mouvement' : 'stationne'}">
        ${enMouvement ? `
          <div class="radar-pulse-ring ring-1"></div>
          <div class="radar-pulse-ring ring-2"></div>
        ` : `
          <div class="radar-halo-statique"></div>
        `}
        <div class="vehicule-corps-maquette" style="transform: rotate(${angleDeg}deg);">
          <svg viewBox="0 0 38 22" width="34" height="20" class="voiture-svg">
            <rect x="2" y="2" width="34" height="18" rx="6" fill="#FF4D2D" stroke="#FFFFFF" stroke-width="1.8" />
            <path d="M24 5 L28 5 L27 17 L24 17 Z" fill="#111627" opacity="0.88" />
            <rect x="11" y="4.5" width="10" height="2.5" rx="1" fill="#111627" opacity="0.8" />
            <rect x="11" y="15" width="10" height="2.5" rx="1" fill="#111627" opacity="0.8" />
            <path d="M6 6 L8 6 L8 16 L6 16 Z" fill="#111627" opacity="0.8" />
            <rect x="34" y="4" width="2" height="3" rx="1" fill="#FFFBEB" />
            <rect x="34" y="15" width="2" height="3" rx="1" fill="#FFFBEB" />
          </svg>
        </div>
      </div>
    `,
    iconSize: [44, 44],
    iconAnchor: [22, 22]
  })
}

/* =========================================================
   INITIALISATION ET GESTION DE LA CARTE LEAFLET
========================================================= */
function initCarteLeaflet() {
  if (!mapEl.value || mapInstance) return

  mapInstance = L.map(mapEl.value, {
    zoomControl: false,
    attributionControl: false,
    fadeAnimation: true,
    zoomAnimation: true,
    minZoom: 11,
    maxZoom: 16
  })

  // FOND CARTOGRAPHIQUE TOPO ESRI : Océan bleu doux + relief de Dakar sans pollution
  topoTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16,
    minZoom: 10,
    attribution: ''
  }).addTo(mapInstance)

  actualiserElementsCarte()
}

function actualiserElementsCarte() {
  if (!mapInstance) return

  const dep = telemetrie.value.departCoords || [14.6853, -17.4502]
  const dest = telemetrie.value.destCoords || [14.6780, -17.4420]

  // Calcul du vecteur et de l'angle d'orientation de la route
  const deltaLat = dest[0] - dep[0]
  const deltaLng = dest[1] - dep[1]
  const angleRad = Math.atan2(-deltaLat, deltaLng)
  const angleDeg = Math.round((angleRad * 180) / Math.PI)

  // Positionnement précis du véhicule sur la ligne de tracé sans chevauchement
  let vehiculePos = dep
  if (estPlanifie.value) {
    // Stationnée à proximité immédiate du départ (décalée de 16% sur le tracé)
    vehiculePos = [
      dep[0] + deltaLat * 0.16,
      dep[1] + deltaLng * 0.16
    ]
  } else if (estEnMouvement.value) {
    // En mouvement : progression selon la distance restante
    const totKm = telemetrie.value.distance_totale_km || 1
    const restKm = telemetrie.value.distance_restante_km || 0
    const progress = Math.max(0.18, Math.min(0.82, 1.0 - (restKm / totKm)))
    vehiculePos = [
      dep[0] + deltaLat * progress,
      dep[1] + deltaLng * progress
    ]
  } else {
    // Terminé : à destination
    vehiculePos = dest
  }

  // 1. Tracé de l'itinéraire double-contour (blanc en sous-couche, navy au centre)
  if (polylineRouteCasing) mapInstance.removeLayer(polylineRouteCasing)
  if (polylineRoute) mapInstance.removeLayer(polylineRoute)

  const routePoints = [dep, dest]

  polylineRouteCasing = L.polyline(routePoints, {
    color: '#FFFFFF',
    weight: 7,
    opacity: 0.95,
    lineCap: 'round',
    lineJoin: 'round'
  }).addTo(mapInstance)

  polylineRoute = L.polyline(routePoints, {
    color: '#1E293B',
    weight: 3.5,
    opacity: 0.95,
    dashArray: estPlanifie.value ? '7, 7' : undefined,
    lineCap: 'round',
    lineJoin: 'round'
  }).addTo(mapInstance)

  // 2. Marqueur Point de Départ (Icône départ avec point vert)
  if (markerDepart) {
    markerDepart.setLatLng(dep)
  } else {
    markerDepart = L.marker(dep, {
      icon: creerIconeDepart(),
      zIndexOffset: 300
    }).addTo(mapInstance)
  }

  // 3. Marqueur Destination (Véritable icône de géolocalisation pin orange)
  if (markerDestination) {
    markerDestination.setLatLng(dest)
  } else {
    markerDestination = L.marker(dest, {
      icon: creerIconeDestination(),
      zIndexOffset: 310
    }).addTo(mapInstance)
  }

  // 4. Marqueur Véhicule (Voiture orientée le long du tracé + halos radar)
  if (markerVehicule) {
    markerVehicule.setLatLng(vehiculePos)
    markerVehicule.setIcon(creerIconeVehicule(estEnMouvement.value, angleDeg))
  } else {
    markerVehicule = L.marker(vehiculePos, {
      icon: creerIconeVehicule(estEnMouvement.value, angleDeg),
      zIndexOffset: 500
    }).addTo(mapInstance)
  }

  ajusterVue()
}

/* =========================================================
   CADRAGE GÉOGRAPHIQUE ÉQUILIBRÉ
========================================================= */
function ajusterVue() {
  if (!mapInstance) return

  const dep = telemetrie.value.departCoords || [14.6853, -17.4502]
  const dest = telemetrie.value.destCoords || [14.6780, -17.4420]

  const bounds = L.latLngBounds([dep, dest])

  // Espacement minimal pour aérer les points et éviter tout chevauchement
  const latDiff = Math.abs(dest[0] - dep[0])
  const lngDiff = Math.abs(dest[1] - dep[1])
  const minSpan = 0.016

  if (latDiff < minSpan || lngDiff < minSpan) {
    const centerLat = (dep[0] + dest[0]) / 2
    const centerLng = (dep[1] + dest[1]) / 2
    bounds.extend([centerLat - minSpan * 0.5, centerLng - minSpan * 0.7])
    bounds.extend([centerLat + minSpan * 0.5, centerLng + minSpan * 0.7])
  }

  // Marge vers l'ouest pour garder la mer bleue visible
  bounds.extend([
    Math.min(dep[0], dest[0]) - 0.01,
    Math.min(dep[1], dest[1]) - 0.02
  ])

  mapInstance.fitBounds(bounds, {
    paddingTopLeft: [70, 30],
    paddingBottomRight: [30, 30],
    maxZoom: 15.2
  })
}

/* =========================================================
   POLLING DE LA TÉLÉMÉTRIE DU BACKEND
========================================================= */
async function chargerDonneesSuivi() {
  if (!props.trajetId) return

  try {
    const res = await serviceTrajets.getSuiviDirect(props.trajetId)
    if (res) {
      const depCoords = res.depart?.lat && res.depart?.lng
        ? [res.depart.lat, res.depart.lng]
        : resoudreCoords(props.lieuDepart)

      const destCoords = res.destination?.lat && res.destination?.lng
        ? [res.destination.lat, res.destination.lng]
        : resoudreCoords(props.destination)

      const vehiculeCoords = res.vehicule_position?.lat && res.vehicule_position?.lng
        ? [res.vehicule_position.lat, res.vehicule_position.lng]
        : depCoords

      telemetrie.value = {
        ...telemetrie.value,
        ...res,
        departCoords: depCoords,
        destCoords: destCoords,
        vehiculeCoords: vehiculeCoords,
        badge_texte: res.badge_texte ? res.badge_texte.replace(' au point de ralliement', '') : (
          res.statut === 'EN_COURS' && res.tracking_actif
            ? `En route • Arrivée dans ${res.temps_restant_minutes || 12} min`
            : (res.statut === 'TERMINE' ? 'Trajet terminé' : `Trajet planifié • Départ prévu à ${props.heureDepart || '08:30'}`)
        )
      }

      actualiserElementsCarte()

      emit('eta-change', {
        statut: res.statut,
        tracking_actif: res.tracking_actif,
        temps_restant_minutes: res.temps_restant_minutes || 12,
        heure_arrivee_estimee: res.heure_arrivee_estimee || '08:45',
        distance_restante_km: res.distance_restante_km || 3.5,
        badge_texte: telemetrie.value.badge_texte
      })

      if (res.statut === 'TERMINE') {
        emit('termine', { trajetId: props.trajetId })
      }
    }
  } catch (err) {
    console.warn('Erreur lors du suivi en direct Leaflet:', err)
  }
}

function demarrerPolling() {
  arreterPolling()
  chargerDonneesSuivi()
  intervalId.value = setInterval(() => {
    chargerDonneesSuivi()
  }, 8000)
}

function arreterPolling() {
  if (intervalId.value) {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

onMounted(() => {
  nextTick(() => {
    initCarteLeaflet()
    demarrerPolling()
    setTimeout(() => {
      if (mapInstance) {
        mapInstance.invalidateSize()
        ajusterVue()
      }
    }, 250)
  })
})

onBeforeUnmount(() => {
  arreterPolling()
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})

watch(() => props.trajetId, () => {
  demarrerPolling()
})

watch(() => props.statut, (nouveauStatut) => {
  if (nouveauStatut) {
    telemetrie.value.statut = nouveauStatut
    telemetrie.value.tracking_actif = (nouveauStatut === 'EN_COURS')
    actualiserElementsCarte()
  }
})

watch(() => props.heureDepart, () => {
  if (estPlanifie.value && !telemetrie.value.badge_texte?.includes(props.heureDepart)) {
    telemetrie.value.badge_texte = `Trajet planifié • Départ prévu à ${props.heureDepart || '08:30'}`
  }
})
</script>

<template>
  <div class="carte-graphique-container">
    <!-- Conteneur Réel Leaflet Map -->
    <div ref="mapEl" class="map-leaflet"></div>

    <!-- =======================================================
         ÉLÉMENTS D'INTERFACE FLOTTANTS (EXACTS À LA MAQUETTE)
    ======================================================== -->

    <!-- 1. Bouton Retour Circulaire (En haut à gauche) -->
    <button
      type="button"
      class="btn-carte-retour"
      aria-label="Fermer la vue carte"
      @click="$emit('fermer')"
    >
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#111627" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>

    <!-- 2. Badge Flottant d'État (Masqué une fois arrivé au point de départ) -->
    <div v-if="badgeVisible" class="badge-flottant-eta">
      <!-- Puce d'état dynamique -->
      <span
        class="point-indicateur"
        :class="{
          'point-pulse-vert': estEnMouvement,
          'point-fixe-planifie': estPlanifie,
          'point-fixe-gris': estTermine
        }"
      ></span>
      <!-- Libellé concis sans écriture superflue -->
      <span class="texte-badge-eta">
        {{ badgeTexteFormate }}
      </span>
    </div>

    <!-- 3. Bouton Recentrer Flottant (En bas à droite de la carte) -->
    <button
      type="button"
      class="btn-carte-recenter"
      title="Recentrer le trajet"
      aria-label="Recentrer le trajet sur la carte"
      @click="ajusterVue"
    >
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#111627" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="8"></circle>
        <line x1="12" y1="2" x2="12" y2="4"></line>
        <line x1="12" y1="20" x2="12" y2="22"></line>
        <line x1="2" y1="12" x2="4" y2="12"></line>
        <line x1="20" y1="12" x2="22" y2="12"></line>
        <circle cx="12" cy="12" r="2.5" fill="#FF4D2D"></circle>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.carte-graphique-container {
  position: relative;
  width: 100%;
  height: 275px;
  min-height: 250px;
  overflow: hidden;
  background-color: #BDE4F8; /* Teinte mer bleue océan */
  border-top-left-radius: 36px;
  border-top-right-radius: 36px;
  user-select: none;
}

/* Rendu Leaflet plein écran avec filtre couleur vibrant */
.map-leaflet {
  width: 100%;
  height: 100%;
  z-index: 1;
}

:deep(.leaflet-tile-pane) {
  filter: saturate(1.3) contrast(1.04) brightness(1.01);
}

/* Bouton Retour Circulaire Blanc */
.btn-carte-retour {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 20;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #FFFFFF;
  border: none;
  box-shadow: 0 4px 14px rgba(17, 22, 39, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.btn-carte-retour:hover {
  background-color: #F8FAFC;
  transform: scale(1.05);
}

.btn-carte-retour:active {
  transform: scale(0.96);
}

/* Badge Flottant ETA */
.badge-flottant-eta {
  position: absolute;
  top: 16px;
  left: 64px;
  right: 16px;
  z-index: 20;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 9999px;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px rgba(17, 22, 39, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.85);
  max-width: fit-content;
  max-width: calc(100% - 80px);
}

/* Puces Indicateur Dynamiques */
.point-indicateur {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 1. Point Vert Pulsant (En Route) */
.point-pulse-vert {
  background-color: #10B981;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulseVertAnim 1.8s infinite;
}

/* 2. Point Bleu Fixe (Planifié) */
.point-fixe-planifie {
  background-color: #3B82F6;
  box-shadow: 0 0 0 2.5px rgba(59, 130, 246, 0.25);
}

/* 3. Point Gris Fixe (Terminé) */
.point-fixe-gris {
  background-color: #94A3B8;
  box-shadow: 0 0 0 2px rgba(148, 163, 184, 0.2);
}

@keyframes pulseVertAnim {
  0% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  }
  70% {
    box-shadow: 0 0 0 7px rgba(16, 185, 129, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}

.texte-badge-eta {
  font-size: 12px;
  font-weight: 700;
  color: #111627;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.2px;
}

/* Bouton Recentrer Flottant */
.btn-carte-recenter {
  position: absolute;
  bottom: 22px;
  right: 16px;
  z-index: 20;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #FFFFFF;
  border: none;
  box-shadow: 0 4px 14px rgba(17, 22, 39, 0.14);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.btn-carte-recenter:hover {
  background-color: #F8FAFC;
  transform: scale(1.06);
}

.btn-carte-recenter:active {
  transform: scale(0.94);
}
</style>

<style>
/* =========================================================
   STYLES GLOBAUX POUR LES MARQUEURS DIVICON LEAFLET
========================================================= */

/* 1. MARQUEUR POINT DE DÉPART */
.marker-depart-custom {
  background: transparent !important;
  border: none !important;
}

.pin-depart-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pin-depart-badge {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background-color: #111627;
  border: 2.2px solid #FFFFFF;
  box-shadow: 0 4px 10px rgba(17, 22, 39, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
}

.pin-depart-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10B981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
}

.pin-depart-anchor {
  width: 3px;
  height: 5px;
  background-color: #111627;
  border-radius: 1px;
  margin-top: -1px;
}

/* 2. MARQUEUR POINT DE DESTINATION (PIN LOCALISATION) */
.marker-destination-custom {
  background: transparent !important;
  border: none !important;
}

.pin-destination-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 4px 8px rgba(17, 22, 39, 0.35));
}

.destination-pin-svg {
  display: block;
}

/* 3. VÉHICULE & HALOS RADAR */
.marker-vehicule-custom {
  background: transparent !important;
  border: none !important;
}

.vehicule-marker-wrapper {
  position: relative;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.vehicule-corps-maquette {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 3px 6px rgba(17, 22, 39, 0.3));
  transition: transform 0.4s ease;
}

.radar-halo-statique {
  position: absolute;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: rgba(255, 77, 45, 0.18);
  border: 1.5px solid rgba(255, 77, 45, 0.3);
  pointer-events: none;
}

.radar-pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background-color: rgba(255, 77, 45, 0.28);
  pointer-events: none;
  animation: radarPulseMockup 2.2s infinite ease-out;
}

.radar-pulse-ring.ring-2 {
  animation: radarPulseMockup 2.2s infinite ease-out 0.7s;
  background-color: rgba(255, 77, 45, 0.14);
}

@keyframes radarPulseMockup {
  0% {
    width: 24px;
    height: 24px;
    opacity: 0.85;
  }
  70% {
    opacity: 0.25;
  }
  100% {
    width: 64px;
    height: 64px;
    opacity: 0;
  }
}
</style>
