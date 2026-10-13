<template>
  <div class="card-croissance">
    <div class="card-header">
      <div class="header-titles">
        <h3 class="card-title">Croissance de la plateforme</h3>
        <p class="card-subtitle">Évolution des utilisateurs et réservations sur les derniers mois</p>
      </div>

      <!-- Légende -->
      <div class="chart-legend">
        <div class="legend-item">
          <span class="legend-dot dot-users"></span>
          <span class="legend-label">Utilisateurs</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot dot-res"></span>
          <span class="legend-label">Réservations</span>
        </div>
      </div>
    </div>

    <!-- Graphique SVG Interactif -->
    <div class="svg-container" ref="containerRef">
      <svg
        :viewBox="`0 0 ${width} ${height}`"
        preserveAspectRatio="none"
        class="chart-svg"
      >
        <defs>
          <!-- Dégradé Utilisateurs (Orange) -->
          <linearGradient id="gradUsers" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#FF4D2D" stop-opacity="0.18" />
            <stop offset="100%" stop-color="#FF4D2D" stop-opacity="0.0" />
          </linearGradient>
          <!-- Dégradé Réservations (Bleu nuit) -->
          <linearGradient id="gradRes" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#111627" stop-opacity="0.08" />
            <stop offset="100%" stop-color="#111627" stop-opacity="0.0" />
          </linearGradient>
        </defs>

        <!-- Lignes horizontales de repère & labels Y -->
        <g class="grid-lines">
          <template v-for="(niveau, idx) in yLevels" :key="idx">
            <line
              :x1="paddingLeft"
              :y1="niveau.y"
              :x2="width - paddingRight"
              :y2="niveau.y"
              class="grid-line"
            />
            <text
              :x="paddingLeft - 10"
              :y="niveau.y + 4"
              class="axis-label y-label"
              text-anchor="end"
            >
              {{ niveau.label }}
            </text>
          </template>
        </g>

        <!-- Aire sous la courbe Utilisateurs -->
        <path :d="areaPathUsers" fill="url(#gradUsers)" />

        <!-- Aire sous la courbe Réservations -->
        <path :d="areaPathRes" fill="url(#gradRes)" />

        <!-- Ligne Utilisateurs (Orange) -->
        <path
          :d="linePathUsers"
          fill="none"
          stroke="#FF4D2D"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="chart-line"
        />

        <!-- Ligne Réservations (Noir / Nuit) -->
        <path
          :d="linePathRes"
          fill="none"
          stroke="#111627"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="chart-line"
        />

        <!-- Points de données Utilisateurs -->
        <g class="points-users">
          <circle
            v-for="(p, i) in pointsUsers"
            :key="'u-' + i"
            :cx="p.x"
            :cy="p.y"
            r="4.5"
            fill="#ffffff"
            stroke="#FF4D2D"
            stroke-width="2.5"
            class="data-point"
            @mouseenter="survolPoint(i, 'users')"
            @mouseleave="quitterPoint"
          />
        </g>

        <!-- Points de données Réservations -->
        <g class="points-res">
          <circle
            v-for="(p, i) in pointsRes"
            :key="'r-' + i"
            :cx="p.x"
            :cy="p.y"
            r="4"
            fill="#ffffff"
            stroke="#111627"
            stroke-width="2.5"
            class="data-point"
            @mouseenter="survolPoint(i, 'res')"
            @mouseleave="quitterPoint"
          />
        </g>

        <!-- Ligne verticale au survol -->
        <line
          v-if="hoverIdx !== null"
          :x1="hoverX"
          :y1="paddingTop"
          :x2="hoverX"
          :y2="height - paddingBottom"
          stroke="#cbd5e1"
          stroke-dasharray="3,3"
          stroke-width="1.5"
        />

        <!-- Labels X (Mois) -->
        <g class="labels-x">
          <text
            v-for="(label, i) in labels"
            :key="'lbl-' + i"
            :x="getX(i)"
            :y="height - 10"
            class="axis-label x-label"
            text-anchor="middle"
          >
            {{ label }}
          </text>
        </g>
      </svg>

      <!-- Tooltip HTML Flottant -->
      <div
        v-if="hoverIdx !== null"
        class="chart-tooltip"
        :style="{ left: tooltipPos.x + 'px', top: tooltipPos.y + 'px' }"
      >
        <span class="tooltip-month">{{ labels[hoverIdx] }}</span>
        <div class="tooltip-row">
          <span class="tooltip-badge dot-users"></span>
          <span>Utilisateurs: <strong>{{ donneesUtilisateurs[hoverIdx] }}</strong></span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-badge dot-res"></span>
          <span>Réservations: <strong>{{ donneesReservations[hoverIdx] }}</strong></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  labels: {
    type: Array,
    default: () => ['Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov'],
  },
  donneesUtilisateurs: {
    type: Array,
    default: () => [12, 14, 15, 16, 16, 16],
  },
  donneesReservations: {
    type: Array,
    default: () => [3, 4, 6, 7, 8, 8],
  },
})

const width = 640
const height = 240
const paddingLeft = 45
const paddingRight = 20
const paddingTop = 25
const paddingBottom = 35

const hoverIdx = ref(null)
const containerRef = ref(null)
const tooltipPos = ref({ x: 0, y: 0 })

// Trouver le max pour l'échelle
const maxVal = computed(() => {
  const all = [...props.donneesUtilisateurs, ...props.donneesReservations]
  const m = Math.max(...all, 10)
  return Math.ceil(m * 1.2)
})

// Paliers Y
const yLevels = computed(() => {
  const m = maxVal.value
  const steps = 4
  const res = []
  for (let i = 0; i <= steps; i++) {
    const val = Math.round((m / steps) * i)
    const y = getY(val)
    let label = `${val}`
    if (val >= 1000) {
      label = `${(val / 1000).toFixed(0)}k`
    }
    res.push({ val, y, label })
  }
  return res
})

function getX(index) {
  const count = props.labels.length
  if (count <= 1) return paddingLeft
  const step = (width - paddingLeft - paddingRight) / (count - 1)
  return paddingLeft + index * step
}

function getY(value) {
  const plotH = height - paddingTop - paddingBottom
  const ratio = value / (maxVal.value || 1)
  return height - paddingBottom - ratio * plotH
}

const pointsUsers = computed(() => {
  return props.donneesUtilisateurs.map((val, idx) => ({
    x: getX(idx),
    y: getY(val),
  }))
})

const pointsRes = computed(() => {
  return props.donneesReservations.map((val, idx) => ({
    x: getX(idx),
    y: getY(val),
  }))
})

// Générer courbe spline lisse (Catmull-Rom ou Bézier cubique)
function creerSpline(points) {
  if (points.length === 0) return ''
  if (points.length === 1) return `M ${points[0].x} ${points[0].y}`
  let d = `M ${points[0].x} ${points[0].y}`
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[Math.max(0, i - 1)]
    const p1 = points[i]
    const p2 = points[i + 1]
    const p3 = points[Math.min(points.length - 1, i + 2)]

    const cp1x = p1.x + (p2.x - p0.x) / 6
    const cp1y = p1.y + (p2.y - p0.y) / 6
    const cp2x = p2.x - (p3.x - p1.x) / 6
    const cp2y = p2.y - (p3.y - p1.y) / 6

    d += ` C ${cp1x.toFixed(1)} ${cp1y.toFixed(1)}, ${cp2x.toFixed(1)} ${cp2y.toFixed(1)}, ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`
  }
  return d
}

const linePathUsers = computed(() => creerSpline(pointsUsers.value))
const linePathRes = computed(() => creerSpline(pointsRes.value))

const areaPathUsers = computed(() => {
  const line = linePathUsers.value
  if (!line || pointsUsers.value.length === 0) return ''
  const first = pointsUsers.value[0]
  const last = pointsUsers.value[pointsUsers.value.length - 1]
  const baseY = height - paddingBottom
  return `${line} L ${last.x} ${baseY} L ${first.x} ${baseY} Z`
})

const areaPathRes = computed(() => {
  const line = linePathRes.value
  if (!line || pointsRes.value.length === 0) return ''
  const first = pointsRes.value[0]
  const last = pointsRes.value[pointsRes.value.length - 1]
  const baseY = height - paddingBottom
  return `${line} L ${last.x} ${baseY} L ${first.x} ${baseY} Z`
})

const hoverX = computed(() => {
  if (hoverIdx.value === null) return 0
  return getX(hoverIdx.value)
})

function survolPoint(idx, type) {
  hoverIdx.value = idx
  if (containerRef.value) {
    const rect = containerRef.value.getBoundingClientRect()
    const px = (getX(idx) / width) * rect.width
    const py = (getY(props.donneesUtilisateurs[idx]) / height) * rect.height
    tooltipPos.value = {
      x: Math.min(Math.max(px - 60, 10), rect.width - 130),
      y: Math.max(py - 70, 10),
    }
  }
}

function quitterPoint() {
  hoverIdx.value = null
}
</script>

<style scoped>
.card-croissance {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 18px;
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.header-titles {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  color: #111627;
  margin: 0;
}

.card-subtitle {
  font-size: 12px;
  color: #8b92a5;
  margin: 0;
}

.chart-legend {
  display: flex;
  align-items: center;
  gap: 18px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 7px;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-users {
  background-color: #ff4d2d;
}

.dot-res {
  background-color: #111627;
}

.legend-label {
  font-size: 12px;
  font-weight: 500;
  color: #555b6d;
}

.svg-container {
  position: relative;
  width: 100%;
  height: 220px;
}

.chart-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.grid-line {
  stroke: #f1f3f7;
  stroke-dasharray: 4,4;
}

.axis-label {
  font-size: 10.5px;
  fill: #9aa1b3;
  font-family: inherit;
  font-weight: 500;
}

.data-point {
  cursor: pointer;
  transition: r 0.15s ease, stroke-width 0.15s ease;
}

.data-point:hover {
  r: 6.5;
  stroke-width: 3.5;
}

.chart-tooltip {
  position: absolute;
  background: rgba(17, 22, 39, 0.92);
  backdrop-filter: blur(8px);
  color: #ffffff;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 11px;
  pointer-events: none;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 20;
  min-width: 120px;
}

.tooltip-month {
  font-weight: 700;
  color: #e2e8f0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 4px;
}

.tooltip-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tooltip-badge {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
</style>
