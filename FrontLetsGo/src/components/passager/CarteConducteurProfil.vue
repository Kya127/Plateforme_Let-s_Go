<script setup>
defineProps({
  id: {
    type: [Number, String],
    default: null,
  },
  nom: {
    type: String,
    required: true,
  },
  photo: {
    type: String,
    default: '',
  },
  note: {
    type: [Number, String],
    default: 4.9,
  },
  telephone: {
    type: String,
    default: '',
  },
  afficherActions: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['voir-profil', 'appeler', 'ecrire'])

function handleImageError(event) {
  event.target.src = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=256'
}
</script>

<template>
  <div
    class="driver-card"
    role="button"
    tabindex="0"
    :title="`Voir le profil et les avis de ${nom}`"
    @click="$emit('voir-profil', id)"
    @keydown.enter="$emit('voir-profil', id)"
    @keydown.space.prevent="$emit('voir-profil', id)"
  >
    <div class="driver-left">
      <img
        :src="photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=256'"
        :alt="`Photo de ${nom}`"
        class="driver-photo"
        @error="handleImageError"
      />
      <div class="driver-meta">
        <div class="driver-name-row">
          <h3 class="driver-name">{{ nom }}</h3>
          <span class="badge-verifie-mini" title="Conducteur vérifié">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="#10B981">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </span>
        </div>
        <div class="driver-rating">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="#FF4D2D" class="star-icon">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          <span class="rating-value">{{ Number(note || 4.9).toFixed(1) }}</span>
          <span class="view-profile-hint">Voir profil & avis</span>
          <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="chevron-hint">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
      </div>
    </div>

    <!-- Actions Conducteur (Appel & Message) -->
    <div v-if="afficherActions" class="driver-actions" @click.stop>
      <button
        type="button"
        class="action-circle-btn"
        aria-label="Appeler le conducteur"
        title="Appeler"
        @click.stop="$emit('appeler')"
      >
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
          <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.053 15.053 0 0 1-6.59-6.59l2.2-2.21a.96.96 0 0 0 .25-1.01A11.36 11.36 0 0 1 8.57 3.9c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.52c0-.55-.45-1-.99-1z"/>
        </svg>
      </button>

      <button
        type="button"
        class="action-circle-btn"
        aria-label="Envoyer un message au conducteur"
        title="Envoyer un message"
        @click.stop="$emit('ecrire')"
      >
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.driver-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.18s ease;
  user-select: none;
}

.driver-card:hover {
  border-color: #FF4D2D;
  background-color: #FFFAF8;
  transform: translateY(-1px);
}

.driver-card:focus-visible {
  outline: 2px solid #FF4D2D;
  outline-offset: 2px;
}

.driver-left {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
  min-width: 0;
}

.driver-photo {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #F3F4F6;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.driver-card:hover .driver-photo {
  transform: scale(1.04);
}

.driver-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.driver-name-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.driver-name {
  font-size: 15px;
  font-weight: 800;
  color: #111627;
  margin: 0;
  line-height: 1.2;
}

.badge-verifie-mini {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.driver-rating {
  display: flex;
  align-items: center;
  gap: 4px;
}

.star-icon {
  flex-shrink: 0;
}

.rating-value {
  font-size: 13px;
  font-weight: 700;
  color: #374151;
}

.view-profile-hint {
  font-size: 11px;
  color: #FF4D2D;
  font-weight: 600;
  margin-left: 6px;
  display: none;
}

.chevron-hint {
  color: #FF4D2D;
  display: none;
}

@media (min-width: 480px) {
  .view-profile-hint,
  .chevron-hint {
    display: inline-block;
  }
}

.driver-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  margin-left: 8px;
}

.action-circle-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #F8FAFC;
  border: 1px solid #E5E7EB;
  color: #111627;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
}

.action-circle-btn:hover {
  background: #FFF5F2;
  border-color: #FEE2DE;
  color: #FF4D2D;
  transform: translateY(-1px);
}
</style>
