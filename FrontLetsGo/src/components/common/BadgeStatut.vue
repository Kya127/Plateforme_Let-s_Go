<script setup>
import { computed } from 'vue'

const props = defineProps({
  statut: {
    type: String,
    required: true,
  },
  taille: {
    type: String,
    default: 'normal',
    validator: (val) => ['petit', 'normal', 'grand'].includes(val),
  },
})

const configurationStatut = computed(() => {
  const s = (props.statut || '').toUpperCase()
  switch (s) {
    case 'PLANIFIE':
      return { libelle: 'Planifié', classe: 'badge-planifie', dotColor: '#3B82F6' }
    case 'EN_COURS':
      return { libelle: 'En cours', classe: 'badge-en-cours', dotColor: '#FF4D2D' }
    case 'TERMINE':
      return { libelle: 'Terminé', classe: 'badge-termine', dotColor: '#10B981' }
    case 'ANNULE':
      return { libelle: 'Annulé', classe: 'badge-annule', dotColor: '#EF4444' }
    case 'CONFIRMEE':
      return { libelle: 'Confirmée', classe: 'badge-confirmee', dotColor: '#10B981' }
    case 'EN_ATTENTE':
      return { libelle: 'En attente', classe: 'badge-en-attente', dotColor: '#F59E0B' }
    default:
      return { libelle: props.statut, classe: 'badge-defaut', dotColor: '#6B7280' }
  }
})
</script>

<template>
  <span :class="['badge-statut', configurationStatut.classe, `badge-taille--${taille}`]">
    <span class="badge-dot" :style="{ backgroundColor: configurationStatut.dotColor }" aria-hidden="true"></span>
    <span class="badge-libelle">{{ configurationStatut.libelle }}</span>
  </span>
</template>

<style scoped>
.badge-statut {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-family: inherit;
  font-weight: 700;
  font-size: 12px;
  line-height: 1;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.badge-taille--petit {
  padding: 3px 8px;
  font-size: 11px;
}

.badge-taille--grand {
  padding: 6px 14px;
  font-size: 13px;
}

/* Variantes de couleurs */
.badge-planifie {
  background-color: #EFF6FF;
  color: #1D4ED8;
  border: 1px solid #BFDBFE;
}

.badge-en-cours {
  background-color: #FFF7ED;
  color: #C2410C;
  border: 1px solid #FFEDD5;
}

.badge-termine,
.badge-confirmee {
  background-color: #ECFDF5;
  color: #047857;
  border: 1px solid #A7F3D0;
}

.badge-annule {
  background-color: #FEF2F2;
  color: #B91C1C;
  border: 1px solid #FECACA;
}

.badge-en-attente {
  background-color: #FFFBEB;
  color: #B45309;
  border: 1px solid #FDE68A;
}

.badge-defaut {
  background-color: #F3F4F6;
  color: #4B5563;
  border: 1px solid #E5E7EB;
}
</style>
