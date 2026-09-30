<template>
  <section class="empty-results" aria-live="polite">
    <div class="empty-icon" aria-hidden="true">
      <slot name="icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="11" cy="11" r="7" />
          <path d="M20 20l-4-4" />
        </svg>
      </slot>
    </div>

    <h2>{{ titre }}</h2>
    <p>{{ description }}</p>

    <div v-if="afficherBouton || (afficherSecondaire && secondaireBoutonTexte)" class="empty-actions">
      <button
        v-if="afficherBouton"
        type="button"
        class="empty-button"
        @click="$emit('action')"
      >
        <slot name="bouton-icone" />
        <span>{{ boutonTexte }}</span>
      </button>

      <button
        v-if="afficherSecondaire && secondaireBoutonTexte"
        type="button"
        class="empty-button secondary"
        @click="$emit('action-secondaire')"
      >
        <slot name="secondaire-icone" />
        <span>{{ secondaireBoutonTexte }}</span>
      </button>
    </div>
  </section>
</template>

<script setup>
defineProps({
  titre: {
    type: String,
    default: 'Aucun trajet disponible'
  },
  description: {
    type: String,
    default: 'Aucun trajet ne correspond actuellement à votre recherche.'
  },
  boutonTexte: {
    type: String,
    default: 'Modifier ma recherche'
  },
  afficherBouton: {
    type: Boolean,
    default: true
  },
  secondaireBoutonTexte: {
    type: String,
    default: ''
  },
  afficherSecondaire: {
    type: Boolean,
    default: false
  }
})

defineEmits(['action', 'action-secondaire'])
</script>

<style scoped>
.empty-results {
  min-height: 350px;
  width: 100%;
  max-width: 760px;
  border-radius: 28px;
  background: var(--white, #ffffff);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 38px 24px;
  border: 1px solid rgba(17, 22, 39, 0.05);
  box-shadow: 0 4px 12px rgba(17, 22, 39, 0.028);
  box-sizing: border-box;
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: rgba(255, 77, 45, 0.08);
  color: var(--brand, #ff4d2d);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
}

.empty-icon svg {
  width: 28px;
  height: 28px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
}

.empty-results h2 {
  margin: 0;
  font-size: 21px;
  font-weight: 800;
  color: var(--black, #111627);
  letter-spacing: -0.4px;
}

.empty-results p {
  max-width: 440px;
  margin: 10px 0 24px;
  color: var(--text-secondary, #6b7280);
  font-size: 14px;
  line-height: 1.5;
}

.empty-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.empty-button {
  height: 46px;
  padding: 0 22px;
  border: none;
  border-radius: 14px;
  background: var(--brand, #ff4d2d);
  color: #ffffff;
  font: inherit;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: transform 0.18s ease, background-color 0.18s ease, box-shadow 0.18s ease;
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.09);
}

.empty-button:hover {
  transform: translateY(-1px);
  background: var(--brand-hover, #ed4327);
  box-shadow: 0 6px 16px rgba(255, 77, 45, 0.13);
}

.empty-button:active {
  transform: translateY(0);
}

.empty-button.secondary {
  background: #f0f2f4;
  color: var(--black, #111627);
  box-shadow: none;
}

.empty-button.secondary:hover {
  background: #e4e7eb;
}

@media (max-width: 480px) {
  .empty-results {
    min-height: 300px;
    padding: 30px 18px;
    border-radius: 22px;
  }

  .empty-results h2 {
    font-size: 19px;
  }

  .empty-results p {
    font-size: 13.5px;
    margin: 8px 0 20px;
  }

  .empty-actions {
    flex-direction: column;
    width: 100%;
  }

  .empty-button {
    width: 100%;
  }
}
</style>
