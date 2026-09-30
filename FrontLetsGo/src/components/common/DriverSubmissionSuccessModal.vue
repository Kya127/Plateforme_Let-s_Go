<template>
  <Teleport to="body">
    <Transition name="success-modal">
      <div
        v-if="modelValue"
        class="modal-overlay"
        role="dialog"
        aria-modal="true"
        aria-labelledby="success-title"
        @click.self="handleClose"
      >
        <div class="success-modal">
          <!-- Icône succès moderne -->
          <div class="success-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
          </div>

          <!-- Contenu -->
          <div class="success-content">
            <h2 id="success-title">
              Votre demande a bien été reçue !
            </h2>

            <p class="success-description">
              Vos informations et documents sont en cours de vérification par nos équipes. Ce processus prend généralement <strong>moins de 24 heures</strong>.
            </p>
          </div>

          <!-- Actions -->
          <div class="success-actions">
            <button
              type="button"
              class="home-button"
              @click="handleHome"
            >
              Retour à l’accueil
            </button>

            <button
              type="button"
              class="close-button"
              @click="handleClose"
            >
              Fermer
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'close',
  'home'
])

const handleClose = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleHome = () => {
  emit('update:modelValue', false)
  emit('home')
}

const handleKeydown = (event) => {
  if (event.key === 'Escape' && props.modelValue) {
    handleClose()
  }
}

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      document.body.classList.add('modal-open')
      document.addEventListener('keydown', handleKeydown)
    } else {
      document.body.classList.remove('modal-open')
      document.removeEventListener('keydown', handleKeydown)
    }
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  document.body.classList.remove('modal-open')
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100dvh;
  background: rgba(17, 24, 39, 0.45);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  padding: 20px;
}

.success-modal {
  position: relative;
  width: min(440px, 94%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 36px 28px 28px;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #f1f2f4;
  text-align: center;
}

.success-icon {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  border-radius: 20px;
  background: #ecfdf5;
  color: #10b981;
  margin-bottom: 20px;
}

.success-icon svg {
  width: 32px;
  height: 32px;
}

.success-content {
  width: 100%;
}

.success-content h2 {
  margin: 0 0 12px;
  color: #111827;
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  font-size: 22px;
  line-height: 1.3;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.success-description {
  margin: 0 0 28px;
  color: #6b7280;
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  font-size: 14px;
  line-height: 1.55;
  font-weight: 400;
}

.success-description strong {
  color: #111827;
  font-weight: 600;
}

.success-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.home-button {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 12px;
  background: #ff4d2d;
  color: #ffffff;
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: none;
  transition: background-color 0.2s ease, transform 0.15s ease;
}

.home-button:hover {
  background: #e63e1f;
}

.home-button:active {
  transform: scale(0.99);
}

.close-button {
  width: 100%;
  height: 38px;
  border: none;
  background: transparent;
  color: #9ca3af;
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 10px;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #4b5563;
}

/* Animations */
.success-modal-enter-active,
.success-modal-leave-active {
  transition: opacity 0.25s ease;
}

.success-modal-enter-active .success-modal,
.success-modal-leave-active .success-modal {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
}

.success-modal-enter-from,
.success-modal-leave-to {
  opacity: 0;
}

.success-modal-enter-from .success-modal,
.success-modal-leave-to .success-modal {
  opacity: 0;
  transform: scale(0.94) translateY(8px);
}
</style>