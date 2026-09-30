<script setup>
defineProps({
  titre: {
    type: String,
    required: true,
  },
  afficherRetour: {
    type: Boolean,
    default: true,
  },
  sousTitre: {
    type: String,
    default: '',
  },
})

defineEmits(['retour'])
</script>

<template>
  <header class="page-header">
    <button
      v-if="afficherRetour"
      type="button"
      class="back-button"
      aria-label="Retour"
      @click="$emit('retour')"
    >
      <svg viewBox="0 0 24 24" aria-hidden="true" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>

    <div class="header-titles">
      <h1 class="header-h1">{{ titre }}</h1>
      <p v-if="sousTitre" class="header-sub">{{ sousTitre }}</p>
      <slot name="badge" />
    </div>

    <div v-if="$slots.actions" class="header-actions">
      <slot name="actions" />
    </div>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.back-button {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid #E5E7EB;
  background-color: #FFFFFF;
  color: #111627;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.18s ease;
  box-shadow: 0 2px 4px rgba(17, 22, 39, 0.028);
}

.back-button:hover {
  background-color: #F8FAFC;
  border-color: #D1D5DB;
  transform: translateX(-2px);
}

.header-titles {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  flex: 1;
}

.header-h1 {
  font-size: 24px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -0.5px;
  margin: 0;
}

.header-sub {
  font-size: 13px;
  color: #6B7280;
  margin: 0;
  width: 100%;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 640px) {
  .page-header {
    gap: 12px;
    margin-bottom: 18px;
  }
  .back-button {
    width: 38px;
    height: 38px;
  }
  .header-h1 {
    font-size: 20px;
  }
}
</style>
