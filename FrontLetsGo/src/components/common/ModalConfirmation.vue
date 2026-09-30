<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  titre: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    default: '',
  },
  texteConfirmer: {
    type: String,
    default: 'Confirmer',
  },
  texteAnnuler: {
    type: String,
    default: 'Retour',
  },
  type: {
    type: String,
    default: 'danger',
    validator: (val) => ['danger', 'avertissement', 'info', 'succes'].includes(val),
  },
  afficherAnnuler: {
    type: Boolean,
    default: true,
  },
  enChargement: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['confirmer', 'annuler', 'fermer'])
</script>

<template>
  <Teleport to="body">
    <Transition name="fade-modal">
      <div
        v-if="visible"
        class="modal-backdrop"
        role="dialog"
        aria-modal="true"
        @click.self="$emit('fermer')"
      >
        <div class="modal-dialog-card">
          <!-- Icône du type -->
          <div :class="['modal-icon-badge', `modal-icon--${type}`]" aria-hidden="true">
            <svg v-if="type === 'danger'" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <svg v-else-if="type === 'avertissement'" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
            <svg v-else-if="type === 'succes'" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            <svg v-else viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
          </div>

          <h2 class="modal-h2">{{ titre }}</h2>
          <p v-if="message" class="modal-text">{{ message }}</p>
          <slot />

          <!-- Boutons d'action -->
          <div class="modal-actions-row">
            <button
              v-if="afficherAnnuler"
              type="button"
              class="btn-modal-annuler"
              :disabled="enChargement"
              @click="$emit('annuler')"
            >
              {{ texteAnnuler }}
            </button>

            <button
              type="button"
              :class="['btn-modal-action', `btn-${type}`]"
              :disabled="enChargement"
              @click="$emit('confirmer')"
            >
              <span v-if="enChargement" class="spinner-inline"></span>
              <span>{{ texteConfirmer }}</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.55);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.modal-dialog-card {
  width: 100%;
  max-width: 440px;
  background: #FFFFFF;
  border-radius: 24px;
  padding: 28px 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.09);
  text-align: center;
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.modal-icon-badge {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.modal-icon--danger {
  background-color: #FEF2F2;
  color: #EF4444;
}

.modal-icon--avertissement {
  background-color: #FFFBEB;
  color: #F59E0B;
}

.modal-icon--info {
  background-color: #EFF6FF;
  color: #3B82F6;
}

.modal-icon--succes {
  background-color: #D1FAE5;
  color: #10B981;
}

.modal-h2 {
  font-size: 20px;
  font-weight: 800;
  color: #111627;
  margin: 0 0 10px;
}

.modal-text {
  font-size: 14px;
  color: #6B7280;
  line-height: 1.5;
  margin: 0 0 24px;
}

.modal-actions-row {
  display: flex;
  gap: 12px;
}

.btn-modal-annuler {
  flex: 1;
  height: 48px;
  border-radius: 14px;
  border: 1px solid #E5E7EB;
  background-color: #FFFFFF;
  color: #374151;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-modal-annuler:hover:not(:disabled) {
  background-color: #F9FAFB;
}

.btn-modal-action {
  flex: 1;
  height: 48px;
  border-radius: 14px;
  border: none;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-danger {
  background-color: #EF4444;
  color: #FFFFFF;
}

.btn-danger:hover:not(:disabled) {
  background-color: #DC2626;
}

.btn-avertissement {
  background-color: #F59E0B;
  color: #FFFFFF;
}

.btn-avertissement:hover:not(:disabled) {
  background-color: #D97706;
}

.btn-info {
  background-color: #3B82F6;
  color: #FFFFFF;
}

.btn-info:hover:not(:disabled) {
  background-color: #2563EB;
}

.btn-succes {
  background-color: #FF4D2D;
  color: #FFFFFF;
}

.btn-succes:hover:not(:disabled) {
  background-color: #F04427;
}

.spinner-inline {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes modalPop {
  0% { transform: scale(0.92); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.fade-modal-enter-active,
.fade-modal-leave-active {
  transition: opacity 0.2s ease;
}

.fade-modal-enter-from,
.fade-modal-leave-to {
  opacity: 0;
}
</style>
