<script setup>
import { computed } from 'vue'

const props = defineProps({
  variante: {
    type: String,
    default: 'primaire',
    validator: (val) =>
      ['primaire', 'secondaire', 'contour', 'fantome', 'sombre', 'noir', 'primary', 'secondary', 'outline', 'ghost', 'dark', 'black'].includes(val),
  },
  type: {
    type: String,
    default: 'button',
  },
  desactive: {
    type: Boolean,
    default: false,
  },
  bloc: {
    type: Boolean,
    default: false,
  },
  chargement: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['clic', 'click'])

const classeVariante = computed(() => {
  const map = {
    primaire: 'btn-primaire',
    primary: 'btn-primaire',
    secondaire: 'btn-secondaire',
    secondary: 'btn-secondaire',
    contour: 'btn-contour',
    outline: 'btn-contour',
    fantome: 'btn-fantome',
    ghost: 'btn-fantome',
    sombre: 'btn-sombre',
    dark: 'btn-sombre',
    noir: 'btn-sombre',
    black: 'btn-sombre',
  }
  return map[props.variante] || 'btn-primaire'
})
</script>

<template>
  <button
    :type="type"
    :disabled="desactive || chargement"
    :class="[
      'bouton-base',
      classeVariante,
      { 'btn-bloc': bloc, 'est-en-chargement': chargement }
    ]"
    @click="$emit('clic', $event); $emit('click', $event)"
  >
    <span v-if="chargement" class="btn-indicateur" aria-hidden="true"></span>
    <span v-if="($slots.prefixe || $slots.prefix) && !chargement" class="btn-icone btn-icone-prefixe">
      <slot name="prefixe">
        <slot name="prefix" />
      </slot>
    </span>
    <span class="btn-libelle">
      <slot />
    </span>
    <span v-if="($slots.suffixe || $slots.suffix) && !chargement" class="btn-icone btn-icone-suffixe">
      <slot name="suffixe">
        <slot name="suffix" />
      </slot>
    </span>
  </button>
</template>

<style scoped>
.bouton-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  height: 54px;
  padding: 0 24px;
  font-family: var(--font-family-base);
  font-size: 16px;
  font-weight: 600;
  border-radius: var(--radius-lg);
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast), background-color var(--transition-fast), border-color var(--transition-fast);
  user-select: none;
  white-space: nowrap;
}

.bouton-base:focus-visible {
  outline: 2px solid var(--color-brand-accent);
  outline-offset: 2px;
}

.bouton-base:active:not(:disabled) {
  transform: scale(0.985);
}

.btn-bloc {
  width: 100%;
}

/* Variante Primaire (Orange) */
.btn-primaire {
  background-color: var(--color-brand-accent);
  color: var(--color-white);
  box-shadow: var(--shadow-accent);
}

.btn-primaire:hover:not(:disabled) {
  background-color: var(--color-brand-accent-hover);
  box-shadow: var(--shadow-hover);
}

/* Variante Secondaire (Gris clair) */
.btn-secondaire {
  background-color: var(--color-input-bg);
  color: var(--color-black);
}

.btn-secondaire:hover:not(:disabled) {
  background-color: var(--color-soft-gray);
}

/* Variante Contour (Bordure) */
.btn-contour {
  background-color: var(--color-white);
  border-color: var(--color-soft-gray);
  color: var(--color-black);
}

.btn-contour:hover:not(:disabled) {
  border-color: #D1D5DB;
  background-color: #FBFBFB;
}

/* Variante Fantôme (Teinte orange légère) */
.btn-fantome {
  background-color: var(--color-brand-accent-light);
  color: var(--color-brand-accent);
}

.btn-fantome:hover:not(:disabled) {
  background-color: rgba(255, 77, 45, 0.16);
}

/* Variante Sombre / Noir (Noir design system #111827) */
.btn-sombre {
  background-color: #111827;
  color: var(--color-white);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-sombre:hover:not(:disabled) {
  background-color: #1f2937;
}

/* État Désactivé */
.bouton-base:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  box-shadow: none !important;
  transform: none !important;
}

/* Icônes */
.btn-icone {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.btn-indicateur {
  width: 20px;
  height: 20px;
  border: 2.5px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: btn-rotation 0.7s linear infinite;
}

@keyframes btn-rotation {
  to {
    transform: rotate(360deg);
  }
}
</style>
