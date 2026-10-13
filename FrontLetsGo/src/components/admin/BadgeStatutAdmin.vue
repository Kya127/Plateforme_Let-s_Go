<template>
  <!-- Format Badge Pilule plein -->
  <span
    v-if="variant === 'pill'"
    class="badge-pill"
    :class="pillClass"
  >
    {{ labelText }}
  </span>

  <!-- Format Point Statut avec Texte (comme dans la colonne STATUT) -->
  <span
    v-else
    class="badge-dot-container"
    :class="dotClass"
  >
    <span class="status-dot"></span>
    <span class="status-text">{{ labelText }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  statut: {
    type: String,
    required: true,
  },
  variant: {
    type: String,
    default: 'dot', // 'dot' ou 'pill'
  },
})

const normStatut = computed(() => {
  return (props.statut || '').trim().toUpperCase()
})

const labelText = computed(() => {
  switch (normStatut.value) {
    case 'PASSAGER':
      return 'PASSAGER'
    case 'CONDUCTEUR':
      return 'CONDUCTEUR'
    case 'ADMINISTRATEUR':
    case 'ADMIN':
      return 'ADMIN'
    case 'ACTIF':
    case 'ACTIVE':
    case 'TRUE':
      return 'Actif'
    case 'SUSPENDU':
    case 'INACTIF':
    case 'FALSE':
      return 'Suspendu'
    case 'EN_ATTENTE':
    case 'EN ATTENTE':
    case 'PENDING':
      return 'En attente'
    case 'VERIFIE':
    case 'APPROVED':
      return 'Vérifié'
    case 'PLANIFIE':
    case 'PROGRAMME':
      return 'Programmé'
    case 'EN_COURS':
      return 'En cours'
    case 'TERMINE':
      return 'Terminé'
    case 'ANNULE':
      return 'Annulé'
    case 'CONFIRMEE':
      return 'Confirmée'
    default:
      return props.statut
  }
})

const pillClass = computed(() => {
  switch (normStatut.value) {
    case 'PASSAGER':
      return 'pill-passager'
    case 'CONDUCTEUR':
      return 'pill-conducteur'
    case 'ADMINISTRATEUR':
    case 'ADMIN':
      return 'pill-admin'
    case 'VERIFIE':
    case 'APPROVED':
      return 'pill-verifie'
    case 'EN_ATTENTE':
    case 'EN ATTENTE':
    case 'PENDING':
      return 'pill-en-attente'
    case 'SUSPENDU':
      return 'pill-suspendu'
    case 'PLANIFIE':
    case 'PROGRAMME':
      return 'pill-programme'
    case 'EN_COURS':
      return 'pill-en-cours'
    case 'TERMINE':
      return 'pill-termine'
    case 'ANNULE':
      return 'pill-annule'
    case 'CONFIRMEE':
      return 'pill-verifie'
    default:
      return 'pill-default'
  }
})

const dotClass = computed(() => {
  switch (normStatut.value) {
    case 'ACTIF':
    case 'ACTIVE':
    case 'TRUE':
      return 'dot-actif'
    case 'SUSPENDU':
    case 'INACTIF':
    case 'FALSE':
      return 'dot-suspendu'
    case 'EN_ATTENTE':
    case 'EN ATTENTE':
    case 'PENDING':
      return 'dot-attente'
    default:
      return 'dot-actif'
  }
})
</script>

<style scoped>
/* Pilule de rôle / statut */
.badge-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.3px;
  padding: 3px 10px;
  border-radius: 12px;
  text-transform: uppercase;
}

.pill-passager {
  background-color: #f3e8ff;
  color: #8b5cf6;
}

.pill-conducteur {
  background-color: #e0f2fe;
  color: #0284c7;
}

.pill-admin {
  background-color: #fff1ee;
  color: #ff4d2d;
}

.pill-verifie {
  background-color: #d1fae5;
  color: #059669;
}

.pill-en-attente {
  background-color: #ebf5ff;
  color: #2563eb;
}

.pill-suspendu {
  background-color: #fee2e2;
  color: #dc2626;
}

.pill-programme {
  background-color: #e0f2fe;
  color: #0284c7;
}

.pill-en-cours {
  background-color: #ffedd5;
  color: #ea580c;
}

.pill-termine {
  background-color: #f1f5f9;
  color: #64748b;
}

.pill-annule {
  background-color: #fee2e2;
  color: #ef4444;
}

.pill-default {
  background-color: #f3f4f6;
  color: #4b5563;
}

/* Format Point Statut avec Texte */
.badge-dot-container {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 500;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Actif : Point vert */
.dot-actif .status-dot {
  background-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}
.dot-actif .status-text {
  color: #10b981;
}

/* Suspendu : Point gris / neutre */
.dot-suspendu .status-dot {
  background-color: #64748b;
}
.dot-suspendu .status-text {
  color: #64748b;
}

/* En attente : Point orange */
.dot-attente .status-dot {
  background-color: #f59e0b;
}
.dot-attente .status-text {
  color: #d97706;
}
</style>
