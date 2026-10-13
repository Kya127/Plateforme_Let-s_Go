<template>
  <div class="carte-kpi" :class="colorVariant">
    <!-- En-tête de la carte : Icône -->
    <div class="kpi-icon-wrap" :style="{ backgroundColor: iconBg, color: iconColor }">
      <slot name="icon">
        <svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
        </svg>
      </slot>
    </div>

    <!-- Contenu principal -->
    <div class="kpi-body">
      <span class="kpi-title">{{ title }}</span>
      <div class="kpi-valeur-row">
        <span class="kpi-valeur">{{ formaterNombre(value) }}</span>
        <span
          v-if="trend"
          class="kpi-trend"
          :class="isTrendUp ? 'trend-up' : 'trend-down'"
        >
          <span class="trend-arrow">{{ isTrendUp ? '↑' : '↓' }}</span>
          <span>{{ trend }}</span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    default: 0,
  },
  trend: {
    type: String,
    default: '',
  },
  trendDirection: {
    type: String,
    default: 'up', // 'up' or 'down'
  },
  iconBg: {
    type: String,
    default: '#FFF1EE',
  },
  iconColor: {
    type: String,
    default: '#FF4D2D',
  },
  colorVariant: {
    type: String,
    default: '',
  },
})

const isTrendUp = computed(() => {
  return props.trendDirection === 'up'
})

function formaterNombre(val) {
  if (val === null || val === undefined) return '0'
  const num = Number(val)
  if (isNaN(num)) return val
  return new Intl.NumberFormat('fr-FR').format(num)
}
</script>

<style scoped>
.carte-kpi {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 18px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.carte-kpi:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
  border-color: #e2e6ee;
}

.kpi-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-icon-wrap :deep(svg) {
  width: 20px;
  height: 20px;
}

.kpi-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-title {
  font-size: 12px;
  font-weight: 500;
  color: #717789;
  letter-spacing: 0.2px;
}

.kpi-valeur-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.kpi-valeur {
  font-size: 24px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -0.5px;
}

.kpi-trend {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 6px;
}

.trend-up {
  color: #10b981;
  background-color: #ecfdf5;
}

.trend-down {
  color: #ef4444;
  background-color: #fef2f2;
}

.trend-arrow {
  font-size: 12px;
  font-weight: 800;
}
</style>
