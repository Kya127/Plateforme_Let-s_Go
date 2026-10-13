<template>
  <div v-if="ouvert" class="modal-overlay" @click.self="fermer">
    <div class="modal-card">
      <div class="modal-header">
        <div class="header-icon-wrap" :class="isDanger ? 'icon-danger' : 'icon-warning'">
          <svg v-if="isDanger" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
        </div>
        <div class="header-text">
          <h3 class="modal-title">{{ titre }}</h3>
          <p class="modal-desc">{{ message }}</p>
        </div>
      </div>

      <div class="modal-actions">
        <button @click="fermer" class="btn-annuler" type="button" :disabled="chargement">
          Annuler
        </button>
        <button
          @click="confirmer"
          class="btn-confirmer"
          :class="isDanger ? 'btn-danger' : 'btn-primary'"
          type="button"
          :disabled="chargement"
        >
          <span v-if="chargement" class="spinner"></span>
          <span>{{ boutonLabel }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  ouvert: {
    type: Boolean,
    default: false,
  },
  titre: {
    type: String,
    default: 'Confirmation',
  },
  message: {
    type: String,
    default: 'Êtes-vous sûr de vouloir effectuer cette action ?',
  },
  boutonLabel: {
    type: String,
    default: 'Confirmer',
  },
  isDanger: {
    type: Boolean,
    default: true,
  },
  chargement: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'confirm'])

function fermer() {
  emit('close')
}

function confirmer() {
  emit('confirm')
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
  max-width: 460px;
  width: 100%;
  padding: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.header-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-danger {
  background-color: #fee2e2;
  color: #ef4444;
}

.icon-warning {
  background-color: #fef3c7;
  color: #d97706;
}

.header-icon-wrap svg {
  width: 22px;
  height: 22px;
}

.header-text {
  flex: 1;
}

.modal-title {
  font-size: 16px;
  font-weight: 700;
  color: #111627;
  margin: 0 0 6px 0;
}

.modal-desc {
  font-size: 13px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-annuler {
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 10px;
  padding: 9px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-annuler:hover {
  background: #e2e8f0;
}

.btn-confirmer {
  border: none;
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-danger {
  background: #ef4444;
  color: #ffffff;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-primary {
  background: #ff4d2d;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #ea3f20;
}

.btn-confirmer:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
