<template>
  <div v-if="ouvert" class="modal-overlay" @click.self="fermer">
    <div class="modal-card">
      <!-- En-tête -->
      <div class="modal-header">
        <div class="header-icon-wrap icon-role">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
        </div>
        <div class="header-text">
          <h3 class="modal-title">Modifier le rôle</h3>
          <p class="modal-desc">
            Sélectionnez le nouveau statut pour <strong>{{ nomUtilisateur }}</strong>
          </p>
        </div>
      </div>

      <!-- Sélecteur de rôle en cartes visuelles -->
      <div class="roles-selection-grid">
        <!-- Option Passager -->
        <label
          class="role-option-card"
          :class="{ 'role-selected': roleSelectionne === 'PASSAGER' }"
        >
          <input
            type="radio"
            name="nouveau_role"
            value="PASSAGER"
            v-model="roleSelectionne"
            class="sr-only"
          />
          <div class="role-icon-box icon-passager">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </div>
          <div class="role-info">
            <div class="role-title-row">
              <span class="role-name">Passager</span>
              <span v-if="roleSelectionne === 'PASSAGER'" class="check-dot">✓</span>
            </div>
            <p class="role-desc">Recherche et réserve des places sur les trajets disponibles.</p>
          </div>
        </label>

        <!-- Option Conducteur -->
        <label
          class="role-option-card"
          :class="{ 'role-selected': roleSelectionne === 'CONDUCTEUR' }"
        >
          <input
            type="radio"
            name="nouveau_role"
            value="CONDUCTEUR"
            v-model="roleSelectionne"
            class="sr-only"
          />
          <div class="role-icon-box icon-conducteur">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H7.5a1 1 0 0 0-.8.4L4 11l-5.16.86a1 1 0 0 0-.84.99V16h3" />
              <circle cx="6.5" cy="16.5" r="2.5" />
              <circle cx="16.5" cy="16.5" r="2.5" />
            </svg>
          </div>
          <div class="role-info">
            <div class="role-title-row">
              <span class="role-name">Conducteur</span>
              <span v-if="roleSelectionne === 'CONDUCTEUR'" class="check-dot">✓</span>
            </div>
            <p class="role-desc">Peut proposer des trajets, gérer son véhicule et recevoir des passagers.</p>
          </div>
        </label>
      </div>

      <!-- Information contextuelle -->
      <div class="info-alert" :class="roleSelectionne === 'CONDUCTEUR' ? 'alert-conducteur' : 'alert-passager'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="alert-icon">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="16" x2="12" y2="12" />
          <line x1="12" y1="8" x2="12.01" y2="8" />
        </svg>
        <span v-if="roleSelectionne === 'CONDUCTEUR'">
          L'utilisateur sera automatiquement marqué comme <strong>conducteur vérifié</strong>.
        </span>
        <span v-else>
          Le statut de vérification conducteur sera révoqué et ses éventuels trajets futurs seront annulés.
        </span>
      </div>

      <!-- Actions -->
      <div class="modal-actions">
        <button
          type="button"
          @click="fermer"
          class="btn-annuler"
          :disabled="chargement"
        >
          Annuler
        </button>
        <button
          type="button"
          @click="appliquer"
          class="btn-appliquer"
          :disabled="chargement || roleSelectionne === roleActuel"
        >
          <span v-if="chargement" class="spinner"></span>
          <span>{{ chargement ? 'Mise à jour...' : 'Appliquer le rôle' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  ouvert: {
    type: Boolean,
    default: false,
  },
  utilisateur: {
    type: Object,
    default: null,
  },
  chargement: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'confirm'])

const roleSelectionne = ref('PASSAGER')

const nomUtilisateur = computed(() => {
  if (!props.utilisateur) return 'l\'utilisateur'
  const u = props.utilisateur
  return `${u.prenom || ''} ${u.nom_famille || u.nom || ''}`.trim() || u.email || 'l\'utilisateur'
})

const roleActuel = computed(() => {
  return (props.utilisateur?.role || 'PASSAGER').toUpperCase()
})

watch(
  () => props.utilisateur,
  (u) => {
    if (u && u.role) {
      roleSelectionne.value = u.role.toUpperCase()
    } else {
      roleSelectionne.value = 'PASSAGER'
    }
  },
  { immediate: true }
)

function fermer() {
  emit('close')
}

function appliquer() {
  if (!props.utilisateur) return
  emit('confirm', {
    id: props.utilisateur.id,
    role: roleSelectionne.value,
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal-card {
  background: #ffffff;
  border-radius: 20px;
  max-width: 500px;
  width: 100%;
  padding: 28px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: modalPop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalPop {
  0% {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-role {
  background-color: #fff1ee;
  color: #ff4d2d;
}

.header-icon-wrap svg {
  width: 24px;
  height: 24px;
}

.header-text {
  flex: 1;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: #111627;
  margin: 0 0 4px 0;
}

.modal-desc {
  font-size: 13px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.modal-desc strong {
  color: #111627;
}

.roles-selection-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-option-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #ffffff;
}

.role-option-card:hover {
  border-color: #cbd5e1;
  background-color: #f8fafc;
}

.role-option-card.role-selected {
  border-color: #ff4d2d;
  background-color: #fffaf9;
  box-shadow: 0 0 0 3px rgba(255, 77, 45, 0.1);
}

.role-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-passager {
  background-color: #eff6ff;
  color: #3b82f6;
}

.icon-conducteur {
  background-color: #fff1ee;
  color: #ff4d2d;
}

.role-icon-box svg {
  width: 20px;
  height: 20px;
}

.role-info {
  flex: 1;
}

.role-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.role-name {
  font-size: 14px;
  font-weight: 700;
  color: #111627;
}

.check-dot {
  font-size: 12px;
  font-weight: 800;
  color: #ff4d2d;
  background: #fff1ee;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-desc {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.info-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 12px;
  line-height: 1.4;
}

.alert-conducteur {
  background-color: #fff7ed;
  border: 1px solid #ffedd5;
  color: #c2410c;
}

.alert-passager {
  background-color: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #475569;
}

.alert-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

.btn-annuler {
  padding: 10px 18px;
  border-radius: 10px;
  background-color: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #475569;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-annuler:hover:not(:disabled) {
  background-color: #e2e8f0;
}

.btn-appliquer {
  padding: 10px 22px;
  border-radius: 10px;
  background-color: #ff4d2d;
  border: none;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.25);
}

.btn-appliquer:hover:not(:disabled) {
  background-color: #e03e1f;
  transform: translateY(-1px);
}

.btn-appliquer:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
