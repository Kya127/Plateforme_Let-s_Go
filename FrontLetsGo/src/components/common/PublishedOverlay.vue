<template>
  <Teleport to="body">
    <Transition name="published-modal">
      <div
        v-if="modelValue"
        class="published-overlay"
        role="dialog"
        aria-modal="true"
        aria-labelledby="published-title"
        @click.self="close"
      >
        <div class="published-card">
          <!-- Icône de succès douce et épurée -->
          <div class="published-icon" aria-hidden="true">
            <svg
              viewBox="0 0 24 24"
              width="26"
              height="26"
              fill="none"
              stroke="#10B981"
              stroke-width="2.6"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>

          <!-- Titre -->
          <h2 id="published-title">
            Votre trajet est publié !
          </h2>

          <!-- Actions -->
          <div class="published-actions">
            <button
              type="button"
              class="published-button"
              @click="handleViewTrip"
            >
              <span>Voir mon trajet</span>
              <svg
                viewBox="0 0 24 24"
                width="17"
                height="17"
                fill="none"
                stroke="currentColor"
                stroke-width="2.2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            </button>

            <!-- Retour à l'accueil -->
            <button
              type="button"
              class="published-close"
              @click="close"
            >
              Retourner à l'accueil
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'update:modelValue',
  'view-trip',
  'close',
])

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleViewTrip = () => {
  emit('update:modelValue', false)
  emit('view-trip')
}
</script>

<style scoped>
/* =========================================================
   OVERLAY / BACKDROP
========================================================= */
.published-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  width: 100%;
  height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: rgba(17, 24, 39, 0.45);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

/* =========================================================
   MODAL CARD
========================================================= */
.published-card {
  width: 100%;
  max-width: 390px;
  background-color: #FFFFFF;
  border-radius: 22px;
  padding: 30px 24px 22px;
  text-align: center;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* =========================================================
   SUCCESS ICON (Soft & Elegant)
========================================================= */
.published-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #ECFDF5;
  border: 1px solid #A7F3D0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 0 0 5px rgba(16, 185, 129, 0.08);
  flex-shrink: 0;
}

/* =========================================================
   TITLE
========================================================= */
.published-card h2 {
  margin: 0 0 22px 0;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  line-height: 1.35;
  letter-spacing: -0.02em;
}

/* =========================================================
   ACTIONS
========================================================= */
.published-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.published-button {
  width: 100%;
  height: 46px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 12px;
  background-color: #FF4D2D;
  color: #FFFFFF;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(255, 77, 45, 0.15);
  transition: all 0.18s ease;
}

.published-button:hover {
  background-color: #F04427;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(255, 77, 45, 0.2);
}

.published-button:active {
  transform: translateY(0);
}

.published-close {
  width: 100%;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #6B7280;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.15s ease;
}

.published-close:hover {
  color: #111827;
}

/* =========================================================
   TRANSITION ANIMATION (Smooth & Soft)
========================================================= */
.published-modal-enter-active,
.published-modal-leave-active {
  transition: opacity 0.2s ease;
}

.published-modal-enter-from,
.published-modal-leave-to {
  opacity: 0;
}

.published-modal-enter-active .published-card,
.published-modal-leave-active .published-card {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
}

.published-modal-enter-from .published-card,
.published-modal-leave-to .published-card {
  opacity: 0;
  transform: translateY(10px) scale(0.97);
}

/* =========================================================
   MOBILE RESPONSIVENESS
========================================================= */
@media (max-width: 480px) {
  .published-overlay {
    padding: 16px;
  }

  .published-card {
    max-width: 340px;
    padding: 24px 18px 18px;
    border-radius: 20px;
  }

  .published-icon {
    width: 50px;
    height: 50px;
    margin-bottom: 14px;
  }

  .published-icon svg {
    width: 24px;
    height: 24px;
  }

  .published-card h2 {
    font-size: 18px;
    margin-bottom: 18px;
  }

  .published-button {
    height: 44px;
    font-size: 14.5px;
  }

  .published-close {
    height: 36px;
    font-size: 13px;
  }
}
</style>