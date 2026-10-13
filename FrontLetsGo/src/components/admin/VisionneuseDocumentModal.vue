<template>
  <div v-if="ouvert" class="modal-overlay" @click.self="fermer">
    <div class="modal-content-doc">
      <!-- En-tête -->
      <div class="modal-header">
        <div class="header-info">
          <h3 class="modal-title">{{ titre || 'Document de vérification' }}</h3>
          <span class="modal-sub">{{ sousTitre }}</span>
        </div>
        <button class="btn-fermer" @click="fermer" title="Fermer" type="button">
          ✕
        </button>
      </div>

      <!-- Corps : Image avec zoom -->
      <div class="modal-body-doc">
        <div class="image-wrapper" :class="{ 'is-zoomed': zoomed }" @click="toggleZoom">
          <img
            v-if="url"
            :src="url"
            :alt="titre"
            class="doc-image"
          />
          <div v-else class="doc-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <path d="m21 15-5-5L5 21" />
            </svg>
            <p>Aucun document téléversé pour cette section.</p>
          </div>
        </div>
      </div>

      <!-- Pied : Commandes -->
      <div class="modal-footer">
        <div class="footer-left">
          <button v-if="url" @click="toggleZoom" class="btn-action-zoom" type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
              <line :x1="zoomed ? 8 : 11" :y1="11" :x2="zoomed ? 14 : 11" :y2="11" />
              <line v-if="!zoomed" x1="8" y1="11" x2="14" y2="11" />
            </svg>
            <span>{{ zoomed ? 'Dézoomer' : 'Agrandir (Zoom)' }}</span>
          </button>
          <a
            v-if="url"
            :href="url"
            target="_blank"
            download
            class="btn-action-zoom"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            <span>Ouvrir dans un nouvel onglet</span>
          </a>
        </div>
        <button class="btn-fermer-action" @click="fermer" type="button">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  ouvert: {
    type: Boolean,
    default: false,
  },
  url: {
    type: String,
    default: '',
  },
  titre: {
    type: String,
    default: '',
  },
  sousTitre: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['close'])

const zoomed = ref(false)

function toggleZoom() {
  if (props.url) {
    zoomed.value = !zoomed.value
  }
}

function fermer() {
  zoomed.value = false
  emit('close')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.7);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 24px;
  animation: fadeIn 0.2s ease-out;
}

.modal-content-doc {
  background: #ffffff;
  border-radius: 20px;
  width: 100%;
  max-width: 860px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-header {
  padding: 18px 24px;
  border-bottom: 1px solid #edf0f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 17px;
  font-weight: 700;
  color: #111627;
  margin: 0;
}

.modal-sub {
  font-size: 12px;
  color: #8b92a5;
}

.btn-fermer {
  background: #f1f3f7;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #555b6d;
  font-size: 14px;
  transition: all 0.15s ease;
}

.btn-fermer:hover {
  background: #e2e6ee;
  color: #111627;
}

.modal-body-doc {
  flex: 1;
  padding: 20px;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f1422;
  min-height: 400px;
}

.image-wrapper {
  max-width: 100%;
  max-height: 60vh;
  cursor: zoom-in;
  transition: transform 0.2s ease;
  display: flex;
  justify-content: center;
}

.image-wrapper.is-zoomed {
  cursor: zoom-out;
  transform: scale(1.4);
}

.doc-image {
  max-width: 100%;
  max-height: 60vh;
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.doc-empty {
  color: #8b92a5;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.doc-empty svg {
  width: 48px;
  height: 48px;
  opacity: 0.5;
}

.modal-footer {
  padding: 14px 24px;
  border-top: 1px solid #edf0f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fafbfc;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-action-zoom {
  background: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-action-zoom svg {
  width: 15px;
  height: 15px;
}

.btn-action-zoom:hover {
  border-color: #ff4d2d;
  color: #ff4d2d;
}

.btn-fermer-action {
  background: #111627;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
