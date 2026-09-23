<template>
  <Teleport to="body">
    <Transition name="success-modal">
      <div
        v-if="modelValue"
        class="modal-overlay"
        role="dialog"
        aria-modal="true"
        aria-labelledby="success-title"
        @click.self="closeModal"
      >
        <div class="success-modal">

          <!-- Icône succès -->
          <div class="success-icon" aria-hidden="true">
            <svg
              viewBox="0 0 48 48"
              fill="none"
            >
              <path
                d="M10 24L19 33L38 14"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>

          <!-- Contenu -->
          <div class="success-content">
            <h2 id="success-title">
              Votre demande a<br />
              bien été reçue !
            </h2>

            <p class="success-description">
              Vos informations et documents sont<br />
              en cours de vérification par nos équipes.<br />
              Ce processus prend généralement<br />
              <strong>moins de 24 heures.</strong>
            </p>
          </div>

          <!-- Actions -->
          <div class="success-actions">
            <button
              type="button"
              class="home-button"
              @click="handleReturnHome"
            >
              Retour à l’accueil
            </button>

            <button
              type="button"
              class="close-button"
              @click="closeModal"
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

/*
 * UX :
 * - fermeture avec Escape
 * - blocage du scroll de la page derrière la modal
 */
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

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');


/* =========================================================
   OVERLAY
========================================================= */

.modal-overlay {
  position: fixed;
  inset: 0;

  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100dvh;

  /*
   * Overlay volontairement léger.
   * La maquette conserve clairement la visibilité
   * de l'écran situé derrière.
   */
  background: rgba(17, 22, 39, 0.42);

  /*
   * Blur léger uniquement.
   */
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);

  padding: 32px 24px;

  overflow-y: auto;
}


/* =========================================================
   MODAL
========================================================= */

.success-modal {
  position: relative;

  width: min(654px, 95%);

  /*
   * Hauteur adaptée au contenu,
   * tout en conservant le centrage.
   */
  min-height: 968px;
  max-height: calc(100dvh - 64px);

  display: flex;
  flex-direction: column;
  align-items: center;

  padding:
    64px
    48px
    52px;

  background: #ffffff;

  border-radius: 48px;

  /*
   * Shadow quasiment invisible,
   * uniquement pour détacher légèrement le blanc
   * de l'overlay.
   */
  box-shadow:
    0 10px 30px rgba(17, 22, 39, 0.06);

  overflow-y: auto;
}


/* =========================================================
   ICON
========================================================= */

.success-icon {
  width: 128px;
  height: 128px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-top: 0;

  border-radius: 38px;

  background: #dcfce8;

  color: #16a34a;
}

.success-icon svg {
  width: 50px;
  height: 50px;
}


/* =========================================================
   CONTENT
========================================================= */

.success-content {
  width: 95%;

  margin-top: 56px;

  text-align: center;
}

.success-content h2 {
  margin: 0;

  color: #111627;

  font-family: 'Plus Jakarta Sans', sans-serif;

  font-size: 48px;
  line-height: 1.20;

  font-weight: 800;

  letter-spacing: -1.5px;
}

.success-description {
  margin: 25px 0 0;

  color: #6b7280;

  font-family: 'Plus Jakarta Sans', sans-serif;

  font-size: 28px;
  line-height: 1.55;

  font-weight: 400;

  letter-spacing: -0.4px;
}

.success-description strong {
  color: #111627;

  font-weight: 800;
}


/* =========================================================
   ACTIONS
========================================================= */

.success-actions {
  width: 100%;

  margin-top: auto;
  padding-top: 48px;

  display: flex;
  flex-direction: column;
  align-items: center;
}


/* =========================================================
   PRIMARY BUTTON
========================================================= */

.home-button {
  width: 100%;
  min-height: 96px;

  border: none;
  border-radius: 30px;

  background: #ff4d2d;
  color: #ffffff;

  font-family: 'Plus Jakarta Sans', sans-serif;

  font-size: 27px;
  line-height: 1.2;
  font-weight: 700;

  cursor: pointer;

  /*
   * Très léger pour rester fidèle à la maquette.
   */
  box-shadow:
    0 8px 20px rgba(255, 77, 45, 0.10);

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.home-button:hover {
  background: #f44729;
  transform: translateY(-1px);
}

.home-button:active {
  transform: translateY(0);
}

.home-button:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.22);
  outline-offset: 4px;
}


/* =========================================================
   CLOSE
========================================================= */

.close-button {
  margin-top: 36px;

  padding: 0;

  border: none;

  background: transparent;

  color: #9ca3af;

  font-family: 'Plus Jakarta Sans', sans-serif;

  font-size: 23px;
  line-height: 1.2;
  font-weight: 700;

  cursor: pointer;

  transition:
    color 0.2s ease;
}

.close-button:hover {
  color: #6b7280;
}

.close-button:focus-visible {
  outline: 3px solid rgba(17, 22, 39, 0.10);
  outline-offset: 5px;
  border-radius: 6px;
}


/* =========================================================
   TRANSITION
========================================================= */

.success-modal-enter-active,
.success-modal-leave-active {
  transition: opacity 0.24s ease;
}

.success-modal-enter-active .success-modal,
.success-modal-leave-active .success-modal {
  transition:
    transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.20s ease;
}

.success-modal-enter-from,
.success-modal-leave-to {
  opacity: 0;
}

.success-modal-enter-from .success-modal,
.success-modal-leave-to .success-modal {
  opacity: 0;
  transform: scale(0.98) translateY(8px);
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 760px) {

  .modal-overlay {
    padding: 24px 20px;
  }

  .success-modal {
    width: min(100%, 654px);

    min-height: auto;

    padding:
      56px
      32px
      44px;

    border-radius: 42px;
  }

  .success-content {
    margin-top: 48px;
  }

  .success-content h2 {
    font-size: 40px;
  }

  .success-description {
    font-size: 23px;
  }

  .home-button {
    min-height: 86px;

    font-size: 24px;
  }

  .close-button {
    font-size: 21px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .modal-overlay {
    padding: 18px 14px;
  }

  .success-modal {
    width: 100%;

    padding:
      42px
      24px
      34px;

    border-radius: 34px;
  }

  .success-icon {
    width: 108px;
    height: 108px;

    border-radius: 32px;
  }

  .success-icon svg {
    width: 42px;
    height: 42px;
  }

  .success-content {
    margin-top: 38px;
  }

  .success-content h2 {
    font-size: 32px;

    letter-spacing: -0.8px;
  }

  .success-description {
    margin-top: 22px;

    font-size: 18px;
    line-height: 1.55;
  }

  .success-actions {
    padding-top: 36px;
  }

  .home-button {
    min-height: 76px;

    border-radius: 24px;

    font-size: 20px;
  }

  .close-button {
    margin-top: 28px;

    font-size: 18px;
  }
}

</style>