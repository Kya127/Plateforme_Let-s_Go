<template>
  <article
    class="document-card"
    :class="{ 'document-card--uploaded': uploaded }"
    @click="openFilePicker"
    role="button"
    tabindex="0"
    @keydown.enter="openFilePicker"
    @keydown.space.prevent="openFilePicker"
  >
    <div
      class="document-icon"
      :class="{ 'document-icon--uploaded': uploaded }"
      aria-hidden="true"
    >
      <!-- Permis / QR -->
      <svg
        v-if="icon === 'license'"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <rect x="3" y="4" width="18" height="16" rx="2" />
        <circle cx="8" cy="10" r="2" />
        <path d="M14 9h4M14 13h4M6 16h12" />
      </svg>

      <!-- Carte grise -->
      <svg
        v-else-if="icon === 'carte'"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <circle cx="12" cy="10" r="3" />
        <path d="M7 17c1.5-2 3.5-2.5 5-2.5s3.5.5 5 2.5" />
      </svg>

      <!-- Assurance -->
      <svg
        v-else
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <path d="m9 12 2 2 4-4" />
      </svg>
    </div>

    <div class="document-content">
      <h3>{{ title }}</h3>

      <p
        v-if="uploaded"
        class="document-status document-status--success"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M5 12.5L9.5 17L19 7"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <span>{{ fileName || 'Document prêt' }}</span>
      </p>

      <p
        v-else
        class="document-description"
      >
        {{ description }}
      </p>
    </div>

    <div class="upload-badge" :class="{ 'is-uploaded': uploaded }">
      <svg v-if="uploaded" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>

    <input
      ref="fileInput"
      class="file-input"
      type="file"
      :accept="accept"
      @change="handleFileChange"
    />
  </article>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  title: {
    type: String,
    required: true
  },

  description: {
    type: String,
    required: true
  },

  fileName: {
    type: String,
    default: ''
  },

  icon: {
    type: String,
    default: 'license'
  },

  uploaded: {
    type: Boolean,
    default: false
  },

  accept: {
    type: String,
    default: '.jpg,.jpeg,.png,.pdf'
  }
})

const emit = defineEmits(['upload'])

const fileInput = ref(null)

const openFilePicker = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files?.[0]

  if (!file) return

  emit('upload', file)

  // Permet de sélectionner à nouveau le même fichier si besoin
  event.target.value = ''
}
</script>

<style scoped>
.document-card {
  width: 100%;
  min-height: 72px;
  display: flex;
  align-items: center;
  gap: 16px;

  padding: 16px 18px;

  border: 1.5px solid #edf0f3;
  border-radius: 16px;

  background: #ffffff;

  cursor: pointer;

  box-shadow: none;

  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.document-card:hover {
  border-color: #d1d5db;
}

.document-card:focus-visible {
  outline: 2px solid #ff4d2d;
  outline-offset: 2px;
}

.document-card--uploaded {
  background: #fbfdfc;
  border-color: #86efac;
}

.document-icon {
  flex: 0 0 46px;
  width: 46px;
  height: 46px;

  display: grid;
  place-items: center;

  border-radius: 12px;

  background: #f3f4f6;
  color: #6b7280;
  transition: all 0.2s ease;
}

.document-icon--uploaded {
  background: #ecfdf5;
  color: #10b981;
}

.document-icon svg {
  width: 24px;
  height: 24px;
}

.document-content {
  min-width: 0;
  flex: 1;
}

.document-content h3 {
  margin: 0 0 3px;

  color: #111627;

  font-size: 15px;
  line-height: 1.25;
  font-weight: 700;
  letter-spacing: -0.2px;
}

.document-description,
.document-status {
  margin: 0;

  font-size: 13px;
  line-height: 1.35;
  font-weight: 500;
}

.document-description {
  color: #9ca3af;
}

.document-status--success {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #059669;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-status svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.upload-badge {
  flex: 0 0 32px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #f3f4f6;
  color: #9ca3af;
  transition: all 0.2s ease;
}

.upload-badge svg {
  width: 16px;
  height: 16px;
}

.upload-badge.is-uploaded {
  background: #10b981;
  color: #ffffff;
}

.file-input {
  display: none;
}
</style>