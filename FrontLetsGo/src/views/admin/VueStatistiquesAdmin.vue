<template>
  <div class="view-statistiques-admin">
    <div class="stats-top-row">
      <div class="header-titles">
        <h2 class="title-main">Statistiques & Analyses de Performance</h2>
        <p class="subtitle-main">Indicateurs clés du réseau de covoiturage LET'S GO</p>
      </div>
    </div>

    <!-- 1. Carte Graphique Croissance -->
    <GraphiqueCroissanceAdmin
      :labels="stats.croissance.labels"
      :donneesUtilisateurs="stats.croissance.utilisateurs"
      :donneesReservations="stats.croissance.reservations"
    />

    <!-- 2. Grille de métriques avancées -->
    <div class="analytics-grid">
      <!-- Répartition des Utilisateurs -->
      <div class="analytics-card">
        <h3 class="card-title">Répartition des Utilisateurs</h3>
        <p class="card-desc">Proportion Passagers vs Conducteurs</p>

        <div class="ratio-bar-wrap">
          <div
            class="ratio-seg seg-passagers"
            :style="{ width: `${pourcentagePassagers}%` }"
          ></div>
          <div
            class="ratio-seg seg-conducteurs"
            :style="{ width: `${pourcentageConducteurs}%` }"
          ></div>
        </div>

        <div class="ratio-legend">
          <div class="ratio-item">
            <span class="ratio-dot dot-purple"></span>
            <span class="ratio-txt">Passagers: <strong>{{ stats.kpis.passagers }} ({{ pourcentagePassagers }}%)</strong></span>
          </div>
          <div class="ratio-item">
            <span class="ratio-dot dot-orange"></span>
            <span class="ratio-txt">Conducteurs: <strong>{{ stats.kpis.conducteurs }} ({{ pourcentageConducteurs }}%)</strong></span>
          </div>
        </div>
      </div>

      <!-- Taux d'occupation moyen réel tiré de la BDD -->
      <div class="analytics-card">
        <h3 class="card-title">Taux de Remplissage</h3>
        <p class="card-desc">Moyenne réelle des places occupées par trajet</p>

        <div class="occupancy-display">
          <span class="occupancy-num">{{ tauxRemplissageFormatted }}%</span>
          <span class="occupancy-badge" :class="occupancyBadgeClass">{{ occupancyBadgeLabel }}</span>
        </div>

        <p class="occupancy-sub">
          Calculé en temps réel sur l'ensemble des trajets et des réservations enregistrés dans la base de données.
        </p>
      </div>

      <!-- Trajets et corridors les plus fréquentés tirés de la BDD -->
      <div class="analytics-card card-full">
        <h3 class="card-title">Corridors et Itinéraires les plus Fréquentés</h3>
        <p class="card-desc">Données réelles des réservations par axe routier</p>

        <div v-if="corridorsList && corridorsList.length" class="corridors-list">
          <div
            v-for="(axe, idx) in corridorsList"
            :key="idx"
            class="corridor-row"
          >
            <div class="corridor-info">
              <span class="corridor-name">{{ axe.route }}</span>
              <span class="corridor-volume">{{ axe.volume }} réservations</span>
            </div>
            <div class="corridor-bar-track">
              <div class="corridor-bar-fill" :style="{ width: `${axe.share}%` }"></div>
            </div>
          </div>
        </div>

        <div v-else class="corridors-empty">
          <p>Aucun corridor enregistré pour le moment dans la base de données.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GraphiqueCroissanceAdmin from '@/components/admin/GraphiqueCroissanceAdmin.vue'
import { serviceAdmin } from '@/services/api'

const stats = ref({
  kpis: {
    total_utilisateurs: 0,
    conducteurs: 0,
    passagers: 0,
    trajets_crees: 0,
    reservations: 0,
    revenus_mensuels: 0,
  },
  croissance: {
    labels: ['Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov'],
    utilisateurs: [0, 0, 0, 0, 0, 0],
    reservations: [0, 0, 0, 0, 0, 0],
  },
  corridors: [],
  taux_remplissage: 0,
})

const pourcentagePassagers = computed(() => {
  const total = stats.value.kpis.passagers + stats.value.kpis.conducteurs
  if (!total) return 50
  return Math.round((stats.value.kpis.passagers / total) * 100)
})

const pourcentageConducteurs = computed(() => {
  return 100 - pourcentagePassagers.value
})

const tauxRemplissage = computed(() => {
  return stats.value.taux_remplissage ?? 0
})

const tauxRemplissageFormatted = computed(() => {
  return Number(tauxRemplissage.value).toFixed(1)
})

const occupancyBadgeLabel = computed(() => {
  const val = Number(tauxRemplissage.value)
  if (val >= 70) return 'Optimal'
  if (val >= 40) return 'Actif'
  return 'En progression'
})

const occupancyBadgeClass = computed(() => {
  const val = Number(tauxRemplissage.value)
  if (val >= 70) return 'badge-green'
  if (val >= 40) return 'badge-orange'
  return 'badge-blue'
})

const corridorsList = computed(() => {
  return stats.value.corridors || []
})

async function chargerStats() {
  try {
    const data = await serviceAdmin.getStats()
    if (data) {
      stats.value = data
    }
  } catch (err) {
    console.error('Erreur chargement statistiques:', err)
  }
}

onMounted(() => {
  chargerStats()
})
</script>

<style scoped>
.view-statistiques-admin {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title-main {
  font-size: 20px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

.subtitle-main {
  font-size: 13px;
  color: #717789;
  margin: 4px 0 0 0;
}

.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 900px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }
}

.analytics-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 20px;
  padding: 24px 26px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.card-full {
  grid-column: 1 / -1;
}

.card-title {
  font-size: 16px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

.card-desc {
  font-size: 12px;
  color: #8b92a5;
  margin: 0;
}

.ratio-bar-wrap {
  width: 100%;
  height: 12px;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  background-color: #f1f5f9;
}

.seg-passagers {
  background-color: #8b5cf6;
}

.seg-conducteurs {
  background-color: #ff4d2d;
}

.ratio-legend {
  display: flex;
  align-items: center;
  gap: 20px;
}

.ratio-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #555b6d;
}

.ratio-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-purple {
  background-color: #8b5cf6;
}

.dot-orange {
  background-color: #ff4d2d;
}

.occupancy-display {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.occupancy-num {
  font-size: 32px;
  font-weight: 800;
  color: #111627;
}

.occupancy-badge {
  font-size: 11px;
  font-weight: 700;
  color: #059669;
  background-color: #d1fae5;
  padding: 3px 8px;
  border-radius: 8px;
}

.occupancy-sub {
  font-size: 13px;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.corridors-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.corridor-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.corridor-info {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.corridor-name {
  font-weight: 700;
  color: #111627;
}

.corridor-volume {
  color: #8b92a5;
  font-size: 12px;
}

.corridor-bar-track {
  width: 100%;
  height: 7px;
  background-color: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.corridor-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff4d2d, #ff7a00);
  border-radius: 4px;
}

.corridors-empty {
  padding: 30px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

.badge-green {
  color: #059669;
  background-color: #d1fae5;
}

.badge-orange {
  color: #d97706;
  background-color: #fef3c7;
}

.badge-blue {
  color: #2563eb;
  background-color: #dbeafe;
}
</style>
