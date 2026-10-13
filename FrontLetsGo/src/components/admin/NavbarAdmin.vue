<template>
  <header class="navbar-admin">
    <!-- Fil d'Ariane / Titre de la page -->
    <div class="breadcrumb-area">
      <nav class="breadcrumb-trail" aria-label="Fil d'Ariane">
        <template v-if="breadcrumbs && breadcrumbs.length">
          <span
            v-for="(item, index) in breadcrumbs"
            :key="index"
            class="breadcrumb-item"
          >
            <router-link
              v-if="item.to && index < breadcrumbs.length - 1"
              :to="item.to"
              class="breadcrumb-link"
            >
              {{ item.label }}
            </router-link>
            <span
              v-else
              class="breadcrumb-current"
              :class="{ 'title-main': index === 0 && breadcrumbs.length === 1 }"
            >
              {{ item.label }}
            </span>
            <span v-if="index < breadcrumbs.length - 1" class="breadcrumb-separator">></span>
          </span>
        </template>
        <template v-else>
          <h1 class="page-title">{{ title || "Vue d'ensemble" }}</h1>
        </template>
      </nav>
    </div>

    <!-- Actions d'en-tête (Recherche globale, notifications, avatar, + Nouveau) -->
    <div class="navbar-actions">
      <!-- Barre de recherche -->
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          v-model="recherche"
          @input="$emit('search', recherche)"
          type="text"
          placeholder="Rechercher..."
          class="search-input"
        />
      </div>

      <!-- Cloche de notification -->
      <button class="btn-icon notif-btn" title="Notifications" type="button" @click="$emit('toggle-notifs')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
        <span v-if="hasNotifs" class="notif-dot"></span>
      </button>

      <!-- Avatar Administrateur en haut à droite (accès direct à Mon profil) -->
      <router-link
        to="/profil"
        class="admin-top-avatar"
        title="Consulter mon profil administrateur"
        aria-label="Mon profil"
      >
        <img :src="adminPhoto" alt="Administrateur" />
      </router-link>

      <!-- Bouton + Nouveau (si affiché) -->
      <button
        v-if="showNouveau"
        @click="$emit('nouveau')"
        class="btn-nouveau"
        type="button"
      >
        <span class="plus-icon">+</span>
        <span>Nouveau</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthentificationStore } from '@/stores/authentification'

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  breadcrumbs: {
    type: Array,
    default: () => [],
  },
  showNouveau: {
    type: Boolean,
    default: true,
  },
  hasNotifs: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['search', 'nouveau', 'toggle-notifs'])

const recherche = ref('')
const storeAuth = useAuthentificationStore()

const adminPhoto = computed(() => {
  return (
    storeAuth.utilisateur?.photoUrl ||
    'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80'
  )
})
</script>

<style scoped>
.navbar-admin {
  height: 72px;
  background-color: #ffffff;
  border-bottom: 1px solid #f0f1f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 30;
  box-sizing: border-box;
}

.breadcrumb-area {
  display: flex;
  align-items: center;
}

.breadcrumb-trail {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.breadcrumb-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb-link {
  color: #717789;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s ease;
}

.breadcrumb-link:hover {
  color: #ff4d2d;
}

.breadcrumb-current {
  color: #111627;
  font-weight: 700;
}

.breadcrumb-separator {
  color: #b0b5c4;
  font-size: 13px;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: #111627;
  margin: 0;
}

.title-main {
  font-size: 20px;
  font-weight: 700;
  color: #111627;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box {
  position: relative;
  width: 240px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 15px;
  height: 15px;
  color: #9aa1b3;
  pointer-events: none;
}

.search-input {
  width: 100%;
  box-sizing: border-box;
  padding: 8px 14px 8px 38px;
  background-color: #f7f8fa;
  border: 1px solid #e7e9ee;
  border-radius: 20px;
  font-size: 13px;
  color: #111627;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  background-color: #ffffff;
  border-color: #ff4d2d;
  box-shadow: 0 0 0 3px rgba(255, 77, 45, 0.1);
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #555b6d;
  position: relative;
  transition: background-color 0.15s ease;
}

.btn-icon:hover {
  background-color: #f4f5f8;
}

.btn-icon svg {
  width: 19px;
  height: 19px;
}

.notif-dot {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 7px;
  height: 7px;
  background-color: #ff4d2d;
  border-radius: 50%;
  border: 1.5px solid #ffffff;
}

.admin-top-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  border: 1.5px solid #e7e9ee;
  cursor: pointer;
}

.admin-top-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-nouveau {
  background-color: #ff4d2d;
  color: #ffffff;
  border: none;
  border-radius: 20px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  box-shadow: none !important;
  transition: all 0.2s ease;
}

.btn-nouveau:hover {
  background-color: #ea3f20;
  transform: translateY(-1px);
  box-shadow: none !important;
}

.btn-nouveau:focus,
.btn-nouveau:active {
  box-shadow: none !important;
}

.plus-icon {
  font-size: 16px;
  line-height: 1;
}
</style>
