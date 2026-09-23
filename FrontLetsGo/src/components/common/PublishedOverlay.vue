<template>
  <Teleport to="body">
    <Transition name="published-overlay">
      <div
        v-if="modelValue"
        class="published-overlay"
        role="dialog"
        aria-modal="true"
        aria-labelledby="published-title"
      >
        <div class="published-content">

          <!-- Icône -->
          <div
            class="published-icon"
            aria-hidden="true"
          >
            <svg
              viewBox="0 0 48 48"
              fill="none"
            >
              <circle
                cx="24"
                cy="24"
                r="22"
                stroke="currentColor"
                stroke-width="2"
              />

              <path
                d="M14 24.5L21 31.5L35 16.5"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>

          <!-- Titre -->
          <h2 id="published-title">
            Votre trajet<br />
            est publié !
          </h2>

          <!-- CTA -->
          <button
            type="button"
            class="published-button"
            @click="handleViewTrip"
          >
            <span>Voir mon trajet</span>

            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M5 12h13" />
              <path d="M13 6l6 6-6 6" />
            </svg>
          </button>

          <!-- Fermeture -->
          <button
            type="button"
            class="published-close"
            @click="close"
          >
            Fermer
          </button>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'view-trip',
  'close'
])

const close = () => {
  emit(
    'update:modelValue',
    false
  )

  emit('close')
}

const handleViewTrip = () => {
  emit(
    'update:modelValue',
    false
  )

  emit('view-trip')
}
</script>

<style scoped>
/* =========================================================
   OVERLAY
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

  padding:
    32px
    24px;

  /*
   * Pas de fond blanc.
   * L'écran précédent reste visible.
   */
  background:
    rgba(
      17,
      22,
      39,
      0.46
    );

  /*
   * Blur très léger.
   */
  backdrop-filter:
    blur(4px);

  -webkit-backdrop-filter:
    blur(4px);

  overflow-y: auto;
}


/* =========================================================
   CONTENT
========================================================= */

.published-content {
  width: min(
    100%,
    560px
  );

  display: flex;
  flex-direction: column;
  align-items: center;

  text-align: center;

  /*
   * Très important :
   * aucun background ici.
   * Aucun border.
   * Aucun shadow.
   * Le contenu flotte directement
   * sur l'écran précédent.
   */
}


/* =========================================================
   SUCCESS ICON
========================================================= */

.published-icon {
  width: 126px;
  height: 126px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-bottom: 52px;

  border-radius: 50%;

  background: #14b87d;

  color: #111627;

  box-shadow:
    0 0 0 18px
      rgba(
        20,
        184,
        125,
        0.22
      );
}

.published-icon svg {
  width: 70px;
  height: 70px;
}


/* =========================================================
   TITLE
========================================================= */

.published-content h2 {
  margin: 0;

  color: #ffffff;

  font-family:
    'Plus Jakarta Sans',
    sans-serif;

  font-size: 48px;

  line-height: 1.18;

  font-weight: 800;

  letter-spacing: -1.4px;
}


/* =========================================================
   BUTTON
========================================================= */

.published-button {
  width: 100%;

  min-height: 92px;

  margin-top: 230px;

  display: flex;
  align-items: center;
  justify-content: center;

  gap: 14px;

  border: 0;

  border-radius: 28px;

  background: #ff4d2d;

  color: #ffffff;

  font-family:
    'Plus Jakarta Sans',
    sans-serif;

  font-size: 25px;

  font-weight: 700;

  cursor: pointer;

  box-shadow:
    0 6px 16px
      rgba(
        255,
        77,
        45,
        0.10
      );

  transition:
    background-color 180ms ease,
    transform 180ms ease,
    box-shadow 180ms ease;
}

.published-button:hover {
  background: #f04427;

  transform: translateY(-1px);

  box-shadow:
    0 8px 18px
      rgba(
        255,
        77,
        45,
        0.12
      );
}

.published-button:active {
  transform: translateY(0);

  background: #e94327;
}

.published-button svg {
  width: 30px;
  height: 30px;

  fill: none;

  stroke: currentColor;

  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;

  transition:
    transform 180ms ease;
}

.published-button:hover svg {
  transform:
    translateX(2px);
}


/* =========================================================
   CLOSE
========================================================= */

.published-close {
  margin-top: 28px;

  border: 0;

  background: transparent;

  color: rgba(
    255,
    255,
    255,
    0.72
  );

  font-family:
    'Plus Jakarta Sans',
    sans-serif;

  font-size: 18px;

  font-weight: 600;

  cursor: pointer;
}

.published-close:hover {
  color: #ffffff;
}


/* =========================================================
   TRANSITION
========================================================= */

.published-overlay-enter-active,
.published-overlay-leave-active {
  transition:
    opacity 220ms ease;
}

.published-overlay-enter-active
.published-content,
.published-overlay-leave-active
.published-content {
  transition:
    transform 280ms ease,
    opacity 220ms ease;
}

.published-overlay-enter-from,
.published-overlay-leave-to {
  opacity: 0;
}

.published-overlay-enter-from
.published-content,
.published-overlay-leave-to
.published-content {
  opacity: 0;

  transform:
    translateY(12px)
    scale(0.98);
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .published-overlay {
    padding:
      24px
      20px;
  }

  .published-icon {
    width: 94px;
    height: 94px;

    margin-bottom: 38px;

    box-shadow:
      0 0 0 13px
        rgba(
          20,
          184,
          125,
          0.22
        );
  }

  .published-icon svg {
    width: 54px;
    height: 54px;
  }

  .published-content h2 {
    font-size: 34px;

    letter-spacing: -0.9px;
  }

  .published-button {
    min-height: 72px;

    margin-top: 150px;

    border-radius: 22px;

    font-size: 20px;
  }

  .published-button svg {
    width: 23px;
    height: 23px;
  }

  .published-close {
    margin-top: 24px;

    font-size: 16px;
  }
}
</style>