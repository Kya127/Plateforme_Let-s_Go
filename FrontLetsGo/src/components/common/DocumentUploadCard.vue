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
        viewBox="0 0 48 48"
        fill="none"
      >
        <rect x="8" y="8" width="11" height="11" rx="2" fill="currentColor" />
        <rect x="29" y="8" width="11" height="11" rx="2" fill="currentColor" />
        <rect x="8" y="29" width="11" height="11" rx="2" fill="currentColor" />
        <rect x="30" y="30" width="5" height="5" rx="1" fill="currentColor" />
        <rect x="37" y="37" width="4" height="4" rx="1" fill="currentColor" />
        <rect x="29" y="23" width="5" height="5" rx="1" fill="currentColor" />
        <rect x="37" y="23" width="4" height="4" rx="1" fill="currentColor" />
      </svg>

      <!-- Carte grise -->
      <svg
        v-else-if="icon === 'carte'"
        viewBox="0 0 48 48"
        fill="none"
      >
        <circle cx="24" cy="24" r="17" fill="currentColor" />
        <circle cx="24" cy="19" r="6" fill="white" />
        <path
          d="M13 36C15.8 31.9 19.5 30 24 30C28.5 30 32.2 31.9 35 36"
          stroke="white"
          stroke-width="4"
          stroke-linecap="round"
        />
      </svg>

      <!-- Assurance -->
      <svg
        v-else
        viewBox="0 0 48 48"
        fill="none"
      >
        <path
          d="M24 5L38 11V21C38 30.8 32.4 38.5 24 42C15.6 38.5 10 30.8 10 21V11L24 5Z"
          fill="currentColor"
        />
        <path
          d="M24 11V35"
          stroke="white"
          stroke-width="3"
          stroke-linecap="round"
          opacity=".65"
        />
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

        Téléchargé
      </p>

      <p
        v-else
        class="document-description"
      >
        {{ description }}
      </p>
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

  // Permet de sélectionner à nouveau le même fichier
  event.target.value = ''
}
</script>

<style scoped>
.document-card {
  width: 100%;
  min-height: 188px;
  display: flex;
  align-items: center;
  gap: 30px;

  padding: 34px 44px;

  border: 4px solid #f1f2f4;
  border-radius: 50px;

  background: #ffffff;

  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background-color 0.2s ease,
    transform 0.2s ease;
}

.document-card:hover {
  border-color: #e6e8eb;
  transform: translateY(-1px);
}

.document-card:focus-visible {
  outline: 3px solid rgba(255, 77, 45, 0.25);
  outline-offset: 4px;
}

.document-card--uploaded {
  background: #fbfcfd;
  border-color: #e3e6ea;
}

.document-icon {
  flex: 0 0 92px;
  width: 92px;
  height: 92px;

  display: grid;
  place-items: center;

  border-radius: 24px;

  background: #f2f3f5;
  color: #9aa3b2;
}

.document-icon--uploaded {
  background: #ffffff;
  color: #ff4d2d;

  box-shadow: 0 8px 18px rgba(17, 22, 39, 0.04);
}

.document-icon svg {
  width: 48px;
  height: 48px;
}

.document-content {
  min-width: 0;
}

.document-content h3 {
  margin: 0 0 4px;

  color: #111627;

  font-size: 27px;
  line-height: 1.25;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.document-description,
.document-status {
  margin: 0;

  font-size: 23px;
  line-height: 1.35;
  font-weight: 500;
}

.document-description {
  color: #9ca5b5;
}

.document-status--success {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #16c76b;
}

.document-status svg {
  width: 26px;
  height: 26px;
}

.file-input {
  display: none;
}

@media (max-width: 700px) {
  .document-card {
    min-height: 150px;
    padding: 25px;
    gap: 20px;
    border-radius: 32px;
  }

  .document-icon {
    flex-basis: 72px;
    width: 72px;
    height: 72px;
    border-radius: 20px;
  }

  .document-icon svg {
    width: 38px;
    height: 38px;
  }

  .document-content h3 {
    font-size: 20px;
  }

  .document-description,
  .document-status {
    font-size: 17px;
  }
}
</style>